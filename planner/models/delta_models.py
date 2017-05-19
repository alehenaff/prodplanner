import datetime
from dateutil import relativedelta
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
from django.db import models


class Delta(models.Model):
    """
    model to store informations necessary to describe a dateutil.relativedelta
    """
    _relative_delta_intfields = ['year', 'month', 'day', 'hour', 'minute',
                                 'second', 'microsecond', 'years', 'months',
                                 'days', 'hours', 'minutes',
                                 'seconds', 'microseconds', 'leapdays', 'yearday', 'nlyearday']
    _relative_delta_strfields = ['weekday']
    year = models.IntegerField(default=None, null=True, blank=True)
    month = models.IntegerField(default=None, null=True, blank=True)
    day = models.IntegerField(default=None, null=True, blank=True)
    hour = models.IntegerField(default=None, null=True, blank=True)
    minute = models.IntegerField(default=None, null=True, blank=True)
    second = models.IntegerField(default=None, null=True, blank=True)
    microsecond = models.IntegerField(default=None, null=True, blank=True)
    years = models.IntegerField(default=None, null=True, blank=True)
    months = models.IntegerField(default=None, null=True, blank=True)
    days = models.IntegerField(default=None, null=True, blank=True)
    hours = models.IntegerField(default=None, null=True, blank=True)
    minutes = models.IntegerField(default=None, null=True, blank=True)
    seconds = models.IntegerField(default=None, null=True, blank=True)
    microseconds = models.IntegerField(default=None, null=True, blank=True)
    weekday = models.CharField(max_length=6, default=None, blank=True)
    leapdays = models.IntegerField(default=None, null=True, blank=True)
    yearday = models.IntegerField(default=None, null=True, blank=True)
    nlyearday = models.IntegerField(default=None, null=True, blank=True)

    def to_custom_dict(self):
        """
        returns the model as a dict that can be passed to relativedelta
        """
        dct = {}
        for f_name in self._relative_delta_intfields:
            if getattr(self, f_name) not in [None, '']:
                f_value = getattr(self, f_name)
                dct[f_name] = f_value
        for f_name in self._relative_delta_strfields:
            if getattr(self, f_name) not in [None, '']:
                f_value = eval(getattr(self, f_name))
                dct[f_name] = f_value
        return dct

    def __str__(self):
        return str(self.to_custom_dict())

    def to_start(self, end):
        """
        Calculate start time given the end time based on relativedelta fields stored in the instance
        """
        begin = end + relativedelta.relativedelta(**(self.to_custom_dict()))
        return begin

    @property
    def calculated_delta(self):
        """
        Calculate the relativedelta applied from now - only fields years, months, days, minutes,
        seconds and microseconds are set in the calculated_delta
        """
        now = datetime.datetime.now()
        then = now + relativedelta.relativedelta(**(self.to_custom_dict()))
        return relativedelta.relativedelta(then, now)
