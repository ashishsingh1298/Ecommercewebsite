from django import forms
from .models import Products

class ProductCreateForm(forms.ModelForm):
	class Meta:
		model = Products
		fields = "__all__"

class ProductSearchForm(forms.ModelForm):
   class Meta:
     model = Products
     fields = ['category', 'product_name']