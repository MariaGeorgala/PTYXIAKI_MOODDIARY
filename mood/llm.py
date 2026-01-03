import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------------------------------------------
# 1) ΖΗΤΑΜΕ 5 ΤΥΧΑΙΕΣ ΕΡΩΤΗΣΕΙΣ ΑΠΟ ΤΟ LLM
# ---------------------------------------------------------
def generate_questions():
    prompt = """
    Δημιούργησε 5 σύντομες ερωτήσεις που βοηθούν στην κατανόηση της ψυχολογικής κατάστασης ενός ανθρώπου.
    Οι ερωτήσεις πρέπει να είναι διαφορετικές κάθε φορά.
    Μην εξηγήσεις τίποτα, απάντησε ΜΟΝΟ έτσι:

    1. ...
    2. ...
    3. ...
    4. ...
    5. ...
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.choices[0].message.content.strip()

    # Κάνουμε split σε γραμμές
    lines = text.split("\n")

    # Βγάζουμε τον αριθμό “1. ”
    questions = [line.split(". ", 1)[1] for line in lines]

    return questions


# ---------------------------------------------------------
# 2) ΑΝΑΛΥΣΗ ΑΠΑΝΤΗΣΕΩΝ ΧΡΗΣΤΗ
# ---------------------------------------------------------
def analyze_conversation_with_llm(answers):

    prompt = f"""
    Ο χρήστης απάντησε στις παρακάτω ερωτήσεις:
    {answers}

    Θέλω:

    1. Να αναλύσεις συνολικά τις απαντήσεις.
    2. Να εντοπίσεις το ΚΥΡΙΟ συναίσθημα (επίλεξε ένα):
       χαρά, λύπη, θυμός, άγχος, φόβος, ενθουσιασμός, ηρεμία, απογοήτευση, κόπωση.
    3. Να δώσεις έναν αριθμό έντασης 1–10.
    4. Η τελική απάντηση να είναι ΜΟΝΟ σε αυτή τη μορφή:

       <συναίσθημα> - <ένταση>
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
