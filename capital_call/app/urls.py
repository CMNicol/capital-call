from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('create_call', views.create_call, name='create_call'),
    path('confirm_call', views.confirm_call, name='confirm_call'),
    path('error', views.error, name='error'),
    path('cancel', views.cancel, name='cancel'),
]
