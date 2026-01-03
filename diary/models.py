from django.db import models
from django.contrib.auth.models import User

class MoodEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    response = models.TextField()
    score = models.FloatField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.mood} ({self.date})"


class MoodQuestion(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class UserQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(MoodQuestion, on_delete=models.CASCADE)
    date_assigned = models.DateField()

    class Meta:
        unique_together = ('user', 'date_assigned')

    def __str__(self):
        return f"{self.user.username} - {self.question.text} ({self.date_assigned})"
