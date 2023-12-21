import os

from rest_framework import generics
from .models import IndianCompany, LLPCompany, FCINCompany, OTP, fileModel, BulkFileModels
from .serializer import IndianCompanySerializer, LLPCompanySerializer, FCINCompanySerializer
from django.core.files.storage import default_storage
import io
from django.db.models import Count, Q
from .forms import importFile, selectCompany
import pandas as pd
from django.contrib.auth import authenticate, login
from .forms import LoginForm, DashboardFile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import datetime, timedelta
import smtplib
import ssl
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import boto3
from botocore.exceptions import NoCredentialsError

def upload_to_s3(local_file_path, s3_file_name):
    bucket_name = "djangobulkinsertfile"
    s3 = boto3.client('s3', aws_access_key_id="AKIA5MQSJ25EJNTBVVUL", aws_secret_access_key='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',
                      endpoint_url="https://djangobulkinsertfile.s3.ap-south-1.amazonaws.com")
    try:
        s3.upload_file(local_file_path, bucket_name, s3_file_name)
        print(f"File uploaded successfully to {bucket_name}/{s3_file_name}")
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")

def custom_logout(request):
    logout(request)
    return redirect(reverse('login'))


class IndianCompanyListAPIView(generics.ListAPIView):
    queryset = IndianCompany.objects.all()
    serializer_class = IndianCompanySerializer

    def get_queryset(self):
        # Get the start_date and end_date from request parameters
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        # Validate and parse the date parameters (you may need to adjust this based on your date format)
        try:
            start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else None
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None
        except ValueError:
            # Handle invalid date format
            return IndianCompany.objects.none()

        # Filter the queryset based on the date range
        queryset = IndianCompany.objects.all()
        if start_date and end_date:
            queryset = queryset.filter(date_of_registration__range=(start_date, end_date))
        elif start_date:
            queryset = queryset.filter(date_of_registration__gte=start_date)
        elif end_date:
            queryset = queryset.filter(date_of_registration__lte=end_date)

        return queryset

class LLPCompanyListAPIView(generics.ListAPIView):
    queryset = LLPCompany.objects.all()
    serializer_class = LLPCompanySerializer

    def get_queryset(self):
        # Get the start_date and end_date from request parameters
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        # Validate and parse the date parameters (you may need to adjust this based on your date format)
        try:
            start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else None
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None
        except ValueError:
            # Handle invalid date format
            return LLPCompany.objects.none()

        # Filter the queryset based on the date range
        queryset = LLPCompany.objects.all()
        if start_date and end_date:
            queryset = queryset.filter(founded__range=(start_date, end_date))
        elif start_date:
            queryset = queryset.filter(founded__gte=start_date)
        elif end_date:
            queryset = queryset.filter(founded__lte=end_date)

        return queryset

