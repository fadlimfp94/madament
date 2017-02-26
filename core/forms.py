from django.forms import *
from .models import * 
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.models import User
import datetime

class LoginForm(AuthenticationForm):
    username = CharField(label="Username", max_length=30, 
                               widget=TextInput(attrs={'class': 'form-control', 'name': 'username', 'placeholder':'Username...'}))
    password = CharField(label="Password", max_length=30, 
                               widget=PasswordInput(attrs={'class': 'form-control', 'name': 'password', 'placeholder':'Password...'}))
    def __init__(self, *args, **kwargs):
        super(LoginForm,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['autofocus'] = 'on'
        self.error_messages['invalid_login'] = "Your username and password didn't match. Please try again."

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email','first_name','last_name', 'password')     
        widgets = {'username' : TextInput(attrs={'autofocus' : '','class' : 'form-control form-username', 'id' :'form-username', 'placeholder' : 'Username...'}), 'email' : EmailInput(attrs={'class' : 'form-control'}), 'first_name' : TextInput(attrs={'class' : 'form-control'}), 'last_name' : TextInput(attrs={'class' : 'form-control'}),
                     'password' : PasswordInput(attrs={'class' : 'form-control form-password', 'id' :'form-password', 'placeholder' : 'Password...'})}
        help_texts = {
            'username': None,
        }
    def clean(self):
        username = self.cleaned_data.get("username")
        user = User.objects.get(username=username)
        password =  self.cleaned_data.get("password")
        if not user.check_password(password):
            msg = "Current Password wrong"
            self._errors["password"] = self.error_class([msg])
    def __init__(self, *args, **kwargs):
        super(UserForm,self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True               