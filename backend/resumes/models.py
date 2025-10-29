from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Resume(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='resumes',
        help_text="The user who owns this resume."
    )
    name = models.CharField(max_length=255, help_text="Full name of the person.")
    bio = models.TextField(help_text="A short biography or profile summary.")
    address = models.CharField(max_length=255, help_text="Current address of the user.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the resume was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Timestamp when the resume was last updated.")

    def __str__(self):
        return self.name


class Skill(models.Model):
    resume = models.ForeignKey(Resume, related_name='skills', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    skill_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return f"{self.name} ({self.skill_level}/5)"


class JobHistory(models.Model):
    resume = models.ForeignKey(Resume, related_name='job_history', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    order = models.PositiveIntegerField(default=0)
    job_title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.job_title} ({self.start_date} - {self.end_date})"


class EducationHistory(models.Model):
    resume = models.ForeignKey(Resume, related_name='education_history', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    qualification = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.qualification}"
