from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.core.cache import cache
from .models import User, UserProfile

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'accounts/register.html')

        user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
        UserProfile.objects.create(user=user)

        # Send verification email
        token = get_random_string(length=32)
        cache.set(f'verify_{token}', user.id, timeout=3600) # 1 hour

        verify_url = request.build_absolute_uri(reverse('accounts:verify_email', args=[token]))

        try:
            send_mail(
                'Verify your StudentHub Account',
                f'Please click this link to verify your account: {verify_url}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Registration successful. Please check your email to verify your account.')
            return redirect('accounts:login')
        except Exception as e:
            # For development, if SMTP isn't fully configured, print and auto-verify or warn
            print(f"EMAIL ERROR: {e}")
            print(f"VERIFICATION LINK: {verify_url}")
            messages.warning(request, f'Registration successful, but email could not be sent. For dev purposes, check the console for the verification link.')
            return redirect('accounts:login')

    return render(request, 'accounts/register.html')

def verify_email(request, token):
    user_id = cache.get(f'verify_{token}')
    if user_id:
        user = User.objects.get(id=user_id)
        user.is_email_verified = True
        user.save()
        cache.delete(f'verify_{token}')
        messages.success(request, 'Email verified successfully! You can now login.')
    else:
        messages.error(request, 'Invalid or expired verification link.')
    return redirect('accounts:login')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if not user.is_email_verified:
                messages.error(request, 'Please verify your email before logging in.')
            else:
                login(request, user)
                return redirect('accounts:profile')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('accounts:login')

@login_required
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        profile.department = request.POST.get('department', '')
        profile.batch = request.POST.get('batch', '')
        profile.hostel = request.POST.get('hostel', '')
        profile.interests = request.POST.get('interests', '')
        profile.mobile_number = request.POST.get('mobile_number', '')
        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('accounts:profile')
    return render(request, 'accounts/profile.html', {'profile': profile})
