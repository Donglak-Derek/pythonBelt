from django.conf.urls import url
from . import views   
urlpatterns = [
	url(r'^main$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^travels$', views.travels),
	url(r'^travels/add$', views.addtrip),
	url(r'^add$', views.add),
	url(r'^join/(?P<id>\d+)$', views.join),
	url(r'^unjoin/(?P<id>\d+)$', views.unjoin),
	url(r'^view/(?P<id>\d+)$', views.viewpage),
	url(r'^logout$', views.logout)
	# url(r'^delete$', views.deleteuser),
]