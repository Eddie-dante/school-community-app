import streamlit as st
from datetime import datetime
import hashlib
import json
import random
import string
from pathlib import Path
from PIL import Image
import base64
from io import BytesIO

# ============ CONFIG ============
st.set_page_config(
    page_title="School Community System",
    page_icon="🏫",
    layout="wide"
)

# ============ CODE GENERATOR ============
def generate_code(prefix, length=6):
    """Generate unique code: e.g., TCH-7K9M, CLS-MATH101, GRP-3B8F"""
    chars = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choices(chars, k=length))
    return f"{prefix}-{random_part}"

# ============ DATA STORAGE ============
DATA_DIR = Path("school_data")
DATA_DIR.mkdir(exist_ok=True)

def load_school():
    school_file = DATA_DIR / "active_school.json"
    if school_file.exists():
        with open(school_file, 'r') as f:
            return json.load(f)
    return None

def save_school(school):
    with open(DATA_DIR / "active_school.json", 'w') as f:
        json.dump(school, f, indent=2)

def load_data(school_code, filename, default):
    filepath = DATA_DIR / f"{school_code}_{filename}"
    if filepath.exists():
        with open(filepath, 'r') as f:
            return json.load(f)
    return default

def save_data(school_code, filename, data):
    with open(DATA_DIR / f"{school_code}_{filename}", 'w') as f:
        json.dump(data, f, indent=2)

# ============ SESSION STATE ============
if 'user' not in st.session_state:
    st.session_state.user = None
if 'school' not in st.session_state:
    st.session_state.school = load_school()
if 'page' not in st.session_state:
    st.session_state.page = 'main'

# ============ MAIN APP ============

# ----- CASE 1: NO SCHOOL EXISTS (FIRST TIME SETUP) -----
if not st.session_state.school:
    st.title("🏫 School Community System - Setup")
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.markdown("""
        ### 👑 Create Your School
        
        You are the **FOUNDER & ADMINISTRATOR**. 
        Create your school community from scratch.
        """)
        
        with st.form("create_school_form"):
            school_name = st.text_input("🏫 School Name", placeholder="e.g., Springfield High School")
            admin_fullname = st.text_input("👤 Your Full Name", placeholder="e.g., Dr. Sarah Johnson")
            admin_email = st.text_input("📧 Your Email", placeholder="admin@springfield.edu")
            admin_password = st.text_input("🔐 Create Password", type="password")
            
            col1_1, col1_2 = st.columns(2)
            with col1_1:
                city = st.text_input("City", placeholder="Springfield")
            with col1_2:
                state = st.text_input("State/Province", placeholder="IL")
            
            school_motto = st.text_input("✨ School Motto", placeholder="Excellence Through Community")
            
            submitted = st.form_submit_button("🚀 CREATE SCHOOL COMMUNITY", use_container_width=True)
            
            if submitted:
                if school_name and admin_email and admin_password:
                    # Generate UNIQUE SCHOOL CODE
                    school_code = generate_code("SCH", 6).replace("-", "")
                    
                    # Create school object
                    school = {
                        "code": school_code,
                        "name": school_name,
                        "city": city,
                        "state": state,
                        "motto": school_motto,
                        "founded": datetime.now().strftime("%Y-%m-%d"),
                        "admin": {
                            "fullname": admin_fullname,
                            "email": admin_email,
                            "password": hashlib.sha256(admin_password.encode()).hexdigest()
                        },
                        "stats": {
                            "students": 0,
                            "teachers": 0,
                            "classes": 0,
                            "groups": 0
                        }
                    }
                    
                    # Save school
                    save_school(school)
                    
                    # Create initial admin user
                    users = [{
                        "user_id": generate_code("USR", 8),
                        "email": admin_email,
                        "fullname": admin_fullname,
                        "password": hashlib.sha256(admin_password.encode()).hexdigest(),
                        "role": "admin",
                        "title": "School Administrator",
                        "profile_pic": None,
                        "bio": "School Founder",
                        "phone": "",
                        "joined": datetime.now().strftime("%Y-%m-%d"),
                        "status": "active",
                        "school_code": school_code
                    }]
                    save_data(school_code, "users.json", users)
                    
                    # Initialize other data files
                    save_data(school_code, "teachers.json", [])
                    save_data(school_code, "students.json", [])
                    save_data(school_code, "classes.json", [])
                    save_data(school_code, "groups.json", [])
                    save_data(school_code, "announcements.json", [])
                    save_data(school_code, "assignments.json", [])
                    save_data(school_code, "resources.json", [])
                    save_data(school_code, "events.json", [])
                    save_data(school_code, "discussions.json", [])
                    
                    st.session_state.school = school
                    st.session_state.user = users[0]
                    st.success(f"✅ School created! Your school code is: **{school_code}**")
                    st.rerun()
    
    with col2:
        st.markdown("""
        ### 📋 Your School Credentials
        
        **After creation, you will receive:**
        
        ```
        🔑 SCHOOL CODE: SCH-XXXXXX
        👑 ADMIN CODE: ADMIN-XXXXXX
        ```
        
        ### 🎯 Your Responsibilities:
        
        1. **Share school code** with everyone
        2. **Generate teacher codes** for staff
        3. **Monitor all activities**
        4. **Manage school settings**
        
        ### 📌 Important:
        
        Save your school code! You'll need it to login.
        """)
        
        st.markdown("---")
        st.markdown("**Already have a school code?**")
        if st.button("🔑 Join Existing School", use_container_width=True):
            st.session_state.page = 'join'
            st.rerun()

