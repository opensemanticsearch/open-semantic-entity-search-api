Open Semantic Entity Search API
===============================

https://opensemanticsearch.org/doc/datamanagement/named_entity_recognition

REST API and Python library for search, recommendation, reconciliation, named entity extraction, named entity linking & named entity disambiguation of named entities like persons, organizations and places for (semi)automatic semantic tagging & analysis of documents by linked data knowledge graph like SKOS thesaurus, Wikidata or RDF ontologies.


Dependencies
============

If you do not want to use the preconfigured Debian packages providing all components out of the box, you have to install the following dependencies:

Dependecies for all components:

Python 3.x


Dependency for dictionary based entity extraction:

Apache Solr 7.x
https://lucene.apache.org/solr/ (preconfigured in Git repository https://github.com/opensemanticsearch/solr.deb)

PySolr

Open Semantic ETL
https://opensemanticsearch.org/etl (Git repository: https://github.com/opensemanticsearch/open-semantic-etl)


Dependencies for import of RDF ontologies and SKOS thesauri:

Solr Ontology Tagger (Git repository: https://github.com/opensemanticsearch/solr-ontology-tagger)


Dependencies for Named Entity Recognition by Machine Learning:

spaCy (Git repository: https://github.com/explosion/spaCy)
spaCy-services (Git repository: https://github.com/explosion/spacy-services)


Web User Interfaces (UI)
========================

Web user interfaces for setup of dictionaries, lists of names, thesauri and ontologies in Django based Open Semantic Search Apps


Dictionary based Named Entity Extraction
========================================

The component dictionary extracts named entities by dictionaries/lists of names


Dictionary matcher
------------------
Apache Lucene/Solr powered dictionary based named entity extaction is done by Dictionary_Matcher in dictionary/matcher.py


Dictionary manager
------------------
For managing dictionaries like lists of names the Dictionary_Manager in dictionary/manager.py is used.
