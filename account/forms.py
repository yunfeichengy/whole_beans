from django import forms
from django.core.exceptions import ValidationError


def validate_email(value):
    if value.endswith('@hotmail.com') or value.endswith('@gmail.com') or value.endswith('@yahoo.com') or value.endswith('@yahoo.ca'):
        return
    else:
        raise ValidationError(
            # error message to print
            'Invalid email. This website requires hotmail, gmail, or yahoo email accounts.',
            # code so that we can override it if we want
            code='invalid_email'
        )


def validate_uname_login(value):
    if value.endswith('@hotmail.com') or value.endswith('@gmail.com') or value.endswith('@yahoo.com') or value.endswith('@yahoo.ca'):
        raise ValidationError(
            'Please use your username instead of email to login.',
            code='invalid_uname'
        )


class SignupForm(forms.Form):

    # USERNAME
    username = forms.CharField(
        max_length=20,
        min_length=4,
        error_messages={'required': 'Please enter a username.',
                        'max_length': 'Please enter a username between 4-20 characters.',
                        'min_length': 'Please enter a username between 4-20 characters.'}
    )

    # EMAIL
    email = forms.EmailField(
        # can pass custom validators (functions you define)
        validators=[validate_email],
        error_messages={'invalid_email': 'We require hotmail, gmail, or yahoo email accounts.'})  # here we override error message to print using same error code

    # AGE OPTIONAL
    # age not required. okay to leave empty
    age = forms.IntegerField(required=False)

    # PASSWORD
    password = forms.CharField()
    password_confirm = forms.CharField()

    # overwrite default clean method, calls on super class to check on values.
    def clean(self):
        # returns a dictionary, then perform a check on the cleaned_data
        cleaned_data = super(SignupForm, self).clean()

        # Validation involving multiple fields
        if 'password' in cleaned_data and 'password_confirm' in cleaned_data and cleaned_data['password'] != cleaned_data['password_confirm']:
            self.add_error(
                'password_confirm', 'Passwords do not match. Please enter the passwords again.')
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(
        validators=[validate_uname_login])
    password = forms.CharField()

