from django.urls import path
from .views import UserApiListView, UserApiView, UserApiUpdateView

urlpatterns = [
    path('', UserApiListView.as_view(), name='user_list'),
    path('<int:user_id>', UserApiView.as_view(), name='user'),
    path('<int:pk>/update', UserApiUpdateView.as_view(), name='update'),
]