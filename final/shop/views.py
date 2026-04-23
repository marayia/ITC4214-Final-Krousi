from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from shop.models import Card, Set
from django.contrib.auth.models import User

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

def home(request):
    latest_cards = Card.objects.order_by('-id')[:8]
    sets = Set.objects.all()
    return render(request, 'shop/home.html', {
        'latest_cards': latest_cards,
        'sets': sets,
    })

# Admin views

# only staff can access admin panel views
staff_required = user_passes_test(lambda u: u.is_staff)

@login_required
@staff_required
def admin_dashboard(request):
    card_count = Card.objects.count()
    set_count = Set.objects.count()
    user_count = User.objects.count()
    return render(request, 'shop/admin/dashboard.html', {
        'card_count': card_count,
        'set_count': set_count,
        'user_count': user_count,
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
        card = Card(
            name=request.POST.get('name'),
            set_id=request.POST.get('set'),
            rarity=request.POST.get('rarity'),
            region=request.POST.get('region'),
            card_number=request.POST.get('card_number'),
            price=request.POST.get('price'),
            stock=request.POST.get('stock', 0),
        )
        if 'images' in request.FILES:
            card.images = request.FILES['images']
        card.save()
        return redirect('admin-cards')
    sets = Set.objects.all()
    return render(request, 'shop/admin/card_form.html', {
        'sets': sets,
        'rarities': Card.RARITY,
        'regions': Card.REGION,
        'action': 'Add',
    })

@login_required
@staff_required
def admin_card_edit(request, id):
    card = get_object_or_404(Card, id=id)
    if request.method == 'POST':
        card.name = request.POST.get('name')
        card.set_id = request.POST.get('set')
        card.rarity = request.POST.get('rarity')
        card.region = request.POST.get('region')
        card.card_number = request.POST.get('card_number')
        card.price = request.POST.get('price')
        card.stock = request.POST.get('stock', 0)
        if 'images' in request.FILES:
            card.images = request.FILES['images']
        card.save()
        return redirect('admin-cards')
    sets = Set.objects.all()
    return render(request, 'shop/admin/card_form.html', {
        'card': card,
        'sets': sets,
        'rarities': Card.RARITY,
        'regions': Card.REGION,
        'action': 'Edit',
    })

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
        s = Set(
            name=request.POST.get('name'),
            code=request.POST.get('code'),
            slug=request.POST.get('slug'),
        )
        s.save()
        return redirect('admin-sets')
    return render(request, 'shop/admin/set_form.html', {'action': 'Add'})

@login_required
@staff_required
def admin_set_edit(request, id):
    s = get_object_or_404(Set, id=id)
    if request.method == 'POST':
        s.name = request.POST.get('name')
        s.code = request.POST.get('code')
        s.slug = request.POST.get('slug')
        s.save()
        return redirect('admin-sets')
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