FROM imagedata/jupyter-docker:0.10.0
MAINTAINER ome-devel@lists.openmicroscopy.org.uk

# create a python3 environment (for OMERO-PY compatibility)
ADD docker/environment-python3-idr.yml .setup/
RUN conda env update -n python3 -q -f .setup/environment-python3-idr.yml
# && \
#    # Jupyterlab component for bokeh (must match jupyterlab version) \
#    jupyter labextension install jupyterlab_bokeh@^0.6.3

RUN /opt/conda/envs/python3/bin/python -m ipykernel install --user --name python3 --display-name 'IDR Python 3'
COPY --chown=1000:100 docker/logo-32x32.png docker/logo-64x64.png .local/share/jupyter/kernels/python3/

# Clone the source git repo into notebooks
COPY --chown=1000:100 . notebooks
