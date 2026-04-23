from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from shop.models import Card, Set

# Public views

def home(request):
    latest_cards = Card.objects.order_by('-id')[:5]
    sets = Set.objects.all()
    return render(request, 'shop/home.html', {
        'latest_cards': latest_cards,
        'sets': sets,
    })

def index(request):
    cards = Card.objects.all()
    sets = Set.objects.all()

    # read filter values from the URL, default to empty if not set
    selected_set = request.GET.get('set', '')
    selected_rarity = request.GET.get('rarity', '')
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    search_query = request.GET.get('q', '')

    # narrow down cards based on whatever filters are active
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

    # get cheapest and most expensive card to set the price slider range
    # fallback to 0-1000 if there are no cards yet
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
    # fetch the card by id, return 404 if it doesn't exist
    card = get_object_or_404(Card, id=id)
    return render(request, 'shop/card_detail.html', {'card': card})

def about(request):
    return render(request, 'shop/about.html', {})


# Admin views 

# only staff users can access admin panel views
staff_required = user_passes_test(lambda u: u.is_staff)

# helper to avoid repeating the card form context in add and edit views
def _card_form_context(action, card=None, error=None):
    return {
        'sets': Set.objects.all(),
        'rarities': Card.RARITY,
        'regions': Card.REGION,
        'action': action,
        'card': card,
        'error': error,
    }

@login_required
@staff_required
def admin_dashboard(request):
    return render(request, 'shop/admin/dashboard.html', {
        'card_count': Card.objects.count(),
        'set_count': Set.objects.count(),
        'user_count': User.objects.count(),
    })

@login_required
@staff_required
def admin_cards(request):
    cards = Card.objects.all().order_by('-id')
    return render(request, 'shop/admin/cards.html', {'cards': cards})

@login_required
@staff_required
def admin_card_add(request):
    if request.method == 'POST':
        try:
            card = Card(
                name=request.POST.get('name'),
                set_id=request.POST.get('set'),
                rarity=request.POST.get('rarity'),
                region=request.POST.get('region'),
                card_number=request.POST.get('card_number'),
                price=request.POST.get('price'),
                stock=request.POST.get('stock', 1),
            )
            if 'images' in request.FILES:
                card.images = request.FILES['images']
            card.save()
            return redirect('admin-cards')
        except Exception:
            return render(request, 'shop/admin/card_form.html', _card_form_context('Add', error='Invalid input — please check all fields.'))
    return render(request, 'shop/admin/card_form.html', _card_form_context('Add'))

@login_required
@staff_required
def admin_card_edit(request, id):
    card = get_object_or_404(Card, id=id)
    if request.method == 'POST':
        try:
            card.name = request.POST.get('name')
            card.set_id = request.POST.get('set')
            card.rarity = request.POST.get('rarity')
            card.region = request.POST.get('region')
            card.card_number = request.POST.get('card_number')
            card.price = request.POST.get('price')
            card.stock = request.POST.get('stock', 1)
            if 'images' in request.FILES:
                card.images = request.FILES['images']
            card.save()
            return redirect('admin-cards')
        except Exception:
            return render(request, 'shop/admin/card_form.html', _card_form_context('Edit', card=card, error='Invalid input — please check all fields.'))
    return render(request, 'shop/admin/card_form.html', _card_form_context('Edit', card=card))

@login_required
@staff_required
def admin_card_delete(request, id):
    card = get_object_or_404(Card, id=id)
    if request.method == 'POST':
        card.delete()
        return redirect('admin-cards')
    return render(request, 'shop/admin/card_confirm_delete.html', {'card': card})

@login_required
@staff_required
def admin_sets(request):
    sets = Set.objects.all()
    return render(request, 'shop/admin/sets.html', {'sets': sets})

@login_required
@staff_required
def admin_set_add(request):
    if request.method == 'POST':
        try:
            s = Set(
                name=request.POST.get('name'),
                code=request.POST.get('code'),
                slug=request.POST.get('slug'),
            )
            s.save()
            return redirect('admin-sets')
        except Exception:
            return render(request, 'shop/admin/set_form.html', {
                'action': 'Add',
                'error': 'Invalid input — please check all fields.',
            })
    return render(request, 'shop/admin/set_form.html', {'action': 'Add'})

@login_required
@staff_required
def admin_set_edit(request, id):
    s = get_object_or_404(Set, id=id)
    if request.method == 'POST':
        try:
            s.name = request.POST.get('name')
            s.code = request.POST.get('code')
            s.slug = request.POST.get('slug')
            s.save()
            return redirect('admin-sets')
        except Exception:
            return render(request, 'shop/admin/set_form.html', {
                'set': s,
                'action': 'Edit',
                'error': 'Invalid input — please check all fields.',
            })
    return render(request, 'shop/admin/set_form.html', {'set': s, 'action': 'Edit'})

@login_required
@staff_required
def admin_set_delete(request, id):
    s = get_object_or_404(Set, id=id)
    if request.method == 'POST':
        s.delete()
        return redirect('admin-sets')
    return render(request, 'shop/admin/set_confirm_delete.html', {'set': s})

@login_required
@staff_required
def admin_users(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'shop/admin/users.html', {'users': users})