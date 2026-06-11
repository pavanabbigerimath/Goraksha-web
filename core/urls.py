from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register_doctor, name='register_doctor'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctor/<int:pk>/', views.doctor_detail, name='doctor_detail'), 
    path('first-aid/', views.first_aid_list, name='first_aid'),
    path('schemes/', views.scheme_list, name='schemes'),
    path('doctor/<int:doctor_id>/add_review/', views.add_review, name='add_review'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile_view, name='profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage/<str:model_name>/<str:action>/', views.manage_core_system, name='manage_core_no_pk'),
    path('manage/<str:model_name>/<str:action>/<int:pk>/', views.manage_core_system, name='manage_core_with_pk'),
    path('admin_dashboard/user/manage/<int:pk>/', views.user_account_manage_view, name='user_account_manage'),
    path('profile/reset-password/request/', views.initiate_profile_password_reset, name='initiate_profile_password_reset'),
    path('profile/reset-password/verify/', views.verify_profile_otp, name='verify_profile_otp'),
    path('profile/reset-password/set/', views.set_new_profile_password, name='set_new_profile_password'),
    path('manage/user/<int:pk>/reset-password/', views.admin_user_password_reset, name='admin_password_reset'),
    path('report-accident/', views.report_accident, name='report_accident'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('admin_dashboard/accidents/', views.admin_accident_list, name='admin_accident_list'),
    ]