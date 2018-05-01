import requests
import json

#
# Management of dictionaries in Solr schema
#

class Dictionary_Manager(object):

	solr = 'http://localhost:8983/solr/'
	solr_core = 'opensemanticsearch-entities'

	def dictionary_exists(self, dict_id):
		
		if solr_is_field(self.solr, self.solr_core, dict_id):
			return True
		else:
			return False


	def create_dictionary(self, dict_id, dict_filename):

		if not self.dictionary_exists(dict_id):
	
			api = self.solr + self.solr_core + '/schema'
			headers = {'content-type' : 'application/json'}

			# add field type for analysis by this dictionary
			data = {
				"add-field-type":
				{
					"name": 'dictionary_matcher_' + dict_id,
					"class": "solr.TextField",
					"sortMissingLast": "true",
					"omitNorms": "true",
					"analyzer":
					{
						"tokenizer":
							{
								"class":"solr.WhitespaceTokenizerFactory",
							},
						"filters":[
							{
								"class": "solr.ShingleFilterFactory",
								"minShingleSize": "2",
								"maxShingleSize": "5",
								"outputUnigramsIfNoShingles": "true"
							},
							{
								"class": "solr.KeepWordFilterFactory",
								"ignoreCase": "true",
								"words": dict_filename
							}
						]
					}
				}
			}
			
			r = requests.post(api, data = json.dumps(data), headers=headers)
			result = r.json()
			if 'errors' in result:
				raise Exception(str(result['errors']))

			# add field of this field type
			data = {

				"add-field":
				{
					"name": dict_id,
					"type": 'dictionary_matcher_' + dict_id,
					"indexed": "true",
					"stored": "false",
					"multiValued": "true"
				}
			}
			
			r = requests.post(api, data = json.dumps(data), headers=headers)
			result = r.json()
			if 'errors' in result:
				raise Exception(str(result['errors']))

			# use all document fields for analysis
			data = {
				"add-copy-field":
				{
					"source": "*",
					"dest": [ dict_id ]
				}
			}

			r = requests.post(api, data = json.dumps(data), headers=headers)
			result = r.json()
			if 'errors' in result:
				raise Exception(str(result['errors']))

#
# Apache Solr field exists?
#

def solr_is_field(solr, solr_core, fieldname):

	url = solr + solr_core + '/schema/fields'

	r = requests.get(url)

	data = r.json()
	
	result = False
	
	for field in data['fields']:
		if field['name'] == fieldname:
			result = True

	return result
