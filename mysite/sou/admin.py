from django.contrib import admin
from .models import UploadProduct,CreateUser,Item,OrderItem,Order,Client

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(UploadProduct)
admin.site.register(Client)

