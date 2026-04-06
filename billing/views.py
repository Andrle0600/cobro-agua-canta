from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Predio, Deuda, Pago, Comprobante
from .serializers import PredioSerializer, DeudaSerializer, PagoSerializer, ComprobanteSerializer

class PredioViewSet(viewsets.ModelViewSet):
    queryset = Predio.objects.all()
    serializer_class = PredioSerializer
    
    @action(detail=True, methods=['get'])
    def deudas(self, request, pk=None):
        predio = self.get_object()
        deudas = Deuda.objects.filter(predio=predio)
        serializer = DeudaSerializer(deudas, many=True)
        return Response(serializer.data)

class DeudaViewSet(viewsets.ModelViewSet):
    queryset = Deuda.objects.all()
    serializer_class = DeudaSerializer

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer

class ComprobanteViewSet(viewsets.ModelViewSet):
    queryset = Comprobante.objects.all()
    serializer_class = ComprobanteSerializer
