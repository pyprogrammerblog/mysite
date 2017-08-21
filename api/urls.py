from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view
from rest_framework.schemas import get_schema_view

from api import views

router = DefaultRouter()
router.register(r'posts', views.BlogEntryModelSet)
router.register(r'titles', views.BlogEntryTitleModelSet)
router.register(r'tags', views.TagModelSet)

schema_view = get_schema_view(title='API PyProgrammer')

urlpatterns = [
    url('^$', schema_view, name='swagger'),
    url(r'^', include(router.urls)),
]
