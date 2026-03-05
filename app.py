# ╔══════════════════════════════════════════════════════════════════╗
# ║  NeuralSum — app.py  (UI/UX polish + copy/export fix pass)     ║
# ║                                                                  ║
# ║  ISSUE 1  Column ratio         → already [3,1] ✓               ║
# ║  ISSUE 2  Word counter layout  → clean flex, no duplicate pill  ║
# ║  ISSUE 3  Export + Copy group  → both inside result card footer ║
# ║  ISSUE 4  Copy button broken   → onclick stripped by Streamlit  ║
# ║            sanitizer (bleach); fixed via components.html inject ║
# ║  ISSUE 5  Config header card   → removed heavy wrapper          ║
# ║  ISSUE 6  Model logic opacity  → reduced to ghost-hint level    ║
# ║  ISSUE 7  Bar height           → already 5px ✓                  ║
# ║  ISSUE 8  Hero spacing         → padding reduced ~30%           ║
# ║  ISSUE 9  Grid light mode      → opacity 0.035→0.015            ║
# ║  FUNC     Word counter unified → orig_words from user_text      ║
# ╚══════════════════════════════════════════════════════════════════╝

import html as _html
import streamlit as st
import streamlit.components.v1 as components
from summarizer import summarize_text
from text_cleaner import clean_text

