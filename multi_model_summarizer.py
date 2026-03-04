from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# -------------------------
# LOAD T5 MODEL
# -------------------------
t5_tokenizer = AutoTokenizer.from_pretrained("t5-small")
t5_model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")

# -------------------------
# LOAD BART MODEL
# -------------------------
bart_tokenizer = AutoTokenizer.from_pretrained("facebook/bart-base")
bart_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-base")


def summarize_text(text, length="medium", model_choice="Auto"):

    word_count = len(text.split())

    # -------------------------
    # AUTO MODEL SELECTION
    # -------------------------
    if model_choice == "Auto":
        if word_count < 200:
            model_choice = "T5"
        else:
            model_choice = "BART"

    # -------------------------
    # SUMMARY LENGTH CONTROL
    # -------------------------
    if length == "short":
        max_len = 60
        min_len = 20
    elif length == "long":
        max_len = 180
        min_len = 80
    else:
        max_len = 120
        min_len = 40

    # =========================
    # T5 SUMMARIZATION
    # =========================
    if model_choice == "T5":

        input_text = "summarize: " + text

        inputs = t5_tokenizer.encode(
            input_text,
            return_tensors="pt",
            max_length=512,
            truncation=True
        )

        summary_ids = t5_model.generate(
            inputs,
            max_length=max_len,
            min_length=min_len,
            num_beams=4,
            length_penalty=2.0,
            early_stopping=True
        )

        summary = t5_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # =========================
    # BART SUMMARIZATION
    # =========================
    else:

        inputs = bart_tokenizer.encode(
            text,
            return_tensors="pt",
            max_length=1024,
            truncation=True
        )

        summary_ids = bart_model.generate(
            inputs,
            max_length=max_len,
            min_length=min_len,
            num_beams=4,
            length_penalty=2.0,
            early_stopping=True
        )

        summary = bart_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary