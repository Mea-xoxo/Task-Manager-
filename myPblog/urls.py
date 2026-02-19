from django.urls import path
from . import views
from .api_views import PostListAPIView
from django.contrib.auth import views as auth_views



urlpatterns = [
    #REGULAR VIEWS
    path('',views.home, name = 'home'),
    path('add/',views.add_post,name = 'add-post'),
    path('post/<int:pk>/edit/',views.edit_post,name = 'edit-post'),
    path('post/<int:pk>/delete/',views.delete_post,name = 'delete-post'),
    path('login/',auth_views.LoginView.as_view(template_name = 'login.html'),name = 'login'),
    path('logout/',auth_views.LogoutView.as_view(),name = 'logout'),


   #API VIEWS
    path('api/posts/', views.post_list_api, name = 'post-list-api'),
    path('api/posts/<int:pk>/',views.post_detail_api, name = 'post-detail-api'),
    path('api/posts/create/',views.create_post_api, name = 'create-post-api'),
    path('api/posts/',PostListAPIView.as_view(), name = 'api-posts'),


]