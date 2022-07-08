from django.db import models
from django.utils.html import format_html

from .enums import RegexValidators, Roles


class Member(models.Model):
    first_name = models.CharField(max_length=64, validators=[RegexValidators.FIRST_NAME.value])
    last_name = models.CharField(max_length=64, validators=[RegexValidators.LAST_NAME.value])
    email = models.EmailField(max_length=64, unique=True)
    number = models.CharField(max_length=10, validators=[RegexValidators.PHONE_NUMBER.value], unique=True)
    role = models.CharField(max_length=32, choices=Roles.CHOICES.value, default=Roles.DEFAULT.value)
    canDelete = models.BooleanField(default=False)

    def list_view_data(self):
        return format_html(
            f"<b>{self.first_name} {self.last_name} {'(' + self.role + ')' if self.role in Roles.CAN_DELETE.value else ''}</b><br>{self.number}<br>{self.email}")

    def save(self, *args, **kwargs):
        if self.role in Roles.CAN_DELETE.value:
            self.canDelete = True
        super().save(*args, **kwargs)
