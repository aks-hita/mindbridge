from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Appointment, Session


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)
    gender = forms.ChoiceField(choices=[('','Select'),('M','Male'),('F','Female'),('O','Other')], required=False)
    dob = forms.DateField(required=False, widget=forms.DateInput(attrs={'type':'date'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'rows':2}), required=False)

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','phone','gender','dob','address','password1','password2']


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['counsellor','app_date','app_time','mode']
        widgets = {
            'app_date': forms.DateInput(attrs={'type':'date'}),
            'app_time': forms.TimeInput(attrs={'type':'time'}),
        }


class SessionFeedbackForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['feedback','rating']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows':3, 'placeholder':'Share your experience...'}),
        }


class SessionNotesForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['session_notes','duration']
        widgets = {
            'session_notes': forms.Textarea(attrs={'rows':4}),
        }
