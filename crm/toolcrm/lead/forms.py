from django import forms
from .models import Lead,Comment,LeadFile

class lead_form(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('name','email','description','priority','status')

class comment_form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class file_form(forms.ModelForm):
    class Meta:
        model = LeadFile
        fields = ('file',)