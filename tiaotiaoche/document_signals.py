import logging

import django
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver

from tiaotiaoche import settings

send_email_signal = django.dispatch.Signal(providing_args=['emailto', 'title', 'content'])

logger = logging.getLogger(__name__)

@receiver(send_email_signal)
def send_email_signal_handler(sender, **kwargs):
    emailto = kwargs['emailto']
    title = kwargs['title']
    content = kwargs['content']

    msg = EmailMultiAlternatives(title, content, from_email=settings.DEFAULT_FROM_EMAIL, to=emailto)
    msg.content_subtype = "html"

    from servermanager.models import EmailSendLog
    log = EmailSendLog()
    log.title = title
    log.content = content
    log.emailto = ','.join(emailto)

    try:
        result = msg.send()
        log.send_result = result > 0
    except Exception as e:
        logger.error(e)
        log.send_result = False
    log.save()