# ----- CASE 2: JOIN EXISTING SCHOOL -----
elif st.session_state.page == 'join':
    st.title("🔐 Join Your School Community")
    
    col1, col2 = st.columns([1.2, 0.8])
    
    with col1:
        st.markdown("""
        ### Enter Your School Code
        
        Get this 6-digit code from your school administrator.
        """)
        
        with st.form("join_school_form"):
            school_code = st.text_input("🏫 School Code", placeholder="e.g., SCH-ABC123", 
                                       help="The 6-digit code from your admin").upper()
            
            st.markdown("---")
            st.markdown("### 👤 Your Information")
            
            fullname = st.text_input("📝 Your Full Name", placeholder="e.g., John Smith")
            email = st.text_input("📧 Your Email", placeholder="john@example.com")
            password = st.text_input("🔐 Create Password", type="password")
            confirm_password = st.text_input("🔐 Confirm Password", type="password")
            
            role = st.radio("I am a:", ["👨‍🎓 Student", "👨‍🏫 Teacher"], horizontal=True)
            
            if role == "👨‍🏫 Teacher":
                teacher_code = st.text_input("🔑 Teacher Code", placeholder="e.g., TCH-X7K9M",
                                           help="Get this code from your admin")
            
            submitted = st.form_submit_button("✅ JOIN SCHOOL", use_container_width=True)
            
            if submitted:
                # Check if school exists
                school_file = DATA_DIR / "active_school.json"
                if school_file.exists():
                    with open(school_file, 'r') as f:
                        school = json.load(f)
                    
                    if school['code'] == school_code:
                        # Load users
                        users = load_data(school_code, "users.json", [])
                        
                        # Check if email exists
                        if any(u['email'] == email for u in users):
                            st.error("❌ This email is already registered!")
                        elif password != confirm_password:
                            st.error("❌ Passwords don't match!")
                        else:
                            if role == "👨‍🏫 Teacher":
                                # Verify teacher code
                                teachers = load_data(school_code, "teachers.json", [])
                                valid_code = False
                                for t in teachers:
                                    if t['code'] == teacher_code and t['status'] == 'pending':
                                        valid_code = True
                                        t['status'] = 'active'
                                        t['used_by'] = email
                                        break
                                
                                if not valid_code:
                                    st.error("❌ Invalid or expired teacher code!")
                                    st.stop()
                            
                            # Create user
                            new_user = {
                                "user_id": generate_code("USR", 8),
                                "email": email,
                                "fullname": fullname,
                                "password": hashlib.sha256(password.encode()).hexdigest(),
                                "role": "student" if "Student" in role else "teacher",
                                "profile_pic": None,
                                "bio": "",
                                "phone": "",
                                "joined": datetime.now().strftime("%Y-%m-%d"),
                                "status": "active",
                                "school_code": school_code,
                                "classes": [],
                                "groups": []
                            }
                            
                            users.append(new_user)
                            save_data(school_code, "users.json", users)
                            
                            # Update stats
                            if "Student" in role:
                                school['stats']['students'] += 1
                            else:
                                school['stats']['teachers'] += 1
                            save_school(school)
                            
                            st.session_state.school = school
                            st.session_state.user = new_user
                            st.session_state.page = 'main'
                            st.success("✅ Successfully joined school!")
                            st.rerun()
                    else:
                        st.error("❌ School code not found!")
                else:
                    st.error("❌ No active school found!")
    
    with col2:
        st.markdown("""
        ### 📋 Need Help?
        
        **Don't have a school code?**
        
        Contact your school administrator.
        
        **Are you an administrator?**
        
        """)
        if st.button("👑 Create School Instead"):
            st.session_state.page = 'main'
            st.rerun()

