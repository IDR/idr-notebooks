"""
Helper functions for accessing the data from other databases from within IPython notebooks.
"""
import requests
import pandas
from io import StringIO
from pandas import DataFrame
from pandas import read_csv
from pandas import concat
import numpy as np

def genes_of_interest_fromGO(goTerm):
    url = 'http://www.ebi.ac.uk/QuickGO/GAnnotation?tax=9606&relType=IP&goid=%20' + goTerm + '%20&format=tsv'
    Res = requests.get(url)
    df = read_csv(StringIO(Res.text), sep='\t', header=None)
    c1 = df.ix[:,3]
    return np.unique(c1.values.ravel())

def genes_of_interest_fromString(gene_names, noOfInteractingPartners):
    url = 'http://string-db.org/api/psi-mi-tab/interactions?identifier='
    for g in gene_names:
        url = url + g + '%0D'
    url = url + '&limit=' + str(noOfInteractingPartners) + '&network_flavor=evidence'
    Res = requests.get(url)
    df = read_csv(StringIO(Res.text), sep='\t', header=None)
    c1 = df.ix[:,2:3]
    return np.unique(c1.values.ravel())

def network_of_interest(gene_names, noOfInteractingPartners):
    imageurl = 'http://string-db.org/api/image/network?identifier='
    for g in gene_names:
        imageurl = imageurl + g  # This doesn't look like it will work
    
    imageurl = imageurl + '&limit=' + str(noOfInteractingPartners) + '&network_flavor=evidence'
    return Image(url=imageurl)

def get_entrezid(gene):
    """
    Use mygene.info api to convert gene_symbols to entrezgeneIds (gets ortholog ids as well)
    
    Note : This returns entrez ids for the gene in all organisms
    (Could consider taxonomy related entrez ids : if need be!) documentation for api:
    
      http://mygene.info/v3/api/#MyGene.info-gene-query-service-GET-Gene-query-service

    Maybe : Could make the search with a taxonomy id as well, to restrict it finding ids
    within a certain organism alone?
    """
    entrezurl = "http://mygene.info/v3/query?q="
    entrezurl = entrezurl+gene
    
    res = requests.get(entrezurl)
    results = pandas.read_json(StringIO(res.text))
    
    entrezid = []
    if results.empty:
        return entrezid

    for i in results.ix[:,0]:
        key = i.keys()
        value = i.values()
        for cntr,k in enumerate(key):
            if k == 'entrezgene':
                entrezid.append(value[cntr])
                return entrezid
            
def get_ensembleid(gene):
    
    ensembleserver = "http://rest.ensembl.org/xrefs/symbol/homo_sapiens/"
    url = ensembleserver + gene + "?content-type=application/json"
    
    res = requests.get(url)
    results = pandas.read_json(StringIO(res.text))
    
    ensembleid = []
    if results.empty:
        return ensembleid
    
    for i in results.ix[:,0]:
        ensembleid.append(i)
    return ensembleid