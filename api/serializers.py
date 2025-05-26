# api/serializers.py
from rest_framework import serializers
from .models import AdminCredential, AccInvDetails, AccInvMast, AccProduct, AccProduction, AccProductionDetails, AccPurchaseDetails, AccPurchaseMaster

class AdminCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminCredential
        fields = ['username', 'password']  # include password if you need it (be cautious)
        extra_kwargs = {
            'password': {'write_only': True}  # hide password in responses for security
        }


class AccInvDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccInvDetails
        fields = '__all__'


class AccInvMastSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccInvMast
        fields = '__all__'


class AccProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccProduct
        fields = '__all__'



class AccProductionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccProductionDetails
        fields = '__all__'


class AccPurchaseDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccPurchaseDetails
        fields = '__all__'


class AccPurchaseMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccPurchaseMaster
        fields = '__all__'