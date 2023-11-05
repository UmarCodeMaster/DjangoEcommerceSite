# forms.py
from django import forms
from .models import Shipping

class ShippingForm(forms.ModelForm):
    class Meta:
        model = Shipping
        fields = [
            'first_name',
            'last_name',
            'comp_name',
            'area_code',
            'phone',
            'address',
            'zip_code',
            'busines_address',
        ]


