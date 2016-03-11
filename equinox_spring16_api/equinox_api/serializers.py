# -*- coding: utf-8 -*-

from django.contrib.auth.models import User

from rest_framework import serializers

from equinox_api.models import Operation, Application, Instances


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ('name', 'open', 'application')


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('name', 'open', 'description')


class InstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instances
        fields = ('name', 'open', 'user')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')