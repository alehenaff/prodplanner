from rest_framework import serializers
from planner.models import Schedule, Task

class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.HyperlinkedIdentityField(view_name='schedule-detail')
    class Meta:
        model = Schedule
        fields = ['id', 'ruleset', 'delta', 'hour', 'minute', 'second']

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.HyperlinkedIdentityField(view_name='task-detail')
    class Meta:
        model = Task
        fields = ['id', 'start', 'due_time', 'schedule']
