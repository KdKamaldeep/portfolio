from django import forms
from team import models as teammodel

class teaminvitesform(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(teaminvitesform, self).__init__(*args, **kwargs)

    teamid =  forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    userid = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','required':'required'}))
    status = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','required':'required'}))
    inviteduserid = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','required':'required'}))


    class Meta:
        model = teammodel.teaminvites
        fields = ('teamid','userid','status','inviteduserid')
        exclude = ()

class teamform(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(teamform, self).__init__(*args, **kwargs)

    teamname =  forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    aboutteam = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    hostedteamid = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    logo = forms.FileField()

    userid = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','required':'required'}))
    status = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','required':'required'}))
    deleted = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','required':'required'}))
    class Meta:
        model = teammodel.team
        fields = ('teamname','aboutteam','logo','userid','status', 'deleted')
        exclude = ('logo',)
