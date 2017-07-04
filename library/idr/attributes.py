"""
Helper functions for accessing the IDR from within IPython notebooks.
"""

def attributes_by_attributes(conn,
                             name="Gene Symbol",
                             value="ASH2L",
                             ns="openmicroscopy.org/mapr/gene",
                             ns2="openmicroscopy.org/mapr/phenotype",
                             name2=None
                             ):

    """
    Return a list of neighbours attributes
    for given case insensitive attribute value.
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
        "and mv.value in (:values) {where_claus}"
    )


    where_claus = []
    if name:
        params.addString("name", name)
        where_claus.append("and mv.name = :name")
    if name2:
        params.addString("name2", name2)
        where_claus.append("and mv2.name = :name2")

    q = q.format(**{'where_claus':" ".join(where_claus)})

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
