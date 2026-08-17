def cart_count(request):
    try:
        cart = getattr(request, 'session', {}).get('cart', {})
        count = sum(cart.values()) if isinstance(cart, dict) else 0
    except Exception:
        count = 0

    return {
        'cart_count': count
    }