from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.

def all_products(request):
    """
    docstring / description of the function:
    A view to display all products, including sorting and search queries
    """

    # return all products from the database using 'Product.objects.all'
    products = Product.objects.all()

    # for products to be available in the template
    # to send some things back to the template
    context = {
        'products': products,
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
