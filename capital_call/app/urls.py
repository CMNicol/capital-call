from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard', views.Dashboard.as_view(), name='dashboard'),
    path('create_call', views.Create.as_view(), name='create_call'),
    path('confirm_call', views.Confirm.as_view(), name='confirm_call'),
    path('error', views.error, name='error'),
]
