from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
# If the query isn't blank, a special object from Jango.db.models 
# called Q will generate a search query
from django.db.models import Q
from .models import Product

# Create your views here.

def all_products(request):
    """
    docstring / description of the function:
    A view to display all products, including sorting and search queries
    """

    # return all products from the database using 'Product.objects.all'
    products = Product.objects.all()
    query = None

    # request for the search form
    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

# In the case of queries when a user submits a query in order for it to match 
# the term would have to appear in both the product name and the product description
# we want to return results where the query was matched in either the product 
# name or the description, to accomplish this 'OR' logic, we need to use 'Q'
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    # for products to be available in the template
    # to send some things back to the template
    context = {
        'products': products,
        'search_term': query,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """
    docstring / description of the function:
    A view to display details about one product
    """

    # return product from the database
    product = get_object_or_404(Product, pk=product_id)

    # for products to be available in the template
    # to send some things back to the template
    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
