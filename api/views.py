from rest_framework import permissions
from rest_framework import viewsets, mixins
from .permissions import HasAPIAccess
from .authentications import APIKEYAccess
from .serializers import BlogEntrySerializer, TagSerializer, BlogEntryTitleSerializer
from pyproblog.models import BlogEntry, Tag

from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import detail_route


class BlogEntryModelSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Operations on Entries
    """
    queryset = BlogEntry.objects.all()
    serializer_class = BlogEntrySerializer
    permission_classes = [IsAuthenticated, ]


class BlogEntryTitleModelSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Operations on Entries
    """
    queryset = BlogEntry.objects.all()
    serializer_class = BlogEntryTitleSerializer
    permission_classes = [IsAuthenticated, ]


class TagModelSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Operations on Tags
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated, ]


# import requests
# HasAPIKey
# headers = {
#     'Api-Key': '***'
# }
# r = requests.get(url='https://pyprogrammer.com/api/posts', headers=headers)

# Key Authorization
# headers = {
#     'authorization': '***'
# }
# r = requests.get(
#     url='https://pyprogrammer.com/api/posts', headers=headers)

# r = requests.get(
#     url='http://127.0.0.1:8000/api/posts', auth=('***', '***'))
#