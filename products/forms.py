# 6th

from django import forms
from django.forms import inlineformset_factory

from .models import (
    report, Image, VechilePart, Task
)


class reportForm(forms.ModelForm):

    class Meta:
        model = report
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'short_description': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
        }


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = '__all__'


class VechilePartForm(forms.ModelForm):

    class Meta:
        model = VechilePart
        fields = '__all__'
        widgets = {
            'size': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'quantity': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
        }


VechilePartFormSet = inlineformset_factory(
    report, VechilePart, form=VechilePartForm,
    extra=1, can_delete=True,
    can_delete_extra=True
)
ImageFormSet = inlineformset_factory(
    report, Image, form=ImageForm,
    extra=1, can_delete=True,
    can_delete_extra=True
)



class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'due_date', 'priority', 'completed']