from rest_framework import viewsets
from planner.serializers import SimpleRuleSerializer, RuleElementSerializer, \
    RuleSetElementSerializer, RuleSetSerializer, BaseRuleSerializer, \
    DateTimeRuleSerializer
from planner.models.models import SimpleRule, RuleElement, \
    RuleSetElement, RuleSet, BaseRule, DateTimeRule
import re


class BaseRuleViewSet(viewsets.ModelViewSet):
    queryset = BaseRule.objects.all()
    serializer_class = BaseRuleSerializer

class SimpleRuleViewSet(viewsets.ModelViewSet):
     queryset = SimpleRule.objects.all()
     serializer_class = SimpleRuleSerializer

class RuleElementViewSet(viewsets.ModelViewSet):
    queryset = RuleElement.objects.all()
    serializer_class = RuleElementSerializer

class RuleSetElementViewSet(viewsets.ModelViewSet):
    queryset = RuleSetElement.objects.all()
    serializer_class = RuleSetElementSerializer

class RuleSetViewSet(viewsets.ModelViewSet):
    queryset = RuleSet.objects.all()
    serializer_class = RuleSetSerializer

class DateTimeRuleViewSet(viewsets.ModelViewSet):
    queryset = DateTimeRule.objects.all()
    serializer_class = DateTimeRuleSerializer
