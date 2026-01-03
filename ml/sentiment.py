from transformers import pipeline

# Δημιουργία sentiment pipeline με προεπιλεγμένο μοντέλο
sentiment_pipeline = pipeline("sentiment-analysis")

def analyze_mood_from_text(text):
    result = sentiment_pipeline(text)[0]
    label = result["label"]
    score = result["score"]

    if label == "POSITIVE":
        mood = "Χαρούμενος 😊"
        comment = "Φαίνεται ότι έχεις θετική διάθεση σήμερα!"
    elif label == "NEGATIVE":
        mood = "Λυπημένος 😢"
        comment = "Μήπως κάτι σε προβληματίζει σήμερα;"
    else:
        mood = "Ουδέτερος 😐"
        comment = "Ούτε πολύ θετικό ούτε πολύ αρνητικό. Ενδιαφέρον!"

    return mood, comment, score
