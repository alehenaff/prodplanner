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
    pass

class DateRule(BaseRule):
    date = models.DateField()

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
        except ValueError:
            return _("Unable to evaluate {0:s} {1:s}").format(self.content, ValueError)

class RuleSet(BaseRule):
    name = models.CharField(max_length=50)

class RuleElement(models.Model):
    direction = models.CharField(max_length=15, choices=direction_choices)
    baserule = models.ForeignKey(BaseRule)

class RuleSetElements(OrderedModel):
    ruleset = models.ForeignKey(RuleSet)
    rule = models.ForeignKey(RuleElement)
    order_with_respect_to = 'rule'

    class Meta:
        ordering = ('rule','order')


# Create your models here.
