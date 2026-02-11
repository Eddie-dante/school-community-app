import streamlit as st
from datetime import datetime

st.set_page_config(page_title="School Community", page_icon="🏫")
st.title("🏫 School Community Hub")

# Initialize data
if 'user' not in st.session_state:
    st.session_state.user = None
if 'announcements' not in st.session_state:
    st.session_state.announcements = [
        {"author": "Admin", "role": "admin", "text": "Welcome to School Community Hub!", "time": "2024-01-01"},
        {"author": "Ms. Smith", "role": "teacher", "text": "Parent-teacher meeting Friday 5pm", "time": "2024-01-02"}
    ]

# Login sidebar
with st.sidebar:
    st.header("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["student", "teacher", "admin"])
    
    if st.button("Login"):
        st.session_state.user = {"email": email, "role": role, "name": email.split('@')[0]}
        st.rerun()
    
    if st.session_state.user:
        if st.button("Logout"):
            st.session_state.user = None
            st.rerun()

# Main app
if st.session_state.user:
    user = st.session_state.user
    st.success(f"Welcome **{user['name']}**! ({user['role']})")
    
    # Announcements
    st.header("📢 Announcements")
    
    # Post announcement (teachers/admins)
    if user['role'] in ['teacher', 'admin']:
        with st.expander("➕ New Announcement"):
            new_ann = st.text_area("Write announcement")
            if st.button("Post"):
                st.session_state.announcements.insert(0, {
                    "author": user['name'],
                    "role": user['role'],
                    "text": new_ann,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                st.rerun()
    
    # Display announcements
    for ann in st.session_state.announcements[:10]:
        with st.container():
            st.markdown(f"**{ann['author']}** · `{ann['role']}`")
            st.markdown(ann['text'])
            st.caption(ann['time'])
            st.divider()
    
    # Classes
    st.header("📚 Your Classes")
    classes = ["Math 101", "English", "Science", "History"]
    cols = st.columns(4)
    for i, class_name in enumerate(classes):
        with cols[i]:
            st.button(class_name, use_container_width=True)
    
else:
    st.info("👋 Please login from the sidebar")
    
    st.markdown("""
    ### Demo Accounts:
    - **Teacher**: any email + teacher role
    - **Student**: any email + student role  
    - **Admin**: any email + admin role
    """)
