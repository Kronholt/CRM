from django.forms import ModelForm
from .models import Order, Customer

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
