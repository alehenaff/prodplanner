from rest_framework import serializers
from planner.models import Delta

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
