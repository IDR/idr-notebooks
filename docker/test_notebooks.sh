#!/bin/bash
# Test notebooks with nbval

set -u

echo_green() {
    echo -e "\033[0;32m$@\033[0m"
}

echo_red() {
    echo -e "\033[0;31m$@\033[0m"
}

for var in IDR_HOST IDR_USER IDR_PASSWORD; do
    [ -n "${!var}" ] || {
        echo_red ERROR: $var is not defined
        exit 2
    }
done

errors=0

# Full reproducibility: output of notebook cells should match the saved cells
pytest --nbval \
    notebooks/README.ipynb \
    notebooks/SysgroRoiLength.ipynb \
    notebooks/Using_Jupyter.ipynb \

[ $? -eq 0 ] || {
    echo_red "FAILED! pytest --nbval"
    errors=1
}

# Run without error: don't compare output of cells
# These notebooks should be modified to pass without -lax
pytest --nbval-lax \
    notebooks/CalculateSharpness.ipynb \
    notebooks/GeneNetwork.ipynb \
    notebooks/GenesToPhenotypes.ipynb \
    notebooks/Getting_Started.ipynb \
    notebooks/IDR_API_example_script.ipynb \

# Not yet tested
# pytest.mark.xfail(reason='Takes too long to run')(
#     'notebooks/Figure_1_Sampling_of_Phenotypes.ipynb'),
# pytest.mark.xfail(reason='Intermittent failures')(
#     'notebooks/PCAanalysisOfCharmFeatures.ipynb'),
# pytest.mark.xfail(reason='New notebook, not yet supported')(
#     'notebooks/QueryIDRWithGeneLists.ipynb'),
# pytest.mark.xfail(reason='Intermittent failures')(
#     'notebooks/RohnPhenotypeClustering.ipynb'),
# pytest.mark.xfail(reason='Takes too long to run')(
#     'notebooks/SysgroOverview.ipynb'),
# pytest.mark.xfail(reason='Broken')(
#     'notebooks/SysgroRoiLength.ipynb'),
#



[ $? -eq 0 ] || {
    echo_red "FAILED! pytest --nbval-lax"
    errors=1
}

[ $errors -eq 0 ] && {
    echo_green "PASSED!"
} || {
    echo_red "FAILED!"
    exit 2
}
