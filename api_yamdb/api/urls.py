from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet, TitleViewSet, CommentViewSet

router_v1 = DefaultRouter()

router_v1.register('reviews', ReviewViewSet, basename='reviews')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)
# router_v1.register(
#     'categories',
#     CategoryViewSet,
#     basename='сategories'
# )

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
