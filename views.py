#from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import website_products

# Create your views here.
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

