from django.urls import path
from . import views

urlpatterns = [
    # ── Main Pages ──────────────────────────────────
    path('', views.home, name='home'),
    path('gallery/', views.gallery, name='gallery'),
    path('gallery/<int:pk>/', views.painting_detail, name='painting_detail'),

    # ── Custom Painting Request ──────────────────────
    path('request-painting/', views.request_painting, name='request_painting'),
    path('request-painting/success/', views.request_success, name='request_success'),

    # ── User Dashboard ───────────────────────────────
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/request/<int:pk>/', views.request_detail, name='request_detail'),

    # ── Authentication ───────────────────────────────
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
