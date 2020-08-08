"""lori_assignment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from .views import index, home, balance
from rest_framework_swagger.views import get_swagger_view
from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', index, name='index'),
    path('home', home, name='home'),
    path('balance', balance, name='balance'),
    path('user/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('api/rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('api-token-verify/', verify_jwt_token),
    path('api/v1/accounts/', include(('users.api.v1.urls', 'users'), namespace='users-api')),
    path('api/v1/books/', include(('books.api.v1.urls', 'books'), namespace='books-api')),
    path('api/v1/book_rentals/', include(('book_rentals.api.v1.urls', 'book_rentals'), namespace='book_rentals-api')),
    path('api/v2/books/', include(('books.api.v2.urls', 'books_v2'), namespace='books-api-v2')),
    path('api/v2/book_rentals/', include(('book_rentals.api.v2.urls', 'book_rentals_v2'), namespace='book_rentals-api-v2')),
    path('api/v3/book_rentals/', include(('book_rentals.api.v3.urls', 'book_rentals_v3'), namespace='book_rentals-api-v3')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
