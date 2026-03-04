import streamlit as st
from summarizer import summarize_text
from text_cleaner import clean_text

# ---------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------
st.set_page_config(
    page_title="AI Summarizer | Light",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------
# 2. MASTERCLASS CSS (LIGHT MODE)
# ---------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background-color: #f8fafc;
    font-family: 'Inter', sans-serif;
}

h1, h2, h3 {
    font-family: 'Inter', sans-serif;
    color: #0f172a !important;
}

.main-title {
    font-size: 3.5rem;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 0px;
    letter-spacing: -1.5px;
}

.accent-text {
    background: linear-gradient(135deg,#4f46e5 0%,#7c3aed 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    font-size: 1.2rem;
    color: #64748b;
    font-weight: 400;
    margin-bottom: 40px;
}

.section-header {
    color: #334155;
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 10px;
}

.stTextArea textarea {
    background-color:#ffffff !important;
    border:1px solid #e2e8f0 !important;
    border-radius:12px;
    color:#1e293b;
    font-size:16px;
    padding:20px;
    box-shadow:0 4px 6px -1px rgba(0,0,0,0.05);
}

.stTextArea textarea:focus {
    border-color:#6366f1 !important;
    box-shadow:0 0 0 4px rgba(99,102,241,0.1) !important;
}

.stTextArea label {
    display:none !important;
}

.stButton > button {
    background:linear-gradient(135deg,#4f46e5 0%,#7c3aed 100%);
    color:white;
    font-weight:600;
    padding:0.75rem 1.5rem;
    border-radius:10px;
    border:none;
    width:100%;
    font-size:1.1rem;
}

.result-card {
    background-color:#ffffff;
    border:1px solid #e2e8f0;
    border-radius:16px;
    padding:30px;
    color:#334155;
    line-height:1.7;
    font-size:1.05rem;
    box-shadow:0 10px 15px -3px rgba(0,0,0,0.05);
}

[data-testid="stMetricValue"] {
    font-size:2.2rem !important;
    font-weight:700 !important;
    color:#0f172a !important;
}

[data-testid="stMetricLabel"] {
    font-size:0.85rem !important;
    color:#64748b !important;
    font-weight:600 !important;
}

div[data-baseweb="select"] > div {
    background-color:#ffffff !important;
    border-color:#e2e8f0 !important;
    color:#1e293b !important;
    border-radius:10px;
}

div[data-testid="stMetric"] {
    background-color:#ffffff;
    padding:15px;
    border-radius:10px;
    border:1px solid #e2e8f0;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# 3. HEADER
# ---------------------------------------------------
st.markdown('<div class="main-title">AI <span class="accent-text">Summarizer</span></div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Transform complex documentation into clear, actionable intelligence.</div>', unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------
# 4. INPUT SECTION
# ---------------------------------------------------
c1, c2 = st.columns([3,1])

with c2:
    st.markdown('<div class="section-header">⚙️ Settings</div>', unsafe_allow_html=True)

    length_option = st.selectbox(
        "Summary Detail",
        ["Short","Medium","Long"],
        index=1
    )

    model_option = st.selectbox(
        "AI Model",
        ["Auto","T5 (Fast)","BART (Accurate)"],
        help="Auto automatically selects the best model"
    )

    model_choice = model_option.split()[0]

    st.write("")
    generate_btn = st.button("✨ Summarize", use_container_width=True)

with c1:
    st.markdown('<div class="section-header">📄 Source Text</div>', unsafe_allow_html=True)

    user_text = st.text_area(
        "Input Text",
        height=320,
        placeholder="Paste your report, article, or raw text here to begin analysis..."
    )

# ---------------------------------------------------
# 5. LOGIC
# ---------------------------------------------------
if generate_btn:

    if not user_text.strip():
        st.warning("⚠️ Please enter some text to process.")

    else:
        progress_text = "Analyzing text..."
        my_bar = st.progress(0, text=progress_text)

        cleaned = clean_text(user_text)

        my_bar.progress(50, text="Generating AI summary...")

        summary, model_used = summarize_text(
            cleaned,
            length_option.lower(),
            model_choice.lower()
        )

        my_bar.progress(100, text="Complete!")
        my_bar.empty()

        st.markdown("<br>", unsafe_allow_html=True)

        r_col1, r_col2 = st.columns([2,1])

        with r_col1:
            st.markdown('<div class="section-header">🧠 Intelligence Output</div>', unsafe_allow_html=True)

            st.markdown(f"""
            <div class="result-card">
                {summary}
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            st.download_button(
                label="📥 Export Report",
                data=summary,
                file_name="AI_Summary_Report.txt",
                mime="text/plain"
            )

        with r_col2:
            st.markdown('<div class="section-header">📊 Analytics</div>', unsafe_allow_html=True)

            orig_words = len(cleaned.split())
            sum_words = len(summary.split())
            reduction = round(((orig_words - sum_words)/orig_words)*100,1) if orig_words else 0

            m1, m2 = st.columns(2)

            with m1:
                st.metric("Original", orig_words)

            with m2:
                st.metric("Summary", sum_words)

            st.write("")

            st.metric(
                "Efficiency Gain",
                f"{reduction}%",
                delta=f"{reduction}% reduction"
            )

            st.write("")

            # ✅ MODEL DISPLAY FIX
            st.markdown(f"**🤖 Model Used:** `{model_used}`")

# ---------------------------------------------------
# 6. FOOTER
# ---------------------------------------------------
st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;color:#94a3b8;font-size:0.8rem;">
Microsoft Elevate Capstone Project • Engineered with Transformers
</div>
""", unsafe_allow_html=True)