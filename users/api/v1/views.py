from rest_framework import generics
from django.db.models import Q
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth.models import User

from .serializers import UserSerializer
from users.models import CustomUser


# class UserApiCreateView(generics.CreateAPIView):
#     serializer_class = UserSerializer
    
    
class UserApiListView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserApiView(generics.ListAPIView):
    serializer_class = UserSerializer
    def get_queryset(self, *args, **kwargs):
        qs = CustomUser.objects.filter(id=self.kwargs['user_id'])
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(username__icontains=query) 
                )
        return qs


class UserApiUpdateView(generics.UpdateAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]
    
    