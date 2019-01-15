FROM snoopycrimecop/jupyter-docker:master_merge_daily
MAINTAINER ome-devel@lists.openmicroscopy.org.uk

# create a python2 environment (for OMERO-PY compatibility)
ADD docker/environment-python2-idr.yml .setup/
RUN conda env update -n python2 -q -f .setup/environment-python2-idr.yml && \
    # Jupyterlab component for bokeh (must match jupyterlab version) \
    jupyter labextension install jupyterlab_bokeh@^0.6.3

RUN /opt/conda/envs/python2/bin/python -m ipykernel install --user --name python2 --display-name 'IDR Python 2'
COPY --chown=1000:100 docker/logo-32x32.png docker/logo-64x64.png .local/share/jupyter/kernels/python2/

# Clone the source git repo into notebooks
COPY --chown=1000:100 . notebooks
