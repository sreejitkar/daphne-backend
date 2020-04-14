from .models import Shop
from rest_framework import serializers

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model=Shop
        fields=['shopid','shop_name','shop_owner','shop_address','shop_category']
