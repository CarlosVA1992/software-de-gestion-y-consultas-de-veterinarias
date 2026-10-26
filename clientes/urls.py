from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.registrar_ficha, name='registrar_ficha'),
    path('buscar/', views.buscar_ficha, name='buscar_ficha'),
]