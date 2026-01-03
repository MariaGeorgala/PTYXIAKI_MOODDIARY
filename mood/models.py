from django.db import models
from django.contrib.auth.models import User

class MoodEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mood_entries")  # Σύνδεση με τον χρήστη
    mood = models.CharField(max_length=50)  # Συναισθηματική κατάσταση
    notes = models.TextField(blank=True, null=True)  # Προαιρετικές σημειώσεις
    created_at = models.DateTimeField(auto_now_add=True)  # Ημερομηνία καταχώρησης

    def __str__(self):
        return f"{self.user.username} - {self.mood} ({self.created_at})"
