from django.db import models
from django.contrib.auth.models import User


class Painting(models.Model):
    """Represents a painting listed in the gallery."""

    STYLE_CHOICES = [
        ('fantasy', 'Fantasy Art'),
        ('digital', 'Digital Art'),
        ('modern', 'Modern Art'),
        ('abstract', 'Abstract'),
        ('portrait', 'Portrait'),
        ('landscape', 'Landscape'),
    ]

    title = models.CharField(max_length=150)
    artist_name = models.CharField(max_length=100)
    style = models.CharField(max_length=30, choices=STYLE_CHOICES, default='digital')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='paintings/', blank=True, null=True)
    emoji = models.CharField(max_length=10, default='🎨', help_text="Emoji shown when no image uploaded")

    # Aura Value scores (0-100)
    aura_popularity = models.IntegerField(default=80, help_text="Artist popularity score (0-100)")
    aura_uniqueness = models.IntegerField(default=80, help_text="Uniqueness score (0-100)")
    aura_interest = models.IntegerField(default=80, help_text="Buyer interest score (0-100)")
    aura_expert = models.IntegerField(default=80, help_text="Expert review score (0-100)")

    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return f"{self.title} — {self.artist_name}"

    @property
    def aura_total(self):
        """Overall Aura Score as average of four components."""
        return round((self.aura_popularity + self.aura_uniqueness +
                      self.aura_interest + self.aura_expert) / 4)

    @property
    def style_label(self):
        return dict(self.STYLE_CHOICES).get(self.style, self.style)


class PaintingRequest(models.Model):
    """A custom painting commission request submitted by a user."""

    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='painting_requests')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField()
    image = models.ImageField(upload_to='requests/', blank=True, null=True,
                              help_text="Upload a reference image or inspiration photo")
    description = models.TextField(help_text="Describe what you want painted in detail")
    preferred_style = models.CharField(max_length=30, choices=Painting.STYLE_CHOICES,
                                       blank=True, default='digital')
    preferred_size = models.CharField(max_length=50, blank=True,
                                      help_text="e.g. A4, A3, 24x36 inches")
    budget = models.CharField(max_length=50, blank=True,
                              help_text="Your approximate budget in INR")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, help_text="Internal notes for admin")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Request by {self.name} ({self.user.username}) — {self.created_at.strftime('%d %b %Y')}"

    @property
    def status_color(self):
        colors = {
            'pending': '#f47c20',
            'accepted': '#3b82f6',
            'in_progress': '#9b3fb5',
            'completed': '#22c55e',
            'rejected': '#ef4444',
        }
        return colors.get(self.status, '#f47c20')
