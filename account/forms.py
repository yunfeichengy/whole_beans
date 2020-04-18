from django import forms
from django.core.exceptions import ValidationError

def validate_mcgill_email(value):
    if not value.endswith('mcgill.ca'):
        raise ValidationError(
            'Email not from mcgill domain',  # error message to print
            code = 'not_mcgill'  # code so that we can override it if we want
        )

class SignupForm(forms.Form):
    username = forms.CharField( 
      error_messages={'required': 'Gotta make a username!'}
    )
    
    email = forms.EmailField(
      validators=[validate_mcgill_email],  # can pass custom validators (functions you define)
      error_messages={'not_mcgill': 'mcgill members only'})  # here we override error message to print using same error code
    
    age = forms.IntegerField(required=False)  # age not required. okay to leave empty
    password = forms.CharField()
    password_confirm = forms.CharField()

    # overwrite default clean method
    def clean(self):
        cleaned_data = super(SignupForm, self).clean()  # returns a dictionary
        
        # Validation involving multiple fields
        if 'password' in cleaned_data and 'password_confirm' in cleaned_data and cleaned_data['password'] != cleaned_data['password_confirm']:
            self.add_error('password_confirm', 'Passwords do not match')
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


