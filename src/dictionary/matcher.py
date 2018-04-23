import requests
import json
import hashlib
import pysolr
from opensemanticetl import export_solr

#
# Extract Named Entities (listed in dictionaries) which occur in text
# by dictionary based named entity extraction
#
# (Dictionaries are managed in Solr dictionaries by manager.py)
#

class Dictionary_Matcher(object):

	solr = 'http://localhost:8983/solr/'
	solr_core = 'core1-dictionary'


	def get_dictionaries(self):
	
		dictionaries = []
		
		url = self.solr + self.solr_core + '/schema/fields'
	
		r = requests.get(url)
	
		data = r.json()
			
		for field in data['fields']:
			if field['type'].startswith('dictionary_matcher_'):
				dictionaries.append(field['name'])
		
		return dictionaries
	
	
	def matches(self, text, dict_ids=None):

		matches = {}

		if not dict_ids:
			dict_ids = self.get_dictionaries()

		hash = hashlib.sha256(text.encode('utf-8'))
		docid = hash.hexdigest()

		solr = export_solr.export_solr(solr = self.solr, core = self.solr_core)

		data = {}
		data['id'] = docid
		data['text_txt'] = text
		
		solr.post(data=data, commit=True)

		headers = {'content-type' : 'application/json'}

		params = {
			'wt': 'json',
			'rows': 0, # we do not need document field results, only the facet
			'facet.limit': -1, # This param indicates the maximum number of constraint counts that should be returned for the facet fields. A negative value means unlimited.
			'facet': 'on',
			'facet.field': dict_ids,
			'fq': 'id:' + docid
		}
		
		r = requests.get(self.solr + self.solr_core + '/select', params=params, headers=headers)
		result = r.json()
		
		for dict_id in dict_ids:
			if dict_id in result['facet_counts']['facet_fields']:
				matches[dict_id] = []
								
				is_value = True
				for value in result['facet_counts']['facet_fields'][dict_id]:
					if is_value:
						matches[dict_id].append(value)
						# next list entry is count
						is_value=False
					else:
						# next list entry is a value
						is_value = True
		
		# delete analyzed and indexed text from dictionary index
		solr = pysolr.Solr(self.solr + self.solr_core)
		result = solr.delete(id=docid)		

		return matches
