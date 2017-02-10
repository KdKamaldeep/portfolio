from __future__ import unicode_literals
from django import forms
from django.contrib.auth.models import User
from .models import Userprofile

class userform(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(userform, self).__init__(*args, **kwargs)

    first_name =  forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','required':'required'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','required':'required'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','required':'required'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','required':'required'}))

    mobileno = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}))

    class Meta:
        model = User
        fields = ('email','username','password','address', 'mobileno','first_name','last_name')


class profileform(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(profileform, self).__init__(*args, **kwargs)

    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phoneno = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    mobileno = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    ext = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    aboutme = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control ','rows':'5', 'required': 'required', 'placeholder':'Tell something about yourself'}))
    profilepic = forms.FileField()
    position = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    skills = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Add your skills - (e.g Asp.net, C#, HTML)',
                                                             'required': 'required', "data-role":"tagsinput"}))

    class Meta:
        model = Userprofile
        fields = ('address', 'mobileno', 'profilepic', 'aboutme', 'phoneno', 'ext','skills','position')

class loginform(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'required'}))