"""
Helper functions for accessing the IDR from within IPython notebooks.
"""
import requests
    
def connection(host=None, user=None, password=None, port=4064):
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

    if host is None:
        host = HOSTNAME
    if user is None:
        user = USERNAME
    if password is None:
        password = PASSWORD

    import omero
    from omero.gateway import BlitzGateway
    c = omero.client(host)
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

def createHTTPsession():
    
    """
    Create and return http session
    """
    IDR_BASE_URL = "http://idr.openmicroscopy.org"
    INDEX_PAGE = "%s/webclient/?experimenter=-1" % IDR_BASE_URL
    
    # create http session
    with requests.Session() as session:
        request = requests.Request('GET', INDEX_PAGE)
        prepped = session.prepare_request(request)
        response = session.send(prepped)
        if response.status_code != 200:
            response.raise_for_status()
            
    return session