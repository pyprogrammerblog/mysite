from django.db import models
import datetime


class PublishedManager(models.Manager):
    # get queryset is a built in function so we overwrite that in order to change 'objects' for 'published'
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

    def in_year(self, year):
        return self.get_queryset().filter(
            blogentry__created_gte=datetime.date(year, 1, 1),
            blogentry__created_lte=datetime.date(year, 12, 31),
        )

    def on_day(self, year, month, day):
        return self.get_queryset().filter(created = datetime.date(year, month, day))

    def during_last_month(self):
        return self.get_queryset().filter(
            blogentry__created_gte=datetime.date.today() - datetime.timedelta(days=30),
            blogentry__created_lte=datetime.date.today(),
        )
