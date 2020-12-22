from django.contrib import admin
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
    path('user/', views.userPage, name='user_page')
    
] 