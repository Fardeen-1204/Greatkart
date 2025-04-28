from django.urls import path, include
from .views import *

urlpatterns = [
    path("", store_home, name="store"),
    path("<slug:category_slug>", store_with_cat, name="products_by_category"),
    path("<slug:category_slug>/<slug:product_slug>/", product_detail, name="product_detail"),
    path('search/', search_products, name='search_products'),
]
