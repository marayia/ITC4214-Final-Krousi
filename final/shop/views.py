from django.shortcuts import render
from shop.models import Card, Set

def home(request):
    return render(request, 'shop/home.html', {})

def index(request):
    cards = Card.objects.all()
    sets = Set.objects.all()

    # read filter values from the URL, default to empty if not set
    selected_set = request.GET.get('set', '')
    selected_rarity = request.GET.get('rarity', '')
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    search_query = request.GET.get('q', '')

    # apply filters
    if selected_set:
        cards = cards.filter(set__slug=selected_set)
    if selected_rarity:
        cards = cards.filter(rarity=selected_rarity)
    if price_min:
        cards = cards.filter(price__gte=price_min)
    if price_max:
        cards = cards.filter(price__lte=price_max)
    if search_query:
        cards = cards.filter(name__icontains=search_query)

    # price bounds for the price range input
    all_cards = Card.objects.all()
    bounds = {
        'min': all_cards.order_by('price').first().price if all_cards.exists() else 0,
        'max': all_cards.order_by('-price').first().price if all_cards.exists() else 1000,
    }

    return render(request, 'shop/shop.html', {
        'cards': cards,
        'sets': sets,
        'rarities': Card.RARITY,
        'selected_set': selected_set,
        'selected_rarity': selected_rarity,
        'price_min': price_min,
        'price_max': price_max,
        'bounds': bounds,
    })

def card_detail(request, id):
    # fetch the card with the given id
    card = Card.objects.get(id=id)
    return render(request, 'shop/card_detail.html', {'card': card})

def about(request):
    return render(request, 'shop/about.html', {})