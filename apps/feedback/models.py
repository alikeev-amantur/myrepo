from django.contrib.auth import get_user_model
from django.db import models

from apps.partner.models import Establishment

User = get_user_model()


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    establishment = models.ForeignKey(
        Establishment, on_delete=models.CASCADE, related_name="feedback"
    )
    text = models.TextField()

    def __str__(self):
        return f"Feedback of {self.establishment.name} from {self.user}"


class FeedbackAnswer(models.Model):
    feedback = models.ForeignKey(
        Feedback, on_delete=models.CASCADE, related_name="feedback_answers"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    text = models.TextField()

    def __str__(self):
        return f"Answer for {self.feedback} from {self.user}"
