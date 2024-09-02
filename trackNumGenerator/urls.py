from django.urls import path
from . import views


urlpatterns = [
    path('next-tracking-number/', views.get_tracking_number, name='next_tracking_number'),

]