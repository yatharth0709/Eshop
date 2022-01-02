from django import forms
from .models import *
class signup(forms.ModelForm):# allows to create form for our model ie customer model
        class Meta:
            model=Customer
            fields={'firstname','lastname','email','password','phone'}
            
            widgets={
                'firstname':forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
                'lastname':forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
                'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
                'password':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}),
                'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'Phone no'})
            }
class login(forms.ModelForm):# allows to create form for our model ie customer model
        class Meta:
            model=Customer
            fields={'email','password'}
            
            widgets={
                'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
                'password':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'})
            }


