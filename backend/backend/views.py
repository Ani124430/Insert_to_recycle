from django.shortcuts import render


def index(request):
    return render(request, 'HTML/index.html')

def leaderboardes(request):
    return render(request, 'HTML/leaderboardes.html')

def profile(request):
    return render(request, 'HTML/profile.html')

def newproject(request):
    return render(request, 'HTML/newproject.html')