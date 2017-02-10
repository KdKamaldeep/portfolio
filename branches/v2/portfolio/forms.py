from __future__ import unicode_literals
from django import forms
from portfolio import models as portfoliomodel


class portfolioForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(portfolioForm, self).__init__(*args, **kwargs)

    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required','placeholder':'Portfolio Title*'}))
    subtitle = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required','placeholder':'Portfolio SubTitle*'}))
    desc = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','rows':'5', 'required': 'required', 'placeholder':'Tell something about this portfolio*'}))
    snapshot = forms.FileField()

    class Meta:
        model = portfoliomodel.portFolio
        exclude = ('user','uuid','totalprojects','url')

class portfolioItemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(portfolioItemForm, self).__init__(*args, **kwargs)

    BIRTH_YEAR_CHOICES = []
    for index in range(2000, 2017):
        BIRTH_YEAR_CHOICES.append(index)


    projectname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}))
    startdate = forms.DateTimeField(widget=forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"),years=BIRTH_YEAR_CHOICES))
    enddate = forms.DateTimeField(widget=forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"),years=BIRTH_YEAR_CHOICES))
    desc = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'required': 'required'}))

    class Meta:
        model = portfoliomodel.portfolioItem
        exclude = ('portfolio',)

class portfolioMediaForm(forms.ModelForm):
    mediapath = forms.FileField()

    class Meta:
        model = portfoliomodel.portfolioItemMedia
        exclude = ('portfolioitem','mediapath', 'mediatype')