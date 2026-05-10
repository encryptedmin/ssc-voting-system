from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from elections.models import Election
from candidates.models import Position, Candidate
from .models import Vote


@login_required
def ballot_view(request, election_id):

    election = get_object_or_404(Election, id=election_id)

    now = timezone.now()

    if not election.is_active:
        messages.error(request, 'Election is inactive.')
        return redirect('voter_dashboard')

    if now < election.start_time:
        messages.error(request, 'Voting has not started yet.')
        return redirect('voter_dashboard')

    if now > election.end_time:
        messages.error(request, 'Voting period has ended.')
        return redirect('voter_dashboard')

    already_voted = Vote.objects.filter(
        voter=request.user,
        election=election
    ).exists()

    if already_voted:
        messages.error(request, 'You already voted in this election.')
        return redirect('voter_dashboard')

    positions = Position.objects.filter(
        election=election
    )

    data = []

    for position in positions:

        candidates = Candidate.objects.filter(
            position=position
        )

        data.append({
            'position': position,
            'candidates': candidates
        })

    return render(request, 'voting/ballot.html', {
        'data': data,
        'election': election
    })


@login_required
def submit_vote(request, election_id):

    election = get_object_or_404(Election, id=election_id)

    already_voted = Vote.objects.filter(
        voter=request.user,
        election=election
    ).exists()

    if already_voted:
        messages.error(request, 'You already voted.')
        return redirect('voter_dashboard')

    if request.method == 'POST':

        positions = Position.objects.filter(
            election=election
        )

        for position in positions:

            candidate_id = request.POST.get(str(position.id))

            if candidate_id:

                candidate = Candidate.objects.get(
                    id=candidate_id
                )

                Vote.objects.create(
                    voter=request.user,
                    election=election,
                    candidate=candidate
                )

        messages.success(request, 'Vote submitted successfully.')

        return redirect('voter_dashboard')

    return redirect('voter_dashboard')


@login_required
def results_view(request, election_id):

    election = get_object_or_404(Election, id=election_id)

    positions = Position.objects.filter(
        election=election
    )

    results = []

    for position in positions:

        candidates = Candidate.objects.filter(
            position=position
        )

        candidate_results = []

        for candidate in candidates:

            total_votes = Vote.objects.filter(
                election=election,
                candidate=candidate
            ).count()

            candidate_results.append({
                'candidate': candidate,
                'votes': total_votes,
                'chart_votes': total_votes,
            })

        candidate_results = sorted(
            candidate_results,
            key=lambda x: x['votes'],
            reverse=True
        )

        results.append({
            'position': position,
            'results': candidate_results
        })

    return render(request, 'voting/results.html', {
        'results': results,
        'election': election
    })