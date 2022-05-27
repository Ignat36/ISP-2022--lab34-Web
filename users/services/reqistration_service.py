from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate
from django.template.loader import render_to_string
from users.tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User
from django.http import HttpResponse
from users.tasks import send_welcoming_email
from .daos.user_dao import UserDAO
from .daos.profile_dao import ProfileDAO


def successful_registration(user: User, current_site) -> None:
    """Registration view, save form if valid."""
    user.is_active = False
    us_dao = UserDAO()
    us_dao.save(user)
    mail_subject = 'Activate your blog account.'
    message = render_to_string('users/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
    })
    to_email = user.email
    email = EmailMessage(
            mail_subject, message, to=[to_email]
    )

    # send_welcoming_email.delay(user.email)
    email.send()


def account_acrivation(uidb64, token) -> User:
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user: User = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    
    user.is_active = True

    us_dao = UserDAO()
    us_dao.update(user)

    return user

def profile_update(user, profile):
    us_dao = UserDAO()
    us_dao.update(user)

    pr_dao = ProfileDAO()
    pr_dao.update(profile)
    