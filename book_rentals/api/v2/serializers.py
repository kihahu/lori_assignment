from django.contrib.auth import get_user_model
from rest_framework import serializers
from book_rentals.models import Book_Rental


class BookRentalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book_Rental
        fields = [
                'ref',
                'user',
                'book',
                'date_rented',
                'status' 
            ]
        
class BookRentalBalanceSerializer(serializers.Serializer):
    
    user_id = serializers.IntegerField()
    balance = serializers.CharField()

   

