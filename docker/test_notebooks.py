import os
import subprocess
import pytest


@pytest.mark.parametrize('notebook', [
    'notebooks/README.ipynb',
    pytest.mark.xfail(reason='Takes too long to run')(
        'notebooks/CalculateSharpness.ipynb'),
    pytest.mark.xfail(reason='Requires R')(
        'notebooks/CondensationBulkAnnotations.R.ipynb'),
    pytest.mark.xfail(reason=(
        'bokeh.charts replaced by bkcharts. '
        'bkcharts is unmaintained and broken '
        'https://stackoverflow.com/a/46287065'))(
        'notebooks/Figure_1_Sampling_of_Phenotypes.ipynb'),
    'notebooks/GeneNetwork.ipynb',
    'notebooks/GenesToPhenotypes.ipynb',
    'notebooks/Getting_Started.ipynb',
    'notebooks/IDR_API_example_script.ipynb',
    pytest.mark.xfail(reason='Intermittent failures')(
        'notebooks/PCAanalysisOfCharmFeatures.ipynb'),
    pytest.mark.xfail(reason='New notebook, not yet supported')(
        'notebooks/QueryIDRWithGeneLists.ipynb'),
    pytest.mark.xfail(reason='Intermittent failures')(
        'notebooks/RohnPhenotypeClustering.ipynb'),
    pytest.mark.xfail(reason='Takes too long to run')(
        'notebooks/SysgroOverview.ipynb'),
    pytest.mark.xfail(reason='Broken')(
        'notebooks/SysgroRoiLength.ipynb'),
    'notebooks/Using_Jupyter.ipynb',
])
def test_notebook(notebook):
    subprocess.check_call([
        'jupyter',
        'nbconvert',
        '--execute',
        '--stdout',
        '--ExecutePreprocessor.timeout=120',
        os.path.join('/home/jovyan', notebook),
    ])
