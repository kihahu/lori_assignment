from rest_framework import generics
from django.db.models import Q
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework import permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from book_rentals.api.v1.serializers import BookRentalSerializer, BookRentalBalanceSerializer
from book_rentals.models import Book_Rental


class BookRentalApiCreateView(generics.CreateAPIView):
    
    serializer_class = BookRentalSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    
class BookRentalApiListView(generics.ListCreateAPIView):
    
    queryset = Book_Rental.objects.all()
    serializer_class = BookRentalSerializer
    authentication_classes = (JSONWebTokenAuthentication, )


class BookRentalApiView(generics.ListAPIView):
    
    serializer_class = BookRentalSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    def get_queryset(self, *args, **kwargs):
        qs = Book_Rental.objects.filter(ref=self.kwargs['book_rental_ref'])
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(name__icontains=query) 
                )
        return qs


class BookRentalApiUpdateView(generics.UpdateAPIView):

    queryset = Book_Rental.objects.all()
    serializer_class = BookRentalSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    
    
class BookRentalApiDeleteView(generics.DestroyAPIView):
    
    queryset = Book_Rental.objects.all()
    serializer_class = BookRentalSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    

class BookRentalBalanceApiView(generics.ListAPIView):
    
    serializer_class = BookRentalBalanceSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    def get_queryset(self, *args, **kwargs):
        user_id = self.kwargs['user_id']
        qs = Book_Rental.objects.filter(user__id=user_id)
        count = qs.count()
        balance_list = list(map(get_payment, qs))
        balance = sum(balance_list)
        obj = {
            'user_id': user_id,
            'balance': balance
        }
        return [obj]
    

class BookRentalUserListApiView(generics.ListAPIView):
    
    serializer_class = BookRentalSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    def get_queryset(self, *args, **kwargs):
        qs = Book_Rental.objects.filter(ref=self.kwargs['user_id'])
        qs.count()
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(name__icontains=query) 
                )
        return qs
   
 
def get_payment(rental):
    now = timezone.now()
    total_time = (now - rental.date_rented)
    seconds = total_time.seconds
    days = total_time.days
    microsecond = total_time.microseconds
    rental_charges = 0
    total_days = 0
    
    if microsecond > 0 or seconds > 0:
        total_days = float(days + 1)
    else:
        total_days = float(days)
        
    if rental.book.book_type == 1:
        return total_days * 1.5
    elif rental.book.book_type == 2:
        return total_days * 3
    elif rental.book.book_type == 3:
        return total_days * 1.5
     
        
    
