# coding: utf-8
from django import forms


class IpAddrForm(forms.Form):
    ip = forms.CharField(label='IP地址',max_length=100)
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
