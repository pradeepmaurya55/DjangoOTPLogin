from django.core.mail import send_mail
import random
from django.conf import settings
from .models import User
from datetime import *

def send_otp(email):
    subject ='Account Login/Register email'
    otp=random.randint(1000,9999)
    email_from = settings.EMAIL_HOST
    message = f'Your otp is {otp}'
    send_mail(subject,message,email_from,[email])
    user_obj = User.objects.get(email=email)
    user_obj.otp=otp
    user_obj.otp_created = datetime.now(timezone.utc)
    user_obj.save()
