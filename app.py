import streamlit as st
from summarizer import summarize_text
from text_cleaner import clean_text

# ---------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------
st.set_page_config(
    page_title="AI Summarizer Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------
# 2. MASTERCLASS CSS SYSTEM
# ---------------------------------------------------
st.markdown("""
<style>
    /* IMPORT FONT - INTER */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* GLOBAL RESET */
    .stApp {
        background-color: #0e1117; /* Deepest Onyx */
        font-family: 'Inter', sans-serif;
    }

    /* --------------------------------------
       TYPOGRAPHY
       -------------------------------------- */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        color: #f8fafc;
    }

    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0px;
        letter-spacing: -1.5px;
        text-shadow: 0 0 40px rgba(99, 102, 241, 0.4);
    }
    
    .accent-text {
        color: #818cf8; /* Indigo 400 */
    }

    .subtitle {
        font-size: 1.2rem;
        color: #94a3b8; /* Slate 400 */
        font-weight: 400;
        margin-bottom: 40px;
    }

    /* --------------------------------------
       INPUT AREA STYLING (THE FIX)
       -------------------------------------- */
    /* Target the text area container */
    .stTextArea textarea {
        background-color: #1e293b !important; /* Slate 800 */
        border: 1px solid #334155 !important;
        border-radius: 12px;
        color: #e2e8f0;
        font-size: 16px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease;
    }

    .stTextArea textarea:focus {
        border-color: #818cf8 !important; /* Indigo Focus */
        box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.2) !important;
    }
    
    /* Remove default top label gap */
    .stTextArea label {
        display: none !important;
    }

    /* --------------------------------------
       BUTTONS
       -------------------------------------- */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        border: none;
        box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.3);
        transition: all 0.2s;
        width: 100%;
        font-size: 1.1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 20px 25px -5px rgba(99, 102, 241, 0.4);
    }

    /* --------------------------------------
       SUMMARY CARD
       -------------------------------------- */
    .result-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 30px;
        color: #e2e8f0;
        line-height: 1.7;
        font-size: 1.05rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        position: relative;
    }
    
    .result-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        border-radius: 16px 16px 0 0;
    }

    /* --------------------------------------
       METRICS
       -------------------------------------- */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #f8fafc !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem !important;
        color: #94a3b8 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* --------------------------------------
       SELECTBOX (Length)
       -------------------------------------- */
    div[data-baseweb="select"] > div {
        background-color: #1e293b !important;
        border-color: #334155 !important;
        color: white !important;
        border-radius: 8px;
    }

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# 3. HEADER SECTION
# ---------------------------------------------------
# Using columns to center align effectively if needed, but keeping it left for modern feel
st.markdown('<div class="main-title">AI <span class="accent-text">Summarizer</span></div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Transform complex documentation into clear, actionable intelligence.</div>', unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------
# 4. INPUT SECTION (The Workspace)
# ---------------------------------------------------
c1, c2 = st.columns([3, 1])

with c2:
    # Controls moved to the side for better ergonomics
    st.markdown("##### ⚙️ Settings")
    length_option = st.selectbox(
        "Summary Detail",
        ["Short", "Medium", "Long"],
        index=1,
        help="Select how detailed you want the summary to be."
    )
    
    # Add some vertical spacing
    st.write("") 
    st.write("") 
    
    generate_btn = st.button("✨ Summarize", use_container_width=True)

with c1:
    st.markdown("##### 📄 Source Text")
    user_text = st.text_area(
        "Input Text", # Hidden by CSS but required for accessibility
        height=300,
        placeholder="Paste your report, article, or raw text here to begin analysis..."
    )

# ---------------------------------------------------
# 5. LOGIC & RESULTS
# ---------------------------------------------------
if generate_btn:
    if not user_text.strip():
        st.toast("⚠️ Please enter some text first!", icon="⚠️")
    else:
        # Progress Bar for UX
        progress_text = "Analyzing text semantics..."
        my_bar = st.progress(0, text=progress_text)
        
        # Simulate processing (remove import time.sleep in prod, just logic here)
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
            st.markdown("### 🧠 Intelligence Output")
            st.markdown(f"""
            <div class="result-card">
                {summary}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Download Button with unique key to prevent reload issues
            st.download_button(
                label="📥 Export Report",
                data=summary,
                file_name="AI_Summary_Report.txt",
                mime="text/plain"
            )

        with r_col2:
            st.markdown("### 📊 Analytics")
            
            # Calculating Metrics
            orig_words = len(cleaned.split())
            sum_words = len(summary.split())
            reduction = round(((orig_words - sum_words)/orig_words)*100, 1) if orig_words else 0
            
            # Using Streamlit Native Metrics for clean alignment
            with st.container(border=True):
                m1, m2 = st.columns(2)
                m1.metric("Original", orig_words)
                m2.metric("Summary", sum_words)
                
                st.divider()
                
                st.metric("Efficiency Gain", f"{reduction}%", delta=f"{reduction}% reduction")

# ---------------------------------------------------
# 6. FOOTER
# ---------------------------------------------------
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #475569; font-size: 0.8rem;">
    Microsoft Elevate Capstone Project &nbsp; • &nbsp; Engineered with Transformers
</div>
""", unsafe_allow_html=True)