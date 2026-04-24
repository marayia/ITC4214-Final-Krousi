# models.py - Set, Card, WishlistItem and Rating models for the shop app
from django.db import models
from django.contrib.auth.models import User

# Models for card sets and individual cards (FK)
class Set(models.Model):
    name = models.CharField(max_length=60) # card set name, eg "Twilight Masquerade"
    code = models.CharField(max_length=10) # card set code, eg "TWM"
    slug = models.SlugField(unique=True, max_length=60)

    def __str__(self):
        return self.name

# Models for individual cards, PK is card name + set code, eg "Gardevoir VMAX - TWM-001"
class Card(models.Model): 
    # card rarity, naming convention based on https://poketcg.in/blogs/guide/%F0%9F%93%B0-pokemon-card-rarity-explained-all-symbols-meaning-complete-guide
    RARITY = [
        ('common', 'Common'),                           
        ('uncommon', 'Uncommon'),                       
        ('rare', 'Rare'),                              
        ('holo_rare', 'Holo Rare'),                     
        ('reverse_holo', 'Reverse Holo'),               
        ('double_rare', 'Double Rare'),                 
        ('ultra_rare', 'Ultra Rare'),                   
        ('illustration_rare', 'Illustration Rare'),    
        ('special_illustration_rare', 'Special Illustration Rare'),  
        ('hyper_rare', 'Hyper Rare'),                   
        ('secret_rare', 'Secret Rare'),                 
        ('ace_spec', 'ACE SPEC'),                       
        ('promo', 'Promo'),                            
    ]
    # card regions
    REGION = [
        ('en', 'English'),
        ('jp', 'Japanese'),
        ('cn', 'Chinese'),
        ('kr', 'Korean'),
        ('de', 'German'),
        ('fr', 'French'),
        ('it', 'Italian'),
        ('pt', 'Portuguese'),
        ('es', 'Spanish'),
    ]
    
    name = models.CharField(max_length=60) # card name, eg "Dreepy"
    set = models.ForeignKey(Set, on_delete=models.CASCADE) # foreign key to Set model
    rarity = models.CharField(max_length=25, choices=RARITY) # card rarity
    region = models.CharField(max_length=5, choices=REGION, default='en') # card region, default to EN
    card_number = models.CharField(max_length=20) # card number in the set, eg "TWM 128/167"
    images = models.ImageField(upload_to='card_images/', blank=True) # card images
    price = models.DecimalField(max_digits=7, decimal_places=2) # card price
    stock = models.IntegerField(default=1)  # how many of this card we have
    
    def __str__(self):
        return f"{self.name} - {self.set.code} {self.card_number}"

# Model for user wishlist items, FK to User and Card, with timestamp
class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # prevent duplicate wishlist entries for same user + card
        unique_together = ('user', 'card')

    def __str__(self):
        return f"{self.user.username} → {self.card.name}"
    
# Model for user ratings of cards, FK to User and Card, 1-5 stars
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    stars = models.IntegerField()  # 1-5

    class Meta:
        # one rating per user per card
        unique_together = ('user', 'card')

    def __str__(self):
        return f"{self.user.username} rated {self.card.name} {self.stars}/5"