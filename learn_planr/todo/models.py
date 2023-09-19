from django.db import models
from django.contrib.auth.models import User


class Schedule(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_progress(self):
        tasks = self.task_set.all()

        if tasks:
            total_chapters = 0
            completed_chapters = 0

            for task in tasks:
                chapters = task.chapter_set.all()
                total_chapters += chapters.count()
                completed_chapters += chapters.filter(completed=True).count()

            if total_chapters > 0:
                # Calculate the progress as a percentage
                progress_percentage = (completed_chapters / total_chapters) * 100
                return progress_percentage

        # If there are no tasks or chapters, return 0% progress
        return 0


class Task(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    data_start = models.DateTimeField(null=True)
    data_finish = models.DateTimeField(null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def incomplete_chapter_count(self):
        return self.chapter_set.filter(completed=True).count()+1

    def all_chapter_count(self):
        return self.chapter_set.count()


class Chapter(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    data_start = models.DateTimeField(null=True)
    data_finish = models.DateTimeField(null=True)
    completed = models.BooleanField(default=False)
    next_button_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.title