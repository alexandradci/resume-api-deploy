from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Resume, JobHistory, Skill, EducationHistory


class ResumeReorderView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk, owner=request.user)

        data = request.data

        required_keys = {"job_history", "skills", "education_history"}

        # 1) Validate keys
        if set(data.keys()) != required_keys:
            return Response(
                {"detail": "Payload must contain exactly job_history, skills, education_history."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2) Validate values are 0,1,2 with no duplicates
        try:
            values = [int(data[k]) for k in ("job_history", "skills", "education_history")]
        except (ValueError, TypeError):
            return Response({"detail": "Values must be integers 0,1,2."}, status=status.HTTP_400_BAD_REQUEST)


        if set(values) != {0, 1, 2}:
            return Response({"detail": "Values must be 0,1,2 with no duplicates."}, status=400)

        # 3) Validate that resume has data for all sections
        if not JobHistory.objects.filter(resume=resume).exists():
            return Response({"detail": "job_history is empty for this resume."}, status=400)

        if not Skill.objects.filter(resume=resume).exists():
            return Response({"detail": "skills are empty for this resume."}, status=400)

        if not EducationHistory.objects.filter(resume=resume).exists():
            return Response({"detail": "education_history is empty for this resume."}, status=400)

        # 4) Update all rows for each section
        JobHistory.objects.filter(resume=resume).update(order=data["job_history"])
        Skill.objects.filter(resume=resume).update(order=data["skills"])
        EducationHistory.objects.filter(resume=resume).update(order=data["education_history"])

        return Response({"detail": "Reordered successfully."}, status=200)
