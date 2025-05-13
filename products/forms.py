from django import forms
from .models import Product, Category


# extend the built in forms.model form
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        # a special dunder or double underscore string to include all the fields
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        # the list comprehension - a shorthand way of creating a for loop that adds items to a list
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        # instead of category ID or the name field displays the friendly name
        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
