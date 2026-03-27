from django.shortcuts import render, get_object_or_404, redirect
from .models import Creation, Rating
from django.contrib.auth.models import User

def leaderboard_view(request):
    creations = Creation.objects.select_related('user', 'project').all()

    def entry(c, score_key, score_val):
        return {
            'id': c.id,
            'username': c.user.username,
            'title': c.title,
            score_key: score_val,
            'result_image': c.image.url if c.image else None,
            'original_image': c.project.oldPic.url if c.project and c.project.oldPic else None,
        }

    ai_leaderboard = sorted(
        [entry(c, 'score', c.ai_score) for c in creations],
        key=lambda x: x['score'], reverse=True
    )
    user_leaderboard = sorted(
        [entry(c, 'score', c.average_user_score()) for c in creations],
        key=lambda x: x['score'], reverse=True
    )

    for i, e in enumerate(ai_leaderboard):
        e['rank'] = i + 1
    for i, e in enumerate(user_leaderboard):
        e['rank'] = i + 1

    return render(request, 'HTML/leaderboard.html', {
        'ai_leaderboard': ai_leaderboard,
        'user_leaderboard': user_leaderboard,
    })

def rate_creation_view(request, creation_id):
    creation = get_object_or_404(Creation, id=creation_id)
    
    if request.method == 'POST':
        score = request.POST.get('score')
        
        if score is None or not (0 <= float(score) <= 100):
            return render(request, 'HTML/rate_creation.html', {
                'creation': creation,
                'error': 'Оценката трябва да е между 0 и 100'
            })
        
        Rating.objects.update_or_create(
            creation=creation,
            user=request.user,
            defaults={'score': float(score)}
        )
        return redirect('leaderboard')
    
    context = {'creation': creation}
    return render(request, 'HTML/rate_creation.html', context)