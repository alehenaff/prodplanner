from django.db import models
from polymorphic.models import PolymorphicModel
from django.utils.translation import ugettext_lazy as _
from ordered_model.models import OrderedModel
import datetime
from dateutil import rrule as rr
import itertools

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
    ('DAILY', _('Daily')),
    ('HOURLY', _('Hourly')),
    ('MINUTELY', _('Minutely')),
    ('SECONDLY', _('Secondly'))
)

direction_choices = (
    ('INCLUDE',_('Include')),
    ('EXCLUDE',_('Exclude'))
)

class BaseRule(PolymorphicModel):
    def to_dateutil(self):
        pass

class DateTimeRule(BaseRule):
    datetime = models.DateTimeField()

    def to_dateutil(self):
        return datetime;

    def __str__(self):
        return _("DateTime")+" : "+str(self.datetime)

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
    byhour = models.CharField(max_length=200, default='0')
    byminute = models.CharField(max_length=200, default='0')
    bysecond = models.CharField(max_length=200, default='0')
    byeaster = models.CharField(max_length=30, default=None, blank=True)

    @property
    def content(self):
        elem = lambda x, y: ";{1:s}={0:s}".format(y, x) if (y != "") else ""

        str = 'FREQ={freq};WKST={wkst}{bwd}{bm}{bsp}{bmd}{byd}{bwn}{bh}{bmi}{bs}{be}'.format(
            freq=self.freq, wkst=self.wkst,
            bwd=elem('BYWEEKDAY', self.byweekday),
            bm=elem('BYMONTH', self.bymonth),
            bsp=elem('BYSETPOS', self.bysetpos),
            bmd=elem('BYMONTHDAY', self.bymonthday),
            byd=elem('BYYEARDAY', self.byyearday),
            bwn=elem('BYWEEKNO', self.byweekno),
            bh=elem('BYHOUR', self.byhour), bmi=elem('BYMINUTE', self.byminute),
            bs=elem('BYSECOND', self.bysecond),
            be=elem('BYEASTER', self.byeaster)
        )
        return str

    @property
    def next10(self):
        try:
            r = rr.rrulestr(self.content,dtstart=datetime.datetime.now())
            return itertools.islice(r,10) # 10 first items
        except ValueError as e:
            return _("Unable to evaluate {0:s} ; Error : {1:s} ").format(self.content, str(e))

    def to_dateutil(self):
        try:
            r = rr.rrulestr(self.content)
            return r
        except ValueError as e:
            return _("Unable to evaluate {0:s} ; Error : {1:s} ").format(self.content, str(e))


    def between(self, start, end):
        try:
            return self.to_rrule().between(start, end, inc=True)
        except ValueError as e:
            return _("Unable to evaluate {0:s} ; Error : {1:s} ").format(self.content, str(e))

    def __str__(self):
        return _('Base rule') + " : " + self.name


class RuleSet(BaseRule):
    name = models.CharField(max_length=50)
    elements = models.ManyToManyField(BaseRule, through='RuleSetElement', related_name='baserule')

    def __str__(self):
        return _('Rule Set')+ " : " + self.name

    def to_dateutil(self):
        r = rr.rruleset()
        for elem in self.rulesetelement_set.all():
            if isinstance(elem.baserule, DateTimeRule):
                if elem.direction=='INCLUDE':
                    r.rdate(elem.baserule.to_dateutil())
                else:
                    r.exdate(elem.baserule.to_dateutil())
            elif isinstance(elem.baserule, SimpleRule):
                if elem.direction=='INCLUDE':
                    r.rrule(elem.baserule.to_dateutil())
                else:
                    r.exrule(elem.baserule.to_dateutil())
            elif isinstance(elem.baserule, RuleSet):
                if elem.direction=='INCLUDE':
                    r.rrule(elem.baserule.to_dateutil())
                else:
                    r.exrule(elem.baserule.to_dateutil())
            else:
                pass
        return r

    def between(self, start, end):
        return self.to_dateutil().between(start, end, inc=True)


class RuleSetElement(OrderedModel):
    direction = models.CharField(max_length=15, choices=direction_choices)
    ruleset = models.ForeignKey(RuleSet)
    baserule = models.ForeignKey(BaseRule, related_name='elements_ruleset')
    order_with_respect_to = 'baserule'

    class Meta:
        ordering = ('baserule','order')

    def __str__(self):
        return self.direction + "-" + self.baserule.__str__()
