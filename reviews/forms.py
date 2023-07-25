from django import forms
from .models import ReviewRating
class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject' , 'review' , 'rating' , 'image1','image2' , 'image3' , 'image4']