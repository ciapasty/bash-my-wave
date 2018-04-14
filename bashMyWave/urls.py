from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views


app_name = 'bashMyWave'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:waveID>/', views.wave, name='wave'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
