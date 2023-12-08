from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MealForm, MenuForm, BookingRequestForm
from .models import Meal, Menu, BookingRequest, Bookings
from django.db.models import Sum

# Create your views here.
@login_required(login_url= 'login')
def addMeal(request):
    user = request.user
    if  user.is_chef == True:
        profile = request.user
        form = MealForm()
        if request.method =='POST':
                form = MealForm(request.POST, request.FILES)
                if form.is_valid():
                    meal =  form.save(commit=False)
                    meal.owner = profile
                    
                    
 
                    
                    meal.save()
                    messages.success(request, 'Meal was added successfully!')    
                    return redirect('add-meal')
        context = {'form': form}
        return render(request, 'meals/add-meal.html', context)
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('dashboard')
    

@login_required(login_url= 'login')
def viewMeals(request):
     user = request.user
     if  user.is_chef == True:
        meals = Meal.objects.all()
        

        context = {
            'meals': meals,
           
        }
        return render(request, 'meals/view-meals.html', context)
     else:
         messages.error(request, "Access Route Denied!")
         return redirect('dashboard')
    

@login_required(login_url= 'login')
def updateMeal(request, pk):
    user = request.user
    if  user.is_chef == True:
        profile = request.user
        meal = Meal.objects.get(id=pk)
        form = MealForm(instance=meal)
        if request.method =='POST':
                form = MealForm(request.POST, request.FILES, instance=meal)
                if form.is_valid():
                    meal =  form.save(commit=False)
                    meal.owner = profile
                    
                    
 
                    
                    meal.save()
                    # messages.success(request, 'Meal was added successfully!')    
                    return redirect('view-meals')
        context = {'form': form}
        return render(request, 'meals/add-meal.html', context)
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('dashboard')


@login_required(login_url='login')
def deleteMeal(request, pk):
    user = request.user
    if  user.is_chef  == True:

        meal = Meal.objects.get(id=pk)
        meal.delete()
        return redirect('view-meals')

    else:
        messages.error(request, "Access Route Denied!")
        return redirect('dashboard')
    

@login_required(login_url= 'login')
def addMenu(request):
    user = request.user
    if  user.is_chef == True:
        profile = request.user
        form = MenuForm()
        if request.method =='POST':
                form = MenuForm(request.POST)
                if form.is_valid():
                    meal =  form.save(commit=False)
                    meal.owner = profile
                    
                    
 
                    
                    meal.save()
                    messages.success(request, 'Menu was added successfully!')    
                    return redirect('add-menu')
        context = {'form': form}
        return render(request, 'meals/add-menu.html', context)
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('dashboard')
    

@login_required(login_url= 'login')
def viewMenu(request):
     user = request.user
     if  user.is_staff == True:
        menu = Menu.objects.all()
        

        context = {
            'menu': menu,
           
        }
        return render(request, 'meals/view-menu.html', context)
     else:
         messages.error(request, "Access Route Denied!")
         return redirect('dashboard')
    
@login_required(login_url= 'login')
def updateMenu(request, pk):
    user = request.user
    if  user.is_chef == True:
        profile = request.user
        menu = Menu.objects.get(id=pk)
        form = MenuForm(instance=meal)
        if request.method =='POST':
                form = MenuForm(request.POST, request.FILES, instance=meal)
                if form.is_valid():
                    meal =  form.save(commit=False)
                    meal.owner = profile
                    
                    
 
                    
                    meal.save()
                    # messages.success(request, 'Meal was added successfully!')    
                    return redirect('view-menu')
        context = {'form': form}
        return render(request, 'meals/add-menu.html', context)
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('dashboard')

@login_required(login_url='login')
def deleteMenu(request, pk):
    user = request.user
    if  user.is_chef  == True:

        menu = Menu.objects.get(id=pk)
        menu.delete()
        return redirect('view-menu')

    else:
        messages.error(request, "Access Route Denied!")
        return redirect('dashboard')


@login_required(login_url= 'login')
def bookMeal(request, pk):
    user = request.user
    if  user.is_staff == True:
        profile = request.user

        try:     

            menu = Menu.objects.get(id=pk)

            
            
            # print(meal)



            book = BookingRequest.objects.create(owner=profile, menu=menu)
            book.save()
            



            messages.success(request, 'Meal Booked successfully!')
            return redirect('view-menu')
        except(BookingRequest.DoesNotExist, Menu.DoesNotExist):
            return redirect('dashboard')
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('dashboard')
    

@login_required(login_url= 'login')
def viewBookingRequests(request):
     user = request.user
     if  user.is_cook == True:
        booking_req = BookingRequest.objects.filter(is_verified=False)
        

        context = {
            'booking_req': booking_req,
           
        }
        return render(request, 'meals/view-booking-requests.html', context)
     else:
         messages.error(request, "Access Route Denied!")
         return redirect('dashboard')


@login_required(login_url= 'login')
def approveBookingRequests(request, pk):
     user = request.user
     if  user.is_cook == True:
        profile = request.user
        booking = BookingRequest.objects.get(id=pk)

   
        
        menu = booking.menu

     
        
        bookings = Bookings.objects.create(owner=booking, approved_by=profile, menu=menu)
        bookings.save()

        booking.is_verified = True
        booking.save()

        print(booking.is_verified)

        

       
        return redirect('view-booking-requests')
     else:
         messages.error(request, "Access Route Denied!")
         return redirect('dashboard')


@login_required(login_url= 'login')
def cancelBookingRequest(request, pk):
    user = request.user
    if  user.is_cook == True:

        booking = BookingRequest.objects.get(id=pk)

        
        booking.delete()
    
        return redirect('view-booking-requests')
    
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('dashboard')



@login_required(login_url= 'login')
def viewBookings(request):
     user = request.user
     if  user.is_cook == True:
        bookings = Bookings.objects.filter(is_complete=False)
        bookings_count = Bookings.objects.filter(is_complete=False).count()
        total_price = Bookings.objects.filter(is_complete=False).aggregate(Sum('menu__meal__amount'))
        tot = total_price['menu__meal__amount__sum']
        context = {
            'bookings': bookings,
            'bookings_count': bookings_count,
            'tot': tot
           
        }
        return render(request, 'meals/view-bookings.html', context)
     else:
         messages.error(request, "Access Route Denied!")
         return redirect('dashboard')

@login_required(login_url= 'login')
def approveBookingList(request):
    user = request.user
    if  user.is_chef == True:

        booking = Bookings.objects.filter(is_complete=False)

        
        booking.update(is_complete=True)
    
    
        return redirect('view-bookings')
    
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('dashboard')


@login_required(login_url= 'login')
def myBookings(request):
     user = request.user
     if  user.is_staff == True:
        profile = request.user.userprofile
        bookings = Bookings.objects.filter(is_complete=True, owner__owner=user)
        bookings_count = Bookings.objects.filter(is_complete=True, owner__owner=user).count()
        total_price = Bookings.objects.filter(is_complete=True, owner__owner=user).aggregate(Sum('menu__meal__amount'))
        tot = total_price['menu__meal__amount__sum']
      
        context = {
            'bookings': bookings,
            'bookings_count': bookings_count,
            'tot': tot
           
        }
        return render(request, 'meals/my-bookings.html', context)
     else:
         messages.error(request, "Access Route Denied!")
         return redirect('dashboard')