from django.db import models

# Create your models here.
from shop.models import Products

class Cart(models.Model):
	products = models.ForeignKey(Products, null=True,blank=True,on_delete=models.CASCADE)
	total = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	active = models.BooleanField(default=True)

	def __str__(self):
		return "Cart id: %s" %(self.id)