from django.db import models
from django.contrib.auth.models import User, AbstractUser
from ecommerce2 import settings


class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=150, null=True)
	last_name = models.CharField(max_length=150, null=True)
	email = models.CharField(max_length=150, null=True)
	phone_number = models.CharField(max_length=20, null=True, blank=True)

	def __str__(self):
		return self.first_name or self.email

class Category(models.Model):
	name = models.CharField(max_length=150, null=True)

	def __str__(self):
		return self.name


class Product(models.Model):
	name = models.CharField(max_length=150, null=True)
	price = models.DecimalField(max_digits=5, decimal_places=2)
	digital = models.BooleanField(default=False,null=True, blank=True)
	image = models.ImageField(null=True, blank=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True, blank=True)
	wholesale_price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	box_price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	minimum_quantity = models.IntegerField(null=True, blank=True)
	def __str__(self):
		return self.name
	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_orderd = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False, blank=True, null=True)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)

	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping
	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total



class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True,blank=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total




class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True,blank=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True,blank=True)
	address = models.CharField(max_length=200, null=True)
	city = models.CharField(max_length=200, null=True)
	state = models.CharField(max_length=200, null=True)
	zipcode = models.CharField(max_length=200, null=True)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address