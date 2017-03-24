# idr-notebooks

A set of Python Notebooks to demonstrate how to access the images and metadata from the Image Data Repository (IDR, http://imagedata.science), including features and all descriptive tags. 

Full access to IDR metadata and images is provided through the standard OMERO API, documentation for which can be found [here](https://www.openmicroscopy.org/site/support/omero5.2/developers/), with the Python bindings found specifically [here](https://www.openmicroscopy.org/site/support/omero5.2/developers/Python.html). The notebooks in this repository are meant to exemplify the use of that API in the context of the IDR, and the sort of queries that can be done. In particular, they show how to reproduce Figure 1 and Figure 2 of the paper. They also make use of the [scipy](https://www.scipy.org/) ecosystem, including [pandas](pandas.pydata.org).

## Available notebooks:

- **Getting_Started.ipynb**: How to connect, some simple data access
- **Figure_1_Sampling_of_Phenotypes.ipynb**: Reproduces Fig. 1 of the paper: downloads annotations from all screens and computes and plots some statistics on phenotypes. Interative visualization is done using [bokeh](bokeh.pydata.org/)
- **GeneNetwork.ipynb**: Reproduces Fig. 2 of the paper: downloads annotations from 3 screens with a phenotype in common, queries StringDB for interactions and plots the resulting network. Uses a conversion table for orthologues and gene identifiers which was built offline using biomart (see article for more details.). It uses [bokeh](bokeh.pydata.org/) and py2cytoscape to display networks.
- **RohnPhenotypeClustering.ipynb**: Downloads annotations from IDR008, and performs some simple phenotypic clustering, building a figure similar to Fig. 1 of the corresponding paper. Builds a gallery of thumbnails from images of several phenotypes.
- **PCAanalysisOfCharmFeatures.ipynb**: Shows how to access the computed CHARM features using OMERO.tables and performs some analysis on them, showing that single cell information can be accessed from generic tile-based features without segmentation.
- **IDR_API_example_script.ipynb**: Shows an example of using the web API to extract metadata from the IDR.

