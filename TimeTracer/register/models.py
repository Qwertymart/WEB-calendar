from django.db import models


class users(models.Model):
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.name


class events(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name