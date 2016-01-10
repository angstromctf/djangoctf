from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML
from crispy_forms.bootstrap import StrictButton, InlineRadios

from ctfapp.validators import validate_unique_username
from ctfapp.util.globals import GENDER_CHOICES, RACE_CHOICES


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())

class ChangePasswordForm(forms.Form):
    password = forms.CharField(label='Current', max_length=50, widget=forms.PasswordInput())
    new_password = forms.CharField(label='New', max_length=50, widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm', max_length=50, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'

        self.helper.layout = Layout(
            Fieldset(
                'Change password',
                'password',
                'new_password',
                'confirm_password',
                StrictButton('Change password', css_class='btn-success', type='button', onclick='change_password();')
            )
        )

class CreateUserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50, required=True, validators=[validate_unique_username])
    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput(), required=True)
    confirm = forms.CharField(label='Confirm password', max_length=50, widget=forms.PasswordInput(), required=True)
    first_name = forms.CharField(label='First name', max_length=50, required=True)
    last_name = forms.CharField(label='Last name', max_length=50, required=True)
    email = forms.CharField(label='Email', max_length=100, required=True, validators=[EmailValidator()])
    school = forms.CharField(label='School', max_length=100, required=True)
    eligible = forms.ChoiceField(label='Eligibility', required=True,
                                         choices=(('Y','High school or middle school student in the US'),
                                                  ('N','Ineligible to compete')))

    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=False)
    race = forms.ChoiceField(choices=RACE_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.initial['eligible'] = 'Y'

        self.helper = FormHelper()

        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset(
                'User information',
                'username',
                'password',
                'confirm',
                'first_name',
                'last_name',
                'email',
                'school',
                InlineRadios('eligible')
            ),
            Fieldset(
                'Demographics',
                HTML(
                    """<span style='color: grey;'>All information in this section is completely optional.
                    It will be used only for statistical purposes after the CTF is over
                    and will not be disclosed to any other parties for any reason.</span>"""),
                InlineRadios('gender'),
                InlineRadios('race')
            ),
            HTML('<br/>'),
            StrictButton('Sign up!', css_class='btn-success', type='submit')
        )

    def clean(self):
        cleaned_data = super(CreateUserForm, self).clean()

        if cleaned_data.get("password") != cleaned_data.get("confirm"):
            raise ValidationError("Passwords do not match.")
