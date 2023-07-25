from django.shortcuts import render , redirect
from django.http import HttpResponse , JsonResponse
from .forms import OrderForm
from .models import Order , Payment , OrderProduct
from cart.context_processors import amount_calculator
import razorpay
from datetime import datetime
from Tsiraa.settings import RZP_KEY_ID , RZP_KEY_SECRET
from cart.models import CartItem
from django.contrib.auth.decorators import login_required
from accounts.utils import send_notification
from store.models import Product , Size , Color

# Create your views here.

client =  razorpay.Client(auth=(RZP_KEY_ID ,RZP_KEY_SECRET))

def generate_order_number(pk):
    now = datetime.now()
    current_date = (now.strftime(r"%Y%m%d%H%M%S"))
    order_number = current_date + str(pk)
    return order_number
@login_required(login_url='login')
def order(request):
    cartitems = CartItem.objects.filter(user=request.user)
    tax = amount_calculator(request)['tax']
    grand_total = amount_calculator(request)['grand_total']
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = request.user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line1 = form.cleaned_data['address_line1']
            data.address_line2 = form.cleaned_data['address_line2']
            data.landmark = form.cleaned_data['landmark']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.zip = form.cleaned_data['zip']
            data.ip = request.META['REMOTE_ADDR']
            
            data.order_total = grand_total
            data.tax = tax
            data.save()
            data.order_number = generate_order_number(data.id)
            data.save()
            rzp_data = {
                'amount':float(data.order_total)*100,
                'currency':"INR",
                'receipt':'receipt #'+data.order_number
            }
            payment = client.order.create(data=rzp_data)
            rzp_order_id = payment['id']
            # print(payment)
            context = {
               'order' :data,
               'cartitems':cartitems,
               'rzp_order_id':rzp_order_id,
               'RZP_KEY_ID':RZP_KEY_ID,
               'rzp_amount':rzp_data['amount']
            }
            return render(request , 'orders/payment_page.html' , context)
        else:
            print(form.errors)
@login_required(login_url='login')    
def payment(request):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest" and request.method =="POST":
        order_number = request.POST['order_number']
        transaction_id = request.POST['transaction_id']
        payment_method = request.POST['payment_method']
        status = request.POST['status']
        razorpay_order_id = request.POST['razorpay_order_id']
        signature = request.POST['razorpay_signature']
        new_status = client.utility.verify_payment_signature({
            'razorpay_order_id':razorpay_order_id,
            'razorpay_payment_id':transaction_id,
            'razorpay_signature':signature
        })
        # Create payment 
        if new_status:
            order = Order.objects.get(user=request.user , order_number=order_number)
            payment =Payment.objects.create(user=request.user ,payment_id= transaction_id , payment_method=payment_method , amount_paid=order.order_total,status=status )
            payment.save()
            #update order table
            order.payment = payment
            order.is_ordered=True
            order.save()
            # Move cartitem to OrderProduct Model
            cartitem = CartItem.objects.filter(user=request.user)
            for item in cartitem:
                ordered_product = OrderProduct()
                ordered_product.order = order
                ordered_product.payment = payment
                ordered_product.user = request.user
                ordered_product.product_id = item.product_id
                ordered_product.size= item.size
                ordered_product.color = item.color
                ordered_product.quantity = item.quantity
                ordered_product.productPrice = item.product.price
                ordered_product.ordered = True
                ordered_product.save()
                # Reduce stock of Product , Size ,Color
                product = Product.objects.get(category = item.product.category , product_name=item.product.product_name)
                product.stock -= item.quantity
                product.save()
                try:
                    size = Size.objects.get(product=product , size=item.size)
                    size.stock -= item.quantity
                    size.save()
                except:
                    pass
                print(size)
                color_status1 = Color.objects.get(product=product , size__size=size , color=item.color)
                color_status2 = Color.objects.get(product=product ,  color=item.color)
                print(color_status1 , color_status2)
                try:
                    if color_status1 is not None:
                        print('here1')
                        color = Color.objects.get(product=product , size__size=size , color=item.color)
                        color.stock -= item.quantity
                        color.save()
                    elif color_status2 is not None:
                        print('here2')
                        color = Color.objects.get(product=product ,  color=item.color)
                        color.stock -= item.quantity
                        color.save()
                except:
                    pass
                

        # Send Order Confirmation Email
        mail_subject = "Tsiraa - Thanks For Ordering At Tsiraa"
        mail_template = "orders/emails/order_confirmation_email.html"
        context = {
            'user':request.user,
            'order':order,
            'to_email':order.email,
        }
        send_notification(mail_subject , mail_template , context)
        # Clear The Cart
        cartitem.delete()
        
        # Send Response  to Ajax request 
        response = {
                'status':'Success',
                'message':'Payment has been properly handled',
                'order_number':order_number,
                'transaction_id':transaction_id,

            }
        return JsonResponse(response)
    else:
        return JsonResponse({
            'status':"Failed",
            'message':"Paymet Failed ! If your money has been deducted ,A refund will be inititated within 7 working days"
        })
def order_complete(request):
    if request.method == "GET":
        order_number = request.GET['order_number']
        transaction_id = request.GET['transaction_id']
        # try:
        order = Order.objects.get(user=request.user , order_number= order_number)
        orderproduct = OrderProduct.objects.filter(order=order)
        # print(orderproduct)
        sub_total = order.order_total - order.tax
        context = {
            'order':order,
            'orderproduct':orderproduct,
            'transaction_id':transaction_id,
            'sub_total':sub_total,
        }
        return render(request , 'orders/order_complete.html' , context)
        # except:
            # return redirect('home')
    # return render(request , 'orders/order_complete.html')
        