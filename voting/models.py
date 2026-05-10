from django.db import models

from accounts.models import CustomUser
from elections.models import Election
from candidates.models import Candidate


class Vote(models.Model):

    voter = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    election = models.ForeignKey(Election, on_delete=models.CASCADE)

    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter', 'election', 'candidate')

    def __str__(self):
        return f"{self.voter.username} voted in {self.election.title}"