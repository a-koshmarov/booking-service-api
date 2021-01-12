# booking-service-api
Django REST API for room booking

### Live service hosted on heroku
[booking-service-api](https://booking-service-api.herokuapp.com/api/)

### Requirments
`pip install requirements.txt`

### Endpoints
- **GET /api/** - generated swagger annotations
- **GET /api/booking/** - list free bookings
  - *?all=true* - list all bookings (including already booked)
  - *?datetime_from=[iso timestamp]&datetime_to=[iso timestamp]* - list bookings in datetime range
- **POST /api/booking/** - create booking entry (Admin only)
- **GET /api/booking/room/{room id}/** - list free bookings in {room id}
  - *?all=true* - list all bookings
- **PUT /api/booking/{booking id}/** - book the room (Authentication: **token**)
- **DELETE /api/booking/{booking id}/** - delete booking (Admin only)
- **POST /api/register/** - register new user
  - *username*
  - *password*
- **POST /api/login/** - get auth token
  - *username*
  - *password*
