from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)

    # to override the init method of the form which will allow us to customize it quite a bit
    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        # call the default init method to set the form up as it would be by default
        super().__init__(*args, **kwargs)
        # created a dictionary of placeholders, fields in form
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }

        # setting the autofocus attribute on the first field
        self.fields['full_name'].widget.attrs['autofocus'] = True
        # iterate through the forms fields
        for field in self.fields:
            # adding a star to the placeholder if it's a required field
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            # setting all the placeholder attributes to their values in the dictionary above
            self.fields[field].widget.attrs['placeholder'] = placeholder
            # adding a CSS class
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            # removing the form fields labels given the placeholders are now set
            self.fields[field].label = False
