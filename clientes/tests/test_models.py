from django.test import TestCase
from clientes.models import Dueno, Mascota


class MascotaCodigoUnicoTest(TestCase):
    def setUp(self):
        self.dueno = Dueno.objects.create(nombre="Juan Pérez", telefono="77712345")

    def test_dos_mascotas_mismo_nombre_codigos_distintos(self):
        m1 = Mascota.objects.create(
            dueno=self.dueno, nombre="Firulais", especie="Perro", edad=3, sexo="M"
        )
        m2 = Mascota.objects.create(
            dueno=self.dueno, nombre="Firulais", especie="Perro", edad=5, sexo="M"
        )
        self.assertNotEqual(m1.codigo_historial, m2.codigo_historial)

    def test_codigo_historial_es_unico(self):
        m1 = Mascota.objects.create(
            dueno=self.dueno, nombre="Luna", especie="Gato", edad=2, sexo="H"
        )
        self.assertIsNotNone(m1.codigo_historial)