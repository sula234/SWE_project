from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("manager/", views.admin_home, name="admin-home"),
    path("", views.driver_home, name="driver-home"),
    path("fueling_person/", views.fueling_person_home, name="fueling-person-home"),
    path("maintenance_person/", views.maintenance_person_home, name="maintenance-person-home"),
    path("login/", views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),
    path("signup/driver/", views.DriverSignUpView.as_view(), name="driver-signup"),
]
