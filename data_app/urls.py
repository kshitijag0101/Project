from django.urls import path

from . import views
from . import api_views
from . import email_script
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import obtain_auth_token



urlpatterns = [
    path('', views.inputSelectedCompany, name='home'),

    # list of data Apis
    path('indian_company_list/', views.IndianCompanyListAPIView.as_view(), name='indian-list'),
    path('llp_company_list/', views.LLPCompanyListAPIView.as_view(), name='llp-list'),
    path('fcin_company_list/', views.FCINCompanyListAPIView.as_view(), name='fcin-list'),
    path('api/token/', views.CustomAuthToken.as_view(), name='api_token_auth'),

    # update of data Apis
    path('update_indian_data/', views.updateIndianCompanyData, name='update_indian_data'),
    path('update_llp_data/', views.updateLLPCompanyData, name='update_llp_data'),
    path('update_fcin_data/', views.updateFCINCompanyData, name='update_fcin_data'),

    path('status_data/', views.statusCompanyView, name='status_data'),
    path('dashboard_data/', views.dashboardCompany, name='dashboard_data'),

    path('file_status_data/', views.filesStatusView, name='file_status_data'),


    path('import/', views.import_excel, name='import_excel'),
    path('success/', views.success_view, name='success'),
    path('login/', views.login_view, name='login'),
    path('otp_verification/', views.otp_verification, name='otp_verification'),
    path('logout/', views.custom_logout, name='logout'),

    path('update_mail/', email_script.updateEmailData),



    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name = 'password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name = 'password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name = 'password_reset_complete'),




]