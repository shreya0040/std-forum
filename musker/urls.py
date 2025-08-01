from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('profile/followers/<int:pk>', views.followers, name='followers'),
    path('profile/follows/<int:pk>', views.follows, name='follows'),
    path('login/', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('meep_like/<int:pk>', views.meep_like, name="meep_like"),
    path('meep_show/<int:pk>', views.meep_show, name="meep_show"),
    path('unfollow/<int:pk>', views.unfollow, name="unfollow"),
    path('follow/<int:pk>', views.follow, name="follow"),
    path('delete_meep/<int:pk>', views.delete_meep, name="delete_meep"),
    path('edit_meep/<int:pk>', views.edit_meep, name="edit_meep"),
    path('search/', views.search, name='search'),
    path('communities/', views.community_list, name='community_list'),
    path('create_community/', views.create_community, name='create_community'),
    path('join_community/<int:pk>/', views.join_community, name='join_community'),
    path('community/<int:pk>/', views.community_detail, name='community_detail'),
    path('community/<int:pk>/unjoin/', views.unjoin_community, name='unjoin_community'),
    path('meep/<int:pk>/comment/', views.comment_on_meep, name='comment_on_meep'),
     path('notifications/', views.notifications, name='notifications'),



]
