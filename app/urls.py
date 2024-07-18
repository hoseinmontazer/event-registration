
# from django.contrib import admin
# from django.urls import path, include , re_path
# from rest_framework_simplejwt import views as jwt_views

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/token/',jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
#     path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(),name ='token_refresh'),
#     re_path(r'^api/auth/', include('djoser.urls')),
#     re_path(r'^api/event/', include('api.urls')),
#     path('', include('api.urls')),

    
# ]


from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Point to your app's URLs
]