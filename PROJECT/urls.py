"""PROJECT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from PROJECTApp.views import*
from PROJECTApp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('userregister/',userregisterview),
    path('userlogin/',userloginview),
    path('userdashboard/',userdashboardview),
    path('emplogin/',emploginview),
    path('userhome/',userhomeview),
    path('savenewuser/',savenewuserview),
    path('savefuel/',savefuelview, name='savefuel'),
    path('savetyre/',savetyreview, name='savetyre'),
    path('success/',successview),
    path('getadminlogin/',adminloginview),
    path('adminlogin/',mainadminloginview),
    path('adminhome/',adminhomeview),
    path('addvehicle/',addvehicleview),
    path('addnewvehicle/',savenewvehicleview),
    path('vehicledetails/',vehicledetailsview),
    path('deletevehicle/<int:id>/', deletevehicleview, name='deletevehicle'),
    path('viewuser/',viewuserview),
    path('inactivatebtn/',inactivatebtnview),
    path('activatebtn/',activatebtnview),
    path('deleteuser/<int:id>/', deleteuserview, name='deleteuser'),
    path('vehiclefuel/', vehiclefuelview, name='vehiclefuel'),
    path('admintyre/',admintyreview,name='admintyre'),
    path('forgotpassword/', views.forgotpasswordview, name='forgotpassword'),
    path('passwordrequest/', views.passwordrequestview, name='passwordrequest'),
    path('checkrequest/', views.checkrequestview, name='checkrequest'),
    path('change_password/<int:user_id>/', views.change_password, name='change_password'),


    path('previewfuel/',previewfuelview),
    path('editfuel/<int:pk>/', editfuelview, name='editfuel'),
    path('saveedit/<int:pk>/', saveeditview, name='saveedit'),


    
    path('previewtyre/',previewtyreview),
    path('edittyre/<int:pk>/', edittyreview, name='edittyre'),
    path('saveeedit/<int:pk>/', saveeeditview, name='saveeedit'),
    path('active_users/', views.active_usersview, name='active_users'),
    path('editvehicle/<int:pk>/', editvehicleview, name='editvehicle'),
    path('savevehicle/<int:pk>/', savevehicleview, name='savevehicle'),
    path('edituser/<int:pk>/', edituserview, name='edituser'),
    path('saveeuser/<int:pk>/', saveeuserview, name='saveeuser'),
  
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

