from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.http import HttpResponse

def home(request):
    return HttpResponse("Resume project is running")

def health(request):
    return HttpResponse("OK")

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('admin/', admin.site.urls),

   
    path('', include('resumes.urls')),

    path('api-auth/', include('rest_framework.urls')),

    path("api/v3/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v3/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path('', home),
    path('healthz/', health),
]
