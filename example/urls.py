from django.urls import path
from example import views

urlpatterns = [
#     url(r'^$', views.HomePageView.as_view(), name='home'), # Notice the URL has been named
#     url(r'^about/$', views.AboutPageView.as_view(), name='about'),
#     path('', views.HomePageView.as_view(), name='home'),
    path('about', views.AboutPageView.as_view(), name='about'),
    path('data', views.DataPageView.as_view(), name='data'),
]