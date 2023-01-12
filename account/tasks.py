from celery import shared_task
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

User = get_user_model()
token_generator = PasswordResetTokenGenerator()


@shared_task
def user_register(email, domain, use_https):
    """
    Task to send email notification on successful registration.
    """
    user = User.objects.get(username=email)
    html_message = render_to_string('account/register_email.html', {
        'user': user,
        'token': token_generator.make_token(user),
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'domain': domain,
        'protocol': 'https' if use_https else 'http'
    })
    if user.first_name:
        subject = f'{user.first_name}, ви успішно зареєструвались на сайті Par.ost.ok'
    else:
        subject = f'{user.username}, ви успішно зареєструвались на сайті Par.ost.ok'
    mail_sent = send_mail(subject,
                          '',
                          'Par.ost.ok',
                          [user.email],
                          html_message=html_message
                          )
    return mail_sent
