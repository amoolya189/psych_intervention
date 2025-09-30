import streamlit as st

# Set page config
st.set_page_config(
    page_title="Digital Psychological Intervention - Manoraksha",
    layout="wide",
    page_icon="🌸"
)

# -------------------- Sidebar Navigation --------------------
st.sidebar.markdown("<h2 style='color:#FF69B4;'>🌸 Manoraksha</h2>", unsafe_allow_html=True)
page = st.sidebar.selectbox(
    "Navigate to",
    [
        "🤖 AI Chat Support",
        "📅 Book Counsellor",
        "📚 Resources",
        "💬 Peer Forum",
        "🛠 Admin Dashboard"
    ]
)

# Optional: Page color themes
page_colors = {
    "🤖 AI Chat Support": "#E0BBE4",
    "📅 Book Counsellor": "#FFDFD3",
    "📚 Resources": "#CFFAFE",
    "💬 Peer Forum": "#B5EAD7",
    "🛠 Admin Dashboard": "#FEE2E2"
}

page_color = page_colors.get(page, "#ffffff")

# -------------------- Homepage Container --------------------
with st.container():
    st.markdown(
        f"<div style='background-color:{page_color}; padding:25px; border-radius:20px'>"
        f"<h1 style='text-align:center; color:#333;'>Welcome to Manoraksha 🌸</h1>"
        f"<p style='text-align:center; font-size:18px; color:#555;'>Your digital companion for mental wellness and psychological guidance.</p>"
        f"</div>",
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

# -------------------- Page Logic --------------------
if page == "🤖 AI Chat Support":
    st.markdown("<h2 style='color:#FF69B4;'>AI Chat Support</h2>", unsafe_allow_html=True)
    import pages.ai_chat

elif page == "📅 Book Counsellor":
    st.markdown("<h2 style='color:#FF69B4;'>Book Counsellor</h2>", unsafe_allow_html=True)
    import pages.booking

elif page == "📚 Resources":
    st.markdown("<h2 style='color:#FF69B4;'>Resources</h2>", unsafe_allow_html=True)
    import pages.resources

elif page == "💬 Peer Forum":
    st.markdown("<h2 style='color:#FF69B4;'>Peer Forum</h2>", unsafe_allow_html=True)
    import pages.forum

elif page == "🛠 Admin Dashboard":
    st.markdown("<h2 style='color:#FF69B4;'>Admin Dashboard</h2>", unsafe_allow_html=True)
    import pages.admin_dashboard  # noqa: F401

# -------------------- Footer --------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:#888;'>© 2025 Manoraksha | Digital Psychological Intervention</p>",
    unsafe_allow_html=True
)
