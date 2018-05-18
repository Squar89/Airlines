from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'flights'

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:flight_id>/', views.detail, name='detail'),
    path('login', auth_views.login, name='login'),
    re_path(r'^logout/$', auth_views.logout, {'next_page': '/flights'}, name='logout')
]
