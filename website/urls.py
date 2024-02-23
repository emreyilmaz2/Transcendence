from django.urls import path
from . import views
from .views import send_friend_request, accept_friend_request

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views. logout_user, name= 'logout'),
    path('register/', views.register_user, name= 'register'),
    path('profile/', views.profile, name= 'profile'),
    path('update_profile/', views.update_profile, name= 'update_profile'),
    path('send-friend-request/<int:receiver_id>/', send_friend_request, name='send_friend_request'),
    path('accept-friend-request/<int:relationship_id>/', accept_friend_request, name='accept_friend_request'),
    
]