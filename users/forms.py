from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from django.forms.forms import Form
from django.forms.models import ModelForm
from .models import Auction, AuctionImage, FuelReport, Route, User, FuelPreson, Driver, MaintenancePerson, Vehicle
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
    middle_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())

    uin = forms.CharField(widget=forms.TextInput())

    address = forms.CharField(widget=forms.TextInput())
    phone_number = forms.CharField(widget=forms.TextInput())
    driving_license = forms.CharField(widget=forms.TextInput())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_driver = True
        if commit:
            user.save()
            driver = Driver.objects.create(
                                           user=user, 
                                           first_name=self.cleaned_data.get('first_name'), 
                                           middle_name=self.cleaned_data.get('middle_name'),
                                           last_name=self.cleaned_data.get('last_name'),
                                           uin = self.cleaned_data.get('uin'),
                                           address = self.cleaned_data.get('address'),
                                           phone_number = self.cleaned_data.get('phone_number'),
                                           driving_license = self.cleaned_data.get('driving_license'),
                                           )

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


class UpdateRouteForm(Form):
    driver = forms.ModelChoiceField(queryset=Driver.objects.all())
    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.all())
    destination = forms.CharField(widget=forms.TextInput())


class UpdateRouteStatusForm(Form):
    choices = [
        ('completed', 'completed'),
        ('canceled', 'canceled'),
        ('delayed', 'delayed')
    ]

    status = forms.CharField(widget=forms.Select(choices=choices))

# AUCTIONS
class CreateAuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ('vehicle', 'description', 'physical_condition')


class UpdateAuctionForm(Form):
    vehicle = forms.ModelChoiceField(queryset=Vehicle.objects.all())
    description = forms.TextInput()
    physical_condition = forms.TextInput()

class UploadImageForm(ModelForm):
    class Meta:
        model = AuctionImage
        fields = ["image"]

class CreateFuelingTaskForm(ModelForm):
    class Meta:
        model = FuelReport
        fields =('fuel_preson', 'driver', 'vehicle')
