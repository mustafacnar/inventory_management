from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm, BundleForm, SalesChannelForm, BundleUpdateForm
from .models import Product, Bundle, SalesChannel


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
            form.save()
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
            form.save()
            return redirect('bundle_list')
    else:
        form = BundleUpdateForm(instance=bundle)
    return render(request, 'products/bundle_update.html', {'form': form, 'bundle': bundle})


def bundle_detail(request, pk):
    bundle = get_object_or_404(Bundle, pk=pk)
    return render(request, 'products/bundle_detail.html', {'bundle': bundle})


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


def delete_sales_channel(request, pk):
    sales_channel = get_object_or_404(SalesChannel, pk=pk)
    if request.method == 'POST':
        sales_channel.delete()
        return redirect('bundle_list')
    return render(request, 'products/delete_sales_channel.html', {'sales_channel': sales_channel})


def home(request):
    return render(request, 'products/home.html')


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


def sales_page(request):
    products = Product.objects.all()
    bundles = Bundle.objects.all()

    if request.method == 'POST':
        if 'sale_product_id' in request.POST:
            product_id = request.POST['sale_product_id']
            product = Product.objects.get(pk=product_id)

            if product.product_quantity <= 0:
                return redirect('sales_page')
            else:
                product.product_quantity -= 1
                product.save()
                product_name = product.product_name
                relevant_bundles = Bundle.objects.filter(products__product_name__icontains=product_name)
                for bundle in relevant_bundles:
                    if product.product_quantity < bundle.stock:
                        bundle.stock -= 1
                        bundle.save()
            return redirect('sales_page')
        if 'sale_bundle_id' in request.POST:
            bundle_id = request.POST['sale_bundle_id']
            bundle = Bundle.objects.get(pk=bundle_id)
            if bundle.stock <= 0:
                return redirect('sales_page')
            else:
                bundle.stock -= 1
                bundle.save()
                for product in bundle.products.all():
                    product.product_quantity -= 1
                    product.save()
                bundle_products = bundle.products.all()
                relevant_bundles = Bundle.objects.filter(products__in=bundle_products).exclude(pk=bundle_id)
                for other_bundle in relevant_bundles:
                    other_bundle_products = other_bundle.products.all()
                    min_product_quantity = min([product.product_quantity for product in other_bundle_products])
                    if other_bundle.stock > min_product_quantity:
                        other_bundle.stock -= 1
                        other_bundle.save()
            return redirect('sales_page')
    return render(request, 'products/sales_page.html', {'products': products, 'bundles': bundles})
