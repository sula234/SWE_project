from django.urls import path
from . import views
from .views import update_route

urlpatterns = [
    path('signup', views.signup),
    path('login', views.login),
    path('test_token', views.test_token),
    path('routes', views.routes),
    path('routes/<int:route_id>/update', update_route, name='update-route'),
    path('driver_info', views.driver_info),
    path('get_dispatcher_number', views.get_dispatcher_number, name='get_dispatcher_number'),
]
