import streamlit as st
from datetime import datetime
import hashlib
import json
from pathlib import Path

# ============ CONFIG ============
st.set_page_config(
    page_title="School Community System",
    page_icon="🏫",
    layout="wide"
)

# ============ DATA STORAGE (Persistent) ============
DATA_DIR = Path("school_data")
DATA_DIR.mkdir(exist_ok=True)

def load_school():
    """Load the single school/community"""
    school_file = DATA_DIR / "school.json"
    if school_file.exists():
        with open(school_file, 'r') as f:
            return json.load(f)
    return None

def save_school(school):
    """Save the school/community"""
    with open(DATA_DIR / "school.json", 'w') as f:
        json.dump(school, f, indent=2)

def load_data(filename, default):
    """Load data for the current school"""
    school = load_school()
    if not school:
        return default
    filepath = DATA_DIR / f"{school['code']}_{filename}"
    if filepath.exists():
        with open(filepath, 'r') as f:
            return json.load(f)
    return default

def save_data(filename, data):
    """Save data for the current school"""
    school = load_school()
    if school:
        with open(DATA_DIR / f"{school['code']}_{filename}", 'w') as f:
            json.dump(data, f, indent=2)

# ============ SESSION STATE ============
if 'user' not in st.session_state:
    st.session_state.user = None
if 'school' not in st.session_state:
    st.session_state.school = load_school()
if 'setup_mode' not in st.session_state:
    st.session_state.setup_mode = False

# ============ MAIN APP LOGIC ============

# ----- CASE 1: NO SCHOOL EXISTS -> ADMIN SETUP -----
if not st.session_state.school and not st.session_state.setup_mode:
    st.title("🏫 Welcome to School Community System")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👑 Create Your School")
        st.markdown("You are the **first user**. Create your school community.")
        
        with st.form("create_school"):
            school_name = st.text_input("School Name", placeholder="e.g., Springfield High School")
            admin_email = st.text_input("Admin Email", placeholder="admin@yourschool.edu")
            admin_password = st.text_input("Admin Password", type="password")
            admin_name = st.text_input("Your Full Name", placeholder="e.g., Dr. Sarah Johnson")
            
            col1_1, col1_2 = st.columns(2)
            with col1_1:
                school_city = st.text_input("City", placeholder="Springfield")
            with col1_2:
                school_state = st.text_input("State", placeholder="IL")
            
            created = st.form_submit_button("🚀 CREATE SCHOOL COMMUNITY", use_container_width=True)
            
            if created:
                if school_name and admin_email and admin_password:
                    # Generate unique school code
                    import random
                    import string
                    school_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                    
                    # Create school
                    school = {
                        "name": school_name,
                        "code": school_code,
                        "city": school_city,
                        "state": school_state,
                        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "admin": {
                            "email": admin_email,
                            "name": admin_name,
                            "password": hashlib.sha256(admin_password.encode()).hexdigest()
                        },
                        "stats": {
                            "students": 0,
                            "teachers": 0,
                            "classes": 0
                        }
                    }
                    
                    save_school(school)
                    st.session_state.school = school
                    st.session_state.user = {
                        "email": admin_email,
                        "name": admin_name,
                        "role": "admin",
                        "joined": datetime.now().strftime("%Y-%m-%d")
                    }
                    st.rerun()
    
    with col2:
        st.markdown("### ℹ️ About")
        st.info("""
        **This is a REAL school community system.**
        
        - You are creating a **real, persistent school**
        - All data saves permanently
        - Users join YOUR school with your school code
        - One school = One community
        
        **Next steps after creation:**
        1. Add teachers
        2. Create classes
        3. Students join with school code
        4. Everyone connects in one community
        """)
    
    st.markdown("---")
    st.markdown("**Already have a school?**")
    if st.button("I need to join an existing school"):
        st.session_state.setup_mode = "join"
        st.rerun()

