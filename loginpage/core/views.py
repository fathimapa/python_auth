from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

# Create your views here.
@login_required(login_url='sign-in')
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def home(request):
    user = User.objects.get(username =request.user.username)
    context = {
        'home_or_not': True,
        'user': user,
        'range': range(5),
    }
    return render(request, 'home.html',context)

def contact(request):
    return render(request,'contact.html')


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        is_user_exists = User.objects.filter(username=username).exists()
        if is_user_exists:
            user = authenticate(username=username, password=password)
            if user:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request, "Incorrect password")
                return render(request,'login.html')

        else:
            messages.error(request, "Invalid username")
            return render(request,'login.html')
       
    return render(request,'login.html')

def sign_out(request):
    logout(request)
    return redirect('sign-in')