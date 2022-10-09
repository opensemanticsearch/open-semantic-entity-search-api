Open Source REST-API for Named Entity Extraction, Normalization, Reconciliation, Recommendation, Named Entity Disambiguation and Named Entity Linking
=====================================================================================================================================================

https://opensemanticsearch.org/doc/datamanagement/named_entity_recognition

REST API and Python library for search, suggestion, recommendation, normalization, reconciliation, named entity extraction, named entity linking & named entity disambiguation of named entities like persons, organizations and places for (semi)automatic semantic tagging, analysis & semantic enrichment of documents by linked data knowledge graph like SKOS thesaurus, Wikidata or RDF ontologies, SQL database(s) or spreadsheets like CSV, TSV or Excel table(s).


Open Source and Open Standards
==============================

By integration of Open Standards for structured data formats ([SKOS](https://www.w3.org/TR/skos-primer/), RDF, JSON) and REST APIs (HTTP, REST) and entity linking/disambiguation/reconciliation ([Open Refine Reconciliation Service API specs](https://reconciliation-api.github.io/specs/latest/)) and Open Source tools for natural language processing and text analytics this Free Software provides an Open Refine Reconciliation Service API (extended with automatic entity extraction, so you can post a full text instead of entity queries) for your own SKOS thesaurus, RDF ontologies and lists of names from lists, spreadsheets or databases as an independent service which can run on your own server or laptop, so you have not to send sensitive content data or names to external cloud service, and you can independent setup additional / own named entities or names.


Usage
=====

After configuration (see section "Web User Interfaces (UI) for configuration and management of named entities") of your named entities from ontologies, thesaurus, database(s) or lists of names (see section "Import entities") you can call the REST API with a plain text / full-text (or even document files like PDF or Word, see section "Rich document formats") as parameter (see section "REST API request parameters") to extract and/or recommend Named Entities like persons, organizations or places and link them (see section "JSON response") in/to your Linked Data Knowledge Graph Database, Linked Open Data and Semantic Web or as facets for faceted search or navigation by Solr or Elastic Search.


Named Entity Linking, Normalization and Disambiguation
======================================================

Links plain text names/labels to ID/URI and normalizes alias or alternate label to preferred label and recommends all found entities for disambiguation and reconciliation.


REST-API (Open Refine Reconciliation Service API standard)
----------------------------------------------------------

The Entity Linker based Named Entity Linking and Normalization REST-API in entity_rest_api provides normalized entities in Open Refine Reconciliation API standard result format (Specification: https://reconciliation-api.github.io/specs/latest/).


Named Entity Extraction from full-text
--------------------------------------

Additional to the specified Open Refine Reconciliation API query parameters, you can POST a full text / context additionally or instead of entity queries of yet extracted entities or structured data field with entities (which in other Open Refine Reconciliation Service APIs are required), so the context will not only be used for disambiguation scoring but entities will be extracted automatically from the text.


REST-API request parameters
---------------------------

### Extract entities from full text

Automatic named entity extraction of all known/imported entities / names / labels (extension only in Open Semantic Entity Search API, not Open Refine Reconciliation Service API query standard / not supported by other Open Refine Reconciliation Services / APIs):

HTTP POST a plain text as parameter "text" to http://localhost/search-apps/entity_rest_api/reconcile so all known entities will be extracted automatically.

Example for posting a full text to the REST-API by Python requests:

```
import requests

text = "Mr. Jon Doe lives in Berlin."

openrefine_server = 'http://localhost/search-apps/entity_rest_api/reconcile'

params = {'text': text}
r = requests.post(openrefine_server, params=params)

results = r.json()
print(results)
```


### Query for IDs and normalized data of your entity labels (Open Refine Reconciliation Service API query standard)

Query for entities (structured by Open Refine Reconciliation Service API query standard specified in https://github.com/OpenRefine/OpenRefine/wiki/Reconciliation-Service-API#query-request):

```
http://localhost/search-apps/entity_rest_api/reconcile?queries={ "q0" : { "query" : "Jon Doe" }, "q1" : { "query" : "Berlin" } }
```
Optionally you can HTTP POST a context as parameter "text" like in the example before to provide more context to improve scoring of disambiguation (scoring of ambiguous entities by context not implemented yet).


JSON response
-------------

In both cases the response (structured by Open Refine Reconciliation Service API response standard specified in https://github.com/OpenRefine/OpenRefine/wiki/Reconciliation-Service-API#query-response) is a JSON literal object with the same keys as in the request

```
{
	"q0" : {
		"result" : { ... }
	},
	"q1" : {
		"result" : { ... }
	}
}
```

Each result consists of a JSON literal object with the structure

```
{
	"result" : [
		{
			"id" : ... string, URI or database ID ...
			"name" : ... string ...
			"type" : ... array of strings ...
			"score" : ... double ...
			"match" : ... boolean, true if the service is quite confident about the match ...
		},
		... more results ...
	]
}
```


Entity Linker, Recommender and Normalizer (Python library)
----------------------------------------------------------

The REST-API uses the Python and Dictionary Matcher based and Apache Solr search index powered module Entity_Linker from the library entity_linking for Entity Linking and Normalization.

Example:

```
from entity_linking.entity_linker import Entity_Linker

linker = Entity_Linker()

# extract and normalize/link all known entities/names/labels
results = linker.entities( text = "Mr. Jon Doe lives in Berlin." )
print (results)

# normalize/link only the queried entities
results = linker.entities( queries = { 'q1': {'query': 'Berlin'}, 'q2': { 'query': 'Jon Doe' } } )
print (results)

```


Dictionary based Named Entity Extraction
========================================

For extraction of named entities from full-text the Entity Linker extracts named entities by dictionaries / lists of names / labels stored in the Solr index / core for named entities.


Dictionary matcher (FST)
------------------------

Apache Lucene/Solr powered dictionary based named entity extraction of indexed names and labels in the full text is done by Solr Text Tagger https://lucene.apache.org/solr/guide/7_4/the-tagger-handler.html by Finite State Transducer (FST) algorithm.


Import named entities
=====================

Entity Manager (Python API)
---------------------------

To add a named entity to the entities index and dictionary use the method add() with the parameter "id" for the unique ID, URI or URL, "preferred_label" for the normalized name / preferred label and "prefLabels" (higher score) and/or "labels" with all aliases or alternate labels/names.

```
from entity_manager.manager import Entity_Manager

entity_manager = Entity_Manager()
    
entity_manager.add( id = "https://entities/1", types=['Person'], preferred_label = "Jon Doe", prefLabels = ["Jon Doe"], labels = ["J. Doe", "Doe, Jon", "Doe, J."] )
```


Web User Interfaces (UI) for configuration and management of named entities
---------------------------------------------------------------------------

Web user interfaces for setup/configuration of dictionaries, lists of names, thesauri and ontologies in Django based Open Semantic Search Apps (Git repository: https://github.com/opensemanticsearch/open-semantic-search-apps):


Thesaurus (SKOS)
----------------

Web user interface for management of a SKOS thesaurus
https://opensemanticsearch.org/doc/datamanagement/thesaurus


Ontologies (RDF)
----------------

Ontologies Manager is a web user interface to import RDF ontologies or SPARQL results
https://opensemanticsearch.org/doc/datamanagement/ontologies


Linked Open Data (LOD) like Wikidata
------------------------------------

Import Linked Open Data
https://opensemanticsearch.org/doc/datamanagement/opendata

Example: Import lists of names from Wikidata
https://opensemanticsearch.org/doc/datamanagement/opendata/wikidata


Import named entities from SQL database(s)
------------------------------------------

Until implementation of the SQL database importer command line tool and UI to import named entities from database(s), that are not available as SKOS thesaurus or RDF ontology and can be imported by the other user interfaces, 
use the module Entity Manager.


Import named entities from lists / plain text files
---------------------------------------------------

How to import lists of names from plain text files with one name per line:


Web User Interface:

The web user interface Ontologies Manager can not only import RDF ontologies, but also lists of names from plain text files
https://opensemanticsearch.org/doc/datamanagement/ontologies

Data format (Example: politicians.txt):
```
Barack Obama
Vladimir Putin
Angela Merkel
```

Command line tool:

```
entity_import_list.py politicians.txt --type Politician
```

Python:

```
from entity_import.entity_import_list import Entity_Importer_List

list_importer = Entity_Importer_List()

list_importer.import_entities(filename="polititians.txt", types=['Person','Politician'])
```


Rich document formats
=====================

For named entity recognition, named entity extraction and named entity linking and disambiguation of entities from other file formats like PDF documents, Word documents, scanned Documents (needing OCR) and many other file formats you can use Open Semantic ETL tools and user interfaces for crawling filesystems, using Apache Tika for text extraction, Tesseract for OCR and many other Open Source tools for data enrichment and analysis and calling this Open Semantic Entity Search API for named entity extraction and named entity linking to your Linked Data Knowledge Graph and the Semantic Web.


Dependencies
============

If you do not want to use the preconfigured Debian packages providing all components out of the box, you have to install the following dependencies:

Python 3.x

Apache Solr (>= 7.4)
https://lucene.apache.org/solr/ (preconfigured Solr core / schema in this Git repository in /src/solr)

Open Semantic ETL
https://opensemanticsearch.org/etl (Git repository: https://github.com/opensemanticsearch/open-semantic-etl)

Solr Ontology Tagger (Git repository: https://github.com/opensemanticsearch/solr-ontology-tagger)

