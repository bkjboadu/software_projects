from django import forms
from .models import Client,Comment,ClientFile


class client_form(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name','email','description') 

class comment_form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class file_form(forms.ModelForm):
    class Meta:
        model = ClientFile
        fields = ('file',) 