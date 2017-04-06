from rest_framework import viewsets
from planner.serializers import SimpleRuleSerializer, RuleElementSerializer, \
    RuleSetElementSerializer, RuleSetSerializer
from planner.models.models import SimpleRule, RuleElement, \
    RuleSetElement, RuleSet
import re



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
