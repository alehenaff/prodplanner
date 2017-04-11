from rest_framework import viewsets
from planner.serializers import SimpleRuleSerializer, \
    RuleSetElementSerializer, RuleSetSerializer, BaseRuleSerializer, \
    DateTimeRuleSerializer
from planner.models.models import SimpleRule,  \
    RuleSetElement, RuleSet, BaseRule, DateTimeRule
import re
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from dateutil.parser import parse

class BaseRuleViewSet(viewsets.ModelViewSet):
    queryset = BaseRule.objects.all()
    serializer_class = BaseRuleSerializer

class SimpleRuleViewSet(viewsets.ModelViewSet):
     queryset = SimpleRule.objects.all()
     serializer_class = SimpleRuleSerializer

class RuleSetElementViewSet(viewsets.ModelViewSet):
    queryset = RuleSetElement.objects.all()
    serializer_class = RuleSetElementSerializer

class RuleSetViewSet(viewsets.ModelViewSet):
    queryset = RuleSet.objects.all()
    serializer_class = RuleSetSerializer

    @detail_route(methods=['get'])
    def between(self, request, pk=None):
        ruleset = self.get_object()
        return Response(ruleset.between(parse(request.GET.get('start')), \
        parse(request.GET.get('end'))))


class DateTimeRuleViewSet(viewsets.ModelViewSet):
    queryset = DateTimeRule.objects.all()
    serializer_class = DateTimeRuleSerializer
