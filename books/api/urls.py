from django.urls import path
from .views import BookApiCreateView, BookApiListView, BookApiView, BookApiUpdateView, BookApiDeleteView

urlpatterns = [
    path('', BookApiListView.as_view(), name='book_list'),
    path('<int:book_id>', BookApiView.as_view(), name='book'),
    path('<int:pk>/update', BookApiUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', BookApiDeleteView.as_view(), name='delete'),
]