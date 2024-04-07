from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import User, products, usersContacts, usersrecycling,quizForm,mapsForm, ShopForm
from django import forms
from .forms import PrivateSignUpForm, CorpSignUpForm, ProductForm, UserDetailsForm, UserDetailsEditForm, UserRecyclingForm, storeProductForm
from django.contrib.admin.views.decorators import staff_member_required

def index(request):
    return render(request, 'index.html')


@staff_member_required
@login_required
def delete_user(request, user_id):
    if not request.user.is_superuser:
        return redirect('/website/home/')  # Redirect if user is not admin
    
    user = User.objects.get(pk=user_id)
    deleted = user.delete()
    return redirect('/website/data_user/')  # Redirect to home page or any other page

@login_required
def rate(request):
    loginuser = request.user
    checkadmin = loginuser.is_superuser
    usertype = loginuser.user_type
    if checkadmin:
        usertype = "a"
    return render(request, 'rate.html', {'userType': usertype})

@login_required
def home(request):
    loginuser = request.user
    checkadmin = loginuser.is_superuser
    usertype = loginuser.user_type
    if checkadmin:
        usertype = "a"
    return render(request, 'home.html', {'userType': usertype})

@login_required
def master(request):
    loginuser = request.user
    checkadmin = loginuser.is_superuser
    usertype = loginuser.user_type
    if checkadmin:
        usertype = "a"

    return render(request, 'master.html', {'userType': usertype})

def register(request):
    return render(request, 'register.html')

def login_view(request):
    return render(request, 'login.html')

@login_required
def contact_view(request):
    #צריך לשלוח את הסוג משתמש בכל דף כדי להציג את התפריט הנכון לפי משתמש
    loginuser = request.user
    checkadmin = loginuser.is_superuser
    usertype = loginuser.user_type
    if checkadmin:
        usertype = "a"
    #

    if request.method == 'POST':
        user_id = int(request.POST.get('user_id'))
        userObj = User.objects.get(id=user_id)
        contact_text = request.POST.get('contactText')
        new_contact = usersContacts(user=userObj, content = contact_text)
        new_contact.save()
        return HttpResponseRedirect("/website/home/")
    else:
        return render(request, 'contact_form.html', {'userType': usertype})


def display_contacts(request):
    loginuser = request.user
    checkadmin = loginuser.is_superuser
    usertype = loginuser.user_type
    if checkadmin:
        usertype = "a"
    contacts = usersContacts.objects.order_by('status', 'creationDT')
    return render(request, 'display_contacts.html', {'contacts': contacts, 'userType': usertype})

def changestatus(request, pk):
    contact = usersContacts.objects.get(id=pk)
    contact.status = True
    contact.save()
    return HttpResponseRedirect("/website/display_contacts/")


def register_view(request):
    # Your register logic goes here
    return render(request, 'register.html')


class privateuser_register(CreateView):
    model = User
    form_class = PrivateSignUpForm
    template_name = 'privateuser_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/website/home/')

class corpuser_register(CreateView):
    model = User
    form_class = CorpSignUpForm
    template_name = 'corpuser_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/website/home/')


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/website/home/")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html', context={'form': AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('/')

def addproduct(request):
    pagetitle = 'הוסף מוצר מיחזור חדש'
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or wherever you want
            return redirect('productslist')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form, 'pagetitle': pagetitle})

def updateproduct(request, pk):
    pagetitle = 'עדכון פרטי מוצר'
    product = products.objects.get(id=pk)
    form = ProductForm(instance=product) # prepopulate the form with an existing band
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            # Redirect to a success page or wherever you want
            return redirect('productslist')
    
    return render(request, 'product_form.html', {'form': form, 'pagetitle': pagetitle})

    
def searchProduct(request):
	myproducts = products.objects.all().values()
	template = loader.get_template('searchProduct.html')

	if request.method == 'POST':
		selected_product_name = request.POST.get('browser', '')
		selected_product = products.objects.filter(product_name=selected_product_name).first()

		context = {
			'myproducts': myproducts,
			'selected_product': selected_product,
			}
	else:
		context = {
		  'myproducts': myproducts,
	  	}
	return HttpResponse(template.render(context, request))

