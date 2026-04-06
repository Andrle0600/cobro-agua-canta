from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PredioViewSet, DeudaViewSet, PagoViewSet, ComprobanteViewSet

router = DefaultRouter()
router.register(r'predios', PredioViewSet)
router.register(r'deudas', DeudaViewSet)
router.register(r'pagos', PagoViewSet)
router.register(r'comprobantes', ComprobanteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
