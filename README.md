# Bus Reservation System

Backend API for a Bus Reservation Platform built with Django REST Framework.

## Features

### Authentication
- Custom User Model
- Phone Number Login
- OTP Authentication
- JWT Authentication using SimpleJWT

### User Roles
- Admin
- Transport Owner
- Passenger

### Transport Management
- Create and manage transport companies
- Create and manage buses
- Create and manage seats
- Create and manage trips

### Reservation System
- Seat reservation
- Gender-based seat restrictions
- Prevent duplicate reservations
- Reservation confirmation
- Reservation cancellation

### Search & Performance
- Trip search by origin and destination
- Redis caching for trip search results

## Tech Stack

- Python 3
- Django
- Django REST Framework
- PostgreSQL
- Redis
- Docker
- Docker Compose
- JWT Authentication

## Project Structure

```text
accounts/
transport/
reservations/
config/
docker-compose.yml
Dockerfile
requirements.txt
```

## Authentication Flow

```text
Phone Number
      │
      ▼
Request OTP
      │
      ▼
Verify OTP
      │
      ▼
Create/Get User
      │
      ▼
Generate JWT Tokens
```

## Reservation Flow

```text
Passenger
    │
    ▼
Select Trip
    │
    ▼
Select Seat
    │
    ▼
Validate Seat
    │
    ├── Seat Available
    ├── Gender Match
    └── Not Reserved
    │
    ▼
Create Reservation
```

## Business Rules

- A seat cannot be reserved twice.
- Only available seats can be reserved.
- Gender-specific seats are enforced.
- Passengers can only access their own reservations.

## Running with Docker

```bash
docker compose up --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```


## Author

Sheida — Django Backend Developer
