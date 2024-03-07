from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import User, website_products
from .forms import PrivateSignUpForm, CorpSignUpForm

def register(request):
    return render(request, 'register.html')

class privateuser_register(CreateView):
    model = User
    form_class = PrivateSignUpForm
    template_name = 'privateuser_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class corpuser_register(CreateView):
    model = User
    form_class = CorpSignUpForm
    template_name = 'corpuser_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html', context={'form': AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('/')


def addproduct(request):
	template = loader.get_template('addProduct.html')
	return HttpResponse(template.render())

def searchProduct(request):
	myproducts = website_products.objects.all().values()
	template = loader.get_template('searchProduct.html')
	selected_product = None

	if request.method == 'POST':
		selected_product_name = request.POST.get('browser', '')
		selected_product = website_products.objects.filter(product_name=selected_product_name).first()

		context = {
			'myproducts': myproducts,
			'selected_product': selected_product,
			}
	else:
		context = {
		  'myproducts': myproducts,
	  	}
	return HttpResponse(template.render(context, request))
