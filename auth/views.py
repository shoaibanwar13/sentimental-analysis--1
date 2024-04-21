from django.shortcuts import render,redirect
from django.contrib.auth import login, logout
from .forms import SignUpForm
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('page2')
    else:
        form = SignUpForm()
        print('error')

    return render(request, 'signup.html', {'form': form})
def logoutfunction(request):
    logout(request)
    return redirect('/')
# Create your views here. cheating hy yee oo sorry 
