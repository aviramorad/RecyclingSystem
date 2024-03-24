from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import User, products, usersContacts, usersrecycling,userpoint,quizForm,mapsForm
from django import forms
from .forms import PrivateSignUpForm, CorpSignUpForm, ProductForm, UserDetailsForm, UserDetailsEditForm, UserRecyclingForm
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
        return HttpResponse("Data successfully inserted!")
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
    pagetitle = 'הוסף מוצר חדש'
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
    all_products = products.objects.all()
    return render(request, 'products_list.html', {'products': all_products})

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

    return render(request, 'user_form.html', {'form': form, 'userType': usertype})

@login_required
def userEditform(request):
    loginuser = request.user
    checkadmin = loginuser.is_superuser
    usertype = loginuser.user_type
    userID = loginuser.id
    if checkadmin:
        usertype = "a"
    #
    userObj = User.objects.get(id=userID)

    form = UserDetailsEditForm(instance=userObj) 
    if usertype == False:
        form.fields['comp_num'].widget = forms.HiddenInput()
    if request.method == 'POST':
        form = UserDetailsEditForm(request.POST, instance=userObj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/website/userform/")

    return render(request, 'edit_user_details.html', {'form': form, 'userType': usertype})

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
            messages.success(request, 'Your data has been saved successfully.')
            return HttpResponse("Data successfully inserted!")
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
    oks = usersrecycling.objects.order_by('status', 'creationDT')
    return render(request, 'display_photos.html', {'contacts': oks, 'userType': usertype})

@login_required
def approve_status(request, pk):
    item = usersrecycling.objects.get(pk=pk)
    item.status = True
    item.save()
    return HttpResponseRedirect("/website/display_photos/")


@login_required
def disapprove_status(request, pk):
    item = usersrecycling.objects.get(pk=pk)
    item.status = False
    item.save()
    return HttpResponseRedirect("/website/display_photos/")


@login_required
def Userpointform(request):
    if request.user.is_authenticated:  # בדיקה האם המשתמש מחובר
        loginuser = request.user
        checkadmin = loginuser.is_superuser
        usertype = loginuser.user_type if hasattr(loginuser, 'user_type') else None

        if checkadmin:
            usertype = "a"
        else:
            usertype = "private" if usertype == 'private' else "public"

        private_users = User.objects.filter(user_type=False)

        for user in private_users:
            if not hasattr(user, 'userpoint'):
                user.userpoint = userpoint.objects.create(user=user, points=0)
            elif user.userpoint.points is None:
                user.userpoint.points = 0
                user.userpoint.save()

        if request.method == 'POST':
            user_id = request.POST.get('user_id')
            points = request.POST.get('points')

            user = User.objects.get(id=user_id)
            user_points, created = userpoint.objects.get_or_create(user=user)
            user_points.points = points
            user_points.save()
            return HttpResponse("Data successfully inserted!")
        else:
            return render(request, 'user_point.html', {'userType': usertype, 'private_users': private_users})
    else:
        return HttpResponse("User not authenticated!")
def update_points(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        product_id = request.POST.get('product_id')
        status = request.POST.get('status')

        if status == 'True':  
            user = User.objects.get(id=user_id)
            product = products.objects.get(id=product_id)

            recycling_instance = usersrecycling.objects.create(user=user, product=product, status=True)

            user_points, created = userpoint.objects.get_or_create(user=user)

            user_points.points += 10
            user_points.save()

            return HttpResponse("Points updated successfully!")

    return HttpResponse("Invalid request")


@login_required
def quiz(request):
    return render(request, 'quiz.html')

@login_required
def check_answer(request, question_id):
    if request.method == 'POST':
        question = get_object_or_404(question, pk=question_id)
        selected_option = request.POST.get('answer')  
        correct_answer = question.correct_answer

        if selected_option == correct_answer:
            user = request.user
            user_points, created = user_points.objects.get_or_create(user=user)
            user_points.points += 10 
            user_points.save()


        return HttpResponse("Answer checked successfully!")
    else:
        return HttpResponse("Invalid request!")
    
@login_required
def maps(request):
    return render(request, 'maps.html')