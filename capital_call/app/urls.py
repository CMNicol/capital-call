from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('create_call', views.create_call, name='create_call'),
    path('preview_call', views.preview_call, name='preview_call'),
    path('error', views.error, name='error'),
]
