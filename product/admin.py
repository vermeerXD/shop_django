from django.contrib import admin
from .models import Smartphone, PowerBank, Case, ScreenProtector, CableAndAdapter, Charger

# Register your models here.
admin.site.register(Smartphone)
admin.site.register(PowerBank)
admin.site.register(Case)
admin.site.register(ScreenProtector)
admin.site.register(CableAndAdapter)
admin.site.register(Charger)
