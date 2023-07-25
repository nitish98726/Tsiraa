from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import ReviewRating
from .forms import ReviewForm
from django.contrib import messages
# Create your views here.

@login_required(login_url = 'login')
def add_review(request , product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method =="POST":
        try:
           review = ReviewRating.objects.get(user__id  = request.user.id , product__id= product_id)
           form = ReviewForm(request.POST ,instance=review )
           form.save()
           messages.success(request , "Thank You! your Review has been updated")
           return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST , request.FILES)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.image1 = form.cleaned_data['image1']
                data.image2 = form.cleaned_data['image2']
                data.image3 = form.cleaned_data['image3']
                data.image4 = form.cleaned_data['image4']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request , "Thank You! your Review has been submitted")
                return redirect(url)
    # return HttpResponse('You reveiew is added successfully')