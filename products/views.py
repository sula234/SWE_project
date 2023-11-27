# 6th
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.edit import (
    CreateView, UpdateView
)

from .forms import (
    reportForm, VechilePartFormSet, ImageFormSet
)
from .models import (
    Image,
    report,
    VechilePart
)

from django.utils.decorators import method_decorator
from users.decorators import maintenance_person_required, admin_required, admin_or_maintenance_person
from django.contrib.auth.decorators import login_required



class reportInline():
    form_class = reportForm
    model = report
    template_name = "reports/report_create_or_update.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('reports:task-list')

    def formset_VechileParts_valid(self, formset):
        """
        Hook for custom formset saving.. useful if you have multiple formsets
        """
        VechileParts = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this, if you have can_delete=True parameter set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for VechilePart in VechileParts:
            VechilePart.report = self.object
            VechilePart.save()

    def formset_images_valid(self, formset):
        """
        Hook for custom formset saving.. useful if you have multiple formsets
        """
        images = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this, if you have can_delete=True parameter set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for image in images:
            image.report = self.object
            image.save()


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_or_maintenance_person, name='dispatch')    
class reportCreate(reportInline, CreateView):

    def get_context_data(self, **kwargs):
        ctx = super(reportCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx
    

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'VechileParts': VechilePartFormSet(prefix='VechileParts'),
                'images': ImageFormSet(prefix='images'),
            }
        else:
            return {
                'VechileParts': VechilePartFormSet(self.request.POST or None, self.request.FILES or None, prefix='VechileParts'),
                'images': ImageFormSet(self.request.POST or None, self.request.FILES or None, prefix='images'),
            }

@method_decorator(login_required, name='dispatch')
@method_decorator(admin_or_maintenance_person, name='dispatch')    
class reportUpdate(reportInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(reportUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'VechileParts': VechilePartFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='VechileParts'),
            'images': ImageFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='images'),
        }


@login_required
@admin_or_maintenance_person
def delete_image(request, pk):
    try:
        image = Image.objects.get(id=pk)
    except Image.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
            )
        return redirect('reports:update_report', pk=image.report.id)

    image.delete()
    messages.success(
            request, 'Image deleted successfully'
            )
    return redirect('reports:update_report', pk=image.report.id)


@login_required
@admin_or_maintenance_person
def delete_VechilePart(request, pk):
    try:
        VechilePart = VechilePart.objects.get(id=pk)
    except VechilePart.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
            )
        return redirect('reports:update_report', pk=VechilePart.report.id)

    VechilePart.delete()
    messages.success(
            request, 'VechilePart deleted successfully'
            )
    return redirect('reports:update_report', pk=VechilePart.report.id)


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')    
class reportList(ListView):
    model = report
    template_name = "reports/report_list.html"
    context_object_name = "reports"


@login_required
@maintenance_person_required
def reportListMaintainance(request):
    reports = report.objects.filter(user=request.user)
    return render(request, 'reports/report_list.html', {'reports': reports})




from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm


@login_required
@maintenance_person_required
def task_list(request):
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
            return redirect('products:task-list')
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
            return redirect('products:task-list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'maintainance_person/task_form.html', {'form': form})


@login_required
@maintenance_person_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.delete()
    return redirect('products:task-list')