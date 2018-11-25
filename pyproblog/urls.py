from django.conf.urls import url
from . import views

app_name = 'pyproblog'

urlpatterns = [
    url(r'^$', views.MyHomeListView.as_view(), name='home'),
    url(r'^posts/(?P<tag>[-\w]+)/$', views.MyPostByTagListView.as_view(), name='entry_tag'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$', views.post_detail, name='entry_details'),
    url(r'^about/$', views.MyAboutTemplateView.as_view(), name='about'),
    url(r'^contact/$', views.MyContactFormView.as_view(), name='contact'),
    url(r'^archive/$', views.MyArchiveTemplateView.as_view(), name='archive'),
    url(r'^search/$', views.MySearchView.as_view(), name='search'),
    # url(r'^subscribe/$', views.MySubscriptionView.as_view(), name='subscribe'),
    # url(r'^email_verify/(?P<subscriber_id>\d+)/(?P<verification_code>[0-9A-Fa-f-]+)', views.EmailVerifyView.as_view(),
    #     name='email_verify'),
    # url(r'^thanks/$', views.MySearchView.as_view(), name='thanks'),
    # url(r'^unsubscribe/(?P<unsubscribe_code>[0-9A-Fa-f-]+)', views.EmailUnsubscribeView.as_view(), name='unsubscribe'),
]
