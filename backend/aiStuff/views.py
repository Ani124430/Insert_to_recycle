from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .aiIdeas import giveIdea, score_reuse_result
from draftsAndProjects.models import Project
from leaderboard.models import Creation


@login_required
def postFunc(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        title = request.POST.get('title', '')
        desc = request.POST.get('desc', '')

        if not image:
            return render(request, 'HTML/newproject.html', {'error': 'Please upload an image.'})

        project = Project.objects.create(
            oldPic=image,
            user=request.user,
            title=title,
            desc=desc,
            state='draft',
        )

        ideas = giveIdea(project.oldPic.path, use_mock=True)
        return render(request, 'HTML/newproject.html', {
            'ideas': ideas,
            'project': project,
        })

    return render(request, 'HTML/newproject.html')


@login_required
def getRating(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)

    if not project.newPic:
        return JsonResponse({'error': 'Project has no finished image yet.'}, status=400)

    result = score_reuse_result(project.oldPic.path, project.newPic.path)

    Creation.objects.create(
        user=request.user,
        title=project.title or f'Project {project.id}',
        image=project.newPic,
        ai_score=result['score'],
    )

    return JsonResponse({'score': result['score'], 'explanation': result['explanation']})
