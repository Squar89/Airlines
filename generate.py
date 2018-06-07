from flights.models import Airplane, City, Flight, Crew
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

last_names = ['Richards', 'Tate', 'Ford', 'Bowman', 'Escobar', 'Rivas', 'Wells', 'Hoffman', 'Johnson', 'Warner', 'Shelton',
               'Hayden', 'Jefferson', 'Pace', 'Melendez', 'Peters', 'Stanley', 'Bean', 'Mosley', 'Hendricks', 'Acosta',
               'Chapman', 'Figueroa', 'Horn', 'Mccarthy', 'Bolton', 'Chandler', 'Cunningham', 'Mayo', 'Pitts', 'Torres',
               'Massey', 'Vargas', 'James', 'Brewer', 'Bryan', 'Lamb', 'Montes', 'Barnes', 'Zhang', 'Austin', 'Pugh',
               'Frost', 'Good', 'Mcgrath', 'Cline', 'Haynes', 'Mcneil', 'Villa', 'Bowers']

first_names = ['Taryn', 'Dean', 'Cindy', 'Cristal', 'Terrence', 'Deborah', 'Shamar', 'Nick', 'Rosa', 'Adalynn', 'Amelie',
               'Monserrat', 'Sanaa', 'Omari', 'Kadence', 'Carmelo', 'Mia', 'Jaidyn', 'Tiffany', 'Antonio', 'Nadia',
               'Adyson', 'Lucas', 'Isabella', 'King', 'Yaritza', 'Mohammad', 'Sienna', 'Pablo', 'Melvin', 'Elena', 'Jan',
               'Ishaan', 'Kameron', 'Maeve', 'Melody', 'Ronan', 'Janessa', 'Damaris', 'Gabriel', 'Sonny', 'Danica',
               'Nikolaj', 'Laura', 'Sebastian', 'Samson', 'Briana', 'Clara', 'Serenity', 'Jaquan']


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
        next_reg = reg_gen()
        while Airplane.objects.filter(registration=next_reg).count() > 0:
            next_reg = reg_gen()
        q = Airplane(registration=next_reg, capacity=random.randrange(20, 100))
        q.save()


def delete_airplanes():
    Airplane.objects.all().delete()


def generate_flights():
    for airplane in Airplane.objects.all():
        city_from = City.objects.get(name=random.choice(cities))
        city_to = city_from
        date_dep = timezone.now() + datetime.timedelta(hours=random.randrange(0, 50), minutes=random.randrange(0, 60))
        for i in range(0, 50):
            while city_to == city_from:
                city_to = City.objects.get(name=random.choice(cities))
            time_taken = random.randrange(30, 300)
            date_arr = date_dep + datetime.timedelta(minutes=time_taken)

            q = Flight(airplane=airplane, city_from=city_from, city_to=city_to, date_dep=date_dep, date_arr=date_arr)
            q.save()

            city_from = city_to
            date_dep = date_arr + datetime.timedelta(hours=random.randrange(10, 24))


def delete_flights():
    Flight.objects.all().delete()


def generate_crews():
    for i in range(0, 50):
        q = Crew(c_first_name=first_names[random.randint(0, 49)], c_last_name=last_names[random.randint(0, 49)])
        q.save()


def delete_crews():
    Crew.objects.all().delete()


def populate_db():
    add_cities()
    generate_airplanes()
    generate_crews()
    generate_flights()


def clear_db():
    delete_flights()
    delete_cities()
    delete_crews()
    delete_airplanes()
