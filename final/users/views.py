# views.py - authentication, profile and dashboard views for the users app
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from django import forms
from shop.models import WishlistItem
from cart.models import Purchase

# custom registration form — extends Django's base Form to require email and validate passwords
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Confirm Password')

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data

def login_view(request):
    # use Django's built-in AuthenticationForm which handles password checking
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    # apply Bootstrap class to inputs
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def register_view(request):
    # custom form so we can require email at registration
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile_view(request):
    # deterministic pokemon based on username — same user always gets same pokemon
    # uses sum of ascii values mod 151 to pick from gen 1 pokemon (gen 5 sprites)
    pokemon_id = (sum(ord(c) for c in request.user.username) % 151) + 1
    return render(request, 'users/profile.html', {'pokemon_id': pokemon_id})

@login_required
def dashboard_view(request):
    # fetch wishlist items and recent purchases for the dashboard
    wishlist_items = WishlistItem.objects.filter(user=request.user).order_by('-added_at')
    purchases = Purchase.objects.filter(user=request.user).order_by('-purchased_at')[:10]
    return render(request, 'users/dashboard.html', {
        'wishlist_items': wishlist_items,
        'purchases': purchases,
    })

@login_required
def edit_profile_view(request):
    # get_or_create ensures a profile exists even if it wasn't made at registration
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        request.user.email = request.POST.get('email', '')
        request.user.save()
        profile.bio = request.POST.get('bio', '')
        profile.header_color = request.POST.get('header_color', '#344657')
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        return redirect('profile')
    return render(request, 'users/edit_profile.html', {'profile': profile})