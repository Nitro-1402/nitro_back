from django.contrib import admin
from . import models

admin.site.register(models.Bookmarks)
admin.site.register(models.Favourites)
admin.site.register(models.Watchedlist)
