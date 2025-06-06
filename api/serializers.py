# api/serializers.py
from rest_framework import serializers
from .models import AccInvDetails, AccInvMast, AccProduct, AccProduction, AccProductionDetails, AccPurchaseDetails, AccPurchaseMaster, AccUsers

class AccUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccUsers
        fields = ['id', 'pass_field']


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