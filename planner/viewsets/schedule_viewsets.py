from rest_framework import viewsets
from planner.serializers import ScheduleSerializer, TaskSerializer
from planner.models import Schedule, Task

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
