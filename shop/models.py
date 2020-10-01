from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

from PIL import Image, ImageDraw, ImageFont

# Create your models here.
class ProductQueryset(models.query.QuerySet):
	
	def active(self):
		return self.filter(active=True)

class ProductManager(models.Manager):

	def get_queryset(self):
		return ProductQueryset(self.model,using=self._db)

	def all(self):
		return self.get_queryset().active()


class Products(models.Model):
	product_id = models.AutoField
	product_name = models.CharField(max_length=50)
	category = models.CharField(max_length=50, default="")
	subcategory = models.CharField(max_length=50,default="")
	desc = models.TextField(null=True ,blank=True, max_length=300)
	price = models.IntegerField(default=0)
	# sale_price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
	gst = models.IntegerField(default=0)
	prodviews = models.IntegerField(default=0) 
	pub_date = models.DateField(auto_now_add=True, auto_now=False)
	updated = models.DateField(auto_now_add=False, auto_now=True)
	image = models.ImageField(upload_to="shop/images",default="shop/images/NIL.png")
	active = models.BooleanField(default=True)

	objects = ProductManager()

	def __str__(self):
		return self.product_name

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		img = Image.open(self.image.path)

		if img.height > 300 or img.weight > 250:
			output_size = (220,180)
			img.thumbnail(output_size)
			d1 = ImageDraw.Draw(img)
			fontsize = 12
			font = ImageFont.truetype("arial.ttf", fontsize)
			d1.text((50, 50), "Image by IE cart",font=font, fill =(222, 163, 69))
			img.save(self.image.path)

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		print('URL:', url)
		return url

class ViewImage(models.Model):
	product = models.ForeignKey(Products, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	viewimage = models.ImageField(upload_to="shop/images",default="shop/images/NIL.png")
	featured = models.BooleanField(default=False)
	thumbnail = models.BooleanField(default=False)
	updated = models.DateField(auto_now_add=False, auto_now=True)
	active = models.BooleanField(default=True)
	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		img = Image.open(self.viewimage.path)

		if img.height > 1300 or img.weight > 1250:
			output_size = (350,450)
			img.thumbnail(output_size)
			d1 = ImageDraw.Draw(img)
			font = ImageFont.truetype("arial.ttf", 32)
			d1.text((450, 350), "Image by IE cart",font=font, fill =(199, 72, 238))
			img.save(self.viewimage.path)
		
			

	@property
	def imageURL(self):
		try:
			url = self.viewimage.url
		except:
			url = ''
		print('URL:', url)
		return url

class ProductStock(models.Model):
	product = models.ForeignKey(Products, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=0)
	updated = models.DateField(auto_now_add=False, auto_now=True)
	active = models.BooleanField(default=False)
	def __str__(self):
		return self.product.product_name

class VariationManager(models.Manager):
	def all(self):
		return super(VariationManager, self).filter(active=True)
	def sizes(self):
		return self.all().filter(var_category='size')
	def colors(self):
		return self.all().filter(var_category='color')
	def packages(self):
		return self.all().filter(var_category='package')

VAR_CATEGORIES = (
	('size','size'),
	('color','color'),
	('package', 'package')
	)

class Variation(models.Model):
	product = models.ForeignKey(Products,on_delete=models.CASCADE)
	var_category = models.CharField(max_length=120, choices=VAR_CATEGORIES, default='size')
	title = models.CharField(max_length=120)	
	image = models.ForeignKey(ViewImage,on_delete=models.CASCADE, null=True, blank=True)
	price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
	updated = models.DateField(auto_now_add=False, auto_now=True)
	active = models.BooleanField(default=True)

	objects = VariationManager()

	def __str__(self):
		return self.title


class Contact(models.Model):
	msz_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	email = models.CharField(max_length=50, default="")
	phone = models.IntegerField(default="")
	desc = models.CharField(max_length=300, default="")
	contact_date = models.DateField(auto_now_add=True, auto_now=False, null=True)
	def __str__(self):
		return self.desc[0:20]


STATUS_CHOICES=(
	("Started", "Started"),
	("Aborted","Aborted"),
	("Finished","Finished"),
	)

class Orders(models.Model):
	order_id = models.AutoField(primary_key=True)
	item_json = models.CharField(max_length=5000)
	user = models.ForeignKey(User,on_delete=models.CASCADE,default="")
	amount = models.FloatField(default=0)
	name = models.CharField(max_length=50)
	email = models.CharField(max_length=50)
	address = models.CharField(max_length=100)
	address2 = models.CharField(max_length=100, default="")
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=50)
	zip_code = models.IntegerField()
	phone = models.IntegerField()
	special = models.TextField(max_length=5000, default=10)
	order_date = models.DateField(auto_now_add=True, auto_now=False, null=True)
	status = models.CharField(max_length=120, choices=STATUS_CHOICES, default="Started")

	def __str__(self):
		return self.name


class OrderUpdate(models.Model):
	update_id = models.AutoField(primary_key=True)
	order_id = models.IntegerField(default="")
	update_desc = models.CharField(max_length=5000)
	timestamp = models.DateField(auto_now_add=True)
	
	def __str__(self):
		return self.update_desc[0:44]  +"..."
	
class ProdComment(models.Model):
	sno = models.AutoField(primary_key=True)
	comment = models.TextField(max_length=1000, blank=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Products, on_delete=models.CASCADE)
	parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
	timestamp = models.DateTimeField(default=now)
	def __str__(self):
		return self.comment[0:15] +"..." + " by " + self.user.username

class Profile(models.Model):
	user = models.OneToOneField(to=User, on_delete=models.CASCADE)
	order = models.ForeignKey(to=Orders, on_delete=models.CASCADE, null=True, blank=True)
	def __str__(self):
		return "%s (%s)" % (self.user.username, self.order)


