#%%
from rdflib import Graph
from io import StringIO
from rdflib import URIRef
from rdflib.namespace import RDF, SKOS

#%%
feelings = Graph()
feelings.add((
    URIRef("http://www.example.com/concepts#love"), # Subject
    RDF.type,
    SKOS.Concept
))
print(feelings.serialize())
