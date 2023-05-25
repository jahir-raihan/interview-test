from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.middleware.csrf import get_token

from product.algorithms import filter_products
from product.models import Category, Product


# Products Page
def products(request):

    """Products page view , with filtering and searching capability"""

    # If request method is post filter out products by search query
    if request.method == 'POST':
        query_data = request.POST

        # Calling out filter function from products.algorithms to filter the products
        products_list = filter_products(query_data)

        # Generating new csrf token for another post request --> Supports simultaneous request
        new_token = get_token(request)

        context = {
            'template': render_to_string('products_filter_template.html', context={'products': products_list},
                                         request=request),
            'token': new_token
        }

        return JsonResponse(context)

    # If request is GET and there is a query string filter out by query string then return the products anyway.

    query = ''
    if 's' in request.GET:
        query = request.GET['s']

    category = Category.objects.filter(category_name__icontains=query)

    products_list = Product.objects.filter(
        Q(product_title__icontains=query) | Q(brand__icontains=query) | Q(product_tags__icontains=query) |
        Q(product_search_keyword__icontains=query) |
        Q(product_category__in=category)
    )

    # We want all products by query when query string is given
    if 's' not in request.GET:
        products_list = products_list.filter(product_in_stock=True)

    # Search keywords for search suggestions
    search_keywords = Product.objects.all()

    # For filtering purpose
    categories = Category.objects.all()

    context = {
        'products': products_list,
        'query': query,
        'query_string': True if query != '' else False,
        'search_keywords': search_keywords,
        'categories': categories,
    }
    return render(request, 'products.html', context)

