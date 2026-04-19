from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import PaintingRequest


# ─────────────────────────────────────────────
# Auth Forms
# ─────────────────────────────────────────────

class RegisterForm(forms.ModelForm):
    """User registration form with email + confirm password."""

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Create a strong password',
            'class': 'ra-input',
            'autocomplete': 'new-password',
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password',
            'class': 'ra-input',
            'autocomplete': 'new-password',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Choose a username',
                'class': 'ra-input',
                'autocomplete': 'username',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your email address',
                'class': 'ra-input',
                'autocomplete': 'email',
            }),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """Styled login form reusing Django's built-in AuthenticationForm."""

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Your username',
            'class': 'ra-input',
            'autocomplete': 'username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password',
            'class': 'ra-input',
            'autocomplete': 'current-password',
        })
    )


# ─────────────────────────────────────────────
# Painting Request Form
# ─────────────────────────────────────────────

class PaintingRequestForm(forms.ModelForm):
    """Form for submitting a custom painting commission request."""

    class Meta:
        model = PaintingRequest
        fields = [
            'name', 'email', 'phone', 'address',
            'image', 'description',
            'preferred_style', 'preferred_size', 'budget',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your full name',
                'class': 'ra-input',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your email address',
                'class': 'ra-input',
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Phone number (optional)',
                'class': 'ra-input',
            }),
            'address': forms.Textarea(attrs={
                'placeholder': 'Delivery address (city, state, PIN)',
                'class': 'ra-input ra-textarea',
                'rows': 3,
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'ra-file-input',
                'accept': 'image/*',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Describe your vision in detail — theme, mood, colours, characters, story...',
                'class': 'ra-input ra-textarea',
                'rows': 5,
            }),
            'preferred_style': forms.Select(attrs={
                'class': 'ra-input ra-select',
            }),
            'preferred_size': forms.TextInput(attrs={
                'placeholder': 'e.g. A4, 24×36 inches',
                'class': 'ra-input',
            }),
            'budget': forms.TextInput(attrs={
                'placeholder': 'e.g. ₹2,000 – ₹5,000',
                'class': 'ra-input',
            }),
        }
        labels = {
            'image': 'Reference / Inspiration Image (optional)',
            'preferred_style': 'Art Style',
            'preferred_size': 'Preferred Canvas Size',
            'budget': 'Your Budget (INR)',
        }
