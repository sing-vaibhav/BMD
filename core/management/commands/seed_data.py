"""
Management command to seed the database with demo paintings.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from core.models import Painting


DEMO_PAINTINGS = [
    {
        'title': 'Mystic Goddess',
        'artist_name': 'Karan Rana',
        'style': 'fantasy',
        'description': 'A breathtaking fantasy portrait of a celestial goddess adorned with flowers and cosmic energy. Hand-drawn with extraordinary detail.',
        'price': 6500,
        'emoji': '🌸',
        'aura_popularity': 95,
        'aura_uniqueness': 92,
        'aura_interest': 88,
        'aura_expert': 96,
        'is_featured': True,
    },
    {
        'title': 'Melody in Blue',
        'artist_name': 'Shubham Lawate',
        'style': 'digital',
        'description': 'A soulful portrait of a musician lost in the world of music. Blues and purples dance across the canvas.',
        'price': 3800,
        'emoji': '🎵',
        'aura_popularity': 82,
        'aura_uniqueness': 85,
        'aura_interest': 79,
        'aura_expert': 87,
        'is_featured': True,
    },
    {
        'title': "Nature's Spirit",
        'artist_name': 'Karan Rana',
        'style': 'modern',
        'description': 'Modern art piece capturing the spirit of nature — lush greens, flowing water, and living energy.',
        'price': 2900,
        'emoji': '🌿',
        'aura_popularity': 78,
        'aura_uniqueness': 80,
        'aura_interest': 74,
        'aura_expert': 82,
        'is_featured': False,
    },
    {
        'title': 'Storm Warrior',
        'artist_name': 'Shubham Lawate',
        'style': 'fantasy',
        'description': 'A powerful warrior stands at the center of a raging storm, lightning crackling around them. Pure epic fantasy.',
        'price': 5200,
        'emoji': '⚡',
        'aura_popularity': 90,
        'aura_uniqueness': 93,
        'aura_interest': 87,
        'aura_expert': 91,
        'is_featured': True,
    },
    {
        'title': 'Ocean Dreams',
        'artist_name': 'Karan Rana',
        'style': 'modern',
        'description': 'A serene dreamscape of deep ocean blues and teals — perfect for creating a calm, luxurious atmosphere.',
        'price': 3100,
        'emoji': '🌊',
        'aura_popularity': 76,
        'aura_uniqueness': 78,
        'aura_interest': 72,
        'aura_expert': 80,
        'is_featured': False,
    },
    {
        'title': 'Transformation',
        'artist_name': 'Shubham Lawate',
        'style': 'digital',
        'description': 'A woman transforms into a butterfly — representing change, growth, and rebirth. Stunning digital artistry.',
        'price': 4400,
        'emoji': '🦋',
        'aura_popularity': 85,
        'aura_uniqueness': 88,
        'aura_interest': 84,
        'aura_expert': 89,
        'is_featured': True,
    },
    {
        'title': "Krishna's Melody",
        'artist_name': 'Karan Rana',
        'style': 'portrait',
        'description': 'A divine portrait of Lord Krishna playing the flute, surrounded by peacocks and lotus flowers.',
        'price': 7500,
        'emoji': '🪈',
        'aura_popularity': 97,
        'aura_uniqueness': 95,
        'aura_interest': 93,
        'aura_expert': 98,
        'is_featured': True,
    },
    {
        'title': 'Starfire Abstract',
        'artist_name': 'Shubham Lawate',
        'style': 'abstract',
        'description': 'Blazing yellows, reds, and oranges explode across the canvas in a fiery abstract composition.',
        'price': 2500,
        'emoji': '🔥',
        'aura_popularity': 72,
        'aura_uniqueness': 82,
        'aura_interest': 68,
        'aura_expert': 75,
        'is_featured': False,
    },
]


class Command(BaseCommand):
    help = 'Seeds the database with demo paintings for RangAura'

    def handle(self, *args, **options):
        created = 0
        for data in DEMO_PAINTINGS:
            _, was_created = Painting.objects.get_or_create(
                title=data['title'],
                artist_name=data['artist_name'],
                defaults=data
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"  ✓ Created: {data['title']}"))
            else:
                self.stdout.write(f"  – Skipped (exists): {data['title']}")

        self.stdout.write(self.style.SUCCESS(
            f'\n🎨 Done! {created} new paintings added to the database.'
        ))
