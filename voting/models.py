from django.db import models
from django.contrib.auth.models import User

class Candidate(models.Model):
    """Model representing a candidate in an election"""
    name = models.CharField(max_length=100)
    party = models.CharField(max_length=100)
    image_url = models.URLField()
    manifesto = models.TextField()
    
    def __str__(self):
        return f"{self.name} - {self.party}"

class Vote(models.Model):
    """Model representing a vote cast by a user"""
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('candidate', 'user')  # Ensure one vote per user per candidate
    
    def __str__(self):
        return f"{self.user.username} voted for {self.candidate.name}"