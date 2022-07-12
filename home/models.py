from django.db import models
from django.utils.html import format_html
from django.utils.safestring import SafeString
from django import forms
from django.forms import ModelForm
from django.core.validators import RegexValidator

ROLES = [('admin', "Admin - Can delete members"), ('regular', "Regular - Can\'t delete members")]
ROLES_DELETE = ['admin']
DEFAULT_ROLE = 'regular'

PHONE_NUMBER_VALIDATOR = [RegexValidator(regex=r'^[0-9]{10}$',
                                         message="Please enter a valid phone number. Digits length should be 10.")]
NAME_VALIDATOR = [RegexValidator(regex=r'^[a-zA-Z]{2,64}$',
                                 message="Please enter a valid first name. Minimum 2 and maximum 64 alphabets allowed.")]


class Member(models.Model):
    first_name = models.CharField(max_length=64, validators=NAME_VALIDATOR)
    last_name = models.CharField(max_length=64, validators=NAME_VALIDATOR)
    email = models.EmailField(max_length=64, unique=True)
    number = models.CharField(max_length=10, validators=PHONE_NUMBER_VALIDATOR, unique=True)
    role = models.CharField(max_length=32, choices=ROLES, default=DEFAULT_ROLE)
    canDelete = models.BooleanField(default=False)

    def list_view_data(self) -> SafeString:
        return format_html(
            f"<b>{self.first_name} {self.last_name} {'(' + self.role + ')' if self.role in ROLES_DELETE else ''}</b><br>{self.number}<br>{self.email}")

    def save(self, *args, **kwargs) -> None:
        if self.role in ROLES_DELETE:
            self.canDelete = True
        super().save(*args, **kwargs)


class MemberForm(ModelForm):
    class Meta:
        model = Member
        exclude = ['canDelete']
        fields = '__all__'
        widgets = {'role': forms.RadioSelect(choices=ROLES)}
