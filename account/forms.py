from __future__ import unicode_literals
from django import forms
from django.contrib.auth.models import User
from .models import Userprofile

class userform(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(userform, self).__init__(*args, **kwargs)

    first_name =  forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'first_name','required': 'required','oninvalid':'this.setCustomValidity(validity.valueMissing ? "Enter First Name":"")','oninput':'setCustomValidity("")'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'last_name','oninvalid':'this.setCustomValidity("Enter Last Name")','oninput':'setCustomValidity("")'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','required':'required','id':'email','oninvalid'
                                                                                                                     '':'this.setCustomValidity("Enter Email")','oninput':'setCustomValidity("")'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','required':'required','id':'username','oninvalid':'this.setCustomValidity("Enter Username")','oninput':'setCustomValidity("")'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','required':'required','id':'password','oninvalid':'this.setCustomValidity("Enter Password")','oninput':'setCustomValidity("")'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','required':'required','id':'address','oninvalid':'this.setCustomValidity("Enter Address")','oninput':'setCustomValidity("")'}))
    mobileno = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required',
                                                             'id':'mobileno','pattern':'[789][0-9]{9}','placeholder':'9855346745','oninvalid':'this.setCustomValidity("Enter Mobileno")','oninput':'setCustomValidity("")'}))
    skypeid = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','id':'skypeid','oninvalid':'this.setCustomValidity("Enter Skypeid")','oninput':'setCustomValidity("")'}))


    class Meta:
        model = User
        fields = ('email','username','password','address', 'mobileno','first_name','last_name','skypeid')


class profileform(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(profileform, self).__init__(*args, **kwargs)

    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','id':'address','oninvalid':'this.setCustomValidity("Enter Address")','oninput':'setCustomValidity("")'}))
    phoneno = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','id':'phoneno','pattern':'[0-9]{6}','placeholder':'502232','oninvalid':'this.setCustomValidity("Enter Phone")','oninput':'setCustomValidity("")'}))
    mobileno = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','id':'mobileno','pattern':'[789][0-9]{9}','placeholder':'9855346745','oninvalid':'this.setCustomValidity("Enter 10 digit for mobileno")','oninput':'setCustomValidity("")'}))
    ext = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','id':'ext','pattern':'[0-9]{4}','placeholder':'0172','oninvalid':'this.setCustomValidity("Enter 4 digits for ext")','oninput':'setCustomValidity("")'}))
    aboutme = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control ckeditor','rows':'5', 'required': 'required', 'placeholder':'Tell something about yourself','id':'aboutme','oninvalid':'this.setCustomValidity("Enter About Me")','oninput':'setCustomValidity("")'}))
    profilepic = forms.FileField()
    position = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','id':'position','oninvalid':'this.setCustomValidity("Enter Position")','oninput':'setCustomValidity("")'}))
    skills = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Add your skills - (e.g Asp.net, C#, HTML)',
                                                             'required': 'required', "data-role":"tagsinput",
                                                           'id':'skills','oninvalid':'this.setCustomValidity("Enter Skills")',
                                                           'oninput':'setCustomValidity("")'}))
    skypeid = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','id':'skpyeid','oninvalid':'this.setCustomValidity("Enter SkpyeId")','oninput':'setCustomValidity("")'}))
    membertype = forms.ChoiceField()

    class Meta:
        model = Userprofile
        fields = ('address', 'mobileno', 'profilepic', 'aboutme', 'phoneno', 'ext','skills','position','skypeid','membertype')

class loginform(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required','oninvalid':'this.setCustomValidity("Enter Username")','oninput':'setCustomValidity("")'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'required','oninvalid':'this.setCustomValidity("Enter Password")','oninput':'setCustomValidity("")'}))