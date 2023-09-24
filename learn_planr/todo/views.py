import json
from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import SignUpForm, RequestForm
from .models import Schedule, Task, Chapter
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import openai
import re


def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("todo:main"))
    else:
        form = SignUpForm()

    return render(request, "registration/sign_up.html", {"form": form})


class MainView(View):
    @method_decorator(login_required(login_url="/login/"))
    def get(self, request):
        form = RequestForm()
        return render(request, 'todo/main.html', {'form': form})

    def post(self, request):
        form = RequestForm(request.POST)
        try:
            if form.is_valid():
                user_input = form.cleaned_data['user_input']
                messages = [{"role": "user", "content": f"что нужно учить чтобы стать {user_input}. Укажи только сколько время уходят. На каждое из них детально. ('тема': 'время'). Верни как JSON dict без вложение"}]

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0.5,
                    max_tokens=3000
                )

                with transaction.atomic():
                    todo = Schedule(author=request.user, title=user_input)
                    todo.save()

                    if response:
                        content = response['choices'][0]['message']['content']
                        content_dict = json.loads(content)
                        current_time = timezone.now()

                        for key, value in content_dict.items():
                            task = Task(schedule=todo, title=key)
                            task.data_start, task.data_finish = self.calculate_time_periods(current_time, value)
                            task.save()

                            current_time = task.data_finish

                            chapter_messages = [{"role": "user",
                                                 "content": f"что нужно учить чтобы учить {user_input.split(' ')[0]} {key}. Укажи только сколько время уходят. На каждое из них детально. ('тема': 'время'). Верни как JSON dict без вложение"}]
                            print(chapter_messages)
                            chapter_response = openai.ChatCompletion.create(
                                model="gpt-3.5-turbo",
                                messages=chapter_messages,
                                temperature=0.5,
                                max_tokens=3000
                            )

                            if chapter_response:
                                chapter_content = chapter_response['choices'][0]['message']['content']
                                chapter_content_dict = json.loads(chapter_content)
                                current_time = timezone.now()
                                print(chapter_content)
                                for key_task, value_task in chapter_content_dict.items():
                                    chapter = Chapter(task=task, title=key_task)
                                    chapter.data_start, chapter.data_finish = self.calculate_time_periods(current_time, value_task)
                                    chapter.save()

                return HttpResponseRedirect(reverse("todo:get_todo", args=(todo.id,)))
            else:
                return render(request, 'todo/main.html', {'form': form})
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return render(request, 'todo/main.html', {'form': form})

    def calculate_time_periods(self, current_time, value):
        data_start = current_time
        data_finish = current_time
        periods = re.findall(r'(\d+)\s*(часов*|часа*|месяцев*|месяца*|годов*|года*|недели*|недель*|минут*|минутов)',
                             value)
        for period in periods:
            num, unit = period
            num = int(num)
            if 'час' in unit:
                data_start = current_time
                data_finish = current_time + timedelta(hours=num)
            elif 'недель' in unit:
                data_start = current_time
                data_finish = current_time + timedelta(weeks=num)
            elif 'минут' in unit:
                data_start = current_time
                data_finish = current_time + timedelta(minutes=num)
            elif 'месяц' in unit:
                data_start = current_time
                data_finish = current_time + timedelta(days=(num * 30))
            elif 'год' in unit:
                data_start = current_time
                data_finish = current_time + timedelta(days=(num * 365))

        return data_start, data_finish


@login_required(login_url="/login/")
def get_todo(request, todo_id):
    todo = get_object_or_404(Schedule, pk=todo_id)
    tasks = Task.objects.filter(schedule=todo).order_by("id")
    chapters_count = 0
    chapters_completed = 0
    chapters = []
    for task in tasks:
        task_data = {
            "task": task,
            "chapters": Chapter.objects.filter(task=task)
        }
        chapters_count += task.all_chapter_count()
        chapters_completed += (task.incomplete_chapter_count()-1)
        chapters.append(task_data)
        print(chapters_completed, chapters_count)
    context = {"todo": todo, "tasks": tasks, "chapters": chapters, "chapters_count": chapters_count, "chapters_completed": chapters_completed}
    return render(request, "todo/page.html", context)


def toggle_task_completion(request):
    if request.method == 'POST':
        task_data_id = request.POST.get('task_data_id')
        try:
            chapter = Chapter.objects.get(pk=task_data_id)
            chapter_next = Chapter.objects.get(pk=str(int(task_data_id)+1))
            chapter.completed = not chapter.completed

            chapter.next_button_enabled = not chapter.next_button_enabled
            chapter_next.next_button_enabled = not chapter_next.next_button_enabled
            if chapter.task.all_chapter_count() == chapter.task.incomplete_chapter_count():
                chapter.task.completed = not chapter.task.completed
            chapter.save()
            chapter.task.save()
            chapter_next.save()

            return JsonResponse({'success': True})
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found'})
        except Chapter.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Chapter not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@login_required(login_url="/login/")
def get_list_todo(request):
    todos = Schedule.objects.filter(author=request.user).order_by("-id")
    context = {"todos": todos}
    return render(request, "todo/todos.html", context)


@login_required(login_url="/login/")
def delete_todo(request, todo_id):
    todo = Schedule.objects.get(pk=todo_id)
    if request.method == "POST":
        if request.user == todo.author:
            todo.delete()
            return redirect(reverse("todo:get_todos"))

    context = {'todo': todo}
    return render(request, 'todo/todo_confirm_delete.html', context)