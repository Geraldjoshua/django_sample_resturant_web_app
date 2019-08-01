from django.contrib import admin
from . models import Order, OrderItem

# Register your models here.

class OrderItemAdmin(admin.TabularInline):
	model = OrderItem
	fieldsets = [
		('product',{'fields':['product'],}),
		('quantity',{'fields':['quantity'],}),
		('price',{'fields':['price'],}),
	]
	readonly_fields = ['product','quantity','price']
	can_delete = False
	max_num=0
	template = 'admin/order/tabular.html'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ['id','customer','emailAddress','created']
	list_display_links = ['id','customer']
	search_fields = ['id','customer','emailAddress']
	readonly_fields = ['id','token','emailAddress','total','created','customer',
					'street_address','country','city','cash_or_card','phone_number','zip_code','province']

	fieldsets = [
		('ORDER INFORMATION',{'fields':['id','token','total','cash_or_card','created'],}),
		('DELIVERY INFORMATION',{'fields':['customer', 'phone_number','street_address','city','country','zip_code','province'],}),
	]

	inlines = [
		OrderItemAdmin,
	]

	def has_delete_permission(self, request, obj=None):
		return False


	def has_add_permission(self,request):
		return False



