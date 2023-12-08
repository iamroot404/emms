from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('my-account/', views.account, name="my-account"),
    path('staffs/', views.staffs, name="staffs"),
    path('add-staff/', views.addStaff, name="add-staff"),
    path('staff-report/', views.staffReport, name="staff-report"),
    # path('delete-account/<str:pk>/', views.deleteAccount, name="delete-account"),
    path('staff-account/<str:pk>/', views.staffAccount, name="staff-account"),
    path('activate-staff/<str:pk>/', views.activateStaff, name="activate-staff"),
    path('deactivate-staff/<str:pk>/', views.deactivateStaff, name="deactivate-staff"),
    path('make-cook/<str:pk>/', views.makeCook, name="make-cook"),
    path('remove-cook/<str:pk>/', views.removeCook, name="remove-cook"),
    path('make-chef/<str:pk>/', views.makeChef, name="make-chef"),
    path('remove-chef/<str:pk>/', views.removeChef, name="remove-chef"),
    path('make-admin/<str:pk>/', views.makeAdmin, name="make-admin"),
    path('remove-admin/<str:pk>/', views.removeAdmin, name="remove-admin"),
]
