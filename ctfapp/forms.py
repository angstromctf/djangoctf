from django import forms

class SubmitForm(forms.Form):
	flag_guess = forms.CharField(max_length=100)
	problem = forms.IntegerField()