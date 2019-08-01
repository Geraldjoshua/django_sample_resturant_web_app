from django.shortcuts import render,redirect, get_object_or_404
from home.models import Product
from . models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from . forms import NameForm
from order.models import Order, OrderItem

# Create your views here.




def _cart_id(request):
	cart = request.session.session_key
	if not cart:
		cart = request.session.create()
	return cart

def add_cart(request,product_id):
	product = Product.objects.get(id=product_id)
	try:
		cart = Cart.objects.get(cart_id=_cart_id(request))
	except Cart.DoesNotExist:
		cart = Cart.objects.create(
				cart_id = _cart_id(request)
			)
		cart.save(),
	try:
		cart_item = CartItem.objects.get(product=product,cart=cart)
		if cart_item.quantity < cart_item.product.stock:
			cart_item.quantity += 1
		cart_item.save()
	except CartItem.DoesNotExist:
		cart_item = CartItem.objects.create(
					product = product,
					quantity = 1,
					cart = cart
			)
		cart_item.save()
	# return redirect('cart:cart_detail')
	return redirect('home:allProdCat')

def cart_detail(request,total=0,counter=0, cart_items = None):
	try:
		cart = Cart.objects.get(cart_id=_cart_id(request))
		cart_items = CartItem.objects.filter(cart=cart,active=True)
		#global sum_total
		for cart_item in cart_items:
			total += (cart_item.product.price * cart_item.quantity)
			counter += cart_item.quantity
		#sum_total=total
	except ObjectDoesNotExist:
		pass

	return render(request,'cart.html',dict(cart_items = cart_items, total = total, counter= counter))


def cart_remove(request, product_id):
	cart = Cart.objects.get(cart_id=_cart_id(request))
	product = get_object_or_404(Product,id=product_id)
	cart_item = CartItem.objects.get(product=product, cart=cart)
	if cart_item.quantity > 1:
		cart_item.quantity -=1
		cart_item.save()
	else:
		cart_item.delete()
	return redirect('cart:cart_detail')

def full_remove(request, product_id):
	cart = Cart.objects.get(cart_id=_cart_id(request))
	product = get_object_or_404(Product,id=product_id)
	cart_item = CartItem.objects.get(product=product, cart=cart)
	cart_item.delete()
	return redirect('cart:cart_detail')

def checkout(request):
	if request.method == 'POST':
		form = NameForm(request.POST)
		if form.is_valid():
			#form.save()
			sum_total=0
			cart = Cart.objects.get(cart_id=_cart_id(request))
			cart_items = CartItem.objects.filter(cart=cart,active=True)
			for cart_item in cart_items:
				sum_total += (cart_item.product.price * cart_item.quantity)
			#global sum_total
			total = sum_total
			emailAddress = form.cleaned_data.get('Email_address')
			customer = form.cleaned_data.get('First_name')+' '+ form.cleaned_data.get('Last_name')
			country= form.cleaned_data.get('Country')
			city= form.cleaned_data.get('City')
			street_address= form.cleaned_data.get('Street_address')
			province= form.cleaned_data.get('Province')
			zip_code= form.cleaned_data.get('Zip')
			phone_number= form.cleaned_data.get('Phone')
			cash_or_card= form.cleaned_data.get('cash_or_card')
			print(cash_or_card)
			"""order form creation"""
			try:
				order_details = Order.objects.create(
						total = sum_total,
						emailAddress = emailAddress,
						customer = customer,
						country= country,
						city= city,
						street_address= street_address,
						province= province,
						zip_code= zip_code,
						phone_number= phone_number,
						cash_or_card= cash_or_card
					)
				order_details.save()
				for order_item in cart_items:
					oi = OrderItem.objects.create(
							product = order_item.product.name,
							quantity = order_item.quantity,
							price = order_item.product.price,
							order = order_details
						)
					oi.save()

					"""reduce product stock"""
					products = Product.objects.get(id=order_item.product_id)
					products.stock = int(order_item.product.stock - order_item.quantity)
					products.save()
					order_item.delete()
				return redirect('order:thanks',order_details.id)

			except ObjectDoesNotExist:
				pass


			# global First_name
			# First_name=form.cleaned_data.get('First_name')
			# global Last_name
			# Last_name=form.cleaned_data.get('Last_name')
			# global Country
			# Country=form.cleaned_data.get('Country')
			# global City
			# City=form.cleaned_data.get('City')
			# global Street_address
			# Street_address=form.cleaned_data.get('Street_address')
			# global Province
			# Province=form.cleaned_data.get('Province')
			# global Zip
			# Zip=form.cleaned_data.get('Zip')
			# global Email_address
			# Email_address=form.cleaned_data.get('Email_address')
			# global Cash_or_card
			# Cash_or_card=form.cleaned_data.get('Cash_or_card')
	else:
		form = NameForm()
		
	return render(request,'checkout.html', {'form':form})