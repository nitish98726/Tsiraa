from django import forms
from .models import Order
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name' , 'last_name' , 'phone' , 'email' , 'address_line1' , 'address_line2' , 'landmark' , 'state' , 'city' , 'zip' ]
     
    def __init__(self , *args , **kwargs):
        super(OrderForm , self).__init__(*args ,**kwargs)
        for field in self.fields:
            
            self.fields[field].widget.attrs['class'] = 'form-control'