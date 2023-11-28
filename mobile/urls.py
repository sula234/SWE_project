from django.urls import path
from . import views
from .views import update_route
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup', views.signup),
    path('login', views.login),
    path('test_token', views.test_token),
    path('routes', views.routes),
    path('routes/<int:route_id>/update', update_route, name='update-route'),
    path('driver_info', views.driver_info),
    path('get_dispatcher_number', views.get_dispatcher_number, name='get_dispatcher_number'),
    path('fueling_reports', views.fueling_reports),
    path('fueling_reports/<int:fueling_report_id>/update', views.update_fueling_report, name='update-route'),
    path('fueling_info', views.fueling_info),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
