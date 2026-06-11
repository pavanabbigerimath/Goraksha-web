from django.contrib import admin
from .models import Doctor, FirstAid, GovtScheme, AccidentReport, Review
from .forms import DoctorRegistrationForm
from django.contrib.auth.models import User

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    form = DoctorRegistrationForm
    list_display = ('name','qualification','specialty','district','taluk','pincode','phone','is_verified') 
    list_filter = ('district', 'is_verified') 
    list_editable = ('is_verified',)
    
    change_form_template = 'admin/doctor_change_form.html'
    

@admin.register(FirstAid)
class FirstAidAdmin(admin.ModelAdmin):
    list_display = ('disease_name', 'treatment_details_short', 'video_url', 'icon_class')
    
    def treatment_details_short(self, obj):
        return obj.treatment_details[:50] + "..." if len(obj.treatment_details) > 50 else obj.treatment_details
    
    treatment_details_short.short_description = 'ಚಿಕಿತ್ಸೆಯ ವಿವರ'

from .models import GovtScheme

@admin.register(GovtScheme)
class GovtSchemeAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')

admin.site.register(Review)

@admin.register(AccidentReport)
class AccidentReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'latitude', 'longitude', 'reported_at')
    list_filter = ('reported_at',)
    readonly_fields = ('reported_at',) 