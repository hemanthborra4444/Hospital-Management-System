from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User,Group
from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponse

from django.utils import timezone
from datetime import datetime

def homepage(request):
    return render(request,'index.html')
def aboutpage(request):
    return render(request,'about.html')
def createaccountpage(request):
    user = "none"
    error = ""
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpassword']
        gender = request.POST['gender']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        birthdate = request.POST['dateofbirth']
        bloodgroup = request.POST['bloodgroup']
        
        try:
            if password == repeatpassword:
                Patient.objects.create(name=name,email=email,gender=gender,phonenumber=phonenumber,address=address,birthdate=birthdate,bloodgroup=bloodgroup)
                user = User.objects.create_user(first_name=name,email=email,password=password,username=email)
                pat_group = Group.objects.get(name = 'Patient')
                pat_group.user_set.add(user)
                user.save()
                error = 'no'
            
            else:
                error = 'yes'
        except Exception as e:
            
            error = 'yes'
    d = { 'error' : error }
              
    return render(request, 'createaccount.html', d )

def Login_admin(request):
    error=""
    if request.method == 'POST':
        u=request.POST['username']
        p=request.POST['password']
        user = authenticate(request,username=u,password=p)
        try:
            if user is not None:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error ="yes"
    d={'error':error}
    return render(request,'adminlogin.html',d)

def loginpage(request):
    error=""
    if request.method == 'POST' :
        u=request.POST['email']
        p=request.POST['password']
        user = authenticate(request,username=u,password=p)
        try:
            if user is not None:
                error = "no"
                login(request,user)
                g = request.user.groups.all()[0].name
                if g == 'Patient':
                   d = { 'error' : error }
                   return render(request,'patienthome.html',d)
                elif g =='Doctor':
                   d = {'error':error}
                   return render(request,'doctorhome.html',d)
                elif g =='Receptionist':
                   d = {'error' : error}
                   return render(request,'receptionhome.html',d)
                
            else:
                error = "yes"
        except Exception as e:
            error = "yes"


    return render(request,'login.html')
def Logout(request):
    logout(request)
    return redirect('loginpage')
def Home(request):
    if not request.user.is_active:
        return redirect('loginpage')
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        return render(request,'patienthome.html')
    elif g == 'Doctor':
        return render(request,'doctorhome.html')
    elif g=='Receptionist':
        return render(request,'receptionhome.html')
    

def profile(request):
    if not request.user.is_active:
        return redirect('loginpage')
    g= request.user.groups.all()[0].name
    if g=='Patient':
        patient_details = Patient.objects.all().filter(email=request.user)
        d = {'patient_details': patient_details}
        return render(request,'patientprofile.html',d)
    elif g=='Doctor':
        doctor_details = Doctor.objects.all().filter(email=request.user)
        d = {'doctor_details': doctor_details}
        return render(request,'doctorprofile.html',d)
    elif g=='Receptionist':
        reception_details = Receptionist.objects.all().filter(email=request.user)
        d = {'reception_details': reception_details}
        return render(request,'receptionprofile.html',d)

def Makeappointment(request):
   
    if not request.user.is_active:
        return redirect('loginpage')
    error=""
    alldoctors=Doctor.objects.all()
    d={ 'alldoctors': alldoctors }
    if request.method == 'POST':
        temp = request.POST['doctoremail']
        doctoremail=temp.split()[0]
        doctorname=temp.split()[1]
        patientname=request.POST['patientname']
        patientemail=request.POST['patientemail']
        appointmentdate =request.POST['appointmentdate']
        appointmenttime=request.POST['appointmenttime']
        symptoms=request.POST['symptoms']
        try:
            Appointment.objects.create(doctorname=doctorname,doctoremail=doctoremail,patientname=patientname,symptoms=symptoms,patientemail=patientemail,appointmentdate=appointmentdate,appointmenttime=appointmenttime,status=True,prescription="")
            error="no"
        except Exception as e:
            error="yes"
        e={'error': error}
        return render(request,'patientmakeappointments.html',e)
    return render(request,'patientmakeappointments.html',d)
