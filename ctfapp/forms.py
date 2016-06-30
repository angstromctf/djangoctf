from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from ctfapp.validators import validate_unique_username, validate_unique_team_name, validate_unique_email, validate_zip
from ctfapp.utils.globals import GENDER_CHOICES, RACE_CHOICES, ELIGIBLE_CHOICES
from ctfapp.models import Team

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML
from crispy_forms.bootstrap import StrictButton, InlineRadios, Field, FieldWithButtons
import lob
import json

"""
All of the forms used in the site.
"""

class LoginForm(forms.Form):
    """
    A form for users to login to the site.
    """
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())

class ChangePasswordForm(forms.Form):
    """
    Form to change password
    """
    password = forms.CharField(label='Current password', max_length=50, widget=forms.PasswordInput())
    new_password = forms.CharField(label='New password', max_length=50, widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm password', max_length=50, widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = 'change_password'

        self.helper.layout = Layout(
            Fieldset(
                'Change password',
                Field('password', placeholder='Current password'),
                Field('new_password', placeholder='New password'),
                Field('confirm_password', placeholder='Confirm password'),
                StrictButton('Change password', css_class='btn-success', type='submit')
            )
        )

    def clean_password(self):
        user = authenticate(username=self.user.get_username(), password=self.cleaned_data['password'])

        if not user:
            raise ValidationError('Incorrect password')

        return self.cleaned_data['password']

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()

        if cleaned_data.get('new_password') != cleaned_data.get('confirm_password'):
            raise ValidationError('Passwords do not match')

        return cleaned_data


class CreateTeamForm(forms.Form):
    """
    Form to create a new team
    """
    name = forms.CharField(label='Team name', max_length=100, validators=[validate_unique_team_name])
    affiliation = forms.CharField(label='School or affiliation', max_length=50)

    def __init__(self, *args, **kwargs):
        super(CreateTeamForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = 'create_team'

        self.helper.layout = Layout(
            Fieldset(
                'Create team',
                Field('name', placeholder='Team name'),
                Field('affiliation', placeholder='School or affiliation'),
                StrictButton('Create team', css_class='btn-success', type='submit')
            )
        )

    def clean_name(self):
        return self.cleaned_data['name'].strip()


class JoinTeamForm(forms.Form):
    """
    Form to join a team
    """
    code = forms.CharField(label='Team code', max_length=100)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(JoinTeamForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = 'join_team'

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

    def clean_code(self):
        # Get all teams with the specified team code
        teams = Team.objects.all().filter(code=self.cleaned_data['code'])

        # Throw an error if the team code wasn't found
        if teams.count() != 1:
            raise ValidationError("Team code not found.")

        team = teams[0]

        if team.user_count == 5:
            raise ValidationError("Team is already full.")

        return self.cleaned_data['code']


class CreateUserForm(forms.Form):
    """
    Signup form to create new user.
    """

    username = forms.CharField(label='Username', max_length=50, required=True, validators=[validate_unique_username])
    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput(), required=True)
    confirm = forms.CharField(label='Confirm password', max_length=50, widget=forms.PasswordInput(), required=True)
    first_name = forms.CharField(label='First name', max_length=50, required=True)
    last_name = forms.CharField(label='Last name', max_length=50, required=True)
    email = forms.CharField(label='Email', max_length=100, required=True, validators=[EmailValidator(), validate_unique_email])
    eligible = forms.ChoiceField(label='Eligibility', required=True,
                            choices=((True,'High school or middle school student in the US (see About for more information)'),
                            (False,'Ineligible to compete')))

    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=False)
    race = forms.ChoiceField(choices=RACE_CHOICES, required=False)
    age = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        with open('djangoctf/settings.json') as config_file:
            config = json.loads(config_file.read())
            captcha_enabled = config['signup_captcha']['enabled']
            public_key = config['signup_captcha']['public'] if captcha_enabled else None

            super(CreateUserForm, self).__init__(*args, **kwargs)

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
                    """<span style='color: grey;'>All information here is completely optional, but we'd
                    greatly appreciate it if you filled this section out.
                    It will be used only for statistical purposes after the CTF is over
                    and will not be disclosed to any other parties for any reason.</span><br/><br/><br/>"""),
                InlineRadios('gender'),
                InlineRadios('race'),
                Field('age', placeholder='Age')
            ),
            HTML('<br/>'),
            (HTML('<div class="g-recaptcha" data-sitekey="' + public_key + '"></div>') if captcha_enabled else HTML('')),
            HTML('<br/>'),
            StrictButton('Sign up!', css_class='btn-success', type='submit')
        )

    def clean(self):
        cleaned_data = super(CreateUserForm, self).clean()

        if cleaned_data.get("password") != cleaned_data.get("confirm"):
            raise ValidationError("Passwords do not match.")

class ResetPasswordForm(forms.Form):
    """
    Resets password if it is forgotten.
    """
    email = forms.CharField(label='Email', max_length=100, required=True, validators=[EmailValidator()])

    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Field('email', placeholder='Enter email'),
            HTML('<br/>'),
            StrictButton('Send reset email', css_class='btn-success', type='submit')
        )

class TeamAddressForm(forms.Form):
    street_address = forms.CharField(label='Street Address', max_length=1000, required=True)
    street_address_line_2 = forms.CharField(label='Street Address Line 2', max_length=1000, required=False)
    zip_5 = forms.CharField(label='US 5-digit ZIP', max_length=5, required=True, validators=[validate_zip])
    # eligible = forms.BooleanField(label='All members of my team are US high school students.', required=True)
    eligible2 = forms.ChoiceField(label='All members of my team are US high school students.', choices=ELIGIBLE_CHOICES, required=True)
    city = forms.CharField(label='City', max_length=1000, required=False)
    state = forms.CharField(label='State', max_length=1000, required=False)
    def __init__(self, *args, **kwargs):

        super(TeamAddressForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = 'submit_addr'
        self.helper.layout = Layout(
            Field('street_address', placeholder='123 Main Street'),

            Field('street_address_line_2', placeholder='(Optional)'),

            Field('zip_5', placeholder='ZIP'),
            HTML('<br/>'),
            InlineRadios('eligible2'),
            HTML('<br/>'),
            StrictButton('Submit', css_class='btn-success', type='submit')
        )
    def clean(self):
        cleaned_data = super(TeamAddressForm, self).clean()
        with open('djangoctf/settings.json') as config_file:
            config = json.loads(config_file.read())
            address_verification_enabled = config['lob_address_verification']['enabled']
            address_verification_api_key = config['lob_address_verification'][
                'api_key'] if address_verification_enabled else None

            if address_verification_enabled:
                lob.api_key = address_verification_api_key
                try:
                    print(self)
                    verifiedAddress = lob.Verification.create(
                        address_line1=cleaned_data.get("street_address"),
                        address_line2=cleaned_data.get("street_address_line_2"),
                        address_zip=cleaned_data.get("zip_5"),
                        address_country="US"

                    )


                    cleaned_data['street_address'] = verifiedAddress.address.address_line1
                    cleaned_data['street_address_line_2'] = verifiedAddress.address.address_line2
                    cleaned_data['zip_5'] = cleaned_data.get("zip_5")
                    cleaned_data['city'] = verifiedAddress.address.address_city

                    cleaned_data['state'] = verifiedAddress.address.address_state

                except Exception as e:
                    raise ValidationError("Unable to locate address! Make sure your address is correct. If you "
                                          "continue to have trouble, you can provide your address by email at "
                                          "contact@angstromctf.com.")

            return cleaned_data






