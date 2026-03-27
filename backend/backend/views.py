from django.shortcuts import render
from aiStuff.aiIdeas import giveIdea
import os
from django.conf import settings

def index(request):
    
    image_path = os.path.join(settings.BASE_DIR, 'images', 'testImage1.png')
    print(image_path)
    ai_ideas = giveIdea(image_path, use_mock=False)
    return render(request, 'HTML/index.html')
