from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("registration", views.regUpdate),
    path("login",views.loginProcess),
    path("logout", views.loggingOut),
    path('success', views.successView), # 
    path('trip/<int:trip_id>', views.view_Trip), #view trip     
    path('trip/<int:trip_id>/delete', views.delete_trip), # deleting a job
    path('trip/<int:trip_id>/edit', views.edit_trip_page), #view edit page
    path('trip/<int:trip_id>/update', views.updatingTrip), #updating trip
    path ('trip/<int:trip_id>/editing', views.edit_trip_process), #
    path('trip/new', views.addingTrip),  #creating a new Trip 
    path('create', views.realAddingTrip),



]