from django.contrib import admin

from travels.models import Destination, Travel, OrderTravel, Order

admin.site.register(Destination)
admin.site.register(Travel)
admin.site.register(OrderTravel)
admin.site.register(Order)
