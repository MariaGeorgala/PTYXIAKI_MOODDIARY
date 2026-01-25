import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ---------------------------------------------------------
# ADAPTIVE ΕΡΩΤΗΣΗ (βάσει βήματος + προηγούμενων απαντήσεων)
# ---------------------------------------------------------
def generate_adaptive_question(previous_answers, step, emotion_memory=None):

    prompt = f"""
     εστω οτι Είσαι ένας ήπιος ψυχολογικός βοηθός.

    Προηγούμενες απαντήσεις χρήστη:
    {previous_answers}

    Βήμα ερώτησης: {step}/5
    Συναισθηματικό ιστορικό προηγούμενων ημερών:
    {emotion_memory}

    Δημιούργησε ΜΙΑ σύντομη ερώτηση που:
    - δεν επαναλαμβάνει καποια απο τις προηγούμενες
    - είναι φυσική συνέχεια
    - εμβαθύνει λίγο περισσότερο κάθε φορά
    - αλλάζει θεματική (σκέψεις, σώμα, ενέργεια, σχέσεις, γεγονότα)

    ΕΠΙΣΤΡΕΨΕ ΜΟΝΟ την ερώτηση.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()


# ---------------------------------------------------------
# FOLLOW-UP ΕΡΩΤΗΣΗ (πάνω στην τελευταία απάντηση)
# ---------------------------------------------------------
def generate_followup_question(previous_answers):

    last_answer = previous_answers[-1]

    prompt = f"""
    Ο χρήστης απάντησε:
    "{last_answer}"

    Δημιούργησε ΜΙΑ σύντομη follow-up ερώτηση
    που ζητά λίγο περισσότερη διευκρίνιση απο τον χρηστη.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()


# ---------------------------------------------------------
# ΑΝΑΛΥΣΗ ΣΥΝΑΙΣΘΗΜΑΤΟΣ
# ---------------------------------------------------------
def analyze_conversation_with_llm(answers):

    prompt = f"""
    Ο χρήστης απάντησε:
    {answers}

    Δώσε:
    1. ΚΥΡΙΟ συναίσθημα (ένα μόνο)
    2. Ένταση 1–10

    ΜΟΡΦΗ:
    <συναίσθημα> - <ένταση>
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
