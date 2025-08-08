# party_register_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # The new root URL will point to our landing page
    path('', views.landing_page, name='landing_page'),
    path('register/', views.register_guest, name='register_guest'),
    path('success/<uuid:guest_uuid>/', views.registration_success, name='registration_success'),
    path('checkin/', views.check_in, name='check_in_scanner'),
    path('checkin/<uuid:guest_uuid>/', views.check_in, name='check_in_detail'),
    path('ticket/download/<uuid:guest_uuid>/', views.download_ticket_pdf, name='download_ticket'),
]
