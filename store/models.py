from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=150, null=True)
	email = models.CharField(max_length=150, null=True)

	def __str__(self):
		return self.name


class Product(models.Model):
	name = models.CharField(max_length=150, null=True)
	price = models.FloatField()
	digital = models.BooleanField(default=False,null=True, blank=True)

	def __str__(self):
		return self.name

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_orderd = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False, blank=True, null=True)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)



class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True,blank=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)


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