from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name='accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        #이미 로그인된 사용자를 자동으로 리디렉션 시켜줌
        redirect_authenticated_user=True,
    ), name='login'),
    path('signup/', views.signup_view, name='signup'),
]