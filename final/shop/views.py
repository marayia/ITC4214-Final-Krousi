from django.shortcuts import render
from shop.models import Card

def home(request):
    return render(request, 'shop/home.html', {})

def index(request):
    cards = Card.objects.all()
    return render(request, 'shop/index.html', {'cards': cards})

def card_detail(request, id):
    card = Card.objects.get(id=id)
    return render(request, 'shop/card_detail.html', {'card': card})