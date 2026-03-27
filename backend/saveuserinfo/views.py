from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import UserProfile

@api_view(['GET'])
def get_profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    profile, created = UserProfile.objects.get_or_create(user=user)

    from draftsAndProjects.models import Project
    drafts = Project.objects.filter(user=user, status='draft')
    finished = Project.objects.filter(user=user, status='finished')

    return Response({
        'username': user.username,
        'email': user.email,
        'bio': profile.bio,
        'avatar': request.build_absolute_uri(profile.avatar.url) if profile.avatar else None,
        'drafts': [{'id': p.id, 'title': p.title, 'created_at': p.created_at} for p in drafts],
        'finished': [{'id': p.id, 'title': p.title, 'ai_score': p.ai_score} for p in finished],
        'total_drafts': drafts.count(),
        'total_finished': finished.count(),
    })

@api_view(['PUT'])
def update_profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    profile, created = UserProfile.objects.get_or_create(user=user)

    bio = request.data.get('bio')
    if bio is not None:
        profile.bio = bio

    if 'avatar' in request.FILES:
        profile.avatar = request.FILES['avatar']

    profile.save()
    return Response({'message': 'Profile updated', 'username': user.username, 'bio': profile.bio})