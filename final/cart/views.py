# views.py - cart views for cart detail, add/remove items, and checkout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from shop.models import Card
from .models import CartItem, Purchase

@login_required
def cart_detail(request):
    items = CartItem.objects.filter(user=request.user)
    # calculate subtotal per item for display in template
    for item in items:
        item.subtotal = item.card.price * item.quantity
    total = sum(item.subtotal for item in items)
    return render(request, 'cart/cart_page.html', {'items': items, 'total': total})

@login_required
def add_to_cart(request, id):
    card = get_object_or_404(Card, id=id)
    item, created = CartItem.objects.get_or_create(user=request.user, card=card)
    if not created:
        # don't exceed available stock
        if item.quantity < card.stock:
            item.quantity += 1
            item.save()
    return redirect('cart-index')

@login_required
def remove_from_cart(request, id):
    item = get_object_or_404(CartItem, id=id, user=request.user)
    item.delete()
    return redirect('cart-index')

@login_required
def checkout(request):
    items = CartItem.objects.filter(user=request.user)
    # calculate subtotal per item for display
    for item in items:
        item.subtotal = item.card.price * item.quantity
    total = sum(item.subtotal for item in items)

    if request.method == 'POST':
        for item in items:
            # save purchase record before clearing cart
            Purchase.objects.create(
                user=request.user,
                card=item.card,
                quantity=item.quantity,
                price_at_purchase=item.card.price,
            )
            # reduce stock
            card = item.card
            card.stock = max(0, card.stock - item.quantity)
            card.save()
        # clear the cart after purchase
        CartItem.objects.filter(user=request.user).delete()
        return render(request, 'cart/checkout_confirmed.html', {})

    return render(request, 'cart/checkout.html', {'items': items, 'total': total})