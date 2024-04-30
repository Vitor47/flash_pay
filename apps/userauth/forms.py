# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms



class loginForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-conta fadeIn second",
                "placeholder": "E-mail",
            }
        ),
        required=True,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-conta fadeIn third",
                "placeholder": "Password",
            }
        ),
        required=True,
    )
