from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from collections import defaultdict
import json
from .models import Candidate, Vote

# Sample candidate data (in a real app, this would come from a database)
CANDIDATES_DATA = [
    {
        'id': 1,
        'name': 'Alexandra Chen',
        'party': 'Democratic Party',
        'image_url': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80',
        'manifesto': 'Education is the foundation of a prosperous society. We must invest in our children\'s future by improving school infrastructure, hiring qualified teachers, and providing technology resources to all students. Healthcare accessibility is another priority, ensuring every citizen has access to quality medical care regardless of their economic status.'
    },
    {
        'id': 2,
        'name': 'Marcus Johnson',
        'party': 'Republican Party',
        'image_url': 'https://media.istockphoto.com/id/2174363314/photo/businessman-looking-at-camera.webp?a=1&b=1&s=612x612&w=0&k=20&c=Wg5df0t9j220uqROFaa9o6UizDHNLLVTgan1Qt5A8is=',
        'manifesto': 'Economic growth comes from empowering businesses and creating jobs for our citizens. We will reduce unnecessary regulations, lower corporate taxes, and incentivize companies to invest in our communities. Infrastructure development is key to attracting businesses and improving quality of life for all residents.'
    },
    {
        'id': 3,
        'name': 'Jordan Smith',
        'party': 'Independent',
        'image_url': 'https://images.unsplash.com/photo-1573496358970-09b04b590c4a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80',
        'manifesto': 'Protecting our environment is protecting our future. We must act now for the next generation by implementing sustainable energy policies, reducing carbon emissions, and preserving our natural resources. Social justice and equality are fundamental to a healthy democracy, and we must ensure all voices are heard in our governance.'
    },
    {
        'id': 4,
        'name': 'Sarah Williams',
        'party': 'Green Party',
        'image_url': 'https://images.unsplash.com/photo-1542131522310-0f412615ff00?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=800&q=80',
        'manifesto': 'Healthcare is a human right. We must ensure every citizen has access to quality care through a comprehensive public healthcare system. Climate change is the defining challenge of our time, requiring immediate action to transition to renewable energy sources and create green jobs for our workforce.'
    }
]

def home(request):
    return render(request, 'index.html')

def register(request):
    """Handle user registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('vote')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def custom_logout(request):
    """Custom logout view"""
    logout(request)
    return redirect('home')

@login_required
def vote_view(request):
    """Display the vote page"""
    # Check if user is superuser, redirect to admin dashboard
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    
    # Get vote statistics
    vote_stats = {}
    total_votes = Vote.objects.count()
    
    # Get all candidates
    candidates = []
    for candidate_data in CANDIDATES_DATA:
        # Try to get or create candidate in database
        candidate, created = Candidate.objects.get_or_create(
            id=candidate_data['id'],
            defaults={
                'name': candidate_data['name'],
                'party': candidate_data['party'],
                'image_url': candidate_data['image_url'],
                'manifesto': candidate_data['manifesto']
            }
        )
        candidates.append({
            'id': candidate.id,
            'name': candidate.name,
            'party': candidate.party,
            'image_url': candidate.image_url,
            'manifesto': candidate.manifesto
        })
    
    for candidate_data in candidates:
        candidate_votes = Vote.objects.filter(candidate__id=candidate_data['id']).count()
        vote_stats[candidate_data['id']] = {
            'count': candidate_votes,
            'percentage': (candidate_votes / total_votes * 100) if total_votes > 0 else 0
        }
    
    # Check if user has voted
    user_votes = Vote.objects.filter(user=request.user)
    user_has_voted = user_votes.exists()
    
    context = {
        'candidates': candidates,
        'vote_stats': vote_stats,
        'total_votes': total_votes,
        'user_has_voted': user_has_voted
    }
    
    return render(request, 'vote.html', context)

@login_required
def candidates(request):
    """Display all candidates for voting"""
    # Get all candidates
    candidates = []
    for candidate_data in CANDIDATES_DATA:
        # Try to get or create candidate in database
        candidate, created = Candidate.objects.get_or_create(
            id=candidate_data['id'],
            defaults={
                'name': candidate_data['name'],
                'party': candidate_data['party'],
                'image_url': candidate_data['image_url'],
                'manifesto': candidate_data['manifesto']
            }
        )
        candidates.append({
            'id': candidate.id,
            'name': candidate.name,
            'party': candidate.party,
            'image_url': candidate.image_url,
            'manifesto': candidate.manifesto
        })
    
    # Check if user has voted
    user_votes = Vote.objects.filter(user=request.user)
    user_has_voted = user_votes.exists()
    
    # Get vote statistics
    vote_stats = {}
    total_votes = Vote.objects.count()
    
    for candidate_data in candidates:
        candidate_votes = Vote.objects.filter(candidate__id=candidate_data['id']).count()
        vote_stats[candidate_data['id']] = {
            'count': candidate_votes,
            'percentage': (candidate_votes / total_votes * 100) if total_votes > 0 else 0
        }
    
    context = {
        'candidates': candidates,
        'vote_stats': vote_stats,
        'user_has_voted': user_has_voted
    }
    
    return render(request, 'candidates.html', context)

@login_required
def manifesto(request, candidate_id):
    """Display a candidate's manifesto"""
    # Try to get candidate from database first, then from static data
    try:
        candidate = Candidate.objects.get(id=candidate_id)
        candidate_data = {
            'id': candidate.id,
            'name': candidate.name,
            'party': candidate.party,
            'image_url': candidate.image_url,
            'manifesto': candidate.manifesto
        }
    except Candidate.DoesNotExist:
        candidate_data = None
        for c in CANDIDATES_DATA:
            if c['id'] == candidate_id:
                candidate_data = c
                break
        
        if candidate_data is None:
            raise Http404("Candidate not found")
    
    return render(request, 'manifesto.html', {'candidate': candidate_data})

