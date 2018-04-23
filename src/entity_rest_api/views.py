#
# Django App / REST-API for linking, normalization, disambiguation and recommendation of named entities like persons, organizations or places
#

# Named Entity Linking, Disambiguation and Normalization by Named Entities in Solr search index
#
# Links plain text names/labels to ID/URI and normalize alias or alternate label to preferred label
#
# Queries are entity names as strings and/or plain text from which named entities will be extracted and can be scored by the context.
# Specification: https://github.com/OpenRefine/OpenRefine/wiki/Reconciliation-Service-API#query-request
#
# If no entity queries the entities will be extracted from the (con)text
#
# Returns Named Entities in Open Refine Reconciliation Service result format
# Specification: https://github.com/OpenRefine/OpenRefine/wiki/Reconciliation-Service-API#query-response


import json
from django.http import HttpResponse
from entity_linking.entity_linker import Entity_Linker


def reconcile(request):

	queries = None
	if 'queries' in request.GET:
		queries = request.GET['queries']
	elif 'queries' in request.POST:
		queries = request.POST['queries']

	text = None
	if 'text' in request.POST:
		text = request.POST['text']
	elif 'text' in request.GET:
		text = request.GET['text']

	# link/normalize/disambiguate entities
	entity_linker = Entity_Linker()
	results = entity_linker.entities(queries=queries, text=text)

	return HttpResponse(json.dumps( results ), content_type="application/json")
