from django.db import models

# Create your models here.
class Order(models.Model):
	token = models.CharField(max_length=250,blank=True,)
	total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='R order total')
	emailAddress = models.EmailField(max_length=250,blank=True, verbose_name='email Address')
	created = models.DateTimeField(auto_now_add=True)
	customer = models.CharField(max_length=250,blank=True)
	country= models.CharField(max_length=250,blank=True)
	city= models.CharField(max_length=250,blank=True)
	street_address= models.CharField(max_length=250,blank=True)
	province= models.CharField(max_length=250,blank=True)
	zip_code= models.CharField(max_length=250,blank=True)
	phone_number= models.IntegerField(blank=True)
	cash_or_card= models.CharField(max_length=250,blank=True, verbose_name='payment mode on delivery')

	class Meta:
		db_table= 'Order'
		ordering = ['-created']

	def __str__(self):
		return str(self.id)


class OrderItem(models.Model):
	product=models.CharField(max_length=250)
	quantity = models.IntegerField()
	price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='R Price')
	order = models.ForeignKey(Order, on_delete=models.CASCADE)

	class Meta:
		db_table= 'OrderItem'


	def sub_total(self):
		return self.quantity * self.price		

	def __str__(self):
		return self.product

