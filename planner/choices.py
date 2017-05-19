from django.utils.translation import ugettext_lazy as _

weekdays = (
    ('MO', _('Monday')),
    ('TU', _('Tuesday')),
    ('WE', _('Wednesday')),
    ('TH', _('Thursday')),
    ('FR', _('Friday')),
    ('SA', _('Saturday')),
    ('SU', _('Sunday'))
)

freq_supradaily_choices = (
    ('YEARLY', _('Yearly')),
    ('MONTHLY', _('Monthly')),
    ('WEEKLY', _('Weekly')),
    ('DAILY', _('Daily'))
)

freq_infradaily_choices = (
    ('HOURLY', _('Hourly')),
    ('MINUTELY', _('Minutely')),
    ('SECONDLY', _('Secondly'))
)

direction_choices = (
    ('INCLUDE',_('Include')),
    ('EXCLUDE',_('Exclude'))
)
