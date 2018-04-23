from django.conf.urls import url

from entity_rest_api import views

urlpatterns = [
	url(r'^reconcile', views.reconcile, name='reconcile'),
]
