from django.urls import path
from . import views

app_name = 'pesel_validator'

urlpatterns = [
    path('', views.validate_pesel, name='validate_pesel'),
]
