from rest_framework import viewsets
from planner.serializers import SimpleRuleSerializer, RuleElementSerializer
from planner.models.models import SimpleRule, RuleElement
import re



class SimpleRuleViewSet(viewsets.ModelViewSet):
     queryset = SimpleRule.objects.all()
     serializer_class = SimpleRuleSerializer

class RuleElementViewSet(viewsets.ModelViewSet):
    queryset = RuleElement.objects.all()
    serializer_class = RuleElementSerializer
