FROM imagedata/jupyter-docker:0.8.0
MAINTAINER ome-devel@lists.openmicroscopy.org.uk

# create a python2 environment (for OMERO-PY compatibility)
ADD docker/environment-python2-idr.yml .setup/
RUN conda env update -n python2 -f .setup/environment-python2-idr.yml

RUN /opt/conda/envs/python2/bin/python -m ipykernel install --user --name python2 --display-name 'IDR Python 2'
ADD docker/logo-32x32.png docker/logo-64x64.png .local/share/jupyter/kernels/python2/

RUN git clone -b jupyter-0.8 https://github.com/manics/idr-notebooks notebooks
