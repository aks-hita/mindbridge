from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('counsellor/dashboard/', views.counsellor_dashboard, name='counsellor_dashboard'),
    path('counsellors/', views.counsellors_list, name='counsellors'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('appointment/<int:apt_id>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    path('appointment/<int:apt_id>/session/', views.session_detail, name='session_detail'),
    path('appointment/<int:apt_id>/complete/', views.complete_appointment, name='complete_appointment'),
]
