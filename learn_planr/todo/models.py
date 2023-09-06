from django.db import models
from django.contrib.auth.models import User


class Schedule(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def incomplete_task_count(self):
        return self.task_set.filter(completed=False).count()

    @property
    def all_task_count(self):
        return self.task_set.count()


class Task(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    data_start = models.DateTimeField(null=True)
    data_finish = models.DateTimeField(null=True)

    def __str__(self):
        return self.title


class Chapter(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    data_start = models.DateTimeField(null=True)
    data_finish = models.DateTimeField(null=True)
    completed = models.BooleanField(default=False)
    next_button_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.title