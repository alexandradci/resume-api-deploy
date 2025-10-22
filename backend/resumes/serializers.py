from rest_framework import serializers
from .models import Resume, Skill, JobHistory, EducationHistory


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name', 'skill_level')


class JobHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobHistory
        fields = ('id', 'start_date', 'end_date', 'job_title', 'description')


class EducationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationHistory
        fields = ('id', 'name', 'qualification')


class ResumeSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, required=False)
    job_history = JobHistorySerializer(many=True, required=False)
    education_history = EducationHistorySerializer(many=True, required=False)

    class Meta:
        model = Resume
        fields = (
            'id', 'owner', 'name', 'bio', 'address',
            'job_history', 'skills', 'education_history', 'created_at',
        )
