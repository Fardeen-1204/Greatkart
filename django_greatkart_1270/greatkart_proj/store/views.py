from django.shortcuts import render, get_object_or_404
from .models import Product
from Category.models import Category


# Create your views here.
def store_home(request):
    products = Product.objects.all().filter(is_available=True)
    products_count = products.count()
    context = {"products": products, 'products_count': products_count}
    return render(request, "store.html", context)


def store_with_cat(request, category_slug=None):
    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=categories, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()
    context = {"products": products, 'products_count': product_count}
    return render(request, "store.html", context)


def product_detail(request, category_slug, product_slug):
	try:
		if product_slug:
			product_slug = product_slug.lower()
			single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
	except Exception as e:
		raise e

	context = {'single_product': single_product}
	return render(request, "product_detail.html",context)

def search_products(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Product.objects.filter(product_name__icontains=query)
    return render(request, 'search_results.html', {
        'query': query,
        'results': results
    })
