from django.contrib import admin
from .models import MoodEntry  # Αν έχεις κάποιο μοντέλο όπως το MoodEntry

admin.site.register(MoodEntry)  # Κάνε register το μοντέλο σου
