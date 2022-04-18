from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.day3, name="day3"),
    path('py/', views.day3py, name="day3py"),
]
