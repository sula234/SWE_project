from django import forms

from .models import Report, Task


class ReportForm(forms.ModelForm):
   class Meta:
     model = Report
     fields = '__all__'


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'due_date', 'priority', 'completed']