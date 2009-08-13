from django import forms

from foialist.models import *


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        exclude = ('entry', 'size')
    
    
class EntryForm(forms.ModelForm):
    govt_entity = forms.CharField(label="Gov't. entity")
    
    class Meta:
        model = Entry
        fields = ('title', 'narrative', 'govt_entity', 'date_requested', 
                  'date_filed', 'poster', 'email')


class CommentForm(forms.ModelForm):
    poster = forms.CharField()

    class Meta:
        model = Comment