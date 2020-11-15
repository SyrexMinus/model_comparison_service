from django.db import models


class User(models.Model):
    name = models.CharField(max_length=64)
    login = models.CharField(max_length=64)
    password = models.CharField(max_length=64)

    def __str__(self):
        return self.name
