import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="School Community", page_icon="🏫", layout="wide")
st.title("🏫 School Community Hub")

# ========== INITIALIZE DATA ==========
if 'user' not in st.session_state:
    st.session_state.user = None
if 'announcements' not in st.session_state:
    st.session_state.announcements = [
        {"author": "Admin", "role": "admin", "text": "🏫 Welcome to School Community Hub! Check your class pages for homework.", "time": "2024-01-01 09:00"},
        {"author": "Ms. Smith", "role": "teacher", "text": "📚 Parent-teacher meeting Friday 5pm in the auditorium", "time": "2024-01-02 14:30"},
        {"author": "Mr. Johnson", "role": "teacher", "text": "📝 Math homework: Page 42, exercises 1-10 (Due Monday)", "time": "2024-01-03 11:15"}
    ]
if 'homework' not in st.session_state:
    st.session_state.homework = [
        {"class": "Math 101", "title": "Algebra Worksheet", "due": "2024-01-10", "teacher": "Mr. Johnson"},
        {"class": "English", "title": "Essay: My Hero", "due": "2024-01-12", "teacher": "Ms. Smith"},
        {"class": "Science", "title": "Lab Report", "due": "2024-01-15", "teacher": "Dr. Brown"}
    ]
if 'events' not in st.session_state:
    st.session_state.events = [
        {"name": "Parent-Teacher Meeting", "date": "2024-01-05", "time": "5:00 PM", "location": "Auditorium"},
        {"name": "Science Fair", "date": "2024-01-20", "time": "10:00 AM", "location": "Gymnasium"},
        {"name": "Spring Break", "date": "2024-03-11", "time": "All Day", "location": "School Closed"}
    ]

# ========== SIDEBAR - LOGIN ==========
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/school.png", width=80)
    st.header("🔐 Login")
    
    if st.session_state.user is None:
        email = st.text_input("Email", value="eddiegucci05@gmail.com")
        password = st.text_input("Password", type="password", value="password123")
        role = st.selectbox("Role", ["student", "teacher", "admin"], index=0)
        
        if st.button("Login", use_container_width=True):
            st.session_state.user = {
                "email": email,
                "role": role,
                "name": email.split('@')[0],
                "full_name": "Eddie Gucci" if email == "eddiegucci05@gmail.com" else email.split('@')[0]
            }
            st.rerun()
    else:
        user = st.session_state.user
        st.success(f"👋 **{user.get('full_name', user['name'])}**")
        st.caption(f"📌 Role: {user['role'].upper()}")
        st.caption(f"📧 {user['email']}")
        st.divider()
        
        # Quick stats
        if user['role'] == 'student':
            st.metric("📚 Classes", "4")
            st.metric("📝 Homework Due", "2")
        elif user['role'] == 'teacher':
            st.metric("👨‍🏫 Students", "32")
            st.metric("📚 Classes", "3")
        else:  # admin
            st.metric("🏫 Total Students", "450")
            st.metric("👨‍🏫 Teachers", "28")
        
        st.divider()
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()

