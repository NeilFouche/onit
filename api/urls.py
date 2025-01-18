"""
Urls for the app front
"""

from django.urls import path
from api import views

urlpatterns = [
    path('abc-testing/', views.test_view, name='abc-testing'),
    path('client/', views.view_manager, name='client-list'),
    path('employee/', views.view_manager, name='employee-list'),
    path('equipment/', views.view_manager, name='equipment-list'),
    path('enquiry/create/', views.view_manager, name='create-enquiry'),
    path('entity-feature/', views.view_manager, name='entity-feature-list'),
    path('entity-media/', views.view_manager, name='entitymedia-list'),
    path('faq/', views.view_manager, name='faq-list'),
    path('feature/', views.view_manager, name='feature-list'),
    path('functional-area/', views.view_manager, name='functionalarea-list'),
    path('media-asset/employee/', views.view_manager, name='employee-media-list'),
    path('media-asset/feature/', views.view_manager, name='feature-media-list'),
    path('media-asset/office/', views.view_manager, name='office-media-list'),
    path('media-asset/service/', views.view_manager, name='service-media-list'),
    path(
        'media-asset/service-method/', views.view_manager, name='servicemethod-media-list'
    ),
    path('office/', views.view_manager, name='office-list'),
    path('operating-hours/', views.view_manager, name='operatinghours-list'),
    path('page/', views.view_manager, name='navigation-data'),
    path('page/header/', views.view_manager, name='navigation-header'),
    path('page/footer/', views.view_manager, name='navigation-footer'),
    path('page/paths/', views.view_manager, name='navigation-paths'),
    path('parameter/', views.view_manager, name='parameter-list'),
    path('person/', views.view_manager, name='person-list'),
    path('project/', views.view_manager, name='project-list'),
    path('region/', views.view_manager, name='region-list'),
    path(
        'reporting-structure/', views.view_manager, name='reportingstructure-list'
    ),
    path('role/', views.view_manager, name='role-list'),
    path('segment/', views.view_manager, name='segment-list'),
    path('service/', views.view_manager, name='service-list'),
    path('service-method/', views.view_manager, name='service-method-list'),
    path('social-platform/', views.view_manager, name='social-list'),
    path('get-csrf-token/', views.view_manager, name='get-csrf-token'),
]
