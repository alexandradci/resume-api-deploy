from rest_framework import generics, permissions, status
from .models import Resume, JobHistory, Skill, EducationHistory
from .serializers import ResumeSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from django.db import transaction


class ResumeList(generics.ListCreateAPIView):      # list + create
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # set owner automatically

class ResumeDetail(generics.RetrieveUpdateDestroyAPIView):  # get one, update, delete
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = (IsOwnerOrReadOnly, )

class ResumeReorderView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk, owner=request.user)

        data = request.data
        required_keys = {"job_history", "skills", "education_history"}

        if set(data.keys()) != required_keys:
            return Response(
                {"detail": "Payload must contain exactly job_history, skills, education_history."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            values = [int(data[k]) for k in ("job_history", "skills", "education_history")]
        except (ValueError, TypeError):
            return Response(
                {"detail": "Values must be integers 0,1,2."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if sorted(values) != [0, 1, 2]:
            return Response(
                {"detail": "Values must be 0,1,2 with no duplicates."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not JobHistory.objects.filter(resume=resume).exists():
            return Response(
                {"detail": "job_history is empty for this resume."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not Skill.objects.filter(resume=resume).exists():
            return Response(
                {"detail": "skills are empty for this resume."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not EducationHistory.objects.filter(resume=resume).exists():
            return Response(
                {"detail": "education_history is empty for this resume."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            JobHistory.objects.filter(resume=resume).update(order=data["job_history"])
            Skill.objects.filter(resume=resume).update(order=data["skills"])
            EducationHistory.objects.filter(resume=resume).update(order=data["education_history"])

        return Response(
            {"detail": "Reordered successfully."},
            status=status.HTTP_200_OK
        )
