from django.contrib import admin
from .models import Schedule, Task


class TaskInline(admin.TabularInline):
    model = Task
    extra = 4


class AdminTodo(admin.ModelAdmin):
    inlines = [TaskInline]
    list_display = ["author", "title", "created_at", "incomplete_task_count"]


admin.site.register(Schedule, AdminTodo)
