from django.shortcuts import render
from .models import Candidate


def candidate_list(request):

    candidates = Candidate.objects.all()

    return render(request, 'candidates/candidate_list.html', {
        'candidates': candidates
    })