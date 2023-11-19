from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from django.forms.forms import Form
from django.forms.models import ModelForm
from .models import Route, User, FuelPreson, Driver, MaintenancePerson, Vehicle
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class FuelPersonSignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    g_station_name = forms.CharField(widget=forms.TextInput())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_fuel_person = True
        if commit:
            user.save()
        student = FuelPreson.objects.create(user=user, first_name=self.cleaned_data.get('first_name'), last_name=self.cleaned_data.get('last_name'), g_station_name=self.cleaned_data.get('g_station_name'))
        return user
    

class DriverSignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_driver = True
        if commit:
            user.save()
        teacher = Driver.objects.create(user=user, first_name=self.cleaned_data.get('first_name'), last_name=self.cleaned_data.get('last_name'))

        return user
    

class MaintenancePersonSignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_maintenance_person = True
        if commit:
            user.save()
        teacher = MaintenancePerson.objects.create(user=user, first_name=self.cleaned_data.get('first_name'), last_name=self.cleaned_data.get('last_name'))
        return user
    

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class AddVehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = ('driver', 'manufacturer', 'model', 'make', 'year', 'license_plate', 'capacity', 'mileage')


class AssignVehicleForm(Form):
    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.all())
    driver = forms.ModelChoiceField(queryset=Driver.objects.all())


class CreateRouteForm(ModelForm):
    class Meta:
        model = Route
        fields = ('driver', 'vehicle', 'destination')