# ----- CASE 2: JOIN EXISTING SCHOOL -----
elif st.session_state.setup_mode == "join":
    st.title("🏫 Join Your School Community")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🔑 Enter School Code")
        st.markdown("Get this code from your school administrator.")
        
        with st.form("join_school"):
            school_code = st.text_input("School Code", placeholder="e.g., ABC123", 
                                       help="6-digit code from your school admin")
            email = st.text_input("Your Email")
            password = st.text_input("Create Password", type="password")
            full_name = st.text_input("Your Full Name")
            role = st.selectbox("I am a:", ["student", "teacher"])
            
            join_btn = st.form_submit_button("🔐 JOIN SCHOOL", use_container_width=True)
            
            if join_btn:
                # Check if school exists
                school_file = DATA_DIR / "school.json"
                if school_file.exists():
                    with open(school_file, 'r') as f:
                        school = json.load(f)
                    
                    if school['code'] == school_code:
                        # Load or create users file
                        users_file = DATA_DIR / f"{school_code}_users.json"
                        if users_file.exists():
                            with open(users_file, 'r') as f:
                                users = json.load(f)
                        else:
                            users = []
                        
                        # Add new user
                        new_user = {
                            "email": email,
                            "password": hashlib.sha256(password.encode()).hexdigest(),
                            "name": full_name,
                            "role": role,
                            "joined": datetime.now().strftime("%Y-%m-%d"),
                            "status": "active"
                        }
                        
                        # Check if email exists
                        email_exists = False
                        for u in users:
                            if u['email'] == email:
                                email_exists = True
                                st.error("This email is already registered!")
                                break
                        
                        if not email_exists:
                            users.append(new_user)
                            with open(users_file, 'w') as f:
                                json.dump(users, f, indent=2)
                            
                            # Update school stats
                            if role == "student":
                                school['stats']['students'] += 1
                            else:
                                school['stats']['teachers'] += 1
                            
                            with open(DATA_DIR / "school.json", 'w') as f:
                                json.dump(school, f, indent=2)
                            
                            st.session_state.school = school
                            st.session_state.user = {
                                "email": email,
                                "name": full_name,
                                "role": role,
                                "joined": datetime.now().strftime("%Y-%m-%d")
                            }
                            st.session_state.setup_mode = False
                            st.success("✅ Successfully joined school!")
                            st.rerun()
                    else:
                        st.error("Invalid school code!")
                else:
                    st.error("School not found!")
    
    with col2:
        st.markdown("### 📋 Don't have a code?")
        st.info("""
        **Ask your school administrator for:**
        
        1. Your school's unique **6-digit code**
        2. Use that code to join
        3. Start connecting with your community
        
        If you're the administrator, go back and **create your school first**.
        """)
        
        if st.button("← Back to create school"):
            st.session_state.setup_mode = False
            st.rerun()

