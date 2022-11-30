from django import forms
from .models import BookReview


class BookReviewsForm(forms.ModelForm):
    stars_given = forms.FloatField(min_value=1, max_value=5)

    class Meta:
        model = BookReview
        fields = ('stars_given', 'comment')
