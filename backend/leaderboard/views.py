from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Creation, Rating
from django.contrib.auth.models import User

@api_view(['GET'])
def leaderboard(request):
    creations = Creation.objects.all()

    ai_leaderboard = []
    user_leaderboard = []

    for c in creations:
        ai_leaderboard.append({
            'username': c.user.username,
            'title': c.title,
            'ai_score': c.ai_score,
        })
        user_leaderboard.append({
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

    return Response({
        'ai_leaderboard': ai_leaderboard,
        'user_leaderboard': user_leaderboard,
    })

@api_view(['POST'])
def rate_creation(request, creation_id):
    try:
        creation = Creation.objects.get(id=creation_id)
    except Creation.DoesNotExist:
        return Response({'error': 'Creation not found'}, status=status.HTTP_404_NOT_FOUND)

    score = request.data.get('score')
    user_id = request.data.get('user_id')

    if score is None or not (0 <= float(score) <= 100):
        return Response({'error': 'Score must be between 0 and 100'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    rating, created = Rating.objects.update_or_create(
        creation=creation,
        user=user,
        defaults={'score': float(score)}
    )

    return Response({'message': 'Rating saved', 'score': score})