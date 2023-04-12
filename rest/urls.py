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
router.register(r'mineralization', MineralizationViewSet, basename='api-mineralization')
router.register(r'wc_reason', WCReasonViewSet, basename='api-wc-reason')
router.register(r'pressure', PressureViewSet, basename='api-pressure')
router.register(r'work', WorkViewSet, basename='api-work')
router.register(r'pressure_recovery_curve', PressureRecoveryCurveViewSet, basename='api-pressure-recovery-curve')
router.register(r'water_analysis', WaterAnalysisViewSet, basename='api-water-analysis')
router.register(r'isotopy', IsotopyViewSet, basename='api-isotopy')
router.register(r'water_micro_macro', WaterMicroMacroViewSet, basename='api-water-micro-macro')
router.register(r'oil_micro_macro', OilMicroMacroViewSet, basename='api-oil-micro-macro')
router.register(r'six_components', SixComponentsViewSet, basename='api-six-components')

urlpatterns = [
    path('', include(router.urls)),
]
