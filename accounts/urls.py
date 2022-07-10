from django.urls import path
from .views import (
    RegistUserView, UserLoginView, UserLogoutView, activate_user, HowToUseView
)

app_name = 'accounts'

urlpatterns = [
    path('regist/', RegistUserView.as_view(), name='regist'),
    path('user_login/', UserLoginView.as_view(), name='user_login'),
    path('user_logout/', UserLogoutView.as_view(), name='user_logout'),
    path('activate_user/<token>', activate_user, name='activate_user'),
    path('howtouse/', HowToUseView.as_view(), name='howtouse'),
]