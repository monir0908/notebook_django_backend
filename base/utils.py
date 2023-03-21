# django
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.conf import Settings, settings
# email utilities
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

def send_email(user):
    
    # used when plain_text needed; django has both plain_text and html
    # plaintext = get_template('email.txt') 
    
    # when template is needed
    _html = get_template('registration_email.html')


    redirect_url = settings.FRONTEND_URL

    context = { 
        'user_full_name': user.first_name + ' ' + user.last_name,
        'user_email': user.email,
        'redirect_url': redirect_url,
    }
    
    subject, from_email, to = 'Notebook | Registration Successful', None, user.email
    # text_content = plaintext.render(context)
    html_content = _html.render(context)
    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
