from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import connection
from datetime import date
from .models import User, Counsellor, Appointment, Session
from .forms import UserRegisterForm, AppointmentForm, SessionFeedbackForm, SessionNotesForm


def home(request):
    counsellors = Counsellor.objects.filter(availability_status=True)[:6]
    return render(request, 'home.html', {'counsellors': counsellors})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created! Welcome to MindBridge.')
            return redirect('dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    user = request.user
    if hasattr(user, 'counsellor_profile'):
        return redirect('counsellor_dashboard')
    
    appointments = Appointment.objects.filter(user=user).select_related('counsellor', 'session').order_by('-app_date', '-app_time')
    upcoming = appointments.filter(status='booked', app_date__gte=date.today())
    past = appointments.filter(status='completed')
    cancelled = appointments.filter(status='cancelled')

    # Raw SQL for stats
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) FROM appointment WHERE user_id = %s AND status = 'completed'
        """, [user.id])
        completed_count = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COALESCE(SUM(s.duration), 0) FROM session s
            JOIN appointment a ON s.appointment_id = a.appointment_id
            WHERE a.user_id = %s
        """, [user.id])
        total_minutes = cursor.fetchone()[0]

    context = {
        'appointments': appointments,
        'upcoming': upcoming,
        'past': past,
        'cancelled': cancelled,
        'completed_count': completed_count,
        'total_hours': round(total_minutes / 60, 1),
    }
    return render(request, 'dashboard.html', context)


@login_required
def counsellor_dashboard(request):
    user = request.user
    if not hasattr(user, 'counsellor_profile'):
        return redirect('dashboard')
    counsellor = user.counsellor_profile

    appointments = Appointment.objects.filter(counsellor=counsellor).select_related('user', 'session').order_by('-app_date', '-app_time')
    upcoming = appointments.filter(status='booked', app_date__gte=date.today())
    today_apts = appointments.filter(status='booked', app_date=date.today())

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) FROM appointment WHERE counsellor_id = %s AND status = 'completed'
        """, [counsellor.counsellor_id])
        completed = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COALESCE(AVG(s.rating), 0) FROM session s
            JOIN appointment a ON s.appointment_id = a.appointment_id
            WHERE a.counsellor_id = %s AND s.rating IS NOT NULL
        """, [counsellor.counsellor_id])
        avg_rating = round(cursor.fetchone()[0], 1)

    context = {
        'counsellor': counsellor,
        'appointments': appointments,
        'upcoming': upcoming,
        'today_apts': today_apts,
        'completed': completed,
        'avg_rating': avg_rating,
    }
    return render(request, 'counsellor_dashboard.html', context)


@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            apt = form.save(commit=False)
            apt.user = request.user
            apt.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('dashboard')
    else:
        form = AppointmentForm()
    counsellors = Counsellor.objects.filter(availability_status=True)
    return render(request, 'book_appointment.html', {'form': form, 'counsellors': counsellors})


@login_required
def cancel_appointment(request, apt_id):
    apt = get_object_or_404(Appointment, appointment_id=apt_id, user=request.user)
    if apt.status == 'booked':
        apt.status = 'cancelled'
        apt.save()
        messages.success(request, 'Appointment cancelled.')
    return redirect('dashboard')


@login_required
def session_detail(request, apt_id):
    apt = get_object_or_404(Appointment, appointment_id=apt_id)
    session = getattr(apt, 'session', None)
    feedback_form = None

    if request.user == apt.user and session:
        if request.method == 'POST':
            feedback_form = SessionFeedbackForm(request.POST, instance=session)
            if feedback_form.is_valid():
                feedback_form.save()
                messages.success(request, 'Feedback submitted!')
                return redirect('dashboard')
        else:
            feedback_form = SessionFeedbackForm(instance=session)

    return render(request, 'session_detail.html', {'apt': apt, 'session': session, 'feedback_form': feedback_form})


@login_required
def complete_appointment(request, apt_id):
    if not hasattr(request.user, 'counsellor_profile'):
        return redirect('dashboard')
    counsellor = request.user.counsellor_profile
    apt = get_object_or_404(Appointment, appointment_id=apt_id, counsellor=counsellor)

    if request.method == 'POST':
        notes = request.POST.get('session_notes', '')
        duration = request.POST.get('duration', 60)
        Session.objects.create(
            appointment=apt,
            session_notes=notes,
            duration=duration,
            session_date=date.today(),
        )
        apt.status = 'completed'
        apt.save()
        messages.success(request, 'Session marked as complete.')
        return redirect('counsellor_dashboard')

    return render(request, 'complete_session.html', {'apt': apt})


def counsellors_list(request):
    counsellors = Counsellor.objects.filter(availability_status=True)
    return render(request, 'counsellors.html', {'counsellors': counsellors})
