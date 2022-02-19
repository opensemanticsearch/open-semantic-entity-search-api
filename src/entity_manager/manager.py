import opensemanticetl.export_solr
import os


#
# Management of entities in Solr index
#

class Entity_Manager(object):

	# Solr host
	solr = 'http://localhost:8983/solr/'
	if os.getenv('OPEN_SEMANTIC_ETL_SOLR'):
		solr = os.getenv('OPEN_SEMANTIC_ETL_SOLR')

	solr_core = 'opensemanticsearch-entities'

	solr_synonyms = solr
	solr_core_synonyms = 'opensemanticsearch'

	wordlist_configfilename = "/etc/opensemanticsearch/ocr/dictionary.txt"

	verbose = False
	
	connector = opensemanticetl.export_solr.export_solr()
	connector.verbose = verbose
	
	
	def add(self, id, preferred_label=None, prefLabels=[], labels=[], types=[], fields={}):

		# all labels
		all_labels = []

		if preferred_label:
			all_labels.append(preferred_label)
		else:
			if len(prefLabels):
				preferred_label = prefLabels[0]
			elif len(labels):
				preferred_label = labels[0]
			else:
				preferred_label = id

		data = {
			'id': id,
			'preferred_label_s': preferred_label,
			'preferred_label_txt': preferred_label,
			'type_ss': types,
		}
		
		data['skos_prefLabel_ss'] = []
		for label in prefLabels:
			if not label in all_labels:
				all_labels.append(label)
			data['skos_prefLabel_ss'].append(label)
		if not len(prefLabels):
			data['skos_prefLabel_ss'] = [preferred_label]
		data['skos_prefLabel_txt'] = data['skos_prefLabel_ss']

		data['label_ss'] = []
		for label in labels:
			if not label in all_labels:
				all_labels.append(label)
			data['label_ss'].append(label)
		data['label_txt'] = data['label_ss']

		data['all_labels_ss'] = all_labels

		# add additional fields, if there
		if fields:
			for field in fields:
				data[field] = fields[field]
		
		# post to Solr index of entities for Normalization and Entity Linking
		self.connector.solr = self.solr
		self.connector.core = self.solr_core
		self.connector.post(data=data, commit=True)
		
		# if synonyms, append to synoynms config file
		if self.solr_core_synonyms and len(all_labels) > 1:
			self.connector.solr = self.solr_synonyms
			self.connector.core = self.solr_core_synonyms

			# map all labels to each other (and to itself) in synonyms dictionary
			synonyms = {}

			for label in all_labels:
				synonyms[label] = []
				for synonym in all_labels:
					synonyms[label].append(synonym)
						
			self.connector.append_synonyms(resourceid='skos', synonyms=synonyms)
	
