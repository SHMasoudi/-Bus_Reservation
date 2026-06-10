from django.contrib import admin
from .models import TransportCompany, Bus, Seat, Trip

# Register your models here.


admin.site.register(TransportCompany)
admin.site.register(Bus)
admin.site.register(Seat)
admin.site.register(Trip)