from django import template
from travels.models import Order

register = template.Library()

@register.filter
def cart_travel_count(user):
    if user.is_authenticated:
        order_qs = Order.objects.filter(user=user, ordered=False)
        if order_qs.exists():
            return order_qs[0].travels.count()
        else:
            return 0