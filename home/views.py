from django.shortcuts import render

# Create your views here.

def index(request):
    """
    docstring / description of the function:
    A simple view to return the index page
    """
    return render(request, 'home/index.html')
