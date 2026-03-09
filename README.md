# ⚡ NeuralSum — AI-Powered Intelligence Distillation

**NeuralSum** is a professional-grade, high-fidelity AI text summarization platform engineered with state-of-the-art Transformer models. It distills vast amounts of information into precise, actionable intelligence through a polished, "neural-inspired" user experience.

[![Live App](https://img.shields.io/badge/Live_Demo-NeuralSum-63ffc8?style=for-the-badge&logo=streamlit&logoColor=090c14)](https://ai-text-summarizer-dev-rshc.streamlit.app/)
![UI-Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python-Version](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)

---

## 🌐 Live Access
The application is fully deployed and accessible via the web:
### 👉 [Launch NeuralSum App](https://ai-text-summarizer-dev-rshc.streamlit.app/)

---

## 🚀 Key Features

### 🧠 Dual-Model Hybrid Engine
NeuralSum intelligently routes your text based on its complexity:
- **T5 (Fast):** Optimized for inputs under 120 words, providing lightning-fast, concise summaries.
- **BART (Accurate):** Employs `distilbart-cnn-6-6` for long-form content, ensuring high-fidelity extraction and logical coherence.
- **Auto-Logic:** The system automatically switches engines based on word count to balance speed and accuracy.

### 🎨 Elite UI/UX Aesthetic
- **Glassmorphism Design:** A modern, semi-transparent interface with mesh gradients and custom grid patterns.
- **Adaptive Themes:** Seamlessly toggle between **Deep Space Dark** and **Clean Indigo Light** modes.
- **Dynamic Loaders:** Custom CSS/JS-driven animated processing bars that provide visual feedback during inference.
- **Responsive Textarea:** Auto-expanding input area that scales with your content.

### 📊 Advanced Intelligence Analytics
- **Compression Ratio:** Visual progress bars showing exactly how much noise was removed.
- **Word Count Metrics:** Real-time comparison between source text and distilled output.
- **Engine Insights:** Transparent reporting on which AI model was used for the generation.

### 🛠️ Productivity Workflow
- **One-Click Export:** Download your results directly as a `.txt` report.
- **Instant Copy:** High-performance clipboard integration (via custom JS injection to bypass sandbox limitations).
- **Smart Sanitization:** Built-in `text_cleaner` module that removes noise characters and detects garbage/repetitive input.

---

## 🛠️ Technical Stack

- **Frontend:** [Streamlit](https://streamlit.io/) (Extensively customized with CSS/JS injection)
- **NLP Framework:** [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)
- **Deep Learning:** [PyTorch](https://pytorch.org/) (CPU-optimized build)
- **Models:** `google-t5/t5-small`, `sshleifer/distilbart-cnn-6-6`
- **Language:** Python 3.11

---

## 🖥️ Usage Guide

1. **Access:** Open the [Live App](https://ai-text-summarizer-dev-rshc.streamlit.app/).
2. **Paste:** Enter your long-form text (research papers, articles, reports).
3. **Configure:** Select your desired summary length (Short/Medium/Long).
4. **Analyze:** Hit **Run Analysis** and watch the neural distillation in real-time.
5. **Manage:** Use the **Copy** or **Export** buttons to save your results.

---

## ⚙️ Local Development (Optional)

If you wish to run the project locally for development purposes:

### 1. Prerequisites
- Python 3.11+
- Virtual environment (Recommended)

### 2. Setup
```bash
# Clone the repository
git clone https://github.com/your-username/NeuralSum.git
cd NeuralSum

# Install dependencies
pip install -r requirements.txt
```

### 3. Run Locally
```bash
streamlit run app.py
```

---

## 📂 Project Structure

```text
├── app.py              # Main UI & Application Logic
├── summarizer.py       # Transformer Inference & Model Loading
├── text_cleaner.py     # Data Sanitization & Garbage Detection
├── requirements.txt    # Project Dependencies
├── runtime.txt         # Python Runtime Spec
└── ...
```

---

## 🛡️ License & Credits

Developed as part of the **Microsoft Elevate Capstone Project**. Engineered with a focus on modern NLP architectures and high-performance UI design.

*Disclaimer: This tool is for informational purposes. The AI models may occasionally generate inaccuracies or omit nuances found in the source text.*
