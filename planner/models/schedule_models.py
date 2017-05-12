from django.db import models
from planner.models import RuleSet, Delta
import datetime
import uuid
from timezone_field import TimeZoneField

class Schedule(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key= True, editable= False)
    ruleset = models.ForeignKey(RuleSet)
    delta = models.ForeignKey(Delta)
    hour = models.IntegerField(default=0)
    minute = models.IntegerField(default=0)
    second = models.IntegerField(default=0)
    timezone = TimeZoneField()

    def datetime_from_date(self,date):
        return datetime.datetime(date.year, date.month, \
        date.day, self.hour, self.minute, self.second)

class Task(models.Model):
    start = models.DateTimeField(blank=True, null=True)
    due_time = models.DateTimeField(blank=True, null=True)
    original_due_time = models.DateTimeField()
    schedule = models.ForeignKey(Schedule)

def task_generate(schedule, start, end):
    for sched_instance in schedule.ruleset.between(start, end):
        task_due_time = schedule.datetime_from_date(sched_instance)
        task_start = schedule.delta.to_start(task_due_time)
        task, created = Task.objects.get_or_create(original_due_time=task_due_time, start=task_start,\
         schedule=schedule)
        if created:
            task.due_time = task.original_due_time
            task.save()
