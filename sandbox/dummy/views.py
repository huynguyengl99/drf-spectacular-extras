from rest_framework import viewsets

from .models import Dummy
from .serializers import DummySerializer


class DummyViewSet(viewsets.ModelViewSet):
    queryset = Dummy.objects.all()
    serializer_class = DummySerializer
    authentication_classes = []
    permission_classes = []
