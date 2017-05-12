from rest_framework import serializers
from planner.models import Schedule, Task
import six
import pytz

class TimezoneField(serializers.Field):
    def to_representation(self, obj):
        return six.text_type(obj)

    def to_internal_value(self, data):
        try:
            return pytz.timezone(str(data))
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValidationError('Unknown timezone')

class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.HyperlinkedIdentityField(view_name='schedule-detail')
    timezone = TimezoneField()
    class Meta:
        model = Schedule
        fields = ['id', 'ruleset', 'delta', 'hour', 'minute', 'second',
         'timezone']

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.HyperlinkedIdentityField(view_name='task-detail')
    class Meta:
        model = Task
        fields = ['id', 'start', 'due_time', 'schedule']
