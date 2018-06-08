from urllib.parse import urljoin
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import *
from datetime import datetime
from django import test
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException


def setUpDatabase():
    airplane1 = Airplane.objects.create(registration='111', capacity=50)
    airplane2 = Airplane.objects.create(registration='222', capacity=1)
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
    User.objects.create_user('bob', password='123')


class AssignCrewTest(TestCase):
    def setUp(self):
        setUpDatabase()

    def testNotAuthenticated(self):
        client = Client()
        response = client.post('/flights/crews', {'crew_id': 1, 'flight_id': 1})

        self.assertEquals("You need to be logged in to do this", response.json()['message'])

    def testSameFlight(self):
        User.objects.create_user('bob2', password='321')
        client = Client()
        client.login(username='bob', password='123')
        client.post('/flights/crews', {'crew_id': 1, 'flight_id': 1})
        client2 = Client()
        client2.login(username='bob2', password='321')
        response = client2.post('/flights/crews', {'crew_id': 1, 'flight_id': 1})

        self.assertEquals("This crew is busy during that flight, try another", response.json()['message'])

    def testCollidingFlights(self):
        client = Client()
        client.login(username='bob', password='123')
        client.post('/flights/crews', {'crew_id': 2, 'flight_id': 1})
        response = client.post('/flights/crews', {'crew_id': 2, 'flight_id': 2})

        self.assertEquals("This crew is busy during that flight, try another", response.json()['message'])

    def testShortInLong(self):
        client = Client()
        client.login(username='bob', password='123')
        client.post('/flights/crews', {'crew_id': 1, 'flight_id': 1})
        response = client.post('/flights/crews', {'crew_id': 1, 'flight_id': 3})

        self.assertEquals("This crew is busy during that flight, try another", response.json()['message'])

    def testLongInShort(self):
        client = Client()
        client.login(username='bob', password='123')
        client.post('/flights/crews', {'crew_id': 2, 'flight_id': 3})
        response = client.post('/flights/crews', {'crew_id': 2, 'flight_id': 1})

        self.assertEquals("This crew is busy during that flight, try another", response.json()['message'])

    def testSimpleOk(self):
        client = Client()
        client.login(username='bob', password='123')
        response = client.post('/flights/crews', {'crew_id': 1, 'flight_id': 2})

        self.assertEquals(1, response.json()['success'])


class TestWithSelenium(test.LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestWithSelenium, cls).setUpClass()
        setUpDatabase()

    @classmethod
    def tearDownClass(cls):
        super(TestWithSelenium, cls).tearDownClass()

    def authenticate(self):
        driver = webdriver.Firefox()
        url = urljoin(self.live_server_url, '/flights/login')
        driver.get(url)
        assert u"Login" in driver.title
        username_elem = driver.find_element_by_name('username')
        password_elem = driver.find_element_by_name('password')
        username_elem.send_keys('bob')
        password_elem.send_keys('123')
        button_elem = driver.find_element_by_xpath("//button[@type='submit']")
        button_elem.click()
        driver.implicitly_wait(1)
        assert u"Home" in driver.title

        return driver

    def testSelenium(self):
        driver = TestWithSelenium.authenticate(self)

        url = urljoin(self.live_server_url, '/flights/1/')
        driver.get(url)
        assert u"Flight details" in driver.title
        driver.implicitly_wait(1)

        #simply buy ticket
        first_name_elem = driver.find_element_by_name('first_name')
        last_name_elem = driver.find_element_by_name('last_name')
        first_name_elem.send_keys('Don')
        last_name_elem.send_keys('Bob')
        button_elem = driver.find_element_by_xpath("//button[@type='submit']")
        button_elem.click()
        driver.implicitly_wait(1)
        message = driver.find_element_by_xpath("//*[contains(text(), 'Success')]")
        assert message.get_attribute('innerHTML') == "Success! Your name should appear on passengers list"

        #try to buy tickets when there are no seats left
        url = urljoin(self.live_server_url, '/flights/2/')
        driver.get(url)
        assert u"Flight details" in driver.title
        driver.implicitly_wait(1)
        first_name_elem = driver.find_element_by_name('first_name')
        last_name_elem = driver.find_element_by_name('last_name')
        first_name_elem.send_keys('Don')
        last_name_elem.send_keys('Bob')
        button_elem = driver.find_element_by_xpath("//button[@type='submit']")
        button_elem.click()
        driver.implicitly_wait(1)
        message = driver.find_element_by_xpath("//*[contains(text(), 'Success')]")
        assert message.get_attribute('innerHTML') == "Success! Your name should appear on passengers list"

        first_name_elem = driver.find_element_by_name('first_name')
        last_name_elem = driver.find_element_by_name('last_name')
        first_name_elem.send_keys('The')
        last_name_elem.send_keys('Bob')
        button_elem = driver.find_element_by_xpath("//button[@type='submit']")
        button_elem.click()
        driver.implicitly_wait(1)
        message = driver.find_element_by_xpath("//*[contains(text(), 'Airplane')]")
        assert message.get_attribute('innerHTML') == "Airplane passengers capacity reached. Try buying ticket for other flight"

        #Test Crew
        url = urljoin(self.live_server_url, '/static/crews.html')
        driver.get(url)
        assert u"Crews information" in driver.title
        date_elem = driver.find_element_by_id('s_day')
        date_elem.send_keys(datetime.strftime(datetime(year=2018, month=1, day=1), '%Y-%m-%d'))
        button_elem = driver.find_element_by_id('submit')
        button_elem.click()

        driver2 = TestWithSelenium.authenticate(self)
        driver2.get(url)
        assert u"Crews information" in driver2.title
        date_elem2 = driver2.find_element_by_id('s_day')
        date_elem2.send_keys(datetime.strftime(datetime(year=2018, month=1, day=1), '%Y-%m-%d'))
        button_elem2 = driver2.find_element_by_id('submit')
        button_elem2.click()

        assign_button = driver.find_element_by_id('assign')
        assign_button.click()
        driver.implicitly_wait(1)
        message = driver.find_element_by_xpath("//*[contains(text(), 'Crew assigned')]")
        assert message.get_attribute('innerHTML') == "Crew assigned successfully"

        assign_button2 = driver2.find_element_by_id('assign')
        assign_button2.click()
        driver.implicitly_wait(1)
        try:
            driver2.switch_to.alert.dismiss()
        except NoAlertPresentException:
            assert False
