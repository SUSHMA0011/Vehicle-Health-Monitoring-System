from django.shortcuts import render,redirect, get_object_or_404
from PROJECTApp.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseNotAllowed, HttpResponse, JsonResponse
from PROJECTApp.models import vehicle
from .models import vehicle, fuel,Tyre, user 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password  # For password hashing
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.core.files.storage import default_storage
import io, json, pytz, urllib, base64
from django.db.models.functions import TruncMonth, TruncWeek, TruncDate
from django.utils import timezone
from django.contrib.sessions.models import Session 


def userregisterview(request):
    return render(request,'userregister.html')

def emploginview(request):
    if request.method == 'POST':
        contact = request.POST.get("contact")
        password = request.POST.get("password")

        if not contact or not password:
            # Handle missing contact or password
            messages.error(request, 'Contact and password are required.')
            return render(request, 'userlogin.html')

        userdata = user.objects.filter(contact=contact)
        if not userdata.exists():
            messages.error(request, 'Invalid login credentials.')
            # Handle case where no user is found with the provided contact
            return render(request, 'userlogin.html')

        userinfo = userdata.first()
        if userinfo.password == password:
            if userinfo.is_active:
                ist = pytz.timezone('Asia/Kolkata')
                login_time = timezone.now().astimezone(ist)

                # Retrieve the existing user_sessions or initialize an empty list
                user_sessions = request.session.get('user_sessions', [])

                # Append the new login details to the user_sessions list
                user_sessions.append({
                    'user_id': userinfo.id,
                    'firstname': userinfo.firstname,
                    'contact': userinfo.contact,
                    'login_time': login_time.strftime('%Y-%m-%d %I:%M:%S %p'),
                    'logout_time': 'Currently logged in'
                })

                # Update the session with the new list
                request.session['user_sessions'] = user_sessions
                request.session['user_id'] = userinfo.id  # Store user_id in session

                return render(request, 'userhome.html')
            else:
                messages.error(request, 'Your account is inactive. Please contact the administrator.')
                return render(request, 'userlogin.html')
        else:
            messages.error(request, 'Invalid login credentials.')
            return render(request, 'userlogin.html')

    return render(request, 'userlogin.html')


def active_usersview(request):
    active_users = user.objects.filter(is_active=True)
    return render(request, 'active_users.html', {'users': active_users})   


def userloginview(request):
    if 'user_id' in request.session:
        ist = pytz.timezone('Asia/Kolkata')
        logout_time = timezone.now().astimezone(ist)

        # Retrieve the existing user_sessions
        user_sessions = request.session.get('user_sessions', [])

        # Update the logout time for the current user
        for session in user_sessions:
            if session['user_id'] == request.session['user_id']:
                session['logout_time'] = logout_time.strftime('%Y-%m-%d %I:%M:%S %p')
                break

        # Update the session with the new list
        request.session['user_sessions'] = user_sessions

        # Clear individual session keys
        del request.session['user_id']

    return render(request, 'userlogin.html')


def userdashboardview(request):
    user_id = request.session.get('user_id')
    if user_id:
        user_obj = user.objects.get(id=user_id)
    else:
        user_obj = None
    
    if request.method == 'GET':
        plate_number = request.GET.get('plate_number')
        try:
            vehicle_obj = vehicle.objects.get(vnumber=plate_number)
            return render(request, 'userdashboard.html', {'vehicle': vehicle_obj, 'user': user_obj})
        except vehicle.DoesNotExist:
            error_message = "Vehicle with plate number {} does not exist.".format(plate_number)
            return render(request, 'userhome.html', {'error_message': error_message, 'user': user_obj})
    return render(request, 'userhome.html', {'user': user_obj})

def savenewuserview(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        license = request.POST['license']
        contact = request.POST['contact']
        password = request.POST['password']
        new_user = user(firstname=firstname, license=license, contact=contact, password=password, is_active=0)
        new_user.save()
        return render(request, 'userregister.html')  # Redirect to a success page after registration
    return render(request, 'userregister.html')


def userhomeview(request):
    user_id = request.session.get('user_id')
    if user_id:
        user_obj = user.objects.get(id=user_id)
        return render(request, 'userhome.html', {'user': user_obj, 'total_employees_count': user.objects.count()})
    else:
        return render(request, 'userhome.html', {'total_employees_count': user.objects.count()})
   

@csrf_exempt
def savefuelview(request):
    if request.method == 'POST':
        vnumber = request.POST.get('vnumber')
        driverName = request.POST.get('driverName')
        date = request.POST.get('date')
        billNumber = request.POST.get('billNumber')
        fuelStation = request.POST.get('fuelStation')
        liter = request.POST.get('liter')
        amount = request.POST.get('amount')
        readings = request.POST.get('readings')
        fuelimage=request.FILES.get('fuelimage')
        # Save to database
        fuel.objects.create(
            vnumber=vnumber,
            driverName=driverName,
            date=date,
            billNumber=billNumber,
            fuelStation=fuelStation,
            liter=liter,
            amount=amount,
            readings=readings,
            fuelimage=fuelimage
        )

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})


