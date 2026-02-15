import streamlit as st
from summarizer import summarize_text
from ocr_reader import extract_text_from_image
from text_cleaner import clean_text

st.set_page_config(
    page_title="AI Text + Image Summarizer",
    page_icon="🧠",
    layout="wide"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.main-title {
    font-size:40px;
    font-weight:700;
}
.sub-text {
    color:gray;
    margin-bottom:20px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("<div class='main-title'>🧠 AI Text + Image Summarizer</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>Upload image or paste text → AI will extract & summarize</div>", unsafe_allow_html=True)

st.divider()

# ---------- OPTIONS ----------
col1, col2 = st.columns([2,1])

with col1:
    option = st.radio("Choose Input Type:", ["Text", "Image"], horizontal=True)

with col2:
    length = st.selectbox("Summary Length", ["short", "medium", "long"])

st.divider()

# ========================= TEXT MODE =========================
if option == "Text":

    st.subheader("📝 Enter Text")
    user_text = st.text_area("", height=200, placeholder="Paste your paragraph here...")

    if st.button("🚀 Generate Summary", use_container_width=True):

        if not user_text.strip():
            st.warning("Enter some text first")
            st.stop()

        with st.spinner("AI is generating summary..."):
            cleaned = clean_text(user_text)
            summary = summarize_text(cleaned, length)

        st.success("Summary generated")

        st.subheader("📌 Summary")
        st.write(summary)

        # ---------- METRICS UI ----------
        orig_words = len(cleaned.split())
        sum_words = len(summary.split())
        reduction = round(((orig_words - sum_words) / orig_words) * 100, 2) if orig_words else 0

        st.markdown("### 📊 Summary Analytics")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div style="
                background:#111827;
                padding:22px;
                border-radius:14px;
                text-align:center;
                box-shadow:0 4px 12px rgba(0,0,0,0.25);
            ">
                <h4 style="color:#9CA3AF;margin-bottom:6px;">Original Words</h4>
                <h2 style="color:#60A5FA;margin:0;">{orig_words}</h2>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="
                background:#111827;
                padding:22px;
                border-radius:14px;
                text-align:center;
                box-shadow:0 4px 12px rgba(0,0,0,0.25);
            ">
                <h4 style="color:#9CA3AF;margin-bottom:6px;">Summary Words</h4>
                <h2 style="color:#34D399;margin:0;">{sum_words}</h2>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            color = "#22C55E" if reduction > 0 else "#EF4444"
            st.markdown(f"""
            <div style="
                background:#111827;
                padding:22px;
                border-radius:14px;
                text-align:center;
                box-shadow:0 4px 12px rgba(0,0,0,0.25);
            ">
                <h4 style="color:#9CA3AF;margin-bottom:6px;">Reduction</h4>
                <h2 style="color:{color};margin:0;">{reduction}%</h2>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # centered download button
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            st.download_button(
                "⬇ Download Summary",
                summary,
                file_name="summary.txt",
                mime="text/plain",
                use_container_width=True
            )


# ========================= IMAGE MODE =========================
if option == "Image":

    st.subheader("🖼 Upload Image")
    uploaded = st.file_uploader("", type=["png", "jpg", "jpeg"])

    if uploaded:
        st.image(uploaded, width=300)

    if uploaded and st.button("🚀 Extract & Summarize", use_container_width=True):

        with st.spinner("Reading image + generating summary..."):
            extracted = extract_text_from_image(uploaded)

            if not extracted.strip():
                st.error("No text detected in image")
                st.stop()

            cleaned = clean_text(extracted)
            summary = summarize_text(cleaned, length)

        st.success("Done")

        st.subheader("📄 Extracted Text")
        st.write(extracted)

        st.subheader("📌 Summary")
        st.write(summary)

        # ---------- METRICS UI ----------
        orig_words = len(cleaned.split())
        sum_words = len(summary.split())
        reduction = round(((orig_words - sum_words) / orig_words) * 100, 2) if orig_words else 0

        st.markdown("### 📊 Summary Analytics")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div style="
                background:#111827;
                padding:22px;
                border-radius:14px;
                text-align:center;
                box-shadow:0 4px 12px rgba(0,0,0,0.25);
            ">
                <h4 style="color:#9CA3AF;margin-bottom:6px;">Original Words</h4>
                <h2 style="color:#60A5FA;margin:0;">{orig_words}</h2>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="
                background:#111827;
                padding:22px;
                border-radius:14px;
                text-align:center;
                box-shadow:0 4px 12px rgba(0,0,0,0.25);
            ">
                <h4 style="color:#9CA3AF;margin-bottom:6px;">Summary Words</h4>
                <h2 style="color:#34D399;margin:0;">{sum_words}</h2>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            color = "#22C55E" if reduction > 0 else "#EF4444"
            st.markdown(f"""
            <div style="
                background:#111827;
                padding:22px;
                border-radius:14px;
                text-align:center;
                box-shadow:0 4px 12px rgba(0,0,0,0.25);
            ">
                <h4 style="color:#9CA3AF;margin-bottom:6px;">Reduction</h4>
                <h2 style="color:{color};margin:0;">{reduction}%</h2>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            st.download_button(
                "⬇ Download Summary",
                summary,
                file_name="image_summary.txt",
                mime="text/plain",
                use_container_width=True
            )
