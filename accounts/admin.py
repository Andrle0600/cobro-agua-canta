from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, RolModel, Titular, PersonaNatural, PersonaJuridica

admin.site.register(Usuario, UserAdmin)
admin.site.register(RolModel)
admin.site.register(Titular)
admin.site.register(PersonaNatural)
admin.site.register(PersonaJuridica)
