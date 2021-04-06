from django import forms

from .models import ProductReview


class AddReviewForm(forms.ModelForm):
    """
    Add review form class.
    """
    title = forms.CharField(
        label='',
        max_length=45, 
        widget=forms.TextInput(attrs={'class':'form-control', 'name':'title', 'required':True}),
    )
    content = forms.CharField(
        label='',
        widget=forms.Textarea(attrs={'class':'form-control', 'name':'content', 'style':'resize:none;', 'required':True}),
    )
    class Meta:
        model   = ProductReview
        fields  = ['title', 'content']