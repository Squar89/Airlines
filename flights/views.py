from django.shortcuts import render
from .models import Flight


def home(request):
    flights_sorted = Flight.objects.order_by('date_dep')[:30]
    context = {
        'flights_list': flights_sorted,
    }
    return render(request, 'flights/home.html', context)


def detail(request, flight_id):
    context = {
        'flight': Flight.objects.get(id=flight_id),
    }
    return render(request, 'flights/detail.html', context)
