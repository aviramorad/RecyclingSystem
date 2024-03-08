from django.urls import path
from . import views

urlpatterns = [
    path('addproduct/', views.addproduct, name='addproduct'),
    path('searchProduct/', views.searchProduct, name='searchProduct'),
]