
[![Actions Status](https://github.com/IDR/idr-notebooks/workflows/repo2docker/badge.svg)](https://github.com/ome/idr-notebooks/actions)
# idr-notebooks

A set of Python Notebooks to demonstrate how to access the images and metadata from the [Image Data Resource (IDR)](https://idr.openmicroscopy.org), including the features and all of the descriptive tags.

Full access to IDR metadata and images is provided through the standard OMERO API, documentation for which can be found [here](https://docs.openmicroscopy.org/latest/omero5.4/developers/index.html), with the Python bindings found specifically [here](https://docs.openmicroscopy.org/latest/omero5.4/developers/Python.html). The notebooks in this repository are meant to exemplify the use of that API in the context of the IDR, and the sort of queries that can be done. In particular, they show how to reproduce Figure 1 and Figure 2 of the paper.<sup>[1](#footnote1)</sup> They also make use of the [scipy](https://www.scipy.org/) ecosystem, including [pandas](https://pandas.pydata.org).


## Running the notebooks

### Running on cloud resources
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/IDR/idr-notebooks/master)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/IDR/idr-notebooks/)

### Running in Docker


Alternatively, if you have Docker installed, you can use the [repo2docker](https://repo2docker.readthedocs.io/en/latest/)
tool to run this repository as a local Docker instance:


    $ git clone https://github.com/IDR/idr-notebooks
    $ cd idr-notebooks
    $ repo2docker .

Then follow the instructions that are printed after the Docker image is built.
Depending on the permissions, you might have to run the command as an admin


### Running locally

Finally, if you would like to install the necessary requirements locally,
we suggest using conda:

You can for example install Anaconda https://www.anaconda.com/products/individual#Downloads

Create an environment:

    $ git clone https://github.com/IDR/idr-notebooks
    $ cd idr-notebooks
    $ conda env create -n idr_env -f binder/environment.yml

and activate the newly created environment:

    $ conda activate idr_env

The following steps are only required if you want to run the notebooks

* If you have Anaconda installed:
  * Start Jupyter from the Anaconda-navigator
  * Select the notebook you wish to run and select the ``Kernel>Change kernel>Python [conda env:idr_env]``
* If Anaconda is not installed:
  * In the environment, install ``jupyter`` e.g. ``pip install jupyter``
  * Add the virtualenv as a jupyter kernel i.e. ``ipython kernel install --name "idr_env" --user``
  * Open jupyter notebook i.e. ``jupyter notebook`` and select the ``idr_env`` kernel or ``[conda env:idr_env]`` according to what is available


An additional benefit of installing the requirements locally is that you
can then use the tools without needing to launch Jupyter itself.


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
| **[Calculate Sharpness](CalculateSharpness.ipynb)**                        | Py       | Example       | Calculates sharpness of images and generates heatmaps.                                                                                                                                                                                                                                                                                                                                                             |

----

<a name="footnote1">1</a>: Available on bioRxiv under https://doi.org/10.1101/089359

<a name="footnote2">2</a>: If you don't yet have [an account](Using_Jupyter.ipynb), notebooks can be viewed under https://github.com/IDR/idr-metadata or more completely under https://nbviewer.jupyter.org/github/idr/idr-notebooks/tree/master/
