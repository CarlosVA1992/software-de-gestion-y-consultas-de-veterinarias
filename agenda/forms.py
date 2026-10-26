from django import forms
from django.core.exceptions import ValidationError
from .models import Cita
from django.utils import timezone

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['mascota', 'veterinario', 'espacio', 'tipo_servicio', 'fecha_hora_inicio']
        widgets = {
            'fecha_hora_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned = super().clean()
        veterinario = cleaned.get('veterinario')
        espacio = cleaned.get('espacio')
        inicio = cleaned.get('fecha_hora_inicio')
        if timezone.is_naive(inicio):
            inicio = timezone.make_aware(inicio)
        tipo = cleaned.get('tipo_servicio')

        if not all([veterinario, espacio, inicio, tipo]):
            return cleaned

        # Calcular fin estimado
        duracion = 90 if tipo == Cita.TIPO_CIRUGIA else 30
        fin = inicio + __import__('datetime').timedelta(minutes=duracion)

        # Validar solapamiento para veterinario y espacio
        conflictos = Cita.objects.filter(
            fecha_hora_inicio__lt=fin,
        ).exclude(estado__in=[Cita.ESTADO_CANCELADA])

        for c in conflictos:
            if c.fecha_hora_fin > inicio:
                if c.veterinario == veterinario:
                    raise ValidationError(
                        f"El veterinario {veterinario} ya tiene una cita en ese horario."
                    )
                if c.espacio == espacio:
                    raise ValidationError(
                        f"El espacio {espacio} ya está ocupado en ese horario."
                    )
        return cleaned