@login_required
def cast_vote(request, candidate_id):
    """Cast a vote for a candidate"""
    # Try to get candidate from database first, then from static data
    try:
        candidate = Candidate.objects.get(id=candidate_id)
    except Candidate.DoesNotExist:
        # Check if candidate exists in static data
        candidate_exists = any(c['id'] == candidate_id for c in CANDIDATES_DATA)
        if not candidate_exists:
            messages.error(request, "Invalid candidate.")
            return redirect('candidates')
        else:
            # Create candidate in database if it exists in static data
            candidate_data = next(c for c in CANDIDATES_DATA if c['id'] == candidate_id)
            candidate, created = Candidate.objects.get_or_create(
                id=candidate_data['id'],
                defaults={
                    'name': candidate_data['name'],
                    'party': candidate_data['party'],
                    'image_url': candidate_data['image_url'],
                    'manifesto': candidate_data['manifesto']
                }
            )
    
    # Check if user has already voted
    existing_vote = Vote.objects.filter(user=request.user).first()
    if existing_vote:
        messages.error(request, "You have already voted.")
        return redirect('candidates')
    
    # Record the vote
    Vote.objects.create(candidate=candidate, user=request.user)
    messages.success(request, "Your vote has been recorded successfully!")
    return redirect('candidates')

@login_required
def vote_results(request):
    """Display vote results for the current user"""
    # Get all candidates
    candidates = []
    for candidate_data in CANDIDATES_DATA:
        # Try to get or create candidate in database
        candidate, created = Candidate.objects.get_or_create(
            id=candidate_data['id'],
            defaults={
                'name': candidate_data['name'],
                'party': candidate_data['party'],
                'image_url': candidate_data['image_url'],
                'manifesto': candidate_data['manifesto']
            }
        )
        candidates.append({
            'id': candidate.id,
            'name': candidate.name,
            'party': candidate.party,
            'image_url': candidate.image_url,
            'manifesto': candidate.manifesto
        })
    
    # Get vote statistics
    vote_stats = {}
    total_votes = Vote.objects.count()
    
    for candidate_data in candidates:
        candidate_votes = Vote.objects.filter(candidate__id=candidate_data['id']).count()
        vote_stats[candidate_data['id']] = {
            'count': candidate_votes,
            'percentage': (candidate_votes / total_votes * 100) if total_votes > 0 else 0
        }
    
    # Check if user has voted
    user_votes = Vote.objects.filter(user=request.user)
    user_has_voted = user_votes.exists()
    
    context = {
        'candidates': candidates,
        'vote_stats': vote_stats,
        'total_votes': total_votes,
        'user_has_voted': user_has_voted,
        'current_user': request.user
    }
    
    return render(request, 'vote_results.html', context)

