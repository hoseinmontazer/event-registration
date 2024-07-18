# from django.urls import path , re_path , include
# from . import views
# from rest_framework.routers import DefaultRouter
# from .views import CustomUserCreateView

# urlpatterns = [
#     #path('', views.Time_Table.as_view(), name='time'),
    
#     path('create/', views.CreateEvent.as_view(), name='CreateEvent'),
#     path('delete/', views.DeleteEvent.as_view(), name='DeleteEvent'),
#     path('edit/', views.EditEVENT.as_view(), name='edit'),
#     path('get-invitation/',views.GetInvitation.as_view(),name='GetInvitation'),
#     #re_path(r'^check-invitation/', views.CheckInvitation.as_view(),name='CheckInvitation')
#     # path('history/', views.TaskHistory.as_view(), name='history'),
#     # path('edit-history/', views.TaskEditHistory.as_view(), name='edit-history'),
#     # path('delete-history/', views.TaskDeletHistory.as_view(), name='delete-history'),
    
#     # Include default Djoser URLs except user create
#     path('auth/', include('djoser.urls')),
#     # Override the user create endpoint
#     path('auth/users/', CustomUserCreateView.as_view(), name='user-create'),
#     # Include the JWT authentication URLs if using JWT
#     path('auth/', include('djoser.urls.jwt')),    

# ]





from django.urls import path, include
from .views import CustomUserCreateView
from api import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('event/', views.Time_Table.as_view(), name='event'),
    path('create/', views.CreateEvent.as_view(), name='CreateEvent'),
    path('delete/', views.DeleteEvent.as_view(), name='DeleteEvent'),
    path('edit/', views.EditEVENT.as_view(), name='edit'),
    path('get-invitation/',views.GetInvitation.as_view(),name='GetInvitation'),
    #re_path(r'^check-invitation/', views.CheckInvitation.as_view(),name='CheckInvitation')
    # path('history/', views.TaskHistory.as_view(), name='history'),
    # path('edit-history/', views.TaskEditHistory.as_view(), name='edit-history'),
    # path('delete-history/', views.TaskDeletHistory.as_view(), name='delete-history'),
    path('token/',jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(),name ='token_refresh'),



    # Your custom view for user creation
    path('auth/users/', CustomUserCreateView.as_view(), name='user-create'),

    # Include Djoser's default URLs
    path('auth/', include('djoser.urls')),

    # Include Djoser's JWT URLs if using JWT
    path('auth/', include('djoser.urls.jwt')),
]