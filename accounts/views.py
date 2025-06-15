from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

# Create your viewsets here.
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else :
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form':form})