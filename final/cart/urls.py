from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart-index'),
    path('add/<int:id>/', views.add_to_cart, name='add-to-cart'),
    path('remove/<int:id>/', views.remove_from_cart, name='remove-from-cart'),
    path('checkout/', views.checkout, name='checkout'),
]