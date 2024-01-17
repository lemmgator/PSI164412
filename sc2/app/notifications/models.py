from django.db import models
from django.contrib.auth import get_user_model


class Notification(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=255)
    content_id = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.notification_type}'
