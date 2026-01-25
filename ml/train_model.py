import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
django.setup()

from diary.models import MoodQuestion

from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch

def load_data():
    questions = MoodQuestion.objects.all()
    texts = [q.text for q in questions]
    return texts

def train_model():
    model_name = "distilgpt2" 
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)

    texts = load_data()

    if not texts:
        print("Δεν βρέθηκαν ερωτήσεις για εκπαίδευση!")
        return

    training_text = "\n\n".join(texts)
    inputs = tokenizer(training_text, return_tensors="pt", truncation=True, max_length=512)

    outputs = model(**inputs, labels=inputs["input_ids"])
    loss = outputs.loss
    loss.backward()

    os.makedirs("./ml/mood_model", exist_ok=True)
    model.save_pretrained("./ml/mood_model")
    tokenizer.save_pretrained("./ml/mood_model")

    print(" Εκπαιδεύτηκε και αποθηκεύτηκε επιτυχώς το μοντέλο!")

if __name__ == "__main__":
    train_model()
