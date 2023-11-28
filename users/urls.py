from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
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
    path("signup/fuel_person/", views.FuelPersonSignUpView.as_view(), name="fuel-person-signup"),
    path("signup/maintenance_person/", views.MaintenancePersonSignUpView.as_view(), name="maintenance-person-signup"),
    path("create/vehicle", views.create_vehicle, name="create-vehicle"),
    path("assign_vehicle", views.assign_vehicle, name="assign-vehicle"),
    path("create/route", views.create_route, name="create-route"),
    path("routes/", views.Routes.as_view(), name="routes"),
    path("routes/<int:pk>", views.update_route, name="update-route"),
    path("report/<int:driver_id>/", views.create_report, name="create_report"),
    path("route-start/<int:pk>", views.start_route, name="start-route"),
    path("create-auction/", views.create_auction, name="create-auction"),
    path("auctions/", views.auctions, name="auctions"),
    path("update_auction/<int:pk>", views.update_auction, name="update-auction"),
    path("auction/<int:pk>", views.auction, name="auction"),
    path("upload_image/<int:pk>", views.uploadImage, name="upload-image"),
    path("delete_image/<int:pk>", views.deleteImage, name="delete-image"),
    path("index1", views.HomePageView.as_view(), name="home"),
    path("maintenance_person_data", views.maintenancePerson_data, name="maintenancePerson_data"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
