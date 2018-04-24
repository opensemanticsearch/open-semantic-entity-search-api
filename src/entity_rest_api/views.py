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


from django.http import JsonResponse
from django.http import HttpResponse
from entity_linking.entity_linker import Entity_Linker
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def reconcile(request):
	queries = None
	if 'queries' in request.GET:
		queries = json.loads(request.GET['queries'])
	elif 'queries' in request.POST:
		queries = json.loads(request.POST['queries'])
		
	text = None
	if 'text' in request.POST:
		text = request.POST['text']
	elif 'text' in request.GET:
		text = request.GET['text']

	if queries or text:

		# link/normalize/disambiguate entities
		entity_linker = Entity_Linker()
		results = entity_linker.entities(queries=queries, text=text)

	else:
	
		# no queries, so just return service metadata		
		results = {
			'name': 'Open Semantic Entity Search API',
		}
	
	# Open Refine uses JSONP callback
	callback = None
	if 'callback' in request.GET:
		callback = request.GET['callback']
	elif 'callback' in request.POST:
		callback = request.POST['callback']

	if callback:
		# JSONP response instead of Jsonresponse
		results = '{}({});'.format( callback, json.dumps(results) )
		return HttpResponse(results, "text/javascript")
	else:
		return JsonResponse(results)
