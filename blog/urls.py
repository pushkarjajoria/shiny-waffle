from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:page>/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new', views.post_new, name='post_new'),
    path('post/error/', views.post_error, name='post_error'),
    path('error/', views.error, name='error'),
]