@csrf_exempt
def savetyreview(request):
    if request.method == 'POST':
        vnumber = request.POST.get('vnumber')
        driver_name = request.POST.get('driver_name')
        tyrenumber = request.POST.get('tyrenumber')
        tyre_type = request.POST.get('tyre_type')
        date = request.POST.get('date')
        kilometer = request.POST.get('kilometer')
        bill_number = request.POST.get('bill_number')
        amount = request.POST.get('amount')
        tyreimage = request.FILES.get('tyreimage')
        
        # Save to database
        Tyre.objects.create(
            vnumber=vnumber,
            driver_name=driver_name,
            tyrenumber=tyrenumber,
            tyre_type=tyre_type,
            date=date,
            kilometer=kilometer,
            bill_number=bill_number,
            amount=amount,
            tyreimage=tyreimage
        )

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})
 
def user_dashboard(request):
    # Add your existing logic here
    return render(request, 'userdashboard.html')
       
def successview(request):
    return render(request,'success.html')

def adminloginview(request):
    return render(request,'adminlogin.html')




def mainadminloginview(request):
    if request.method == "GET":
        return render(request, 'adminlogin.html')
    elif request.method == "POST":
        aname = request.POST.get("aname", None)
        apassword = request.POST.get("apassword", None)
        if aname == "admin" and apassword == "admin":
            context = {"login_success": True}
            return render(request, 'adminlogin.html', context)
        else:
            context = {"login_failed": True}
            return render(request, 'adminlogin.html', context)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


def addvehicleview(request):
    return render(request,'addvehicle.html')

def savenewvehicleview(request):
    name=request.POST["name"]
    model=request.POST["model"]
    vnumber=request.POST["vnumber"]
    cnumber=request.POST["cnumber"]
    
    newvehicle=vehicle(name=name,model=model,vnumber=vnumber,cnumber=cnumber)
    newvehicle.save()
    return render(request,'addvehicle.html')
 
def vehicledetailsview(request):
    vehicles = vehicle.objects.all()  # Retrieve all vehicle records
    total_vehicles_count = vehicles.count()  # Calculate total number of vehicles
    return render(request, 'vehicledetails.html', {'vehicles': vehicles, 'total_vehicles_count': total_vehicles_count})

def viewuserview(request):
    userdetails = user.objects.all()
    return render(request, 'viewuser.html', {'users': userdetails})


def inactivatebtnview(request):
    userid=request.GET["userid"]
    user.objects.filter(id=userid).update(is_active=0)
    userdetails=user.objects.all()
    return render(request,'viewuser.html',{'users':userdetails})

def activatebtnview(request):
    userid=request.GET["userid"]
    user.objects.filter(id=userid).update(is_active=1)
    userdetails=user.objects.all()
    return render(request,'viewuser.html',{'users':userdetails})    


def deleteuserview(request, id):
    if request.method == "POST":
        user_instance = get_object_or_404(user, id=id)
        user_instance.delete()
        return redirect('/viewuser/')  # Make sure this URL is correct and points to the page listing the users
    else:
        return HttpResponseNotAllowed(['POST'])    

def vehiclefuelview(request, vehicle_id):
    # Vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    fueldetails = fuel.objects.all()
    return render(request, 'vehicledetails.html', { 'fuels': fueldetails})        


def deletevehicleview(request, id):
    if request.method == "POST":
        vehicle_instance = get_object_or_404(vehicle, id=id)
        vehicle_instance.delete()
        return redirect('/vehicledetails/')
    else:
        return HttpResponseNotAllowed(['POST'])    


def vehiclefuelview(request):
    fueldetails = fuel.objects.all()
    return render(request, 'vehiclefuel.html', {'fuels': fueldetails})   


def forgotpasswordview(request):
    return render(request, 'forgotpassword.html')


