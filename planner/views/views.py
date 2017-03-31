from django.shortcuts import render
from rest_framework import serializers, viewsets
from planner.models.models import SimpleRule
import re

def pattern_validate(nbmax):
    def validate(value):
        pattern = "^(-?\d{1,2}(,-?\d{1,2}){0,"+str(nbmax)+"})?$"
        if not re.match(pattern,value) :
            raise serializers.ValidationError("Doesn't respect pattern : \
            integer or sequence of integers (comma separated)")
    return validate



class SimpleRuleSerializer(serializers.HyperlinkedModelSerializer):

    byweekday = serializers.CharField(allow_blank=True)
    bymonth = serializers.CharField(allow_blank=True)
    bysetpos = serializers.CharField(allow_blank=True)
    bymonthday = serializers.CharField(allow_blank=True)
    byyearday = serializers.CharField(allow_blank=True)
    byweekno = serializers.CharField(allow_blank=True)
    byhour = serializers.CharField(allow_blank=True)
    byminute = serializers.CharField(allow_blank=True)
    bysecond = serializers.CharField(allow_blank=True)
    byeaster = serializers.CharField(allow_blank=True)

    def validate_byweekday(self,value):
        weekday_pattern = "^$|^(MO|TU|WE|TH|FR|SA|SU)(\([+|-]\d\)){0,1}(,(MO|TU|WE|TH|FR|SA|SU)(\([+|-]\d\)){0,1})*$"
        if not re.match(weekday_pattern,value):
                raise serializers.ValidationError("Day not in \
                'MO','TU','WE','TH','FR','SA','SU','MO(+1)', ...")
        return value


    def validate_month(self, value):
        validation = pattern_validate(12)
        validation(value)
        return value

    def validate_bysetpos(self, value):
        validation = pattern_validate(15)
        validation(value)
        return value

    def validate_bymonthday(self, value):
        validation = pattern_validate(31)
        validation(value)
        return value

    def validate_byyearday(self, value):
        validation = pattern_validate(365)
        validation(value)
        return value

    def validate_byweekno(self, value):
        validation = pattern_validate(52)
        validation(value)
        return value

    def validate_byhour(self, value):
        validation = pattern_validate(24)
        validation(value)
        return value

    def validate_byminute(self, value):
        validation = pattern_validate(60)
        validation(value)
        return value

    def validate_bysecond(self, value):
        validation = pattern_validate(60)
        validation(value)
        return value

    def validate_byeaster(self, value):
        validation = pattern_validate(60)
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
