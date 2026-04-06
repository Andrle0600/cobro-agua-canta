from django.contrib import admin
from .models import TipoPredio, TipoVia, Via, Direccion, CajaAgua, Predio, Tarifa, Deuda, Pago, Comprobante

admin.site.register(TipoPredio)
admin.site.register(TipoVia)
admin.site.register(Via)
admin.site.register(Direccion)
admin.site.register(CajaAgua)
admin.site.register(Predio)
admin.site.register(Tarifa)
admin.site.register(Deuda)
admin.site.register(Pago)
admin.site.register(Comprobante)
