from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from planner.models import SimpleRule
import json

class SimpleRuleTests(APITestCase):
    def test_create_simplerule(self):
        url = '/planner/simplerules/'
        data = {"name_fr": "Lundi de Pâques", "name_en": "Easter Monday","freq": "YEARLY", "byeaster": "1"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SimpleRule.objects.count(),1)
        self.assertEqual(SimpleRule.objects.get().name_fr,'Lundi de Pâques')

# Create your tests here.
