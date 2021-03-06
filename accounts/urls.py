from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.products, name="products"),
    #using <str:pk> allows for dynamic link based on customer id look at view for application
    path('customer/<str:pk>/', views.customer, name="customer"),
    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('create_customer/', views.createCustomer, name="create_customer"),
    path('update_customer/<str:pk>/', views.updateCustomer, name="update_customer"),
    path('add_order/<str:pk>/', views.addOrder, name="add_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
    path('register/', views.register, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('user/', views.userPage, name='user_page'),
    path('settings/', views.accountSettings, name="account_settings"),
    #these views are imported from auth to reset the password the names are required by django docs
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name="password_reset_complete"),
    
] 