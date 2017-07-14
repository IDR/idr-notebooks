"""
Helper functions for accessing the IDR from within IPython notebooks.
"""
from idr import createHTTPsession
import pandas
from pandas import DataFrame
from pandas import read_csv
from pandas import concat

def attributes_by_attributes(conn,
                             name="Gene Symbol",
                             value="ASH2L",
                             ns="openmicroscopy.org/mapr/gene",
                             ns2="openmicroscopy.org/mapr/phenotype",
                             name2=None,
                             sId=None
                             ):

    """
    Return a list of neighbours attributes
    for given case insensitive attribute value. (Uses the python blitz gateway)
    """
    from omero.rtypes import rstring, rlist, unwrap
    from omero.sys import ParametersI

    params = ParametersI()
    params.addString("value", value.lower())
    q = (
        "select distinct new map( mv.value as value) "
        "from Annotation as a "
        "join a.mapValue as mv "
        "where lower(mv.value) = :value {where_claus}"
    )
    where_claus = []
    if name:
        params.addString("name", name)
        where_claus.append("and mv.name = :name")
    q = q.format(**{'where_claus':" ".join(where_claus)})

    values = [v[0]['value'] for v in unwrap(
        conn.getQueryService().projection(q, params))]

    params = ParametersI()
    valuelist = [rstring(unicode(v)) for v in values]
    params.add('values', rlist(valuelist))
    params.addString("ns", ns)
    params.addString("ns2", ns2)

    q = (
        "select distinct new map("
            "mv.name as name, "
            "mv.value as value, "
            "mv2.name as name2, "
            "mv2.value as value2) "
        "from Image as i "
        "join i.annotationLinks as ial "
        "join i.annotationLinks as ial2 "
        "join ial.child as a "
        "join a.mapValue as mv "
        "join ial2.child as a2 "
        "join a2.mapValue as mv2 "
        "where a.ns = :ns and a2.ns = :ns2 "
        "and mv.value in (:values) {where_claus} "
    )
    
    where_claus = []
    if name:
        params.addString("name", name)
        where_claus.append("and mv.name = :name")
    if name2:
        params.addString("name2", name2)
        where_claus.append("and mv2.name = :name2")

    q = q.format(**{'where_claus':" ".join(where_claus)})
    
    if sId != None:
        q = q + ("and i in (select image from WellSample "
            "where well.plate in "
            "(select child from ScreenPlateLink where parent.id = {sId}))")

        screenidList = []
        screenidList.append(str(sId))
        q = q.format(**{'sId':" ".join(screenidList)})
    
    res = {}
    for r in unwrap(conn.getQueryService().projection(q, params)):
        r = r[0]
        try:
            res[(r['name'], r['value'])].append((r['name2'], r['value2']))
        except KeyError:
            res[(r['name'], r['value'])] = [(r['name2'], r['value2'])]
    return res

def annotation_ids_by_field(conn,
                            value="CMPO_0000077",
                            key="Phenotype Term Accession",
                            ns="openmicroscopy.org/mapr/phenotype"):
    """
    Return a list of IDs for map annotations with the given namespace
    that have a key=value pair matching the given parameters.
    """
    from omero.rtypes import unwrap
    from omero.sys import ParametersI
    params = ParametersI()
    params.addString("value", value)
    params.addString("key", key)
    params.addString("ns", ns)
    q = (
        "select a.id from MapAnnotation a join a.mapValue as mv "
        "where a.ns = :ns and mv.name = :key and mv.value = :value"
    )
    return unwrap(conn.getQueryService().projection(q, params))[0]

def get_phenotypes_for_gene(gene_name, screenid=None):
    
    # initial data
    IDR_BASE_URL = "http://idr.openmicroscopy.org"
    INDEX_PAGE = "%s/webclient/?experimenter=-1" % IDR_BASE_URL
    SCREENS_PROJECTS_URL = "{base}/mapr/api/{key}/?value={value}"
    PLATES_URL = "{base}/mapr/api/{key}/plates/?value={value}&id={screen_id}"
    IMAGES_URL = "{base}/mapr/api/{key}/images/?value={value}&node={parent_type}&id={parent_id}"
    ATTRIBUTES_URL = "{base}/webclient/api/annotations/?type=map&image={image_id}"
    MAP_URL = "{base}/webclient/api/annotations/?type=map&{type}={image_id}"
    
    """
    Return a list of phenotype 
    for given case insensitive gene_name. (Uses the json api)
    """
    session = createHTTPsession()
    screenidList = []
    if screenid is not None:
        screenidList.append(screenid)
    else:
        qs = {'base': IDR_BASE_URL, 'key': 'gene', 'value': gene_name}
        url = SCREENS_PROJECTS_URL.format(**qs)
        for s in session.get(url).json()['screens']:
            screenidList.append(s['id'])
            
    uniquelist = []
    uniquelist1 = []
    
    if len(screenidList) == 0:
        phenotypeIdsDataframe = pandas.DataFrame(
            {'Name': uniquelist,
             'Accession': uniquelist1,
             'phenotypeAndScreenId': uniquelist1
            })
        return phenotypeIdsDataframe
    
    for sid in screenidList:
        screen_id = sid
        screenqs = {'base': IDR_BASE_URL, 'key': 'gene', 'value': gene_name, 'screen_id': screen_id}    
        screenurl = PLATES_URL.format(**screenqs)
        phenotypePerScreen = []
        phenotypeIdPerScreen = []
        screenIdForPhenotype = []
        for p in session.get(screenurl).json()['plates']:
            plate_id = p['id']
            imageqs = {'base': IDR_BASE_URL, 'key': 'gene', 'value': gene_name, 'parent_type': 'plate', 'parent_id': plate_id}
            plateurl = IMAGES_URL.format(**imageqs)
            for i in session.get(plateurl).json()['images']:
                image_id = i['id']
                qs = {'base': IDR_BASE_URL, 'type': 'image', 'image_id': image_id}
                url = MAP_URL.format(**qs)
                for a in session.get(url).json()['annotations']:
                    namespace = a['ns']
                    for v in a['values']:
                        key = v[0]
                        value = v[1]
                        if key.startswith('Phenotype Term Name') & key.endswith('Phenotype Term Name'):
                            phenotypePerScreen.append(value)
                        if key.startswith('Phenotype Term Accession') & key.endswith('Phenotype Term Accession'):
                            phenotypeIdPerScreen.append(value)
                            
        uniquelist = uniquelist + list(set(phenotypePerScreen))
        uniquelist1 = uniquelist1 + list(set(phenotypeIdPerScreen))
        uniquelist2 = [screen_id] * len(uniquelist)

        phenotypeIdsDataframe = pandas.DataFrame(
            {'Name': uniquelist,
             'Accession': uniquelist1,
             'phenotypeAndScreenId': uniquelist2
            })
        
    return phenotypeIdsDataframe
