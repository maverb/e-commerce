from django.contrib import admin
from .models import CreateUser,Item,OrderItem,Order

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)

