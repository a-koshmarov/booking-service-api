from rest_framework import serializers
from django.utils import dateparse
from .models import Room, Booking, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

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
    
