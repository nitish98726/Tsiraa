$(document).ready(function(){
    $('#p_image_side').on('click' , function(e){
        e.preventDefault()
        $('#product_detail_image').attr({'src' : $(this).attr('href')})

    })
    
    
    
})

// Add to cart functionality
$(document).ready(function(){
    $('.add_cart').on('click' , function(e){
        
        e.preventDefault()
        url = $(this).attr('data-url')
        item_id = $(this).attr('data-id')
        console.log(url)
        $.ajax({
            type:"GET",
            url:url,
            success:function(response){
                console.log(response)
                if(response.status=='Success'){
                    
                    
                    $('#header_cart_counter').html(response.cart_counter['cart_count'])
                    $('#qty-'+item_id).html(response.qty)
                    $('#item_wise_total'+item_id).html(response.item_wise_total)
                    applyCartAmounts(response.cart_amount['sub_total'] ,response.cart_amount['tax'] , response.cart_amount['grand_total'] )
                }
            }
        })
    })
    // Decrease Cart Item Quantity
    $('.decrease_cart').on('click' , function(e){
        e.preventDefault()
        url = $(this).attr('data-url')
        item_id = $(this).attr('data-id')

        console.log(url ,item_id)
        $.ajax({
            type:"GET",
            url:url,
            success:function(response){
                console.log(response)
                if(response.status=='Success'){
                    
                    swal(response.status , response.message , 'success')
                    $('#header_cart_counter').html(response.cart_counter['cart_count'])
                    $('#qty-'+item_id).html(response.qty)
                    $('#item_wise_total'+item_id).html(response.item_wise_total)
                    applyCartAmounts(response.cart_amount['sub_total'] ,response.cart_amount['tax'] , response.cart_amount['grand_total'] )
                    removeCartItem(response.qty , item_id)
                    checkEmptyCart()
                    removeCheckoutButton(response.cart_counter['cart_count'])
                }
            }
        })
    })

    // Remove Cart Item
    $('.cart-remove').on('click' , function(e){
        e.preventDefault()
        url = $(this).attr('data-url')
        item_id = $(this).attr('data-id')
        swal("Are you Sure you want to delete the cart Item?" , {buttons:["Cancel" , 'Proceed'],})
        .then((value)=>{
            if (value){
                $.ajax({
                    type:'GET',
                    url:url,
                    success:function(response){
                        if(response.status=="Success"){
                            $('#header_cart_counter').html(response.cart_counter['cart_count'])   
                            applyCartAmounts(response.cart_amount['sub_total'] ,response.cart_amount['tax'] , response.cart_amount['grand_total'] )
                            removeCartItem(response.qty ,item_id)
                            checkEmptyCart()
                            removeCheckoutButton(response.cart_counter['cart_count'])
                        }
                    }
                })
            }
        })
        
    })
    function applyCartAmounts(sub_total , tax , grand_total){
        $('#subtotal').html('INR '+sub_total);
        $('#tax_amount').html('INR '+tax);
        $('#grand_total').html('INR '+grand_total);
    }
    function removeCartItem(quantity , cart_item_id){
        if(quantity<=0){
            document.getElementById("cart-item-"+cart_item_id).remove()
            
        }
    

    }
    function removeCheckoutButton(quantity){
        if(quantity<1){
            document.getElementById('checkout-button').remove()
        }
    }
    function checkEmptyCart(){
        var cart_count = document.getElementById('header_cart_counter').innerHTML
        if(cart_count==0){
            document.getElementById('empty-cart').classList.remove('d-none')
        }
    }

    // check pin code servicable or not
    $('#pin-code').on('keyup' , function(){
        pin_code = $(this).val()
        if(pin_code.length==6){
            url = $(this).attr('data-url')
            data = {
                'pin_code':pin_code,
            }
            $.ajax({
                type:"GET",
                url:url,
                data:data,
                success:function(response){
                    if(response.status=="Success"){
                        if(response.data.delivery_codes[0]==undefined){
                            swal('' , 'Pin Code is Either Incorrect or not Servicable' , 'error')
                        }else{
                            console.log(response.data.delivery_codes[0])
                            var city = response.data.delivery_codes[0].postal_code.city
                            var check = response.data.delivery_codes[0].postal_code.cash
                            if(check=='Y'){
                                message = 'Pin code of your city '+city+' is covered'
                                swal('' , message , 'success')
                            }else if(response.data.delivery_codes[0].postal_code.cod=='Y'){
                                message = 'Pin code of your city '+city+' is covered'
                                swal('' , message , 'success')

                            }
                        }
                        
                    }else{
                        swal('' , 'Pin Code is Either Incorrect or not Servicable' , 'error')
                    }
                    
                }
                
            })
        }
    })
        
    
})