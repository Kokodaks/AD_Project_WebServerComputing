from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
# def signup_view(request):
#     # if request.method == 'POST':
#     #
#     # return render(request, 'accounts/signup.html')

def login_view(request):
    if request.method == 'POST':
        username=request.POST.username
        password=request.POST.password

        user = authenticate(request, username, password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, '아이디 또는 비밀번호가 올바르지 않습니다.')
    return render(request, 'accounts/login.html')

@login_required
def home_view(request):
    return render(request, 'accounts/home.html', {'user', request.user})