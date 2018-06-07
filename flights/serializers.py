from rest_framework import serializers
from .models import Flight, Crew


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ('c_first_name', 'c_last_name', )


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ('airplane', 'city_from', 'city_to', 'date_dep', 'date_arr', 'passengers', 'crew', )
