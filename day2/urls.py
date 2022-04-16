from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

# app_name = 'cart'

urlpatterns = [
    path('', views.day2, name="day2"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
