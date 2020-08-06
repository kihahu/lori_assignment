from django.urls import path
from .views import (
    BookRentalApiCreateView, 
    BookRentalApiListView, 
    BookRentalApiView, 
    BookRentalApiUpdateView, 
    BookRentalUserListApiView, 
    BookRentalApiDeleteView,
    BookRentalBalanceApiView
    )

urlpatterns = [
    path('', BookRentalApiListView.as_view(), name='book_rental_list'),
    path('create', BookRentalApiCreateView.as_view(), name='book_rental_create'),
    path('<int:book_rental_ref>', BookRentalApiView.as_view(), name='book_rental'),
    path('users/<int:user_id>', BookRentalUserListApiView.as_view(), name='user_book_rental'),
    path('users/balance/<int:user_id>', BookRentalBalanceApiView.as_view(), name='user_rental_balance'),
    path('<int:pk>/update', BookRentalApiUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', BookRentalApiDeleteView.as_view(), name='delete'),
]