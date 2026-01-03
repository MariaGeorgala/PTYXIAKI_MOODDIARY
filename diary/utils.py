import random
from datetime import date
from .models import MoodQuestion, UserQuestion

# ---------------------------------------
# ΤΥΧΑΙΕΣ ΕΡΩΤΗΣΕΙΣ (χρησιμοποιούνται μόνο
# αν δεν υπάρχουν στη βάση)
# ---------------------------------------
QUESTIONS = [
    "Πώς νιώθεις σήμερα;",
    "Τι σε επηρέασε πιο πολύ στη διάθεσή σου σήμερα;",
    "Αν η μέρα σου ήταν χρώμα, ποιο θα ήταν;",
    "Τι θα μπορούσε να κάνει τη μέρα σου καλύτερη;",
    "Πόσο στρες ένιωσες σήμερα; (0–10)",
    "Πόσο συχνά ένιωσες ότι χρειάστηκες διάλειμμα; (1–10)",
    "Έκανες κάτι σήμερα που σε έκανε χαρούμενο;",
    "Πόσο ικανοποιημένος/η είσαι από τη μέρα σου; (1–10)",
]

def get_random_question():
    """Fallback όταν δεν υπάρχουν questions στη βάση."""
    return random.choice(QUESTIONS)

# ---------------------------------------
# Δίνουμε στον χρήστη 1 ερώτηση την ημέρα
# ---------------------------------------
def get_daily_question(user):
    today = date.today()

    # Έχει ήδη ερώτηση σήμερα?
    uq = UserQuestion.objects.filter(user=user, date_assigned=today).first()
    if uq:
        return uq.question

    # Αν δεν έχει – διαλέγουμε από τη βάση
    all_q = list(MoodQuestion.objects.all())
    if not all_q:
        return get_random_question()

    q = random.choice(all_q)

    UserQuestion.objects.create(
        user=user,
        question=q,
        date_assigned=today
    )

    return q
