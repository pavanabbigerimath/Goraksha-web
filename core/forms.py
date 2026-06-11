from django import forms
from .models import Doctor
from django.contrib.auth.models import User

class DoctorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'qualification', 'specialty', 'district', 'taluk','village','pincode', 'latitude', 'longitude', 'phone', 'image', 'certificate']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'specialty': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.Select(attrs={'class': 'form-control'}),
            'taluk': forms.TextInput(attrs={'class': 'form-control'}),
            'village': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'certificate': forms.FileInput(attrs={'class': 'form-control'}),
        }

class AdminProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(AdminProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].help_text = ""

class UserAdminManagementForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=15, 
        required=False, 
        label="Phone Number",
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )
    class Meta:
        model = User
        fields = ['username', 'is_active', 'is_staff', 'is_superuser']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if hasattr(self.instance, 'doctor'):
                self.fields['phone_number'].initial = self.instance.doctor.phone
        # ಬೂಟ್‌ಸ್ಟ್ರ್ಯಾಪ್ ಡಿಸೈನ್ ಅಪ್ಲೈ ಮಾಡುವುದು
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'readonly': 'readonly'})
        if 'phone_number' in self.fields:
            self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'readonly': 'readonly'})
        self.fields['is_active'].widget.attrs.update({'class': 'form-check-input', 'role': 'switch'})
        self.fields['is_staff'].widget.attrs.update({'class': 'form-check-input', 'role': 'switch'})
        self.fields['is_superuser'].widget.attrs.update({'class': 'form-check-input', 'role': 'switch'})