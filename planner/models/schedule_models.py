from django.db import models
from planner.models import RuleSet, Delta
import datetime
import uuid

class Schedule(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key= True, editable= False)
    ruleset = models.ForeignKey(RuleSet)
    delta = models.ForeignKey(Delta)
    hour = models.IntegerField(default=0)
    minute = models.IntegerField(default=0)
    second = models.IntegerField(default=0)

    def datetime_from_date(self,date):
        return datetime.datetime(date.year, date.month, \
        date.day, self.hour, self.minute, self.second)

class Task(models.Model):
    original_start = models.DateTimeField()
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField()
    schedule = models.ForeignKey(Schedule)

def task_generate(schedule, start, end):
    for sched_instance in schedule.ruleset.between(start, end):
        task_start = schedule.datetime_from_date(sched_instance)
        task_end = schedule.delta.to_end(task_start)
        task, created = Task.objects.get_or_create(original_start=task_start, end=task_end,\
         schedule=schedule)
        if created:
            task.start = task.original_start
            task.save()
