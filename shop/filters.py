import django_filters

from .models import Products

class ProductFilter(django_filters.FilterSet):

	class Meta:
		model = Products
		fields = [
				'product_name',
				'category',
				'subcategory',
				'gst',
				]