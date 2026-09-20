import uuid
from django.db import models

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None
    
class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('programming', 'Programming Language'),
        ('framework', 'Framework/Library'),
        ('tool', 'Tool'),
        ('soft-skill', 'Soft Skill'),
        ('language', 'Language'),
    ]

    PROFICIENCY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='programming')
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES, default='intermediate')
    icon = models.URLField(blank=True, null=True)
    added_at = models.DateTimeField()


    def __str__(self):
        return self.name


    class Project(models.Model):

        id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
        title = models.CharField(max_length=255)
        description = models.TextField()
        is_finished = models.BooleanField(default=False)
        project_url = models.URLField(blank=True, null=True)
        timestamp = models.DateTimeField(auto_now_add=True)