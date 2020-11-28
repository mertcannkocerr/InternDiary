from django.conf.urls import url
from django.contrib.auth.views import login, logout
from .views import (RegisterInternView, RegisterEmployeeView, ProfileView,
                   EditProfileView, LoginView, RegisterCompanyView)
from django.urls import path


urlpatterns = [

    path('register-intern/', RegisterInternView.as_view(), name='register-intern'),
    path('register-employee/', RegisterEmployeeView.as_view(), name='register-employee'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', ProfileView.as_view(), name='view_profile'),
    path('profile/edit', EditProfileView.as_view() , name='edit_profile'),
    path('register-company/', RegisterCompanyView.as_view(), name="register-company")
]
