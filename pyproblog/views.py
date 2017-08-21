from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.views.generic import TemplateView, ListView, View
from .models import BlogEntry, Subscriber
from django.db.models import Q
from .forms import ContactForm, SubscriberForm
import requests
from django.conf import settings
from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponseNotFound


# Create your views here.
class MyHomeListView(ListView):

    model = BlogEntry
    queryset = BlogEntry.publish.all()
    context_object_name = 'posts'
    template_name = "index.html"
    paginate_by = 9


class MyAboutTemplateView(TemplateView):

    template_name = 'about.html'


class MyContactTemplateView(TemplateView):

    template_name = 'contact.html'


class MyArchiveTemplateView(ListView):

    model = BlogEntry
    queryset = BlogEntry.publish.all()
    context_object_name = 'posts'
    template_name = "archive.html"
    paginate_by = 10


class MyPostByTagListView(ListView):

    model = BlogEntry
    context_object_name = 'posts'
    template_name = "index_tag.html"
    paginate_by = 5

    def get_queryset(self):
        return BlogEntry.objects.filter(tags__tagname__in=[self.kwargs['tag']])

    def get_context_data(self, **kwargs):
        context = super(MyPostByTagListView, self).get_context_data(**kwargs)
        context.update({'tag': self.kwargs['tag']})
        return context


def post_detail(request, year, month, day, post):

    post = get_object_or_404(BlogEntry, slug=post,
                             status='published',
                             published__year=year,
                             published__month=month,
                             published__day=day)

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = BlogEntry.publish.filter(tags__in=post_tags_ids).exclude(pk=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags')[:4]

    return render(request, 'post.html', {'post': post, 'similar_posts': similar_posts})


class MyContactFormView(View):

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            ''' End reCAPTCHA validation '''
            if result['success']:
                form.send_email_to_me()
                form.save()
                messages.success(request, 'reCAPTCHA worked fine!')
                return render(request, 'contact.html', {"form": form, "success": True})
            else:
                messages.error(request, 'Invalid reCAPTCHA!')
                return render(request, 'contact.html', {"form": form, "errors": True, "message": 'Invalid reCAPTCHA!'})

        else:
            messages.error(request, 'Form contain errors')
            return render(request, 'contact.html', {"form": form, "errors": True,
                                                    "message": 'Data in the form is not valid'})

    def get(self, request):
        form = ContactForm()
        return render(request, 'contact.html', {"form": form})


class MySubscriptionView(View):

    def post(self, request):
        form = SubscriberForm(request.POST)
        if form.is_valid():
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            ''' End reCAPTCHA validation '''
            if result['success']:
                form.save()
                messages.success(request, 'reCAPTCHA worked fine!')
                return render(request, 'subscribe.html', {"form": form, "success": True})
            else:
                messages.error(request, 'Invalid reCAPTCHA!')
                return render(request, 'subscribe.html', {"form": form, "errors": True, "message": 'Invalid reCAPTCHA!'})

        else:
            messages.error(request, 'Form contain errors')
            return render(request, 'subscribe.html', {"form": form, "errors": True})

    def get(self, request):
        form = SubscriberForm()
        return render(request, 'subscribe.html', {"form": form})


class EmailVerifyView(View):
    """
    This class change verified true by clicking
    """

    def get(self, request, *args, **kwargs):
        if not self.kwargs.get('subscriber_id') or not self.kwargs.get('verification_code'):
            return HttpResponseNotFound('Something went wrong!')

        user = get_object_or_404(
            Subscriber,
            pk=self.kwargs['subscriber_id'],
            email_verification_code=self.kwargs['verification_code']
        )
        user.email_verified = True
        user.email_verification_code = None
        user.save()
        return render(request, 'subscribed.html', {'message': user})


class EmailUnsubscribeView(View):
    """
    Unsuscribing
    """

    def get(self, request, *args, **kwargs):
        if not self.kwargs.get('unsubscribe_code'):
            return HttpResponseNotFound('Something went wrong!')

        user = get_object_or_404(
            Subscriber,
            unsubscribe_code=self.kwargs['unsubscribe_code']
        )
        user.delete()
        return render(request, 'unsubscribed.html', {})


class MySearchView(View):

    def post(self, request):
        query = request.POST.get("search")

        if query:
            post_entries = BlogEntry.publish.filter(
                Q(title__icontains=query)|
                Q(tags__tagname__icontains=query)
            ).distinct()
            context = {"post_entries": post_entries}

            if post_entries.count() == 0:
                context.update({"message": "No post match the search."})
        else:
            context = {"message": "Please enter a search field before clicking."}

        return render(request, 'search.html', context)

    def get(self, request):
        return render(request, 'search.html', {"message": ""})
