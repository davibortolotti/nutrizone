from django.shortcuts import render
from django.conf import settings

import requests

from . import serializer
from .forms import SubmitFood
from .serializer import USDASerializer
from .models import Food, Nutrients


# Create your views here.

def save_food(request):

	if request.method == 'POST':
		form = SubmitFood(request.POST)
		if form.is_valid():

			# serializing data
			ndbno = form.cleaned_data['food']
			r = requests.get('https://api.nal.usda.gov/ndb/reports/?ndbno=' + ndbno + '&type=b&format=json&api_key=' + settings.USDA_KEY)
			json = r.json()
			serializer = USDASerializer(data=json)
			#valid = serializer.is_valid() # DEBUG

			# checks to see if food already exists in database
			try:
				Food.objects.filter(ndbno=ndbno)[0]
			except IndexError:
				if serializer.is_valid(): 
					nutrition = serializer.save()	

			# defining variables to parse food information
			food = Food.objects.all()[0]

			return render(request, 'foods.html', {'food': food})
	else:
		form = SubmitFood()

	return render(request, 'index.html', {'form': form})

def nutrition(request, foodname=None):

	food = Food.objects.filter(name=foodname)[0] # TEMPORARIO
	nutrients = Nutrients.objects.filter(food__name=foodname)
	energy = nutrients.get(name='Energy')
	sugars = nutrients.get(name='Sugars, total')
	fat = nutrients.get(name='Total lipid (fat)')

	context = {
	'food': food, 
	'energy': energy,
	'sugars': sugars,
	'fat': fat
	}


	if(request.GET.get('mybtn')):
		request.session[food.name] = 100
		cart = 'voce adicionou ' + str(request.session.get(food.name))
		context['cart'] = cart
	
	return render(request, 'nutrition.html', context)


