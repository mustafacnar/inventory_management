from django.urls import path
from .views import add_product, product_list, update_product, delete_product, create_bundle, bundle_list, bundle_detail, \
    create_sales_channel, sales_channel_list, home, sales_channel_details, bundle_update, delete_bundle, sales_page, \
    delete_sales_channel

urlpatterns = [
    path('create_product/', add_product, name='add_product'),
    path('product_list/', product_list, name='product_list'),
    path('update/<int:pk>/', update_product, name='update_product'),
    path('delete_product/<int:pk>/', delete_product, name='delete_product'),
    path('create_bundle/', create_bundle, name='create_bundle'),
    path('bundle_list/', bundle_list, name='bundle_list'),
    path('bundle/<int:pk>/', bundle_detail, name='bundle_detail'),
    path('create_sales_channel/', create_sales_channel, name='create_sales_channel'),
    path('sales_channel_list/', sales_channel_list, name='sales_channel_list'),
    path('sales_channel/<int:pk>/', sales_channel_details, name='sales_channel_details'),
    path('bundle_update/<int:bundle_id>/', bundle_update, name='bundle_update'),
    path('delete_sales_channel/<int:sales_channel_id>/', delete_sales_channel, name='delete_sales_channel'),
    path('delete_bundle/<int:pk>/', delete_bundle, name='delete_bundle'),
    path('', home, name='home'),
    path('sales_page', sales_page, name='sales_page')
]