def productslist(request):
    recycling_products = products.objects.filter(Product_type=False)
    return render(request, 'products_list.html', {'products': recycling_products})

@login_required
def userform(request):
    #צריך לשלוח את הסוג משתמש בכל דף כדי להציג את התפריט הנכון לפי משתמש
    loginuser = request.user
    checkadmin = loginuser.is_superuser
    usertype = loginuser.user_type
    userID = loginuser.id
    if checkadmin:
        usertype = "a"
    #
    userObj = User.objects.get(id=userID)

    form = UserDetailsForm(instance=userObj) # prepopulate the form with an existing band
    if usertype == False:
        form.fields['comp_num'].widget = forms.HiddenInput()

    return render(request, 'user_form.html', {'form': form, 'userType': usertype, 'checkAdmin': checkadmin})

@login_required
def userEditform(request):
    #צריך לשלוח את הסוג משתמש בכל דף כדי להציג את התפריט הנכון לפי משתמש
    loginuser = request.user
    checkadmin = loginuser.is_superuser
    usertype = loginuser.user_type
    userID = loginuser.id
    if checkadmin:
        usertype = "a"
    #
    userObj = User.objects.get(id=userID)

    form = UserDetailsEditForm(instance=userObj) # prepopulate the form with an existing band
    if usertype == False:
        form.fields['comp_num'].widget = forms.HiddenInput()
    if request.method == 'POST':
        form = UserDetailsEditForm(request.POST, instance=userObj)
        if form.is_valid():
            form.save()
            # Redirect to a success page or wherever you want
            return HttpResponseRedirect("/website/home/")

    return render(request, 'edit_user_details.html', {'form': form, 'userType': usertype})

@login_required
def recycling_bin(request):
    #צריך לשלוח את הסוג משתמש בכל דף כדי להציג את התפריט הנכון לפי משתמש
    loginuser = request.user
    checkadmin = loginuser.is_superuser
    usertype = loginuser.user_type
    userID = loginuser.id
    userLocation = loginuser.location
    if checkadmin:
        usertype = "a"
    
    recycling_data = usersrecycling.objects.filter(user__location=userLocation)  # ניגשנו לשדה בתוך שדה עם __
    context = {
        
        'recycling_data': recycling_data,
        'userType': usertype,
    }
    return render(request, 'recycling_bin.html', context)

@login_required
def my_authority(request):
    #צריך לשלוח את הסוג משתמש בכל דף כדי להציג את התפריט הנכון לפי משתמש
    loginuser = request.user
    checkadmin = loginuser.is_superuser
    usertype = loginuser.user_type
    userID = loginuser.id
    userLocation = loginuser.location
    if checkadmin:
        usertype = "a"
    
    recycling_data = User.objects.filter(location=userLocation)  # ניגשנו לשדה בתוך שדה עם __
    context = {
        
        'recycling_data': recycling_data,
        'userType': usertype,
    }
    return render(request, 'my_authority.html', context)

@login_required
def data_recycling(request):
    #צריך לשלוח את הסוג משתמש בכל דף כדי להציג את התפריט הנכון לפי משתמש
    loginuser = request.user
    checkadmin = loginuser.is_superuser
    usertype = loginuser.user_type
    userID = loginuser.id
    userLocation = loginuser.location
    if checkadmin:
        usertype = "a"
    
    recycling_data = usersrecycling.objects.all()  # ניגשנו לשדה בתוך שדה עם __
    context = {
        
        'recycling_data': recycling_data,
    }
    return render(request, 'data_recycling.html', context)

@login_required
def data_user(request):
    #צריך לשלוח את הסוג משתמש בכל דף כדי להציג את התפריט הנכון לפי משתמש
    loginuser = request.user
    checkadmin = loginuser.is_superuser
    usertype = loginuser.user_type
    userID = loginuser.id
    userLocation = loginuser.location
    if checkadmin:
        usertype = "a"
    
    recycling_data = User.objects.all()  # ניגשנו לשדה בתוך שדה עם __
    context = {
        
        'recycling_data': recycling_data,
    }
    return render(request, 'data_user.html', context)

