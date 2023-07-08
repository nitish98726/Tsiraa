from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse
from .forms import UserForm , UserProfileForm
from django.contrib import messages , auth
from .models import User
import random
from .utils import send_password_reset_mail , user_activation

from cart.models import Cart , CartItem
# Create your views here.

#Test page
def accounts(request):
    return HttpResponse("this is accounts page")

# cart id function
def cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

#Login Functionality
def login(request):
    if request.user.is_authenticated:
        messages.warning(request , "You are already Logged In ")
        return redirect('home')
    if request.method =="POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email , password=password)
        # print(user , email , password)
        
        if user is not None:
            # Moving items of logged in user to logged in cart
            try:
                
                cart = Cart.objects.get(cart_id=cart_id(request))
                
                cartitems = CartItem.objects.filter(cart=cart)
                product_variations = []
                id_nouser = []
                if cartitems is not None:
                    
                    for item in cartitems:
                        item_list = [item.product , item.size , item.color , item.quantity ]
                        product_variations.append(item_list) #here this list contains 4 items in each list
                        id_nouser.append(item.id)
                    
                    user_cartitems = CartItem.objects.filter(user=user)
                    print(user_cartitems)
                    ex_var_list  =[] #here each sublist conatins three items
                    id_user = []
                    for item in user_cartitems:
                        item_list = [item.product , item.size , item.color]
                        ex_var_list.append(item_list)
                        id_user.append(item.id)
                    
                    for item in product_variations:
                        
                        if item[:3] in ex_var_list:
                            
                            index = ex_var_list.index(item[:3])
                            prod_id = id_user[index]
                            new_cart = CartItem.objects.get(user=user , id=prod_id)
                            new_cart.quantity += int(item[3])
                            new_cart.save()
                        else:
                            
                            index_cart_item_nouser = product_variations.index(item)
                            prod_id_nouser = id_nouser[index_cart_item_nouser]
                            cartitem_nouser = CartItem.objects.get(id = prod_id_nouser,cart=cart)
                            
                            cartitem_nouser.user = user
                            cartitem_nouser.save()
                
            except:
                pass
            auth.login(request , user)
            messages.success(request , "You are Logged in")
            return redirect('home')
        
        else:
            messages.error(request , 'Login Credentials Donot Match')
            return redirect('login')


    return render(request , 'accounts/login.html')

# Register User Functionality
def register(request):
    if request.method =='POST':
        form = UserForm(request.POST)
        if form.is_valid():
            
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = email.split('@')[0]+'#'+str(random.randint(0,30))
            password = form.cleaned_data['password']
           
            user = User.objects.create_user(email=email , password=password , first_name=first_name ,last_name=last_name , username=username )
            user.is_active = True
            user.save()
            
            user.username = user.username.split('#')[0]+str(user.id)
            user.save()
            messages.success(request ,'Your account has been Successfully Created')
            return redirect('login')

            
        else:
            print(form.errors)
    else:       
        form = UserForm()
    
    
    context = {
        'form':form,
    }
    return render(request , 'accounts/register.html' , context)

# lOGOUT FUNCTIONALITY
def logout(request):
    auth.logout(request)
    messages.info(request , "You have been Successfully Logged Out")
    return render(request , 'home.html')

def forgotPassword(request):
    if request.method =='POST':
        email = request.POST['email']
        try:
            user = get_object_or_404(User , email=email)
            # send password reset email
            send_password_reset_mail(request , user)
            messages.info(request , 'An account Reset Email has been sent to Your registered Email id')
            return redirect('login')
        except :
            messages.error(request , 'Email ID entered is not registered')


    return render(request , 'accounts/forgotPassword.html')

def reset_password_validate(request , uidb64,token):
    try:
        user_activation(request ,uidb64 , token) #imported from utils.py
        
        return redirect("reset_password")
    
    except:
        messages.error(request , "Invalid Link")
        return redirect("home")
    
def reset_password(request):
    if request.method == "POST":
        password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk = pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request , "Password Reset Successfull")
            return redirect('login')
        else:
            messages.error(request , "Passwords do not Match .Kinldy re-enter carefully")
    return render(request , 'accounts/reset_password.html')