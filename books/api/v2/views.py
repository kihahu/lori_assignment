from rest_framework import generics
from django.db.models import Q
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import BookSerializer
from books.models import Book


class BookApiCreateView(generics.CreateAPIView):
    serializer_class = BookSerializer
    
    
class BookApiListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookApiView(generics.ListAPIView):
    serializer_class = BookSerializer
    def get_queryset(self, *args, **kwargs):
        qs = Book.objects.filter(id=self.kwargs['book_id'])
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(name__icontains=query) 
                )
        return qs


class BookApiUpdateView(generics.UpdateAPIView):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    
class BookApiDeleteView(generics.DestroyAPIView):
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    