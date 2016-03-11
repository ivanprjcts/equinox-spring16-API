from django.contrib.auth.models import User

from rest_framework import viewsets

from equinox_api.models import Operation, Application, Instances
from equinox_api.serializers import ApplicationSerializer, OperationSerializer, InstanceSerializer, UserSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows applications to be viewed and edited.
    """
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


class OperationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows operations to be viewed and edited.
    """
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer


class InstancesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows instances to be viewed and edited.
    """
    queryset = Instances.objects.all()
    serializer_class = InstanceSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed and edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer