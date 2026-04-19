from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Painting, PaintingRequest
from .forms import RegisterForm, LoginForm, PaintingRequestForm


# ─────────────────────────────────────────────
# Home / Landing Page
# ─────────────────────────────────────────────

def home(request):
    """Main landing page with featured paintings."""
    featured_paintings = Painting.objects.filter(is_featured=True, is_available=True)[:6]
    all_paintings = Painting.objects.filter(is_available=True)[:6]
    # If no featured, fall back to latest
    gallery_items = featured_paintings if featured_paintings.exists() else all_paintings
    context = {
        'gallery_items': gallery_items,
        'total_paintings': Painting.objects.filter(is_available=True).count(),
    }
    return render(request, 'core/home.html', context)


# ─────────────────────────────────────────────
# Gallery
# ─────────────────────────────────────────────

def gallery(request):
    """Full gallery page with filter support."""
    style_filter = request.GET.get('style', '')
    search_query = request.GET.get('q', '')

    paintings = Painting.objects.filter(is_available=True)

    if style_filter:
        paintings = paintings.filter(style=style_filter)

    if search_query:
        paintings = paintings.filter(
            Q(title__icontains=search_query) |
            Q(artist_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    style_choices = Painting.STYLE_CHOICES

    context = {
        'paintings': paintings,
        'style_choices': style_choices,
        'active_style': style_filter,
        'search_query': search_query,
    }
    return render(request, 'core/gallery.html', context)


# ─────────────────────────────────────────────
# Painting Detail
# ─────────────────────────────────────────────

def painting_detail(request, pk):
    """Detail page for a single painting."""
    painting = get_object_or_404(Painting, pk=pk, is_available=True)
    related = Painting.objects.filter(style=painting.style, is_available=True).exclude(pk=pk)[:4]
    context = {
        'painting': painting,
        'related': related,
    }
    return render(request, 'core/painting_detail.html', context)


# ─────────────────────────────────────────────
# Custom Painting Request
# ─────────────────────────────────────────────

@login_required
def request_painting(request):
    """Form for submitting a custom painting commission."""
    if request.method == 'POST':
        form = PaintingRequestForm(request.POST, request.FILES)
        if form.is_valid():
            painting_req = form.save(commit=False)
            painting_req.user = request.user
            painting_req.save()
            messages.success(
                request,
                f"✨ Your custom painting request has been submitted successfully! "
                f"We'll contact you at {painting_req.email} within 24 hours."
            )
            return redirect('request_success')
        else:
            messages.error(request, "Please fix the errors below and try again.")
    else:
        # Pre-fill name and email if user is logged in
        initial = {
            'name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
        }
        form = PaintingRequestForm(initial=initial)

    return render(request, 'core/request_painting.html', {'form': form})


def request_success(request):
    """Success page after painting request submission."""
    return render(request, 'core/request_success.html')


# ─────────────────────────────────────────────
# User Dashboard
# ─────────────────────────────────────────────

@login_required
def dashboard(request):
    """User dashboard showing their painting requests."""
    user_requests = PaintingRequest.objects.filter(user=request.user)
    context = {
        'user_requests': user_requests,
        'pending_count': user_requests.filter(status='pending').count(),
        'in_progress_count': user_requests.filter(status='in_progress').count(),
        'completed_count': user_requests.filter(status='completed').count(),
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def request_detail(request, pk):
    """Detail view of a single painting request (user must own it)."""
    painting_request = get_object_or_404(PaintingRequest, pk=pk, user=request.user)
    return render(request, 'core/request_detail.html', {'req': painting_request})


# ─────────────────────────────────────────────
# Authentication
# ─────────────────────────────────────────────

def register_view(request):
    """User registration."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to RangAura, {user.username}! Your account is ready. 🎨")
            return redirect('dashboard')
        else:
            messages.error(request, "Registration failed. Please check the details below.")
    else:
        form = RegisterForm()

    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    """User login."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}! 🎨")
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = LoginForm(request)

    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    """User logout."""
    if request.method == 'POST':
        logout(request)
        messages.info(request, "You've been logged out. See you soon! 👋")
    return redirect('home')
