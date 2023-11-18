from logging import warn
from re import template
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from .forms import FuelPresonSignUpForm, DriverSignUpForm, MaintenancePersonSignUpForm ,LoginForm
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .decorators import admin_required, fuel_person_required, driver_required, maintenance_person_required

from django.http import HttpResponse
from .models import User


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
        return redirect('driver-home')

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
    return HttpResponse("Hello maintenance person!")
