from django.db import models


class User(models.Model):
    login = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class Randomaizer(models.Model):
    something = models.CharField(max_length=30)


