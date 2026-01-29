from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from profiles_app.models import UserProfile
from .serializers import ProfileSerializer
from .permissions import IsProfileOwnerOrReadOnly


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.select_related("user").all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsProfileOwnerOrReadOnly]
