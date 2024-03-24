from django.urls import path
from . import views

urlpatterns = [
    path('master/', views.master, name='master'),
    path('contact_view/', views.contact_view, name='contact_view'),
    path('display_contacts/', views.display_contacts, name='display_contacts'),
    path('register/', views.register, name='register'),
    path('privateuser_register/', views.privateuser_register.as_view(), name='privateuser_register'),
    path('corpuser_register/', views.corpuser_register.as_view(), name='corpuser_register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('searchProduct/', views.searchProduct, name='searchProduct'),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('productslist/', views.productslist, name='productslist'),
    path('updateproduct/<int:pk>/', views.updateproduct, name='updateproduct'),
    path('changestatus/<int:pk>/', views.changestatus, name='changestatus'),
    path('approve_status/<int:pk>/', views.approve_status, name='approve_status'),
    path('disapprove_status/<int:pk>/', views.disapprove_status, name='disapprove_status'),
    path('userform/', views.userform, name='userform'),
    path('userEditform/', views.userEditform, name='userEditform'),
    path('userrecycling/', views.userRecyclingform, name='userrecycling'),
    path('display_photos/', views.display_photos, name='display_photos'),
    path('User_point/', views.Userpointform, name='User_point'),
    path('quiz/', views.quiz, name='quiz'),
    path('maps/', views.maps, name='maps'),




]
