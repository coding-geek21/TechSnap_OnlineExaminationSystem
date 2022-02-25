from django.contrib import admin
from .import models

admin.site.register(models.Subject)
admin.site.register(models.TestName)
admin.site.register(models.Questions)
admin.site.register(models.Answer)
