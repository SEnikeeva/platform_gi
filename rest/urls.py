from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rest.views import *

router = DefaultRouter()
router.register(r'project', ProjectViewSet, basename='api-project')
router.register(r'oil_deposit', OilDepositViewSet, basename='api-deposit')
router.register(r'well', WellViewSet, basename='api-well')
router.register(r'coords', CoordsViewSet, basename='api-coords')
router.register(r'perforation', PerforationViewSet, basename='api-perforation')
router.register(r'eor_prod', EORProdViewSet, basename='api-eor-prod')
router.register(r'eor_inj', EORInjViewSet, basename='api-eor-inj')

urlpatterns = [
    path('', include(router.urls)),
]
