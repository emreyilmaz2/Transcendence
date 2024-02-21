from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User
from .forms import SignUpForm


# Create your views here.

def home(request):
    # Check if someone is trying to log in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You Have Been Logged In Sir')
            return redirect('home')
        else:
            messages.success(request, "There Was Error Sir Please Give Me Ten(10) Pounds...")
            return redirect('home')
    else:
        return render(request, 'home.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "Cikis Yaptiniz!")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if(form.is_valid()):
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered :)")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    return render(request, 'register.html', {'form':form})
    
# @login_required
def profile(request):
    # Kullanıcının bilgilerini al
    if request.user.is_authenticated:        
        user = request.user
        context = {
            'user': user  # Kullanıcıyı template'e gönder
        }
        return render(request, 'profile.html', context)
    else:
        messages.success(request, "You must be logged in")
        return redirect('home')
        

def update_profile(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(nickname=request.user.nickname)

        form = SignUpForm(request.POST or None, instance=current_user)
        if form.is_valid():
            form.save()
            login(request, current_user)
            messages.success(request, "Your information has been updated :D")
            return redirect('home')
        
        return render(request, "update_profile.html", {'form':form})
    else:
        messages.success(request, ("You must be logged in!"))
        return redirect('home')
        