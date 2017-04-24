from rest_framework import serializers
from planner.models import Delta
import re

class CalculatedDeltaSerializer(serializers.Serializer):
    years = serializers.CharField()
    months = serializers.CharField()
    days = serializers.CharField()
    hours = serializers.CharField()
    minutes = serializers.CharField()
    seconds = serializers.CharField()
    microseconds = serializers.CharField()


class DeltaSerializer(serializers.HyperlinkedModelSerializer):
    calculated_delta = CalculatedDeltaSerializer(read_only=True)

    class Meta:
        model = Delta
        fields = ['url', 'year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond', \
        'years', 'months', 'days', 'hours', 'minutes', 'seconds', 'microseconds', \
        'weekday', 'leapdays', 'yearday', 'nlyearday', 'calculated_delta']

    def validate_weekday(self,value):
        weekday_pattern = "^$|^(MO|TU|WE|TH|FR|SA|SU)(\([+|-]?\d\)){0,1}$"
        if not re.match(weekday_pattern, value):
            raise serializers.ValidationError("Day not in \
                'MO','TU','WE','TH','FR','SA','SU','MO(+1)', ...")
        return value
