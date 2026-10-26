from datetime import timedelta
from django.db import models
from clientes.models import Mascota


class Cita(models.Model):
    # --- Estados (RD-02) ---
    ESTADO_PROGRAMADA = 'programada'
    ESTADO_REPROGRAMADA = 'reprogramada'
    ESTADO_CANCELADA = 'cancelada'
    ESTADO_INASISTENCIA = 'inasistencia'
    ESTADOS = [
        (ESTADO_PROGRAMADA, 'Programada'),
        (ESTADO_REPROGRAMADA, 'Reprogramada'),
        (ESTADO_CANCELADA, 'Cancelada'),
        (ESTADO_INASISTENCIA, 'Inasistencia'),
    ]

    # --- Tipos de servicio (RD-01) ---
    TIPO_CONSULTA = 'consulta'
    TIPO_DESPARASITACION = 'desparasitacion'
    TIPO_CIRUGIA = 'cirugia'
    TIPOS_SERVICIO = [
        (TIPO_CONSULTA, 'Consulta'),
        (TIPO_DESPARASITACION, 'Desparasitación'),
        (TIPO_CIRUGIA, 'Cirugía'),
    ]

    # --- Campos ---
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, related_name='citas')
    veterinario = models.CharField(max_length=100)  # por ahora texto; Sprint 2 puede ser FK a usuarios
    espacio = models.CharField(max_length=50, default='consultorio')
    tipo_servicio = models.CharField(max_length=20, choices=TIPOS_SERVICIO)
    fecha_hora_inicio = models.DateTimeField()
    duracion_minutos = models.PositiveIntegerField(editable=False)
    estado = models.CharField(max_length=20, choices=ESTADOS, default=ESTADO_PROGRAMADA)
    creada_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mascota.nombre} - {self.fecha_hora_inicio} ({self.estado})"

    # --- Regla de duración (RD-01) ---
    def calcular_duracion(self):
        if self.tipo_servicio == self.TIPO_CIRUGIA:
            return 90  # 60–120+ según complejidad; base 90
        return 30      # consulta/desparasitación 20–30; base 30

    def save(self, *args, **kwargs):
        if not self.duracion_minutos:
            self.duracion_minutos = self.calcular_duracion()
        super().save(*args, **kwargs)

    @property
    def fecha_hora_fin(self):
        return self.fecha_hora_inicio + timedelta(minutes=self.duracion_minutos)