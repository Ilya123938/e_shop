from .cart import CartConfig


def cart(request):
    return {'cart': CartConfig(request)}