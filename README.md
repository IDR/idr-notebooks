
[![Actions Status](https://github.com/IDR/idr-notebooks/workflows/repo2docker/badge.svg)](https://github.com/ome/idr-notebooks/actions)
# idr-notebooks

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/IDR/idr-notebooks/master)

A set of Python Notebooks to demonstrate how to access the images and metadata from the [Image Data Resource (IDR)](https://idr.openmicroscopy.org), including features and all descriptive tags.

Full access to IDR metadata and images is provided through the standard OMERO API, documentation for which can be found [here](https://docs.openmicroscopy.org/latest/omero5.4/developers/index.html), with the Python bindings found specifically [here](https://docs.openmicroscopy.org/latest/omero5.4/developers/Python.html). The notebooks in this repository are meant to exemplify the use of that API in the context of the IDR, and the sort of queries that can be done. In particular, they show how to reproduce Figure 1 and Figure 2 of the paper.<sup>[1](#footnote1)</sup> They also make use of the [scipy](https://www.scipy.org/) ecosystem, including [pandas](https://pandas.pydata.org).

To run the notebooks, you can either [run on mybinder.org](https://mybinder.org/v2/gh/IDR/idr-notebooks/master) or build locally with [repo2docker](https://repo2docker.readthedocs.io/).

To build locally:

 * Install [Docker](https://www.docker.com/) if required
 * Create a virtual environment and install repo2docker from PyPI.
 * Clone this repository
 * Run ``repo2docker``. 
 * Depending on the permissions, you might have to run the command as an admin

```
pip install jupyter-repo2docker
git clone https://github.com/IDR/idr-notebooks.git
cd idr-notebooks
repo2docker .
```

| **Notebook**                                                               | **Lang** | **Level**     | **Description**                                                                                                                                                                                                                                                                                                                                                                                                    |
|----------------------------------------------------------------------------|----------|---------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **[Using Jupyter](Using_Jupyter.ipynb)**                                   | Markdown | Intro         | Getting a login account                                                                                                                                                                                                                                                                                                                                                                                            |
| **[IDR API example script](IDR_API_example_script.ipynb)**                 | Py       | Intro         | Shows an example of using the web API to extract metadata from the IDR. Can also be launched **locally**.                                                                                                                                                                                                                                                                                                          |
| **[Getting Started](Getting_Started.ipynb)**                               | Py       | Intro         | How to connect, some simple data access                                                                                                                                                                                                                                                                                                                                                                            |
| **[Figure 1 Sample of Phenotypes](Figure_1_Sampling_of_Phenotypes.ipynb)** | Py       | IDR Paper     | Reproduces Fig. 1 of the paper: downloads annotations from all screens and computes and plots some statistics                                                                                                                                                                                                                                                                                                      |
| **[Gene Network](GeneNetwork.ipynb)**                                      | Py       | IDR Paper     | Reproduces Fig. 2 of the paper: downloads annotations from 3 screens,with a phenotype in common, queries StringDB for interactions and plots the resulting network. Uses a conversion table for orthologues and gene identifiers which was built offline using biomart (see article for more details). It uses [Bokeh](https://bokeh.pydata.org/) and [NetworkX](https://networkx.github.io/) to display networks. |
| **[PCA analysis of Charm features](PCAanalysisOfCharmFeatures.ipynb)**     | Py       | Study details | Shows how to access the computed CHARM features using OMERO.tables, and performs some analysis on them, showing that single cell information can be accessed from generic tile-based features, without segmentation.                                                                                                                                                                                               |
| **[Rohn Phenotype Clustering](RohnPhenotypeClustering.ipynb)**             | Py       | Study details | Downloads annotations from idr0008-rohn-actinome, and performs some simple phenotypic clustering, building a figure, similar to Fig. 1 of the corresponding paper. Builds a gallery of thumbnails from images of several phenotypes.                                                                                                                                                                               |
| **[Sysgro ROI Length](SysgroRoiLength.ipynb)**                             | Py       | Study details | Loads polygons which are linked to the images of idr0001-graml-sysgro and compares the length of cells labelled with a particular gene such as ASH2 versus the wild type.                                                                                                                                                                                                                                          |
| **[Calculate Sharpness](https://github.com/ome/omero-guide-python/blob/master/notebooks/CalculateSharpnessOneImage.ipynb)**                        | Py       | Example       | Calculates sharpness of images and generates heatmaps.                                                                                                                                                                                                                                                                                                                                                             |

----

<a name="footnote1">1</a>: Available on bioRxiv under https://doi.org/10.1101/089359

<a name="footnote2">2</a>: If you don't yet have [an account](Using_Jupyter.ipynb), notebooks can be viewed under https://github.com/IDR/idr-metadata or more completely under https://nbviewer.jupyter.org/github/idr/idr-notebooks/tree/master/
