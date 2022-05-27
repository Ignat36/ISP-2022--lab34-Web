from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from users.services.reqistration_service import successful_registration, account_acrivation, profile_update
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User
from django.http import HttpResponse
from .tasks import send_welcoming_email


def register(request):
    """Registration view, save form if valid."""
    if request.method == 'POST':

        form = UserRegisterForm(request.POST)
        if form.is_valid():
            successful_registration(
                form.save(commit=False),
                get_current_site(request)
            )

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Please confirm your email adress.')
            return redirect('news-index')
    
    else:   
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def activate(request, uidb64, token):
    user = account_acrivation(uidb64, token)

    if user is not None:
        login(request, user)
        messages.success(request, f'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def profile(request):
    """Profile view with required login."""

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        prof_form = ProfileUpdateForm(request.POST,
                                      request.FILES,
                                      instance=request.user.profile)

        if user_form.is_valid() and prof_form.is_valid():
            profile_update(user_form, prof_form)
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
        
    else:
        user_form = UserUpdateForm(instance=request.user)
        prof_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'prof_form': prof_form
    }

    return render(request, 'users/profile.html', context)