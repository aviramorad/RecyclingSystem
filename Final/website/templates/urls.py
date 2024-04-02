from django.urls import path
from .import views
from .views import two_factor_verify
from django.contrib.auth import views as auth_views

urlpatterns=[
     path('register/',views.register, name='register'),
     path('privateuser_register/',views.privateuser_register.as_view(), name='privateuser_register'),
     path('corpuser_register/',views.corpuser_register.as_view(), name='corpuser_register'),
     path('login/',views.login_request, name='login'),
     path('logout/',views.logout_view, name='logout'),
     path('login/register.php', views.register_view, name='register'),
     path('addproduct/', views.addproduct, name='addproduct'),
    path('searchProduct/', views.searchProduct, name='searchProduct'),
    path('2fa-verify/', two_factor_verify, name='2fa_verify'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
          name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),
          name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view
         (template_name="password_reset_form.html"),
          name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view
         (template_name="password_reset_done.html"),
          name= "password_reset_complete"),

]   