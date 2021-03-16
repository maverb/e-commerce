from rest_framework import serializers
from .models import *


class UploadProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=UploadProduct
        fields = "__all__"

class Client(serializers.ModelSerializer):
    class Meta:
        model=Client
        fields = "__all__"

class Product(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields = "__all__"

class Shipping(serializers.ModelSerializer):
    class Meta:
        model=Shipping
        fields = "__all__"

class Payment(serializers.ModelSerializer):
    class Meta:
        model=Payment
        fields = "__all__"
