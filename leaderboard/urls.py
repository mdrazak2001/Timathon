from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.leaderboard, name="leaderboard"),
    path('analysis', views.analysis, name="analysis"),
]
