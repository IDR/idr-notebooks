# idr-notebooks

A set of Python Notebooks to demonstrate how to access the images and metadata from the Image Data Repository (IDR, http://imagedata.science), including features and all descriptive tags. 

Full access to IDR metadata and images is provided through the standard OMERO API, whose full documentation can be found [here](https://www.openmicroscopy.org/site/support/omero5.2/developers/), with the python bindings found specifically [here](https://www.openmicroscopy.org/site/support/omero5.2/developers/Python.html). The notebooks in this repository are meant to examplify the use of that API in the context of the IDR, and of the sort of query that can be done. In particular, they show how to reproduce Figure 1b and Figure 2 of the paper. They also make use of the [scipy](https://www.scipy.org/) ecosystem, including [pandas](pandas.pydata.org)

## Available notebooks:

- **Getting_Started.ipynb**s: How to connect, some simple data access
- **Figure_1_Sampling_of_Phenotypes.ipynb**: Reproduces fig. 1 of the paper: Download annotations from all screens and compute and plot some statistics on phenotypes. Interative visualisation is done using [bokeh](bokeh.pydata.org/)
- **GeneNetwork.ipynb**: Reproduces fig. 2 of the paper: download annotations from 3 screens with a phenotype in common, query StrinDB for interactions and plot the resulting network. Uses a conversion table for orthologues and gene identifiers which was built off line using biomart (see article for more details.). It uses [bokeh](bokeh.pydata.org/) and py2cytoscape to display networks.
- **RohnPhenotypeClustering.ipynb**: Downloads annotations from IDR008, and perform some simple phenotypic clustering, building a figure similar to Fig. 1 of the corresponding paper. Builds a galery of thumbnails from images of several phenotypes.
- **PCAanalysisOfCharmFeatures.ipynb**: Shows how to access the computed CHARM features using OMERO.table and perform some analysis on them, showing that single cell information can be accessed from generic tile-based features without segmentation.
- **IDR_API_example_script.ipynb**: Shows example of using the web API to extract metadata from the IDR.

