from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category


# extend the built in forms.model form
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        # a special dunder or double underscore string to include
        # all the fields from model class Product
        fields = '__all__'

    # product image field on the form with the new custom code which utilizes the widget
    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        # the list comprehension - a shorthand way of creating a for loop that adds items to a list
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        # instead of category ID or the name field displays the friendly name
        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
