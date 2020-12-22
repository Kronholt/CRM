# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm, CustomerForm, CreateUserForm
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group

# ------ Home -------
#dashboard for admins in application - allows viewing of all customers and orders 

#this @ tag makes a login required to access this page, users not logged in will be redirected to login screen
@login_required(login_url='login')
@allowed_users(allowed_roles = ['admin'])
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    #these get the customer counts and order status counts to send to status.html and dashboard.html
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    is_admin = True
    context = {'is_admin':is_admin, 'orders':orders, 'customers':customers, 'total_customers':total_customers, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending,}
    return render(request, 'accounts/dashboard.html', context)

# ------ userPage -------
#this page can only be accessed by customers, and is their dashboard - allows viewing of all orders
@login_required(login_url='login')
@allowed_users(allowed_roles = ['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    template = 'accounts/user.html'
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders':orders, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
    
    
    return render(request, template, context)


# ------ accountSettings -------
#This allows the customer to view their settings and change profile picture 
@login_required(login_url='login')
@allowed_users(allowed_roles = ['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid:
            form.save()
    template = 'accounts/account_settings.html'
    context = {'form':form}

    return render(request, template, context)

# ------ register -------
#this allows new users to create an account 

#this tag prevents authenticated users from re-registering
@unauthenticated_user
def register(request):
    #this functionality stops a user from visiting register while logged int
    form = CreateUserForm()
    context={'form':form}
    template = 'accounts/register.html'
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
    
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
        else:
            messages.error(request, 'Something went wrong, please try again.')
    return render(request, template, context)

# ------ loginPage-------
#accessed by unauthenticated (not logged in) users - used to login
@unauthenticated_user
def loginPage(request):
    #this functionality stops a user from visiting login page while logged int
    form=UserCreationForm()
    context={'form':form}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')
    template = 'accounts/login.html'
    return render(request, template, context)

# ------ logoutUser-------
#logs user out of application
def logoutUser(request):
    logout(request)
    return redirect('login')

# ------ products -------
#allows admins to view the products page
@login_required(login_url='login')
@allowed_users(allowed_roles = ['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products':products})


# ------ customer -------
#This allows the admin to locate a customer's information page 
#this receives the pk from view and matches with customer
@login_required(login_url='login')
@allowed_users(allowed_roles = ['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_total = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {'customer': customer, 'orders':orders, 'order_total':order_total, 'myFilter':myFilter}
    return render(request, 'accounts/customer.html', context)

# Create your views here.

# ------ createOrders -------
#allows admin to create orders for customer's 
#this creates an order using the form specified as OrderForm in forms.py
@login_required(login_url='login')
@allowed_users(allowed_roles = ['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(id=pk)
    formSet = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    context = {'formSet':formSet}
    #received POST request from client
    if request.method == 'POST':
        formSet = OrderFormSet(request.POST, instance=customer)
        #if form is valid, save the Order to database
        if formSet.is_valid():
            formSet.save()
            return redirect('/')


    return render(request, 'accounts/order_form.html', context)

# ------ updateOrder -------
#functionality for updating an existing order
@login_required(login_url='login')
@allowed_users(allowed_roles = ['admin'])
def updateOrder(request, pk):

    order = Order.objects.get(id = pk)
    form = OrderForm(instance= order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance = order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}

    return render(request, 'accounts/order_form.html', context)

# ------ createCustomer -------
#allows the admin to create a new customer object - this feature is deprecated.
@login_required(login_url='login')
@allowed_users(allowed_roles = ['admin'])
def createCustomer(request):
    form = CustomerForm()
    context = {'form': form}
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'accounts/customer_form.html', context)


# ------ updateCustomer -------
#this allows the admin to update a customer object
@login_required(login_url='login')
@allowed_users(allowed_roles = ['admin'])
def updateCustomer(request, pk):
    
    customer = Customer.objects.get(id = pk)
    form = CustomerForm(instance= customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance = customer)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}

    return render(request, 'accounts/customer_form.html', context)

# ------ deleteCustomer -------
#allows deletion of customer object 
#use a delete template
@login_required(login_url='login')
@allowed_users(allowed_roles = ['admin'])
def deleteCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == "POST":
        customer.delete()
        return redirect('/')
    context = {'customer':customer}
    return render(request, 'accounts/delete_customer.html', context)

# ------ addOrder -------
#this function is deprecated
@login_required(login_url='login')
@allowed_users(allowed_roles = ['admin'])
def addOrder(request, pk):
    customer = Customer.objects.get(id=pk)
    

# ------ deleteOrder -------
#allows admin to delete order
@login_required(login_url='login')
@allowed_users(allowed_roles = ['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(request, 'accounts/delete.html', context)

    

