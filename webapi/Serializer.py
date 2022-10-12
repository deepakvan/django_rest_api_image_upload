from rest_framework import serializers
from .models import UserImages
class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserImages
        fields=('name','path')

class UserSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=100)
    password=serializers.CharField(max_length=100)
    class Meta:
        fields='__all__'



class RegisterSerializer(serializers.Serializer):
    name=serializers.CharField(max_length=50)
    username=serializers.CharField(max_length=50)
    password=serializers.CharField(max_length=50)
    class Meta:
        fields='__all__'
