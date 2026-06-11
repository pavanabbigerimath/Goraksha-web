from django.shortcuts import render, redirect, get_object_or_404
from .forms import DoctorRegistrationForm
from .models import Doctor, FirstAid, Review
from django.db.models import Q
from django.contrib import messages
from .models import GovtScheme
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth import login
from .forms import DoctorRegistrationForm, AdminProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.decorators import user_passes_test
from .forms import UserAdminManagementForm
from .models import AccidentReport,AlertLog
from math import radians, cos, sin, asin, sqrt
import random
from django.contrib.auth.hashers import make_password


def home(request):
    return render(request, 'index.html')

from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def register_doctor(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            doctor_profile = form.save(commit=False)
            doctor_profile.user = request.user
            doctor_profile.save()
            return redirect('home')
    else:
        form = DoctorRegistrationForm()
    return render(request, 'register.html', {'form': form})

def doctor_list(request):
    query = request.GET.get('search_text')

    if query:
        doctors = Doctor.objects.filter(
            Q(village__icontains=query) | 
            Q(taluk__icontains=query) |    
            Q(district__icontains=query) |  
            Q(name__icontains=query) |
            Q(specialty__icontains=query)
        ).distinct()
    else:
        doctors = Doctor.objects.filter(is_verified=True)
    return render(request, 'doctor_list.html', {'doctors': doctors, 'query': query})

def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'doctor_detail.html', {'doctor': doctor})

def first_aid_list(request):
    aids = FirstAid.objects.all()
    return render(request, 'first_aid.html', {'aids': aids})

def scheme_list(request):
    schemes = GovtScheme.objects.all().order_by('-created_at')
    return render(request, 'schemes.html', {'schemes': schemes})

def add_review(request, doctor_id):
    if request.method == "POST":
        doctor = Doctor.objects.get(id=doctor_id)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        farmer_name = request.POST.get('farmer_name', 'Anonymous')
        
        Review.objects.create(
            doctor=doctor,
            farmer_name=farmer_name,
            rating=rating,
            comment=comment
        )
        return redirect('doctor_detail', pk=doctor_id)
    
def about(request):
    return render(request, 'about.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "ಖಾತೆಯನ್ನು ಯಶಸ್ವಿಯಾಗಿ ಸೃಷ್ಟಿಸಲಾಗಿದೆ!")
            return redirect('register_doctor') 
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def profile_view(request):
    user = request.user
    doctor = None
    form = None

    if user.is_superuser:
        if request.method == 'POST':
            form = AdminProfileForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, "ಅಡ್ಮಿನ್ ಮಾಹಿತಿ ಅಪ್‌ಡೇಟ್ ಆಗಿದೆ!")
                return redirect('profile')
        else:
            form = AdminProfileForm(instance=user)
            
    else:
        # 2. If Doctore is logined
        try:
            doctor = Doctor.objects.get(user=user)
            if request.method == 'POST':
                form = DoctorRegistrationForm(request.POST, request.FILES, instance=doctor)
                if form.is_valid():
                    form.save()
                    messages.success(request, "ವೈದ್ಯರ ಪ್ರೊಫೈಲ್ ಅಪ್‌ಡೇಟ್ ಆಗಿದೆ!")
                    return redirect('profile')
            else:
                form = DoctorRegistrationForm(instance=doctor)
        except Doctor.DoesNotExist:
            form = None 

    return render(request, 'profile.html', {
        'user': user, 
        'doctor': doctor, 
        'form': form,
        'is_admin': user.is_superuser
    })

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')

    context = {
        'doctors': Doctor.objects.all().order_by('-id'),
        'schemes': GovtScheme.objects.all().order_by('-created_at'),
        'first_aids': FirstAid.objects.all(),
        'accidents': AccidentReport.objects.all(),
        'reviews': Review.objects.all().order_by('-id'),
        'users': User.objects.all(),
        'stats': {
            'docs': Doctor.objects.count(),
            'users': User.objects.count(),
            'schemes': GovtScheme.objects.count(),
            'accident': AccidentReport.objects.count(),
            'reviews': Review.objects.count(),
        }
    }
    return render(request, 'admin_dashboard.html', context)

