from django.db import models


class Election(models.Model):

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True, null=True)

    start_time = models.DateTimeField()

    end_time = models.DateTimeField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title