from django.db import models
from elections.models import Election


class Position(models.Model):

    election = models.ForeignKey(Election, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.election.title})"


class Candidate(models.Model):

    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    fullname = models.CharField(max_length=200)

    photo = models.ImageField(upload_to='candidates/')

    platform = models.TextField()

    def __str__(self):
        return self.fullname