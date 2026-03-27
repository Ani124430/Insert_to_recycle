from django.shortcuts import render, get_object_or_404, redirect
from .models import Creation, Rating
from django.contrib.auth.models import User

def leaderboard_view(request):
    creations = Creation.objects.all()

    ai_leaderboard = []
    user_leaderboard = []

    for c in creations:
        ai_leaderboard.append({
            'id': c.id,
            'username': c.user.username,
            'title': c.title,
            'ai_score': c.ai_score,
        })
        user_leaderboard.append({
            'id': c.id,
            'username': c.user.username,
            'title': c.title,
            'user_score': c.average_user_score(),
        })

    ai_leaderboard = sorted(ai_leaderboard, key=lambda x: x['ai_score'], reverse=True)
    user_leaderboard = sorted(user_leaderboard, key=lambda x: x['user_score'], reverse=True)

    for i, entry in enumerate(ai_leaderboard):
        entry['rank'] = i + 1
    for i, entry in enumerate(user_leaderboard):
        entry['rank'] = i + 1

    context = {
        'ai_leaderboard': ai_leaderboard,
        'user_leaderboard': user_leaderboard,
    }
    return render(request, 'HTML/leaderboard.html', context)

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