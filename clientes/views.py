from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .forms import DuenoForm, MascotaForm
from .models import Mascota


def registrar_ficha(request):
    if request.method == 'POST':
        dueno_form = DuenoForm(request.POST)
        mascota_form = MascotaForm(request.POST)
        if dueno_form.is_valid() and mascota_form.is_valid():
            with transaction.atomic():
                dueno = dueno_form.save()
                mascota = mascota_form.save(commit=False)
                mascota.dueno = dueno
                mascota.save()
            messages.success(
                request,
                f"Ficha registrada. Código de historial: {mascota.codigo_historial}"
            )
            return redirect('clientes:buscar_ficha')
    else:
        dueno_form = DuenoForm()
        mascota_form = MascotaForm()
    return render(request, 'clientes/registro.html', {
        'dueno_form': dueno_form,
        'mascota_form': mascota_form,
    })


def buscar_ficha(request):
    query = request.GET.get('q', '').strip()
    resultados = []
    if query:
        resultados = Mascota.objects.filter(
            nombre__icontains=query
        ) | Mascota.objects.filter(
            codigo_historial__icontains=query
        )
    return render(request, 'clientes/busqueda.html', {
        'query': query,
        'resultados': resultados,
    })