from __future__ import absolute_import

from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from django.urls import reverse_lazy
from django.template import Template, Context
from django.utils import timezone


@shared_task()
def send_email_registration(id):
    """
    Task to send an e-mail notification when an order is successfully created.
    """
    from pyproblog.models import Email
    email = Email.objects.get(pk=id)
    try:
        send_mail(email.subject, '', settings.EMAIL_PROVIDER, [email.to], html_message=email.text)
        email.sent_date = timezone.now()
    except Exception as e:
        email.error_message = e
    finally:
        email.save()


@shared_task()
def send_weekly_mass_email():
    """
    Task to send an e-mail notification when an order is successfully created.
    """
    from pyproblog.models import Subscriber, EditableTemplate, Email
    queryset = Subscriber.objects.filter(email_verified=True)
    for subscriber in queryset:
        email = Email.objects.create(to=subscriber.email, subject="Hi, {}".format(subscriber.email))
        try:
            context = {
                'link_unsubscribe': 'https://pyprogrammer.com' + str(reverse_lazy(
                    'pyproblog:unsubscribe',
                    kwargs={'unsubscribe_code': subscriber.unsubscribe_code}, ))
            }
            template = Template(EditableTemplate.objects.get(name__exact='weekly_email').text).render(Context(context))
            email.text = template
            send_mail('I hope you had a nice week!', '', settings.EMAIL_PROVIDER, [subscriber.email], html_message=template)
            email.sent_date = timezone.now()
        except Exception as e:
            email.error_message = e
        finally:
            email.save()


@shared_task()
def send_email_to_me(subject, body):
    """
    For notification
    """
    return send_mail(subject, body, settings.EMAIL_PROVIDER, [settings.EMAIL_TO_ME])


# JUST FOR TESTING

@shared_task()
def send_weekly_mass_email_to_me():
    """
    For testing.
    """
    from pyproblog.models import EditableTemplate
    context = {
            'link_unsubscribe': 'http://127.0.0.1:8000' +
                                str(reverse_lazy('pyproblog:unsubscribe', kwargs={'unsubscribe_code': 0000}, ))}
    template = Template(EditableTemplate.objects.get(name__exact='weekly_email').text).render(Context(context))
    send_mail('Testing!', '', settings.EMAIL_PROVIDER, [settings.EMAIL_TO_ME], html_message=template)