@login_required
def admin_dashboard(request):
    """Admin dashboard to view detailed voting statistics"""
    # Check if user is superuser/admin
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('home')
    
    # Get all candidates
    candidates = []
    for candidate_data in CANDIDATES_DATA:
        # Try to get or create candidate in database
        candidate, created = Candidate.objects.get_or_create(
            id=candidate_data['id'],
            defaults={
                'name': candidate_data['name'],
                'party': candidate_data['party'],
                'image_url': candidate_data['image_url'],
                'manifesto': candidate_data['manifesto']
            }
        )
        candidates.append({
            'id': candidate.id,
            'name': candidate.name,
            'party': candidate.party,
            'image_url': candidate.image_url,
            'manifesto': candidate.manifesto
        })
    
    # Get vote statistics
    vote_stats = {}
    total_votes = Vote.objects.count()
    
    for candidate_data in candidates:
        candidate_votes = Vote.objects.filter(candidate__id=candidate_data['id']).count()
        vote_stats[candidate_data['id']] = {
            'count': candidate_votes,
            'percentage': (candidate_votes / total_votes * 100) if total_votes > 0 else 0,
            'name': candidate_data['name'],
            'party': candidate_data['party']
        }
    
    # Prepare data for charts
    chart_data = []
    for candidate_id, stats in vote_stats.items():
        chart_data.append({
            'name': stats['name'],
            'votes': stats['count'],
            'percentage': round(stats['percentage'], 1)
        })
    
    # Get all votes for detailed view
    votes = {}
    for candidate_data in candidates:
        votes[candidate_data['id']] = list(Vote.objects.filter(candidate__id=candidate_data['id']).values_list('user__id', flat=True))
    
    context = {
        'candidates': candidates,
        'vote_stats': vote_stats,
        'total_votes': total_votes,
        'chart_data': json.dumps(chart_data),
        'votes': votes  # Pass the raw votes data
    }
    
    return render(request, 'admin_dashboard.html', context)

@login_required
def admin_results(request):
    """Enhanced admin results view with detailed voting data"""
    # Check if user is superuser
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('home')
    
    # Get all candidates
    candidates = []
    for candidate_data in CANDIDATES_DATA:
        # Try to get or create candidate in database
        candidate, created = Candidate.objects.get_or_create(
            id=candidate_data['id'],
            defaults={
                'name': candidate_data['name'],
                'party': candidate_data['party'],
                'image_url': candidate_data['image_url'],
                'manifesto': candidate_data['manifesto']
            }
        )
        candidates.append({
            'id': candidate.id,
            'name': candidate.name,
            'party': candidate.party,
            'image_url': candidate.image_url,
            'manifesto': candidate.manifesto
        })
    
    # Get vote statistics
    vote_stats = {}
    total_votes = Vote.objects.count()
    
    for candidate_data in candidates:
        candidate_votes = Vote.objects.filter(candidate__id=candidate_data['id']).count()
        vote_stats[candidate_data['id']] = {
            'count': candidate_votes,
            'percentage': (candidate_votes / total_votes * 100) if total_votes > 0 else 0,
            'name': candidate_data['name'],
            'party': candidate_data['party']
        }
    
    # Prepare data for charts
    chart_data = []
    for candidate_id, stats in vote_stats.items():
        chart_data.append({
            'name': stats['name'],
            'votes': stats['count'],
            'percentage': round(stats['percentage'], 1)
        })
    
    # Get all votes for detailed view
    votes = {}
    for candidate_data in candidates:
        votes[candidate_data['id']] = list(Vote.objects.filter(candidate__id=candidate_data['id']).values_list('user__id', flat=True))
    
    context = {
        'candidates': candidates,
        'vote_stats': vote_stats,
        'total_votes': total_votes,
        'chart_data': json.dumps(chart_data),
        'votes': votes,  # Pass the raw votes data
        'current_user': request.user
    }
    
    return render(request, 'admin_results.html', context)

