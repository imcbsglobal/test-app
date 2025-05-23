# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response

class HomeView(APIView):
    def get(self, request):
        return Response({"message": "Welcome to the Omega-Backend API"})
