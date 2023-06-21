from django.urls import include, path
from rest_framework import routers

from users.views import UserViewSet, UserSignUpView, ConfirmCodeView


router_v1 = routers.DefaultRouter()
router_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/signup/', UserSignUpView.as_view(), name='signup'),
    path('auth/token/', ConfirmCodeView.as_view(), name='token'),
    # path('auth/token/', VerifyCodeTokenObtainPairView.as_view()),
    # path('users/<str:username>/', UsernameView.as_view()),
    # path('users/', UsersView.as_view()),
]
