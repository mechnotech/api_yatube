from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, PostViewSet

router = DefaultRouter()
router.register('api/v1/users', UserViewSet)
router.register('api/v1/posts', PostViewSet)

urlpatterns = [
    path('api/v1/api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
]
