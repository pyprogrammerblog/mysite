from django import forms
from .models import Contact
from .models import Subscriber
from .tasks import send_email_to_me


class ContactForm(forms.ModelForm):
    """
    Contact Form is used to contact with owner
    """

    class Meta:
        model = Contact
        fields = ('name', 'email', 'message')

    def send_email_to_me(self):
        subject = 'Jose, you have a new message in PyProgrammer admin'
        body = 'A new message from {}, with email {}, with body {} has been send to you, so please ' \
               'check your admin pannel!'.format(self.cleaned_data.get('name'),
                                                 self.cleaned_data.get('email'),
                                                 self.cleaned_data.get('message'))
        send_email_to_me.delay(subject, body)


class SubscriberForm(forms.ModelForm):
    """
    This form is used to create a new user account.
    """

    class Meta:
        model = Subscriber
        fields = ['email', ]

    def save(self, commit=True):
        instance = super(SubscriberForm, self).save(commit=False)
        if commit:
            instance.save()
            instance.send_email_verification_code()
        return instance