# ========== MAIN CONTENT ==========
if st.session_state.user:
    user = st.session_state.user
    
    # Welcome banner
    col1, col2 = st.columns([3, 1])
    with col1:
        if user['role'] == 'student':
            st.header(f"📚 Welcome back, {user.get('full_name', user['name'])}!")
            st.caption("Here's what's happening at school today.")
        elif user['role'] == 'teacher':
            st.header(f"👨‍🏫 Welcome, {user.get('full_name', user['name'])}!")
            st.caption("Manage your classes and announcements.")
        else:
            st.header(f"👑 Welcome, {user.get('full_name', user['name'])}!")
            st.caption("School administration dashboard.")
    
    with col2:
        st.metric("📅 Date", datetime.now().strftime("%b %d, %Y"))
    
    st.divider()
    
    # ========== TABS ==========
    if user['role'] == 'student':
        tab1, tab2, tab3, tab4 = st.tabs(["📢 Announcements", "📚 My Classes", "📝 Homework", "📅 Events"])
    elif user['role'] == 'teacher':
        tab1, tab2, tab3, tab4 = st.tabs(["📢 Announcements", "📚 My Classes", "📝 Assignments", "📅 Events"])
    else:  # admin
        tab1, tab2, tab3, tab4 = st.tabs(["📢 Announcements", "🏫 School Overview", "👥 Users", "📅 Events"])
    
    # ========== TAB 1: ANNOUNCEMENTS (Everyone) ==========
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📢 Latest Announcements")
            for ann in st.session_state.announcements[:5]:
                with st.container(border=True):
                    cols = st.columns([1, 10])
                    with cols[0]:
                        if ann['role'] == 'teacher':
                            st.markdown("👨‍🏫")
                        elif ann['role'] == 'admin':
                            st.markdown("👑")
                        else:
                            st.markdown("👤")
                    with cols[1]:
                        st.markdown(f"**{ann['author']}** · `{ann['role']}`")
                        st.markdown(ann['text'])
                        st.caption(f"🕐 {ann['time']}")
        
        with col2:
            if user['role'] in ['teacher', 'admin']:
                st.subheader("✏️ Post Announcement")
                with st.form("announcement_form"):
                    ann_text = st.text_area("Message", placeholder="Write your announcement...", height=150)
                    if st.form_submit_button("📢 Post Announcement", use_container_width=True):
                        st.session_state.announcements.insert(0, {
                            "author": user.get('full_name', user['name']),
                            "role": user['role'],
                            "text": ann_text,
                            "time": datetime.now().strftime("%Y-%m-%d %H:%M")
                        })
                        st.success("✅ Announcement posted!")
                        st.rerun()
            else:
                st.info("👋 Teachers and admins can post announcements")
    
    # ========== TAB 2: CLASSES ==========
    with tab2:
        if user['role'] == 'student':
            st.subheader("📚 Your Classes")
            
            classes_data = {
                "Math 101": {"teacher": "Mr. Johnson", "room": "201", "next": "Algebra", "grade": "A-"},
                "English": {"teacher": "Ms. Smith", "room": "105", "next": "Essay Writing", "grade": "B+"},
                "Science": {"teacher": "Dr. Brown", "room": "301", "next": "Chemistry", "grade": "A"},
                "History": {"teacher": "Mr. Davis", "room": "110", "next": "World War II", "grade": "B"}
            }
            
            for class_name, details in classes_data.items():
                with st.expander(f"📖 {class_name}", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"**👨‍🏫 Teacher:** {details['teacher']}")
                        st.markdown(f"**🚪 Room:** {details['room']}")
                    with col2:
                        st.markdown(f"**📝 Next Topic:** {details['next']}")
                        st.markdown(f"**📊 Current Grade:** {details['grade']}")
                    with col3:
                        st.markdown("**📌 Upcoming:**")
                        st.markdown("- Quiz Friday")
                        st.markdown("- Homework due Monday")
        
        elif user['role'] == 'teacher':
            st.subheader("📚 Your Classes")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 🧮 Math 101")
                st.markdown("**Students:** 28")
                st.markdown("**Next:** Algebra Quiz")
                st.button("📝 Post Assignment", key="math_btn")
            
            with col2:
                st.markdown("### 🔬 Science")
                st.markdown("**Students:** 24")
                st.markdown("**Next:** Lab Report")
                st.button("📝 Post Assignment", key="science_btn")
        
        else:  # admin
            st.subheader("🏫 School Overview")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Students", "450", "+12")
            with col2:
                st.metric("Total Teachers", "28", "+2")
            with col3:
                st.metric("Classes", "45", "+3")
            with col4:
                st.metric("Avg. Attendance", "94%", "-1%")
    
    # ========== TAB 3: HOMEWORK/ASSIGNMENTS ==========
    with tab3:
        if user['role'] == 'student':
            st.subheader("📝 Upcoming Homework")
            
            for hw in st.session_state.homework:
                with st.container(border=True):
                    cols = st.columns([2, 1, 1])
                    with cols[0]:
                        st.markdown(f"**{hw['class']}**")
                        st.markdown(f"📌 {hw['title']}")
                    with cols[1]:
                        st.markdown(f"📅 Due: {hw['due']}")
                        st.markdown(f"👨‍🏫 {hw['teacher']}")
                    with cols[2]:
                        if st.button("✓ Mark Done", key=hw['title']):
                            st.success("Good job!")
        
        elif user['role'] == 'teacher':
            st.subheader("📝 Assign Homework")
            
            with st.form("homework_form"):
                col1, col2 = st.columns(2)
                with col1:
                    class_name = st.selectbox("Class", ["Math 101", "English", "Science", "History"])
                    title = st.text_input("Assignment Title")
                with col2:
                    due_date = st.date_input("Due Date")
                    teacher_name = st.text_input("Teacher Name", value=user.get('full_name', user['name']))
                
                description = st.text_area("Description")
                
                if st.form_submit_button("✅ Assign Homework", use_container_width=True):
                    st.session_state.homework.append({
                        "class": class_name,
                        "title": title,
                        "due": due_date.strftime("%Y-%m-%d"),
                        "teacher": teacher_name,
                        "description": description
                    })
                    st.success(f"Homework assigned to {class_name}!")
                    st.rerun()
            
            st.divider()
            st.subheader("📋 Recent Assignments")
            for hw in st.session_state.homework[-3:]:
                st.markdown(f"- **{hw['class']}**: {hw['title']} (Due: {hw['due']})")
    
    # ========== TAB 4: EVENTS ==========
    with tab4:
        st.subheader("📅 School Calendar")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            for event in st.session_state.events:
                with st.container(border=True):
                    cols = st.columns([1, 3, 1])
                    with cols[0]:
                        st.markdown("📌")
                    with cols[1]:
                        st.markdown(f"**{event['name']}**")
                        st.markdown(f"📍 {event['location']}")
                    with cols[2]:
                        st.markdown(f"**{event['date']}**")
                        st.caption(f"⏰ {event['time']}")
        
        with col2:
            if user['role'] in ['teacher', 'admin']:
                st.subheader("➕ Add Event")
                with st.form("event_form"):
                    event_name = st.text_input("Event Name")
                    event_date = st.date_input("Date")
                    event_time = st.text_input("Time")
                    event_loc = st.text_input("Location")
                    if st.form_submit_button("Add Event", use_container_width=True):
                        st.success("Event added!")

else:
    # ========== LANDING PAGE (Not logged in) ==========
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.title("🏫 School Community Hub")
        st.markdown("""
        ### Welcome to your school's digital community!
        
        **✨ Features:**
        - 📢 Real-time announcements
        - 📚 Class pages & materials
        - 📝 Homework assignments
        - 📅 Event calendar
        - 👥 Role-based access (Students, Teachers, Admin)
        
        ### 🎯 Demo Login:
        ```
        Student:  any email + student role
        Teacher:  any email + teacher role
        Admin:    any email + admin role
        ```
        
        👈 **Login from the sidebar to get started!**
        """)
    
    with col2:
        st.image("https://img.icons8.com/fluency/96/classroom.png", width=150)
        st.metric("Active Students", "450+", "+12")
        st.metric("Teachers", "28", "+2")
        st.metric("Upcoming Events", "3", "")

# ========== FOOTER ==========
st.divider()
st.markdown("🏫 **School Community Hub** · Made with Streamlit · v2.0")
