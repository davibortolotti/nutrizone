from django import forms

class SubmitFood(forms.Form):
	food = forms.CharField(max_length=15)


class RenameFood(forms.Form):
    rename = forms.CharField(max_length=20)
    renmeasure = forms.CharField(max_length=20)