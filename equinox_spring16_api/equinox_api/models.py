# -*- coding: utf-8 -*-


from django.db import models


class Application(models.Model):
    name = models.CharField(max_length=40)
    open = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Operation(models.Model):
    name = models.CharField(max_length=40)
    open = models.BooleanField(default=True)
    application = models.ForeignKey(Application)

    def __str__(self):
        return self.name
