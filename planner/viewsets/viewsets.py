from rest_framework import viewsets
from planner.serializers import SimpleRuleSerializer
from planner.models.models import SimpleRule
import re



class SimpleRuleViewSet(viewsets.ModelViewSet):
     queryset = SimpleRule.objects.all()
     serializer_class = SimpleRuleSerializer


# Create your views here.
