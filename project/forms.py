from __future__ import unicode_literals
from django import forms
from project import models as projectmodel
from onlineportfolio import settings
from multiupload.fields import MultiFileField

class projectform(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(projectform, self).__init__(*args, **kwargs)

    BIRTH_YEAR_CHOICES = []
    for index in range(2000, 2017):
        BIRTH_YEAR_CHOICES.append(index)


    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Title*', 'required': 'required'}))
    clientname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Client*', 'required': 'required'}))
    projectname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Project*', 'required': 'required'}))
    services = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'Services provided*',
                                                             'required': 'required', "data-role":"tagsinput"}))
    startdate = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,
                                widget=forms.TextInput(attrs={'class': 'form-control datepicker', 'placeholder':'Date when project start*','required': 'required'}))
    enddate = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS,
                              widget=forms.TextInput(attrs={'class': 'form-control datepicker',
                                                            'placeholder':'Date when project end*','required': 'required'}))
    url = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'URL of the project*', 'required': 'required'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control ckeditor','placeholder':'Here You can fill project details',
                                                               'required': 'required'}))
    #projectpic = forms.FileField()
    projectpic = MultiFileField(min_num=1, max_num=10, max_file_size=1024 * 1024 * 5,required=False)

    class Meta:
        model = projectmodel.project
        exclude = ('user',)