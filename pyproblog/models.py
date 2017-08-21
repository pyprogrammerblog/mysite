import uuid

from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from django.db import models
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.template import Template, Context

from .managers import PublishedManager
from .tasks import send_email_registration


class Tag(models.Model):
    tagname = models.CharField(max_length=100)
    created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ("tagname",)

    def __str__(self):
        return self.tagname


class Image(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="img")

    def __str__(self):
        return self.name


class BlogEntry(models.Model):
    STATUS_CHOICES = (
        ('draft', 'DRAFT'),
        ('published', 'PUBLISHED'),
    )
    title = models.CharField(max_length=250)
    subheading = models.CharField(max_length=250)
    tags = models.ManyToManyField(Tag, default="Python")
    slug = models.SlugField(max_length=250, unique_for_date='published')
    author = models.ForeignKey(User, related_name='blog_posts')
    body = models.TextField()
    published = models.DateField(default=timezone.now)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=15, default='draft')
    images = models.ManyToManyField(Image, blank=True)

    # Managers
    objects = models.Manager()
    publish = PublishedManager()

    class Meta:
        ordering = ["-published", ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pyproblog:entry_details', args=[self.published.year,
                                                        self.published.strftime('%m'),
                                                        self.published.strftime('%d'),
                                                        self.slug])


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    send_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.email


class EditableTemplate(models.Model):
    """
    This model defines reusable templates that can be used with Django's template.Template and template.Context
    classes to create and update contextualized templates on the fly without having to change them in the source
    code.
    """

    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=256)
    text = models.TextField()

    class Meta:
        default_permissions = ['manage']
        ordering = ('name',)

    def __str__(self):
        return self.name


class Email(models.Model):
    """
    Used as a queue, every minute a cron job should run a command in management folder.
    """

    created_date = models.DateTimeField(auto_now_add=True)
    sent_date = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    to = models.CharField(max_length=256)
    subject = models.CharField(max_length=256)
    text = models.TextField()

    class Meta:
        default_permissions = ['manage']
        ordering = ('-created_date',)

    def __str__(self):
        return '{} - {} - {}'.format(self.created_date.strftime('%d/%m/%Y'), self.to, self.subject)


class Subscriber(models.Model):

    email = models.EmailField(unique=True)
    created = models.DateField(auto_now_add=True)
    email_verified = models.BooleanField(default=False)
    email_verification_code = models.UUIDField(default=uuid.uuid4, null=True)
    unsubscribe_code = models.UUIDField(default=uuid.uuid4, null=True)

    def __str__(self):
        return self.email

    def send_email_verification_code(self):
        """
        Sends the user an email with a link to click to verify their email address
        """

        if self.email_verification_code:
            verification_code = self.email_verification_code
        else:
            verification_code = uuid.uuid4()
            self.email_verification_code = verification_code
            self.save()

        context = {
            'link': 'https://pyprogrammer.com' + str(reverse_lazy(
                'pyproblog:email_verify',
                kwargs={'subscriber_id': self.id,
                        'verification_code': verification_code})
            ),
            'link_unsubscribe': 'https://pyprogrammer.com' + str(reverse_lazy(
                'pyproblog:unsubscribe',
                kwargs={'unsubscribe_code': self.unsubscribe_code},))
        }
        template = Template(EditableTemplate.objects.get(name__exact='confirm_email').text).render(Context(context))
        email = Email.objects.create(
            to=self.email,
            subject="Hi, {}".format(self.email),
            text=template,
        )
        send_email_registration.delay(email.id)