# ---------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------
st.set_page_config(
    page_title="NeuralSum · AI Summarizer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------
# 2. THEME STATE
# ---------------------------------------------------
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

is_dark = st.session_state.theme == "dark"

# ---------------------------------------------------
# 3. THEME VARIABLES
# ---------------------------------------------------
T = {
    # ── BACKGROUNDS ────────────────────────────────────────────────────────
    "app_bg":          "#090c14"                    if is_dark else "#f5f3ff",
    "textarea_bg":     "#111622"                    if is_dark else "#ffffff",
    "textarea_border": "rgba(255,255,255,0.10)"     if is_dark else "rgba(79,70,229,0.20)",
    "settings_bg":     "#0d1119"                    if is_dark else "#ffffff",
    "select_bg":       "#111622"                    if is_dark else "#f5f3ff",
    "select_border":   "rgba(255,255,255,0.09)"     if is_dark else "rgba(79,70,229,0.15)",
    "popover_bg":      "#141824"                    if is_dark else "#ffffff",
    "metric_bg":       "rgba(255,255,255,0.03)"     if is_dark else "rgba(79,70,229,0.05)",
    "metric_border":   "rgba(255,255,255,0.06)"     if is_dark else "rgba(79,70,229,0.14)",
    "card_border":     "rgba(255,255,255,0.07)"     if is_dark else "rgba(79,70,229,0.14)",
    "settings_border": "rgba(255,255,255,0.06)"     if is_dark else "rgba(79,70,229,0.12)",
    "pill_bg":         "rgba(255,255,255,0.04)"     if is_dark else "rgba(79,70,229,0.07)",
    "pill_border":     "rgba(255,255,255,0.07)"     if is_dark else "rgba(79,70,229,0.16)",
    "toggle_bg":       "#0d1119"                    if is_dark else "#ffffff",
    # ── TEXT ───────────────────────────────────────────────────────────────
    "text_primary":    "#ffffff"                    if is_dark else "#1e1b4b",
    "text_secondary":  "rgba(255,255,255,0.42)"     if is_dark else "rgba(49,46,129,0.65)",
    "text_muted":      "rgba(255,255,255,0.22)"     if is_dark else "rgba(49,46,129,0.50)",
    "text_label":      "rgba(255,255,255,0.28)"     if is_dark else "rgba(79,70,229,0.65)",
    "placeholder":     "rgba(255,255,255,0.18)"     if is_dark else "rgba(79,70,229,0.30)",
    "textarea_text":   "rgba(255,255,255,0.88)"     if is_dark else "#1e1b4b",
    "select_text":     "rgba(255,255,255,0.75)"     if is_dark else "#312e81",
    "select_icon":     "rgba(255,255,255,0.35)"     if is_dark else "rgba(79,70,229,0.55)",
    "opt_text":        "rgba(255,255,255,0.70)"     if is_dark else "rgba(49,46,129,0.85)",
    # ── RESULT CARD ────────────────────────────────────────────────────────
    "result_bg":       "rgba(99,255,200,0.03)"      if is_dark else "rgba(79,70,229,0.04)",
    "result_border":   "rgba(99,255,200,0.12)"      if is_dark else "rgba(79,70,229,0.20)",
    "result_text":     "rgba(255,255,255,0.82)"     if is_dark else "#1e1b4b",
    # ── STRUCTURE / MESH ───────────────────────────────────────────────────
    "grid":            "rgba(255,255,255,0.018)"    if is_dark else "rgba(79,70,229,0.015)",
    #                                                                       ↑ ISSUE 9 — was 0.035
    "mesh1":           "rgba(99,255,200,0.07)"      if is_dark else "rgba(79,70,229,0.07)",
    "mesh2":           "rgba(120,80,255,0.09)"      if is_dark else "rgba(124,58,237,0.07)",
    "mesh3":           "rgba(0,180,255,0.06)"       if is_dark else "rgba(192,38,211,0.05)",
    "divider_mid":     "rgba(99,255,200,0.15)"      if is_dark else "rgba(79,70,229,0.30)",
    "divider_side":    "rgba(255,255,255,0.04)"     if is_dark else "rgba(79,70,229,0.06)",
    "footer_border":   "rgba(255,255,255,0.04)"     if is_dark else "rgba(79,70,229,0.10)",
    "footer_text":     "rgba(255,255,255,0.15)"     if is_dark else "rgba(79,70,229,0.38)",
    "compress_sub":    "rgba(255,255,255,0.22)"     if is_dark else "rgba(49,46,129,0.48)",
    # ── BADGE / TIPS — ISSUE 6: reduced to ghost-hint level ───────────────
    "badge_bg":        "rgba(99,255,200,0.02)"      if is_dark else "rgba(79,70,229,0.03)",
    "badge_border":    "rgba(99,255,200,0.06)"      if is_dark else "rgba(79,70,229,0.10)",
    "tip_label":       "rgba(99,255,200,0.35)"      if is_dark else "rgba(79,70,229,0.55)",
    "tip_bold":        "rgba(255,255,255,0.30)"     if is_dark else "rgba(30,27,75,0.50)",
    # ── ACCENT PALETTE ─────────────────────────────────────────────────────
    "accent":          "#63ffc8"                    if is_dark else "#4f46e5",
    "accent_blue":     "#3b82f6"                    if is_dark else "#7c3aed",
    "accent_purple":   "#a78bfa"                    if is_dark else "#c026d3",
    # ── COPY BUTTON — ISSUE 4: visible, clickable-looking ─────────────────
    # dark  → mint border at 35% opacity + subtle mint tint bg
    # light → indigo border at 35% opacity + subtle indigo tint bg
    "copy_border":     "rgba(99,255,200,0.35)"      if is_dark else "rgba(79,70,229,0.35)",
    "copy_bg":         "rgba(99,255,200,0.05)"      if is_dark else "rgba(79,70,229,0.05)",
    "copy_text":       "rgba(99,255,200,0.75)"      if is_dark else "rgba(79,70,229,0.75)",
    # ── SEMANTIC EXTRAS ────────────────────────────────────────────────────
    "btn_text":        "#050810"                    if is_dark else "#ffffff",
    "engine_bg":       "rgba(59,130,246,0.08)"      if is_dark else "rgba(79,70,229,0.07)",
    "engine_border":   "rgba(59,130,246,0.18)"      if is_dark else "rgba(79,70,229,0.20)",
    "engine_dot":      "#3b82f6"                    if is_dark else "#4f46e5",
    "engine_val":      "#7dd3fc"                    if is_dark else "#4f46e5",
}

# ---------------------------------------------------
# 3b. Model lookup tables
# ---------------------------------------------------
_MODEL_LABEL_TO_KEY = {
    "Auto":            "auto",
    "T5 (Fast)":       "t5",
    "BART (Accurate)": "bart",
}
_MODEL_KEY_TO_DISPLAY = {
    "auto": "Auto \u2192 BART",   # ISSUE minor: proper spaced arrow
    "t5":   "T5 (Fast)",
    "bart": "BART (Accurate)",
}

# ---------------------------------------------------
# 4. PRE-BUILD BLOCK LOADER HTML
# ---------------------------------------------------
_bar_heights = [10, 16, 22, 10, 16, 22, 10, 16, 22, 10, 16, 22, 10, 16, 22, 10]
_grad        = "linear-gradient(180deg,#63ffc8,#3b82f6)"
_bar_style   = "flex:1;border-radius:2px;transform-origin:bottom;background:" + _grad + ";"

_bars_dim = "".join(
    '<div style="' + _bar_style
    + f'height:{_bar_heights[i]}px;opacity:0.12;'
    + f'animation:blockFill 0.4s ease {round(i * 0.07, 3)}s infinite alternate;"></div>'
    for i in range(16)
)
_bars_mid = "".join(
    '<div style="' + _bar_style
    + f'height:{_bar_heights[i]}px;'
    + ('opacity:0.95;' if i < 8 else
       f'opacity:0.12;animation:blockFill 0.4s ease {round((i-8)*0.07,3)}s infinite alternate;')
    + '"></div>'
    for i in range(16)
)

_lbl   = ("font-family:'Syne',sans-serif;font-size:0.60rem;font-weight:700;"
          "letter-spacing:0.18em;text-transform:uppercase;"
          "margin-bottom:10px;display:flex;align-items:center;gap:8px;")
_lline = '<span style="width:10px;height:1px;background:#63ffc855;display:inline-block;"></span>'
_brow  = "display:flex;gap:4px;align-items:flex-end;height:28px;"

LOADER_PHASE1 = (
    '<div style="margin-top:18px;margin-bottom:4px;">'
    + '<div style="' + _lbl + 'color:#63ffc899;">' + _lline + "Processing" + _lline + '</div>'
    + '<div style="' + _brow + '">' + _bars_dim + '</div></div>'
)
LOADER_PHASE2 = (
    '<div style="margin-top:18px;margin-bottom:4px;">'
    + '<div style="' + _lbl + 'color:#63ffc8cc;">' + _lline + "Generating Summary" + _lline + '</div>'
    + '<div style="' + _brow + '">' + _bars_mid + '</div></div>'
)

# ---------------------------------------------------
# 5. CSS
# ---------------------------------------------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap');

*, *::before, *::after {{ box-sizing: border-box; }}

html, body, .stApp {{
    background-color: {T['app_bg']} !important;
    font-family: 'DM Sans', sans-serif;
}}

.stApp {{
    position:   relative;
    min-height: 100vh;
    overflow-x: hidden;
}}

.stApp::before {{
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 10%  0%,  {T['mesh1']} 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 90% 10%,  {T['mesh2']} 0%, transparent 55%),
        radial-gradient(ellipse 50% 40% at 50% 90%,  {T['mesh3']} 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}}

/* ISSUE 9 — grid opacity reduced in light mode via T['grid'] token above */
.stApp::after {{
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient({T['grid']} 1px, transparent 1px),
        linear-gradient(90deg, {T['grid']} 1px, transparent 1px);
    background-size: 60px 60px;
    pointer-events: none;
    z-index: 0;
}}

section.main > div,
[data-testid="stAppViewContainer"] > .main {{
    position: relative;
    z-index: 1;
}}

#MainMenu, footer, header {{ visibility: hidden !important; }}
[data-testid="collapsedControl"] {{ display: none !important; }}
.stDeployButton {{ display: none !important; }}

::-webkit-scrollbar {{ width: 4px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: {T['accent']}55; border-radius: 2px; }}

.block-container {{
    padding:   0 2rem !important;
    max-width: 1300px !important;
}}
[data-testid="column"] {{ padding: 0 10px !important; }}

/* ── TEXTAREA ─────────────────────────────────────────── */
.stTextArea > div,
.stTextArea > div > div,
.stTextArea > div > div > div,
[data-baseweb="textarea"],
[data-baseweb="textarea"] > div,
[data-baseweb="base-input"],
[data-baseweb="base-input"] > div {{
    background:       {T['textarea_bg']} !important;
    background-color: {T['textarea_bg']} !important;
    border:           none !important;
    box-shadow:       none !important;
}}

.stTextArea textarea {{
    background:         {T['textarea_bg']} !important;
    background-color:   {T['textarea_bg']} !important;
    border:             1px solid {T['textarea_border']} !important;
    border-radius:      14px !important;
    color:              {T['textarea_text']} !important;
    font-family:        'DM Sans', sans-serif !important;
    font-size:          0.97rem !important;
    font-weight:        300 !important;
    line-height:        1.8 !important;
    padding:            22px 24px !important;   /* ISSUE minor: 24px padding */
    caret-color:        {T['accent']} !important;
    resize:             none !important;
    overflow-y:         hidden !important;
    box-shadow:         none !important;
    outline:            none !important;
    -webkit-box-shadow: none !important;
    -webkit-appearance: none !important;
    min-height:         220px !important;
    transition:         border-color 0.25s ease, box-shadow 0.25s ease !important;
}}

.stTextArea textarea::placeholder {{
    color:       {T['placeholder']} !important;
    font-style:  italic !important;
    font-weight: 300 !important;
}}

.stTextArea textarea:focus {{
    border-color:       {T['accent']}55 !important;
    box-shadow:         0 0 0 3px {T['accent']}0f !important;
    outline:            none !important;
    -webkit-box-shadow: 0 0 0 3px {T['accent']}0f !important;
}}

.stTextArea textarea:invalid,
.stTextArea textarea:required,
.stTextArea textarea:-moz-ui-invalid {{
    box-shadow:         none !important;
    -webkit-box-shadow: none !important;
    border-color:       {T['textarea_border']} !important;
    outline:            none !important;
}}

.stTextArea label {{ display: none !important; }}

/* ── SELECTBOX ────────────────────────────────────────── */
div[data-baseweb="select"] > div {{
    background-color: {T['select_bg']} !important;
    border-color:     {T['select_border']} !important;
    border-radius:    10px !important;
    color:            {T['select_text']} !important;
    font-family:      'DM Sans', sans-serif !important;
    font-size:        0.9rem !important;
}}

div[data-baseweb="select"] > div:hover {{
    border-color: {T['accent']}44 !important;
}}

div[data-baseweb="select"] svg {{ color: {T['select_icon']} !important; }}

[data-baseweb="popover"], [data-baseweb="menu"] {{
    background:    {T['popover_bg']} !important;
    border:        1px solid {T['select_border']} !important;
    border-radius: 10px !important;
}}

[role="option"] {{
    color:            {T['opt_text']} !important;
    font-family:      'DM Sans', sans-serif !important;
    font-size:        0.88rem !important;
    background-color: {T['popover_bg']} !important;
}}

[role="option"]:hover, [aria-selected="true"] {{
    background-color: {T['accent']}14 !important;
    color:            {T['accent']} !important;
}}

.stSelectbox label {{
    font-family:    'DM Sans', sans-serif !important;
    font-size:      0.72rem !important;
    font-weight:    600 !important;
    color:          {T['text_label']} !important;
    letter-spacing: 0.10em !important;
    text-transform: uppercase !important;
    margin-bottom:  2px !important;
}}

/* ── RUN ANALYSIS BUTTON ──────────────────────────────── */
.stButton > button {{
    background:     linear-gradient(135deg, {T['accent']} 0%, {T['accent_blue']} 100%) !important;
    color:          {T['btn_text']} !important;
    font-family:    'Syne', sans-serif !important;
    font-weight:    800 !important;
    font-size:      0.82rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    padding:        0.82rem 1.5rem !important;
    border-radius:  12px !important;
    border:         none !important;
    width:          100% !important;
    cursor:         pointer !important;
    box-shadow:     0 2px 22px {T['accent']}35, 0 1px 0 rgba(255,255,255,0.15) inset !important;
    transition:     transform 0.18s ease, box-shadow 0.18s ease !important;
}}

.stButton > button:hover {{
    transform:  translateY(-2px) !important;
    box-shadow: 0 8px 30px {T['accent']}55 !important;
}}

.stButton > button:active {{
    transform: translateY(0) !important;
}}

/* ── METRICS ──────────────────────────────────────────── */
div[data-testid="stMetric"] {{
    background:    {T['metric_bg']} !important;
    border:        1px solid {T['metric_border']} !important;
    border-radius: 14px !important;
    padding:       18px 20px !important;
}}

div[data-testid="stMetric"]:hover {{
    border-color: {T['accent']}22 !important;
}}

[data-testid="stMetricValue"] {{
    font-family:    'Syne', sans-serif !important;
    font-size:      1.9rem !important;
    font-weight:    800 !important;
    color:          {T['text_primary']} !important;
    letter-spacing: -1px !important;
}}

[data-testid="stMetricLabel"] {{
    font-size:      0.70rem !important;
    font-weight:    600 !important;
    color:          {T['text_label']} !important;
    letter-spacing: 0.10em !important;
    text-transform: uppercase !important;
}}

[data-testid="stMetricDelta"],
[data-testid="stMetricDeltaIcon"] {{
    color:     {T['accent']} !important;
    font-size: 0.78rem !important;
}}

/* ── ALERT ────────────────────────────────────────────── */
.stAlert > div {{
    background:    rgba(251,191,36,0.06) !important;
    border:        1px solid rgba(251,191,36,0.20) !important;
    border-radius: 10px !important;
    color:         {T['text_secondary']} !important;
}}

/* ── GRADIENT TITLE — CSS class bypasses Streamlit sanitizer ── */
.ns-grad {{
    background:              linear-gradient(90deg, {T['accent']} 0%, {T['accent_blue']} 50%, {T['accent_purple']} 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip:         text !important;
    display:                 inline !important;
}}

/* ── COPY TOAST ───────────────────────────────────────── */
#ns-toast {{
    position:       fixed;
    bottom:         36px;
    left:           50%;
    transform:      translateX(-50%) translateY(16px);
    background:     {T['settings_bg']};
    border:         1px solid {T['accent']}55;
    border-radius:  100px;
    padding:        11px 24px 11px 18px;
    display:        flex;
    align-items:    center;
    gap:            11px;
    font-family:    'Syne', sans-serif;
    font-size:      0.78rem;
    font-weight:    600;
    letter-spacing: 0.06em;
    color:          {T['accent']};
    box-shadow:     0 10px 40px rgba(0,0,0,0.28), 0 0 0 1px {T['accent']}22;
    opacity:        0;
    transition:     opacity 0.22s ease, transform 0.22s ease;
    z-index:        99999;
    pointer-events: none;
    white-space:    nowrap;
}}
#ns-toast.ns-show {{
    opacity:   1;
    transform: translateX(-50%) translateY(0);
}}

