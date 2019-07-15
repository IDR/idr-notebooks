FROM imagedata/jupyter-docker:0.9.2
MAINTAINER ome-devel@lists.openmicroscopy.org.uk

# create a python2 environment (for OMERO-PY compatibility)
ADD docker/environment-python2-idr.yml .setup/
RUN conda env update -n python2 -q -f .setup/environment-python2-idr.yml && \
    # Jupyterlab component for bokeh (must match jupyterlab version) \
    jupyter labextension install jupyterlab_bokeh@^0.6.3

# Don't use this:
# /opt/conda/envs/python2/bin/python -m ipykernel install --user --name python2 --display-name 'IDR Python 2'
# because it doesn't activate conda environment variables
COPY --chown=1000:100 docker/logo-32x32.png docker/logo-64x64.png .local/share/jupyter/kernels/python2/
COPY --chown=1000:100 docker/python2-kernel.json .local/share/jupyter/kernels/python2/kernel.json

# Cell Profiler (add to the Python2 environment)
ADD docker/environment-python2-cellprofiler.yml .setup/
RUN conda env update -n python2 -q -f .setup/environment-python2-cellprofiler.yml
# CellProfiler has to be installed in a separate step because it requires
# the JAVA_HOME environment variable set in the updated environment
ARG CELLPROFILER_VERSION=v3.1.8
RUN bash -c "source activate python2 && pip install git+https://github.com/CellProfiler/CellProfiler.git@$CELLPROFILER_VERSION"

# R-kernel and R-OMERO prerequisites
ADD docker/environment-r-omero.yml .setup/
RUN conda env update -n r-omero -q -f .setup/environment-r-omero.yml && \
    /opt/conda/envs/r-omero/bin/Rscript -e "IRkernel::installspec(displayname='OMERO R')"

USER root
RUN mkdir /opt/romero && \
    fix-permissions /opt/romero
# R requires these two packages at runtime
RUN apt-get install -y -q \
    libxrender1 \
    libsm6
USER $NB_UID

# install rOMERO
ENV _JAVA_OPTIONS="-Xss2560k -Xmx2g"
ARG ROMERO_VERSION=v0.4.2
RUN cd /opt/romero && \
    curl -sf https://raw.githubusercontent.com/ome/rOMERO-gateway/$ROMERO_VERSION/install.R --output install.R && \
    bash -c "source activate r-omero && Rscript install.R --version=$ROMERO_VERSION --quiet"

# Experimental: Install nbval for testing reproducibility of notebooks
RUN conda install nbval

COPY --chown=1000:100 . notebooks
