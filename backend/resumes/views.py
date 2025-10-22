from rest_framework import generics, permissions
from .models import Resume
from .serializers import ResumeSerializer
from .permissions import IsOwnerOrReadOnly

class ResumeList(generics.ListCreateAPIView):      # list + create
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # set owner automatically

class ResumeDetail(generics.RetrieveUpdateDestroyAPIView):  # get one, update, delete
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = (IsOwnerOrReadOnly, )

