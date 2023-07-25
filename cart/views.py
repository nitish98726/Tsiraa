from django.shortcuts import render , redirect
from django.http import HttpResponse , JsonResponse
from .models import CartItem , Cart
from store.models import Product
from .context_processors import cart_counter , amount_calculator
from django.contrib.auth.decorators import login_required
from orders.forms import OrderForm
# Create your views here.
def cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def cart(request , cart_items =None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user).order_by('-created_at')
        else:
            cart = Cart.objects.get(cart_id = cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart).order_by('-created_at')
    except:
        pass
    context = {
        'cart_items':cart_items,
    }
    return render(request , 'cart/cart.html' , context)


def add_cart(request ,product_id):
    user = request.user
    product = Product.objects.get(id= product_id)
    
    if user.is_authenticated:
        if request.method=="POST":
            try:
                           
                size= request.POST['size']
            except:
                
                size = None
            try:
                color = request.POST['color']            
                
            except:
                color = None
                
            
            quantity = request.POST['items']
            product_variation = [product , size , color]
            cart_items_exists = CartItem.objects.filter(product = product  , user=request.user).exists()
            # print(cart_items_exists)
            if cart_items_exists:
                cart_item = CartItem.objects.filter(product=product , user=user)
                ex_var_list = []
                id = []
                for item in cart_item:
                    item_list = [item.product , item.size , item.color]
                    ex_var_list.append(item_list)
                    id.append(item.id)
                
                if product_variation in ex_var_list:
                    print("same combination exists")
                    index = (ex_var_list.index(product_variation))
                    ex_cart_item =CartItem.objects.get(product=product , id =id[index])
                    ex_cart_item.quantity += int(quantity)
                    ex_cart_item.save()
                    
                else:
                    print('new_product')
                    new_item = CartItem.objects.create(
                    user = request.user,
                    product=product,
                    quantity = quantity,
                    color = color,
                    size = size,
                    is_active = True,
                    )
                    new_item.save()
            else:
                new_item = CartItem.objects.create(
                    user = request.user,
                    product=product,
                    quantity = quantity,
                    color = color,
                    size = size,
                    is_active = True,
                )
                new_item.save()
    # User Not authenticated
    else:
        if request.method=="POST":
            try:
                           
                size= request.POST['size']
            except:
                
                size = None
            try:
                color = request.POST['color']            
                
            except:
                color = None
                
            
            quantity = request.POST['items']
            product_variation = [product , size , color]
           
            try:
                cart = Cart.objects.get(cart_id = cart_id(request))
            except Cart.DoesNotExist:
                cart = Cart.objects.create(cart_id = cart_id(request))
                cart.save()
            cart_items_exists = CartItem.objects.filter(product=product , cart= cart).exists()
            if cart_items_exists:
                cartitem = CartItem.objects.filter(product=product , cart=cart)
                ex_var_list = []
                id = []
                for item in cartitem:
                    item_list = [item.product , item.size , item.color]
                    ex_var_list.append(item_list)
                    id.append(item.id)
                
                if product_variation in ex_var_list:
                    print("same combination exists")
                    index = (ex_var_list.index(product_variation))
                    ex_cart_item =CartItem.objects.get(product=product , id =id[index])
                    ex_cart_item.quantity += int(quantity)
                    ex_cart_item.save()
                    
                else:
                    print('new_product')
                    new_item = CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity = quantity,
                    color = color,
                    size = size,
                    is_active = True,
                    )
                    new_item.save()
            else:
                new_item = CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity = quantity,
                    color = color,
                    size = size,
                    is_active = True,
                )
                new_item.save()
    return redirect('cart')

    

def add_cart_ajax(request , cart_item_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            cartitem = CartItem.objects.get(id = cart_item_id)
            cartitem.quantity +=1
            cartitem.save()
            item_total = cartitem.item_wise_total()
            print(item_total)
            return JsonResponse({
                'status':'Success',
                'message':"Cart Item Increased",
                'cart_counter':cart_counter(request),
                'qty':cartitem.quantity,
                'cart_amount':amount_calculator(request),
                'item_wise_total':item_total,
            })
        except:
            return JsonResponse({
                'status':'Failed',
                'message':"Cart Item does not exist",

            })
def decrease_cart(request , cart_item_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        qty =0
        item_total=0
        try:
            cartitem = CartItem.objects.get(id = cart_item_id)
            if cartitem.quantity <=1:
                cartitem.delete()
                  
            else:
                cartitem.quantity -=1
                cartitem.save()
                qty = cartitem.quantity
                item_total = cartitem.item_wise_total()
            return JsonResponse({
                'status':'Success',
                'message':'Cart Item Decreased',
                'cart_counter':cart_counter(request),
                'qty':qty,
                'cart_amount':amount_calculator(request),
                'item_wise_total':item_total,

            })
        except:
            return JsonResponse({
                'status':'Failed',
                'message':'No such cart Item Exists'
            })
    # return HttpResponse('decrease cart working')

def remove_cart(request , cart_item_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            cartitem = CartItem.objects.get(id = cart_item_id)
            cartitem.delete()
            return JsonResponse({
                'status':'Success',
                'message':"Cart Item deleted Succesfully",
                'cart_counter':cart_counter(request),
                'qty':0,
                'cart_amount':amount_calculator(request),
            })
        except:
            return JsonResponse({
                'status':"Failed",
                'message':"No such Cart Item Exists",
                
            })

@login_required(login_url = 'login')    
def checkout(request):
    cartitem = CartItem.objects.filter(user=request.user).exists()
    # print(cartitem)
    if cartitem:
        form = OrderForm()
        context = {
            'form':form,
        }
        return render(request , 'cart/checkout.html' , context)
    else:
        return redirect('home')