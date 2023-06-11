from django.urls import path
from rest_framework.routers import SimpleRouter

from users.views import get_token, UserViewSet, signup

router = SimpleRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('auth/signup/', signup),
    path('auth/token/', get_token),
]
