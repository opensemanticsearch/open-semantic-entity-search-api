Open Semantic Entity Search API
===============================

REST API for search, recommendation, reconciliation, named entity extraction, named entity linking & named entity disambiguation of named entities like persons, organizations and places for (semi)automatic semantic tagging & analysis of documents by linked data knowledge graph like SKOS thesaurus, Wikidata or RDF ontologies.

https://opensemanticsearch.org/doc/datamanagement/named_entity_recognition


Dependencies
============

Apache Solr (preconfigured in Git repository solr.deb)
PySolr
Open Semantic ETL


Web User Interfaces (UI)
========================

Web user interfaces for setup of dictionaries, lists of names, thesauri and ontologies in Django based Open Semantic Search Apps


Dictionary based Entity Extaction
=================================

Extracts named entities by dictionaries/lists of names


Dictionary matcher
------------------
Apache Lucene/Solr powered dictionary based named entity extaction is done by Dictionary_Matcher in dictionary/matcher.py


Dictionary manager
------------------
For managing dictionaries like lists of names the Dictionary_Manager in dictionary/manager.py is used.
