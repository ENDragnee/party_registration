# registration/apis/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GuestViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'guests', GuestViewSet, basename='guest')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