class FCINCompanyListAPIView(generics.ListAPIView):
    queryset = FCINCompany.objects.all()
    serializer_class = FCINCompanySerializer

    def get_queryset(self):
        # Get the start_date and end_date from request parameters
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        # Validate and parse the date parameters (you may need to adjust this based on your date format)
        try:
            start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date() if start_date else None
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date() if end_date else None
        except ValueError:
            # Handle invalid date format
            return FCINCompany.objects.none()

        # Filter the queryset based on the date range
        queryset = FCINCompany.objects.all()
        if start_date and end_date:
            queryset = queryset.filter(date__range=(start_date, end_date))
        elif start_date:
            queryset = queryset.filter(date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(date__lte=end_date)

        return queryset

@login_required(login_url='login')
def import_excel(request):
    if request.method == 'POST':
        form = importFile(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            category = form.cleaned_data['category']
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            print(excel_file)
            excel_buffer = io.BytesIO(excel_file.read())
            print(excel_buffer)
            df = pd.read_excel(excel_buffer)
            df = df.dropna(axis=1, how='all')
            df = df.fillna("")
            default_url = "https://djangobulkinsertfile.s3.ap-south-1.amazonaws.com/djangobulkinsertfile/"
            if len(df) > 0:
                df.rename(columns=lambda x: x.strip(), inplace=True)
                # print(df)
                if category == "Indian":
                    print("yes")
                    indian_df = df.copy()
                    if len(indian_df) > 0:
                        columns_required = ['CIN', 'Company Name', 'Date of Registration', 'Month Name', 'State',
                                            'ROC', 'Company', 'Category', 'Class', 'Company Type', 'Authorized',
                                            'Paid up', 'Activity', 'Activity Description', 'Description',
                                            'Registered Office Address']
                        missing_columns = set(columns_required) - set(indian_df.columns)
                        if missing_columns:
                            return render(request, 'import_excel.html', {'form': form, 'missing_columns': missing_columns})
                        else:
                            try:
                                df['CIN'] = df['CIN'].str.strip()
                                rename_data = {'CIN': "CIN", 'Company Name': "company_name",
                                               'Date of Registration': "date_of_registration",
                                               'Month Name': "month_name", 'State': "state", 'ROC': "roc", 'Company': "company",
                                               'Category': "category", 'Class': "Class", 'Company Type': "company_type",
                                               'Authorized': "authorized_capital", 'Paid up': "paid_up_capital",
                                               'Activity': "activity",
                                               'Activity Description': "activity_description", 'Description': "description",
                                               'Registered Office Address': "registered_office_address"}
                                indian_df.rename(columns=rename_data, inplace=True)
                                indian_df['date_of_registration'] = pd.to_datetime(indian_df['date_of_registration'],  dayfirst=True).dt.date
                                indian_df['CIN'] = indian_df['CIN'].str.strip()
                                file_name = "indian_" + str(datetime.now().strftime("%Y%m%d%H%M%S"))+".xlsx"
                                indian_df.to_excel(file_name)
                                upload_to_s3(file_name, file_name)
                                BulkFileModels.objects.create(file_name=file_name, file_url=default_url+file_name, year=year, month=month)
                                try:
                                    os.remove(file_name)
                                except:
                                    print("rr")
                                # fileModel.objects.create(file_name=file_name, data=indian_df.to_dict("records"))
                                # for index, row in indian_df.iterrows():
                                #     data_point = {
                                #         'CIN': str(row['CIN']),
                                #         'company_name': str(row['company_name']),
                                #         "date_of_registration" :row['date_of_registration'],
                                #         "month_name": str(row['month_name']),
                                #         "state": str(row['state']),
                                #         "roc": str(row['roc']),
                                #         "company": str(row['company']),
                                #         "category": str(row['category']),
                                #         "company_type": str(row['company_type']),
                                #         "authorized_capital": float(row['authorized_capital']) if row['authorized_capital'] != "" else None,
                                #         "paid_up_capital": float(row['paid_up_capital']) if row['paid_up_capital'] != "" else None,
                                #         "activity": str(row['activity']),
                                #         "activity_description": str(row['activity_description']),
                                #         "description": str(row['description']),
                                #         "registered_office_address": str(row['registered_office_address']),
                                #         'month':str(month),
                                #         'year': year,
                                #         "email": None,
                                #         "file_name": file_name
                                #     }
                                #     IndianCompany.objects.update_or_create(CIN=data_point['CIN'], defaults=data_point)
                            except Exception as e:
                                print("error", e)

                    else:
                        return render(request, 'import_excel.html', {'form': form, 'missing_columns': "No Data"})

                elif category == "LLP":
                    llp_df = df.copy()
                    if len(llp_df) > 0:
                        columns_required = ['LLPIN', 'LLP Name', 'Founded', 'Roc Location', 'Status',
                                            'Industrial Activity', 'Activity Description', 'Description',
                                            'Obligation Of Contribution', 'Number Of Partners',
                                            'Number Of Designated Partners', 'State', 'District', 'Address']
                        missing_columns = set(columns_required) - set(df.columns)
                        if missing_columns:
                            return render(request, 'import_excel.html', {'form': form, 'missing_columns': missing_columns})
                        else:
                            rename_data = {'LLPIN': "LLPIN", 'LLP Name': "llp_name", 'Founded': "founded",
                                           'Roc Location': "roc_location",
                                           'Status': "status",
                                           'Industrial Activity': "industrial_activity",
                                           'Activity Description': "activity_description", 'Description': "description",
                                           'Obligation Of Contribution': "obligation_of_contribution",
                                           'Number Of Partners': "number_of_partners",
                                           'Number Of Designated Partners': "number_of_designated_partners", 'State': "state",
                                           'District': "district", 'Address': "address"}
                            llp_df.rename(columns=rename_data, inplace=True)
                            llp_df['founded'] = pd.to_datetime(llp_df['founded'],  dayfirst=True).dt.date
                            llp_df['LLPIN'] = llp_df['LLPIN'].str.strip()
                            file_name = "llp_" + str(datetime.now().strftime("%Y%m%d%H%M%S")) + ".xlsx"
                            llp_df.to_excel(file_name)
                            upload_to_s3(file_name, file_name)
                            BulkFileModels.objects.create(file_name=file_name, file_url=default_url + file_name,
                                                          year=year, month=month)
                            try:
                                os.remove(file_name)
                            except:
                                print("rr")
                            # for index, row in llp_df.iterrows():
                            #     data_point = {
                            #         'LLPIN': str(row['LLPIN']),
                            #         'llp_name': str(row['llp_name']),
                            #         'founded': row['founded'],
                            #         'roc_location': str(row['roc_location']),
                            #         'status': str(row['status']),
                            #         'industrial_activity': str(row['industrial_activity']),
                            #         'activity_description': str(row['activity_description']),
                            #         'description': str(row['description']),
                            #         'obligation_of_contribution': float(row['obligation_of_contribution']) if row['obligation_of_contribution'] != "" else None,
                            #         'number_of_partners': row['number_of_partners'],
                            #         'number_of_designated_partners': row['number_of_designated_partners'],
                            #         'state': str(row['state']),
                            #         'district': str(row['district']),
                            #         'address': str(row['address']),
                            #         'month': str(month),
                            #         'year': year,
                            #         "email": None,
                            #         "file_name": file_name
                            #     }
                            #     LLPCompany.objects.update_or_create(LLPIN=data_point['LLPIN'], defaults=data_point)
                    else:
                        return render(request, 'import_excel.html', {'form': form, 'missing_columns': "No Data"})

                elif category == "Foreign":
                    fcin_df = df.copy()
                    columns_required = ['FCIN', 'Company Name', 'Date', 'Status', 'Activity',
                                        'Activity Description', 'Description', 'Office Type', 'Address',
                                        'State']

                    missing_columns = set(columns_required) - set(fcin_df.columns)

                    if missing_columns:
                        return render(request, 'import_excel.html', {'form': form,  'missing_columns': missing_columns})
                    else:
                        rename_data = {'FCIN': "FCIN", 'Company Name': "company_name", 'Date': "date", 'Status': "status",
                                       'Activity': "activity",
                                       'Activity Description': "activity_description", 'Description': "description",
                                       'Office Type': "office_type",
                                       'Address': "address",
                                       'State': "state", }
                        fcin_df.rename(columns=rename_data, inplace=True)
                        fcin_df['date'] = pd.to_datetime(fcin_df['date'], dayfirst=True).dt.date
                        fcin_df['FCIN'] = fcin_df['FCIN'].str.strip()
                        file_name = "fcin_" + str(datetime.now().strftime("%Y%m%d%H%M%S")) + ".xlsx"
                        fcin_df.to_excel(file_name)
                        upload_to_s3(file_name, file_name)
                        BulkFileModels.objects.create(file_name=file_name, file_url=default_url + file_name,
                                                      year=year, month=month)
                        try:
                            os.remove(file_name)
                        except:
                            print("rr")
                        # for index, row in fcin_df.iterrows():
                        #     print(row.office_type)
                        #     data_point = {
                        #         'FCIN': str(row['FCIN']),
                        #         'company_name': str(row['company_name']),
                        #         'date': row['date'],
                        #         'status': str(row['status']),
                        #         'activity': str(row['activity']),
                        #         'activity_description': str(row['activity_description']),
                        #         'description': str(row['description']),
                        #         'office_type': row['office_type'],
                        #         'address': str(row['address']),
                        #         'state': str(row['state']),
                        #         'month': str(month),
                        #         'year': year,
                        #         "email": None,
                        #         "file_name": file_name
                        #     }
                        #     FCINCompany.objects.update_or_create(FCIN=data_point['FCIN'], defaults=data_point)
                return redirect('success')  # Redirect to a success page
            else:
                return render(request, 'import_excel.html', {'form': form, 'missing_columns': "No Data"})
    else:
        form = importFile()
    return render(request, 'import_excel.html', {'form': form})

@login_required(login_url='login')
def success_view(request):
    return render(request, 'data_app/success.html')

def send_otp_email(email, otp):
    # Email configuration
    sender_email = "admin@mapletree-india.in"
    sender_password = "nzvq kyoc stat gpmx"
    subject = "Your OTP Code"

    # Create the message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = subject

    # Add the OTP to the email body
    body = f"Your OTP code is: {otp}"
    message.attach(MIMEText(body, "plain"))

    # Connect to the SMTP server
    smtp_server = "smtp.gmail.com"
    port = 587
    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message.as_string())
def generate_otp():
    return str(random.randint(100000, 999999))

@login_required
def otp_verification(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        otp_record = OTP.objects.filter(user=request.user, otp=str(entered_otp))
        if otp_record:
            return redirect('home')
        else:
            messages.error(request, 'Incorrect OTP. Please try again.')
    return render(request, 'data_app/otp.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            email = email.lower()
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                existing_otp = OTP.objects.filter(user=user).first()
                generated_otp = generate_otp()
                new_time_in_ist = datetime.now() + timedelta(minutes=3)
                if existing_otp:
                    existing_otp.otp = generated_otp
                    existing_otp.expiration_time = new_time_in_ist
                    existing_otp.save()
                else:
                    OTP.objects.create(
                        user=request.user,
                        otp=generated_otp,
                        expiration_time=new_time_in_ist
                    )
                send_otp_email(email, generated_otp)
                return redirect('otp_verification')
            else:
                messages.error(request, 'Invalid email or password. Please try again.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url='login')
def inputSelectedCompany(request):
    if request.method == 'POST':
        form = selectCompany(request.POST)
        if form.is_valid():
            selected_company = form.cleaned_data['company']
            fetch_data = {'form': form}
            if selected_company == "LLP":
                queryset = LLPCompany.objects.all()
                serializer = LLPCompanySerializer(queryset, many=True)
                serialized_data = serializer.data
                return render(request, 'llp_company.html',
                              {"llp_data": json.dumps(serialized_data), 'form': form, 'selectedCompany': "LLP"})
            elif selected_company == "Indian":
                queryset = IndianCompany.objects.all()
                serializer = IndianCompanySerializer(queryset, many=True)
                serialized_data = serializer.data
                return render(request, 'indian_company.html',
                              {"indian_data": json.dumps(serialized_data), 'form': form, 'selectedCompany': "Indian"})

            elif selected_company == "Foreign":
                queryset = FCINCompany.objects.all()
                serializer = FCINCompanySerializer(queryset, many=True)
                serialized_data = serializer.data
                return render(request, 'fcin_company.html', {"fcin_data": json.dumps(serialized_data), 'form': form,
                                                             'selectedCompany': "Foreign"})
            return render(request, 'seletctdropdown.html', fetch_data)
    else:
        form = selectCompany()
    return render(request, 'seletctdropdown.html', {'form': form})


@csrf_exempt
def updateIndianCompanyData(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cin = data.pop('CIN', None)
        id = data.pop('id', None)
        filtered_companies = IndianCompany.objects.filter(CIN=cin).update(**data)
        return JsonResponse({'message': 'Data updated successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'})


@csrf_exempt
def updateLLPCompanyData(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        llpin = data.pop('LLPIN', None)
        id = data.pop('id', None)
        filtered_companies = LLPCompany.objects.filter(LLPIN=llpin).update(**data)
        return JsonResponse({'message': 'Data updated successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'})


@csrf_exempt
def updateFCINCompanyData(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        fcin = data.pop('FCIN', None)
        id = data.pop('id', None)
        filtered_companies = FCINCompany.objects.filter(FCIN=fcin).update(**data)
        return JsonResponse({'message': 'Data updated successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'})


from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'


from django.shortcuts import render

def password_reset_confirm_view(request, uidb64, token):
    context = {'uidb64': uidb64, 'token': token}
    return render(request, 'password_reset_confirm.html', context)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    def get_context_data(self, **kwargs):
        # Call the parent class method to get the default context
        context = super().get_context_data(**kwargs)

        # Add additional context data, in this case, uidb64 and token
        context['uidb64'] = self.kwargs['uidb64']
        context['token'] = self.kwargs['token']

        return context



@csrf_exempt
def statusCompanyView(request):
    final_compnay_list = []
    indaian_result = IndianCompany.objects.exclude(file_name = None).values('file_name').annotate(
        file_count=Count('file_name'),
        email_count=Count('email', filter=~Q(email__isnull=True) & ~Q(email='')),
    )
    final_compnay_list.extend(indaian_result)
    fcin_result = FCINCompany.objects.exclude(file_name = None).values('file_name').annotate(
        file_count=Count('file_name'),
        email_count=Count('email', filter=~Q(email=None) & ~Q(email=''))

    )
    final_compnay_list.extend(fcin_result)
    llp_result = LLPCompany.objects.exclude(file_name = None).values('file_name').annotate(
        file_count=Count('file_name'),
        email_count=Count('email', filter=~Q(email=None) & ~Q(email=''))
    )
    final_compnay_list.extend(llp_result)

    for entry in final_compnay_list:
        entry['remaining_update_count'] = entry['file_count'] - entry['email_count']

    return render(request, 'status_company.html', {"status_data": json.dumps(final_compnay_list),
                                                 'selectedCompany': "Status"})


@csrf_exempt
def filesStatusView(request):
    final_compnay_list = []

    result_list = BulkFileModels.objects.values('file_name', 'year', 'month', 'is_active')
    # result_list = result_list.order_by('created_at')
    final_compnay_list = list(result_list)
    for company in final_compnay_list:
        if company['is_active'] == False:
            company['is_active'] = "Done"
        else:
            company['is_active'] = "Not Yet"
    print(final_compnay_list)
    return render(request, 'file_status_data.html', {"status_data":final_compnay_list,
                                                 'selectedCompany': "File Insert Status"})



@login_required(login_url='login')
def dashboardCompany(request):

    count_data = {"company": "No Data"}
    count = 0
    if request.method == 'POST':
        form = DashboardFile(request.POST)
        if form.is_valid():
            selected_company = form.cleaned_data['company']
            selected_month = form.cleaned_data['month']
            selected_year = form.cleaned_data['year']
            # print(selected_company, selected_year, selected_month)
            count_data['form'] = form
            count_data["company"] = selected_company

            if "LLP" in selected_company:
                if selected_month != "All":
                    queryset = LLPCompany.objects.filter(year=selected_year, month=selected_month)
                else:
                    queryset = LLPCompany.objects.filter(year=selected_year)
                count += queryset.values('llp_name').distinct().count()

            if "Indian" in selected_company:
                if selected_month != "All":
                    queryset = IndianCompany.objects.filter(year=selected_year, month=selected_month)
                else:
                    queryset = IndianCompany.objects.filter(year=selected_year)

                count += queryset.values('company_name').distinct().count()
            if "Foreign" in selected_company:
                if selected_month != "All":
                    queryset = FCINCompany.objects.filter(year=selected_year, month=selected_month)
                else:
                    queryset = FCINCompany.objects.filter(year=selected_year)
                count += queryset.values('company_name').distinct().count()
            count_data['count'] = count
    else:
        count_data['form'] = DashboardFile()
        llp_queryset = LLPCompany.objects.all()

        count += llp_queryset.values('llp_name').distinct().count()
        ind_queryset = IndianCompany.objects.filter()
        count += ind_queryset.values('company_name').distinct().count()
        fcin_queryset = FCINCompany.objects.filter()
        count += fcin_queryset.values('company_name').distinct().count()
        count_data['count'] = count
    return render(request, 'dashboard_company.html', count_data)

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.models import User

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        print(request.data)
        if "email" in request.data:
            email = request.data['email']
        else:
            return Response({"status": 200, "message": "please enter the email"}, status=400)

        if "password" in request.data:
            password = request.data['password']
        else:
            return Response({"status": 200, "message": "please enter the password"}, status=400)

        user = User.objects.filter(email=email).first()

        if user is not None and user.check_password(password):
            # User exists and password is correct
            try:
                existing_token = Token.objects.get(user=user)
                existing_token.delete()
            except Token.DoesNotExist:
                pass
            token = Token.objects.create(user=user)
            print(token)
            return Response({'token': token.key}, status=200)
        else:
            return Response({'error': 'Invalid credentials'}, status=401)


