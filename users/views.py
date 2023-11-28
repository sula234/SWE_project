from http.client import OK
from logging import warn
from re import template
from django.core.exceptions import BadRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, View

from django.views.generic import TemplateView

from .forms import AddVehicleForm, AssignVehicleForm, CreateFuelingTaskForm, CreateRouteForm, FuelPersonSignUpForm, DriverSignUpForm, MaintenancePersonSignUpForm ,LoginForm, UpdateRouteForm, UpdateRouteStatusForm
from .forms import AddVehicleForm, AssignVehicleForm, CreateAuctionForm, CreateRouteForm, FuelPersonSignUpForm, DriverSignUpForm, MaintenancePersonSignUpForm ,LoginForm, UpdateAuctionForm, UpdateRouteForm, UpdateRouteStatusForm, UploadImageForm

from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .decorators import admin_or_driver, admin_required, fuel_person_required, driver_required, maintenance_person_required, non_admin_required

from django.http import HttpResponse

from .models import Driver, Route, User, Vehicle, MaintenancePerson

from django.http import HttpResponseRedirect

###########################

class HomePageView(TemplateView):
    template_name = "users/index1.html"

def maintenancePerson_data(request):
#     MaintenancePerson_data = list(MaintenancePerson.objects.all())
    MaintenancePerson_data = MaintenancePerson.objects.get(user=request.user)
    return render(request, 'users/maintenance_person_data.html',
    {'MaintenancePerson_data': MaintenancePerson_data})

###########################


from .models import Driver, Route, User, Vehicle, FuelPreson, FuelReport
from .models import Auction, AuctionImage, Driver, Route, User, Vehicle, is_admin

from django.http import HttpResponseRedirect
from datetime import datetime


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
        #login(self.request, user)
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
        #login(self.request, user)
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
        #login(self.request, user)
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
            return render(request, 'pages/driver_route_list.html', {'routes': list(Route.objects.filter(driver=driver, status='pending'))})
        return render(request, 'pages/route_list.html', {'routes': list(Route.objects.all())})


#   ADMIN ROUTE UPDATE PAGE
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


#   DRIVER ROUTE UPDATE PAGE
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
            return redirect('driver-home')
    else:
        form = UpdateRouteStatusForm(initial=initial)
    return render(request, 'forms/update_route.html', {'form': form, 'pk': pk})


@login_required
@driver_required
def start_route(request, pk):
    route = Route.objects.get(pk=pk)
    route.status = 'in_progress'
    route.save()
    return redirect('driver-home')


@login_required
@admin_required
def admin_home(request):
    if request.method == 'POST':
        driver_id = request.POST.get('driver')
        return redirect('create_report', driver_id = driver_id)

    drivers = Driver.objects.all()
    return render(request, 'pages/manager_page.html', {'drivers': drivers})

@login_required
@admin_required
def create_report(request, driver_id):
    driver = Driver.objects.get(pk = driver_id)
    routes = Route.objects.filter( driver=driver_id, status='finished' )
    tasks_number = routes.count()
    total_distance = 0
    total_time = 0
    for route in routes:
        if( route.finish_time is not None and route.start_time is not None):
            total_time += (route.finish_time - route.start_time).days
        total_distance += route.distance
    distlabels = [route.start_time.strftime('%Y-%m-%d') + ' ' + route.finish_time.strftime('%Y-%m-%d') for route in routes]
    distdata = [route.distance for route in routes]

    vehicles = Vehicle.objects.filter( driver = driver_id )
    fueldata=[]
    for vehicle in vehicles:
        fuels = FuelReport.objects.filter( driver=driver_id, vehicle=vehicle.id )
        labels = [fuel.date.strftime('%Y-%m-%d') for fuel in fuels]
        data = [fuel.fuelAmount for fuel in fuels]
        fueldata.append({
            'vehicle':vehicle.license_plate,
            'labels':labels,
            'data':data,
        })
    return render(request, 'pages/report.html', {'driver': driver, 'routes': routes, 'tasks_number': tasks_number,
                                                 'total_distance': total_distance, 'total_time': total_time,
                                                 'distlabels': distlabels, 'distdata': distdata,
                                                 'fueldata':fueldata})

@login_required
@fuel_person_required
def fueling_person_home(request):
    fuelPerson = FuelPreson.objects.get(user=request.user)
    return render(request, 'pages/fueling_page.html', {'fuelPerson': fuelPerson})

