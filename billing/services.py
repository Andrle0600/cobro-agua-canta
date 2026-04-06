from datetime import date
from django.db import transaction
from .models import Predio, Deuda, Tarifa

class GeneradorDeudas:
    @staticmethod
    def generar_mensual(year=None, month=None):
        if year is None or month is None:
            hoy = date.today()
            year, month = hoy.year, hoy.month
            
        periodo_actual = date(year, month, 1)
        predios_activos = Predio.objects.filter(activo=True)
        deudas_generadas = []
        
        with transaction.atomic():
            for predio in predios_activos:
                # Comprobar si ya existe deuda para el periodo
                if Deuda.objects.filter(predio=predio, periodo=periodo_actual).exists():
                    continue
                    
                # Obtener la tarifa vigente para este tipo de predio
                tarifa_vigente = Tarifa.objects.filter(
                    tipo_predio=predio.tipo_predio,
                    vigente_desde__lte=periodo_actual
                ).exclude(
                    vigente_hasta__lt=periodo_actual
                ).order_by('-vigente_desde').first()
                
                if tarifa_vigente:
                    deuda = Deuda.objects.create(
                        predio=predio,
                        tarifa=tarifa_vigente,
                        periodo=periodo_actual,
                        monto_total=tarifa_vigente.monto,
                        estado='pendiente'
                    )
                    deudas_generadas.append(deuda)
                    
        return deudas_generadas
