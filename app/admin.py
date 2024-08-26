from django.contrib import admin
from .models import Profile,ConsentDocument,ConsentStatus

admin.site.register(Profile)
admin.site.register(ConsentDocument)
admin.site.register(ConsentStatus)
