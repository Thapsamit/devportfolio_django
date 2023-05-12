from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.registerUser,name='register'),
    path('login/',views.LoginPage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('',views.Profiles,name="profiles"),
    path('profile/<str:pk>',views.UserProfile,name="user-profile"),
    path('account/',views.UserAccount,name="user-account"),
    path('edit-account/',views.editAccount,name="edit-account"),
    path('create-skill/',views.createSkill,name="create-skill"),
    path('update-skill/<str:pk>/',views.updateSkill,name="update-skill"),
    path('delete-skill/<str:pk>/',views.deleteSkill,name="delete-skill"),
    path('inbox/',views.inbox,name='inbox')
]