@login_required
@driver_required
def driver_home(request):
    driver = Driver.objects.get(user = request.user)
    routes = Route.objects.filter(driver=driver, status='in_progress')
    history = Route.objects.filter(driver=driver, status='completed') | Route.objects.filter(driver=driver, status='canceled')
    return render(request, 'pages/driver_page.html', {'driver': driver, 'routes': list(routes), 'history': list(history)})

@login_required
@maintenance_person_required
def maintenance_person_home(request):
     return HttpResponseRedirect(reverse('products:task-list'))


# AUCTIONS
@login_required
@admin_required
def create_auction(request):
    if request.method == 'POST':
        form = CreateAuctionForm(request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.admin = request.user
            auction.save()
            return redirect('admin-home')
    else:
        form = CreateAuctionForm()
    return render(request, 'forms/create_auction.html', {'form': form})


def auctions(request):
    auctions = list(Auction.objects.all())
    data = []
    for auction in auctions:
        image = AuctionImage.objects.filter(auction=auction).first()
        data.append((auction, image))
    return render(request, 'pages/auction_list.html', {'data': data})


@login_required
@admin_required
def update_auction(request, pk):
    auction = Auction.objects.get(pk=pk)
    initial = {'vehicle': auction.vehicle}
    images = list(AuctionImage.objects.filter(auction=auction))
    imageForm = UploadImageForm()
    if request.method == 'POST':
        form = UpdateAuctionForm(request.POST)
        if form.is_valid():
            auction.vehicle = form.cleaned_data['vehicle']
            auction.description = form.cleaned_data['description']
            auction.physical_condition = form.cleaned_data['physical_condition']
            auction.save()
            return redirect('auctions')
    else:
        form = UpdateAuctionForm(initial=initial)
    return render(request, 'forms/update_auction.html', {'form': form, 'pk': pk, 'imageForm': imageForm, 'images': images})

@login_required
def auction(request, pk):
    user = request.user
    if user.is_staff:
        return redirect('update-auction', pk=pk)
    auction = Auction.objects.get(pk=pk)
    images = list(AuctionImage.objects.filter(auction=auction))
    return render(request, 'pages/auction.html', {'auction': auction, 'images': images})


@login_required
@admin_required
def uploadImage(request, pk):
    auction = Auction.objects.get(pk=pk)
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.auction = auction
            image.save()
            return redirect('update-auction', pk=pk)
    return BadRequest


@login_required
@admin_required
def deleteImage(request, pk):
    image = AuctionImage.objects.get(pk=pk)
    auction = image.auction
    image.delete()
    return redirect('update-auction', pk=auction.id)


@login_required
@admin_required
def update_fueling_task(request, pk):
    fueling_task = FuelReport.objects.get(pk=pk)
    initial = {'vehicle': fueling_task.vehicle, 'driver': fueling_task.driver, 'fuel_preson': fueling_task.fuel_preson}
    if request.method == 'POST':
        form = CreateFuelingTaskForm(request.POST)
        if form.is_valid():
            fueling_task.vehicle = form.cleaned_data['vehicle']
            fueling_task.driver = form.cleaned_data['driver']
            fueling_task.fuel_preson = form.cleaned_data['fuel_preson']
            fueling_task.save()
            return redirect('fueling-tasks-list')
    else:
        form = CreateFuelingTaskForm(initial=initial)
    return render(request, 'forms/update_fueling_task.html', {'form': form, 'pk': pk})


@login_required
@admin_required
def create_fueling_task(request):
    if request.method == 'POST':
        form = CreateFuelingTaskForm(request.POST)
        if form.is_valid():
            fueling_task = form.save(commit=False)
            fueling_task.save()
            return redirect('fueling-tasks-list')
    else:
        form = CreateFuelingTaskForm()
    return render(request, 'forms/create_fueling_task.html', {'form': form})


@login_required
@admin_required
def list_fueling_reports(request):
    fueling_tasks = list(FuelReport.objects.exclude(date__isnull=True))
    print('yo')
    return render(request, 'pages/fueling_reports_list.html', {'fueling_reports': fueling_tasks})


@login_required
@admin_required
def list_fueling_tasks(request):
    fueling_tasks = list(FuelReport.objects.filter(date__isnull=True))
    return render(request, 'pages/fueling_tasks_list.html', {'fueling_tasks': fueling_tasks})
