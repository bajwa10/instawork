from enum import Enum

from django.core.validators import RegexValidator


class RegexValidators(Enum):
    PHONE_NUMBER = RegexValidator(regex=r'^[0-9]{10}$',
                                  message="Please enter a valid phone number. Digits length should be 10.")
    FIRST_NAME = RegexValidator(regex=r'^[a-zA-Z]{2,64}$',
                                message="Please enter a valid first name. Minimum 2 and maximum 64 alphabets allowed.")
    LAST_NAME = RegexValidator(regex=r'^[a-zA-Z]{2,64}$',
                               message="Please enter a valid last name. Minimum 2 and maximum 64 alphabets allowed.")


class Roles(Enum):
    CHOICES = [('admin', "Admin - Can delete members"), ('regular', "Regular - Can\'t delete members")]
    CAN_DELETE = ['admin']
    DEFAULT = 'regular'
