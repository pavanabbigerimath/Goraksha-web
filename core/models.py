from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User

class Doctor(models.Model):
    
    DISTRICTS = [
        ('Gadag', 'Gadag'),
        ('Dharwad', 'Dharwad'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200) 
    qualification = models.CharField(max_length=100) 
    specialty = models.CharField(max_length=100) 
    district = models.CharField(max_length=100, choices=DISTRICTS) 
    taluk = models.CharField(max_length=100) 
    village = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=6, verbose_name="Pincode", null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    phone = models.CharField(max_length=15) 
    image = models.ImageField(upload_to='doctors/') 
    certificate = models.FileField(upload_to='certificates/', verbose_name="Doctor Certificate", null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    from django.db.models import Avg

    def get_average_rating(self):
        return self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    def __str__(self):
        return f"{self.name} ({self.district})"
    
class FirstAid(models.Model):
    disease_name = models.CharField(max_length=200, verbose_name="ಕಾಯಿಲೆಯ ಹೆಸರು")
    treatment_details = models.TextField(verbose_name="ಪ್ರಥಮ ಚಿಕಿತ್ಸೆಯ ವಿವರಣೆ")
    video_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="YouTube ಲಿಂಕ್")
    icon_class = models.CharField(max_length=50, default="bi-heart-pulse")

    def __str__(self):
        return self.disease_name
    
class GovtScheme(models.Model):
    title = models.CharField(max_length=200, verbose_name="ಯೋಜನೆಯ ಹೆಸರು")
    description = models.TextField(verbose_name="ಯೋಜನೆಯ ವಿವರ")
    benefits = models.TextField(verbose_name="ಪ್ರಯೋಜನಗಳು")
    eligibility = models.TextField(verbose_name="ಅರ್ಹತೆಗಳು (Eligibility)")
    apply_link = models.URLField(blank=True, null=True, verbose_name="ಅರ್ಜಿ ಸಲ್ಲಿಸುವ ಲಿಂಕ್")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Review(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='reviews')
    farmer_name = models.CharField(max_length=100, default="Anonymous") # ರೈತನ ಹೆಸರು
    rating = models.IntegerField(default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class AccidentReport(models.Model):
    image = models.ImageField(upload_to='accidents/')
    latitude = models.FloatField()
    longitude = models.FloatField()
    reported_at = models.DateTimeField(auto_now_add=True)

class AlertLog(models.Model):
    accident = models.ForeignKey(AccidentReport, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    alerted_at = models.DateTimeField(auto_now_add=True)