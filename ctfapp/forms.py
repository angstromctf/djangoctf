from django import forms


class SubmitForm(forms.Form):
    flag_guess = forms.CharField(max_length=100)
    problem = forms.IntegerField()


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())