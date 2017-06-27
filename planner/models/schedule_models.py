import datetime
import uuid
import pytz
from django.db import models
from planner.models import RuleSet, Delta
from timezone_field import TimeZoneField

class Schedule(models.Model):
    """
    schedule for tasks based on ruleset for then end of the task,
    a delta to calculate the beginning
    a daytime and a timezone
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    ruleset = models.ForeignKey(RuleSet)
    delta = models.ForeignKey(Delta)
    hour = models.IntegerField(default=0)
    minute = models.IntegerField(default=0)
    second = models.IntegerField(default=0)
    timezone = TimeZoneField(default='UTC')

    def datetime_from_date(self, date):
        """
        returns localized datetime for a given day, using daytime in the instance
        """
        return self.timezone.localize(datetime.datetime(date.year, date.month,
                                                        date.day, self.hour,
                                                        self.minute, self.second))

class Task(models.Model):
    """
    A task generated from a schedule
    a reference to the schedule is kept in the task
    the due_time can be modified. The original due_time is kept
    to avoid regenerate a duplicate.
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    start = models.DateTimeField(blank=True, null=True)
    due_time = models.DateTimeField(blank=True, null=True)
    original_due_time = models.DateTimeField()
    schedule = models.ForeignKey(Schedule)

def task_generate(schedule, start, end):

    for sched_instance in schedule.ruleset.between(start, end):
        task_due_time = schedule.datetime_from_date(sched_instance)
        task_start = schedule.delta.to_start(task_due_time)
        task, created = Task.objects.get_or_create(original_due_time=task_due_time,
                                                   start=task_start, schedule=schedule)

        # TODO : transfer this part in the task model (init ?)
        if created:
            task.due_time = task.original_due_time
            task.save()
