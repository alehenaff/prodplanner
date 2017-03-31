from django.shortcuts import render
from rest_framework import serializers, viewsets
from planner.models.models import SimpleRule


class SimpleRuleSerializer(serializers.HyperlinkedModelSerializer):

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
