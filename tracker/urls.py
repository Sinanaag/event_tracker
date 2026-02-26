from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('update-status/', views.update_status, name='update_status'),
    path('add-event/', views.add_event, name='add_event'),
    path('event/<int:id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/add-task/', views.add_task, name='add_task'),
    path('event/<int:event_id>/add-attendee/', views.add_attendee, name='add_attendee'),
    path('task/<int:task_id>/update-status/', views.update_task_status, name='update_task_status'),
]