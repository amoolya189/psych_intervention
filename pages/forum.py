import streamlit as st
from utils.db_utils import get_connection, initialize_db
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
import os

# Initialize DB
initialize_db()

# Auto-refresh every 10 seconds
st_autorefresh(interval=10000, key="forum_refresh")

st.title("💬 Peer Support Forum")

# -------------------------
# Session state for likes and replies
# -------------------------
if "like_post_id" not in st.session_state:
    st.session_state["like_post_id"] = None

if "reply_post_id" not in st.session_state:
    st.session_state["reply_post_id"] = None

# -------------------------
# 1️⃣ Post a new message
# -------------------------
with st.form("post_form"):
    username = st.text_input("Your Name / Pseudonym")
    anonymous = st.checkbox("Post anonymously")
    categories = st.multiselect("Select Categories", ["MentalHealth", "Stress", "Advice", "Other"])
    content = st.text_area("Your Message")
    uploaded_file = st.file_uploader("Attach a file (image, pdf, audio, video)", type=["png","jpg","jpeg","pdf","mp3","mp4"])
    submit = st.form_submit_button("Post Message")
    
    if submit:
        if content:
            username_to_store = "Anonymous" if anonymous or not username else username

            # Save attached file
            file_path = None
            if uploaded_file:
                folder = "uploaded_files"
                os.makedirs(folder, exist_ok=True)
                file_path = os.path.join(folder, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO forum_posts (username, content, categories, file_path, likes, timestamp, parent_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (username_to_store, content, ",".join(categories), file_path, 0, datetime.now().isoformat(), None))
            conn.commit()
            conn.close()
            st.success("✅ Message posted!")
        else:
            st.error("Please enter a message.")

# -------------------------
# 2️⃣ Filter by Category
# -------------------------
filter_category = st.selectbox("Filter by Category", ["All", "MentalHealth", "Stress", "Advice", "Other"])

# -------------------------
# 3️⃣ Display posts
# -------------------------
conn = get_connection()
cursor = conn.cursor()
cursor.execute("""
SELECT id, username, content, categories, file_path, likes, timestamp, parent_id
FROM forum_posts
ORDER BY timestamp DESC
""")
posts = cursor.fetchall()
conn.close()

st.subheader("Recent Posts")

# Helper: format timestamp
def format_timestamp(ts: str) -> str:
    try:
        return datetime.fromisoformat(ts).strftime("%b %d, %Y %H:%M")
    except ValueError:
        return ts

# -------------------------
# Display posts with likes and replies
# -------------------------
for post in posts:
    post_id, uname, content, categories_str, file_path, likes, ts, parent_id = post
    categories_list = categories_str.split(",") if categories_str else []

    # Filter by category only
    if filter_category != "All" and filter_category not in categories_list:
        continue
    if parent_id:
        continue  # only show top-level posts
    
    timestamp_formatted = format_timestamp(ts)
    
    st.markdown(f"""
    <div style='border:1px solid #ccc; padding:10px; border-radius:10px; margin-bottom:10px'>
        <b>{uname}</b> ({timestamp_formatted}) | Categories: {", ".join(categories_list)}<br>
        {content}
    """, unsafe_allow_html=True)

    # Show file if uploaded
    if file_path:
        if file_path.lower().endswith(".mp4"):
            st.video(file_path)
        elif file_path.lower().endswith(".mp3"):
            st.audio(file_path)
        elif file_path.lower().endswith(".pdf"):
            st.download_button(f"Download {os.path.basename(file_path)}", open(file_path, "rb").read(), file_name=os.path.basename(file_path))
        elif file_path.lower().endswith((".png", ".jpg", ".jpeg")):
            st.image(file_path)
    
    # -------------------------
    # Like button
    # -------------------------
    if st.button(f"👍 Like ({likes})", key=f"like_{post_id}"):
        st.session_state["like_post_id"] = post_id

    # -------------------------
    # Reply form
    # -------------------------
    with st.form(key=f"reply_form_{post_id}"):
        reply_content = st.text_area(f"Reply to {uname}", key=f"reply_input_{post_id}")
        reply_submit = st.form_submit_button("Reply")
        if reply_submit and reply_content:
            st.session_state["reply_post_id"] = (post_id, reply_content)

    # Show replies
    for reply in posts:
        r_id, r_uname, r_content, r_cats, r_file, r_likes, r_ts, r_parent = reply
        if r_parent == post_id:
            reply_ts = format_timestamp(r_ts)
            st.markdown(f"""
            <div style='margin-left:30px; border-left:2px solid #aaa; padding-left:10px; margin-top:5px'>
            <b>{r_uname}</b> ({reply_ts}): {r_content}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Handle likes after loop
# -------------------------
if st.session_state["like_post_id"]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE forum_posts SET likes = likes + 1 WHERE id = ?",
        (st.session_state["like_post_id"],)
    )
    conn.commit()
    conn.close()
    st.session_state["like_post_id"] = None
    st.experimental_rerun()

# -------------------------
# Handle replies after loop
# -------------------------
if st.session_state["reply_post_id"]:
    parent_id, reply_text = st.session_state["reply_post_id"]
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO forum_posts (username, content, categories, likes, timestamp, parent_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, ("Anonymous", reply_text, "", 0, datetime.now().isoformat(), parent_id))
    conn.commit()
    conn.close()
    st.session_state["reply_post_id"] = None
    st.experimental_rerun()
