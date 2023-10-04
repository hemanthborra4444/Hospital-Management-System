
from django.contrib import admin

from django.urls import path
from hospital.views import * 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homepage,name='homepage'),
    path('about/',aboutpage,name='aboutpage'),
    path('createaccount/',createaccountpage,name='createaccountpage'),
    path('login/',loginpage,name='loginpage'),
    path('logout/',Logout,name='logout'),
    path('home/',Home,name='home'),
    path('profile/',profile,name='profile'),
    path('makeappointments/',Makeappointment,name='makeappointment'),
    path('viewappointments/',viewappointments,name='viewappointments'),
    path('patientdeleteappointment<int:aid>',patient_delete_appointment,name='patient_delete_appointment'),
    path('login_admin/',Login_admin,name='login_admin'),
    path('admindeletedoctor/',admin_delete_doctor,name='admin_delete_doctor'),
    path('adminaddDoctor/',adminaddDoctor,name='adminaddDoctor'),
    path('adminviewReceptionist/',adminviewReceptionist,name='adminviewReceptionist'),
    path('adminaddReceptionist/',adminaddReceptionist,name='adminaddReceptionist'),
    path('admin_delete_receptionist/',admin_delete_receptionist,name='admin_delete_receptionist'),
    
]
