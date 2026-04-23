from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Counsellor, Admin, Appointment, Session

admin.site.register(User, UserAdmin)
admin.site.register(Counsellor)
admin.site.register(Admin)
admin.site.register(Appointment)
admin.site.register(Session)