@login_required
def userRecyclingform(request):
    loginuser = request.user
    checkadmin = loginuser.is_superuser
    usertype = loginuser.user_type
    userID = loginuser.id
    if checkadmin:
        usertype = "a"

    if request.method == 'POST':
        form = UserRecyclingForm(request.POST, request.FILES)
        if form.is_valid():
            user_recycling_instance = form.save(commit=False)
            user_recycling_instance.user = request.user
            user_recycling_instance.save()
        return HttpResponseRedirect("/website/userrecycling/")
    else:
        form = UserRecyclingForm()

    return render(request, 'user_recycling.html', {'form': form, 'userType': usertype})

@login_required
def display_photos(request):
    loginuser = request.user
    checkadmin = loginuser.is_superuser
    usertype = loginuser.user_type
    if checkadmin:
        usertype = "a"
    oks = usersrecycling.objects.filter(status=0).order_by('creationDT')
    return render(request, 'display_photos.html', {'contacts': oks, 'userType': usertype})

@login_required
def approve_status(request, pk, userID):
    recycling_row = usersrecycling.objects.get(pk=pk)
    recycling_user = User.objects.get(id=userID)
    recycling_row.status = 1
    recycling_row.save()
    oldPoints = recycling_user.points
    newPoints = oldPoints + 10
    recycling_user.points = newPoints
    recycling_user.save()
    return HttpResponseRedirect("/website/display_photos/")


@login_required
def disapprove_status(request, pk):
    recycling_row = usersrecycling.objects.get(pk=pk)
    recycling_row.status = 2
    recycling_row.save()
    return HttpResponseRedirect("/website/display_photos/")



@login_required
def quiz(request):
    return render(request, 'quiz.html')

def view(request):
    return render(request, 'maps.html')

 
def about(request):
    return render(request, 'about.html')

    
def maps(request):
    return render(request, 'maps.html')

    
def recycle_bins(request):
    return render(request, 'recycle.html')



@login_required
def addstoreproduct(request):
    loginuser = request.user
    checkadmin = loginuser.is_superuser
    usertype = loginuser.user_type
    if checkadmin:
        usertype = "a"
    pagetitle = 'הוספת מוצר חנות'
    if request.method == 'POST':
        form = storeProductForm(request.POST, request.FILES)
        if form.is_valid():
            store_product_instance = form.save(commit=False)
            store_product_instance.Product_type = True
            store_product_instance.save()

            # Redirect to a success page or wherever you want
            return redirect('adminstore')
    else:
        form = storeProductForm()
    return render(request, 'store_product_form.html', {'form': form, 'pagetitle': pagetitle, 'userType': usertype})


@login_required
def updatestoreproduct(request, pk):
    loginuser = request.user
    checkadmin = loginuser.is_superuser
    usertype = loginuser.user_type
    if checkadmin:
        usertype = "a"
    pagetitle = 'עדכון פרטי מוצר'
    product = products.objects.get(id=pk)
    form = storeProductForm(instance=product) # prepopulate the form with an existing band
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()

            # Redirect to a success page or wherever you want
            return redirect('adminstore')
    return render(request, 'store_product_form.html', {'form': form, 'pagetitle': pagetitle, 'userType': usertype})



@login_required
def store(request):
    loginuser = request.user
    checkadmin = loginuser.is_superuser
    usertype = loginuser.user_type
    if checkadmin:
        usertype = "a"
    store_products = products.objects.filter(Product_type=True)
    return render(request, 'store.html', {'products': store_products, 'userType': usertype, 'userObj': loginuser})

@login_required
def updatepoints(request, pk):
    productObj = products.objects.get(pk=pk)
    loginuser = request.user
    pValue = productObj.value
    oldPoints = loginuser.points
    newPoints = oldPoints - pValue
    loginuser.points = newPoints
    loginuser.save()

    return HttpResponseRedirect("/website/store/")

@login_required
def updatepointsquiz(request, pVal):
    loginuser = request.user
    oldPoints = loginuser.points
    newPoints = oldPoints + pVal
    loginuser.points = newPoints
    loginuser.save()
    return HttpResponseRedirect("/website/home/")

@login_required
def adminstore(request):
    loginuser = request.user
    checkadmin = loginuser.is_superuser
    usertype = loginuser.user_type
    if checkadmin:
        usertype = "a"
    store_products = products.objects.filter(Product_type=True)
    return render(request, 'adminStore.html', {'products': store_products, 'userType': usertype})


