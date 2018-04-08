from django.urls import path

from . import views


app_name = 'bashMyWave'
urlpatterns = [
    path('', views.index, name='index'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('<str:waveName>/', views.wave, name='wave'),
]
