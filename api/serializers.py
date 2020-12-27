from rest_framework import serializers
from django.utils import dateparse
from .models import Room, Booking
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( "id", "username", "password", )
    
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"

    def to_representation(self, obj):
        ret = super(BookingSerializer, self).to_representation(obj)
        # print(vars(u))
        if ret['user'] == None:
            ret.pop('user')
        else:
            ret['user'] = obj.user.username

        return ret 
    
