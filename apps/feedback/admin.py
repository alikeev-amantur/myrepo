from django.contrib import admin

from .models import Feedback, FeedbackAnswer

admin.site.register(Feedback)
admin.site.register(FeedbackAnswer)
