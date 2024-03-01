from django.urls import path
from . import views
from .views import send_friend_request, accept_friend_request

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('login_page/', views.login_page, name='login_page'),
    #path('forget_passwd/', views.forget_passwd, name='forget_passwd'),
    path('friends/', views.friends, name= 'friends'),
    path('profile_set', views.profile_set, name= 'profile_set'),
    path('logout_user/', views.logout_user, name= 'logout_user'),
    path('register/', views.register_user, name= 'register'),
    path('profile/', views.profile, name= 'profile'),
    path('update_profile/', views.update_profile, name= 'update_profile'),
    path('send-friend-request/<int:receiver_id>/', send_friend_request, name='send_friend_request'),
    path('accept-friend-request/<int:relationship_id>/', accept_friend_request, name='accept_friend_request'),
    
]