import streamlit as st
from summarizer import summarize_text
from text_cleaner import clean_text

st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="🧠",
    layout="wide"
)

# ===================== CUSTOM CSS =====================
st.markdown("""
<style>

body {
    background-color:#0e1117;
}

.main-title {
    font-size:48px;
    font-weight:800;
    background: linear-gradient(90deg,#60a5fa,#34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.tagline {
    color:#9ca3af;
    font-size:18px;
    margin-top:-10px;
    margin-bottom:30px;
}

.block-container {
    padding-top:2rem;
}

.card {
    background:#111827;
    padding:28px;
    border-radius:16px;
    box-shadow:0 8px 25px rgba(0,0,0,0.35);
    border:1px solid #1f2937;
}

.metric-card {
    background:#111827;
    padding:25px;
    border-radius:16px;
    text-align:center;
    box-shadow:0 6px 18px rgba(0,0,0,0.35);
    border:1px solid #1f2937;
}

.metric-title {
    color:#9CA3AF;
    font-size:16px;
}

.metric-value {
    font-size:32px;
    font-weight:700;
}

</style>
""", unsafe_allow_html=True)

# ===================== HEADER =====================
st.markdown("<div class='main-title'>🧠 AI Text Summarizer</div>", unsafe_allow_html=True)
st.markdown("<div class='tagline'>Paste any text → Get smart AI summary instantly</div>", unsafe_allow_html=True)

st.divider()

# ===================== TOP SETTINGS =====================
colA, colB = st.columns([3,1])

with colA:
    st.markdown("#### ✏ Enter your text")

with colB:
    length = st.selectbox("Summary Length", ["short", "medium", "long"])

# ===================== INPUT AREA =====================
st.markdown("<div class='card'>", unsafe_allow_html=True)

user_text = st.text_area(
    "",
    height=220,
    placeholder="Paste article, paragraph, research paper, notes..."
)

generate = st.button("🚀 Generate AI Summary", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# ===================== PROCESS =====================
if generate:

    if not user_text.strip():
        st.warning("Please enter text first")
        st.stop()

    with st.spinner("AI is generating smart summary..."):
        cleaned = clean_text(user_text)
        summary = summarize_text(cleaned, length)

    st.success("Summary generated successfully")

    # ===================== OUTPUT LAYOUT =====================
    left, right = st.columns([1.2,1])

    # -------- SUMMARY PANEL --------
    with left:
        st.markdown("### 📌 AI Summary")
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write(summary)
        st.markdown("</div>", unsafe_allow_html=True)

        # download centered
        d1, d2, d3 = st.columns([1,2,1])
        with d2:
            st.download_button(
                "⬇ Download Summary",
                summary,
                file_name="AI_Summary.txt",
                mime="text/plain",
                use_container_width=True
            )

    # -------- ANALYTICS PANEL --------
    with right:
        st.markdown("### 📊 Analytics")

        orig_words = len(cleaned.split())
        sum_words = len(summary.split())
        reduction = round(((orig_words - sum_words) / orig_words) * 100, 2) if orig_words else 0

        m1, m2, m3 = st.columns(3)

        with m1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-title'>Original Words</div>
                <div class='metric-value' style='color:#60a5fa'>{orig_words}</div>
            </div>
            """, unsafe_allow_html=True)

        with m2:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-title'>Summary Words</div>
                <div class='metric-value' style='color:#34d399'>{sum_words}</div>
            </div>
            """, unsafe_allow_html=True)

        color = "#22c55e" if reduction > 0 else "#ef4444"

        with m3:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-title'>Reduction</div>
                <div class='metric-value' style='color:{color}'>{reduction}%</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("Built with ❤️ using Transformers + Streamlit | Microsoft Elevate Capstone Project")
