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
                if(response.status=='Success'){
                    swal(response.status , response.message , 'success')
                    $('#header_cart_counter').html(response.cart_counter['cart_count'])
                    $('#qty-'+item_id).html(response.qty)
                }
            }
        })
    })
})