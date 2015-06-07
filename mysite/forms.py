#coding:utf-8
from django import forms
from django.forms import widgets

class LoginForm(forms.Form):
    username = forms.CharField(required=True, label=u"用户名", widget=
        forms.TextInput(attrs={'placeholder':u"用户名",'required':"required"}),)
    password = forms.CharField(required=True, label=u"密码", widget=
        forms.PasswordInput(attrs={'placeholder':u"密码",'required':"required"}),)

class ChangepwForm(forms.Form):
    oldpassword = forms.CharField(required=True, label=u"原密码", widget=
        forms.PasswordInput(attrs={'placeholder':u"原密码",'required':"required"}),)
    newpassword1 = forms.CharField(required=True,label=u"新密码",widget=
        forms.PasswordInput(attrs={'placeholder':u"新密码",'required':"required"}),)
    newpassword2 = forms.CharField(required=True,label=u"确认密码",widget=
        forms.PasswordInput(attrs={'placeholder':u"确认密码",'required':"required"}),)

    def clean(self):
        cleaned_data = super(ChangepwForm, self).clean()
        if cleaned_data['newpassword1'] <> cleaned_data['newpassword2']:
            raise forms.ValidationError(u"两次输入的新密码不一样")
        return cleaned_data
