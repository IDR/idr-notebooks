"""
Helper functions for accessing the IDR from within IPython notebooks.
"""


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


def connection():
    """
    Connect to the IDR analysis OMERO server
    :return: A BlitzGateway object
    """

    # WARNING: The following block is automatically updated by the IDR
    # deployment scripts. Do not edit this file without testing.
# BEGIN ANSIBLE MANAGED BLOCK
    HOSTNAME = "localhost"
    USERNAME = "omero"
    PASSWORD = "omero"
# END ANSIBLE MANAGED BLOCK

    import omero
    from omero.gateway import BlitzGateway
    c = omero.client(HOSTNAME)
    c.enableKeepAlive(300)
    c.createSession(USERNAME, PASSWORD)
    conn = BlitzGateway(client_obj=c)
    return conn
