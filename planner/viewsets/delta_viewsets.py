from rest_framework import viewsets
from planner.serializers import DeltaSerializer
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from planner.models import Delta

class DeltaViewSet(viewsets.ModelViewSet):
    queryset = Delta.objects.all()
    serializer_class = DeltaSerializer

    @detail_route(methods=['get'])
    def deltatime(self, request, pk=None):
        return Response(self.get_object().real_delta_str())
