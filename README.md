Open Source REST-API for Named Entity Extraction, Normalization, Reconciliation, Recommendation, Named Entity Disambiguation and Named Entity Linking
=====================================================================================================================================================

https://opensemanticsearch.org/doc/datamanagement/named_entity_recognition

REST API and Python library for search, suggestion, recommendation, normalization, reconciliation, named entity extraction, named entity linking & named entity disambiguation of named entities like persons, organizations and places for (semi)automatic semantic tagging & analysis of documents by linked data knowledge graph like SKOS thesaurus, Wikidata or RDF ontologies, SQL database(s) or spreadsheets like CSV, TSV or Excel table(s).


Usage
=====

After setup of your named entities by ontologies, thesaurus, database(s) or lists of names (see the section web user interfaces) you can call the API with a plain text as parameter to extract and/or recommend Named Entities like persons, organizations or places and link them to your Linked Data Knowledge Graph or the Semantic Web.


Rich document formats
---------------------

For other file formats like PDF documents, Word documents, scanned Documents (needing OCR) and many other file formats you can use Open Semantic ETL tools which uses Apache Tika for text extraction and this Open Semantic Entity Search API for named entity linking to your Linked Data Knowledge Graph and the Semantic Web.


Named Entity Linking, Normalization and Disambiguation
======================================================

Link plain text names/labels to ID/URI and normalize alias or alternate label to preferred label and recommends all found entitites for disambiguation and reconciliation.


Entity Linker, Recommender and Normalizer (Python library)
----------------------------------------------------------

Python and Dictionary Matcher based and Apache Solr search index powered Library Entity_Linker from the library entity_linking for Entity Linking and Normalization.


Entity Linking REST-API (Open Refine Reconciliation Service API standard)
-------------------------------------------------------------------------

The Entity Linker based Named Entity Linking and Normalization REST-API in entity_rest_api provides normalized entities in Open Refine Reconciliation API standard result format (Specification: https://github.com/OpenRefine/OpenRefine/wiki/Reconciliation-Service-API).

So this Open Source software provides an Open Refine Reconciliation Service API for your own SKOS thesaurus, RDF ontologies and Named Entity Lists as an independent service which can run on your own server or laptop, so you have not to send sensitive content data or names to external cloud service and you can independent setup additional / own named entities or names.

Additional to the specified Open Refine Reconciliation API query parameters, you can POST a full text / context additionally or instead of entity queries of yet extracted entities or strucutred data field with entities (which in other Open Refine Reconciliation Service APIs are required), so the context will not only used for disambiguation scoring but entities will be extracted automatically from the text.


Dictionary based Named Entity Extraction
========================================

The component dictionary extracts named entities by dictionaries/lists of names


Dictionary matcher
------------------
Apache Lucene/Solr powered dictionary based named entity extaction is done by Dictionary_Matcher in dictionary/matcher.py


Dictionary manager
------------------
For managing dictionaries like lists of names the Dictionary_Manager in dictionary/manager.py is used.


Web User Interfaces (UI) for metadata management and setup of named entities
============================================================================

Web user interfaces for setup of dictionaries, lists of names, thesauri and ontologies in Django based Open Semantic Search Apps (Git repository: https://github.com/opensemanticsearch/open-semantic-search-apps)


Thesaurus
---------

Web user interface for management of a SKOS thesaurus
https://opensemanticsearch.org/doc/datamanagement/thesaurus


Ontologies Manager
------------------

Web user interface to import RDF ontologies or SPARQL results
https://opensemanticsearch.org/doc/datamanagement/ontologies


Linked Open Data (LOD) like Wikidata
------------------------------------

Import Linked Open Data
https://opensemanticsearch.org/doc/datamanagement/opendata

Example: Import lists of names from Wikidata
https://opensemanticsearch.org/doc/datamanagement/opendata/wikidata


Import named entities from SQL database(s)
------------------------------------------

Until implementation of the SQL database importer command line tool and UI to import named entities from database(s), that are not available as SKOS thesaurus or RDF ontology and can be imported by the other user interfaces, add a dictionary of the labels by Dictionary Manager and index them to the Solr search index using the field name "id" for the ID or URI, "preferred_label_s" for the normalized name / preferred label and "label_ss" or "skos_altLabel_ss" with all aliases or alternate labels/names.


Dependencies
============

If you do not want to use the preconfigured Debian packages providing all components out of the box, you have to install the following dependencies:

Python 3.x

Apache Solr 7.x
https://lucene.apache.org/solr/ (preconfigured in Git repository https://github.com/opensemanticsearch/solr.deb)

PySolr

Open Semantic ETL
https://opensemanticsearch.org/etl (Git repository: https://github.com/opensemanticsearch/open-semantic-etl)

Solr Ontology Tagger (Git repository: https://github.com/opensemanticsearch/solr-ontology-tagger)


Dependencies for Named Entity Recognition of entities by Machine Learning, that are not in ontologies, thesauri, databases or lists:

spaCy (Git repository: https://github.com/explosion/spaCy)

spaCy-services (Git repository: https://github.com/explosion/spacy-services)
