from django.contrib import admin
from .models import Candidate, Vote

# Register your models here.
admin.site.register(Candidate)
admin.site.register(Vote)