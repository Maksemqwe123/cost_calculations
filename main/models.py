from django.db import models

from django.db import models


class UsersExpenses(models.Model):
    user_id = models.BigIntegerField(null=True)
    user_name = models.CharField(max_length=128, null=True)
    company_name = models.CharField(max_length=256, null=True)
    category_name = models.CharField(max_length=512, null=True)
    price = models.FloatField(null=True)
    dttm = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'users_expenses'


class UserRegistration(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    user_name = models.CharField(max_length=128, null=True)
    login = models.CharField(max_length=6000, null=True)
    password = models.CharField(max_length=6000, null=True)
    date_registration = models.DateTimeField(null=True)

    def __str__(self):
        return self.login, self.password

    class Meta:
        managed = False
        db_table = 'user_registration'
