from django import forms
from django.forms import ModelForm

from .enums import Roles
from .models import Member


class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'email', 'number', 'role']
        labels = {'first_name': 'First Name', 'last_name': 'Last Name', 'email': 'Email', 'number': 'Phone Number',
                  'role': 'Role'}
        widgets = {'role': forms.RadioSelect(choices=Roles.CHOICES.value)}
