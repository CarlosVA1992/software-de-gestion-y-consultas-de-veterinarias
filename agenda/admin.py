from django.contrib import admin
from .models import Cita


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('mascota', 'veterinario', 'espacio', 'fecha_hora_inicio', 'duracion_minutos', 'estado')
    list_filter = ('estado', 'tipo_servicio', 'veterinario')