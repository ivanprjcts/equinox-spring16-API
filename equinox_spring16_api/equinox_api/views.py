from rest_framework import viewsets

from equinox_api.models import Operation, Application
from equinox_api.serializers import ApplicationSerializer, OperationSerializer


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
