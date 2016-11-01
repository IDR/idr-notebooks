# idr-notebooks

A set of Python Notebooks to demonstrate how to access the images and metadata from the Image Data Repository (IDR, http://imagedata.science), including features and all descriptive tags. 

Full access to IDR metadata and images is provided through the standard OMERO API, whose full documentation can be found at (...). The notebooks in this repository are meant to examplify the use of that API in the context of the IDR, and of the sort of query that can be done. In particular, they show how to reproduce Figure 1b and Figure 2 of the paper.

**Available notebooks:**

- Getting_Started.ipynb: How to connect, some simple data access
- fig1b.ipynb: Reproducing fig. 1b of the paper: Download annotations from all screens and compute and plot some statistics on phenotypes
- GeneNetwork.ipynb: Reproduce fig. 2 of the paper: download annotations from 3 screens with a phenotype in common, query StrinDB for interactions and plot the resulting network. Uses a conversion table for orthologues and gene identifier which was built off line using biomart (see article for more details.) 
- RohnPhenotypeClustering.ipynb: Download annotations from IDR008, and perform some simple phenotypic clusering, building a figure similar to Fig. 1 of the corresponding paper. Built a galery of thumbnails from images of several phenotypes.
- CondensationPCAanalysis.ipynb: Shows how to access the computed CHARM features using OMERO.table and perform some analysis on them, showing that single cell informtion can be accessed from generic tile-based features without segmentation.

