from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    phone = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    dob = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20, choices=[('user','User'),('counsellor','Counsellor'),('admin','Admin')], default='user')

    class Meta:
        db_table = 'user'


class Counsellor(models.Model):
    counsellor_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='counsellor_profile')
    name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    experience_years = models.IntegerField(default=0)
    availability_status = models.BooleanField(default=True)

    class Meta:
        db_table = 'counsellor'

    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    name = models.CharField(max_length=200)
    email = models.EmailField()

    class Meta:
        db_table = 'admin_profile'


class Appointment(models.Model):
    STATUS_CHOICES = [('booked','Booked'),('cancelled','Cancelled'),('completed','Completed')]
    MODE_CHOICES = [('online','Online'),('offline','Offline')]

    appointment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    counsellor = models.ForeignKey(Counsellor, on_delete=models.CASCADE, related_name='appointments')
    app_date = models.DateField()
    app_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='booked')
    booking_timestamp = models.DateTimeField(auto_now_add=True)
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='online')

    class Meta:
        db_table = 'appointment'

    def __str__(self):
        return f"Apt #{self.appointment_id} - {self.user.get_full_name()} with {self.counsellor.name}"


class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='session')
    session_notes = models.TextField(blank=True)
    duration = models.IntegerField(help_text='Duration in minutes', default=60)
    session_date = models.DateField()
    feedback = models.TextField(blank=True)
    rating = models.IntegerField(null=True, blank=True, choices=[(i,i) for i in range(1,6)])

    class Meta:
        db_table = 'session'
