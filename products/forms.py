from django import forms
from django.core.exceptions import ValidationError

from .models import Product, Bundle, SalesChannel


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'product_quantity']

    def clean_product_name(self):
        product_name = self.cleaned_data.get('product_name').title()
        if self.instance.pk is None:
            if Product.objects.filter(product_name=product_name).exists():
                raise forms.ValidationError('This product already exists.')
        else:
            if Product.objects.filter(product_name=product_name).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('This product already exists.')
        return product_name


class BundleForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(queryset=Product.objects.all(), widget=forms.CheckboxSelectMultiple)
    sales_channel = forms.ModelChoiceField(queryset=SalesChannel.objects.all(), required=False)

    class Meta:
        model = Bundle
        fields = ['products', 'stock', 'sales_channel']

    def clean(self):
        cleaned_data = super().clean()
        selected_products = cleaned_data.get('products')
        sales_channel = cleaned_data.get('sales_channel')
        bundle_name = ' & '.join([product.product_name for product in selected_products])
        if sales_channel:
            if Bundle.objects.filter(name__iexact=bundle_name, sales_channel=sales_channel).exists():
                raise ValidationError("A bundle with this name and sales channel already exists.")
        else:
            raise ValidationError("Please select a Sales Channel.")

        cleaned_data['name'] = bundle_name
        min_stock = min(product.product_quantity for product in selected_products)
        max_stock = cleaned_data.get('stock')

        if max_stock > min_stock:
            raise ValidationError(f"Stock cannot be greater than the minimum product quantity ({min_stock}).")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.name = self.cleaned_data['name']
        if commit:
            instance.save()
            self.save_m2m()
        return instance


class BundleUpdateForm(forms.ModelForm):
    class Meta:
        model = Bundle
        fields = ['stock']

    def clean_stock(self):
        new_stock = self.cleaned_data['stock']
        products = self.instance.products.all()
        min_product_quantity = min(product.product_quantity for product in products)

        if new_stock > min_product_quantity:
            raise forms.ValidationError(
                f"New stock must be less than or equal to the minimum product quantity ({min_product_quantity})!")

        return new_stock


class SalesChannelForm(forms.ModelForm):
    class Meta:
        model = SalesChannel
        fields = ['sales_channel_name']

    def clean(self):
        cleaned_data = super().clean()
        sales_channel_name = cleaned_data.get('sales_channel_name').title()
        if sales_channel_name and SalesChannel.objects.filter(sales_channel_name__iexact=sales_channel_name).exists():
            raise forms.ValidationError("A sales channel with this name already exists.")
        return cleaned_data
