from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Category,Product
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth.models import Group, User
from .forms import SignUpForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout

# Create your views here.
def index(request):
	text_var='this is my first django app.'
	#return HttpResponse(text_var)
	return redirect('home:allProdCat')

#category view
def allProdCat(request, c_slug=None):
	c_page = None
	products = None
	if c_slug!= None:
		c_page = get_object_or_404(Category,slug=c_slug)
		products = Product.objects.filter(category=c_page,available=True)
	else:
		products = Product.objects.all().filter(available=True)
		"""paginator code
	paginator = Paginator(products_list, 6)
	try:
		page=int(request.Get.get('page','1'))
	except:
		page = 1
	try:
		products = paginator.page(page)
	except (EmptyPage,InvalidPage):
		products=paginator.page(paginator.num_pages)"""

	return render(request,'home/category.html',{'category':c_page,'products':products})

def ProdCatDetail(request,c_slug,product_slug):
	try:
		product = Product.objects.get(category__slug=c_slug, slug=product_slug)
	except Exception as e:
		raise 
	return render(request,'home/product.html',{'product':product})


def SignupView(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			signup_user = User.objects.get(username=username)
			customer_group = Group.objects.get(name='Customer')
			customer_group.user_set.add(signup_user)
	else:
		form = SignUpForm()
	return render(request,'accounts/signup.html', {'form':form})

def SigninView(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username,password=password)
			if user is not None:
				login(request,user)
				return redirect('home:allProdCat')
			else:
				return redirect('signup')
	else:
		form =AuthenticationForm()
	return render(request,'accounts/signin.html', {'form':form})

def SignoutView(request):
	logout(request)
	return redirect('signin')