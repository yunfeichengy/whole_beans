from django import forms
from django.core.exceptions import ValidationError

def validate_email(value):
    if not value.endswith('@hotmail.com') or not value.endswith('@gmail.com') or not value.endswith('@yahoo.com') or not value.endswith('@yahoo.ca'):
        raise ValidationError(
            'Invalid email. This website requires hotmail, gmail, or yahoo email accounts.',  # error message to print
            code = 'invalid_email'                                                            # code so that we can override it if we want
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
      validators=[validate_email],                                                              # can pass custom validators (functions you define)
      error_messages={'invalid_email': 'We require hotmail, gmail, or yahoo email accounts.'})  # here we override error message to print using same error code
    
    # AGE OPTIONAL
    age = forms.IntegerField(required=False)                                                    # age not required. okay to leave empty
    
    # PASSWORD
    password = forms.CharField()
    password_confirm = forms.CharField()

    # overwrite default clean method, calls on super class to check on values.
    def clean(self):
        cleaned_data = super(SignupForm, self).clean()                                          # returns a dictionary, then perform a check on the cleaned_data
        
        # Validation involving multiple fields
        if 'password' in cleaned_data and 'password_confirm' in cleaned_data and cleaned_data['password'] != cleaned_data['password_confirm']:
            self.add_error('password_confirm', 'Passwords do not match. Please enter the passwords again.')
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
