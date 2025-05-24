# api/permissions.py
from rest_framework.permissions import BasePermission
import jwt
from django.conf import settings
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

class IsAdminAuthenticated(BasePermission):
    def has_permission(self, request, view):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return False

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            request.user = payload  # Optional: Store decoded data in request
            return True
        except (InvalidTokenError, ExpiredSignatureError):
            return False
