from django import forms
from .models import Product, Bundle, SalesChannel


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'product_quantity']

    def clean_product_name(self):
        product_name = self.cleaned_data.get('product_name').lower()
        if self.instance.pk is None:
            if Product.objects.filter(product_name=product_name).exists():
                raise forms.ValidationError('This product already exists.')
        else:
            if Product.objects.filter(product_name=product_name).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('This product already exists.')
        return product_name


class BundleForm(forms.Form):
    products = forms.ModelMultipleChoiceField(queryset=Product.objects.all(), widget=forms.CheckboxSelectMultiple)

    def clean(self):
        cleaned_data = super().clean()
        selected_products = cleaned_data.get('products')
        bundle_name = ' & '.join([product.product_name for product in selected_products])
        if Bundle.objects.filter(name__iexact=bundle_name).exists():
            raise forms.ValidationError("A bundle with this name already exists.")
        cleaned_data['name'] = bundle_name
        return cleaned_data


class BundleUpdateForm(forms.ModelForm):
    class Meta:
        model = Bundle
        fields = ['stock']

    def clean_stock(self):
        new_stock = self.cleaned_data['stock']
        if new_stock >= self.instance.stock:
            raise forms.ValidationError("New stock must be less than current stock!")
        return new_stock


class SalesChannelForm(forms.ModelForm):
    class Meta:
        model = SalesChannel
        fields = ['sales_channel_name']

    def clean(self):
        cleaned_data = super().clean()
        sales_channel_name = cleaned_data.get('sales_channel_name')
        if sales_channel_name and SalesChannel.objects.filter(sales_channel_name__iexact=sales_channel_name).exists():
            raise forms.ValidationError("A sales channel with this name already exists (case-insensitive).")
        return cleaned_data
