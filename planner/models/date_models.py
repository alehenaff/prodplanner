from datetime import datetime
import itertools
import uuid
from dateutil import rrule as rr
from django.utils.translation import ugettext_lazy as _
from django.db import models
from polymorphic.models import PolymorphicModel
from planner.choices import freq_supradaily_choices, weekdays, direction_choices


class BaseRule(PolymorphicModel):
    """
    Base class for date rules
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    def to_dateutil(self, start):
        """
        to be overriden - must return the date object intended to be described by
        the model :
        DateRule -> datetime
        SimpleRule -> dateutil rrule
        RuleSet -> dateutil rruleset
        ...
        """
        pass


class DateRule(BaseRule):
    """
    Simple Date, heriting from BaseRule to be able to add it to RuleSet
    """
    date = models.DateField()

    def to_dateutil(self, start):
        """
        returns a datetime
        """
        if start < datetime.combine(self.date, datetime.min.time()):
            return datetime.combine(self.date, datetime.min.time())
        else:
            return None

    def __str__(self):
        return _("Date") + " : " + str(self.date)


class DayTemplateRule(BaseRule):
    """
    dateutil RRule, heriting from BaseRule to be able to add it to RuleSet
    """
    name = models.CharField(max_length=50)
    wkst = models.CharField(max_length=2, choices=weekdays, default='MO')
    freq = models.CharField(max_length=10, default='YEARLY',
                            choices=freq_supradaily_choices)
    byweekday = models.CharField(max_length=25, default=None, blank=True)
    bymonth = models.CharField(max_length=50, default=None, blank=True)
    bysetpos = models.CharField(max_length=50, default=None, blank=True)
    bymonthday = models.CharField(max_length=50, default=None, blank=True)
    byyearday = models.CharField(max_length=200, default=None, blank=True)
    byweekno = models.CharField(max_length=200, default=None, blank=True)
    byeaster = models.CharField(max_length=30, default=None, blank=True)

    @property
    def content(self):
        """
        return the ruleset in a string format that can be reinterpreted by rrulestr()
        """
        def elem(x, y):
            """
            returns an empty string if y is not set
            """
            return ";{0:s}={1:s}".format(x, y) if (y != "") else ""

        rstr = 'FREQ={freq};WKST={wkst}{bwd}{bm}{bsp}{bmd}{byd}{bwn}{bhms}{be}'.format(
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
        return rstr

    def next10(self):
        """
        returns next 10 occurrences from now
        """
        try:
            simpr = self.to_dateutil(datetime.now())
            # 10 first items
            return map(lambda x: x.date(), itertools.islice(simpr, 10))
        except ValueError as err:
            return _("Unable to evaluate {0:s} ; Error : {1:s} ").format(self.content, err.__str__)

    def to_dateutil(self, start):
        try:
            simpr = rr.rrulestr(self.content, dtstart=start)
            return simpr
        except ValueError as err:
            return _("Unable to evaluate {0:s} ; Error : {1:s} ").format(self.content, err.__str__)

    def between(self, start, end):
        """
        returns occurrences between start and end
        """
        try:
            return map(lambda x: x.date(), self.to_dateutil(start).between(start, end, inc=True))
        except ValueError as err:
            return _("Unable to evaluate {0:s} ; Error : {1:s} ").format(self.content, err.__str__)

    def __str__(self):
        return _('Base rule') + " : " + self.name


class CompleteRule(BaseRule):

    daytemplate = models.ForeignKey(DayTemplateRule)
    byhour = models.CharField(max_length=50, default=None, blank=True)
    byminute = models.CharField(max_length=50, default=None, blank=True)
    bysecond = models.CharField(max_length=50, default=None, blank=True)

    @property
    def content(self):
        """
        return the ruleset in a string format that can be reinterpreted by rrulestr()
        """
        def elem(x, y):
            """
            returns an empty string if y is not set
            """
            return ";{0:s}={1:s}".format(x, y) if (y != "") else ""

        rstr = 'FREQ={freq};WKST={wkst}{bwd}{bm}{bsp}{bmd}{byd}{bwn}{bho}{bmi}{bse}{be}'.format(
            freq=self.daytemplate.freq, wkst=self.daytemplate.wkst,
            bwd=elem('BYWEEKDAY', self.daytemplate.byweekday),
            bm=elem('BYMONTH', self.daytemplate.bymonth),
            bsp=elem('BYSETPOS', self.daytemplate.bysetpos),
            bmd=elem('BYMONTHDAY', self.daytemplate.bymonthday),
            byd=elem('BYYEARDAY', self.daytemplate.byyearday),
            bwn=elem('BYWEEKNO', self.daytemplate.byweekno),
            bho=elem('BYHOUR', self.byhour),
            bmi=elem('BYMINUTE', self.byminute),
            bse=elem('BYSECOND', self.bysecond),
            be=elem('BYEASTER', self.daytemplate.byeaster)
        )
        return rstr

    def next10(self):
        """
        returns next 10 occurrences from now
        """
        try:
            simpr = self.to_dateutil(datetime.now())
            # 10 first items
            return map(lambda x: x.date(), itertools.islice(simpr, 10))
        except ValueError as err:
            return _("Unable to evaluate {0:s} ; Error : {1:s} ").format(self.content, err.__str__)

    def to_dateutil(self, start):
        try:
            simpr = rr.rrulestr(self.content, dtstart=start)
            return simpr
        except ValueError as err:
            return _("Unable to evaluate {0:s} ; Error : {1:s} ").format(self.content, err.__str__)

    def between(self, start, end):
        """
        returns occurrences between start and end
        """
        try:
            return map(lambda x: x.date(), self.to_dateutil(start).between(start, end, inc=True))
        except ValueError as err:
            return _("Unable to evaluate {0:s} ; Error : {1:s} ").format(self.content, err.__str__)

    def __str__(self):
        return _('Base rule') + " : " + self.name

class RuleSet(BaseRule):
    """
    corresponds to dateutil rruleset
    """

    name = models.CharField(max_length=50)
    elements = models.ManyToManyField(
        BaseRule, through='RuleSetElement', related_name='baserule')

    def __str__(self):
        return _('Rule Set') + " : " + self.name

    def to_dateutil(self, start):
        rlst = rr.rruleset()
        for elem in self.rulesetelement_set.all():
            if isinstance(elem.baserule, DateRule):
                if elem.direction == 'INCLUDE':
                    rlst.rdate(elem.baserule.to_dateutil(start))
                else:
                    rlst.exdate(elem.baserule.to_dateutil(start))
            elif isinstance(elem.baserule, DayTemplateRule):
                if elem.direction == 'INCLUDE':
                    rlst.rrule(elem.baserule.to_dateutil(start))
                else:
                    rlst.exrule(elem.baserule.to_dateutil(start))
            elif isinstance(elem.baserule, RuleSet):
                if elem.direction == 'INCLUDE':
                    rlst.rrule(elem.baserule.to_dateutil(start))
                else:
                    rlst.exrule(elem.baserule.to_dateutil(start))
            else:
                pass
        return rlst

    def next10(self):
        """
        returns next 10 occurrences of the recurrence
        """
        try:
            rlst = self.to_dateutil(datetime.now())
            # 10 first items
            return map(lambda x: x.date(), itertools.islice(rlst, 10))
        except ValueError as err:
            return _("Unable to evaluate {0:s} ; Error : {1:s} ").format(self.__str__, str(err))

    def between(self, start, end):
        """
        returns the list of occurrences between start and end
        """
        return map(lambda x: x.date(), self.to_dateutil(start).between(start, end, inc=True))


class RuleSetElement(models.Model):
    """
    through table for manytomany between rulesets and baserules
    """
    class Meta:
        unique_together = (('direction', 'ruleset', 'baserule'))

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    direction = models.CharField(max_length=15, choices=direction_choices)
    ruleset = models.ForeignKey(RuleSet)
    baserule = models.ForeignKey(BaseRule, related_name='elements_ruleset')

    def __str__(self):
        return self.direction + "-" + self.baserule.__str__()
