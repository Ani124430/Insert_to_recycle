from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email', '')

        if password != password2:
            return render(request, 'HTML/register.html', {'error': 'Паролите не съвпадат'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'HTML/register.html', {'error': 'Потребителят вече съществува'})

        user = User.objects.create_user(username=username, password=password, email=email)
        return redirect('login')
    
    return render(request, 'HTML/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'HTML/login.html', {'error': 'Невалидни данни'})
    
    return render(request, 'HTML/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def profile_view(request):
    user = request.user
    context = {
        'username': user.username,
        'email': user.email,
    }
    return render(request, 'HTML/profile.html', context)