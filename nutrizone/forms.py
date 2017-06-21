from django import forms

class SubmitFood(forms.Form):
	food = forms.CharField(max_length=15)