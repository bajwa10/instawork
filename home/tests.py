from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TransactionTestCase

from .models import Member, ROLES


class MemberTest(TransactionTestCase):
    def setUp(self) -> None:
        self.fields = {'first_name', 'last_name', 'number', 'email', 'role'}
        self.invalid_field_values = {'first_name': ['', 'a', 'ab123', '123gag', 'ABsaf123',
                                                    'AZSfulavWQoJpHLrbqrwmnCcgNgpeUtirCJjrXYPOHVBEKVdzwKSTSekyYIYCWorP'],
                                     'last_name': ['', 'a', 'ab123', '123gag', 'ABsaf123',
                                                   'AZSfulavWQoJpHLrbqrwmnCcgNgpeUtirCJjrXYPOHVBEKVdzwKSTSekyYIYCWorP'],
                                     'number': ['', 'abc', '123', '123atsr213', 'avfsg1234r', '12345678910',
                                                '-123456789', '+234152598'],
                                     'email': ['', '@gmail.com', 'test..test@gmail.com', 'test@gmail,com',
                                               '214test@@gmail.com', 'test@test@gmail.com'],
                                     'role': ['', 'anything', 'Regular', 'Admin', 'REGULAR', 'ADMIN', 'rEguLar',
                                              "AdMin",
                                              'pLdHOLengqFBrbSnThEVPAWSuwPgFYmUJ']}
        self.valid_field_values = {'first_name': ['test', 'TEST', 'TEst', 'teST', 'te', 'TE', 'Te', 'tE',
                                                  'AZSfulavWQoJpHLrbqrwmnCcgNgpeUtirCJjrXYPOHVBEKVdzwKSTSekyYIYCWor'],
                                   'last_name': ['test', 'TEST', 'TEst', 'teST', 'te', 'TE', 'Te', 'tE',
                                                 'AZSfulavWQoJpHLrbqrwmnCcgNgpeUtirCJjrXYPOHVBEKVdzwKSTSekyYIYCWor'],
                                   'number': ['1234567891', '8752571581', '5257156297'],
                                   'email': ['test@gmail.com', 'test.test@gmail.com', 'test123@gmail.com',
                                             'test.123@gmail.com', 'test.test.test@gmail.com', 'test.123.te@gmail.com'],
                                   'role': [value[0] for value in ROLES]}

    def testInvalidFields(self) -> None:
        for field in self.fields:
            exclude_fields = tuple(self.fields - {field})
            invalid_values = self.invalid_field_values[field]
            for invalid_value in invalid_values:
                params = {field: invalid_value}
                with self.assertRaises(ValidationError):
                    Member(**params).clean_fields(exclude=exclude_fields)

    def testValidFields(self) -> None:
        for field in self.fields:
            exclude_fields = tuple(self.fields - {field})
            valid_values = self.valid_field_values[field]
            for valid_value in valid_values:
                params = {field: valid_value}
                Member(**params).clean_fields(exclude=exclude_fields)

    def testSaveDelete(self) -> None:
        self.assertEquals(Member.objects.count(), 0)
        Member.objects.create(first_name='test', last_name='test', email='test1@gmail.com', number='1234567890').save()
        self.assertEquals(Member.objects.count(), 1)
        Member.objects.create(first_name='test', last_name='test', email='test2@gmail.com', number='1234567891').save()
        self.assertEquals(Member.objects.count(), 2)
        Member.objects.create(first_name='test', last_name='test', email='test3@gmail.com', number='1234567892').save()
        self.assertEquals(Member.objects.count(), 3)
        Member.objects.filter(email='test3@gmail.com').delete()
        self.assertEquals(Member.objects.count(), 2)
        Member.objects.all().delete()
        self.assertEquals(Member.objects.count(), 0)

    def testUnique(self) -> None:
        self.assertEquals(Member.objects.count(), 0)
        Member.objects.create(first_name='test', last_name='test', email='test@gmail.com', number='1234567890')
        self.assertEquals(Member.objects.count(), 1)
        with self.assertRaises(IntegrityError):
            Member.objects.create(first_name='test2', last_name='test2', email='test@gmail.com',
                                  number='1234567890')
        self.assertEquals(Member.objects.count(), 1)
        with self.assertRaises(IntegrityError):
            Member.objects.create(first_name='test2', last_name='test2', email='test@gmail.com',
                                  number='1234567891')
        self.assertEquals(Member.objects.count(), 1)
        with self.assertRaises(IntegrityError):
            Member.objects.create(first_name='test2', last_name='test2', email='test1@gmail.com',
                                  number='1234567890')
        self.assertEquals(Member.objects.count(), 1)
        Member.objects.create(first_name='test2', last_name='test2', email='test1@gmail.com',
                              number='1234567891')
        self.assertEquals(Member.objects.count(), 2)
        Member.objects.create(first_name='test2', last_name='test2', email='test2@gmail.com',
                              number='1234567892')
        self.assertEquals(Member.objects.count(), 3)
        Member.objects.all().delete()
        self.assertEquals(Member.objects.count(), 0)

    def testCanDelete(self) -> None:
        self.assertEquals(Member.objects.create(number='1234567890', email='test@gmail.com').canDelete, False)
        self.assertEquals(Member.objects.create(role='admin').canDelete, True)
        self.assertEquals(Member.objects.create(number='1234567891', email='test1@gmail.com', role='regular').canDelete,
                          False)
        Member.objects.all().delete()
