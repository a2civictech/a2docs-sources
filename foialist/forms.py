from django import forms

from foialist.models import *


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        exclude = ('entry', 'size')
    
    
class EntryForm(forms.ModelForm):
    fake_entity = forms.CharField()
    
    class Meta:
        model = Entry
        exclude = ('slug', 'poster_slug', 'show', 'date_posted', 'entity')
        fields = ('title', 'narrative', 'fake_entity', 'reason', 'date_requested', 'date_filed', 'poster', 'email')


class CommentForm(forms.ModelForm):
    poster = forms.CharField()

    class Meta:
        model = Comment