from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail


@shared_task
def sendemail(subject, message, to):
    send_mail(subject, message, 'moflasky@163.com', to)