def passwordrequestview(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        contact = request.POST.get('contact')

        try:
            user_instance = user.objects.get(firstname=firstname, contact=contact)
            # Log the user request
            request.session['requested_user_ids'] = request.session.get('requested_user_ids', [])
            if user_instance.id not in request.session['requested_user_ids']:
                request.session['requested_user_ids'].append(user_instance.id)
            return render(request, 'userlogin.html')
        except user.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect('passwordrequest')

    return render(request, 'userlogin.html')


def checkrequestview(request):
    requested_user_ids = request.session.get('requested_user_ids', [])
    users = user.objects.filter(id__in=requested_user_ids) if requested_user_ids else []

    return render(request, 'adminpassword.html', {'users': users})

def change_password(request, user_id):
    user_instance = user.objects.get(id=user_id)

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        user_instance.password = new_password  # This should ideally hash the password
        user_instance.save()

        requested_user_ids = request.session.get('requested_user_ids', [])
        if user_instance.id in requested_user_ids:
            requested_user_ids.remove(user_instance.id)
            request.session['requested_user_ids'] = requested_user_ids

        messages.success(request, 'Password changed successfully')
        return redirect('checkrequest')
    return render(request, 'change_password.html', {'user': user_instance, 'old_password': user_instance.password })    

   
def previewfuelview(request):
    driver_name = request.GET.get('driverName')
    fuel_data = fuel.objects.filter(driverName=driver_name)
    return render(request, 'view_fuel.html', {'fuel_data': fuel_data})

def editfuelview(request,pk):
    Fuel=fuel.objects.get(id=pk)
    return render(request, 'edit_fuel.html', {'fuel': Fuel})

def saveeditview(request, pk):
    Fuel = get_object_or_404(fuel, id=pk)
    if request.method == 'POST':
        Fuel.date = request.POST.get('date')
        Fuel.billNumber = request.POST.get('billNumber')
        Fuel.fuelStation = request.POST.get('fuelStation')
        Fuel.liter = request.POST.get('liter')
        Fuel.amount = request.POST.get('amount')
        Fuel.readings = request.POST.get('readings')
        Fuel.fuelimage = request.POST.get('fuelimage')

        if 'fuelimage' in request.FILES:
            Fuel.fuelimage = request.FILES['fuelimage']
        else:
            Fuel.fuelimage.name = request.POST.get('existing_image')

        Fuel.save()
        driver_name = Fuel.driverName
        return redirect(f'/previewfuel/?driverName={driver_name}')

    return render(request, 'edit_fuel.html', {'fuel': Fuel})


def previewtyreview(request):
    driverName = request.GET.get('driver_name')
    tyre_data = Tyre.objects.filter(driver_name=driverName)
    return render(request, 'view_tyre.html', {'tyre_data': tyre_data})

def edittyreview(request,pk):
    tyre=Tyre.objects.get(id=pk)
    return render(request, 'edit_tyre.html', {'Tyre': tyre})

def saveeeditview(request, pk):
    tyre = get_object_or_404(Tyre, id=pk)
    
    if request.method == "POST":
        tyre.tyrenumber = request.POST.get('tyrenumber')
        tyre.tyre_type = request.POST.get('tyre_type')
        tyre.date = request.POST.get('date')
        tyre.kilometer = request.POST.get('kilometer')
        tyre.bill_number = request.POST.get('billNumber')
        tyre.amount = request.POST.get('amount')
        # tyre.tyreimage = request.POST.get('tyreimage')
        
        if 'tyreimage' in request.FILES:
            tyre.tyreimage = request.FILES['tyreimage']
        else:
            tyre.tyreimage.name = request.POST.get('existing_image')
        
        tyre.save()

        driver_name = request.GET.get('driver_name', '')  # Get driver_name from the query parameters
        return redirect(f'/previewtyre/?driver_name={driver_name}')
    
    return render(request, 'edit_tyre.html', {'Tyre': tyre})
    

def admintyreview(request):
    tyredetails = Tyre.objects.all()  
    alert_tyres = Tyre.objects.filter(kilometer__gte=1000)
    return render(request, 'admintyre.html', {'tyres': tyredetails, 'alert_tyres': alert_tyres})



def adminhomeview(request):
    total_employees_count = user.objects.count() 
    total_vehicles_count = vehicle.objects.count() 
    active_users_count = user.objects.filter(is_active=True).count()
    login_details = request.session.get('user_sessions', [])

    # Fetch fuel and tyre data
    fuels = fuel.objects.all()
    tyres = Tyre.objects.all()
    alert_tyres = Tyre.objects.filter(kilometer__gte=10000)
    alert_tyres_count = alert_tyres.count()
    
    # Aggregate fuel data
    fuel_data = fuel.objects.annotate(fuel_date=TruncDate('date')).values('fuel_date').annotate(total_amount=Sum('amount')).order_by('fuel_date')
    fuel_chart_data = [['Date', 'Total Amount']]
    for entry in fuel_data:
        fuel_chart_data.append([entry['fuel_date'].strftime('%Y-%m-%d'), entry['total_amount']])
    
    # Aggregate tyre data
    tyre_data = Tyre.objects.annotate(tyre_date=TruncDate('date')).values('tyre_date').annotate(total_amount=Sum('amount')).order_by('tyre_date')
    tyre_chart_data = [['Date', 'Total Amount']]
    for entry in tyre_data:
        tyre_chart_data.append([entry['tyre_date'].strftime('%Y-%m-%d'), entry['total_amount']])

    # Combine fuel and tyre data for monthly and weekly reports
    def aggregate_data(data, frequency):
        aggregated_data = {}
        for entry in data:
            date_key = entry[frequency].strftime('%Y-%m') if frequency == 'month' else entry[frequency].strftime('%Y-%W')
            aggregated_data[date_key] = aggregated_data.get(date_key, 0) + entry['total_amount']
        return aggregated_data
    

    # Monthly aggregation
    monthly_fuel_data = fuel.objects.annotate(month=TruncMonth('date')).values('month').annotate(total_amount=Sum('amount')).order_by('month')
    monthly_tyres_data = Tyre.objects.annotate(month=TruncMonth('date')).values('month').annotate(total_amount=Sum('amount')).order_by('month')
    
    combined_monthly_data = aggregate_data(monthly_fuel_data, 'month')
    for entry in monthly_tyres_data:
        month = entry['month'].strftime('%Y-%m')
        combined_monthly_data[month] = combined_monthly_data.get(month, 0) + entry['total_amount']
    
    monthly_chart_data = [['Date', 'Total Amount']]
    for date, amount in combined_monthly_data.items():
        monthly_chart_data.append([date, amount])


    # Weekly aggregation
    weekly_fuel_data = fuel.objects.annotate(week=TruncWeek('date')).values('week').annotate(total_amount=Sum('amount')).order_by('week')
    weekly_tyres_data = Tyre.objects.annotate(week=TruncWeek('date')).values('week').annotate(total_amount=Sum('amount')).order_by('week')
    
    combined_weekly_data = aggregate_data(weekly_fuel_data, 'week')
    for entry in weekly_tyres_data:
        week = entry['week'].strftime('%Y-%W')
        combined_weekly_data[week] = combined_weekly_data.get(week, 0) + entry['total_amount']
    
    weekly_chart_data = [['Date', 'Total Amount']]
    for date, amount in combined_weekly_data.items():
        weekly_chart_data.append([date, amount])    

    context = {
        'password_request_count': len(request.session.get('requested_user_ids', [])),
        'total_employees_count': total_employees_count,
        'total_vehicles_count': total_vehicles_count,
        'fuels': fuels,
        'tyres': tyres,
        'total_tyres_count': alert_tyres_count,
        'active_users_count': active_users_count,
        'login_details': login_details,
        'fuel_chart_data': json.dumps(fuel_chart_data),
        'tyre_chart_data': json.dumps(tyre_chart_data),
        'monthly_chart_data': json.dumps(monthly_chart_data),
        'weekly_chart_data': json.dumps(weekly_chart_data),
    }
    return render(request, 'adminhome.html', context)


def editvehicleview(request, pk):
    Vehicle = get_object_or_404(vehicle, id=pk)
    return render(request, 'edit_vehicle.html', {'vehicle': Vehicle})

def savevehicleview(request, pk):
    Vehicle = get_object_or_404(vehicle, id=pk)
    if request.method == 'POST':
        Vehicle.name = request.POST.get('name')
        Vehicle.model = request.POST.get('model')
        Vehicle.vnumber = request.POST.get('vnumber')
        Vehicle.cnumber = request.POST.get('cnumber')
        Vehicle.save()
        return redirect('/vehicledetails/')

def edituserview(request, pk):
    User = get_object_or_404(user, id=pk)
    return render(request, 'edit_user.html', {'user': User})

def saveeuserview(request, pk):
    User = get_object_or_404(user, id=pk)
    if request.method == 'POST':
        User.firstname = request.POST.get('firstname')
        User.license = request.POST.get('license')
        User.contact = request.POST.get('contact')
        User.password = request.POST.get('password')
        User.save()
        return redirect('/viewuser/')
    return render(request, 'edit_user.html', {'user': User})