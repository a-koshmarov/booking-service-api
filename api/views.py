from django.utils import dateparse
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import Booking
from .serializers import BookingSerializer, UserSerializer

class BookingView(APIView):

    display_all_param = openapi.Parameter('all', openapi.IN_QUERY, description="Display all bookings", type=openapi.TYPE_BOOLEAN)
    datetime_from_param = openapi.Parameter('datetime_from', openapi.IN_QUERY, description="Display bookings starting from datetime (accepts iso datetime)", type=openapi.TYPE_STRING)
    datetime_to_param = openapi.Parameter('datetime_to', openapi.IN_QUERY, description="Display bookings ending by datetime (accepts iso datetime)", type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[display_all_param, datetime_from_param, datetime_to_param])
    def get(self, request):
        display_all = request.GET.get('all', '')
        datetime_from = request.GET.get('datetime_from', '')
        datetime_to = request.GET.get('datetime_to', '')
        

        if display_all == 'true':
            bookings = Booking.objects.all().filter()
        else:
            bookings = Booking.objects.all().filter(booked=False)
        
        if datetime_from and datetime_to:
            datetime_from = dateparse.parse_datetime(datetime_from)
            if datetime_from == None:
                return Response({"error": "Invalid iso format (datetime_from)"}, status=status.HTTP_400_BAD_REQUEST)        

            datetime_to = dateparse.parse_datetime(datetime_to)
            if datetime_to == None:
                return Response({"error": "Invalid iso format (datetime_to)"}, status=status.HTTP_400_BAD_REQUEST) 

            if datetime_from >= datetime_to:
                return Response({"error": "Invalid time interval"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                bookings = bookings.filter(start_time__range = (datetime_from, datetime_to))

        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

class RoomView(APIView):
    
    display_all_param = openapi.Parameter('all', openapi.IN_QUERY, description="Display all bookings", type=openapi.TYPE_BOOLEAN)
    @swagger_auto_schema(manual_parameters=[display_all_param])
    def get(self, request, room):
        display_all = request.GET.get('all', '')

        if display_all == 'true':
            bookings = Booking.objects.all().filter(workplace=room)
            serializer = BookingSerializer(bookings, many=True)
            return Response(serializer.data)
        bookings = Booking.objects.all().filter(workplace=room, booked=False)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

class MakeBookingView(APIView):

    def get_object(self, pk):
        try:
            return Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return Response ({"error": "Booking does not exist"}, status=status.HTTP_404_NOT_FOUND)

    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        booking = self.get_object(pk)
        data = {"user": request.user.id, "booked": True}
        serializer = BookingSerializer(instance=booking, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response ({"success": "{} has been booked from {} to {}".format(
                booking.workplace,
                booking.start_time.strftime("%b %d %Y %H:%M"), 
                booking.end_time.strftime("%b %d %Y %H:%M"))}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.get(username=username)
        print(username, password)
        print(user)

        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        print("auth: ", user)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                        status=status.HTTP_404_NOT_FOUND)

        token, _ = Token.objects.get_or_crerate(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
