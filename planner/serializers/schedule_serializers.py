from rest_framework import serializers
from planner.models import Schedule, Task
import six
import pytz


# from https://github.com/mfogel/django-timezone-field/issues/29
# adapted for a ChoiceField

class TimezoneField(serializers.ChoiceField):
    def to_representation(self, obj):
        return six.text_type(obj)

    def to_internal_value(self, data):
        try:
            return pytz.timezone(str(data))
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValidationError('Unknown timezone')

class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.HyperlinkedIdentityField(view_name='schedule-detail')
    timezone = TimezoneField(choices=pytz.all_timezones, default='UTC', initial='UTC')
    class Meta:
        model = Schedule
        fields = ['id', 'ruleset', 'delta', 'hour', 'minute', 'second',
         'timezone']

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.HyperlinkedIdentityField(view_name='task-detail')
    class Meta:
        model = Task
        fields = ['id', 'start', 'due_time', 'schedule']