#ns-spinner {{
    width:            15px;
    height:           15px;
    border:           2px solid {T['accent']}30;
    border-top-color: {T['accent']};
    border-radius:    50%;
    animation:        ns-spin 0.65s linear infinite;
    flex-shrink:      0;
    display:          none;
}}
#ns-toast.ns-show  #ns-spinner {{ display: block; }}
#ns-check {{
    display:     none;
    font-size:   1rem;
    line-height: 1;
    color:       {T['accent']};
}}
#ns-toast.ns-done #ns-spinner {{ display: none; }}
#ns-toast.ns-done #ns-check   {{ display: block; }}

/* ── RESULT CARD ACTION BUTTONS ───────────────────────── */
/* ISSUE 4 — copy button visible & clickable-looking in dark mode */
.ns-action-btn {{
    background:    {T['copy_bg']} !important;
    border:        1px solid {T['copy_border']} !important;
    border-radius: 8px !important;
    color:         {T['copy_text']} !important;
    font-family:   'DM Sans', sans-serif !important;
    font-size:     0.78rem !important;
    font-weight:   500 !important;
    letter-spacing:0.05em !important;
    padding:       7px 18px !important;
    cursor:        pointer !important;
    transition:    all 0.2s ease !important;
    display:       inline-flex !important;
    align-items:   center !important;
    gap:           7px !important;
    text-decoration: none !important;
    line-height:   1 !important;
}}
.ns-action-btn:hover {{
    background:   {T['accent']}15 !important;
    border-color: {T['accent']}66 !important;
    color:        {T['accent']} !important;
    transform:    translateY(-1px) !important;
}}
.ns-action-btn svg {{ opacity: 0.7; flex-shrink: 0; }}

