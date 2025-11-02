from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('vote/', views.vote_view, name='vote'),
    path('vote/results/', views.vote_results, name='vote_results'),
    path('candidates/', views.candidates, name='candidates'),
    path('candidates/vote/<int:candidate_id>/', views.cast_vote, name='cast_vote'),
    path('manifesto/<int:candidate_id>/', views.manifesto, name='manifesto'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-results/', views.admin_results, name='admin_results'),
    path('export-votes/', views.export_votes_to_excel, name='export_votes'),
    path('export-detailed-votes/', views.export_detailed_votes_to_csv, name='export_detailed_votes'),
    path('voter-guide/', views.voter_guide, name='voter_guide'),
    path('security/', views.security, name='security'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
]