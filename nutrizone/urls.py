from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^save_food$', views.save_food, name="save_food"),
    url(r'^rename_food$', views.rename_food, name='rename_food'),
	url(r'^nutrition/(?P<foodname>.*)/$', views.nutrition),
	url(r'^meal$', views.meal, name='meal'),
    url(r'^mymeal$', views.mymeal, name='mymeal'),
    url(r'^mymeallist$', views.mymeallist, name='mymeallist'),
    url(r'^mymeallist/(?P<mealname>.*)$', views.mymeal, name='mymeal'),
	url(r'^alimentos$', views.foodlist, name='foodlist'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^logmeout$', views.logmeout, name='logmeout'),
    url(r'^logmein$', views.logmein, name='logmein'),
    url(r'^account$', views.accountinfo, name='account'),



]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)