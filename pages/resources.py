import streamlit as st
import os

st.header("📚 Psychoeducational Resources")

# 1️⃣ Language selection
language = st.selectbox("Select Language", ["English", "Hindi", "Telugu"])

# 2️⃣ Resource type selection
resource_type = st.selectbox("Select Resource Type", ["Videos", "Audios", "PDFs"])

# 3️⃣ Construct folder path
resource_path = f"resources/{language.lower()}/{resource_type.lower()}/"

if os.path.exists(resource_path):
    if resource_type == "Audios":
        subcategories = [d for d in os.listdir(resource_path) if os.path.isdir(os.path.join(resource_path, d))]

        if subcategories:
            for sub in subcategories:
                with st.expander(f"🎵 {sub}"):   # 🔹 Expandable box
                    sub_path = os.path.join(resource_path, sub)
                    audio_files = [f for f in os.listdir(sub_path) if f.endswith(".mp3")]
                    if audio_files:
                        for af in audio_files:
                            st.markdown(f"**{af}**")
                            st.audio(os.path.join(sub_path, af))
                    else:
                        st.info(f"No audios in {sub}.")
        else:
            st.warning("No audio categories found.")
