import re

from django import forms

from .models import Order


class AddOrderForm(forms.ModelForm):
    """
    Order creation form class.
    """
    full_name = forms.CharField(
        label='',
        max_length=50, 
        widget=forms.TextInput(attrs={'class':'form-control', 'name':'full_name', 'required':True}),
    )
    address1 = forms.CharField(
        label='',
        max_length=200, 
        widget=forms.TextInput(attrs={'class':'form-control', 'name':'address1', 'required':True}),
    )
    address2 = forms.CharField(
        label='',
        max_length=200, 
        widget=forms.TextInput(attrs={'class':'form-control', 'name':'address2'}),
    )
    city = forms.CharField(
        label='',
        max_length=40, 
        widget=forms.TextInput(attrs={'class':'form-control', 'name':'city', 'required':True}),
    )
    post_code = forms.CharField(
        label='',
        max_length=15, 
        widget=forms.TextInput(attrs={'class':'form-control', 'name':'post_code', 'required':True}),
    )
    phone = forms.CharField(
        label='', 
        max_length=17,
        widget=forms.TextInput(attrs={
            'class':'form-control', 
            'name':'phone', 
            'placeholder':"It must be entered in the format: '+999999999'. Up to 15 digits allowed.",
            'required': True,
        })
    )

    class Meta:
        model   = Order
        fields  = ['full_name', 'address1', 'address2', 'city', 'post_code', 'phone']    

    def clean_phone(self):
        """
        Validate phone.
        """
        phone = self.cleaned_data.get("phone").strip()
        is_phone = re.compile(r'^\+?1?\d{9,15}$').search(phone)
        if not is_phone:
            raise forms.ValidationError('Enter a valid phone number.')
        return phone