from multiprocessing import context
from django.shortcuts import render, redirect,get_object_or_404

from . forms import RegistrationForm, UserForm, UserProfileForm
from . models import Account, UserProfile
from .utils import searchStaff, paginateStaff
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
import string  
import random

#report
from django.http import HttpResponse
from .report import render_to_pdf

# Create your views here.
def login(request):
    if request.method == 'POST':
        staff_number = request.POST['staff_number']
        password = request.POST['password']

        user = auth.authenticate(staff_number=staff_number, password=password, is_active=True)

        if user is not None:
            auth.login(request, user)
            #messages.success(request, 'You are now logged in.')
            return redirect(request.GET['next'] if 'next' in request.GET  else 'dashboard')
        else:
            messages.error(request, 'Invalid Login Credentials!')
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required(login_url= 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You Are Logged Out!')
    return redirect('login')

@login_required(login_url= 'login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

@login_required(login_url= 'login')
def account(request):
    profile = request.user.userprofile
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    form = UserProfileForm(instance=profile)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid:
            form.save()

            return redirect('my-account')
    
    context = {
        'userprofile': userprofile,
        'form':form
    }
    return render(request, 'accounts/account.html', context)


@login_required(login_url= 'login')
def staffs(request):
    user = request.user
    if  user.is_admin == True:
        staff, search_query = searchStaff(request)
        custom_range, staff = paginateStaff(request, staff, 10)
       

        context = {
            'staff':staff,
            'search_query': search_query, 
            'custom_range': custom_range
        }
        return render(request, 'accounts/staffs.html', context)
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('dashboard')
    
@login_required(login_url= 'login')
def addStaff(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            # Staff Number Generator
            S = 1
            ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))
            num = random.randrange(100)
            staff = "PH-"
            number =  staff + str(num) + str(ran)
            
            

            staff_number =  number
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, staff_number=staff_number,phone_number=phone_number, password=password)

            user.save()
 
            
            # messages.success(request, 'Thank you for registering us. We have sent you a verification email to your email address')
            return redirect('staffs')
    else:
        form = RegistrationForm()
    context = {
        'form':form,
    }

    return render(request, 'accounts/add-staff.html', context)


@login_required(login_url= 'login')
def staffAccount(request, pk):
    user = request.user
    if  user.is_admin == True:
        userprofile = UserProfile.objects.get(id=pk)
        form = UserProfileForm(instance=userprofile)
        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
            if form.is_valid:
                form.save()

                return redirect('staff-account', pk=userprofile.id)
        
        context = {
            'userprofile': userprofile,
            'form':form
        }
        return render(request, 'accounts/account.html', context)
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('dashboard')


@login_required(login_url= 'login')
def activateStaff(request, pk):
    user = request.user
    if  user.is_admin == True:

        users = Account.objects.get(id=pk)

        users.is_active = True
        users.save()
    
        return redirect('staffs')
    
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('dashboard')
    
@login_required(login_url= 'login')
def deactivateStaff(request, pk):
    user = request.user
    if  user.is_admin == True:

        users = Account.objects.get(id=pk)

        users.is_active = False
        users.save()
    

        return redirect('staffs')
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('dashboard')
    
@login_required(login_url= 'login')
def makeCook(request, pk):
    user = request.user
    if  user.is_admin == True:

        users = Account.objects.get(id=pk)

        users.is_cook = True
   
        
        
        users.save()
    
        return redirect('staffs')
    
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('dashboard')
    
@login_required(login_url= 'login')
def removeCook(request, pk):
    user = request.user
    if  user.is_admin == True:

        users = Account.objects.get(id=pk)

        users.is_cook = False
   
        
        
        users.save()
    
        return redirect('staffs')
    
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('dashboard')

@login_required(login_url= 'login')
def makeChef(request, pk):
    user = request.user
    if  user.is_admin == True:

        users = Account.objects.get(id=pk)

        users.is_cook = True
        users.is_chef = True
        
        
        users.save()
    
        return redirect('staffs')
    
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('dashboard')

@login_required(login_url= 'login')
def removeChef(request, pk):
    user = request.user
    if  user.is_admin == True:

        users = Account.objects.get(id=pk)

        users.is_cook = False
        users.is_chef = False
        
        
        users.save()
    
        return redirect('staffs')
    
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('dashboard')

@login_required(login_url= 'login')
def makeAdmin(request, pk):
    user = request.user
    if  user.is_admin == True:

        users = Account.objects.get(id=pk)

        users.is_cook = True
        users.is_chef = True
        users.is_admin = True
        
        users.save()
    
        return redirect('staffs')
    
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('dashboard')

@login_required(login_url= 'login')
def removeAdmin(request, pk):
    user = request.user
    if  user.is_admin == True:

        users = Account.objects.get(id=pk)

        users.is_cook = False
        users.is_chef = False
        users.is_admin = False
        users.save()
    
        return redirect('staffs')
    
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('dashboard')

# @login_required(login_url= 'login')
# def deleteAccount(request, pk):
#     user = request.user
#     if  user.is_admin == True:

#         users = Account.objects.get(id=pk)

#         users.delete()
#         users.save()
    

#         return redirect('staffs')
#     else:
#         messages.error(request, "Access Route Denied!")
#         return redirect('dashboard')
    

    #REPORT
@login_required(login_url= 'login')
def staffReport(request):
    user = request.user
    if  user.is_admin == True:

        try:
            staff = Account.objects.all()
            staff_count = Account.objects.all().count()
           
            context = {
                'staff': staff, 
                'staff_count': staff_count,
            }
            pdf = render_to_pdf('accounts/staff-list.html', context)
            return HttpResponse(pdf, content_type='application/pdf')
        except(Account.DoesNotExist):
            return redirect('dashboard')
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('dashboard')
