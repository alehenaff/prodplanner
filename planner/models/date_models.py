from django.db import models
from polymorphic.models import PolymorphicModel
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from dateutil import rrule as rr
import itertools
import uuid

weekdays = (
    ('MO', _('Monday')),
    ('TU', _('Tuesday')),
    ('WE', _('Wednesday')),
    ('TH', _('Thursday')),
    ('FR', _('Friday')),
    ('SA', _('Saturday')),
    ('SU', _('Sunday'))
)

freq_choices = (
    ('YEARLY', _('Yearly')),
    ('MONTHLY', _('Monthly')),
    ('WEEKLY', _('Weekly')),
    ('DAILY', _('Daily'))
)

direction_choices = (
    ('INCLUDE',_('Include')),
    ('EXCLUDE',_('Exclude'))
)

class BaseRule(PolymorphicModel):
    id = models.UUIDField(default=uuid.uuid4, primary_key= True, editable= False)

    def to_dateutil(self, start):
        pass

class DateRule(BaseRule):
    date = models.DateField()

    def to_dateutil(self, start):
        if (start<datetime.combine(self.date,datetime.min.time())):
            return datetime.combine(self.date,datetime.min.time());
        else:
            return None
    def __str__(self):
        return _("Date")+" : "+str(self.date)

class SimpleRule(BaseRule):
    name = models.CharField(max_length=50)
    wkst = models.CharField(max_length=2, choices=weekdays, default='MO')
    freq = models.CharField(max_length=10, default='YEARLY',
                            choices=freq_choices)
    byweekday = models.CharField(max_length=25, default=None, blank=True)
    bymonth = models.CharField(max_length=50, default=None, blank=True)
    bysetpos = models.CharField(max_length=50, default=None, blank=True)
    bymonthday = models.CharField(max_length=50, default=None, blank=True)
    byyearday = models.CharField(max_length=200, default=None, blank=True)
    byweekno = models.CharField(max_length=200, default=None, blank=True)
    byeaster = models.CharField(max_length=30, default=None, blank=True)

    @property
    def content(self):
        elem = lambda x, y: ";{1:s}={0:s}".format(y, x) if (y != "") else ""

        str = 'FREQ={freq};WKST={wkst}{bwd}{bm}{bsp}{bmd}{byd}{bwn}{bhms}{be}'.format(
            freq=self.freq, wkst=self.wkst,
            bwd=elem('BYWEEKDAY', self.byweekday),
            bm=elem('BYMONTH', self.bymonth),
            bsp=elem('BYSETPOS', self.bysetpos),
            bmd=elem('BYMONTHDAY', self.bymonthday),
            byd=elem('BYYEARDAY', self.byyearday),
            bwn=elem('BYWEEKNO', self.byweekno),
            bhms=';BYHOUR=0;BYMINUTE=0;BYSECOND=0',
            be=elem('BYEASTER', self.byeaster)
        )
        return str

    def next10(self):
        try:
            r = self.to_dateutil(datetime.now())
            return map(lambda x:x.date(), itertools.islice(r,10)) # 10 first items
        except ValueError as e:
            return _("Unable to evaluate {0:s} ; Error : {1:s} ").format(self.content, str(e))

    def to_dateutil(self, start):
        try:
            r = rr.rrulestr(self.content, dtstart=start)
            return r
        except ValueError as e:
            return _("Unable to evaluate {0:s} ; Error : {1:s} ").format(self.content, str(e))


    def between(self, start, end):
        try:
            return map(lambda x:x.date(), self.to_dateutil(start).between(start, end, inc=True))
        except ValueError as e:
            return _("Unable to evaluate {0:s} ; Error : {1:s} ").format(self.content, str(e))

    def __str__(self):
        return _('Base rule') + " : " + self.name


class RuleSet(BaseRule):
    name = models.CharField(max_length=50)
    elements = models.ManyToManyField(BaseRule, through='RuleSetElement', related_name='baserule')

    def __str__(self):
        return _('Rule Set')+ " : " + self.name

    def to_dateutil(self,start):
        r = rr.rruleset()
        for elem in self.rulesetelement_set.all():
            if isinstance(elem.baserule, DateRule):
                if elem.direction=='INCLUDE':
                    r.rdate(elem.baserule.to_dateutil(start))
                else:
                    r.exdate(elem.baserule.to_dateutil(start))
            elif isinstance(elem.baserule, SimpleRule):
                if elem.direction=='INCLUDE':
                    r.rrule(elem.baserule.to_dateutil(start))
                else:
                    r.exrule(elem.baserule.to_dateutil(start))
            elif isinstance(elem.baserule, RuleSet):
                if elem.direction=='INCLUDE':
                    r.rrule(elem.baserule.to_dateutil(start))
                else:
                    r.exrule(elem.baserule.to_dateutil(start))
            else:
                pass
        return r

    def next10(self):
        try:
            r = self.to_dateutil(datetime.now())
            return map(lambda x:x.date(), itertools.islice(r,10)) # 10 first items
        except ValueError as e:
            return _("Unable to evaluate {0:s} ; Error : {1:s} ").format(self.__str__, str(e))

    def between(self, start, end):
        return map(lambda x:x.date(),self.to_dateutil(start).between(start, end, inc=True))


class RuleSetElement(models.Model):
    class Meta:
        unique_together=(('direction', 'ruleset', 'baserule'))

    id = models.UUIDField(default=uuid.uuid4, primary_key= True, editable= False)
    direction = models.CharField(max_length=15, choices=direction_choices)
    ruleset = models.ForeignKey(RuleSet)
    baserule = models.ForeignKey(BaseRule, related_name='elements_ruleset')

    def __str__(self):
        return self.direction + "-" + self.baserule.__str__()
