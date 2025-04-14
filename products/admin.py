from django.contrib import admin
from .models import Product, Category

# Register your models here.

# both classes will extend the built in model admin class
# with order of fields to display in Admin preview
# to change the order of the columns in the Admin, just adjust the order here in the list display attribute
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
    )

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Product)
admin.site.register(Category)
