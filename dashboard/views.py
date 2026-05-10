from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.models import CustomUser
from candidates.models import Candidate
from elections.forms import ElectionForm
from elections.models import Election
from voting.models import Vote


def is_admin(user):
    return user.is_authenticated and user.role == 'ADMIN'


def build_election_insights(elections, total_eligible_voters):
    statistics = []
    live_counts = []

    for election in elections:
        voted_count = Vote.objects.filter(
            election=election
        ).values('voter_id').distinct().count()

        not_voted_count = max(total_eligible_voters - voted_count, 0)

        statistics.append({
            'id': election.id,
            'title': election.title,
            'voted': voted_count,
            'not_voted': not_voted_count,
            'total_voters': total_eligible_voters,
            'total_votes': Vote.objects.filter(election=election).count(),
        })

        candidates = Candidate.objects.filter(
            position__election=election
        ).annotate(vote_count=Count('vote')).order_by(
            'position__name',
            'fullname',
        )

        live_counts.append({
            'id': election.id,
            'title': election.title,
            'labels': [candidate.fullname for candidate in candidates],
            'votes': [candidate.vote_count for candidate in candidates],
        })

    return statistics, live_counts


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_voters = CustomUser.objects.filter(role='VOTER').count()
    approved_voters = CustomUser.objects.filter(
        role='VOTER',
        is_approved=True
    ).count()
    pending_voters = CustomUser.objects.filter(
        role='VOTER',
        is_approved=False
    ).count()
    total_votes = Vote.objects.count()
    total_candidates = Candidate.objects.count()
    total_elections = Election.objects.count()

    elections = Election.objects.all().order_by('-created_at')
    active_elections = elections.filter(is_active=True)
    pending_voter_list = CustomUser.objects.filter(
        role='VOTER',
        is_approved=False
    ).order_by('date_joined')
    approved_voter_list = CustomUser.objects.filter(
        role='VOTER',
        is_approved=True
    ).order_by('username')

    election_statistics, live_election_counts = build_election_insights(
        active_elections,
        approved_voters,
    )

    context = {
        'total_voters': total_voters,
        'approved_voters': approved_voters,
        'pending_voters': pending_voters,
        'total_votes': total_votes,
        'total_candidates': total_candidates,
        'total_elections': total_elections,
        'elections': elections,
        'election_form': ElectionForm(),
        'pending_voter_list': pending_voter_list,
        'approved_voter_list': approved_voter_list,
        'election_statistics': election_statistics,
        'live_election_counts': live_election_counts,
    }

    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def election_create(request):
    if request.method == 'POST':
        form = ElectionForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Election created successfully.')
            return redirect('admin_dashboard')
    else:
        form = ElectionForm()

    return render(request, 'dashboard/election_form.html', {
        'form': form,
        'page_title': 'Create Election',
        'submit_label': 'Create Election',
    })


@login_required
@user_passes_test(is_admin)
def election_update(request, election_id):
    election = get_object_or_404(Election, id=election_id)

    if request.method == 'POST':
        form = ElectionForm(request.POST, instance=election)

        if form.is_valid():
            form.save()
            messages.success(request, 'Election updated successfully.')
            return redirect('admin_dashboard')
    else:
        form = ElectionForm(instance=election)

    return render(request, 'dashboard/election_form.html', {
        'form': form,
        'page_title': 'Edit Election',
        'submit_label': 'Save Changes',
        'election': election,
    })


@login_required
@user_passes_test(is_admin)
@require_POST
def election_delete(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    election.delete()
    messages.success(request, 'Election deleted successfully.')
    return redirect('admin_dashboard')


@login_required
@user_passes_test(is_admin)
@require_POST
def voter_action(request, voter_id, action):
    voter = get_object_or_404(CustomUser, id=voter_id, role='VOTER')

    if action == 'approve':
        voter.is_approved = True
        voter.save(update_fields=['is_approved'])
        messages.success(request, f'{voter.username} has been approved.')
    elif action == 'deny':
        username = voter.username
        voter.delete()
        messages.success(request, f'{username} registration has been denied.')
    elif action == 'delete':
        username = voter.username
        voter.delete()
        messages.success(request, f'{username} has been deleted.')
    else:
        messages.error(request, 'Invalid voter action.')

    return redirect('admin_dashboard')


@login_required
def voter_dashboard(request):
    elections = Election.objects.filter(is_active=True)
    now = timezone.now()
    total_eligible_voters = CustomUser.objects.filter(
        role='VOTER',
        is_approved=True
    ).count()

    election_data = []

    for election in elections:
        if now < election.start_time:
            status = 'Upcoming'
        elif now > election.end_time:
            status = 'Closed'
        else:
            status = 'Ongoing'

        has_voted = Vote.objects.filter(
            voter=request.user,
            election=election
        ).exists()

        election_data.append({
            'election': election,
            'status': status,
            'has_voted': has_voted,
        })

    election_statistics, live_election_counts = build_election_insights(
        elections,
        total_eligible_voters,
    )

    return render(request, 'dashboard/voter_dashboard.html', {
        'election_data': election_data,
        'election_statistics': election_statistics,
        'live_election_counts': live_election_counts,
    })
