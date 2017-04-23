from dateutil import relativedelta
from django.db import models
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
import datetime

class Delta(models.Model):
    year = models.CharField(max_length=4, default=None, blank=True)
    month = models.CharField(max_length=4, default=None, blank=True)
    day = models.CharField(max_length=4, default=None, blank=True)
    hour = models.CharField(max_length=4, default=None, blank=True)
    minute = models.CharField(max_length=4, default=None, blank=True)
    second = models.CharField(max_length=4, default=None, blank=True)
    microsecond = models.CharField(max_length=4, default=None, blank=True)
    years = models.CharField(max_length=4, default=None, blank=True)
    months = models.CharField(max_length=4, default=None, blank=True)
    days = models.CharField(max_length=4, default=None, blank=True)
    hours = models.CharField(max_length=4, default=None, blank=True)
    minutes = models.CharField(max_length=4, default=None, blank=True)
    seconds = models.CharField(max_length=4, default=None, blank=True)
    microseconds = models.CharField(max_length=4, default=None, blank=True)
    weekday = models.CharField(max_length=6, default=None, blank=True)
    leapdays = models.CharField(max_length=6, default=None, blank=True)
    yearday = models.CharField(max_length=4, default=None, blank=True)
    nlyearday = models.CharField(max_length=4, default=None, blank=True)

    def to_custom_dict(self):
        dict = {}
        for f in Delta._meta.get_fields():
            f_name = f.name
            if getattr(self, f_name) not in [None, ''] and f_name is not 'id':
                f_value = eval(getattr(self, f_name))
                dict[f_name] = f_value
        return dict

    @property
    def calculated_delta(self):
        now = datetime.datetime.now()
        then = now + relativedelta.relativedelta(**(self.to_custom_dict()))
        return relativedelta.relativedelta(then, now)
