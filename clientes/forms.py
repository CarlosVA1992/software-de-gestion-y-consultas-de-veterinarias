from django import forms
from .models import Dueno, Mascota


class DuenoForm(forms.ModelForm):
    class Meta:
        model = Dueno
        fields = ['nombre', 'telefono', 'email']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'edad', 'sexo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'especie': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
        }