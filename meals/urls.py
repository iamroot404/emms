from django.urls import path
from . import views

urlpatterns = [
    path('add-meal/', views.addMeal, name="add-meal"),
    path('view-meals/', views.viewMeals, name="view-meals"),
    path('update-meal/<str:pk>/', views.updateMeal, name="update-meal"),
    path('delete-meal/<str:pk>/', views.deleteMeal, name="delete-meal"),

    path('add-menu/', views.addMenu, name="add-menu"),
    path('view-menu/', views.viewMenu, name="view-menu"),
    path('update-menu/<str:pk>/', views.updateMenu, name="update-menu"),
    path('delete-menu/<str:pk>/', views.deleteMenu, name="delete-menu"),

    path('book-meal/<str:pk>/', views.bookMeal, name="book-meal"),
    path('view-booking-requests/', views.viewBookingRequests, name="view-booking-requests"),
    path('approve-booking-request/<str:pk>/', views.approveBookingRequests, name="approve-booking-request"),
    path('cancel-booking-request/<str:pk>/', views.cancelBookingRequest, name="cancel-booking-request"),
    
    path('view-bookings/', views.viewBookings, name="view-bookings"),
    path('approve-booking-list/', views.approveBookingList, name="approve-booking-list"),

    path('my-bookings/', views.myBookings, name="my-bookings"),
]
