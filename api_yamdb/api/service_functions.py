import re

from rest_framework import serializers


def check_username(username):
    if username == 'me':
        raise serializers.ValidationError(
            'Введенное имя недопустимо!'
        )
    if not re.match(r'[\w.@+-]+\Z', username):
        raise serializers.ValidationError(
            'В username использованы недопустимые символы!'
        )
    return username
