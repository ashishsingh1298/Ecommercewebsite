from rest_framework import serializers
from shop.models import Products, Orders
from django.contrib.auth.models import User

class ProductSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Products
		fields = "__all__"

class OrderSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Orders
		fields = "__all__"


class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = "__all__"