from django.contrib import admin

from .models import AudioFile, Comment


admin.site.register(AudioFile)
admin.site.register(Comment)
