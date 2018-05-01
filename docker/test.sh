#!/bin/sh
# To check that most notebooks can be executed:
#
#    IDR_HOST=<host> -e IDR_USER=<user> -e IDR_PASSWORD=<password> ./test.sh
#
# This will exclude notebooks that take a long time to execute or require
# manual input; you should test these manually in the Jupyter notebook web
# interface.
# See the `pytest.mark.xfail` markers in test_notebooks.py for details.

set -eu
set -x
docker rm -f test-jupyter-docker || true
docker build -t test-jupyter-docker ..
docker run -d --name test-jupyter-docker \
    -e IDR_HOST="$IDR_HOST" \
    -e IDR_USER="$IDR_USER" \
    -e IDR_PASSWORD="$IDR_PASSWORD" \
    test-jupyter-docker
docker cp test_notebooks.py test-jupyter-docker:/
docker exec test-jupyter-docker /opt/conda/envs/python2/bin/pytest /test_notebooks.py
