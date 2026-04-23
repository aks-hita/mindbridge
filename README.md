# 🌿 MindBridge — Mental Health Counselling Platform

A full-stack Django web application for booking mental health counselling appointments.

## ER Schema (from your diagram)
- **User** (User-ID PK, Name, Email, Phone, Gender, DOB, Address, Reg-date)
- **Counsellor** (Counsellor-ID PK, Name, Specialization, Email, Phone, Experience-years, Availability-status)
- **Appointment** (Appointment-ID PK, User-ID FK, Counsellor-ID FK, Date, Time, Status, Booking-Timestamp, Mode)
- **Session** (Session-ID PK, Appointment-ID FK, Notes, Duration, Session-date, Feedback, Rating)
- **Admin** (Admin-ID PK, Name, Email)

## Relationships implemented
- User → Appointments: 1:Many
- Counsellor → Appointments: 1:Many  
- Appointment → Session: 1:0..1

## Setup Instructions

```bash
# Install dependencies
pip install django

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Seed sample data (optional, already done)
python manage.py shell < seed.py

# Start server
python manage.py runserver
```

## Test Accounts (password: password123)
| Username    | Role       |
|-------------|------------|
| arjun       | Patient    |
| dr_priya    | Counsellor (Anxiety & Depression) |
| dr_rahul    | Counsellor (Trauma & PTSD) |
| dr_ananya   | Counsellor (Relationship Therapy) |

## Features
- ✅ User registration & login
- ✅ Browse available counsellors
- ✅ Book appointments (online/offline)
- ✅ Cancel appointments
- ✅ Session history with notes & ratings
- ✅ Counsellor dashboard (see all bookings, mark complete)
- ✅ Session feedback & star ratings
- ✅ Raw SQL queries via Django connection cursor
- ✅ SQLite database (LiveSQL compatible schema)
