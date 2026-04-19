from django.db import models

# Create your models here.

# Models for card sets and individual cards (FK)
class Set(models.Model):
    name = models.CharField(max_length=100) # card set name, eg "Twilight Masquerade"
    code = models.CharField(max_length=10) # card set code, eg "TWM"
    slug = models.SlugField(unique=True)

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
    
    name = models.CharField(max_length=200) # card name, eg "Dreepy"
    set = models.ForeignKey(Set, on_delete=models.CASCADE) # foreign key to Set model
    rarity = models.CharField(max_length=25, choices=RARITY) # card rarity
    region = models.CharField(max_length=5, choices=REGION, default='en') # card region, default to EN
    card_number = models.CharField(max_length=20) # card number in the set, eg "TWM 128/167"
    images = models.ImageField(upload_to='card_images/', blank=True) # card images
    price = models.DecimalField(max_digits=6, decimal_places=2) # card price
    
    
    def __str__(self):
        return f"{self.name} - {self.set.code} {self.card_number}"