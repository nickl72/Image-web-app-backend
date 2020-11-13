from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_optain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/images/', views.ImageListCreate.as_view() ),
    path('api/images/<int:id>/', views.GetImageById.as_view() ),
    path('api/users/', views.UserListCreate.as_view() ),
    path('api/users/<str:username>/', views.SingleUser.as_view() ),
    path('api/userimages/', views.UserImagesCreate.as_view() ),
    path('api/edit/image/<int:id>/<str:actions>/<str:changes>/', views.edit),
    path('api/download/<int:id>/', views.send_file),
    path('api/ascii/<int:id>/', views.send_ascii),
    path('api/ascii/<int:id>/<str:html>/', views.send_ascii ),
    path('api/crop/<int:id>/<int:left>/<int:top>/<int:right>/<int:bottom>/', views.crop ),
    path('api/overlay/<int:id_1>/<int:id_2>/<int:left>/<int:top>/', views.overlay ),
]