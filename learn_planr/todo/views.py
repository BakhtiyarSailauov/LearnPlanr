import datetime
import json
from datetime import timedelta

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import SignUpForm, RequestForm
from .models import Schedule, Task
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

    @method_decorator(login_required(login_url="/login/"))
    def post(self, request):
        form = RequestForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data['user_input']
            messages = [{"role": "user", "content": f"что нужно учить чтобы стать {user_input}, укажи сколько время уходят на каждое из них детально. Верни как JSON dict без вложение"}]

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.5,
                max_tokens=3000
            )
            todo = Schedule(author=request.user,
                            title=user_input,
                            )
            todo.save()
            if response:
                list_of_dicts = json.loads(str(response).strip())
                content = response['choices'][0]['message']['content']
                content_dict = json.loads(content)
                print(content_dict)
                current_time = datetime.datetime.now()

                for key, value in content_dict.items():
                    task = Task()
                    task.schedule = todo
                    task.title = value[0]
                    periods = re.findall(r'(\d+)\s*(часов*|часа*|месяцев*|месяца*|годов*|года*|недели*|недель*|минут*|минутов)', value)
                    print(periods, "per", value)
                    for period in periods:
                        num, unit = period
                        num = int(num)
                        print(num, unit)
                        if 'час' in unit:
                            task.data_start = current_time
                            task.data_finish = current_time + timedelta(hours=num)
                        elif 'недель' in unit:
                            task.data_start = current_time
                            task.data_finish = current_time + timedelta(weeks=num)
                        elif 'минут' in unit:
                            task.data_start = current_time
                            task.data_finish = current_time + timedelta(minutes=num)
                        elif 'месяц' in unit:
                            task.data_start = current_time
                            task.data_finish = current_time + timedelta(days=(num * 30))
                        elif 'год' in unit:
                            task.data_start = current_time
                            task.data_finish = current_time + timedelta(days=(num * 365))

                    current_time = task.data_finish
                    task.title = key
                    task.save()
            else:
                print("Invalid JSON string")

            return HttpResponseRedirect(reverse("todo:get_todo", args=(todo.id, )))

        return render(request, 'todo/main.html', {'form': form})


@login_required(login_url="/login/")
def get_todo(request, todo_id):
    todo = get_object_or_404(Schedule, pk=todo_id)
    tasks = Task.objects.filter(schedule=todo).order_by("id")
    context = {"todo": todo, "tasks": tasks}
    return render(request, "todo/page.html", context)


@login_required(login_url="/login/")
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if task.schedule.author == request.user:
        task.completed = True
        task.save()

    return redirect("todo:get_todo", todo_id=task.schedule.id)


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