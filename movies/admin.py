from django.contrib import admin
from . import models

admin.site.register(models.Actor)
admin.site.register(models.Category)
admin.site.register(models.Movie)
admin.site.register(models.Director)
admin.site.register(models.News)
admin.site.register(models.Rating)
admin.site.register(models.Series_episode)
