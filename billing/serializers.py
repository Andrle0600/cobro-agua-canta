from rest_framework import serializers
from .models import Predio, Deuda, Pago, Comprobante

class PredioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Predio
        fields = '__all__'

class DeudaSerializer(serializers.ModelSerializer):
    predio_detalle = PredioSerializer(source='predio', read_only=True)
    
    class Meta:
        model = Deuda
        fields = '__all__'

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'

class ComprobanteSerializer(serializers.ModelSerializer):
    pago_detalle = PagoSerializer(source='pago', read_only=True)
    
    class Meta:
        model = Comprobante
        fields = '__all__'
