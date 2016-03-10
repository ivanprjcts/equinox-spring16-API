# -*- coding: utf-8 -*-


from rest_framework import serializers

from equinox_api.models import Operation, Application


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ('name', 'open', 'application')


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('name', 'open')