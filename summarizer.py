from transformers import pipeline
from text_cleaner import clean_text, is_garbage_input


class TextSummarizer:

    def __init__(self):

        # Load models once
        self.bart = pipeline(
            "summarization",
            model="facebook/bart-large-cnn"
        )

        self.t5 = pipeline(
            "summarization",
            model="t5-small"
        )

    def summarize(self, text, model="auto", detail="medium"):

        text = clean_text(text)

        if is_garbage_input(text):
            return "Input text is too short for meaningful summarization.", "None"

        words = len(text.split())

        # ----------------------------
        # Dynamic Length Control
        # ----------------------------

        if detail == "short":
            max_len = int(words * 0.35)
            min_len = int(words * 0.15)

        elif detail == "medium":
            max_len = int(words * 0.55)
            min_len = int(words * 0.25)

        else:
            max_len = int(words * 0.75)
            min_len = int(words * 0.40)

        max_len = max(20, min(max_len, 200))
        min_len = max(10, min(min_len, max_len - 5))

        # ----------------------------
        # Model Selection
        # ----------------------------

        if model == "bart":
            summarizer = self.bart
            model_used = "🧠 BART (Accurate)"
            text = "summarize: " + text

        elif model == "t5":
            summarizer = self.t5
            model_used = "⚡ T5 (Fast)"
            text = "summarize: " + text

        else:
            if words > 120:
                summarizer = self.bart
                model_used = "⚙️ Auto → BART"
            else:
                summarizer = self.t5
                model_used = "⚙️ Auto → T5"

            text = "summarize: " + text

        summary = summarizer(
            text,
            max_length=max_len,
            min_length=min_len,
            do_sample=False,
            repetition_penalty=1.3,
            no_repeat_ngram_size=3,
            early_stopping=True
        )[0]["summary_text"]

        summary = summary.strip()

        if summary:
            summary = summary[0].upper() + summary[1:]

        return summary, model_used


# -----------------------------------
# GLOBAL INSTANCE
# -----------------------------------

summarizer = TextSummarizer()


def summarize_text(text, detail="medium", model="auto"):

    summary, model_used = summarizer.summarize(text, model, detail)

    return summary, model_used