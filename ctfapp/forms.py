from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML
from crispy_forms.bootstrap import StrictButton, InlineRadios, Field, FieldWithButtons

from ctfapp.validators import validate_unique_username
from ctfapp.util.globals import GENDER_CHOICES, RACE_CHOICES


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())

class ChangePasswordForm(forms.Form):
    password = forms.CharField(label='Current password', max_length=50, widget=forms.PasswordInput())
    new_password = forms.CharField(label='New password', max_length=50, widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm password', max_length=50, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.layout = Layout(
            Fieldset(
                'Change password',
                Field('password', placeholder='Current password'),
                Field('new_password', placeholder='New password'),
                Field('confirm_password', placeholder='Confirm password'),
                StrictButton('Change password', css_class='btn-success', type='button', onclick='change_password();')
            )
        )

class CreateTeamForm(forms.Form):
    name = forms.CharField(label='Team name', max_length=100)
    affiliation = forms.CharField(label='School or affiliation', max_length=50)

    def __init__(self, *args, **kwargs):
        super(CreateTeamForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.layout = Layout(
            Fieldset(
                'Create team',
                Field('name', placeholder='Team name'),
                Field('affiliation', placeholder='School or affiliation'),
                StrictButton('Create team', css_class='btn-success', type='submit')
            )
        )


class JoinTeamForm(forms.Form):
    code = forms.CharField(label='Team code', max_length=100)

    def __init__(self, *args, **kwargs):
        super(JoinTeamForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.layout = Layout(
            Fieldset(
                'Join team',
                HTML(
                    """<span style='color: grey;'>If you want to join a team that already exists,
                    ask somebody already on the team for the team code.  It will be on their account page.</span>
                    <br/><br/>"""),
                FieldWithButtons(Field('code', placeholder='Team code'),
                                 StrictButton('Join team', css_class='btn-success', type='submit'))
            )
        )

class CreateUserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=50, required=True, validators=[validate_unique_username])
    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput(), required=True)
    confirm = forms.CharField(label='Confirm password', max_length=50, widget=forms.PasswordInput(), required=True)
    first_name = forms.CharField(label='First name', max_length=50, required=True)
    last_name = forms.CharField(label='Last name', max_length=50, required=True)
    email = forms.CharField(label='Email', max_length=100, required=True, validators=[EmailValidator()])
    eligible = forms.ChoiceField(label='Eligibility', required=True,
                                         choices=(('Y','High school or middle school student in the US'),
                                                  ('N','Ineligible to compete')))

    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=False)
    race = forms.ChoiceField(choices=RACE_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.initial['eligible'] = 'Y'

        self.helper = FormHelper()

        self.helper.layout = Layout(
            Fieldset(
                'User information',
                Field('username', placeholder='Username'),
                Field('password', placeholder='Password'),
                Field('confirm', placeholder='Confirm password'),
                Field('first_name', placeholder='First name'),
                Field('last_name', placeholder='Last name'),
                Field('email', placeholder='Email'),
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
