from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
import jwt
from django.conf import settings
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework import viewsets

from .permissions import UsersPermissions
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UsersPermissions,)


@csrf_exempt
def signup(request):
    """Return confirmation code"""
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')

        confirmation_code = get_random_string(length=6)

        user = User.objects.get_or_create(username=username, email=email)
        user.confirmation_code = confirmation_code
        user.save()

        subject = 'Account Confirmation'
        message = f'Please use this confirmation code: {confirmation_code}'
        from_email = 'noreply@example.com'
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

        return JsonResponse({'email': email,
                             'username': username}, status=200)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)


@csrf_exempt
def get_token(request):
    """Return jwt token"""
    if request.method == 'POST':
        username = request.POST.get('username')
        confirmation_code = request.POST.get('confirmation_code')

        user = get_object_or_404(User, username=username)

        if user.is_active:
            return JsonResponse(
                {'message': 'User account already activated.'},
                status=400)

        if confirmation_code != user.confirmation_code:
            return JsonResponse(
                {'message': 'Invalid confirmation code.'},
                status=400)

        user.is_active = True
        user.save()

        token_payload = {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(days=7)
        }
        token = jwt.encode(
            token_payload,
            settings.SECRET_KEY,
            algorithm='HS256')

        return JsonResponse({'token': token})
    else:
        return JsonResponse({'message': 'Invalid request method.'})
