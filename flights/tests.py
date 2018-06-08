from django.test import TestCase, Client
from django.test.utils import setup_test_environment
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
from datetime import datetime
import json


class AssignCrewTest(TestCase):
    def setUp(self):
        airplane1 = Airplane.objects.create(registration='111', capacity=50)
        airplane2 = Airplane.objects.create(registration='222', capacity=30)
        city1 = City.objects.create(name='City1')
        city2 = City.objects.create(name='City2')
        crew1 = Crew.objects.create(c_first_name='raz', c_last_name='dwa')
        crew2 = Crew.objects.create(c_first_name='trzy', c_last_name='cztery')
        Flight.objects.create(airplane=airplane1, city_from=city1, city_to=city2,
                              date_dep=datetime(year=2018, month=1, day=1, hour=12, minute=0),
                              date_arr=datetime(year=2018, month=1, day=1, hour=14, minute=30), crew=None)
        Flight.objects.create(airplane=airplane2, city_from=city1, city_to=city2,
                              date_dep=datetime(year=2018, month=1, day=1, hour=13, minute=0),
                              date_arr=datetime(year=2018, month=1, day=1, hour=15, minute=30), crew=None)
        Flight.objects.create(airplane=airplane1, city_from=city1, city_to=city2,
                              date_dep=datetime(year=2018, month=1, day=1, hour=12, minute=5),
                              date_arr=datetime(year=2018, month=1, day=1, hour=13, minute=30), crew=None)

    def testNotAuthenticated(self):
        client = Client()
        response = client.post('/flights/crews', {'crew_id': 1, 'flight_id': 1})

        self.assertEquals("You need to be logged in to do this", response.json()['message'])

    def testSameFlight(self):
        User.objects.create_user('bob', password='123')
        User.objects.create_user('bob2', password='321')
        client = Client()
        client.login(username='bob', password='123')
        client.post('/flights/crews', {'crew_id': 1, 'flight_id': 1})
        client2 = Client()
        client2.login(username='bob2', password='321')
        response = client2.post('/flights/crews', {'crew_id': 1, 'flight_id': 1})

        self.assertEquals("This crew is busy during that flight, try another", response.json()['message'])

    def testCollidingFlights(self):
        User.objects.create_user('bob', password='123')
        client = Client()
        client.login(username='bob', password='123')
        client.post('/flights/crews', {'crew_id': 2, 'flight_id': 1})
        response = client.post('/flights/crews', {'crew_id': 2, 'flight_id': 2})

        self.assertEquals("This crew is busy during that flight, try another", response.json()['message'])

    def testShortInLong(self):
        User.objects.create_user('bob', password='123')
        client = Client()
        client.login(username='bob', password='123')
        client.post('/flights/crews', {'crew_id': 1, 'flight_id': 1})
        response = client.post('/flights/crews', {'crew_id': 1, 'flight_id': 3})

        self.assertEquals("This crew is busy during that flight, try another", response.json()['message'])

    def testLongInShort(self):
        User.objects.create_user('bob', password='123')
        client = Client()
        client.login(username='bob', password='123')
        client.post('/flights/crews', {'crew_id': 2, 'flight_id': 3})
        response = client.post('/flights/crews', {'crew_id': 2, 'flight_id': 1})

        self.assertEquals("This crew is busy during that flight, try another", response.json()['message'])

    def testSimpleOk(self):
        User.objects.create_user('bob', password='123')
        client = Client()
        client.login(username='bob', password='123')
        response = client.post('/flights/crews', {'crew_id': 1, 'flight_id': 2})

        self.assertEquals(1, response.json()['success'])
