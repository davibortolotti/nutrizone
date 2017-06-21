from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
	url(r'^$', views.save_food),
	url(r'^nutrition/(?P<foodname>.*)/$', views.nutrition)
]