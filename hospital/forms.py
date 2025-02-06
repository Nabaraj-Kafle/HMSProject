from django import forms
from django.contrib.auth.models import User
from . import models



#for admin signup
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }


#for doctor related form
class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class DoctorForm(forms.ModelForm):
    
    #edit paxi

    available_times = forms.MultipleChoiceField(
        choices=[
            ('06:00-10:00', '06:00 AM - 10:00 AM'),
            ('10:00-14:00', '10:00 AM - 02:00 PM'),
            ('14:00-18:00', '02:00 PM - 06:00 PM'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Available Time Slots"
    )

    #edit paxi

    class Meta:
        model=models.Doctor
        fields=['address','mobile','department','status','profile_pic']



#for teacher related form
class PatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class PatientForm(forms.ModelForm):
    assignedDoctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Name and Department", to_field_name="user_id")
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model=models.Patient
        fields=['address','mobile','status','symptoms','profile_pic','age','gender']
        
       

# if edit wala remove keep this

# class AppointmentForm(forms.ModelForm):
#     doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
#     patientId=forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True),empty_label="Patient Name and Symptoms", to_field_name="user_id")
#     class Meta:
#         model=models.Appointment
#         fields=['description','status']

# if edit wala remove keep this
from datetime import datetime, timedelta 

class AppointmentForm(forms.ModelForm):
    doctorId = forms.ModelChoiceField(
        queryset=models.Doctor.objects.all().filter(status=True),
        empty_label="Doctor Name and Department",
        to_field_name="user_id"
    )
    patientId = forms.ModelChoiceField(
        queryset=models.Patient.objects.all().filter(status=True),
        empty_label="Patient Name and Symptoms",
        to_field_name="user_id"
    )

    # This field will show the available times dynamically
    appointmentTime = forms.ChoiceField(choices=[])  # Initially, no choices

    class Meta:
        model = models.Appointment
        fields = ['description', 'status', 'doctorId', 'patientId', 'appointmentTime']

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        
        if self.instance and self.instance.doctorId:
            # Get the available time slots of the selected doctor
            available_times = self.instance.doctorId.available_times
            # Update the choices for the 'appointmentTime' field
            self.fields['appointmentTime'].choices = [(time, time) for time in available_times]


class PatientAppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']


#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

#edit 2  
class DoctorAvailabilityForm(forms.ModelForm):
    class Meta:
        model = models.DoctorAvailability
        fields = ['doctor', 'date', 'start_time', 'end_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("Start time must be before end time.")

        return cleaned_data
#edit 2 