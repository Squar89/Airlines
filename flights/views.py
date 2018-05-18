from django.shortcuts import render, get_object_or_404
from .models import Flight, Passenger
from datetime import datetime


def home(request):
    date_format_hint = 'YYYY-MM-DD hour:minute'
    try:
        in_date_from = request.POST['date_from']
        in_date_to = request.POST['date_to']
        if (not in_date_from) or (not in_date_to) or (in_date_from == date_format_hint) or (in_date_to == date_format_hint):
            form_result = "Both fields are required. Try again"
            flights = Flight.objects.order_by('date_dep')[:30]
        else:
            flights = Flight.objects.filter(
                date_dep__range=(datetime.strptime(in_date_from, '%Y-%m-%d %H:%M'), datetime.strptime(in_date_to, '%Y-%m-%d %H:%M')))\
                .order_by('date_dep')[:30]
            form_result = "Filter applied"
    except ValueError:
        form_result = "Wrong data format. Use the one given in hint"
        flights = Flight.objects.order_by('date_dep')[:30]
    except KeyError:
        form_result = None
        flights = Flight.objects.order_by('date_dep')[:30]

    context = {
        'flights_list': flights,
        'form_result': form_result,
        'date_format_hint': date_format_hint,
    }
    return render(request, 'flights/home.html', context)


def detail(request, flight_id):
    if request.user.is_authenticated:
        try:
            #atomic transaction zeby uniknac data race
            flight = get_object_or_404(Flight, pk=flight_id)
            in_first_name = request.POST['first_name']
            in_last_name = request.POST['last_name']
            if (not in_first_name) or (not in_last_name):
                form_result = "Both fields are required. Try again"
            elif flight.airplane.capacity == flight.passengers.count():
                form_result = "Airplane passengers capacity reached. Try buying ticket for other flight"
            else:
                passenger = Passenger(first_name=in_first_name, last_name=in_last_name)
                passenger.save()
                flight.passengers.add(passenger)
                form_result = "Success! Your name should appear on passengers list"
        except KeyError:
            form_result = None
    else:
        form_result = None

    context = {
        'flight': Flight.objects.get(id=flight_id),
        'form_result': form_result,
    }
    return render(request, 'flights/detail.html', context)
