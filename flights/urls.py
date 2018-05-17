from django.urls import path

from . import views

app_name = 'flights'

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:flight_id>/', views.detail, name='detail'),
]