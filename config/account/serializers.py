from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username','first_name','last_name','email','country','password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def create(self, validated_data):
        user = Account.objects.create_user(**validated_data)
        return user