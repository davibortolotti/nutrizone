from django.shortcuts import render
from django.conf import settings
from decimal import *

import requests

from . import serializer
from .forms import SubmitFood
from .serializer import USDASerializer
from .models import Food, Nutrients

# Create your views here.

def index(request):
	return render(request, 'index.html')

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

			return render(request, 'save_food.html', {'food': food})
	else:
		form = SubmitFood()

	return render(request, 'save_food.html', {'form': form})


###


def foodlist(request):

	foodlist = Food.objects.all()

	return render(request, 'foodlist.html', {'foodlist': foodlist})

def nutrition(request, foodname=None):


	context = {}

	food = Food.objects.filter(name=foodname)[0] # TEMPORARIO
	nutrients = Nutrients.objects.filter(food__name=foodname)

	energy = nutrients.get(name='Energy')
	fat = nutrients.get(name='Total lipid (fat)')

	if nutrients.filter(name='Sugars, total').exists():
		sugars = nutrients.get(name='Sugars, total')
		context['sugars'] = sugars

	context.update({
	'food': food, 
	'energy': energy,
	'fat':fat,
	})



	if(request.POST.get('mybtn')):

		if 'meal' not in request.session.keys(): # checks if there's already a meal in existance
			request.session['meal'] = {} # creates a new meal
		meal = request.session.get('meal', {})
		quantity = float(request.POST.get('quantity'))
		
		if foodname in meal.keys():
			meal[foodname] += quantity
		else:
			meal[foodname] = quantity

		meal_phrase = 'Você adicionou ' + str(int(quantity)) + 'g de ' + foodname.lower() + ' ao seu prato.'

		context['meal_phrase'] = meal_phrase
		request.session['meal'] = meal

	return render(request, 'nutrition.html', context)


###


def meal(request):
	if 'meal' in request.session.keys():
		

		if(request.POST.get('clearbutton')):
			request.session['meal'] = {}
			return render(request, 'meal.html')




		meal = request.session['meal']	
		meal_phrase = {}

		if(request.POST.get('remove')):
			meal.pop(request.POST.get('remove'), None)
			request.session['meal']	= meal

		totalenergy, totalsugars, totalfat = 0, 0, 0

		for foodname in meal:

			quantity = meal[foodname]

			food = Food.objects.filter(name=foodname)[0] # TEMPORARIO
			nutrients = Nutrients.objects.filter(food__name=foodname)
			energy = nutrients.get(name='Energy').value
			fat = nutrients.get(name='Total lipid (fat)').value

			if nutrients.filter(name='Sugars, total').exists():
				sugars = nutrients.get(name='Sugars, total').value
			else: sugars = 0

			getcontext().prec = 3

			phrase = ' (' + str(Decimal(quantity)) + 'g)'
			meal_phrase[foodname] = phrase

            	

			totalenergy += Decimal(energy)*Decimal(quantity)/100
			totalsugars += Decimal(sugars)*Decimal(quantity)/100
			totalfat += Decimal(fat)*Decimal(quantity)/100



		context = {
		'meal_phrase': meal_phrase,
		'totalenergy': totalenergy,
		'totalfat': totalfat,
		'totalsugars': totalsugars,
		}

		return render(request, 'meal.html', context)
	
	else:

		return render(request, 'meal.html')


