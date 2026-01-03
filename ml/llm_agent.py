import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def analyze_conversation_with_llm(answers):
    """
    Στέλνουμε όλες τις απαντήσεις στο LLM και ζητάμε:
    - βασικό συναίσθημα
    - ένταση 1–10
    """

    prompt = f"""
Είσαι σύμβουλος ψυχικής υγείας.

Ο χρήστης απάντησε σε 5 ερωτήσεις. Ανάλυσε όλες τις απαντήσεις
και βρες:

1) Το βασικό συναίσθημα (χαρά, λύπη, θυμός, άγχος, ουδέτερος κ.λπ.)
2) Την ένταση (1–10)

Οι απαντήσεις του χρήστη είναι:

{answers}

Η τελική σου απάντηση να είναι ΜΟΝΟ στη μορφή:

συναίσθημα - αριθμός

Παράδειγμα:
χαρά - 7
"""

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