/* ── KEYFRAMES ────────────────────────────────────────── */
@keyframes blockFill {{
    0%   {{ opacity: 0.12; transform: scaleY(0.55); }}
    100% {{ opacity: 1;    transform: scaleY(1); }}
}}
@keyframes pulse {{
    0%,100% {{ opacity:1;   transform:scale(1); }}
    50%     {{ opacity:0.5; transform:scale(0.85); }}
}}
@keyframes ns-spin {{
    to {{ transform: rotate(360deg); }}
}}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# 6. AUTO-RESIZE TEXTAREA via JS
# ---------------------------------------------------
components.html("""
<script>
(function() {
  function autoResize(ta) {
    ta.style.overflow = 'hidden';
    ta.style.height   = 'auto';
    ta.style.height   = Math.max(220, ta.scrollHeight) + 'px';
  }
  function attachAll() {
    var doc = window.parent.document;
    doc.querySelectorAll('.stTextArea textarea').forEach(function(ta) {
      if (ta.dataset.arAttached) return;
      ta.dataset.arAttached = '1';
      ta.addEventListener('input', function() { autoResize(ta); });
      autoResize(ta);
    });
  }
  attachAll();
  new MutationObserver(attachAll).observe(
    window.parent.document.body,
    { childList: true, subtree: true }
  );
})();
</script>
""", height=0)

