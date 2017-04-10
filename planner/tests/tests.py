from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from planner.models import SimpleRule, RuleSet, RuleSetElement

class SimpleRuleTests(APITestCase):
    def test_create_simplerule(self):
        url = '/planner/simplerules/'
        data = {"name_fr": "Lundi de Pâques", "name_en": "Easter Monday","freq": "YEARLY", "byeaster": "1"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SimpleRule.objects.count(),1)
        self.assertEqual(SimpleRule.objects.get().name_fr,'Lundi de Pâques')


class RuleSetTests(APITestCase):
    def test_create_ruleset(self):
        url = '/planner/rulesets/'
        data = {"name" : "Jours fériés"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RuleSet.objects.count(),1)
        self.assertEqual(RuleSet.objects.get().name,'Jours fériés')

class RuleSetElementTests(APITestCase):
    def test_create_rulesetelement(self):
        url = '/planner/simplerules/'
        data = {"name_fr": "Lundi de Pâques", "name_en": "Easter Monday","freq": "YEARLY", "byeaster": "1"}
        response = self.client.post(url, data, format='json')

        url = '/planner/rulesets/'
        data = {"name" : "Jours fériés"}
        response = self.client.post(url, data, format='json')

        url = '/planner/rulesetelements/'
        data = {"direction":"INCLUDE", "ruleset" : RuleSet.objects.get().pk, \
        "baserule" : SimpleRule.objects.get().pk }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RuleSetElement.objects.count(),1)

# Create your tests here.
