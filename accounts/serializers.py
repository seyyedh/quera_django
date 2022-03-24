from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(max_length=50)
    # password = serializers.CharField(max_length=50)
    # first_name = serializers.CharField(max_length=50)
    # last_name = serializers.CharField(max_length=50)
    # email = serializers.EmailField()


    class Meta:
        model = User
        fields = ('username','password','phone','address','gender','age','description','first_name','last_name','email')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
