# api/serializers.py
from rest_framework import serializers
from .models import AdminCredential

class AdminCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminCredential
        fields = ['username', 'password']  # include password if you need it (be cautious)
        extra_kwargs = {
            'password': {'write_only': True}  # hide password in responses for security
        }
