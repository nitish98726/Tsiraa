from django import forms
from .models import User , UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget= forms.PasswordInput(attrs={
        'placeholder':'Password'
    }))
    confirm_password = forms.CharField(widget= forms.PasswordInput(attrs={
        'placeholder':'Confirm password'
    }))
    phone_number = forms.CharField(required=False)
    username = forms.CharField(required=False)
    class Meta:
        model = User
        fields = ['first_name' , 'last_name' , 'username' , 'email' , 'phone_number' , 'password']
    def __init__(self , *args , **kwargs):
        super(UserForm , self).__init__(*args ,**kwargs)
        for field in self.fields:
            
            self.fields[field].widget.attrs['class'] = 'form-control fs-6'
     
    def clean(self):
        cleaned_data = super(UserForm , self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Start Typing...' , 'required':'required'}))
    
    class Meta:
        model = UserProfile
        fields = ['profile_picture'  , 'address1', 'address2',  'state' , 'city' ,'landmark' , 'pin_code' , ]
    

