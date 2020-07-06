from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from api.views import CommentViewSet, PostViewSet

router = DefaultRouter()
router.register(r'v1/posts', PostViewSet)
router.register(
    r'v1/posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='post_comments'
)

urlpatterns = [
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
]
