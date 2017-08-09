from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from decimal import *

from . import serializer
from .forms import *
from .serializer import USDASerializer
from .models import Food, Nutrient, Measure



import requests
# Create your views here.

def index(request):
	authUser = request.user.is_authenticated
	if authUser:
		user = User.objects.get(username=request.user.username)
		firstname = request.user.first_name
		return render(request, 'index.html', {'authenticated':authUser, 'firstname':firstname})
	return render(request, 'index.html')

def save_food(request):

	if request.method == 'POST':
		form = SubmitFood(request.POST)
		if form.is_valid():

			# serializing data
			ndbno = form.cleaned_data['food'];
			r = requests.get('https://api.nal.usda.gov/ndb/reports/?ndbno=' + ndbno + '&type=b&format=json&api_key=' + settings.USDA_KEY);
			json = r.json();
			serializer = USDASerializer(data=json);

			# checks to see if food already exists in database
			
			try:
				Food.objects.filter(ndbno=ndbno)[0];
				context = {
					"message" : "Alimento já presente no banco de dados",
				}
				return render(request, 'save_food.html', context)
			
			except IndexError: # if not in database

				if serializer.is_valid(): 
					serializer.save(); #saves to database
					request.session['ndbno'] = ndbno
					return rename_food(request)
			
			# defining variables to parse food information
		

				else:
					context = {
						"message" : "error!",
					}
					return render(request, 'save_food.html', context)

	else:
		form = SubmitFood()

	return render(request, 'save_food.html', {'form': form})


def rename_food(request):
	ndbno = request.session.get('ndbno')
	thisfood = Food.objects.filter(ndbno=ndbno)[0]
	food_oldname = thisfood.name
	nutrient = Nutrient.objects.filter(food__name=food_oldname)[0]
	thisfoodmeasures = Measure.objects.filter(nutrient=nutrient)

	if (request.POST.get('rename')):

		rename = RenameFood(request.POST)
		if rename.is_valid():
			thisfood.brname = rename.cleaned_data['rename']
			thisfood.altmeasurename = rename.cleaned_data['renmeasure']
			thisfood.altmeasuregram = request.POST.get('measurevalue')
			thisfood.save();
			Measure.objects.filter(nutrient__food__name=food_oldname).delete()
			context = {
				'done' : 'Alimento adicionado com sucesso',
			}
		return render(request, 'rename_food.html', context)

	else:
		rename = RenameFood()
		context = {
			'rename': rename,
			'oldname': food_oldname,
			'thisfoodmeasures': thisfoodmeasures,
		}
	return render(request, 'rename_food.html', context)


###









def foodlist(request):

	foodList = Food.objects.all()
	for food in foodList:
		food.__setattr__('index', food.brname[0])#first letter of headline
	return render(request, 'foodlist.html', {'foodlist': foodList})

def nutrition(request, foodname=None):


	context = {}

	food = Food.objects.filter(brname=foodname)[0] # TEMPORARIO
	nutrients = Nutrient.objects.filter(food__brname=foodname)

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



	if request.method == "POST":
		quantity = request.POST.get('quantity')

		if 'meal' not in request.session.keys(): # checks if there's already a meal in existance
			request.session['meal'] = {} # creates a new meal
		meal = request.session.get('meal', {})
		quantity = float(request.POST.get('quantity'))
		
		if foodname in meal.keys():
			meal[foodname] += quantity
		else:
			meal[foodname] = quantity
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

			food = Food.objects.filter(brname=foodname)[0] # TEMPORARIO
			nutrients = Nutrient.objects.filter(food__brname=foodname)
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




def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('index')
	else:
	    form = SignUpForm()
	return render(request, 'signup.html', {'form': form})


def logmein(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			login(request, form.get_user())
			return redirect('index')
	else:
	    form = AuthenticationForm()
	return render(request, 'login.html', {'form': form})

def logmeout(request):
	logout(request)
	return redirect('index')