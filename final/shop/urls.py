from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.index, name='shop-index'),
    path('shop/card/<int:id>/', views.card_detail, name='card-detail'),
    path('about/', views.about, name='about'),
    
    # admin URLs
    path('admin-panel/', views.admin_dashboard, name='admin-dashboard'),
    path('admin-panel/cards/', views.admin_cards, name='admin-cards'),
    path('admin-panel/cards/add/', views.admin_card_add, name='admin-card-add'),
    path('admin-panel/cards/<int:id>/edit/', views.admin_card_edit, name='admin-card-edit'),
    path('admin-panel/cards/<int:id>/delete/', views.admin_card_delete, name='admin-card-delete'),
    path('admin-panel/sets/', views.admin_sets, name='admin-sets'),
    path('admin-panel/sets/add/', views.admin_set_add, name='admin-set-add'),
    path('admin-panel/sets/<int:id>/edit/', views.admin_set_edit, name='admin-set-edit'),
    path('admin-panel/sets/<int:id>/delete/', views.admin_set_delete, name='admin-set-delete'),
    path('admin-panel/users/', views.admin_users, name='admin-users'),
    
    # wishlist URLs
    path('wishlist/add/<int:id>/', views.wishlist_add, name='wishlist-add'),
    path('wishlist/remove/<int:id>/', views.wishlist_remove, name='wishlist-remove'),
]