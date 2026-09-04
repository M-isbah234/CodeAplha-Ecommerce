from django import forms
from shop.models import Product, Category, ProductVariant, ProductImage

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'slug', 'image', 'description', 'price', 'stock', 'available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'parent']

from .models import StoreSettings

class StoreSettingsForm(forms.ModelForm):
    class Meta:
        model = StoreSettings
        fields = '__all__'
        widgets = {
            'default_currency': forms.TextInput(attrs={'class': 'form-control'}),
            'timezone': forms.TextInput(attrs={'class': 'form-control'}),
            'support_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'support_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'staff_roles_enabled': forms.CheckboxInput(attrs={'style': 'margin-top:0.5rem;'}),
            'email_webhooks_enabled': forms.CheckboxInput(attrs={'style': 'margin-top:0.5rem;'}),
            'auto_maintenance': forms.CheckboxInput(attrs={'style': 'margin-top:0.5rem;'}),
        }
