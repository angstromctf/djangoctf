from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div

from crispy_forms.bootstrap import StrictButton

from ctfapp.validators import validate_unique_username

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())


class CreateUserForm(forms.Form):
    teamname = forms.CharField(label='Team name', max_length=50, required=True, validators=[validate_unique_username])
    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput(), required=True)
    confirm = forms.CharField(label='Confirm password', max_length=50, widget=forms.PasswordInput(), required=True)
    email = forms.CharField(label='Contact email', max_length=100, required=True, validators=[EmailValidator()])
    school = forms.CharField(label='School', max_length=100, required=True)

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            'teamname',
            'password',
            'confirm',
            'email',
            'school',
            StrictButton('Sign up!', css_class='btn-success', type='submit')
        )

    def clean(self):
        cleaned_data = super(CreateUserForm, self).clean()

        if cleaned_data.get("password") != cleaned_data.get("confirm"):
            raise ValidationError("Passwords do not match.")
