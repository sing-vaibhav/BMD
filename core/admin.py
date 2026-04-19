from django.contrib import admin
from django.utils.html import format_html
from .models import Painting, PaintingRequest


@admin.register(Painting)
class PaintingAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'artist_name', 'style', 'price',
        'aura_total', 'is_featured', 'is_available', 'created_at'
    ]
    list_filter = ['style', 'is_featured', 'is_available']
    search_fields = ['title', 'artist_name', 'description']
    list_editable = ['is_featured', 'is_available', 'price']
    readonly_fields = ['aura_total', 'image_preview', 'created_at']
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'artist_name', 'style', 'description', 'price', 'emoji')
        }),
        ('Image', {
            'fields': ('image', 'image_preview')
        }),
        ('Aura Value System', {
            'fields': (
                'aura_popularity', 'aura_uniqueness',
                'aura_interest', 'aura_expert', 'aura_total'
            ),
            'description': 'Scores are out of 100. The Aura Total is calculated automatically.'
        }),
        ('Visibility', {
            'fields': ('is_featured', 'is_available')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:200px;border-radius:8px;"/>',
                obj.image.url
            )
        return "No image uploaded"
    image_preview.short_description = "Image Preview"

    def aura_total(self, obj):
        score = obj.aura_total
        color = '#22c55e' if score >= 80 else '#f47c20' if score >= 60 else '#ef4444'
        return format_html(
            '<strong style="color:{}">{} / 100</strong>', color, score
        )
    aura_total.short_description = "Aura Score"


@admin.register(PaintingRequest)
class PaintingRequestAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'user', 'email', 'preferred_style',
        'budget', 'status', 'status_badge', 'created_at'
    ]
    list_filter = ['status', 'preferred_style', 'created_at']
    search_fields = ['name', 'email', 'description', 'user__username']
    readonly_fields = ['user', 'created_at', 'updated_at', 'image_preview', 'status_badge']
    list_editable = ['status']
    fieldsets = (
        ('Request Info', {
            'fields': ('user', 'name', 'email', 'phone', 'address')
        }),
        ('Painting Details', {
            'fields': (
                'description', 'preferred_style',
                'preferred_size', 'budget',
                'image', 'image_preview'
            )
        }),
        ('Status', {
            'fields': ('status', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:250px;border-radius:8px;"/>',
                obj.image.url
            )
        return "No reference image uploaded"
    image_preview.short_description = "Reference Image"

    def status_badge(self, obj):
        colors = {
            'pending': '#f47c20',
            'accepted': '#3b82f6',
            'in_progress': '#9b3fb5',
            'completed': '#22c55e',
            'rejected': '#ef4444',
        }
        color = colors.get(obj.status, '#888')
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 10px;'
            'border-radius:50px;font-size:0.78rem;font-weight:600;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = "Status"


# Customize admin site header
admin.site.site_header = "🎨 RangAura Admin"
admin.site.site_title = "RangAura Admin Portal"
admin.site.index_title = "Welcome to RangAura Admin Panel"
