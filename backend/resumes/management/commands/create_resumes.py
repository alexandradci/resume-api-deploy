from django.core.management.base import BaseCommand
from resumes.models import Resume
from django.utils import timezone
import random

class Command(BaseCommand):
    help = "Create 10 random Resume instances for testing."

    def handle(self, *args, **options):
        sample_names = [
            "Alice Smith", "Bob Johnson", "Carol Williams", "David Brown",
            "Emily Davis", "Frank Miller", "Grace Wilson", "Henry Moore",
            "Ivy Taylor", "Jack Anderson"
        ]

        sample_skills = [
            "Python", "Django", "React", "Machine Learning", "SQL",
            "Docker", "Git", "Linux", "REST APIs", "JavaScript"
        ]

        sample_jobs = [
            "Software Developer at TechCorp",
            "Web Engineer at CodeFactory",
            "Backend Developer at DataSystems",
            "AI Assistant at NeuralNet",
        ]

        sample_education = [
            "BSc Computer Science, University of Berlin",
            "MSc Software Engineering, TU Munich",
            "Certificate in Data Science, Coursera"
        ]

        Resume.objects.all().delete()  # Clear old data first
        for _ in range(10):
            name = random.choice(sample_names)
            resume = Resume.objects.create(
                name=name,
                bio=f"{name} is a highly motivated developer with passion for coding.",
                skills=", ".join(random.sample(sample_skills, 5)),
                address=f"{random.randint(10, 99)} Berlin Street, Germany",
                job_history="\n".join(random.sample(sample_jobs, 2)),
                education_history="\n".join(random.sample(sample_education, 2)),
            )
            self.stdout.write(self.style.SUCCESS(f"Created resume for {resume.name}"))

        self.stdout.write(self.style.SUCCESS("Successfully created 10 resumes."))
