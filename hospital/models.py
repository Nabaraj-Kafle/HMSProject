from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



departments=[
    ('Cardiologist','Cardiologist'),
    ('Dermatologists', 'Dermatologists'),
    ('Emergency Medicine Specialists', 'Emergency Medicine Specialists'),
    ('Allergists/Immunologists', 'Allergists/Immunologists'),
    ('Anesthesiologists', 'Anesthesiologists'),
    ('Colon and Rectal Surgeons', 'Colon and Rectal Surgeons'),
    ('Endocrinologists', 'Endocrinologists'),
    ('Gastroenterologists', 'Gastroenterologists'),
    ('Hematologists', 'Hematologists'),
    ('Infectious Disease Specialists', 'Infectious Disease Specialists'),
    ('Nephrologists', 'Nephrologists'),
    ('Neurologists', 'Neurologists'),
    ('Obstetricians/Gynecologists', 'Obstetricians/Gynecologists'),
    ('Oncologists', 'Oncologists'),
    ('Ophthalmologists', 'Ophthalmologists'),
    ('Orthopedic Surgeons', 'Orthopedic Surgeons'),
    ('Otolaryngologists', 'Otolaryngologists'),
    ('Pathologists', 'Pathologists'),
    ('Pediatricians', 'Pediatricians'),
    ('Psychiatrists', 'Psychiatrists'),
    ('Pulmonologists', 'Pulmonologists'),
    ('Radiologists', 'Radiologists'),
    ('Rheumatologists', 'Rheumatologists'),
    ('Urologists', 'Urologists')
]

class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
    status=models.BooleanField(default=False)
    #edit paxi
    available_times = models.JSONField(default=list)  # Store available time slots as a list of times
    #edit paxi

    #added after edit 2
    status = models.BooleanField(default=False)
    #added after edit 2


    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)

# edit paxi


class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)  # Link to Doctor
    start_time = models.TimeField()  # Start time of availability
    end_time = models.TimeField()    # End time of availability
    #added after edit 2
    date = models.DateField(default=timezone.now)  # Use the current date as default    #added after edit 2
    time_slot = models.CharField(max_length=100, default='default_time')  #edit 4


    #added after edit 2 (placed instead of xx3)
    class Meta:
        unique_together = ('doctor', 'date', 'start_time')  # Ensure that each slot is unique

    def __str__(self):
        return f"{self.doctor.get_name}: {self.start_time} - {self.end_time} on {self.date}"

    #added after edit 2 (placed instead of xx3)
    
    #xx3
    # def __str__(self):
    #     return f"{self.doctor.get_name}: {self.start_time} - {self.end_time}"
    #xx3

# edit paxi 

class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/PatientProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    # age = models.IntegerField()  # Make sure this field exists
    # age = models.CharField(max_length=10, null=False, default=0)
    gender = models.CharField(max_length=10, null=False, default='Male')    
    mobile = models.CharField(max_length=20,null=False)
    symptoms = models.CharField(max_length=100,null=False)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    admitDate=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)

    def get_recommended_doctors(self, limit=5):
        """Get recommended doctors for this patient based on symptoms"""
        symptoms = [s.strip().lower() for s in self.symptoms.split(',')]
        
        # Get relevant department mappings
        department_scores = defaultdict(float)
        
        for symptom in symptoms:
            mappings = SymptomDepartmentMapping.objects.filter(
                symptom__icontains=symptom
            )
            
            for mapping in mappings:
                department_scores[mapping.department.department] += mapping.weight
        
        # Get doctors from the most relevant departments
        recommended_doctors = []
        
        for department, score in sorted(
            department_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        ):
            doctors = Doctor.objects.filter(
                department=department,
                status=True  # Only active doctors
            ).order_by('?')[:limit]  # Random selection within department
            
            recommended_doctors.extend(doctors)
            
            if len(recommended_doctors) >= limit:
                break
        
        return recommended_doctors[:limit]



    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.symptoms+")"
 
class Appointment(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    doctorId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40,null=True)
    doctorName=models.CharField(max_length=40,null=True)
    appointmentDate=models.DateField(auto_now=True)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)



class PatientDischargeDetails(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40)
    assignedDoctorName=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    symptoms = models.CharField(max_length=100,null=True)

    admitDate=models.DateField(null=False)
    releaseDate=models.DateField(null=False)
    daySpent=models.PositiveIntegerField(null=False)

    roomCharge=models.PositiveIntegerField(null=False)
    medicineCost=models.PositiveIntegerField(null=False)
    doctorFee=models.PositiveIntegerField(null=False)
    OtherCharge=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)
    id = models.BigAutoField(primary_key=True) #edit 4

# class DoctorSpecialization(models.Model):
#     department = models.CharField(max_length=50, choices=departments)
#     keywords = models.TextField(help_text="Comma-separated keywords related to this specialization")
    
#     def __str__(self):
#         return self.department

# class SymptomDepartmentMapping(models.Model):
#     symptom = models.CharField(max_length=100)
#     department = models.ForeignKey(DoctorSpecialization, on_delete=models.CASCADE)
#     weight = models.FloatField(default=1.0)
    
#     def __str__(self):
#         return f"{self.symptom} -> {self.department}"










