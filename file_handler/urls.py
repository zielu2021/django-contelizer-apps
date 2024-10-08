from django.urls import path
from . import views

app_name = 'file_handler'

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('save/', views.save_result, name='save_result'),
]
