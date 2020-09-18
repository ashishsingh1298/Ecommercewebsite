from django.contrib import admin
from .forms import ProductCreateForm
from .models import Products, Variation, ProductStock
from .models import ProdComment
from .models import Contact
from .models import Orders
from .models import OrderUpdate
from .models import Profile
from .models import ViewImage

class ProductCreateAdmin(admin.ModelAdmin):
	date_hierarchy = 'pub_date'
	list_display = ['category','subcategory','product_name','price', 'pub_date', 'active']
	# form = ProductCreateForm
	list_filter = ['subcategory', 'active']
	search_fields = ['category','product_name','subcategory']
	list_editable = ['price', 'active']
	class Meta:
		model = Products

class ProdCommentCreateAdmin(admin.ModelAdmin):
	date_hierarchy = 'timestamp'
	list_display = ['user','product', 'timestamp','comment']
	list_filter = ['user']
	class Meta:
		model = ProdComment

class OrderUpdateCreateAdmin(admin.ModelAdmin):
	date_hierarchy = 'timestamp'
	list_display = ['order_id', 'timestamp','__str__']
	class Meta:
		model = OrderUpdate
	
class ContactCreateAdmin(admin.ModelAdmin):
	date_hierarchy = 'contact_date'
	list_display = ['name', 'email', 'phone','__str__']
	class Meta:
		model = Contact	

class ViewImageCreateAdmin(admin.ModelAdmin):
	date_hierarchy = 'updated'
	list_display = ['product','featured', 'active']
	class Meta:
		model = ViewImage	

class OrderAdmin(admin.ModelAdmin):
	date_hierarchy = 'order_date'
	list_display = ['name','amount', 'state', 'status']
	list_filter = ['user','status','state']
	search_fields = ['name','user']
	class Meta:
		model = Orders

class ProductStockAdmin(admin.ModelAdmin):
	date_hierarchy = 'updated'
	list_display = ['product','quantity', 'active']
	list_filter = ['active']
	search_fields = ['quantity']
	class Meta:
		model = ProductStock

# Register your models here.
admin.site.register(Products,ProductCreateAdmin)
admin.site.register(Contact,ContactCreateAdmin)
admin.site.register(ProdComment,ProdCommentCreateAdmin)
admin.site.register(Orders,OrderAdmin)
admin.site.register(OrderUpdate,OrderUpdateCreateAdmin)
admin.site.register(Profile)
admin.site.register(ViewImage,ViewImageCreateAdmin)
admin.site.register(Variation)
admin.site.register(ProductStock,ProductStockAdmin)