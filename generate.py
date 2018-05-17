from flights.models import Airplane, City, Flight
import random, string, time, datetime
from django.utils import timezone

cities = ['Andorra la Vella', 'Kabul', "St. John's", 'Tirana', 'Yerevan', 'Luanda', 'Buenos Aires', 'Vienna', 'Canberra',
          'Baku', 'Bridgetown', 'Dhaka', 'Brussels', 'Ouagadougou', 'Sofia', 'Manama', 'Bujumbura', 'Porto-Novo',
          'Bandar Seri Begawan', 'Sucre', 'Brasilia', 'Nassau', 'Thimphu', 'Gaborone', 'Minsk', 'Belmopan', 'Ottawa',
          'Kinshasa', 'Brazzaville', 'Santiago', 'Beijing', 'Bogota', 'San Jose', 'Havana', 'Praia', 'Nicosia', 'Prague',
          'Berlin', 'Djibouti City', 'Copenhagen', 'Roseau', 'Santo Domingo', 'Quito', 'Tallinn', 'Cairo', 'Asmara',
          'Addis Ababa', 'Helsinki', 'Suva', 'Paris', 'Libreville', 'Tbilisi', 'Accra', 'Banjul', 'Conakry', 'Athens',
          'Guatemala City', 'Port-au-Prince', 'Bissau', 'Georgetown', 'Tegucigalpa', 'Budapest', 'Jakarta', 'Dublin',
          'Jerusalem', 'New Delhi', 'Baghdad', 'Tehran', 'Reykjavik', 'Rome', 'Kingston', 'Amman', 'Tokyo', 'Nairobi',
          'Bishkek', 'Tarawa', 'Pyongyang', 'Seoul', 'Kuwait City', 'Beirut', 'Vaduz', 'Monrovia', 'Maseru', 'Vilnius',
          'Luxembourg City', 'Riga', 'Tripoli', 'Antananarivo', 'Majuro', 'Skopje', 'Bamako', 'Naypyidaw', 'Ulaanbaatar',
          'Nouakchott', 'Valletta', 'Port Louis', 'Male', 'Lilongwe', 'Mexico City', 'Kuala Lumpur', 'Maputo', 'Windhoek',
          'Niamey', 'Abuja', 'Managua', 'Amsterdam', 'Oslo', 'Kathmandu', 'Yaren', 'Wellington', 'Muscat', 'Panama City',
          'Lima', 'Port Moresby', 'Manila', 'Islamabad', 'Warsaw', 'Lisbon', 'Ngerulmud', 'Asuncion', 'Doha', 'Bucharest',
          'Moscow', 'Kigali', 'Riyadh', 'Honiara', 'Victoria', 'Khartoum', 'Stockholm', 'Singapore', 'Ljubljana',
          'Bratislava', 'Freetown', 'San Marino', 'Dakar', 'Mogadishu', 'Paramaribo', 'Damascus', 'Lome', 'Bangkok',
          'Dushanbe', 'Ashgabat', 'Tunis', 'Ankara', 'Port of Spain', 'Funafuti', 'Dodoma', 'Kiev', 'Kampala',
          'Washington, D.C.', 'Montevideo', 'Tashkent', 'Vatican City', 'Caracas', 'Hanoi', 'Port Vila', "Sana'a",
          'Lusaka', 'Harare', 'Algiers', 'Sarajevo', 'Phnom Penh', 'Bangui', "N'Djamena", 'Moroni', 'Zagreb', 'Dili',
          'San Salvador', 'Malabo', "St. George's", 'Astana', 'Vientiane', 'Palikir', 'Chisinau', 'Monaco', 'Podgorica',
          'Rabat', 'Basseterre', 'Castries', 'Kingstown', 'Apia', 'Belgrade', 'Pretoria', 'Madrid',
          'Sri Jayewardenepura Kotte', 'Mbabane', 'Bern', 'Abu Dhabi', 'London']


def reg_gen(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def add_cities():
    for city in cities:
        q = City(name=city)
        q.save()


def delete_cities():
    City.objects.all().delete()


def generate_airplanes():
    for _ in range(0, 50):
        try:
            q = Airplane(registration=reg_gen(), capacity=random.randrange(20, 100))
        except:
            #unlucky, we generated the same registration twice
            time.sleep(2)
            q = Airplane(registration=reg_gen(), capacity=random.randrange(20, 100))
            #what are the odds for that happening again, right?
        q.save()


def delete_airplanes():
    Airplane.objects.all().delete()


def generate_flights():
    for airplane in Airplane.objects.all():
        city_from = City.objects.get(name=random.choice(cities))
        date_dep = timezone.now() + datetime.timedelta(hours=random.randrange(0, 50), minutes=random.randrange(0, 60))
        for i in range(0, 50):
            city_to = City.objects.get(name=random.choice(cities))
            time_taken = random.randrange(30, 300)
            date_arr = date_dep + datetime.timedelta(minutes=time_taken)

            q = Flight(airplane=airplane, city_from=city_from, city_to=city_to, date_dep=date_dep, date_arr=date_arr)
            q.save()

            city_from = city_to
            date_dep = date_arr + datetime.timedelta(hours=random.randrange(10, 24))


def delete_flights():
    Flight.objects.all().delete()


def populate_db():
    add_cities()
    generate_airplanes()
    generate_flights()


def clear_db():
    delete_flights()
    delete_cities()
    delete_airplanes()
