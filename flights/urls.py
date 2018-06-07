from django.conf import settings
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

from . import views

app_name = 'flights'

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:flight_id>/', views.detail, name='detail'),
    path('login', auth_views.login, name='login'),
    re_path(r'^logout/$', auth_views.logout, {'next_page': '/flights'}, name='logout'),
    path('crew', views.crew_view, name='crew'),#TODO
    path('123', views.flights_view, name='flightsjson')#TODO
]

static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
