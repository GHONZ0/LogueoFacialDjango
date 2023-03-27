from dataclasses import fields
from pyexpat import model
from django import forms
from .models import users

class FormRegisterForm(forms.ModelForm):
    class Meta:
        model = users
        fields = ['usuario', 'password', 'foto']