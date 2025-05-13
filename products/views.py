from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
# If the query isn't blank, a special object from Jango.db.models 
# called Q will generate a search query
from django.db.models import Q
# used to annotate the product list with the lowercase name when sorting
from django.db.models.functions import Lower
from .models import Product, Category
from .forms import ProductForm

# Create your views here.

def all_products(request):
    """
    docstring / description of the function:
    A view to display all products, including sorting and search queries
    """

    # return all products from the database using 'Product.objects.all'
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    # request for the search form
    if request.GET:

        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if sortkey == 'category':
                sortkey = 'category__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

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

    current_sorting = f'{sort}_{direction}'

    # for products to be available in the template to send some things back to the template
    # A Context is a dictionary with variable names as the key and their values as the value. 
    # If context for the 'home/index.html' template looks like: {myvar1: 101, myvar2: 102}, 
    # when it's passed this context to the template render method, {{ myvar1 }} would be replaced with 101 
    # and {{ myvar2 }} with 102 in template. 
    # A Context object is the context in which the template is being rendered.
    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
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


# render an empty instance of form so can be seen how it looks
def add_product(request):
    """ Add a product to the store """
    form = ProductForm()
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
