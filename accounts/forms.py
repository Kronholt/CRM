from django.forms import ModelForm
from .models import Order, Customer
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

#this is how we specify which fields to use in the form
class OrderForm(ModelForm):
    class Meta:
        model = Order
        #this automatically requests all fields from Order to be filled in by form
        fields = '__all__'
        # we could do a list here if we do not want all fields - fields = ['customer', 'product']


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