@login_required
def export_votes_to_excel(request):
    """Export voting data to Excel format"""
    # Check if user is superuser/admin
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('home')
    
    # Get all candidates
    candidates = []
    for candidate_data in CANDIDATES_DATA:
        # Try to get or create candidate in database
        candidate, created = Candidate.objects.get_or_create(
            id=candidate_data['id'],
            defaults={
                'name': candidate_data['name'],
                'party': candidate_data['party'],
                'image_url': candidate_data['image_url'],
                'manifesto': candidate_data['manifesto']
            }
        )
        candidates.append({
            'id': candidate.id,
            'name': candidate.name,
            'party': candidate.party,
            'image_url': candidate.image_url,
            'manifesto': candidate.manifesto
        })
    
    # Create CSV content
    csv_content = "Candidate Name,Party,Votes,Percentage\n"
    
    total_votes = Vote.objects.count()
    
    for candidate_data in candidates:
        candidate_votes = Vote.objects.filter(candidate__id=candidate_data['id']).count()
        percentage = (candidate_votes / total_votes * 100) if total_votes > 0 else 0
        csv_content += f"{candidate_data['name']},{candidate_data['party']},{candidate_votes},{percentage:.1f}%\n"
    
    # Add detailed vote data
    csv_content += "\nDetailed Vote Data\n"
    csv_content += "Candidate,Voter ID\n"
    
    for candidate_data in candidates:
        votes = Vote.objects.filter(candidate__id=candidate_data['id'])
        for vote in votes:
            csv_content += f"{candidate_data['name']},{vote.user.id}\n"
    
    # Create HTTP response with CSV content
    response = HttpResponse(content=csv_content.encode('utf-8'), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="voting_data.csv"'
    
    return response

@login_required
def export_detailed_votes_to_csv(request):
    """Export detailed voting data to CSV format"""
    # Check if user is superuser
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('home')
    
    # sare candisates ko fetch karna from db
    candidates = []
    for candidate_data in CANDIDATES_DATA:
        # Try to get or create candidate in database
        candidate, created = Candidate.objects.get_or_create(
            id=candidate_data['id'],
            defaults={
                'name': candidate_data['name'],
                'party': candidate_data['party'],
                'image_url': candidate_data['image_url'],
                'manifesto': candidate_data['manifesto']
            }
        )
        candidates.append({
            'id': candidate.id,
            'name': candidate.name,
            'party': candidate.party,
            'image_url': candidate.image_url,
            'manifesto': candidate.manifesto
        })
    
    # Create CSV content
    csv_content = "Candidate Name,Party,Votes,Percentage\n"
    
    total_votes = Vote.objects.count()
    
    for candidate_data in candidates:
        candidate_votes = Vote.objects.filter(candidate__id=candidate_data['id']).count()
        percentage = (candidate_votes / total_votes * 100) if total_votes > 0 else 0
        csv_content += f"{candidate_data['name']},{candidate_data['party']},{candidate_votes},{percentage:.1f}%\n"
    
    # vote ke details wale data ko add ka
    csv_content += "\nDetailed Vote Data\n"
    csv_content += "Candidate Name,Voter ID,Timestamp\n"
    
    import datetime
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for candidate_data in candidates:
        votes = Vote.objects.filter(candidate__id=candidate_data['id'])
        for vote in votes:
            csv_content += f"{candidate_data['name']},{vote.user.id},{vote.timestamp}\n"
    
    # Create  CSV file ke liye data gather karo
    response = HttpResponse(content=csv_content.encode('utf-8'), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="detailed_voting_data.csv"'
    
    return response

def voter_guide(request):
    """Display the voter guide page"""
    return render(request, 'voter_guide.html')

def security(request):
    """Display the security page"""
    return render(request, 'security.html')

def privacy_policy(request):
    """Display the privacy policy page"""
    return render(request, 'privacy_policy.html')

def terms_of_service(request):
    """Display the terms of service page"""
    return render(request, 'terms_of_service.html')