MODEL_CONFIG = {
    'doctor': {
        'model': Doctor,
        'fields': ['name', 'qualification', 'specialty', 'district', 'taluk','pincode', 'latitude', 'longitude','phone', 'image', 'certificate', 'is_verified'],
        'title_add': 'Add Doctor',
        'title_edit': 'Edit Doctor',
        'msg': 'ವೈದ್ಯರ ವಿವರ'
    },
    'scheme': {
        'model': GovtScheme,
        'fields': ['title', 'description', 'benefits', 'eligibility', 'apply_link'],
        'title_add': 'ಹೊಸ ಯೋಜನೆ ಸೇರಿಸಿ (Add Scheme)',
        'title_edit': 'ಯೋಜನೆಯ ವಿವರ ಎಡಿಟ್ ಮಾಡಿ (Edit Scheme)',
        'msg': 'ಸರ್ಕಾರಿ ಯೋಜನೆಯ ವಿವರ'
    },
    'firstaid': {
        'model': FirstAid,
        'fields': ['disease_name', 'treatment_details', 'video_url', 'icon_class'],
        'title_add': 'ಹೊಸ ಪ್ರಥಮ ಚಿಕಿತ್ಸೆ ಸೇರಿಸಿ (Add First Aid)',
        'title_edit': 'ಪ್ರಥಮ ಚಿಕಿತ್ಸೆ ವಿವರ ಎಡಿಟ್ ಮಾಡಿ (Edit First Aid)',
        'msg': 'ಪ್ರಥಮ ಚಿಕಿತ್ಸೆಯ ವಿವರ'
    },
    'review': {
        'model': Review,
        'msg': 'ರೈತರ ರಿವ್ಯೂ'
    }
}

