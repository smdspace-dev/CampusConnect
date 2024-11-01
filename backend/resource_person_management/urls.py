from rest_framework import routers
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ResourcePersonViewSet, WorkshopViewSet, WorkshopRegistrationViewSet,
    ConsultationViewSet, KnowledgeSharingViewSet
)

router = DefaultRouter()
router.register(r'resource-persons', ResourcePersonViewSet, basename='resource-persons')
router.register(r'workshops', WorkshopViewSet, basename='workshops')
router.register(r'workshop-registrations', WorkshopRegistrationViewSet, basename='workshop-registrations')
router.register(r'consultations', ConsultationViewSet, basename='consultations')
router.register(r'knowledge-sharing', KnowledgeSharingViewSet, basename='knowledge-sharing')

urlpatterns = [
    path('', include(router.urls)),
]
