from django.contrib import admin
from .models import Product, SalesChannel, Bundle


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_quantity')
    search_fields = ('product_name',)


@admin.register(SalesChannel)
class SalesChannelAdmin(admin.ModelAdmin):
    search_fields = ('sales_channel_name',)


@admin.register(Bundle)
class BundleAdmin(admin.ModelAdmin):
    search_fields = ('bundle_name',)
