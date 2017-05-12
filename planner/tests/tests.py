from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from planner.models import SimpleRule, RuleSet, RuleSetElement, DateRule, \
    Schedule, Task
from datetime import datetime, date
import testing.postgresql as pg

class PgTestCase(APITestCase):
    def setUp(self):
        self.postgresql = pg.Postgresql()

    def tearDown(self):
        self.postgresql.stop()


class SimpleRuleTests(PgTestCase):
    def test_create_simplerule(self):
        url = '/planner/simplerules/'
        data = {"name_fr": "Lundi de Pâques", "name_en": "Easter Monday","freq": "YEARLY", "byeaster": "1"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SimpleRule.objects.count(),1)
        self.assertEqual(SimpleRule.objects.get().name_fr,'Lundi de Pâques')


class RuleSetTests(PgTestCase):
    def test_create_ruleset(self):
        url = '/planner/rulesets/'
        data = {"name_fr" : "Jours fériés France", "name_en" : "Days off France"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RuleSet.objects.count(),1)
        self.assertEqual(RuleSet.objects.get().name,'Jours fériés France')

class RuleSetElementTests(PgTestCase):
    def test_create_rulesetelement(self):
        url = '/planner/simplerules/'
        data = {"name_fr": "Lundi de Pâques", "name_en": "Easter Monday","freq": "YEARLY", "byeaster": "1"}
        response = self.client.post(url, data, format='json')

        url = '/planner/rulesets/'
        data = {"name_fr" : "Jours fériés France", "name_en" : "Days off France"}
        response = self.client.post(url, data, format='json')

        url = '/planner/rulesetelements/'
        data = {"direction":"INCLUDE", "ruleset" : RuleSet.objects.get().pk, \
        "baserule" : SimpleRule.objects.get().pk }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RuleSetElement.objects.count(),1)

        url= '/planner/rulesets/'+ str(RuleSet.objects.get().pk) +'/between/?start=2017-01-01&end=2018-01-01'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content.decode('UTF-8'),'["2017-04-17"]')

    def test_precedence(self):
        '''
        https://www.ietf.org/rfc/rfc2445.txt
        This implies that start date and times within exclusion related
        properties (i.e., "EXDATE" and "EXRULE") take precedence over those
        specified by inclusion properties (i.e., "RDATE" and "RRULE").

        There is so no need to order inclusions / exclusions
        '''

        mercredis = SimpleRule.objects.create(name_fr='Mercredis', name_en='Wednesdays',\
         freq='WEEKLY', byweekday='WE', bymonth='', bysetpos='', bymonthday='', byyearday='',\
         byweekno='', byeaster='')
        mercredis.save()

        derniers_mercredis_mois = SimpleRule.objects.create(name_fr="Derniers mercredis du mois",\
          name_en="Last wednesdays of month", freq="MONTHLY", byweekday="WE", bymonth='',bysetpos="-1",\
          bymonthday='', byyearday='', byweekno='', byeaster='')
        derniers_mercredis_mois.save()

        april26_2017 = DateRule.objects.create(date = '2017-04-26')
        april26_2017.save()

        ruleset1 = RuleSet.objects.create(name='ruleset1')
        RuleSetElement.objects.create(direction='INCLUDE', baserule=mercredis, ruleset = ruleset1)
        RuleSetElement.objects.create(direction='EXCLUDE', baserule=derniers_mercredis_mois, ruleset = ruleset1)
        RuleSetElement.objects.create(direction='INCLUDE', baserule=april26_2017, ruleset = ruleset1)
        self.assertTrue(datetime(2017,3,22).date() in list(ruleset1.between(datetime(2017,3,1),datetime(2017,5,1))))
        self.assertFalse(datetime(2017,4,26).date() in list(ruleset1.between(datetime(2017,3,1),datetime(2017,5,1))))


class DeltaTests(APITestCase):
    pass




# Create your tests here.
