from django.shortcuts import render
from aiIdeas import scoreRes, giveIdea
from draftAndProjects.models import Project
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
@login_required


def postFunc(request):
    if request == 'POST':
        image = request.FILES.get('media/waste')
        if image:
            project = Project.objects.create(
            oldPic=image,
            user=request.user,
            state=0 
        )
        image_path = project.oldPic.path
        ai_ideas = giveIdea(image_path, use_mock=True)
        print(ai_ideas)
        return render(request, "frontend/new_with_AI.html", {"ideas": ai_ideas})

    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)

def getRating(request):
    if request == 'POST':
        imageNew = request.FILES.get('uploaded_recycled_image')
        if imageNew:
            if imageNew:
                project = Project.objects.create(
                    oldPic=imageNew,
                    user=request.user,
                    state=0 
                )
                
                return JsonResponse({
                    "status": 1, 
                    "project_id": project.id
                })
