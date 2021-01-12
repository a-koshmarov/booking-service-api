from django.urls import path
from .views import BookingView, RoomView, MakeBookingView, LoginView, CreateUserView, DeleteBookingView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Booking Service API",
      default_version='v1',
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('booking/', BookingView.as_view(), name='bookings'),
    path('booking/room/<int:room>/', RoomView.as_view(), name='room'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', CreateUserView.as_view(), name='register'),
    path('booking/<int:pk>/', MakeBookingView.as_view(), name='create'),
    path('booking/<int:pk>/delete/', DeleteBookingView.as_view(), name='delete')
]
