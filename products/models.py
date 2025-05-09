from django.db import models


# positioning class two lines below import
class Category(models.Model):

    # to fix the Python spelling issue on the Admin 'Categorys' by adding a special metaclass to the model itself
    # this won't require migration since we're not making any changes to the structure of the model
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    # model method
    def __str__(self):
        return self.name

    # model method
    def get_friendly_name(self):
        return self.friendly_name


# each product requires a name, a description, and a price, everything else is optional
class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    has_sizes = models.BooleanField(default=False, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    # model method, string representation
    def __str__(self):
        return self.name
