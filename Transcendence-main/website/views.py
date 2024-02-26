from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, Relationship
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required



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
        user = User.objects.get(id=request.user.id)
        
        # other_users = User.objects.exclude(id=request.user.id)  # Mevcut kullanıcıyı listeden çıkar
        friends = user.get_friends()
        sent_requests = Relationship.objects.filter(sender=user, status='send')
        
        other_users = User.objects.exclude(id__in=sent_requests).exclude(id=user.id).exclude(id__in=[friend.id for friend in friends])
        received_requests = Relationship.objects.filter(receiver=user, status='send')
        context = {
            'user': user,  # Kullanıcıyı template'e gönder
            'other_users' : other_users,
            'sent_requests' : sent_requests,
            'received_requests' : received_requests,
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

# @login_required
# def send_friend_request(request, receiver_id):
#     receiver = User.objects.get(id=receiver_id)
#     Relationship.objects.create(sender=request.user, receiver=receiver, status='send')
#     return redirect('profile')

@login_required
def accept_friend_request(request, relationship_id):
    relationship = Relationship.objects.get(id=relationship_id)
    if relationship.receiver == request.user:
        relationship.status = 'accepted'
        relationship.save()
    return redirect('profile')



@login_required
def send_friend_request(request, receiver_id):
    receiver = User.objects.get(id=receiver_id)
    
    # Mevcut ilişkiyi kontrol et
    existing_relationship = Relationship.objects.filter(sender=request.user, receiver=receiver).first()
    
    # Eğer ilişki yoksa veya ilişki kabul edilmişse, yeni bir istek gönder
    if not existing_relationship or existing_relationship.status == 'accepted':
        Relationship.objects.create(sender=request.user, receiver=receiver, status='send')
        # Diğer Kullanıcılar listesinden sil
        other_users = User.objects.exclude(id=request.user.id)
        other_users = other_users.exclude(id=receiver.id)
    return redirect('profile')
