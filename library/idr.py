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


def images_by_phenotype(conn,
                        phenotype="CMPO_0000077"):
    """
    Passes phenotype as the value argument to annotation_ids_by_field
    and loads Image objects which can be used for loading thumbnails, etc.
    """
    ann_ids = annotation_ids_by_field(conn, phenotype)
    return list(conn.getObjectsByAnnotations("Image", ann_ids))



def simple_colocalisation(image):
    """
    Perform a simple comparison of the red and green channels.

    Pearson coefficient described at https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3074624/
    """
    p = image.getPrimaryPixels()

    # get 2D planes and reshape to 1D array
    r = p.getPlane(0,0,0)
    red = r.reshape(r.size)
    g = p.getPlane(0,1,0)
    green = g.reshape(g.size)

    # pearson colocalistion coefficient
    from scipy.stats import pearsonr
    pearsonr(red, green)

    # scatter plot
    import matplotlib.pyplot as plt
    plt.scatter(red, green)
    plt.show()


def configuration_from_url(config_url):
    """
    OMERO binary protocol doesn't support load balancing nor session pinning
    so it has to be done client-side by connecting to a random server/port
    """
    import random
    import requests

    r = requests.get(config_url)
    r.raise_for_status()
    cfgs = r.json()
    cfg = random.choice(cfgs)
    return cfg


def _lookup_parameter(initial, paramname, autocfg, default):
    import os
    if initial is not None:
        return initial
    v = autocfg.get(paramname)
    if v is not None:
        return v
    v = os.getenv('IDR_' + paramname.upper())
    if v is not None:
        return v
    return default


def connection(host=None, user=None, password=None, port=None):
    """
    Connect to the IDR analysis OMERO server
    Lookup of connection parameters is done in this order:
    1. Parameters passed as arguments to this method
    2. Parameters obtained from IDR_OMERO_CONFIGURATION_URL
    3. Parameters obtained from IDR_{HOST,PORT,USER,PASSWORD}
    4. Built-in defaults

    :return: A BlitzGateway object
    """
    import os
    import sys

    autocfg = {}
    config_url = os.getenv('IDR_OMERO_CONFIGURATION_URL')
    if config_url:
        try:
            autocfg = configuration_from_url(config_url)
        except Exception as e:
            print >> sys.stderr, 'Failed to fetch configuration: %r' % e

    host = _lookup_parameter(host, 'host', autocfg, 'localhost')
    port = _lookup_parameter(port, 'port', autocfg, 4064)
    user = _lookup_parameter(user, 'user', autocfg, 'omero')
    password = _lookup_parameter(password, 'password', autocfg, 'omero')


    import omero
    from omero.gateway import BlitzGateway
    c = omero.client(host, int(port))
    c.enableKeepAlive(300)
    c.createSession(user, password)
    conn = BlitzGateway(client_obj=c)

    # You are now logged in. In order to guarantee
    # that the connection is closed if a notebook
    # does not complete, we are installing a handler
    # below. This is ONLY for use in a notebook

    # http://stackoverflow.com/questions/40110540/jupyter-magic-to-handle-notebook-exceptions
    def custom_exc(shell, etype, evalue, tb, tb_offset=None):
        print "Closing IDR connection..."
        c.__del__()
        shell.showtraceback((etype, evalue, tb), tb_offset=tb_offset)
    print "Connected to IDR..."
    get_ipython().set_custom_exc((Exception,), custom_exc)
    
    return conn
