from django.shortcuts import render
from rest_framework import serializers, viewsets
from planner.models.models import SimpleRule
import re

def pattern_validate(nbmax):
    def validate(value):
        pattern = "^(-?\d{1,2}(,-?\d{1,2}){0,"+str(nbmax)+"})?$"
        if not re.match(pattern,value) :
            raise serializers.ValidationError("Doesn't respect pattern")
    return validate



class SimpleRuleSerializer(serializers.HyperlinkedModelSerializer):

    byweekday = serializers.CharField()

    def validate_byweekday(self,value):
        validation = pattern_validate(7)
        validation(value)
        return value

    class Meta:
        model = SimpleRule
        fields = (
        'content', 'name', 'url', 'freq', 'wkst', 'byweekday', 'bymonth',
        'bysetpos', 'bymonthday', 'byyearday', 'byweekno', 'byhour', 'byminute',
        'bysecond', 'byeaster', 'next10')




class SimpleRuleViewSet(viewsets.ModelViewSet):
     queryset = SimpleRule.objects.all()
     serializer_class = SimpleRuleSerializer


# Create your views here.