# ----- CASE 3: SCHOOL EXISTS - MAIN APPLICATION -----
elif st.session_state.school and st.session_state.user:
    school = st.session_state.school
    user = st.session_state.user
    
    # Load all school data
    users = load_data(school['code'], "users.json", [])
    teachers = load_data(school['code'], "teachers.json", [])
    students = load_data(school['code'], "students.json", [])
    classes = load_data(school['code'], "classes.json", [])
    groups = load_data(school['code'], "groups.json", [])
    announcements = load_data(school['code'], "announcements.json", [])
    assignments = load_data(school['code'], "assignments.json", [])
    resources = load_data(school['code'], "resources.json", [])
    events = load_data(school['code'], "events.json", [])
    discussions = load_data(school['code'], "discussions.json", [])
    
    # ============ SIDEBAR ============
    with st.sidebar:
        # School Header
        st.markdown(f"""
        # 🏫 {school['name']}
        *{school['motto']}*
        
        **School Code:** `{school['code']}`
        ---
        """)
        
        # User Profile Section
        col1, col2 = st.columns([1, 2])
        with col1:
            if user.get('profile_pic'):
                st.image(user['profile_pic'], width=60)
            else:
                if user['role'] == 'admin':
                    st.markdown("👑" * 3)
                elif user['role'] == 'teacher':
                    st.markdown("👨‍🏫" * 3)
                else:
                    st.markdown("👨‍🎓" * 3)
        
        with col2:
            st.markdown(f"""
            **{user['fullname']}**
            `{user['role'].upper()}`
            {user['email']}
            """)
        
        # Navigation
        st.markdown("---")
        st.markdown("### 📌 Navigation")
        
        if user['role'] == 'admin':
            menu = st.radio("", [
                "🏠 Dashboard",
                "📢 Announcements",
                "👥 Manage Teachers",
                "📚 Manage Classes",
                "👨‍🎓 Manage Students",
                "🔑 Generate Codes",
                "📊 School Reports",
                "⚙️ Settings",
                "👤 My Profile"
            ])
        elif user['role'] == 'teacher':
            menu = st.radio("", [
                "🏠 Dashboard",
                "📢 Announcements",
                "📚 My Classes",
                "👥 My Groups",
                "📝 Assignments",
                "📎 Resources",
                "💬 Discussions",
                "📊 Grade Book",
                "👤 My Profile"
            ])
        else:  # student
            menu = st.radio("", [
                "🏠 Dashboard",
                "📢 Announcements",
                "📚 My Classes",
                "👥 My Groups",
                "📝 Homework",
                "📎 Study Materials",
                "💬 Discussion Board",
                "📅 Events",
                "📊 My Grades",
                "👤 My Profile"
            ])
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = 'main'
            st.rerun()
    
    # ============ MAIN CONTENT ============
    
    # ----- ADMIN DASHBOARD -----
    if user['role'] == 'admin':
        
        if menu == "🏠 Dashboard":
            st.title(f"👑 Admin Dashboard - {school['name']}")
            
            # Key Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("👨‍🎓 Total Students", school['stats']['students'])
            with col2:
                st.metric("👨‍🏫 Total Teachers", school['stats']['teachers'])
            with col3:
                st.metric("📚 Total Classes", school['stats']['classes'])
            with col4:
                st.metric("👥 Total Groups", school['stats'].get('groups', 0))
            
            st.divider()
            
            # Quick Actions
            col1, col2, col3 = st.columns(3)
            with col1:
                with st.container(border=True):
                    st.markdown("### 🔑 Generate Teacher Codes")
                    st.markdown("Create codes for new teachers to join")
                    if st.button("Generate New Code", key="gen_teacher"):
                        teacher_code = generate_code("TCH", 6)
                        teachers.append({
                            "code": teacher_code,
                            "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "status": "pending",
                            "used_by": None
                        })
                        save_data(school['code'], "teachers.json", teachers)
                        st.success(f"Teacher Code: **{teacher_code}**")
                        st.rerun()
            
            with col2:
                with st.container(border=True):
                    st.markdown("### 📚 Create Class")
                    st.markdown("Create a new class and generate class code")
                    if st.button("Create New Class", key="create_class_btn"):
                        st.session_state.page = 'create_class'
                        st.rerun()
            
            with col3:
                with st.container(border=True):
                    st.markdown("### 📢 Post Announcement")
                    st.markdown("Share news with the whole school")
                    if st.button("New Announcement", key="new_announcement"):
                        st.session_state.page = 'new_announcement'
                        st.rerun()
            
            # Recent Activity
            st.divider()
            st.subheader("📋 Recent Activity")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Recent Teachers Joined**")
                recent_teachers = [t for t in teachers if t.get('status') == 'active'][:5]
                for t in recent_teachers:
                    st.markdown(f"- {t.get('used_by', 'Unknown')} joined using code `{t['code']}`")
            
            with col2:
                st.markdown("**Recent Classes Created**")
                recent_classes = classes[-5:]
                for c in recent_classes:
                    st.markdown(f"- **{c['name']}** - Code: `{c['code']}`")
        
        elif menu == "🔑 Generate Codes":
            st.title("🔑 Code Generation Center")
            
            tab1, tab2, tab3, tab4 = st.tabs(["👨‍🏫 Teacher Codes", "📚 Class Codes", "👥 Group Codes", "📎 Resource Codes"])
            
            with tab1:
                st.subheader("Generate Teacher Registration Codes")
                st.markdown("Teachers will use these codes to join your school")
                
                col1, col2 = st.columns([1, 1])
                with col1:
                    num_codes = st.number_input("Number of codes to generate", min_value=1, max_value=20, value=1)
                    if st.button("Generate Teacher Codes", use_container_width=True):
                        for _ in range(num_codes):
                            teacher_code = generate_code("TCH", 6)
                            teachers.append({
                                "code": teacher_code,
                                "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "status": "pending",
                                "used_by": None
                            })
                        save_data(school['code'], "teachers.json", teachers)
                        st.success(f"✅ Generated {num_codes} teacher code(s)!")
                        st.rerun()
                
                with col2:
                    st.markdown("### Active Teacher Codes")
                    pending_codes = [t for t in teachers if t['status'] == 'pending']
                    if pending_codes:
                        for t in pending_codes:
                            st.code(t['code'])
                    else:
                        st.info("No pending teacher codes")
            
            with tab2:
                st.subheader("Class Codes")
                st.markdown("Each class gets a unique code for students to join")
                
                if classes:
                    for c in classes:
                        with st.container(border=True):
                            col1, col2 = st.columns([2, 1])
                            with col1:
                                st.markdown(f"**{c['name']}**")
                                st.markdown(f"Teacher: {c['teacher']}")
                            with col2:
                                st.code(c['code'])
                else:
                    st.info("No classes created yet")
        
        elif menu == "👥 Manage Teachers":
            st.title("👨‍🏫 Teacher Management")
            
            col1, col2 = st.columns([1, 1.5])
            
            with col1:
                st.subheader("Generate Teacher Code")
                if st.button("➕ Generate New Teacher Code", use_container_width=True):
                    teacher_code = generate_code("TCH", 6)
                    teachers.append({
                        "code": teacher_code,
                        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "status": "pending",
                        "used_by": None
                    })
                    save_data(school['code'], "teachers.json", teachers)
                    st.success(f"Code: {teacher_code}")
                    st.rerun()
                
                st.divider()
                st.subheader("Pending Codes")
                pending = [t for t in teachers if t['status'] == 'pending']
                for t in pending:
                    st.code(t['code'])
            
            with col2:
                st.subheader("Active Teachers")
                active_teachers = [u for u in users if u['role'] == 'teacher']
                for t in active_teachers:
                    with st.container(border=True):
                        st.markdown(f"**{t['fullname']}**")
                        st.markdown(f"📧 {t['email']}")
                        st.markdown(f"📅 Joined: {t['joined']}")
        
        elif menu == "📚 Manage Classes":
            st.title("📚 Class Management")
            
            col1, col2 = st.columns([1, 1.5])
            
            with col1:
                st.subheader("Create New Class")
                with st.form("create_class_form"):
                    class_name = st.text_input("Class Name", placeholder="e.g., Mathematics 101")
                    class_subject = st.text_input("Subject", placeholder="Mathematics")
                    class_grade = st.selectbox("Grade Level", ["9", "10", "11", "12"])
                    
                    # Get active teachers
                    active_teachers = [u for u in users if u['role'] == 'teacher']
                    teacher_options = {f"{t['fullname']} ({t['email']})": t['email'] for t in active_teachers}
                    
                    if teacher_options:
                        selected_teacher = st.selectbox("Assign Teacher", list(teacher_options.keys()))
                        teacher_email = teacher_options[selected_teacher]
                    else:
                        st.warning("No teachers available. Create teacher codes first.")
                        teacher_email = None
                    
                    class_room = st.text_input("Room Number", placeholder="201")
                    
                    if st.form_submit_button("✅ Create Class", use_container_width=True):
                        if class_name and teacher_email:
                            class_code = generate_code("CLS", 6)
                            
                            new_class = {
                                "id": generate_code("CID", 4),
                                "code": class_code,
                                "name": class_name,
                                "subject": class_subject,
                                "grade": class_grade,
                                "teacher": teacher_email,
                                "room": class_room,
                                "students": [],
                                "created": datetime.now().strftime("%Y-%m-%d"),
                                "schedule": {},
                                "resources": []
                            }
                            
                            classes.append(new_class)
                            save_data(school['code'], "classes.json", classes)
                            school['stats']['classes'] += 1
                            save_school(school)
                            
                            st.success(f"✅ Class created! Code: {class_code}")
                            st.rerun()
            
            with col2:
                st.subheader("All Classes")
                for c in classes:
                    with st.expander(f"📖 {c['name']} - {c.get('code', 'No Code')}"):
                        st.markdown(f"**Teacher:** {c['teacher']}")
                        st.markdown(f"**Room:** {c.get('room', 'TBD')}")
                        st.markdown(f"**Students Enrolled:** {len(c.get('students', []))}")
                        st.markdown(f"**Class Code:** `{c.get('code', 'N/A')}`")
                        
                        if st.button(f"View Class Details", key=f"view_{c['id']}"):
                            st.session_state.view_class = c
                            st.rerun()
        
        elif menu == "👤 My Profile":
            st.title("👤 My Profile")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("Profile Picture")
                if user.get('profile_pic'):
                    st.image(user['profile_pic'], width=200)
                else:
                    st.markdown("👑" * 10)
                
                uploaded_file = st.file_uploader("Upload Photo", type=['png', 'jpg', 'jpeg'])
                if uploaded_file:
                    # Convert image to base64
                    image = Image.open(uploaded_file)
                    buffered = BytesIO()
                    image.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    # Update user profile
                    for u in users:
                        if u['email'] == user['email']:
                            u['profile_pic'] = f"data:image/png;base64,{img_str}"
                            break
                    
                    save_data(school['code'], "users.json", users)
                    user['profile_pic'] = f"data:image/png;base64,{img_str}"
                    st.success("Profile picture updated!")
                    st.rerun()
            
            with col2:
                st.subheader("Edit Profile")
                with st.form("edit_profile"):
                    fullname = st.text_input("Full Name", value=user.get('fullname', ''))
                    email = st.text_input("Email", value=user.get('email', ''), disabled=True)
                    phone = st.text_input("Phone Number", value=user.get('phone', ''))
                    bio = st.text_area("Bio", value=user.get('bio', ''), height=100)
                    
                    if st.form_submit_button("💾 Update Profile"):
                        for u in users:
                            if u['email'] == user['email']:
                                u['fullname'] = fullname
                                u['phone'] = phone
                                u['bio'] = bio
                                break
                        
                        save_data(school['code'], "users.json", users)
                        user['fullname'] = fullname
                        user['phone'] = phone
                        user['bio'] = bio
                        st.success("Profile updated!")
                        st.rerun()
    
    # ----- TEACHER DASHBOARD -----
    elif user['role'] == 'teacher':
        
        if menu == "🏠 Dashboard":
            st.title(f"👨‍🏫 Welcome, {user['fullname']}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                my_classes = [c for c in classes if c.get('teacher') == user['email']]
                st.metric("📚 My Classes", len(my_classes))
            with col2:
                my_groups = [g for g in groups if g.get('teacher') == user['email']]
                st.metric("👥 My Groups", len(my_groups))
            with col3:
                active_assignments = [a for a in assignments if a.get('teacher') == user['email']]
                st.metric("📝 Active Assignments", len(active_assignments))
            
            st.divider()
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("My Classes")
                for c in my_classes[:3]:
                    with st.container(border=True):
                        st.markdown(f"**{c['name']}** - Code: `{c['code']}`")
                        st.markdown(f"Students: {len(c.get('students', []))}")
            
            with col2:
                st.subheader("Recent Activity")
                # Show recent announcements by this teacher
                teacher_announcements = [a for a in announcements if a.get('author') == user['email']][:3]
                for a in teacher_announcements:
                    st.markdown(f"- {a['title']}")
        
        elif menu == "📚 My Classes":
            st.title("📚 My Classes")
            
            my_classes = [c for c in classes if c.get('teacher') == user['email']]
            
            for c in my_classes:
                with st.expander(f"📖 {c['name']} - {c['code']}", expanded=True):
                    tab1, tab2, tab3, tab4 = st.tabs(["📝 Info", "👥 Students", "📎 Resources", "⚙️ Settings"])
                    
                    with tab1:
                        st.markdown(f"**Class Code:** `{c['code']}`")
                        st.markdown(f"**Subject:** {c.get('subject', 'N/A')}")
                        st.markdown(f"**Room:** {c.get('room', 'N/A')}")
                        st.markdown(f"**Students Enrolled:** {len(c.get('students', []))}")
                        
                        # QR Code placeholder
                        st.info(f"Students join with code: {c['code']}")
                    
                    with tab2:
                        st.subheader("Enrolled Students")
                        enrolled_students = [u for u in users if u['email'] in c.get('students', [])]
                        
                        for s in enrolled_students:
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.markdown(f"**{s['fullname']}**")
                                st.markdown(f"📧 {s['email']}")
                            with col2:
                                st.markdown(f"Joined: {s.get('joined', 'N/A')}")
                            st.divider()
                        
                        st.markdown("---")
                        st.markdown("**Add Student Manually**")
                        add_email = st.text_input("Student Email", key=f"add_{c['code']}")
                        if st.button("Add Student", key=f"add_btn_{c['code']}"):
                            if add_email and add_email not in c['students']:
                                c['students'].append(add_email)
                                save_data(school['code'], "classes.json", classes)
                                st.success(f"Added {add_email} to class!")
                                st.rerun()
        
        elif menu == "📝 Assignments":
            st.title("📝 Create Assignment")
            
            my_classes = [c['name'] for c in classes if c.get('teacher') == user['email']]
            
            if my_classes:
                with st.form("create_assignment"):
                    class_name = st.selectbox("Select Class", my_classes)
                    title = st.text_input("Assignment Title")
                    description = st.text_area("Description")
                    due_date = st.date_input("Due Date")
                    total_points = st.number_input("Total Points", min_value=1, value=100)
                    assignment_code = generate_code("ASN", 6)
                    
                    if st.form_submit_button("✅ Create Assignment"):
                        new_assignment = {
                            "code": assignment_code,
                            "class": class_name,
                            "teacher": user['email'],
                            "title": title,
                            "description": description,
                            "due": due_date.strftime("%Y-%m-%d"),
                            "points": total_points,
                            "created": datetime.now().strftime("%Y-%m-%d"),
                            "submissions": []
                        }
                        assignments.append(new_assignment)
                        save_data(school['code'], "assignments.json", assignments)
                        st.success(f"Assignment created! Code: {assignment_code}")
                        st.rerun()
            else:
                st.warning("You don't have any classes yet.")
        
        elif menu == "👤 My Profile":
            st.title("👤 My Profile")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("Profile Picture")
                if user.get('profile_pic'):
                    st.image(user['profile_pic'], width=200)
                else:
                    st.markdown("👨‍🏫" * 10)
                
                uploaded_file = st.file_uploader("Upload Photo", type=['png', 'jpg', 'jpeg'])
                if uploaded_file:
                    image = Image.open(uploaded_file)
                    buffered = BytesIO()
                    image.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    for u in users:
                        if u['email'] == user['email']:
                            u['profile_pic'] = f"data:image/png;base64,{img_str}"
                            break
                    
                    save_data(school['code'], "users.json", users)
                    user['profile_pic'] = f"data:image/png;base64,{img_str}"
                    st.success("Profile picture updated!")
                    st.rerun()
            
            with col2:
                st.subheader("Edit Profile")
                with st.form("edit_teacher_profile"):
                    fullname = st.text_input("Full Name", value=user.get('fullname', ''))
                    email = st.text_input("Email", value=user.get('email', ''), disabled=True)
                    phone = st.text_input("Phone Number", value=user.get('phone', ''))
                    bio = st.text_area("Bio", value=user.get('bio', ''), height=100)
                    
                    if st.form_submit_button("💾 Update Profile"):
                        for u in users:
                            if u['email'] == user['email']:
                                u['fullname'] = fullname
                                u['phone'] = phone
                                u['bio'] = bio
                                break
                        
                        save_data(school['code'], "users.json", users)
                        user['fullname'] = fullname
                        user['phone'] = phone
                        user['bio'] = bio
                        st.success("Profile updated!")
                        st.rerun()
    
    # ----- STUDENT DASHBOARD -----
    else:  # student
        if menu == "🏠 Dashboard":
            st.title(f"👨‍🎓 Welcome, {user['fullname']}")
            
            # Get student's classes
            my_classes = [c for c in classes if user['email'] in c.get('students', [])]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📚 My Classes", len(my_classes))
            with col2:
                upcoming_assignments = [a for a in assignments if a.get('class') in [c['name'] for c in my_classes]][:3]
                st.metric("📝 Due This Week", len(upcoming_assignments))
            with col3:
                st.metric("👥 Study Groups", len(user.get('groups', [])))
            
            st.divider()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📚 My Classes")
                for c in my_classes[:3]:
                    with st.container(border=True):
                        st.markdown(f"**{c['name']}**")
                        st.markdown(f"Teacher: {c['teacher']}")
                        st.markdown(f"Room: {c.get('room', 'TBD')}")
                        st.markdown(f"Class Code: `{c['code']}`")
            
            with col2:
                st.subheader("📝 Upcoming Homework")
                for a in upcoming_assignments:
                    with st.container(border=True):
                        st.markdown(f"**{a['title']}**")
                        st.markdown(f"Class: {a['class']}")
                        st.markdown(f"Due: {a['due']}")
        
        elif menu == "📚 My Classes":
            st.title("📚 My Classes")
            
            my_classes = [c for c in classes if user['email'] in c.get('students', [])]
            
            if my_classes:
                for c in my_classes:
                    with st.expander(f"📖 {c['name']} - {c['code']}", expanded=True):
                        st.markdown(f"**Teacher:** {c['teacher']}")
                        st.markdown(f"**Room:** {c.get('room', 'TBD')}")
                        
                        # Get class assignments
                        class_assignments = [a for a in assignments if a.get('class') == c['name']]
                        if class_assignments:
                            st.markdown("**📝 Assignments:**")
                            for a in class_assignments:
                                st.markdown(f"- {a['title']} (Due: {a['due']})")
                        
                        # Join button if not enrolled
                        if user['email'] not in c.get('students', []):
                            if st.button(f"Join {c['name']}", key=f"join_{c['code']}"):
                                c['students'].append(user['email'])
                                save_data(school['code'], "classes.json", classes)
                                st.success(f"Joined {c['name']}!")
                                st.rerun()
            else:
                st.info("You haven't joined any classes yet.")
                st.markdown("### 🔑 Join a Class")
                join_code = st.text_input("Enter Class Code", placeholder="e.g., CLS-ABC123")
                if st.button("Join Class"):
                    for c in classes:
                        if c['code'] == join_code:
                            if user['email'] not in c['students']:
                                c['students'].append(user['email'])
                                save_data(school['code'], "classes.json", classes)
                                st.success(f"Joined {c['name']}!")
                                st.rerun()
        
        elif menu == "👤 My Profile":
            st.title("👤 My Profile")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("Profile Picture")
                if user.get('profile_pic'):
                    st.image(user['profile_pic'], width=200)
                else:
                    st.markdown("👨‍🎓" * 10)
                
                uploaded_file = st.file_uploader("Upload Photo", type=['png', 'jpg', 'jpeg'])
                if uploaded_file:
                    image = Image.open(uploaded_file)
                    buffered = BytesIO()
                    image.save(buffered, format="PNG")
                    img_str = base64.b64encode(buffered.getvalue()).decode()
                    
                    for u in users:
                        if u['email'] == user['email']:
                            u['profile_pic'] = f"data:image/png;base64,{img_str}"
                            break
                    
                    save_data(school['code'], "users.json", users)
                    user['profile_pic'] = f"data:image/png;base64,{img_str}"
                    st.success("Profile picture updated!")
                    st.rerun()
            
            with col2:
                st.subheader("Edit Profile")
                with st.form("edit_student_profile"):
                    fullname = st.text_input("Full Name", value=user.get('fullname', ''))
                    email = st.text_input("Email", value=user.get('email', ''), disabled=True)
                    phone = st.text_input("Phone Number", value=user.get('phone', ''))
                    bio = st.text_area("Bio", value=user.get('bio', ''), height=100)
                    
                    if st.form_submit_button("💾 Update Profile"):
                        for u in users:
                            if u['email'] == user['email']:
                                u['fullname'] = fullname
                                u['phone'] = phone
                                u['bio'] = bio
                                break
                        
                        save_data(school['code'], "users.json", users)
                        user['fullname'] = fullname
                        user['phone'] = phone
                        user['bio'] = bio
                        st.success("Profile updated!")
                        st.rerun()
