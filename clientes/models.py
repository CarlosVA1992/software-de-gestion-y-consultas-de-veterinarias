import uuid
from django.db import models


class Dueno(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.nombre


class Mascota(models.Model):
    dueno = models.ForeignKey(Dueno, on_delete=models.CASCADE, related_name='mascotas')
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    edad = models.PositiveIntegerField()
    sexo = models.CharField(max_length=10, choices=[('M', 'Macho'), ('H', 'Hembra')])
    codigo_historial = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def __str__(self):
        return f"{self.nombre} ({self.codigo_historial})"
    