from .models import CartItem , Tax , Cart


def cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def cart_counter(request):
    cart_count =0
    try:
        if request.user.is_authenticated:     
            items = CartItem.objects.filter(user = request.user)
            
            if items:
                for item in items:
                    cart_count += item.quantity
            else:
                cart_count =0
            print(cart_count)
        else:
            cart = Cart.objects.get(cart_id= cart_id(request))
            cartitems = CartItem.objects.filter(cart=cart)
            if cartitems:
                for item in cartitems:
                    cart_count += item.quantity
            else:
                cart_count=0
        return dict(cart_count=cart_count)
    except:
       return dict(cart_count=cart_count)
    


def amount_calculator(request):
    sub_total =0
    tax_total = 0
    tax_list =[]
    grand_total =0
    try:
        if request.user.is_authenticated:
            items = CartItem.objects.filter(user = request.user)
            
            taxes =Tax.objects.all()
           
            for item in items:
                sub_total += (item.quantity*item.product.price)
                
            for tax in taxes:
                for item in items:
                    if item.product.category== tax.category:
                        tax_type = tax.tax_name

                        tax_percent =tax.percent
                        tax_amount = round((tax_percent*item.product.price*item.quantity)/100 ,2)
                        tax_dict = {
                            'tax_type':tax_type,
                            'tax_percent':tax_percent,
                            'tax_amount':tax_amount,

                        }
                        tax_list.append(tax_dict)
                    else:
                        pass
            # print(tax_list)
            
            for tax_dict in tax_list:
                tax_total += tax_dict['tax_amount']
            sub_total -= tax_total
            grand_total = sub_total+tax_total
           
        else:
            cart = Cart.objects.get(cart_id=cart_id(request))
            items = CartItem.objects.filter(cart=cart)
            taxes =Tax.objects.all()
           
            for item in items:
                sub_total += (item.quantity*item.product.price)
                
            for tax in taxes:
                for item in items:
                    if item.product.category== tax.category:
                        tax_type = tax.tax_name

                        tax_percent =tax.percent
                        tax_amount = round((tax_percent*item.product.price*item.quantity)/100 ,2)
                        tax_dict = {
                            'tax_type':tax_type,
                            'tax_percent':tax_percent,
                            'tax_amount':tax_amount,

                        }
                        tax_list.append(tax_dict)
                    else:
                        pass
            # print(tax_list)
            
            for tax_dict in tax_list:
                tax_total += tax_dict['tax_amount']
            sub_total -= tax_total
            grand_total = round((sub_total+tax_total),2)
        return {
                'sub_total':round(sub_total,2),
                'tax':round(tax_total,2),
                'tax_list':tax_list,
                'grand_total':grand_total,
            }   
        
        
                
    except:
        return {
                'sub_total':round(sub_total,2),
                'tax':round(tax_total,2),
                'tax_list':tax_list,
                'grand_total':grand_total,
            }