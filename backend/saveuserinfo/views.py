from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile
from draftsAndProjects.models import Project

def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    drafts = Project.objects.filter(user=user, state='draft')
    finished = Project.objects.filter(user=user, state='finished')
    
    context = {
        'user': user,
        'profile': profile,
        'drafts': drafts,
        'finished': finished,
        'total_drafts': drafts.count(),
        'total_finished': finished.count(),
    }
    return render(request, 'HTML/profile.html', context)

def update_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        bio = request.POST.get('bio')
        if bio:
            profile.bio = bio
        
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        
        profile.save()
        return redirect('profile_detail', username=user.username)
    
    context = {'profile': profile}
    return render(request, 'HTML/edit_profile.html', context)