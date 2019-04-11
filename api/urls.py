from django.urls import path,re_path
from . import views

urlpatterns = [
    path('get_version', views.version),
    path('', views.api_update)
]