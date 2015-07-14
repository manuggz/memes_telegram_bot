# -*- coding: utf-8 -*-

from django import forms

class LogPrincipalForm(forms.Form):
    username = forms.CharField(
                    required = True,
                    label = "Username",
                    help_text="Your user name.",
                    widget=forms.TextInput
                )
    password = forms.CharField(
                    required = True,
                    label = "Password",
                    help_text="Your password.",
                    widget=forms.PasswordInput
                )

class FormEnviarMensaje(forms.Form):
    mensaje = forms.CharField(
                    required = True,
                    label = "mensaje",
                    help_text="Mensaje a enviar."
                )
