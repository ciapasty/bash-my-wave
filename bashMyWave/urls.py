from django.urls import path

from . import views


app_name = 'bashMyWave'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:waveName>/', views.wave, name='wave'),
]
