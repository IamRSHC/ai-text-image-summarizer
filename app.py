import streamlit as st
from summarizer import summarize_text
from text_cleaner import clean_text

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="🧠",
    layout="wide"
)

# ---------------------------------------------------
# PREMIUM CSS (Clean + Modern + Submission Ready)
# ---------------------------------------------------
st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* HEADER */
.title {
    font-size:48px;
    font-weight:800;
    color:#60a5fa;
    margin-bottom:0;
}

.subtitle {
    color:#9ca3af;
    margin-top:6px;
    margin-bottom:25px;
    font-size:18px;
}

/* MAIN CARD */
.main-card {
    background:#0f172a;
    padding:30px;
    border-radius:18px;
    box-shadow:0 8px 30px rgba(0,0,0,0.35);
    border:1px solid #1f2937;
}

/* SUMMARY CARD */
.summary-card {
    background:#020617;
    padding:25px;
    border-radius:16px;
    border:1px solid #1f2937;
}

/* METRIC CARDS */
.metric-card {
    background:#020617;
    padding:22px;
    border-radius:14px;
    text-align:center;
    box-shadow:0 6px 18px rgba(0,0,0,0.4);
    border:1px solid #1f2937;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg,#2563eb,#06b6d4);
    color:white;
    border:none;
    padding:14px;
    font-size:16px;
    font-weight:600;
    border-radius:12px;
}

.stButton>button:hover {
    transform:scale(1.02);
}

/* TEXT AREA */
textarea {
    background:#020617 !important;
    color:white !important;
    border-radius:12px !important;
}

/* FOOTER */
.footer {
    text-align:center;
    margin-top:40px;
    color:#6b7280;
    font-size:14px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.markdown("<div class='title'>🧠 AI Text Summarizer</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Paste any text and generate intelligent AI summaries instantly</div>", unsafe_allow_html=True)
st.divider()

# ---------------------------------------------------
# MAIN LAYOUT
# ---------------------------------------------------
left, right = st.columns([3,1])

with right:
    length = st.selectbox("Summary Length", ["short", "medium", "long"])

# ---------------------------------------------------
# INPUT AREA
# ---------------------------------------------------
st.markdown("<div class='main-card'>", unsafe_allow_html=True)
st.subheader("✍️ Enter your text")

user_text = st.text_area(
    "",
    height=220,
    placeholder="Paste your paragraph, article, notes, or documentation here..."
)

generate = st.button("🚀 Generate AI Summary", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# PROCESS
# ---------------------------------------------------
if generate:

    if not user_text.strip():
        st.warning("Please enter some text first.")
        st.stop()

    with st.spinner("AI is analyzing and generating summary..."):
        cleaned = clean_text(user_text)
        summary = summarize_text(cleaned, length)

    st.success("Summary generated successfully")

    # ---------------------------------------------------
    # SUMMARY + ANALYTICS LAYOUT
    # ---------------------------------------------------
    colA, colB = st.columns([2,1])

    # ---------------- SUMMARY ----------------
    with colA:
        st.markdown("## 📌 AI Summary")
        st.markdown("<div class='summary-card'>", unsafe_allow_html=True)
        st.write(summary)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            st.download_button(
                "⬇ Download Summary",
                summary,
                file_name="AI_Summary.txt",
                mime="text/plain",
                use_container_width=True
            )

    # ---------------- ANALYTICS ----------------
    with colB:
        st.markdown("## 📊 Analytics")

        orig_words = len(cleaned.split())
        sum_words = len(summary.split())
        reduction = round(((orig_words - sum_words)/orig_words)*100,2) if orig_words else 0

        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color:#9CA3AF">Original Words</h4>
            <h2 style="color:#60a5fa">{orig_words}</h2>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color:#9CA3AF">Summary Words</h4>
            <h2 style="color:#34d399">{sum_words}</h2>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        color = "#22c55e" if reduction > 0 else "#ef4444"
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color:#9CA3AF">Reduction</h4>
            <h2 style="color:{color}">{reduction}%</h2>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("""
<div class='footer'>
Built using Transformers + Streamlit | Microsoft Elevate Capstone Project
</div>
""", unsafe_allow_html=True)

st.caption("Built with ❤️ using Transformers + Streamlit | Microsoft Elevate Capstone Project")
