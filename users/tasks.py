# Create your tasks here

from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail
from celery import shared_task
from time import sleep

@shared_task
def send_welcoming_email(user_mail: str):

    sleep(60)

    mail_subject = 'Welcomr to news project site.'
    mail_message = 'Darova :)'
    send_mail(
        mail_subject,
        mail_message, 
        'sharignat9@gmail.com', 
        [user_mail]
    ) 

    return None




