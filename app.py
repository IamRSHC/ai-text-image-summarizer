import streamlit as st
from summarizer import summarize_text
from text_cleaner import clean_text

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------
# EXPERT CSS (Polished & Imported)
# ---------------------------------------------------
st.markdown("""
<style>
/* IMPORT FONTS */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #020617; /* Deepest dark for contrast */
}

/* HEADER */
.title {
    font-size: 52px;
    font-weight: 800;
    background: linear-gradient(90deg, #60a5fa, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
}

.subtitle {
    color: #94a3b8;
    margin-top: 10px;
    font-size: 18px;
    font-weight: 400;
}

/* CARDS - Modern Glassy Feel */
.main-card {
    background: #0f172a;
    padding: 30px;
    border-radius: 16px;
    border: 1px solid rgba(148, 163, 184, 0.1); /* Subtle border */
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.summary-card {
    background: #1e293b;
    padding: 25px;
    border-radius: 12px;
    border-left: 4px solid #60a5fa; /* Accent line */
    color: #e2e8f0;
    font-size: 16px;
    line-height: 1.6;
}

/* METRIC CARDS */
.metric-card {
    background: #1e293b;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.metric-label {
    color: #94a3b8;
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.metric-value {
    font-size: 32px;
    font-weight: 700;
    margin: 5px 0 0 0;
}

/* BUTTON OVERRIDE */
.stButton>button {
    background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    color: white;
    border: none;
    padding: 16px;
    font-size: 18px !important;
    font-weight: 600;
    border-radius: 10px;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    box-shadow: 0 0 15px rgba(59, 130, 246, 0.6);
    transform: translateY(-2px);
}

/* INPUT TEXT AREA */
textarea {
    background-color: #1e293b !important;
    color: #f8fafc !important;
    border: 1px solid #334155 !important;
}
textarea:focus {
    border-color: #60a5fa !important;
    box-shadow: 0 0 0 1px #60a5fa !important;
}

/* FOOTER */
.footer {
    text-align: center;
    margin-top: 50px;
    padding-top: 20px;
    border-top: 1px solid #1e293b;
    color: #64748b;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER SECTION
# ---------------------------------------------------
st.markdown("<div class='title'>🧠 AI Summarizer</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Transform long documents into clear, concise insights in seconds.</div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------
# MAIN CONTROL PANEL
# ---------------------------------------------------
# We use a container to wrap inputs for a "Card" look
with st.container():
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    
    # Header inside the card
    c1, c2 = st.columns([4, 1])
    with c1:
        st.subheader("📝 Input Text")
    with c2:
        # Move Length Selector HERE for better UX
        length_option = st.selectbox("", ["Short", "Medium", "Long"], index=1, label_visibility="collapsed")

    user_text = st.text_area(
        "", 
        height=250, 
        placeholder="Paste your article, report, or notes here..."
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Full width button
    generate_btn = st.button("✨ Summarize Text", use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# RESULTS SECTION
# ---------------------------------------------------
if generate_btn:
    if not user_text.strip():
        st.error("Please enter some text to summarize.")
    else:
        with st.spinner("Analyzing text patterns..."):
            cleaned = clean_text(user_text)
            # Map UI options to backend requirements if needed
            summary = summarize_text(cleaned, length_option.lower()) 

        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # 2/3 Split for Summary vs Analytics
        res_col1, res_col2 = st.columns([2, 1])

        # --- LEFT: SUMMARY ---
        with res_col1:
            st.markdown("### 📄 Generated Summary")
            st.markdown(f"<div class='summary-card'>{summary}</div>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                label="📥 Download Summary",
                data=summary,
                file_name="summary.txt",
                mime="text/plain"
            )

        # --- RIGHT: ANALYTICS ---
        with res_col2:
            st.markdown("### 📊 Metrics")
            
            orig_words = len(cleaned.split())
            sum_words = len(summary.split())
            reduction = round(((orig_words - sum_words)/orig_words)*100, 1) if orig_words else 0
            
            # Custom Metric Card Function to keep code clean
            def metric_html(label, value, color_hex):
                return f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value" style="color: {color_hex}">{value}</div>
                </div>
                <br>
                """

            st.markdown(metric_html("Original Words", orig_words, "#94a3b8"), unsafe_allow_html=True)
            st.markdown(metric_html("Summary Words", sum_words, "#60a5fa"), unsafe_allow_html=True)
            
            # Dynamic color for reduction
            red_color = "#34d399" if reduction > 0 else "#f87171" 
            st.markdown(metric_html("Reduction", f"{reduction}%", red_color), unsafe_allow_html=True)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("""
<div class='footer'>
    Microsoft Elevate Capstone Project • Powered by Transformers & Streamlit
</div>
""", unsafe_allow_html=True)