import opensemanticetl.export_solr
import os
from dictionary.manager import Dictionary_Manager


#
# Management of entities in Solr index
#

class Entity_Manager(object):

	solr = 'http://localhost:8983/solr/'
	solr_core = 'opensemanticsearch-entities'

	solr_synonyms = 'http://localhost:8983/solr/'
	solr_core_synonyms = 'opensemanticsearch'

	wordlist_configfilename = "/etc/opensemanticsearch/ocr/dictionary.txt"

	verbose = False
	
	connector = opensemanticetl.export_solr.export_solr()
	connector.verbose = verbose
	dictionary_manager = Dictionary_Manager()
	
	
	def add(self, id, preferred_label=None, prefLabels=[], labels=[], types=[], dictionary="skos", facet_dictionary_is_tempfile=False):

		# create dictionary, if not yet exists
		self.dictionary_manager.create_dictionary( dict_id = dictionary )

		dictionary_labels = []

		if preferred_label:
			dictionary_labels.append(preferred_label)
		else:
			if len(pref_Labels):
				preferred_label = pref_Lables[0]
			elif len(labels):
				preferred_label = lables[0]
			else:
				preferred_label = id

		data = {
			'id': id,
			'preferred_label_s': preferred_label,
			'type_ss': types,
		}
		
		data['skos_prefLabel_ss'] = []
		for label in prefLabels:
			if not label in dictionary_labels:
				dictionary_labels.append(label)
			data['skos_prefLabel_ss'].append(label)

		data['label_ss'] = []
		for label in labels:
			if not label in dictionary_labels:
				dictionary_labels.append(label)
			data['label_ss'].append(label)
		
		# post to Solr index of entities for Normalization and Entity Linking
		self.connector.solr = self.solr
		self.connector.core = self.solr_core
		self.connector.post(data=data, commit=True)

		# append to dictionary file for Entity Extraction
		if facet_dictionary_is_tempfile:
			dict_filename = self.dictionary_manager.solr_dictionary_config_path + os.path.sep + 'tmp_' + dictionary + '.txt'
		else:
			dict_filename = self.dictionary_manager.solr_dictionary_config_path + os.path.sep + dictionary + '.txt'
		
		dict_file = open(dict_filename, 'a', encoding="UTF-8")
	
		for label in dictionary_labels:
			dict_file.write(label + "\n")
	
		dict_file.close()
				
		# if synonyms, append to synoynms config file
		if self.solr_core_synonyms and len(dictionary_labels) > 1:
			self.connector.solr = self.solr_synonyms
			self.connector.core = self.solr_core_synonyms

			self.connector.append_synonyms(resourceid='skos', label=dictionary_labels[0], synonyms=dictionary_labels[1:])
	
