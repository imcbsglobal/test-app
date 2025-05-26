import logging
from rest_framework.permissions import BasePermission
import jwt
from django.conf import settings
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

logger = logging.getLogger(__name__)

class IsAdminAuthenticated(BasePermission):
    def has_permission(self, request, view):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            logger.warning("Missing or malformed Authorization header")
            return False

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

            # Check if expected claim exists
            if 'username' not in payload:
                logger.warning("JWT token missing 'username' claim")
                return False
            
            # Optionally set user info in request for downstream use
            request.user = payload['username']  # or fetch actual user if needed

            logger.debug(f"JWT token valid for user: {request.user}")
            return True

        except ExpiredSignatureError:
            logger.warning("JWT token has expired.")
            return False
        except InvalidTokenError:
            logger.warning("JWT token is invalid.")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during token verification: {str(e)}", exc_info=True)
            return False
