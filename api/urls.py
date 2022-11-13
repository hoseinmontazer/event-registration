from django.urls import path
from . import views

urlpatterns = [
    path('', views.Time_Table.as_view(), name='time'),
    path('create/', views.CreateEvent.as_view(), name='CreateEvent'),
    path('delete/', views.DeleteEvent.as_view(), name='DeleteEvent'),
    path('edit/', views.EditEVENT.as_view(), name='edit'),
    path('history/', views.TaskHistory.as_view(), name='history'),
    path('edit-history/', views.TaskEditHistory.as_view(), name='edit-history'),
    path('delete-history/', views.TaskDeletHistory.as_view(), name='delete-history'),

]