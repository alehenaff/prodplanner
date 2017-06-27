from rest_framework import viewsets
from planner.serializers import DayTemplateRuleSerializer, \
    RuleSetElementSerializer, RuleSetSerializer, BaseRuleSerializer, \
    DateRuleSerializer
from planner.models import DayTemplateRule,  \
    RuleSetElement, RuleSet, BaseRule, DateRule
import re
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from dateutil.parser import parse

class BaseRuleViewSet(viewsets.ModelViewSet):
    queryset = BaseRule.objects.all()
    serializer_class = BaseRuleSerializer

class DayTemplateRuleViewSet(viewsets.ModelViewSet):
     queryset = DayTemplateRule.objects.all()
     serializer_class = DayTemplateRuleSerializer

     @detail_route(methods=['get'])
     def next10(self, request, pk=None):
        ruleset = self.get_object()
        return Response(ruleset.next10())

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

    @detail_route(methods=['get'])
    def next10(self, request, pk=None):
        ruleset = self.get_object()
        return Response(ruleset.next10())


class DateRuleViewSet(viewsets.ModelViewSet):
    queryset = DateRule.objects.all()
    serializer_class = DateRuleSerializer
