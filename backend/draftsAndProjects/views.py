from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Project

def create_project_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('desc', '')
        oldPic = request.FILES.get('oldPic')
        
        if not title:
            return render(request, 'HTML/newproject.html', {'error': 'Титлата е задължителна'})
        
        project = Project.objects.create(
            user=request.user,
            title=title,
            desc=desc,
            oldPic=oldPic,
            state='draft'
        )
        return redirect('project_detail', project_id=project.id)
    
    return render(request, 'HTML/newproject.html')

def project_detail_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    context = {'project': project}
    return render(request, 'HTML/project_detail.html', context)

def finish_project_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        newPic = request.FILES.get('newPic')
        
        if not newPic:
            return render(request, 'HTML/second_pic.html', {
                'project': project,
                'error': 'Финалната снимка е задължителна'
            })
        
        project.newPic = newPic
        project.state = 'finished'
        project.save()
        return redirect('profile_detail', username=request.user.username)
    
    context = {'project': project}
    return render(request, 'HTML/second_pic.html', context)

def user_projects_view(request, username):
    user = get_object_or_404(User, username=username)
    
    drafts = Project.objects.filter(user=user, state='draft')
    finished = Project.objects.filter(user=user, state='finished')
    
    context = {
        'user': user,
        'drafts': drafts,
        'finished': finished,
        'total_drafts': drafts.count(),
        'total_finished': finished.count(),
    }
    return render(request, 'HTML/profile.html', context)