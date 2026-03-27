from django.db import models
from django.contrib.auth.models import User
from draftsAndProjects.models import Project

class Creation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='creations/')
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    ai_score = models.FloatField(default=0)

    def average_user_score(self):
        ratings = self.ratings.all()
        if not ratings:
            return 0
        return round(sum(r.score for r in ratings) / len(ratings), 2)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

class Rating(models.Model):
    creation = models.ForeignKey(Creation, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['creation', 'user']

    def __str__(self):
        return f"{self.user.username} -> {self.creation.title}: {self.score}"