# ----- CASE 3: SCHOOL EXISTS -> NORMAL APP -----
elif st.session_state.school and st.session_state.user:
    school = st.session_state.school
    user = st.session_state.user
    
    # Load all data for this school
    users = load_data("users.json", [])
    classes = load_data("classes.json", [])
    announcements = load_data("announcements.json", [])
    assignments = load_data("assignments.json", [])
    
    # ============ SIDEBAR ============
    with st.sidebar:
        st.markdown(f"""
        # 🏫 {school['name']}
        **{school['city']}, {school['state']}**
        Code: `{school['code']}`
        ---
        """)
        
        st.markdown(f"""
        ### 👤 {user['name']}
        **Role:** {user['role'].upper()}
        **Email:** {user['email']}
        **Joined:** {user['joined']}
        ---
        """)
        
        # School Stats
        st.markdown("### 📊 School Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Students", school['stats']['students'])
            st.metric("Classes", school['stats']['classes'])
        with col2:
            st.metric("Teachers", school['stats']['teachers'])
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    
    # ============ MAIN CONTENT ============
    
    # Welcome header
    st.title(f"Welcome to {school['name']}")
    st.markdown(f"*{school.get('motto', 'Learning Together, Growing Together')}*")
    
    # Role-based dashboards
    if user['role'] == 'admin':
        # ===== ADMIN DASHBOARD =====
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📢 Announcements", "👥 Manage Users", "📚 Classes", 
            "📊 Reports", "⚙️ Settings"
        ])
        
        with tab1:
            st.subheader("School Announcements")
            
            # Post announcement
            with st.form("post_announcement"):
                ann_title = st.text_input("Title")
                ann_content = st.text_area("Content")
                ann_audience = st.multiselect("Audience", ["All", "Teachers", "Students", "Parents"])
                
                if st.form_submit_button("📢 Post Announcement"):
                    new_ann = {
                        "id": f"ann_{datetime.now().timestamp()}",
                        "title": ann_title,
                        "content": ann_content,
                        "author": user['name'],
                        "author_role": "admin",
                        "audience": ann_audience,
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "pinned": False
                    }
                    announcements.insert(0, new_ann)
                    save_data("announcements.json", announcements)
                    st.success("Announcement posted!")
                    st.rerun()
            
            # Display announcements
            for ann in announcements[:10]:
                with st.container(border=True):
                    st.markdown(f"### {ann['title']}")
                    st.markdown(ann['content'])
                    st.caption(f"Posted by {ann['author']} on {ann['date']}")
        
        with tab2:
            st.subheader("Manage School Users")
            
            # List all users
            all_users = load_data("users.json", [])
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("### Add New User")
                with st.form("add_user"):
                    new_email = st.text_input("Email")
                    new_name = st.text_input("Full Name")
                    new_role = st.selectbox("Role", ["student", "teacher", "admin"])
                    new_password = st.text_input("Temporary Password", type="password")
                    
                    if st.form_submit_button("➕ Add User"):
                        new_user = {
                            "email": new_email,
                            "name": new_name,
                            "role": new_role,
                            "password": hashlib.sha256(new_password.encode()).hexdigest(),
                            "joined": datetime.now().strftime("%Y-%m-%d"),
                            "status": "active"
                        }
                        all_users.append(new_user)
                        save_data("users.json", all_users)
                        
                        # Update stats
                        if new_role == "student":
                            school['stats']['students'] += 1
                        elif new_role == "teacher":
                            school['stats']['teachers'] += 1
                        save_school(school)
                        
                        st.success(f"Added {new_name} as {new_role}")
                        st.rerun()
            
            with col2:
                st.markdown("### Current Users")
                for u in all_users:
                    with st.expander(f"{u['name']} - {u['role']}"):
                        st.markdown(f"**Email:** {u['email']}")
                        st.markdown(f"**Joined:** {u['joined']}")
                        st.markdown(f"**Status:** {u.get('status', 'active')}")
                        if st.button(f"Deactivate", key=f"deact_{u['email']}"):
                            u['status'] = 'inactive'
                            save_data("users.json", all_users)
                            st.rerun()
        
        with tab3:
            st.subheader("Manage Classes")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("### Create New Class")
                with st.form("create_class"):
                    class_name = st.text_input("Class Name")
                    class_code = st.text_input("Class Code")
                    teacher_email = st.selectbox(
                        "Teacher",
                        [u['email'] for u in users if u['role'] == 'teacher']
                    )
                    room = st.text_input("Room")
                    
                    if st.form_submit_button("➕ Create Class"):
                        new_class = {
                            "id": f"cls_{datetime.now().timestamp()}",
                            "name": class_name,
                            "code": class_code,
                            "teacher": teacher_email,
                            "room": room,
                            "students": [],
                            "created": datetime.now().strftime("%Y-%m-%d")
                        }
                        classes.append(new_class)
                        save_data("classes.json", classes)
                        school['stats']['classes'] += 1
                        save_school(school)
                        st.success(f"Class {class_name} created!")
                        st.rerun()
    
    elif user['role'] == 'teacher':
        # ===== TEACHER DASHBOARD =====
        tab1, tab2, tab3 = st.tabs(["📢 Announcements", "📚 My Classes", "📝 Assignments"])
        
        with tab1:
            st.subheader("Post Class Announcement")
            with st.form("teacher_announcement"):
                ann_title = st.text_input("Title")
                ann_content = st.text_area("Content")
                class_choice = st.selectbox(
                    "Class",
                    [c['name'] for c in classes if c.get('teacher') == user['email']]
                )
                
                if st.form_submit_button("📢 Post"):
                    new_ann = {
                        "title": ann_title,
                        "content": ann_content,
                        "class": class_choice,
                        "author": user['name'],
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                    }
                    announcements.insert(0, new_ann)
                    save_data("announcements.json", announcements)
                    st.success("Posted!")
                    st.rerun()
    
    else:  # STUDENT
        # ===== STUDENT DASHBOARD =====
        st.subheader("📚 My Classes")
        
        # Find classes this student is in
        my_classes = [c for c in classes if user['email'] in c.get('students', [])]
        
        if my_classes:
            for c in my_classes:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"### {c['name']}")
                        st.markdown(f"**Teacher:** {c['teacher']} | **Room:** {c['room']}")
                    with col2:
                        st.button("View Class", key=f"view_{c['id']}")
        else:
            st.info("You're not enrolled in any classes yet. Ask your teacher to add you.")
        
        # Show announcements
        st.subheader("📢 Recent Announcements")
        for ann in announcements[:5]:
            with st.container(border=True):
                st.markdown(f"**{ann['title']}**")
                st.markdown(ann['content'])
                st.caption(f"Posted by {ann['author']} on {ann['date']}")

# ----- CASE 4: LOGGED OUT BUT SCHOOL EXISTS -----
elif st.session_state.school and not st.session_state.user:
    school = st.session_state.school
    
    st.title(f"🏫 {school['name']}")
    st.markdown(f"*{school['city']}, {school['state']}*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔐 Login")
        with st.form("login"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            
            if st.form_submit_button("Login", use_container_width=True):
                # Load users
                users = load_data("users.json", [])
                
                # Check credentials
                hashed_pw = hashlib.sha256(password.encode()).hexdigest()
                found_user = None
                
                for u in users:
                    if u['email'] == email and u['password'] == hashed_pw:
                        found_user = u
                        break
                
                if found_user:
                    st.session_state.user = {
                        "email": found_user['email'],
                        "name": found_user['name'],
                        "role": found_user['role'],
                        "joined": found_user['joined']
                    }
                    st.rerun()
                else:
                    st.error("Invalid email or password")
    
    with col2:
        st.markdown("### 📋 School Information")
        st.markdown(f"""
        **Principal:** {school.get('principal', 'Not set')}
        **Established:** {school.get('established', 'Not set')}
        **Students:** {school['stats']['students']}
        **Teachers:** {school['stats']['teachers']}
        **Classes:** {school['stats']['classes']}
        """)
        
        st.markdown("### 🆕 New User?")
        st.markdown(f"Use school code: **`{school['code']}`**")
        if st.button("Join this school"):
            st.session_state.setup_mode = "join"
            st.rerun()
