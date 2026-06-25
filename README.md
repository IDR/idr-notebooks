# idr-notebooks

A set of Python Notebooks to demonstrate how to access the images and metadata from the [Image Data Resource (IDR)](https://idr.openmicroscopy.org), including the features and all of the descriptive tags.

The recommended way to access IDR metadata and images is via the OMERO Web-based API, which doesn't require a login. This primarily consists of the [JSON API](https://omero.readthedocs.io/en/stable/developers/json-api.html)
and the [WebGateway](https://omero.readthedocs.io/en/stable/developers/Web/WebGateway.html).

IDR is currently migrating to the [OME-Zarr](https://ngff.openmicroscopy.org/) image format. Many images have been converted to OME-Zarr, which are hosted on public object storage allowing scalable access
to binary pixel data. Other images that have not yet been converted must be downloaded and read locally to access pixel data.
The [IDR home page](https://idr.openmicroscopy.org/) indicates which studies have been converted to OME-Zarr. Only Images in that are in OME-Zarr format will be viewable in the main image viewer on IDR, and
OME-Zarr Images can also be identified in the IDR webclient by the display of a "Zarr" button above the right panel which will display the Zarr URL (`External Info`).

The OMERO web API can be used to identify OME-Zarr Images by the presence of `External Info` annotation of the image, as described in the `IDR API example script` notebook below.

The notebooks in this repository are meant to exemplify the use of the OMERO web API in the context of the IDR, and the sort of queries that can be done.
In particular, they show how to reproduce Figure 1 and Figure 2 of the paper.<sup>[1](#footnote1)</sup>
They also make use of the [scipy](https://www.scipy.org/) ecosystem, including [pandas](https://pandas.pydata.org).


## Running the notebooks locally

To install the necessary requirements locally, we suggest using conda:

You can for example install Anaconda https://www.anaconda.com/products/individual#Downloads

Create an environment with dependencies:

    $ conda create -n jupyter_idr python=3.12
    $ conda activate jupyter_idr
    $ pip install jupyterlab notebook matplotlib pandas tifffile bokeh

For reading pixel data from OME-Zarrs, we also need: 

    $ pip install zarr aiohttp dask fsspec s3fs

For Figure 2 GeneNetwork notebook, we need:

    $ pip install networkx

Then we can launch with:

    $ jupyter notebook


| **Notebook**                                                               | **Lang** | **Level**     | **Description**                                                                                                                                                                                                                                                                                                                                                                                                    |
|----------------------------------------------------------------------------|----------|---------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **[IDR API example script](IDR_API_example_script.ipynb)**                 | Py       | Intro         | Shows an example of using the web API to extract metadata from the IDR.                                                                                                                                                                                                                                                                                                                                            |
| **[Figure 1 Sample of Phenotypes](Figure_1_Sampling_of_Phenotypes.ipynb)** | Py       | IDR Paper     | Reproduces Fig. 1 of the paper: downloads annotations from all screens and computes and plots some statistics                                                                                                                                                                                                                                                                                                      |
| **[Figure 2: Gene Network](GeneNetwork.ipynb)**                            | Py       | IDR Paper     | Reproduces Fig. 2 of the paper: downloads annotations from 3 screens, with a phenotype in common, queries StringDB for interactions and plots the resulting network. Uses a conversion table for orthologues and gene identifiers which was built offline using biomart (see article for more details). It uses [Bokeh](https://bokeh.pydata.org/) and [NetworkX](https://networkx.github.io/) to display networks.|

----

<a name="footnote1">1</a>: Available on bioRxiv under https://doi.org/10.1101/089359
