from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^save_food$', views.save_food),
	url(r'^nutrition/(?P<foodname>.*)/$', views.nutrition),
	url(r'^meal$', views.meal, name='meal'),
	url(r'^alimentos$', views.foodlist, name='foodlist'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)