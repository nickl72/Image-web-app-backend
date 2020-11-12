from django.urls import path
from . import views

urlpatterns = [
    path('api/images/', views.ImageListCreate.as_view() ),
    path('api/images/<int:id>/', views.GetImageById.as_view() ),
    path('api/users/', views.UserListCreate.as_view() ),
    path('api/userimages/', views.UserImagesCreate.as_view() ),
    path('api/edit/image/<int:id>/<str:actions>/<str:changes>/', views.edit),
    path('api/download/<int:id>/', views.send_file),
]