# api/views.py
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from datetime import datetime, timedelta
from django.conf import settings
from .models import AdminCredential
from django.contrib.auth.hashers import check_password
import jwt
from .permissions import IsAdminAuthenticated



# INDEX VIEW
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

# HOME VIEW
class HomeView(APIView):
    def get(self, request):
        #return Response({"message": "Welcome to the Omega-Backend API"})
        return render(request, 'home.html')

# LOGIN VIEW
class LoginView(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = AdminCredential.objects.get(username=username)
        except AdminCredential.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if user.password != password:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(days=365),  # Token valid for 1 year
            'iat': datetime.utcnow()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return Response({'token': token})
    

# LOGOUT VIEW
class LogoutView(APIView):
    def post(self, request):
        # In a real JWT system, you can't "invalidate" the token server-side unless you store a blacklist.
        # This is just a dummy response to indicate a successful logout.
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)

