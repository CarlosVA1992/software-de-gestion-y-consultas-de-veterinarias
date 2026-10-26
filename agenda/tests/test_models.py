from datetime import datetime
from django.utils import timezone
from django.test import TestCase
from django.core.exceptions import ValidationError
from clientes.models import Dueno, Mascota
from agenda.models import Cita
from agenda.forms import CitaForm


class DuracionCitaTest(TestCase):
    def setUp(self):
        self.dueno = Dueno.objects.create(nombre="Ana", telefono="70000000")
        self.mascota = Mascota.objects.create(
            dueno=self.dueno, nombre="Rocky", especie="Perro", edad=4, sexo="M"
        )
        self.inicio = timezone.make_aware(datetime(2026, 11, 1, 10, 0))

    def test_duracion_consulta_es_30(self):
        cita = Cita.objects.create(
            mascota=self.mascota, veterinario="Dr. A", espacio="consultorio",
            tipo_servicio=Cita.TIPO_CONSULTA, fecha_hora_inicio=self.inicio,
        )
        self.assertEqual(cita.duracion_minutos, 30)

    def test_duracion_cirugia_es_90(self):
        cita = Cita.objects.create(
            mascota=self.mascota, veterinario="Dr. A", espacio="quirofano",
            tipo_servicio=Cita.TIPO_CIRUGIA, fecha_hora_inicio=self.inicio,
        )
        self.assertEqual(cita.duracion_minutos, 90)


class DobleAgendamientoTest(TestCase):
    def setUp(self):
        self.dueno = Dueno.objects.create(nombre="Ana", telefono="70000000")
        self.mascota = Mascota.objects.create(
            dueno=self.dueno, nombre="Rocky", especie="Perro", edad=4, sexo="M"
        )
        self.inicio = timezone.make_aware(datetime(2026, 11, 1, 10, 0))
        Cita.objects.create(
            mascota=self.mascota, veterinario="Dr. A", espacio="consultorio",
            tipo_servicio=Cita.TIPO_CONSULTA, fecha_hora_inicio=self.inicio,
        )

    def test_rechaza_mismo_veterinario_mismo_horario(self):
        form = CitaForm(data={
            'mascota': self.mascota.id,
            'veterinario': 'Dr. A',
            'espacio': 'quirofano',
            'tipo_servicio': Cita.TIPO_CONSULTA,
            'fecha_hora_inicio': '2026-11-01 10:15',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('veterinario', str(form.errors).lower() + str(form.non_field_errors()).lower())

    def test_rechaza_mismo_espacio_mismo_horario(self):
        form = CitaForm(data={
            'mascota': self.mascota.id,
            'veterinario': 'Dr. B',
            'espacio': 'consultorio',
            'tipo_servicio': Cita.TIPO_CONSULTA,
            'fecha_hora_inicio': '2026-11-01 10:15',
        })
        self.assertFalse(form.is_valid())

    def test_permite_horario_libre(self):
        form = CitaForm(data={
            'mascota': self.mascota.id,
            'veterinario': 'Dr. A',
            'espacio': 'consultorio',
            'tipo_servicio': Cita.TIPO_CONSULTA,
            'fecha_hora_inicio': '2026-11-01 11:00',
        })
        self.assertTrue(form.is_valid(), form.errors)