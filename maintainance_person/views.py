from django.shortcuts import render
from users.decorators import maintenance_person_required
from django.contrib.auth.decorators import login_required
# Create your views here.


from .forms import ReportForm


@login_required
@maintenance_person_required
def band_create(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.save()
            return redirect('task-list')
    else:
        form = ReportForm()
    return render(request, 'maintainance_person/report-create.html', {'form': form})


from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm


@login_required
@maintenance_person_required
def task_list(request):
    print(request)
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'maintainance_person/task_list.html', {'tasks': tasks})


@login_required
@maintenance_person_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task-list')
    else:
        form = TaskForm()
    return render(request, 'maintainance_person/task_form.html', {'form': form})


@login_required
@maintenance_person_required
def edit_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task-list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'maintainance_person/task_form.html', {'form': form})


@login_required
@maintenance_person_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.delete()
    return redirect('task-list')
