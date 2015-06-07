#!/usr/bin/python
# coding:utf-8
from django import forms
from django.forms import widgets

class SearchForm(forms.Form):
    y = forms.DecimalField(required=True, widget=
        forms.TextInput(attrs={'placeholder':u"年份",'required':"required"}),)
    m = forms.DecimalField(required=True, widget=
        forms.TextInput(attrs={'placeholder':u"月份",'required':"required"}),)

    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        y=cleaned_data.get('y')#如果默认clean不通过，y为空值
        m=cleaned_data.get('m')
        if (y and int(y) < 1000) or (m and (int(m) < 1 or int(m) > 12)):
            raise forms.ValidationError("Invalid Input!")
        return cleaned_data
