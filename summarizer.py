from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re

MODEL_NAME = "t5-small"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)



# ---------- HEAVY OCR CLEANING ----------
def smart_clean(text):
    text = text.replace("\n", " ")

    # remove weird OCR symbols
    text = re.sub(r"[^a-zA-Z0-9.,!?%()\-:; ]+", " ", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text)

    # fix OCR mistakes
    text = text.replace(" al ", " AI ")
    text = text.replace(" Al ", " AI ")
    text = text.replace(" are al", " are AI")
    text = text.replace(" Self are", " Self aware")

    return text.strip()


# ---------- CONVERT BULLETS → SENTENCES ----------
def structure_ocr_text(text):
    """
    Converts broken OCR bullet text into readable paragraph
    """
    lines = text.split(". ")

    # If text has many short broken words → treat as bullet list
    if len(text.split()) < 80 and "\n" in text:
        words = text.replace("\n", " ").split()
        return " ".join(words)

    return text


# ---------- MAIN SUMMARIZER ----------
def summarize_text(text, length="medium"):

    text = smart_clean(text)
    text = structure_ocr_text(text)

    if len(text.split()) < 25:
        return "Text too short to summarize properly."

    if length == "short":
        max_len = 60
        min_len = 20
    elif length == "long":
        max_len = 180
        min_len = 80
    else:
        max_len = 120
        min_len = 40

    prompt = "Summarize clearly in simple sentences: " + text

    inputs = tokenizer.encode(
        prompt,
        return_tensors="pt",
        max_length=512,
        truncation=True
    )

    summary_ids = model.generate(
        inputs,
        max_length=max_len,
        min_length=min_len,
        num_beams=6,
        length_penalty=2.2,
        no_repeat_ngram_size=3,
        early_stopping=True
    )

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary
