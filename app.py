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
    /* IMPORT FONT - INTER */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* GLOBAL RESET */
    .stApp {
        background-color: #f8fafc; /* Very light slate background */
        font-family: 'Inter', sans-serif;
    }

    /* --------------------------------------
       TYPOGRAPHY
       -------------------------------------- */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        color: #0f172a !important; /* Slate 900 */
    }

    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0px;
        letter-spacing: -1.5px;
    }
    
    .accent-text {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        font-size: 1.2rem;
        color: #64748b; /* Slate 500 */
        font-weight: 400;
        margin-bottom: 40px;
    }
    
    .section-header {
        color: #334155;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 10px;
    }

    /* --------------------------------------
       INPUT AREA STYLING (Clean White)
       -------------------------------------- */
    /* Target the text area container */
    .stTextArea textarea {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important; /* Light border */
        border-radius: 12px;
        color: #1e293b; /* Dark text */
        font-size: 16px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); /* Soft shadow */
        transition: all 0.2s ease;
    }

    .stTextArea textarea:focus {
        border-color: #6366f1 !important; /* Indigo Focus */
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1) !important; /* Soft glow ring */
    }
    
    /* Remove default label space */
    .stTextArea label {
        display: none !important;
    }

    /* --------------------------------------
       BUTTONS
       -------------------------------------- */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); /* Indigo to Purple */
        color: white;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2);
        transition: all 0.2s;
        width: 100%;
        font-size: 1.1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.3);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
    }

    /* --------------------------------------
       RESULT CARD
       -------------------------------------- */
    .result-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 30px;
        color: #334155; /* Slate 700 */
        line-height: 1.7;
        font-size: 1.05rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05); /* Elevated look */
        position: relative;
    }
    
    .result-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 6px;
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        border-radius: 16px 16px 0 0;
    }

    /* --------------------------------------
       METRICS (FORCE DARK TEXT)
       -------------------------------------- */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #0f172a !important; /* Slate 900 */
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        color: #64748b !important; /* Slate 500 */
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* --------------------------------------
       SELECTBOX & UI ELEMENTS
       -------------------------------------- */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border-color: #e2e8f0 !important;
        color: #1e293b !important;
        border-radius: 10px;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    }
    
    /* Metric container background */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.02);
    }

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# 3. HEADER SECTION
# ---------------------------------------------------
st.markdown('<div class="main-title">AI <span class="accent-text">Summarizer</span></div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Transform complex documentation into clear, actionable intelligence.</div>', unsafe_allow_html=True)

st.divider()

# ---------------------------------------------------
# 4. INPUT SECTION (The Workspace)
# ---------------------------------------------------
c1, c2 = st.columns([3, 1])

with c2:
    # CONTROLS
    st.markdown('<div class="section-header">⚙️ Settings</div>', unsafe_allow_html=True)
    
    length_option = st.selectbox(
        "Summary Detail",
        ["Short", "Medium", "Long"],
        index=1,
        help="Select how detailed you want the summary to be."
    )
    
    st.write("") 
    st.write("") 
    
    generate_btn = st.button("✨ Summarize", use_container_width=True)

with c1:
    # INPUT
    st.markdown('<div class="section-header">📄 Source Text</div>', unsafe_allow_html=True)
    user_text = st.text_area(
        "Input Text",
        height=320,
        placeholder="Paste your report, article, or raw text here to begin analysis..."
    )

# ---------------------------------------------------
# 5. LOGIC & RESULTS
# ---------------------------------------------------
if generate_btn:
    if not user_text.strip():
        st.warning("⚠️ Please enter some text to process.")
    else:
        # Progress Bar
        progress_text = "Analyzing text semantics..."
        my_bar = st.progress(0, text=progress_text)
        
        # PROCESSING
        cleaned = clean_text(user_text)
        my_bar.progress(50, text="Generating natural language summary...")
        
        summary = summarize_text(cleaned, length_option.lower()) 
        my_bar.progress(100, text="Complete!")
        my_bar.empty()

        st.markdown("<br>", unsafe_allow_html=True)
        
        # ---------------------------------------------------
        # RESULT LAYOUT
        # ---------------------------------------------------
        r_col1, r_col2 = st.columns([2, 1])

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
            
            # Metrics Logic
            orig_words = len(cleaned.split())
            sum_words = len(summary.split())
            reduction = round(((orig_words - sum_words)/orig_words)*100, 1) if orig_words else 0
            
            # Metric Layout
            m1, m2 = st.columns(2)
            with m1:
                st.metric("Original", orig_words)
            with m2:
                st.metric("Summary", sum_words)
            
            st.write("")
            st.metric("Efficiency Gain", f"{reduction}%", delta=f"{reduction}% reduction")

# ---------------------------------------------------
# 6. FOOTER
# ---------------------------------------------------
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 0.8rem;">
    Microsoft Elevate Capstone Project &nbsp; • &nbsp; Engineered with Transformers
</div>
""", unsafe_allow_html=True)