# ---------------------------------------------------
# 7. THEME TOGGLE
# ---------------------------------------------------
_, _, _, _, toggle_col = st.columns([4, 1, 1, 1, 1])
with toggle_col:
    toggle_label = "☀️ Light" if is_dark else "🌙 Dark"
    if st.button(toggle_label, key="theme_btn"):
        st.session_state.theme = "light" if is_dark else "dark"
        st.rerun()

st.markdown(f"""
<style>
[data-testid="stHorizontalBlock"]:first-of-type .stButton > button {{
    background:     {T['toggle_bg']} !important;
    border:         1px solid {T['card_border']} !important;
    border-radius:  100px !important;
    color:          {T['text_secondary']} !important;
    font-family:    'DM Sans', sans-serif !important;
    font-size:      0.75rem !important;
    font-weight:    500 !important;
    letter-spacing: 0.04em !important;
    padding:        6px 16px !important;
    box-shadow:     0 2px 10px rgba(0,0,0,0.15) !important;
    width:          auto !important;
    text-transform: none !important;
}}
[data-testid="stHorizontalBlock"]:first-of-type .stButton > button:hover {{
    border-color: {T['accent']}55 !important;
    color:        {T['accent']} !important;
    transform:    none !important;
    box-shadow:   0 2px 14px rgba(0,0,0,0.2) !important;
}}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# 8. HERO — ISSUE 8: padding reduced ~30%
# ---------------------------------------------------
eyebrow_bg     = "rgba(99,255,200,0.07)"  if is_dark else "rgba(79,70,229,0.07)"
eyebrow_border = "rgba(99,255,200,0.18)"  if is_dark else "rgba(79,70,229,0.20)"

st.markdown(f"""
<div style="padding:12px 0 20px 0;">
    <div style="display:inline-flex;align-items:center;gap:8px;
        background:{eyebrow_bg};border:1px solid {eyebrow_border};
        border-radius:100px;padding:5px 14px 5px 10px;margin-bottom:14px;">
        <span style="width:7px;height:7px;background:{T['accent']};border-radius:50%;
            box-shadow:0 0 8px {T['accent']};display:inline-block;
            animation:pulse 2s ease infinite;"></span>
        <span style="font-family:'DM Sans',sans-serif;font-size:0.70rem;font-weight:600;
            color:{T['accent']};letter-spacing:0.14em;text-transform:uppercase;">
            Transformer &middot; T5 &amp; BART &middot; NLP
        </span>
    </div>
    <div style="font-family:'Syne',sans-serif;
        font-size:clamp(2.4rem,5vw,4.2rem);font-weight:800;
        line-height:1.0;letter-spacing:-2px;
        color:{T['text_primary']};margin-bottom:10px;">
        Neural<span class="ns-grad">Sum</span>
    </div>
    <div style="font-size:1.0rem;color:{T['text_secondary']};font-weight:300;
        max-width:460px;line-height:1.6;font-family:'DM Sans',sans-serif;">
        Distill vast information into precise intelligence &mdash; powered by transformer models.
    </div>
</div>
<div style="height:1px;margin-bottom:24px;
    background:linear-gradient(90deg,{T['divider_side']},{T['divider_mid']} 50%,{T['divider_side']});"></div>
""", unsafe_allow_html=True)

# ── reusable section label ────────────────────────
def sec_label(text):
    return (
        '<div style="font-family:\'Syne\',sans-serif;font-size:0.65rem;font-weight:700;'
        'letter-spacing:0.16em;text-transform:uppercase;'
        f'color:{T["text_label"]};display:flex;align-items:center;'
        'gap:8px;margin-bottom:12px;">'
        f'<span style="width:16px;height:1px;background:{T["accent"]}88;'
        f'display:inline-block;"></span>{text}'
        '</div>'
    )

# ---------------------------------------------------
# 9. MAIN LAYOUT
# ---------------------------------------------------
col_input, col_settings = st.columns([3, 1], gap="medium")

with col_settings:
    # ISSUE 5 — removed heavy card wrapper with border-bottom separator.
    # Now just a simple inline section label above the controls.
    st.markdown(
        f'<div style="font-family:\'Syne\',sans-serif;font-size:0.62rem;font-weight:700;'
        f'letter-spacing:0.16em;text-transform:uppercase;color:{T["text_label"]};'
        f'display:flex;align-items:center;gap:7px;margin-bottom:14px;">'
        f'<span style="width:14px;height:1px;background:{T["accent"]}88;display:inline-block;"></span>'
        '&#9881; Configuration</div>',
        unsafe_allow_html=True
    )

    length_option = st.selectbox("Summary Detail", ["Short", "Medium", "Long"], index=1)
    st.write("")
    model_option  = st.selectbox(
        "AI Engine",
        list(_MODEL_LABEL_TO_KEY.keys()),
        help="Auto picks the best model based on word count"
    )
    model_choice  = _MODEL_LABEL_TO_KEY[model_option]

    st.markdown("<br>", unsafe_allow_html=True)
    generate_btn = st.button("⚡  RUN ANALYSIS", use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ISSUE 6 — model logic shown as ghost hint, not a prominent UI control
    st.markdown(
        f'<div style="background:{T["badge_bg"]};border:1px solid {T["badge_border"]};'
        'border-radius:10px;padding:10px 12px;">'
        '<div style="font-family:\'Syne\',sans-serif;font-size:0.58rem;font-weight:700;'
        f'letter-spacing:0.14em;text-transform:uppercase;color:{T["tip_label"]};margin-bottom:6px;">'
        'Auto Model Logic</div>'
        f'<div style="font-size:0.74rem;color:{T["text_muted"]};'
        'font-family:\'DM Sans\',sans-serif;line-height:1.7;">'
        f'<span style="color:{T["tip_bold"]};">&lt;120 words</span> &rarr; T5 Fast<br>'
        f'<span style="color:{T["tip_bold"]};">&#8805;120 words</span> &rarr; BART Accurate'
        '</div></div>',
        unsafe_allow_html=True
    )

with col_input:
    # Source Text header — clean, no word count pill above (it's shown below textarea)
    st.markdown(
        f'<div style="font-family:\'Syne\',sans-serif;font-size:0.65rem;font-weight:700;'
        f'letter-spacing:0.16em;text-transform:uppercase;color:{T["text_label"]};'
        'display:flex;align-items:center;gap:8px;margin-bottom:8px;">'
        f'<span style="width:16px;height:1px;background:{T["accent"]}88;display:inline-block;"></span>'
        'Source Text</div>',
        unsafe_allow_html=True
    )

    user_text = st.text_area(
        "Input Text",
        height=220,
        placeholder="Paste your research paper, article, report, or any long-form text here...",
        key="main_input"
    )

    # ISSUE 2 — clean single-row flex: left group (count | model hint) + right pill
    # Both wc values come from user_text (current render, always accurate)
    if user_text and user_text.strip():
        wc     = len(user_text.split())
        m_hint = "T5" if wc < 120 else "BART"
        m_col  = T['accent'] if wc < 120 else T['accent_blue']
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:0;margin-top:6px;">'
            # ── left group ──
            f'<div style="display:flex;align-items:center;gap:8px;flex:1;">'
            f'<span style="font-size:0.74rem;font-family:\'DM Sans\',sans-serif;color:{T["text_muted"]};">'
            f'<b style="color:{T["text_primary"]};font-family:\'Syne\',sans-serif;">{wc}</b>'
            '&nbsp;words detected'
            '</span>'
            f'<span style="width:1px;height:11px;background:{T["pill_border"]};'
            'display:inline-block;flex-shrink:0;"></span>'
            f'<span style="font-size:0.72rem;font-family:\'DM Sans\',sans-serif;color:{T["text_muted"]};">'
            f'Auto:&nbsp;<b style="color:{m_col};font-family:\'Syne\',sans-serif;">{m_hint}</b>'
            '</span>'
            '</div>'
            # ── right pill — ISSUE minor: border-radius 8px ──
            f'<span style="display:inline-flex;align-items:center;gap:5px;'
            f'background:{T["pill_bg"]};border:1px solid {T["pill_border"]};'
            'border-radius:8px;padding:3px 10px;font-size:0.72rem;'
            f'color:{T["text_muted"]};font-family:\'DM Sans\',sans-serif;flex-shrink:0;">'
            f'<b style="color:{T["accent"]};font-family:\'Syne\',sans-serif;">{wc}</b>'
            '&nbsp;words'
            '</span>'
            '</div>',
            unsafe_allow_html=True
        )

# ---------------------------------------------------
# 10. PROCESSING & OUTPUT
# ---------------------------------------------------
if generate_btn:
    raw = (user_text or "").strip()

    if not raw:
        st.warning("⚠️  Please paste some text before running the analysis.")

    elif len(raw.split()) < 10:
        st.warning(
            "⚠️  Input is too short — please provide at least **10 words** "
            "so the model has enough context to summarize."
        )

    elif len(raw) > 50_000:
        st.warning(
            f"⚠️  Input is too long ({len(raw):,} characters). "
            "Please trim it to under 50,000 characters."
        )

    else:
        loader_slot = st.empty()
        loader_slot.markdown(LOADER_PHASE1, unsafe_allow_html=True)

        cleaned = clean_text(raw)

        if not cleaned or not cleaned.strip() or len(cleaned.split()) < 5:
            loader_slot.empty()
            st.warning(
                "⚠️  No readable content remained after cleaning. "
                "Please try different input text."
            )
        else:
            loader_slot.markdown(LOADER_PHASE2, unsafe_allow_html=True)

            summary, model_used_raw = summarize_text(
                cleaned,
                length_option.lower(),
                model_choice
            )

            loader_slot.empty()

            model_used_display = _MODEL_KEY_TO_DISPLAY.get(
                str(model_used_raw).lower().strip(),
                str(model_used_raw).upper()
            )

            st.markdown("<br>", unsafe_allow_html=True)
            out_left, out_right = st.columns([2, 1], gap="medium")

            # ── SUMMARY OUTPUT ──────────────────────────────────────────────
            with out_left:
                st.markdown(sec_label("Intelligence Output"), unsafe_allow_html=True)

                # Escape summary for safe embedding in HTML attribute
                summary_attr = _html.escape(summary, quote=True)

                # ── ISSUE 4 FIX: Copy button root cause ────────────────────
                # Streamlit's bleach HTML sanitizer strips 'onclick' and ALL
                # event-handler attributes from st.markdown content — even with
                # unsafe_allow_html=True.  The button renders but is dead.
                #
                # Solution: render the buttons as pure HTML (no onclick),
                # then attach JS event listeners from components.html() which
                # runs in its own iframe and accesses the parent document via
                # window.parent.document — bypassing bleach entirely.
                # ──────────────────────────────────────────────────────────

                # SVG icons
                _icon_copy = (
                    '<svg width="11" height="13" viewBox="0 0 11 13" fill="none" '
                    f'xmlns="http://www.w3.org/2000/svg" style="flex-shrink:0;">'
                    f'<rect x="3" y="0.5" width="7.5" height="9.5" rx="1.5" stroke="currentColor" stroke-width="1.2"/>'
                    f'<rect x="0.5" y="3" width="7.5" height="9.5" rx="1.5" fill="{T["result_bg"]}" stroke="currentColor" stroke-width="1.2"/>'
                    '</svg>'
                )
                _icon_dl = (
                    '<svg width="12" height="13" viewBox="0 0 12 13" fill="none" '
                    'xmlns="http://www.w3.org/2000/svg" style="flex-shrink:0;">'
                    '<path d="M6 1v8M3 6l3 3 3-3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>'
                    '<path d="M1 11h10" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>'
                    '</svg>'
                )

                action_row = (
                    # Toast notification (position:fixed, appears above everything)
                    '<div id="ns-toast">'
                    '<div id="ns-spinner"></div>'
                    '<span id="ns-check">&#10003;</span>'
                    '<span id="ns-toast-msg">Copied to Clipboard</span>'
                    '</div>'
                    # Action button row inside card footer
                    '<div style="display:flex;align-items:center;gap:10px;'
                    'justify-content:flex-end;margin-top:18px;'
                    f'padding-top:14px;border-top:1px solid {T["result_border"]};">'
                    # Export button — id + data-payload (handler injected via components.html)
                    f'<button id="ns-export-btn" class="ns-action-btn" data-payload="{summary_attr}">'
                    + _icon_dl
                    + 'Export</button>'
                    # Copy button — id + data-payload
                    f'<button id="ns-copy-btn" class="ns-action-btn" data-payload="{summary_attr}">'
                    + _icon_copy
                    + 'Copy</button>'
                    '</div>'
                )

                result_card = (
                    f'<div style="background:{T["result_bg"]};border:1px solid {T["result_border"]};'
                    'border-radius:16px;padding:28px 30px 22px 30px;'
                    f'color:{T["result_text"]};line-height:1.85;font-size:1.0rem;'
                    "font-weight:300;font-family:'DM Sans',sans-serif;"
                    'position:relative;overflow:hidden;">'
                    f'<div style="position:absolute;top:0;left:0;right:0;height:1px;'
                    f'background:linear-gradient(90deg,transparent,{T["accent"]}55,transparent);"></div>'
                    f'<div style="position:absolute;top:4px;right:20px;font-size:5.5rem;'
                    f"font-family:'Syne',sans-serif;color:{T['accent']}0d;"
                    'line-height:1;pointer-events:none;user-select:none;">&ldquo;</div>'
                    f'<div style="position:relative;z-index:1;">{summary}</div>'
                    + action_row
                    + '</div>'
                )

                st.markdown(result_card, unsafe_allow_html=True)

                # ISSUE 4 FIX — Inject event handlers via components.html().
                # This script runs inside Streamlit's component iframe and reaches
                # into window.parent.document to attach real click handlers —
                # completely bypassing bleach sanitization.
                #
                # Copy strategy: try modern navigator.clipboard API first (works on
                # HTTPS / localhost), then fall back to legacy execCommand('copy').
                # Export strategy: create Blob → object URL → auto-click <a> → revoke.
                components.html(f"""
<script>
(function() {{
  var doc = window.parent.document;

  function showToast(ok) {{
    var toast = doc.getElementById('ns-toast');
    var msg   = doc.getElementById('ns-toast-msg');
    if (!toast) return;
    toast.classList.remove('ns-done');
    toast.classList.add('ns-show');
    if (ok) {{
      msg.textContent = 'Copied to Clipboard';
      setTimeout(function() {{ toast.classList.add('ns-done'); }}, 350);
    }} else {{
      msg.textContent = 'Could not copy \u2014 please copy manually';
    }}
    setTimeout(function() {{ toast.classList.remove('ns-show', 'ns-done'); }}, 2500);
  }}

  function execCopy(text) {{
    var ta = doc.createElement('textarea');
    ta.value = text;
    ta.style.cssText = 'position:fixed;top:-9999px;left:-9999px;opacity:0;';
    doc.body.appendChild(ta);
    ta.focus(); ta.select();
    var ok = false;
    try {{ ok = doc.execCommand('copy'); }} catch(e) {{}}
    doc.body.removeChild(ta);
    showToast(ok);
  }}

  function attachHandlers() {{
    // ── Copy button ──────────────────────────────────────────────────
    var copyBtn = doc.getElementById('ns-copy-btn');
    if (copyBtn && !copyBtn.dataset.nsAttached) {{
      copyBtn.dataset.nsAttached = '1';
      copyBtn.addEventListener('click', function() {{
        var text = copyBtn.getAttribute('data-payload');
        if (window.parent.isSecureContext && navigator.clipboard && navigator.clipboard.writeText) {{
          navigator.clipboard.writeText(text)
            .then(function() {{ showToast(true); }})
            .catch(function() {{ execCopy(text); }});
        }} else {{
          execCopy(text);
        }}
      }});
    }}

    // ── Export button ────────────────────────────────────────────────
    var expBtn = doc.getElementById('ns-export-btn');
    if (expBtn && !expBtn.dataset.nsAttached) {{
      expBtn.dataset.nsAttached = '1';
      expBtn.addEventListener('click', function(e) {{
        e.preventDefault();
        var text = expBtn.getAttribute('data-payload');
        var blob = new Blob([text], {{type: 'text/plain'}});
        var url  = URL.createObjectURL(blob);
        var a    = doc.createElement('a');
        a.href     = url;
        a.download = 'NeuralSum_Report.txt';
        doc.body.appendChild(a);
        a.click();
        doc.body.removeChild(a);
        URL.revokeObjectURL(url);
      }});
    }}
  }}

  // Attach immediately, then watch for DOM changes (Streamlit may re-render)
  attachHandlers();
  new MutationObserver(function() {{ attachHandlers(); }}).observe(
    doc.body, {{ childList: true, subtree: true }}
  );
}})();
</script>
""", height=0)

            # ── ANALYTICS ──────────────────────────────────────────────────
            with out_right:
                # FUNCTIONAL FIX — word counter discrepancy:
                # analytics "Original" used len(cleaned.split()) which differs
                # from the badge showing len(user_text.split()).
                # Unified to user_text so both displays show the same number.
                orig_words = len(user_text.split())
                sum_words  = len(summary.split())

                if orig_words > 0:
                    reduction = round(((orig_words - sum_words) / orig_words) * 100, 1)
                else:
                    reduction = 0.0

                bar_pct     = max(0.0, min(reduction, 100.0))
                display_pct = max(0.0, reduction)

                compress_bg  = "rgba(255,255,255,0.03)" if is_dark else "rgba(79,70,229,0.04)"
                compress_brd = "rgba(255,255,255,0.06)" if is_dark else "rgba(79,70,229,0.12)"
                bar_track    = "rgba(255,255,255,0.07)" if is_dark else "rgba(79,70,229,0.10)"

                st.markdown(sec_label("Analytics"), unsafe_allow_html=True)

                m1, m2 = st.columns(2)
                with m1: st.metric("Original", orig_words)
                with m2: st.metric("Summary",  sum_words)

                st.markdown(
                    f'<div style="background:{compress_bg};border:1px solid {compress_brd};'
                    'border-radius:12px;padding:16px 18px;margin-top:14px;">'
                    f'<div style="font-size:0.68rem;color:{T["text_label"]};'
                    "font-family:'DM Sans',sans-serif;text-transform:uppercase;"
                    'letter-spacing:0.12em;margin-bottom:10px;font-weight:600;">Compression Ratio</div>'
                    f'<div style="background:{bar_track};border-radius:100px;'
                    'height:5px;width:100%;overflow:hidden;margin-bottom:10px;">'
                    f'<div style="height:5px;border-radius:100px;width:{bar_pct}%;'
                    f'background:linear-gradient(90deg,{T["accent"]},{T["accent_blue"]});"></div></div>'
                    f'<div style="font-family:\'Syne\',sans-serif;font-size:1.8rem;font-weight:800;'
                    f'color:{T["accent"]};letter-spacing:-1px;">{display_pct}%</div>'
                    f'<div style="font-size:0.73rem;color:{T["compress_sub"]};'
                    f"font-family:'DM Sans',sans-serif;margin-top:2px;"
                    f'">{orig_words} &rarr; {sum_words} words</div>'
                    '</div>'
                    '<div style="margin-top:12px;display:inline-flex;align-items:center;gap:8px;'
                    f'background:{T["engine_bg"]};border:1px solid {T["engine_border"]};'
                    'border-radius:8px;padding:8px 14px;'
                    f"font-family:'DM Sans',sans-serif;font-size:0.80rem;color:{T['text_muted']};"
                    '">'
                    f'<span style="width:6px;height:6px;background:{T["engine_dot"]};'
                    f'border-radius:50%;box-shadow:0 0 6px {T["engine_dot"]};'
                    'display:inline-block;flex-shrink:0;"></span>'
                    '<span>Engine:</span>'
                    # ISSUE minor — model_used_display uses spaced arrow "Auto → BART"
                    f'<span style="font-family:\'Syne\',sans-serif;font-weight:700;'
                    f'color:{T["engine_val"]};font-size:0.85rem;">{model_used_display}</span>'
                    '</div>',
                    unsafe_allow_html=True
                )

# ---------------------------------------------------
# 11. FOOTER
# ---------------------------------------------------
st.markdown(
    f'<div style="text-align:center;padding:38px 0 24px 0;'
    f"font-family:'DM Sans',sans-serif;font-size:0.73rem;"
    f'color:{T["footer_text"]};letter-spacing:0.08em;'
    f'border-top:1px solid {T["footer_border"]};margin-top:60px;">'
    'Microsoft Elevate Capstone &nbsp;&middot;&nbsp;'
    f'<span style="color:{T["accent"]}55;">NeuralSum</span>'
    '&nbsp;&middot;&nbsp; Engineered with Transformers'
    '</div>',
    unsafe_allow_html=True
)
