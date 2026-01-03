from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from .models import MoodEntry
from mood.llm import analyze_conversation_with_llm, generate_questions


# ---------------- HOME ----------------
def home(request):
    return render(request, "diary/home.html")


# ---------------- LOG MOOD ----------------
@login_required
def log_mood(request):

    # 🟢 Αν δεν υπάρχει session → αρχικοποίηση
    if "answers" not in request.session:
        request.session["answers"] = []
        request.session["question_index"] = 0
        request.session["questions"] = generate_questions()  #na tiponei erotiseis gia na dei an einai 5

    answers = request.session["answers"]
    index = request.session["question_index"]
    questions = request.session["questions"]

    # 🟢 Αν ο χρήστης απαντήσει
    if request.method == "POST":
        answer = request.POST.get("response")

        if not answer:
            return render(request, "diary/log_mood.html", {
                "question": questions[index],
                "error": "Παρακαλώ γράψτε μια απάντηση."
            })

        answers.append(answer)
        request.session["answers"] = answers
        request.session["question_index"] = index + 1

        # 🟢 Όταν συμπληρωθούν 5 απαντήσεις
        if len(answers) >= 5:
            result = analyze_conversation_with_llm(answers)

            emotion = result.split("-")[0].strip()
            score = int(result.split("-")[1].strip())

            MoodEntry.objects.create(
                user=request.user,
                mood=emotion,
                score=score,
                response=str(answers)
            )

            # καθαρισμός session
            for key in ["answers", "question_index", "questions"]:
                request.session.pop(key, None)

            return render(request, "diary/result.html", {
                "result": result,
                "emotion": emotion,
                "score": score
            })

    # 🟢 Ασφάλεια: αν index ξεφύγει
    if index >= len(questions):
        request.session["question_index"] = 0
        index = 0

    question = questions[index]

    return render(request, "diary/log_mood.html", {
        "question": question
    })


# ---------------- HISTORY ----------------
@login_required
def history_view(request):
    entries = MoodEntry.objects.filter(user=request.user).order_by("-date")
    return render(request, "diary/history.html", {"entries": entries})


# ---------------- STATS ----------------
@login_required
def stats_view(request):
    entries = MoodEntry.objects.filter(user=request.user)

    avg_score = entries.aggregate(Avg("score"))["score__avg"]
    mood_counts = entries.values("mood").annotate(total=Count("mood"))

    return render(request, "diary/stats.html", {
        "avg_score": avg_score,
        "mood_counts": mood_counts,
        "entries": entries
    })

@login_required
def history_view(request):
    entries = MoodEntry.objects.filter(
        user=request.user
    ).order_by("-date")

    return render(request, "diary/history.html", {
        "entries": entries
    })