@login_required
@user_passes_test(lambda u: u.is_superuser)
def manage_core_system(request, model_name, action, pk=None):
    """
    ಒಂದೇ ಒಂದು ಡೈನಾಮಿಕ್ ವ್ಯೂ ಮೂಲಕ Doctor, Scheme, FirstAid ಮತ್ತು Review ಗಳ 
    ADD, EDIT ಮತ್ತು DELETE ಮೂರೂ ಆಪರೇಷನ್‌ಗಳನ್ನು ಹ್ಯಾಂಡಲ್ ಮಾಡುತ್ತದೆ.
    """
    from django.forms import modelform_factory  # ಡೈನಾಮಿಕ್ ಫಾರ್ಮ್ ಜನರೇಟರ್ ಇಂಪೋರ್ಟ್

    config = MODEL_CONFIG.get(model_name.lower())
    if not config:
        messages.error(request, "ಅಮಾನ್ಯವಾದ ಮಾಡೆಲ್ ಹೆಸರು!")
        return redirect('admin_dashboard')

    model_class = config['model']

    # 1. 🛑 DELETE ACTION HANDLING (ಡಿಲೀಟ್ ಆಪರೇಷನ್)
    if action == 'delete' and pk:
        item = get_object_or_404(model_class, pk=pk)
        item.delete()
        messages.success(request, f"{config['msg']}ಯನ್ನು ಯಶಸ್ವಿಯಾಗಿ ಡಿಲೀಟ್ ಮಾಡಲಾಗಿದೆ.")
        return redirect('admin_dashboard')

    # 2. 📝 ADD & EDIT ACTION HANDLING 
    if action not in ['add', 'edit']:
        return redirect('admin_dashboard')
        
    instance = get_object_or_404(model_class, pk=pk) if (action == 'edit' and pk) else None
    page_title = config['title_edit'] if instance else config['title_add']

    DynamicForm = modelform_factory(model_class, fields=config['fields'])

    if request.method == 'POST':
        form = DynamicForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, f"{config['msg']}ಯನ್ನು ಯಶಸ್ವಿಯಾಗಿ ಉಳಿಸಲಾಗಿದೆ!")
            return redirect('admin_dashboard')
    else:
        form = DynamicForm(instance=instance)

    # 🎨 ನಿಮ್ಮ ಹಳೆಯ ಯುಐ ಸ್ಟೈಲ್ ಹಾಳಾಗದಂತೆ ಬೂಟ್‌ಸ್ಟ್ರ್ಯಾಪ್ ಕ್ಲಾಸ್‌ಗಳನ್ನು ಡೈನಾಮಿಕ್ ಆಗಿ ಅಪ್ಲೈ ಮಾಡುವುದು
    for field_name, field in form.fields.items():
        if isinstance(field.widget, forms.CheckboxInput):
            field.widget.attrs.update({'class': 'form-check-input', 'role': 'switch'})
        elif isinstance(field.widget, forms.Textarea):
            field.widget.attrs.update({'class': 'form-control', 'rows': 4})
        else:
            field.widget.attrs.update({'class': 'form-control'})

    return render(request, 'edit_form.html', {
        'form': form, 
        'title': page_title, 
        'item': instance, 
        'model_name': model_name
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_account_manage_view(request, pk):
    """
    ಬಳಕೆದಾರರ ಪರ್ಮಿಷನ್ ಹಾಗೂ ಸ್ಟೇಟಸ್ ಅನ್ನು ಯೂಸರ್ ಸೈಡ್ ಫ್ರಂಟ್-ಎಂಡ್‌ನಲ್ಲೇ 
    ಬದಲಾಯಿಸಲು ಸಹಾಯ ಮಾಡುವ ವ್ಯೂ ಫಂಕ್ಷನ್.
    """
    target_user = get_object_or_404(User, pk=pk)
    if request.method == 'POST' and request.POST.get('action') == 'delete':
        if target_user == request.user:
            messages.error(request, "ನಿಮ್ಮ ಸ್ವಂತ ಅಡ್ಮಿನ್ ಖಾತೆಯನ್ನು ನೀವೇ ಡಿಲೀಟ್ ಮಾಡಲು ಸಾಧ್ಯವಿಲ್ಲ!")
            return redirect('user_account_manage', pk=pk)
            
        username = target_user.username
        target_user.delete() 
        messages.success(request, f"{username} ಅವರ ಖಾತೆಯನ್ನು ಯಶಸ್ವಿಯಾಗಿ ಡಿಲೀಟ್ ಮಾಡಲಾಗಿದೆ.")
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = UserAdminManagementForm(request.POST, instance=target_user)
        if form.is_valid():
            form.save()
            messages.success(request, f"{target_user.username} ಅವರ ವಿವರಗಳನ್ನು ಯಶಸ್ವಿಯಾಗಿ ಅಪ್ಡೇಟ್ ಮಾಡಲಾಗಿದೆ!")
            return redirect('admin_dashboard')
    else:
        form = UserAdminManagementForm(instance=target_user)
        
    return render(request, 'manage_user_account.html', {
        'form': form,
        'target_user': target_user
    })

def initiate_profile_password_reset(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        try:
            doctor = Doctor.objects.get(phone=phone) 
            
            otp = str(random.randint(100000, 999999))
            request.session['reset_otp'] = otp
            request.session['reset_user_id'] = doctor.user.id 
            
            print(f"OTP FOR {doctor.user.username}: {otp}")
            messages.success(request, "ನಿಮ್ಮ ಫೋನ್ ಸಂಖ್ಯೆಗೆ OTP ಕಳುಹಿಸಲಾಗಿದೆ.")
            return redirect('verify_profile_otp')
        except Doctor.DoesNotExist:
            messages.error(request, "ಈ ಫೋನ್ ಸಂಖ್ಯೆ ನೋಂದಣಿಯಾಗಿಲ್ಲ.")
    return render(request, 'password_reset_otp_request.html')

def verify_profile_otp(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        if user_otp == request.session.get('reset_otp'):
            return redirect('set_new_profile_password')
        else:
            messages.error(request, "ತಪ್ಪಾದ OTP! ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.")
    return render(request, 'password_reset_otp_verify.html')

def set_new_profile_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        user = User.objects.get(id=request.session.get('reset_user_id'))
        user.set_password(new_password)
        user.save()
        messages.success(request, "ಪಾಸ್‌ವರ್ಡ್ ಯಶಸ್ವಿಯಾಗಿ ಬದಲಾಯಿಸಲಾಗಿದೆ!")
        return redirect('profile')
    return render(request, 'set_new_password.html')


def admin_user_password_reset(request, pk):
    target_user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = SetPasswordForm(user=target_user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "ಪಾಸ್‌ವರ್ಡ್ ಯಶಸ್ವಿಯಾಗಿ ಬದಲಾಯಿಸಲಾಗಿದೆ!")
            return redirect('admin_dashboard') 
    else:
        form = SetPasswordForm(user=target_user)
        
        for field in form.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
    return render(request, 'admin_password_reset.html', {'form': form, 'target_user': target_user})


def haversine(lon1, lat1, lon2, lat2):
    try:
        lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        return 6371 * c
    except:
        return 9999 

def report_accident(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')

        if image and lat and lon:
            # 1. Report ಆಬ್ಜೆಕ್ಟ್ ಸೃಷ್ಟಿಸಿ
            report = AccidentReport.objects.create(
                image=image,
                latitude=float(lat),
                longitude=float(lon)
            )
            
            doctors = Doctor.objects.all()
            for doc in doctors:
                if doc.latitude and doc.longitude:
                    dist = haversine(lon, lat, doc.longitude, doc.latitude)
                    
                    if dist < 10:
                        AlertLog.objects.create(accident=report, doctor=doc)
                        print(f"Alerting Doctor {doc.name} at {doc.phone}")
            
            return redirect('thank_you')
        else:
            messages.error(request, "Error: Could not capture location or image.")
            
    return render(request, 'report_accident.html')
def thank_you(request):
    return render(request, 'thank_you.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_accident_list(request):
    accidents = AccidentReport.objects.all().order_by('-reported_at')
    return render(request, 'accident_report_list.html', {'accidents': accidents})