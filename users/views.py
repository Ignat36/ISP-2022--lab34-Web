from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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

def register(request):
    """Registration view, save form if valid."""
    if request.method == 'POST':

        form = UserRegisterForm(request.POST)
        if form.is_valid():
            
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Please confirm your email adress.')
            return redirect('news-index')
    
    else:   
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
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
            user_form.save()
            prof_form.save()
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