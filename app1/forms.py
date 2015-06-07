from django import forms
from django.forms import ModelForm

from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        #fields = ('title', 'authors') #fields to edited
        #exclude = ('publisher',) #fields not to be edited

class SearchForm(forms.Form):
    keyword = forms.CharField()
