from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.index, name='shop-index'),
    path('shop/card/<int:id>/', views.card_detail, name='card-detail'),
]