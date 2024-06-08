from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm, BundleForm, SalesChannelForm, BundleUpdateForm
from .models import Product, Bundle, SalesChannel
from django.db.models.signals import post_save, pre_delete


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/create_product.html', {'form': form})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})


def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            updated_product = form.save(commit=False)
            if updated_product.product_quantity == 0:
                product.delete()
                return redirect('product_list')
            else:
                updated_product.save()
                return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/update_product.html', {'form': form, 'product': product})


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'products/delete_product.html', {'product': product})


def create_bundle(request):
    if request.method == 'POST':
        form = BundleForm(request.POST)
        if form.is_valid():
            selected_products = form.cleaned_data['products']
            if len(selected_products) < 2:
                return render(request, 'products/create_bundle.html',
                              {'form': form, 'error_message': 'Select at least 2 products'})
            else:
                bundle_name = ' & '.join([str(product) for product in selected_products])
                bundle = Bundle.objects.create(name=bundle_name,
                                               stock=min([product.product_quantity for product in selected_products]))
                bundle.products.set(selected_products)
                bundle.save()
                return redirect('bundle_list')
    else:
        form = BundleForm()
    return render(request, 'products/create_bundle.html', {'form': form})


def bundle_list(request):
    bundles = Bundle.objects.all()
    return render(request, 'products/bundle_list.html', {'bundles': bundles})


def bundle_update(request, bundle_id):
    bundle = get_object_or_404(Bundle, pk=bundle_id)
    if request.method == 'POST':
        form = BundleUpdateForm(request.POST, instance=bundle)
        if form.is_valid():
            new_stock = form.cleaned_data['stock']
            bundle.stock = new_stock
            bundle.save()
            products = bundle.products.all()
            stock_list = list()
            for product in products:
                stock_list.append(product.product_quantity)
            difference = (min(stock_list) - new_stock)
            for product in products:
                product.product_quantity = product.product_quantity - difference
                product.save()

            return redirect('bundle_list')
    else:
        form = BundleUpdateForm(instance=bundle)
    return render(request, 'products/bundle_update.html', {'form': form, 'bundle': bundle})


def bundle_detail(request, pk):
    bundle = get_object_or_404(Bundle, pk=pk)
    return render(request, 'products/bundle_detail.html', {'bundle': bundle})


@receiver(post_save, sender=Product)
def update_bundles_stock(sender, instance, **kwargs):
    for bundle in instance.bundle_set.all():
        bundle.stock = min([product.product_quantity for product in bundle.products.all()])
        bundle.save()


@receiver(pre_delete, sender=Product)
def delete_related_bundles(sender, instance, **kwargs):
    instance.bundle_set.all().delete()


def create_sales_channel(request):
    if request.method == 'POST':
        form = SalesChannelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sales_channel_list')
    else:
        form = SalesChannelForm()
    return render(request, 'products/create_sales_channel.html', {'form': form})


def sales_channel_list(request):
    sales_channels = SalesChannel.objects.all()
    return render(request, 'products/sales_channel_list.html', {'sales_channels': sales_channels})


def home(request):
    return render(request, 'products/home.html', )


def sales_channel_details(request, pk):
    sales_channel = get_object_or_404(SalesChannel, pk=pk)
    products = Product.objects.all()
    bundles = Bundle.objects.all()
    return render(request, 'products/sales_channel_details.html',
                  {'sales_channel': sales_channel, 'products': products, 'bundles': bundles})


def delete_bundle(request, pk):
    bundle = get_object_or_404(Bundle, pk=pk)
    if request.method == 'POST':
        bundle.delete()
        return redirect('bundle_list')
    return render(request, 'products/delete_bundle.html', {'bundle': bundle})
