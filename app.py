# app.py

import streamlit as st
from rembg import remove
from PIL import Image
import io

st.set_page_config(page_title="Background Remover", layout="centered")

# Title
st.markdown("<h1 style='text-align: center;'>🖼️ Background Remover</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Remove background from images — single or multiple uploads. Free, fast & mobile-friendly!</p>", unsafe_allow_html=True)
st.markdown("---")

# Toggle mode (single / multi)
if "multi_mode" not in st.session_state:
    st.session_state.multi_mode = False

col1, col2 = st.columns([1, 1])
with col1:
    if not st.session_state.multi_mode:
        if st.button("📂 Upload Multiple Images "):
            st.session_state.multi_mode = True
with col2:
    if st.session_state.multi_mode:
        if st.button("🔙 Back to Single Image Mode"):
            st.session_state.multi_mode = False

st.markdown("---")

# === MULTIPLE IMAGE MODE ===
if st.session_state.multi_mode:
    uploaded_files = st.file_uploader(
        "Upload up to 4 images (PNG, JPG, JPEG)",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    if uploaded_files:
        if len(uploaded_files) > 4:
            st.warning("🚫 You can upload up to 4 images only.")
        elif st.button("🚀 Process All Images"):
            for i, uploaded_file in enumerate(uploaded_files, start=1):
                st.markdown(f"#### 📷 Image {i}")

                if uploaded_file.size > 10 * 1024 * 1024:
                    st.warning(f"❌ `{uploaded_file.name}` is too large (Max 10MB). Skipping.")
                    continue

                input_bytes = uploaded_file.read()

                try:
                    input_image = Image.open(io.BytesIO(input_bytes))
                    st.image(input_image, caption="Original Image", use_container_width=True)
                except Exception:
                    st.error("⚠️ Could not open this image. Skipping.")
                    continue

                with st.spinner("⏳ Removing background..."):
                    try:
                        result = remove(input_bytes)
                        output_image = Image.open(io.BytesIO(result))

                        st.success("✅ Background removed!")
                        st.image(output_image, caption="Without Background", use_container_width=True)

                        buf = io.BytesIO()
                        output_image.save(buf, format="PNG")

                        st.download_button(
                            label="📥 Download Transparent Image",
                            data=buf.getvalue(),
                            file_name=f"{uploaded_file.name.rsplit('.',1)[0]}_no_bg.png",
                            mime="image/png"
                        )
                        st.markdown("---")
                    except Exception:
                        st.error("❌ Failed to process this image.")

# === SINGLE IMAGE MODE ===
else:
    uploaded_file = st.file_uploader("Upload a single image (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        if uploaded_file.size > 10 * 1024 * 1024:
            st.warning("🚫 Please upload an image smaller than 10MB.")
        else:
            input_bytes = uploaded_file.read()

            try:
                input_image = Image.open(io.BytesIO(input_bytes))
                st.image(input_image, caption="Original Image", use_container_width=True)
            except Exception:
                st.error("⚠️ Could not open the uploaded image. Please try another one.")

            with st.spinner("⏳ Removing background..."):
                try:
                    result = remove(input_bytes)
                    output_image = Image.open(io.BytesIO(result))

                    st.success("✅ Background removed!")
                    st.image(output_image, caption="Without Background", use_container_width=True)

                    buf = io.BytesIO()
                    output_image.save(buf, format="PNG")

                    st.download_button(
                        label="📥 Download Image",
                        data=buf.getvalue(),
                        file_name="no_bg.png",
                        mime="image/png"
                    )
                except Exception:
                    st.error("❌ Failed to remove background.")

# Footer with local logo
st.markdown("---")

col1, col2 = st.columns([1, 8])
with col1:
    st.image("default.png", width=50)
with col2:
    st.markdown("Pixels cleaned up by **FusionStack 🧼**")