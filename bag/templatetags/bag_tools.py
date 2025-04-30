from django import template

register = template.Library()

@register.filter(name='calc_subtotal')
# takes in a price and a quantity as parameters and simply returns their irproduct
def calc_subtotal(price, quantity):
    return price * quantity