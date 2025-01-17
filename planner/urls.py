from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('save-status/', views.save_status, name='save_status'),
]
