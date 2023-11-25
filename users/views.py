from logging import warn
from re import template
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, View

from .forms import AddVehicleForm, AssignVehicleForm, CreateRouteForm, FuelPersonSignUpForm, DriverSignUpForm, MaintenancePersonSignUpForm ,LoginForm, UpdateRouteForm, UpdateRouteStatusForm
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .decorators import admin_or_driver, admin_required, fuel_person_required, driver_required, maintenance_person_required

from django.http import HttpResponse
from .models import Driver, Route, User, Vehicle

from django.http import HttpResponseRedirect


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_fuel_person:
                return reverse('fueling-person-home')
            elif user.is_driver:
                return reverse('driver-home')
            elif user.is_maintenance_person:
                return reverse('maintenance-person-home')
            elif user.is_staff:
                return reverse('admin-home')
        else:
            return reverse('login')
        
@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class DriverSignUpView(CreateView):
    model = User
    form_class = DriverSignUpForm
    template_name = 'users/driver_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'driver'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('admin-home')


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class FuelPersonSignUpView(CreateView):
    model = User
    form_class = FuelPersonSignUpForm
    template_name = 'users/fuel_person_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'fuel_person'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('admin-home')


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class MaintenancePersonSignUpView(CreateView):
    model = User
    form_class = MaintenancePersonSignUpForm
    template_name = 'users/maintenance_person_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'maintenance_person'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('admin-home')


@login_required
@admin_required
def create_vehicle(request):
    if request.method == 'POST':
        form = AddVehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save()
            return redirect('admin-home')
    else:
        form = AddVehicleForm()
    return render(request, 'forms/create_vehicle.html', {'form': form})


@login_required
@admin_required
def create_route(request):
    if request.method == 'POST':
        form = CreateRouteForm(request.POST)
        if form.is_valid():
            route = form.save(commit=False)
            route.admin = request.user
            route.save()
            return redirect('admin-home')
    else:
        form = CreateRouteForm()
    return render(request, 'forms/create_route.html', {'form': form})


@login_required
@admin_required
def assign_vehicle(request):
    if request.method == 'POST':
        form = AssignVehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.cleaned_data['vehicle']
            driver = form.cleaned_data['driver']
            vehicle.driver = driver
            vehicle.save()
            return redirect('admin-home')
    else:
        form = AssignVehicleForm()
    return render(request, 'forms/assign_vehicle.html', {'form': form})


@method_decorator(admin_or_driver, name='get')
class Routes(View):
    def get(self, request):
        user = request.user
        if user.is_driver:
            driver = Driver.objects.get(user=user)
            return render(request, 'pages/route_list.html', {'routes': list(Route.objects.filter(driver=driver))})
        return render(request, 'pages/route_list.html', {'routes': list(Route.objects.all())})


@login_required
@admin_required
def update_route(request, pk):
    route = Route.objects.get(pk=pk)
    initial = {'driver': route.driver, 'vehicle': route.vehicle, 'destination': route.destination}
    if request.method == 'POST':
        form = UpdateRouteForm(request.POST)
        if form.is_valid():
            route.driver = form.cleaned_data['driver']
            route.vehicle = form.cleaned_data['vehicle']
            route.destination = form.cleaned_data['destination']
            route.save()
            return redirect('routes')
    else:
        form = UpdateRouteForm(initial=initial)
    return render(request, 'forms/update_route.html', {'form': form, 'pk': pk})


@login_required
@driver_required
def update_route(request, pk):
    route = Route.objects.get(pk=pk)
    initial = {'status': route.status}
    if request.method == 'POST':
        form = UpdateRouteStatusForm(request.POST)
        if form.is_valid():
            route.status = form.cleaned_data['status']
            route.save()
            return redirect('routes')
    else:
        form = UpdateRouteStatusForm(initial=initial)
    return render(request, 'forms/update_route.html', {'form': form, 'pk': pk})


@login_required
@admin_required
def admin_home(request):
    return render(request, 'pages/manager_page.html')

@login_required
@fuel_person_required
def fueling_person_home(request):
    return HttpResponse("Hello fuel person!")

@login_required
@driver_required
def driver_home(request):
    return HttpResponse("Hello driver!")

@login_required
@maintenance_person_required
def maintenance_person_home(request):
     return HttpResponseRedirect(reverse('task-list'))
