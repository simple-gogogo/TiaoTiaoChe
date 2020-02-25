from _md5 import md5

from django.contrib.sites.models import Site

from tiaotiaoche.document_signals import send_email_signal


def get_current_site():
    site = Site.objects.get_current()
    return site

def get_md5(str):
    m = md5(str.encode('utf-8'))
    return m.hexdigest()

def send_email(emailto, title, content):
    send_email_signal.send(send_email.__class__, emailto=emailto, title=title, content=content)