def viewappointments(request):
    if not request.user.is_active:
        return redirect('loginpage')
    g=request.user.groups.all()[0].name
    if g == 'Patient':
        upcomming_appointments=Appointment.objects.all().filter(patientemail=request.user,appointmentdate__gte=timezone.now()).order_by('appointmentdate')
        previous_appointments=Appointment.objects.all().filter(patientemail=request.user,appointmentdate__lt=timezone.now()).order_by('appointmentdate') | Appointment.objects.filter(patientemail=request.user,status=False).order_by('-appointmentdate')
        d={'upcomming_appointments':upcomming_appointments ,'previous_appointments':previous_appointments}
        return render(request,'patientviewappointments.html',d)
    elif g == 'Doctor':
        if request.method == 'POST':
            prescriptiondata = request.POST['prescription']
            idvalue = request.POST['idofappointment']
            Appointment.objects.filter(id=idvalue).update(prescription=prescriptiondata,status=False)
        upcomming_appointments=Appointment.objects.all().filter(doctoremail=request.user,appointmentdate__gte=timezone.now()).order_by('appointmentdate')
        previous_appointments=Appointment.objects.all().filter(doctoremail=request.user, appointmentdate__lt=timezone.now()).order_by('appointmentdate') | Appointment.objects.filter(doctoremail=request.user,status=False).order_by('-appointmentdate')

        d={'upcomming_appointments':upcomming_appointments ,'previous_appointments':previous_appointments}
        return render(request,'doctorviewappointment.html',d)  
    elif g == 'Receptionist':
        upcomming_appointments=Appointment.objects.filter(email=request.user,appointmentdate__gte=timezone.now()).order_by('appointmentdate')
        previous_appointments=Appointment.objects.filter(email=request.user,appointmentdate__lt=timezone.now()).order_by('appointmentdate') | Appointment.objects.filter(email=request.user,status=False).order_by('-appointmentdate')
        d={'upcomming_appointments':upcomming_appointments ,'previous_appointments':previous_appointments}
        return render(request,'receptionviewappointments.html',d)
def patient_delete_appointment(request,aid):
        appointment = Appointment.objects.get(id=aid)
        appointment.delete()
        return redirect('viewappointments')
def admin_delete_doctor(request,pid,email):
    if not request.user.is_staff:
        return redirect('login_admin')
    doctor=Doctor.objects.get(id=pid)
    doctor.delete()
    users=User.objects.filter(username=email)
    users.delete()
    return redirect('adminviewDoctor')
def adminaddDoctor(request):
    user = "none"
    error = ""
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpassword']
        gender = request.POST['gender']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        birthdate = request.POST['dateofbirth']
        bloodgroup = request.POST['bloodgroup']
        
        try:
            if password == repeatpassword:
                Doctor.objects.create(name=name,email=email,gender=gender,phonenumber=phonenumber,address=address,birthdate=birthdate,bloodgroup=bloodgroup)
                user = User.objects.create_user(first_name=name,email=email,password=password,username=email)
                doc_group = Group.objects.get(name = 'Doctor')
                doc_group.user_set.add(user)
                user.save()
                error = 'no'
            
            else:
                error = 'yes'
        except Exception as e:
            
            error = 'yes'
    d = { 'error' : error }
              
    return render(request,'adminadddoctor.html', d )
def adminviewReceptionist(request):
    if not request.user.is_staff:
        return redirect('login_admin')
    rec=Receptionist.objects.all()
    r={'rec':rec}
    return render(request,'adminviewreceptionists.html',r)
def adminaddReceptionist(request):
    error=""
    if not request.user.is_staff:
        return redirect('login_admin')
    if request.method =="POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpassword']
        gender = request.POST['gender']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        birthdate = request.POST['dateofbirth']
        bloodgroup = request.POST['bloodgroup']
        
        try:
            if password == repeatpassword:
                Receptionist.objects.create(name=name,email=email,gender=gender,phonenumber=phonenumber,address=address,birthdate=birthdate,bloodgroup=bloodgroup)
                user = User.objects.create_user(first_name=name,email=email,password=password,username=email)
                rec_group = Group.objects.get(name = 'Receptionist')
                rec_group.user_set.add(user)
                user.save()
                error = 'no'
            
            else:
                error = 'yes'
        except Exception as e:
            
            error = 'yes'
    d = { 'error' : error }
              
    return render(request,'adminaddReceptionist.html', d )
        



def admin_delete_receptionist(request,pid,email):
    if not request.user.is_staff:
        return redirect('login_admin')
    reception=Receptionist.objects.get(id=pid)
    reception.delete()
    users=User.objects.filter(username=email)

