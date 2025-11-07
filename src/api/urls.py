"""
Urls for the app front
"""

from django.urls import path
from api import views

urlpatterns = [
    path('health', views.health_check, name='health-check'),
    path('health/', views.health_check, name='health-check'),
    path('backend-test/', views.backend_test, name='backend-test'),
    path('clear-cache/', views.clear_cache, name='clear-cache'),
    path('abc-testing/', views.test_view, name='abc-testing'),
    path('', views.view_manager, name='database-request'),
    path('get-csrf-token/', views.view_manager, name='get-csrf-token'),
]
