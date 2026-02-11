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
    """Generate unique code with prefix"""
    chars = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choices(chars, k=length))
    return f"{prefix}-{random_part}"

def generate_teacher_code(teacher_name):
    """Generate teacher code with name embedded"""
    # Take first 3 letters of name, uppercase, remove spaces
    name_part = ''.join([c for c in teacher_name.split()[0][:3].upper() if c.isalnum()])
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"TCH-{name_part}{random_part}"

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
    if not school_code:
        return default
    filepath = DATA_DIR / f"{school_code}_{filename}"
    if filepath.exists():
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except:
            return default
    return default

def save_data(school_code, filename, data):
    if school_code:
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

# ----- CASE 1: NO SCHOOL EXISTS -----
if not st.session_state.school and st.session_state.page != 'join':
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
                            "groups": 0,
                            "announcements": 0
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
                        "bio": "School Founder and Administrator",
                        "phone": "",
                        "joined": datetime.now().strftime("%Y-%m-%d"),
                        "status": "active",
                        "school_code": school_code
                    }]
                    save_data(school_code, "users.json", users)
                    
                    # Initialize all data files
                    save_data(school_code, "teachers.json", [])
                    save_data(school_code, "students.json", [])
                    save_data(school_code, "classes.json", [])
                    save_data(school_code, "groups.json", [])
                    save_data(school_code, "announcements.json", [])
                    save_data(school_code, "assignments.json", [])
                    save_data(school_code, "resources.json", [])
                    save_data(school_code, "events.json", [])
                    save_data(school_code, "discussions.json", [])
                    save_data(school_code, "grades.json", [])
                    save_data(school_code, "attendance.json", [])
                    
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
        
        Get this code from your school administrator.
        """)
        
        with st.form("join_school_form"):
            school_code = st.text_input("🏫 School Code", placeholder="e.g., SCH-ABC123", 
                                       help="The code from your admin").upper()
            
            st.markdown("---")
            st.markdown("### 👤 Your Information")
            
            fullname = st.text_input("📝 Your Full Name", placeholder="e.g., John Smith")
            email = st.text_input("📧 Your Email", placeholder="john@example.com")
            password = st.text_input("🔐 Create Password", type="password")
            confirm_password = st.text_input("🔐 Confirm Password", type="password")
            
            role = st.radio("I am a:", ["👨‍🎓 Student", "👨‍🏫 Teacher"], horizontal=True)
            
            teacher_code_input = None
            if role == "👨‍🏫 Teacher":
                teacher_code_input = st.text_input("🔑 Teacher Code", placeholder="e.g., TCH-JOH4K9M",
                                           help="Get your personalized code from admin")
            
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
                                teacher_record = None
                                for t in teachers:
                                    if t['code'] == teacher_code_input and t['status'] == 'pending':
                                        valid_code = True
                                        teacher_record = t
                                        t['status'] = 'active'
                                        t['used_by'] = email
                                        t['used_by_name'] = fullname
                                        t['activated_date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
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
    grades = load_data(school['code'], "grades.json", [])
    attendance = load_data(school['code'], "attendance.json", [])
    
    # ============ SIDEBAR ============
    with st.sidebar:
        # School Header
        st.markdown(f"""
        # 🏫 {school['name']}
        *{school.get('motto', 'Learning Together')}*
        
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
                    st.markdown("# 👑")
                elif user['role'] == 'teacher':
                    st.markdown("# 👨‍🏫")
                else:
                    st.markdown("# 👨‍🎓")
        
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
            menu_options = [
                "🏠 Dashboard",
                "📢 Announcements",
                "👥 Manage Teachers",
                "📚 Manage Classes",
                "👨‍🎓 Manage Students",
                "👥 Manage Groups",
                "🔑 Generate Codes",
                "📊 School Reports",
                "⚙️ Settings",
                "👤 My Profile"
            ]
            selected_index = 0
            if 'menu_index' in st.session_state:
                selected_index = st.session_state.menu_index
            menu = st.radio("", menu_options, index=selected_index, key="admin_menu")
            
        elif user['role'] == 'teacher':
            menu_options = [
                "🏠 Dashboard",
                "📢 Announcements",
                "📚 My Classes",
                "👥 My Groups",
                "📝 Assignments",
                "📎 Resources",
                "💬 Discussions",
                "📊 Grade Book",
                "👤 My Profile"
            ]
            selected_index = 0
            if 'menu_index' in st.session_state:
                selected_index = st.session_state.menu_index
            menu = st.radio("", menu_options, index=selected_index, key="teacher_menu")
            
        else:  # student
            menu_options = [
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
            ]
            selected_index = 0
            if 'menu_index' in st.session_state:
                selected_index = st.session_state.menu_index
            menu = st.radio("", menu_options, index=selected_index, key="student_menu")
        
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = 'main'
            st.rerun()
    
    # ============ MAIN CONTENT ============
    
    # ----- ADMIN DASHBOARD -----
    if user['role'] == 'admin':
        
        # ---------- DASHBOARD ----------
        if menu == "🏠 Dashboard":
            st.title(f"👑 Admin Dashboard - {school['name']}")
            
            # Key Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("👨‍🎓 Total Students", school['stats'].get('students', 0))
            with col2:
                st.metric("👨‍🏫 Total Teachers", school['stats'].get('teachers', 0))
            with col3:
                st.metric("📚 Total Classes", school['stats'].get('classes', 0))
            with col4:
                st.metric("👥 Total Groups", school['stats'].get('groups', 0))
            
            st.divider()
            
            # Quick Actions
            col1, col2, col3 = st.columns(3)
            with col1:
                with st.container(border=True):
                    st.markdown("### 🔑 Generate Teacher Codes")
                    st.markdown("Create personalized codes for new teachers")
                    with st.form("quick_teacher_code"):
                        teacher_name = st.text_input("Teacher Full Name", key="quick_teacher_name")
                        if st.form_submit_button("Generate Code", use_container_width=True):
                            if teacher_name:
                                teacher_code = generate_teacher_code(teacher_name)
                                teachers.append({
                                    "name": teacher_name,
                                    "code": teacher_code,
                                    "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                    "status": "pending",
                                    "used_by": None,
                                    "used_by_name": None
                                })
                                save_data(school['code'], "teachers.json", teachers)
                                st.success(f"✅ Code generated for {teacher_name}: **{teacher_code}**")
                                st.rerun()
            
            with col2:
                with st.container(border=True):
                    st.markdown("### 📚 Create Class")
                    st.markdown("Create a new class with unique code")
                    if st.button("➕ Create New Class", use_container_width=True):
                        st.session_state.menu_index = 2  # Manage Classes tab
                        st.rerun()
            
            with col3:
                with st.container(border=True):
                    st.markdown("### 📢 Post Announcement")
                    st.markdown("Share news with the whole school")
                    if st.button("📝 New Announcement", use_container_width=True):
                        st.session_state.menu_index = 1  # Announcements tab
                        st.rerun()
            
            # Recent Activity
            st.divider()
            st.subheader("📋 Recent Activity")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**📢 Latest Announcements**")
                recent_announcements = announcements[-3:] if announcements else []
                if recent_announcements:
                    for ann in reversed(recent_announcements):
                        with st.container(border=True):
                            st.markdown(f"**{ann['title']}**")
                            st.caption(f"By {ann['author']} on {ann['date']}")
                else:
                    st.info("No announcements yet")
            
            with col2:
                st.markdown("**👨‍🏫 Recently Joined Teachers**")
                active_teachers = [t for t in teachers if t.get('status') == 'active'][-3:]
                if active_teachers:
                    for t in active_teachers:
                        st.markdown(f"- **{t.get('used_by_name', 'Unknown')}** joined with code `{t['code']}`")
                else:
                    st.info("No teachers joined yet")
        
        # ---------- ANNOUNCEMENTS (FIXED) ----------
        elif menu == "📢 Announcements":
            st.title("📢 School Announcements")
            
            col1, col2 = st.columns([1.2, 0.8])
            
            with col1:
                st.subheader("📝 Create New Announcement")
                with st.form("admin_announcement_form"):
                    ann_title = st.text_input("Title", placeholder="e.g., School Closure Tomorrow")
                    ann_content = st.text_area("Content", placeholder="Write your announcement here...", height=150)
                    
                    col_aud1, col_aud2 = st.columns(2)
                    with col_aud1:
                        audience = st.multiselect(
                            "Target Audience",
                            ["All", "Students", "Teachers", "Parents"],
                            default=["All"]
                        )
                    with col_aud2:
                        is_important = st.checkbox("⭐ Mark as Important")
                        is_pinned = st.checkbox("📌 Pin to Top")
                    
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        submitted = st.form_submit_button("📢 Post Announcement", use_container_width=True)
                    with col_btn2:
                        preview = st.form_submit_button("👁️ Preview", use_container_width=True)
                    
                    if submitted:
                        if ann_title and ann_content:
                            new_announcement = {
                                "id": generate_code("ANN", 6),
                                "title": ann_title,
                                "content": ann_content,
                                "author": user['fullname'],
                                "author_email": user['email'],
                                "author_role": "admin",
                                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "audience": audience,
                                "important": is_important,
                                "pinned": is_pinned,
                                "views": 0
                            }
                            announcements.append(new_announcement)
                            save_data(school['code'], "announcements.json", announcements)
                            school['stats']['announcements'] = school['stats'].get('announcements', 0) + 1
                            save_school(school)
                            st.success("✅ Announcement posted successfully!")
                            st.rerun()
            
            with col2:
                st.subheader("📋 Quick Stats")
                st.metric("Total Announcements", len(announcements))
                st.metric("This Month", len([a for a in announcements if a['date'].startswith(datetime.now().strftime("%Y-%m"))]))
                
                st.divider()
                st.subheader("📌 Pinned Announcements")
                pinned = [a for a in announcements if a.get('pinned')][:3]
                if pinned:
                    for p in pinned:
                        st.markdown(f"• **{p['title']}**")
                else:
                    st.info("No pinned announcements")
            
            st.divider()
            st.subheader("📋 All Announcements")
            
            if announcements:
                for ann in reversed(announcements[-20:]):
                    with st.container(border=True):
                        col_a1, col_a2 = st.columns([3, 1])
                        with col_a1:
                            if ann.get('pinned'):
                                st.markdown(f"📌 **{ann['title']}** ⭐" if ann.get('important') else f"📌 **{ann['title']}**")
                            else:
                                st.markdown(f"**{ann['title']}**" + (" ⭐" if ann.get('important') else ""))
                            st.markdown(ann['content'])
                        with col_a2:
                            st.markdown(f"*Posted: {ann['date']}*")
                            st.markdown(f"*By: {ann['author']}*")
                            st.caption(f"Audience: {', '.join(ann.get('audience', ['All']))}")
                            
                            if st.button("🗑️ Delete", key=f"del_ann_{ann['id']}"):
                                announcements.remove(ann)
                                save_data(school['code'], "announcements.json", announcements)
                                st.rerun()
            else:
                st.info("No announcements yet. Create your first announcement!")
        
        # ---------- MANAGE TEACHERS (FIXED) ----------
        elif menu == "👥 Manage Teachers":
            st.title("👨‍🏫 Teacher Management")
            
            tab1, tab2, tab3 = st.tabs(["➕ Generate Codes", "✅ Active Teachers", "⏳ Pending Codes"])
            
            with tab1:
                st.subheader("Generate Teacher Registration Codes")
                st.markdown("Each teacher gets a **personalized code** with their name")
                
                with st.form("generate_teacher_code"):
                    teacher_name = st.text_input("Teacher Full Name", placeholder="e.g., John Smith")
                    teacher_email = st.text_input("Teacher Email (Optional)", placeholder="teacher@school.edu")
                    teacher_department = st.selectbox(
                        "Department",
                        ["Mathematics", "Science", "English", "History", "Computer Science", "Physical Education", "Arts", "Other"]
                    )
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        num_codes = st.number_input("Number of Codes", min_value=1, max_value=10, value=1)
                    
                    submitted = st.form_submit_button("🔑 Generate Teacher Code(s)", use_container_width=True)
                    
                    if submitted and teacher_name:
                        for i in range(num_codes):
                            teacher_code = generate_teacher_code(teacher_name if i == 0 else f"{teacher_name}{i+1}")
                            teachers.append({
                                "name": teacher_name if num_codes == 1 else f"{teacher_name} #{i+1}",
                                "code": teacher_code,
                                "email": teacher_email,
                                "department": teacher_department,
                                "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "status": "pending",
                                "used_by": None,
                                "used_by_name": None,
                                "activated_date": None
                            })
                        save_data(school['code'], "teachers.json", teachers)
                        st.success(f"✅ Generated {num_codes} teacher code(s)!")
                        st.rerun()
                
                st.divider()
                st.subheader("📋 Recently Generated Codes")
                recent_codes = [t for t in teachers if t['status'] == 'pending'][-5:]
                if recent_codes:
                    for t in recent_codes:
                        with st.container(border=True):
                            col1, col2, col3 = st.columns([2, 2, 1])
                            with col1:
                                st.markdown(f"**{t['name']}**")
                                st.markdown(f"Dept: {t.get('department', 'Not specified')}")
                            with col2:
                                st.code(t['code'])
                                st.caption(f"Created: {t['created']}")
                            with col3:
                                if st.button("❌ Revoke", key=f"revoke_{t['code']}"):
                                    teachers.remove(t)
                                    save_data(school['code'], "teachers.json", teachers)
                                    st.rerun()
                else:
                    st.info("No pending teacher codes")
            
            with tab2:
                st.subheader("✅ Active Teachers")
                active_teachers = [t for t in teachers if t['status'] == 'active']
                active_teacher_users = [u for u in users if u['role'] == 'teacher']
                
                if active_teachers or active_teacher_users:
                    # Show from teacher codes
                    for t in active_teachers:
                        with st.container(border=True):
                            col1, col2, col3 = st.columns([2, 2, 1])
                            with col1:
                                st.markdown(f"**{t.get('used_by_name', t['name'])}**")
                                st.markdown(f"Email: {t.get('used_by', 'N/A')}")
                            with col2:
                                st.markdown(f"Code: `{t['code']}`")
                                st.markdown(f"Activated: {t.get('activated_date', 'N/A')}")
                            with col3:
                                st.markdown(f"**{t.get('department', 'N/A')}**")
                    
                    # Show from users table
                    for u in active_teacher_users:
                        if not any(t.get('used_by') == u['email'] for t in active_teachers):
                            with st.container(border=True):
                                col1, col2 = st.columns([3, 1])
                                with col1:
                                    st.markdown(f"**{u['fullname']}**")
                                    st.markdown(f"Email: {u['email']}")
                                with col2:
                                    st.markdown(f"Joined: {u['joined']}")
                else:
                    st.info("No active teachers yet")
            
            with tab3:
                st.subheader("⏳ Pending Teacher Codes")
                pending_codes = [t for t in teachers if t['status'] == 'pending']
                
                if pending_codes:
                    for t in pending_codes:
                        with st.container(border=True):
                            col1, col2, col3 = st.columns([2, 2, 1])
                            with col1:
                                st.markdown(f"**{t['name']}**")
                                st.markdown(f"Created: {t['created']}")
                            with col2:
                                st.code(t['code'])
                            with col3:
                                if st.button("🗑️ Delete", key=f"del_pending_{t['code']}"):
                                    teachers.remove(t)
                                    save_data(school['code'], "teachers.json", teachers)
                                    st.rerun()
                else:
                    st.info("No pending teacher codes")
        
        # ---------- MANAGE CLASSES ----------
        elif menu == "📚 Manage Classes":
            st.title("📚 Class Management")
            
            tab1, tab2 = st.tabs(["➕ Create Class", "📋 All Classes"])
            
            with tab1:
                st.subheader("Create New Class")
                
                with st.form("create_class_form"):
                    class_name = st.text_input("Class Name", placeholder="e.g., Mathematics 101")
                    class_subject = st.text_input("Subject", placeholder="Mathematics")
                    class_grade = st.selectbox("Grade Level", ["9", "10", "11", "12", "College"])
                    
                    # Get active teachers
                    active_teachers_list = []
                    for t in teachers:
                        if t['status'] == 'active' and t.get('used_by'):
                            teacher_user = next((u for u in users if u['email'] == t['used_by']), None)
                            if teacher_user:
                                display_name = f"{teacher_user['fullname']} ({t['used_by']})"
                                active_teachers_list.append({"display": display_name, "email": t['used_by']})
                    
                    # Also add teachers from users table
                    for u in users:
                        if u['role'] == 'teacher' and u['email'] not in [t['used_by'] for t in teachers if t.get('used_by')]:
                            active_teachers_list.append({"display": f"{u['fullname']} ({u['email']})", "email": u['email']})
                    
                    if active_teachers_list:
                        teacher_options = [t['display'] for t in active_teachers_list]
                        selected_teacher = st.selectbox("Assign Teacher", teacher_options)
                        teacher_email = next(t['email'] for t in active_teachers_list if t['display'] == selected_teacher)
                    else:
                        st.warning("⚠️ No teachers available. Generate teacher codes first.")
                        teacher_email = None
                    
                    class_room = st.text_input("Room Number", placeholder="201")
                    class_schedule = st.text_input("Schedule", placeholder="Mon/Wed 10:00 AM")
                    max_students = st.number_input("Maximum Students", min_value=1, max_value=100, value=30)
                    
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
                                "teacher_name": selected_teacher.split("(")[0].strip(),
                                "room": class_room,
                                "schedule": class_schedule,
                                "max_students": max_students,
                                "students": [],
                                "created": datetime.now().strftime("%Y-%m-%d"),
                                "status": "active"
                            }
                            
                            classes.append(new_class)
                            save_data(school['code'], "classes.json", classes)
                            school['stats']['classes'] = school['stats'].get('classes', 0) + 1
                            save_school(school)
                            
                            st.success(f"✅ Class created! Class Code: **{class_code}**")
                            st.rerun()
            
            with tab2:
                st.subheader("All Classes")
                
                if classes:
                    for c in classes:
                        with st.expander(f"📖 {c['name']} - {c['code']}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"**Subject:** {c.get('subject', 'N/A')}")
                                st.markdown(f"**Teacher:** {c.get('teacher_name', c['teacher'])}")
                                st.markdown(f"**Room:** {c.get('room', 'TBD')}")
                            with col2:
                                st.markdown(f"**Schedule:** {c.get('schedule', 'TBD')}")
                                st.markdown(f"**Students:** {len(c.get('students', []))}/{c.get('max_students', 30)}")
                                st.markdown(f"**Class Code:** `{c['code']}`")
                            
                            if st.button("🗑️ Delete Class", key=f"del_class_{c['id']}"):
                                classes.remove(c)
                                save_data(school['code'], "classes.json", classes)
                                school['stats']['classes'] -= 1
                                save_school(school)
                                st.rerun()
                else:
                    st.info("No classes created yet")
        
        # ---------- MANAGE STUDENTS ----------
        elif menu == "👨‍🎓 Manage Students":
            st.title("👨‍🎓 Student Management")
            
            tab1, tab2, tab3 = st.tabs(["📋 All Students", "📊 Statistics", "➕ Add Student"])
            
            with tab1:
                st.subheader("All Enrolled Students")
                
                student_users = [u for u in users if u['role'] == 'student']
                
                if student_users:
                    for s in student_users:
                        with st.container(border=True):
                            col1, col2, col3 = st.columns([2, 2, 1])
                            with col1:
                                st.markdown(f"**{s['fullname']}**")
                                st.markdown(f"📧 {s['email']}")
                            with col2:
                                st.markdown(f"📅 Joined: {s['joined']}")
                                # Get student's classes
                                student_classes = [c['name'] for c in classes if s['email'] in c.get('students', [])]
                                st.markdown(f"📚 Classes: {len(student_classes)}")
                            with col3:
                                if st.button("👤 View", key=f"view_student_{s['user_id']}"):
                                    st.session_state.view_student = s
                                    st.rerun()
                else:
                    st.info("No students enrolled yet")
            
            with tab2:
                st.subheader("Student Statistics")
                
                total_students = school['stats'].get('students', 0)
                total_classes = school['stats'].get('classes', 0)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Students", total_students)
                with col2:
                    st.metric("Average per Class", round(total_students / total_classes, 1) if total_classes > 0 else 0)
                with col3:
                    st.metric("New This Month", len([u for u in student_users if u['joined'].startswith(datetime.now().strftime("%Y-%m"))]))
                
                # Class distribution
                st.subheader("📊 Class Distribution")
                if classes:
                    class_data = []
                    for c in classes:
                        class_data.append({
                            "Class": c['name'],
                            "Students": len(c.get('students', []))
                        })
                    st.dataframe(class_data, use_container_width=True)
                else:
                    st.info("No classes created yet")
            
            with tab3:
                st.subheader("Manually Add Student")
                st.markdown("Add a student manually (they can also join with school code)")
                
                with st.form("add_student_form"):
                    student_fullname = st.text_input("Full Name")
                    student_email = st.text_input("Email")
                    student_password = st.text_input("Temporary Password", type="password")
                    
                    if st.form_submit_button("➕ Add Student", use_container_width=True):
                        if student_fullname and student_email and student_password:
                            # Check if email exists
                            if any(u['email'] == student_email for u in users):
                                st.error("Email already exists!")
                            else:
                                new_student = {
                                    "user_id": generate_code("USR", 8),
                                    "email": student_email,
                                    "fullname": student_fullname,
                                    "password": hashlib.sha256(student_password.encode()).hexdigest(),
                                    "role": "student",
                                    "profile_pic": None,
                                    "bio": "",
                                    "phone": "",
                                    "joined": datetime.now().strftime("%Y-%m-%d"),
                                    "status": "active",
                                    "school_code": school['code'],
                                    "classes": [],
                                    "groups": []
                                }
                                users.append(new_student)
                                save_data(school['code'], "users.json", users)
                                school['stats']['students'] += 1
                                save_school(school)
                                st.success(f"✅ Student {student_fullname} added successfully!")
                                st.rerun()
        
        # ---------- MANAGE GROUPS (FIXED) ----------
        elif menu == "👥 Manage Groups":
            st.title("👥 Group Management")
            
            tab1, tab2 = st.tabs(["➕ Create Group", "📋 All Groups"])
            
            with tab1:
                st.subheader("Create New Study Group")
                
                with st.form("create_group_form"):
                    group_name = st.text_input("Group Name", placeholder="e.g., Math Study Group")
                    group_description = st.text_area("Description", placeholder="What will this group focus on?")
                    
                    # Select class
                    class_options = [c['name'] for c in classes]
                    if class_options:
                        related_class = st.selectbox("Related Class", ["None"] + class_options)
                    else:
                        related_class = "None"
                        st.info("No classes available. Create classes first.")
                    
                    # Select teacher leader
                    teacher_users = [u for u in users if u['role'] == 'teacher']
                    teacher_options = [f"{t['fullname']} ({t['email']})" for t in teacher_users]
                    
                    if teacher_options:
                        group_leader = st.selectbox("Group Leader (Teacher)", teacher_options)
                        leader_email = teacher_users[teacher_options.index(group_leader)]['email']
                    else:
                        leader_email = user['email']
                        st.info("No teachers available. Admin will be group leader.")
                    
                    max_members = st.number_input("Maximum Members", min_value=2, max_value=50, value=10)
                    
                    submitted = st.form_submit_button("✅ Create Group", use_container_width=True)
                    
                    if submitted and group_name:
                        group_code = generate_code("GRP", 6)
                        
                        new_group = {
                            "id": generate_code("GID", 4),
                            "code": group_code,
                            "name": group_name,
                            "description": group_description,
                            "class": None if related_class == "None" else related_class,
                            "leader": leader_email,
                            "leader_name": group_leader.split("(")[0].strip() if teacher_options else user['fullname'],
                            "created_by": user['email'],
                            "created_by_name": user['fullname'],
                            "created": datetime.now().strftime("%Y-%m-%d"),
                            "max_members": max_members,
                            "members": [user['email']],  # Creator is first member
                            "pending_requests": [],
                            "status": "active"
                        }
                        
                        groups.append(new_group)
                        save_data(school['code'], "groups.json", groups)
                        school['stats']['groups'] = school['stats'].get('groups', 0) + 1
                        save_school(school)
                        
                        st.success(f"✅ Group created! Group Code: **{group_code}**")
                        st.rerun()
            
            with tab2:
                st.subheader("All Groups")
                
                if groups:
                    for g in groups:
                        with st.expander(f"👥 {g['name']} - {g['code']}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"**Description:** {g.get('description', 'No description')}")
                                st.markdown(f"**Leader:** {g.get('leader_name', 'Unknown')}")
                                st.markdown(f"**Class:** {g.get('class', 'General')}")
                            with col2:
                                st.markdown(f"**Members:** {len(g.get('members', []))}/{g.get('max_members', 10)}")
                                st.markdown(f"**Created:** {g['created']}")
                                st.markdown(f"**Group Code:** `{g['code']}`")
                            
                            if st.button("🗑️ Delete Group", key=f"del_group_{g['id']}"):
                                groups.remove(g)
                                save_data(school['code'], "groups.json", groups)
                                school['stats']['groups'] -= 1
                                save_school(school)
                                st.rerun()
                else:
                    st.info("No groups created yet")
        
        # ---------- GENERATE CODES ----------
        elif menu == "🔑 Generate Codes":
            st.title("🔑 Code Generation Center")
            
            tab1, tab2, tab3 = st.tabs(["👨‍🏫 Teacher Codes", "📚 Class Codes", "👥 Group Codes"])
            
            with tab1:
                st.subheader("Generate Teacher Codes")
                
                with st.form("gen_teacher_codes"):
                    teacher_name = st.text_input("Teacher Full Name", key="gen_teacher_name")
                    teacher_dept = st.selectbox("Department", ["Mathematics", "Science", "English", "History", "Computer Science", "Other"])
                    num_codes = st.number_input("Number of Codes", min_value=1, max_value=5, value=1)
                    
                    if st.form_submit_button("🔑 Generate", use_container_width=True):
                        if teacher_name:
                            for i in range(num_codes):
                                code_name = teacher_name if num_codes == 1 else f"{teacher_name} #{i+1}"
                                teacher_code = generate_teacher_code(code_name)
                                teachers.append({
                                    "name": code_name,
                                    "code": teacher_code,
                                    "department": teacher_dept,
                                    "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                    "status": "pending",
                                    "used_by": None,
                                    "used_by_name": None
                                })
                            save_data(school['code'], "teachers.json", teachers)
                            st.success(f"✅ Generated {num_codes} teacher code(s)!")
                            st.rerun()
            
            with tab2:
                st.subheader("Class Codes")
                if classes:
                    for c in classes:
                        with st.container(border=True):
                            col1, col2 = st.columns([2, 1])
                            with col1:
                                st.markdown(f"**{c['name']}**")
                                st.markdown(f"Teacher: {c.get('teacher_name', c['teacher'])}")
                            with col2:
                                st.code(c['code'])
                                st.caption(f"Students: {len(c.get('students', []))}")
                else:
                    st.info("No classes created yet")
            
            with tab3:
                st.subheader("Group Codes")
                if groups:
                    for g in groups:
                        with st.container(border=True):
                            col1, col2 = st.columns([2, 1])
                            with col1:
                                st.markdown(f"**{g['name']}**")
                                st.markdown(f"Leader: {g.get('leader_name', 'Unknown')}")
                            with col2:
                                st.code(g['code'])
                                st.caption(f"Members: {len(g.get('members', []))}")
                else:
                    st.info("No groups created yet")
        
        # ---------- SCHOOL REPORTS (FIXED) ----------
        elif menu == "📊 School Reports":
            st.title("📊 School Reports & Analytics")
            
            tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "👨‍🎓 Student Reports", "👨‍🏫 Teacher Reports", "📚 Class Reports"])
            
            with tab1:
                st.subheader("School Overview Report")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Students", school['stats'].get('students', 0))
                with col2:
                    st.metric("Total Teachers", school['stats'].get('teachers', 0))
                with col3:
                    st.metric("Total Classes", school['stats'].get('classes', 0))
                with col4:
                    st.metric("Total Groups", school['stats'].get('groups', 0))
                
                st.divider()
                
                # Growth chart
                st.subheader("📈 Growth Over Time")
                
                # Get join dates
                student_joins = [u['joined'] for u in users if u['role'] == 'student']
                teacher_joins = [u['joined'] for u in users if u['role'] == 'teacher']
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**👨‍🎓 Student Growth**")
                    st.markdown(f"- This Month: {len([j for j in student_joins if j.startswith(datetime.now().strftime('%Y-%m'))])}")
                    st.markdown(f"- This Year: {len([j for j in student_joins if j.startswith(datetime.now().strftime('%Y'))])}")
                    st.markdown(f"- All Time: {len(student_joins)}")
                
                with col2:
                    st.markdown("**👨‍🏫 Teacher Growth**")
                    st.markdown(f"- This Month: {len([j for j in teacher_joins if j.startswith(datetime.now().strftime('%Y-%m'))])}")
                    st.markdown(f"- This Year: {len([j for j in teacher_joins if j.startswith(datetime.now().strftime('%Y'))])}")
                    st.markdown(f"- All Time: {len(teacher_joins)}")
            
            with tab2:
                st.subheader("Student Reports")
                
                student_users = [u for u in users if u['role'] == 'student']
                
                if student_users:
                    # Student list with stats
                    report_data = []
                    for s in student_users[:20]:  # Show first 20
                        student_classes = [c['name'] for c in classes if s['email'] in c.get('students', [])]
                        student_groups = [g['name'] for g in groups if s['email'] in g.get('members', [])]
                        
                        report_data.append({
                            "Name": s['fullname'],
                            "Email": s['email'],
                            "Joined": s['joined'],
                            "Classes": len(student_classes),
                            "Groups": len(student_groups)
                        })
                    
                    st.dataframe(report_data, use_container_width=True)
                    
                    # Export option
                    if st.button("📥 Export Student Report"):
                        st.success("Report exported! (CSV format would download here)")
                else:
                    st.info("No student data available")
            
            with tab3:
                st.subheader("Teacher Reports")
                
                teacher_users = [u for u in users if u['role'] == 'teacher']
                active_teachers_list = [t for t in teachers if t['status'] == 'active']
                
                if teacher_users or active_teachers_list:
                    # Teacher performance
                    teacher_data = []
                    
                    for t in teacher_users:
                        teacher_classes = [c for c in classes if c.get('teacher') == t['email']]
                        total_students = sum(len(c.get('students', [])) for c in teacher_classes)
                        
                        teacher_data.append({
                            "Name": t['fullname'],
                            "Email": t['email'],
                            "Classes": len(teacher_classes),
                            "Total Students": total_students,
                            "Joined": t['joined']
                        })
                    
                    st.dataframe(teacher_data, use_container_width=True)
                else:
                    st.info("No teacher data available")
            
            with tab4:
                st.subheader("Class Reports")
                
                if classes:
                    class_data = []
                    for c in classes:
                        class_data.append({
                            "Class": c['name'],
                            "Code": c['code'],
                            "Teacher": c.get('teacher_name', c['teacher']),
                            "Students": len(c.get('students', [])),
                            "Room": c.get('room', 'TBD')
                        })
                    
                    st.dataframe(class_data, use_container_width=True)
                    
                    # Class size distribution
                    st.subheader("📊 Class Size Distribution")
                    sizes = [len(c.get('students', [])) for c in classes]
                    if sizes:
                        avg_size = sum(sizes) / len(sizes)
                        st.metric("Average Class Size", round(avg_size, 1))
                        st.metric("Largest Class", max(sizes))
                        st.metric("Smallest Class", min(sizes))
                else:
                    st.info("No class data available")
        
        # ---------- SETTINGS (FIXED) ----------
        elif menu == "⚙️ Settings":
            st.title("⚙️ School Settings")
            
            tab1, tab2, tab3 = st.tabs(["🏫 School Info", "🔐 Security", "📧 Notifications"])
            
            with tab1:
                st.subheader("School Information")
                
                with st.form("school_settings"):
                    school_name = st.text_input("School Name", value=school.get('name', ''))
                    school_motto = st.text_input("School Motto", value=school.get('motto', ''))
                    school_city = st.text_input("City", value=school.get('city', ''))
                    school_state = st.text_input("State", value=school.get('state', ''))
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        principal = st.text_input("Principal Name", value=school.get('principal', user['fullname']))
                    with col2:
                        established = st.text_input("Year Established", value=school.get('established', datetime.now().strftime("%Y")))
                    
                    school_email = st.text_input("School Email", value=school.get('email', 'admin@school.edu'))
                    school_phone = st.text_input("School Phone", value=school.get('phone', '(555) 123-4567'))
                    school_address = st.text_area("Address", value=school.get('address', ''))
                    
                    if st.form_submit_button("💾 Save School Settings", use_container_width=True):
                        school['name'] = school_name
                        school['motto'] = school_motto
                        school['city'] = school_city
                        school['state'] = school_state
                        school['principal'] = principal
                        school['established'] = established
                        school['email'] = school_email
                        school['phone'] = school_phone
                        school['address'] = school_address
                        
                        save_school(school)
                        st.success("✅ School settings saved!")
                        st.rerun()
            
            with tab2:
                st.subheader("Security Settings")
                
                with st.form("security_settings"):
                    st.markdown("**Password Policy**")
                    min_password_length = st.slider("Minimum Password Length", min_value=6, max_value=20, value=8)
                    require_special = st.checkbox("Require special characters", value=True)
                    require_numbers = st.checkbox("Require numbers", value=True)
                    
                    st.markdown("**Session Settings**")
                    session_timeout = st.number_input("Session Timeout (minutes)", min_value=15, max_value=480, value=120)
                    
                    if st.form_submit_button("💾 Save Security Settings", use_container_width=True):
                        school['security'] = {
                            "min_password_length": min_password_length,
                            "require_special": require_special,
                            "require_numbers": require_numbers,
                            "session_timeout": session_timeout
                        }
                        save_school(school)
                        st.success("✅ Security settings saved!")
            
            with tab3:
                st.subheader("Notification Settings")
                
                with st.form("notification_settings"):
                    st.markdown("**Email Notifications**")
                    email_announcements = st.checkbox("New Announcements", value=True)
                    email_assignments = st.checkbox("New Assignments", value=True)
                    email_grades = st.checkbox("Grade Postings", value=True)
                    
                    st.markdown("**System Notifications**")
                    notify_new_users = st.checkbox("New User Registrations", value=True)
                    notify_class_joins = st.checkbox("Student Class Joins", value=True)
                    
                    if st.form_submit_button("💾 Save Notification Settings", use_container_width=True):
                        school['notifications'] = {
                            "email_announcements": email_announcements,
                            "email_assignments": email_assignments,
                            "email_grades": email_grades,
                            "notify_new_users": notify_new_users,
                            "notify_class_joins": notify_class_joins
                        }
                        save_school(school)
                        st.success("✅ Notification settings saved!")
        
        # ---------- MY PROFILE ----------
        elif menu == "👤 My Profile":
            st.title("👤 My Profile")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("Profile Picture")
                if user.get('profile_pic'):
                    st.image(user['profile_pic'], width=200)
                else:
                    st.markdown("# 👑")
                    st.markdown("*No profile picture*")
                
                uploaded_file = st.file_uploader("Upload Photo", type=['png', 'jpg', 'jpeg'], key="admin_upload")
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
                    st.success("✅ Profile picture updated!")
                    st.rerun()
            
            with col2:
                st.subheader("Edit Profile")
                with st.form("edit_admin_profile"):
                    fullname = st.text_input("Full Name", value=user.get('fullname', ''))
                    email = st.text_input("Email", value=user.get('email', ''), disabled=True)
                    phone = st.text_input("Phone Number", value=user.get('phone', ''))
                    title = st.text_input("Title/Position", value=user.get('title', 'School Administrator'))
                    bio = st.text_area("Bio", value=user.get('bio', ''), height=100)
                    
                    if st.form_submit_button("💾 Update Profile", use_container_width=True):
                        for u in users:
                            if u['email'] == user['email']:
                                u['fullname'] = fullname
                                u['phone'] = phone
                                u['title'] = title
                                u['bio'] = bio
                                break
                        
                        save_data(school['code'], "users.json", users)
                        user['fullname'] = fullname
                        user['phone'] = phone
                        user['title'] = title
                        user['bio'] = bio
                        st.success("✅ Profile updated successfully!")
                        st.rerun()
                
                st.divider()
                st.subheader("Account Information")
                st.markdown(f"**User ID:** `{user.get('user_id', 'N/A')}`")
                st.markdown(f"**Joined:** {user.get('joined', 'N/A')}")
                st.markdown(f"**Role:** {user['role'].upper()}")
    
    # ----- TEACHER DASHBOARD -----
    elif user['role'] == 'teacher':
        
        # ---------- TEACHER DASHBOARD ----------
        if menu == "🏠 Dashboard":
            st.title(f"👨‍🏫 Welcome, {user['fullname']}")
            
            my_classes = [c for c in classes if c.get('teacher') == user['email']]
            my_groups = [g for g in groups if g.get('leader') == user['email']]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📚 My Classes", len(my_classes))
            with col2:
                st.metric("👥 My Groups", len(my_groups))
            with col3:
                my_assignments = [a for a in assignments if a.get('teacher') == user['email']]
                st.metric("📝 Active Assignments", len(my_assignments))
            
            st.divider()
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📚 My Classes")
                if my_classes:
                    for c in my_classes[:3]:
                        with st.container(border=True):
                            st.markdown(f"**{c['name']}**")
                            st.markdown(f"Code: `{c['code']}`")
                            st.markdown(f"Students: {len(c.get('students', []))}")
                else:
                    st.info("You haven't been assigned any classes yet")
            
            with col2:
                st.subheader("📝 Recent Activity")
                # Show recent announcements by this teacher
                teacher_announcements = [a for a in announcements if a.get('author_email') == user['email']][:3]
                if teacher_announcements:
                    for a in teacher_announcements:
                        st.markdown(f"- **{a['title']}** ({a['date']})")
                else:
                    st.info("No recent activity")
        
        # ---------- TEACHER ANNOUNCEMENTS ----------
        elif menu == "📢 Announcements":
            st.title("📢 Post Announcement")
            
            with st.form("teacher_announcement_form"):
                ann_title = st.text_input("Title", placeholder="e.g., Homework Reminder")
                ann_content = st.text_area("Content", placeholder="Write your announcement...", height=150)
                
                my_classes = [c['name'] for c in classes if c.get('teacher') == user['email']]
                if my_classes:
                    target_class = st.selectbox("Target Class", ["All Classes"] + my_classes)
                else:
                    target_class = "All Classes"
                    st.info("You don't have any classes yet")
                
                col1, col2 = st.columns(2)
                with col1:
                    is_important = st.checkbox("⭐ Mark as Important")
                with col2:
                    is_pinned = st.checkbox("📌 Pin to Top")
                
                if st.form_submit_button("📢 Post Announcement", use_container_width=True):
                    if ann_title and ann_content:
                        new_announcement = {
                            "id": generate_code("ANN", 6),
                            "title": ann_title,
                            "content": ann_content,
                            "author": user['fullname'],
                            "author_email": user['email'],
                            "author_role": "teacher",
                            "target_class": target_class,
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "important": is_important,
                            "pinned": is_pinned
                        }
                        announcements.append(new_announcement)
                        save_data(school['code'], "announcements.json", announcements)
                        st.success("✅ Announcement posted!")
                        st.rerun()
            
            st.divider()
            st.subheader("📋 My Recent Announcements")
            my_announcements = [a for a in announcements if a.get('author_email') == user['email']][-5:]
            if my_announcements:
                for a in reversed(my_announcements):
                    with st.container(border=True):
                        st.markdown(f"**{a['title']}**")
                        st.markdown(a['content'])
                        st.caption(f"Posted: {a['date']} | Target: {a.get('target_class', 'All')}")
            else:
                st.info("You haven't posted any announcements yet")
        
        # ---------- MY CLASSES ----------
        elif menu == "📚 My Classes":
            st.title("📚 My Classes")
            
            my_classes = [c for c in classes if c.get('teacher') == user['email']]
            
            if my_classes:
                for c in my_classes:
                    with st.expander(f"📖 {c['name']} - {c['code']}", expanded=True):
                        tab1, tab2, tab3, tab4 = st.tabs(["📝 Info", "👥 Students", "📎 Resources", "📊 Grades"])
                        
                        with tab1:
                            st.markdown(f"**Class Code:** `{c['code']}`")
                            st.markdown(f"**Subject:** {c.get('subject', 'N/A')}")
                            st.markdown(f"**Room:** {c.get('room', 'TBD')}")
                            st.markdown(f"**Schedule:** {c.get('schedule', 'TBD')}")
                            st.markdown(f"**Students Enrolled:** {len(c.get('students', []))}/{c.get('max_students', 30)}")
                        
                        with tab2:
                            st.subheader("Enrolled Students")
                            enrolled_students = [u for u in users if u['email'] in c.get('students', [])]
                            
                            if enrolled_students:
                                for s in enrolled_students:
                                    col1, col2 = st.columns([3, 1])
                                    with col1:
                                        st.markdown(f"**{s['fullname']}**")
                                        st.markdown(f"📧 {s['email']}")
                                    with col2:
                                        st.markdown(f"Joined: {s.get('joined', 'N/A')}")
                                    st.divider()
                            else:
                                st.info("No students enrolled yet")
                            
                            st.markdown("---")
                            st.markdown("**Add Student Manually**")
                            add_email = st.text_input("Student Email", key=f"add_{c['code']}")
                            if st.button("Add Student", key=f"add_btn_{c['code']}"):
                                if add_email:
                                    if add_email not in c['students']:
                                        c['students'].append(add_email)
                                        save_data(school['code'], "classes.json", classes)
                                        st.success(f"✅ Added {add_email} to class!")
                                        st.rerun()
                        
                        with tab3:
                            st.subheader("Class Resources")
                            class_resources = [r for r in resources if r.get('class') == c['name']]
                            
                            if class_resources:
                                for r in class_resources:
                                    st.markdown(f"📎 **{r['title']}**")
                                    st.caption(f"Added: {r['date']}")
                            else:
                                st.info("No resources yet")
                            
                            if st.button("➕ Add Resource", key=f"resource_{c['code']}"):
                                st.session_state.menu_index = 4  # Resources tab
                                st.rerun()
                        
                        with tab4:
                            st.subheader("Grade Book")
                            class_students = [u for u in users if u['email'] in c.get('students', [])]
                            
                            if class_students:
                                for s in class_students:
                                    col1, col2 = st.columns([2, 1])
                                    with col1:
                                        st.markdown(f"**{s['fullname']}**")
                                    with col2:
                                        grade = st.selectbox(
                                            "Grade",
                                            ["A", "B", "C", "D", "F", "I"],
                                            key=f"grade_{c['code']}_{s['email']}"
                                        )
                                        if st.button("Save", key=f"save_grade_{c['code']}_{s['email']}"):
                                            new_grade = {
                                                "student": s['email'],
                                                "class": c['name'],
                                                "grade": grade,
                                                "teacher": user['email'],
                                                "date": datetime.now().strftime("%Y-%m-%d")
                                            }
                                            grades.append(new_grade)
                                            save_data(school['code'], "grades.json", grades)
                                            st.success("Grade saved!")
                            else:
                                st.info("No students to grade")
            else:
                st.warning("You haven't been assigned to any classes yet. Contact your admin.")
        
        # ---------- MY GROUPS ----------
        elif menu == "👥 My Groups":
            st.title("👥 My Groups")
            
            my_groups = [g for g in groups if g.get('leader') == user['email']]
            
            tab1, tab2 = st.tabs(["➕ Create Group", "📋 My Groups"])
            
            with tab1:
                st.subheader("Create Study Group")
                
                with st.form("teacher_create_group"):
                    group_name = st.text_input("Group Name")
                    group_description = st.text_area("Description")
                    
                    my_classes = [c['name'] for c in classes if c.get('teacher') == user['email']]
                    related_class = st.selectbox("Related Class", ["None"] + my_classes)
                    
                    max_members = st.number_input("Maximum Members", min_value=2, max_value=50, value=10)
                    
                    if st.form_submit_button("✅ Create Group", use_container_width=True):
                        if group_name:
                            group_code = generate_code("GRP", 6)
                            new_group = {
                                "id": generate_code("GID", 4),
                                "code": group_code,
                                "name": group_name,
                                "description": group_description,
                                "class": None if related_class == "None" else related_class,
                                "leader": user['email'],
                                "leader_name": user['fullname'],
                                "created": datetime.now().strftime("%Y-%m-%d"),
                                "max_members": max_members,
                                "members": [user['email']],
                                "status": "active"
                            }
                            groups.append(new_group)
                            save_data(school['code'], "groups.json", groups)
                            school['stats']['groups'] = school['stats'].get('groups', 0) + 1
                            save_school(school)
                            st.success(f"✅ Group created! Code: {group_code}")
                            st.rerun()
            
            with tab2:
                if my_groups:
                    for g in my_groups:
                        with st.expander(f"👥 {g['name']} - {g['code']}"):
                            st.markdown(f"**Description:** {g.get('description', 'No description')}")
                            st.markdown(f"**Members:** {len(g.get('members', []))}/{g.get('max_members', 10)}")
                            st.markdown(f"**Join Code:** `{g['code']}`")
                            
                            if st.button("🗑️ Delete Group", key=f"del_teacher_group_{g['id']}"):
                                groups.remove(g)
                                save_data(school['code'], "groups.json", groups)
                                st.rerun()
                else:
                    st.info("You haven't created any groups yet")
        
        # ---------- ASSIGNMENTS ----------
        elif menu == "📝 Assignments":
            st.title("📝 Create Assignment")
            
            my_classes = [c['name'] for c in classes if c.get('teacher') == user['email']]
            
            if my_classes:
                with st.form("create_assignment"):
                    class_name = st.selectbox("Select Class", my_classes)
                    title = st.text_input("Assignment Title")
                    description = st.text_area("Description")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        due_date = st.date_input("Due Date")
                    with col2:
                        total_points = st.number_input("Total Points", min_value=1, value=100)
                    
                    assignment_code = generate_code("ASN", 6)
                    
                    if st.form_submit_button("✅ Create Assignment", use_container_width=True):
                        new_assignment = {
                            "code": assignment_code,
                            "class": class_name,
                            "teacher": user['email'],
                            "teacher_name": user['fullname'],
                            "title": title,
                            "description": description,
                            "due": due_date.strftime("%Y-%m-%d"),
                            "points": total_points,
                            "created": datetime.now().strftime("%Y-%m-%d"),
                            "submissions": []
                        }
                        assignments.append(new_assignment)
                        save_data(school['code'], "assignments.json", assignments)
                        st.success(f"✅ Assignment created! Code: {assignment_code}")
                        st.rerun()
                
                st.divider()
                st.subheader("📋 Recent Assignments")
                my_assignments = [a for a in assignments if a.get('teacher') == user['email']][-5:]
                if my_assignments:
                    for a in my_assignments:
                        with st.container(border=True):
                            st.markdown(f"**{a['title']}** - {a['class']}")
                            st.caption(f"Due: {a['due']} | Code: {a['code']}")
                else:
                    st.info("No assignments yet")
            else:
                st.warning("You need to be assigned to a class first")
        
        # ---------- RESOURCES ----------
        elif menu == "📎 Resources":
            st.title("📎 Resource Library")
            
            tab1, tab2 = st.tabs(["➕ Upload Resource", "📋 My Resources"])
            
            with tab1:
                st.subheader("Upload Study Material")
                
                my_classes = [c['name'] for c in classes if c.get('teacher') == user['email']]
                
                with st.form("upload_resource"):
                    if my_classes:
                        target_class = st.selectbox("Class", my_classes)
                    else:
                        target_class = "General"
                        st.info("No classes assigned")
                    
                    title = st.text_input("Resource Title")
                    description = st.text_area("Description")
                    resource_type = st.selectbox("Type", ["Notes", "Worksheet", "Presentation", "Video", "Link", "Other"])
                    
                    resource_code = generate_code("RES", 6)
                    
                    if st.form_submit_button("📤 Upload Resource", use_container_width=True):
                        if title:
                            new_resource = {
                                "code": resource_code,
                                "class": target_class,
                                "title": title,
                                "description": description,
                                "type": resource_type,
                                "teacher": user['fullname'],
                                "date": datetime.now().strftime("%Y-%m-%d"),
                                "downloads": 0
                            }
                            resources.append(new_resource)
                            save_data(school['code'], "resources.json", resources)
                            st.success(f"✅ Resource uploaded! Code: {resource_code}")
                            st.rerun()
            
            with tab2:
                st.subheader("My Resources")
                my_resources = [r for r in resources if r.get('teacher') == user['fullname']]
                if my_resources:
                    for r in my_resources:
                        with st.container(border=True):
                            st.markdown(f"**{r['title']}**")
                            st.markdown(f"Class: {r['class']} | Type: {r['type']}")
                            st.caption(f"Code: {r['code']} | Added: {r['date']}")
                else:
                    st.info("No resources uploaded yet")
        
        # ---------- DISCUSSIONS ----------
        elif menu == "💬 Discussions":
            st.title("💬 Class Discussions")
            
            my_classes = [c['name'] for c in classes if c.get('teacher') == user['email']]
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("Start Discussion")
                with st.form("teacher_discussion"):
                    if my_classes:
                        class_name = st.selectbox("Class", my_classes)
                    else:
                        class_name = "General"
                    
                    topic = st.text_input("Topic")
                    message = st.text_area("Message")
                    
                    if st.form_submit_button("💬 Post Discussion"):
                        new_discussion = {
                            "id": generate_code("DIS", 6),
                            "class": class_name,
                            "topic": topic,
                            "message": message,
                            "author": user['fullname'],
                            "author_role": "teacher",
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "replies": []
                        }
                        discussions.append(new_discussion)
                        save_data(school['code'], "discussions.json", discussions)
                        st.success("Discussion posted!")
                        st.rerun()
            
            with col2:
                st.subheader("Recent Discussions")
                recent_discussions = discussions[-5:]
                if recent_discussions:
                    for d in reversed(recent_discussions):
                        st.markdown(f"**{d['topic']}**")
                        st.caption(f"By {d['author']} in {d['class']}")
                else:
                    st.info("No discussions yet")
        
        # ---------- GRADE BOOK ----------
        elif menu == "📊 Grade Book":
            st.title("📊 Grade Book")
            
            my_classes = [c['name'] for c in classes if c.get('teacher') == user['email']]
            
            if my_classes:
                selected_class = st.selectbox("Select Class", my_classes)
                class_obj = next((c for c in classes if c['name'] == selected_class), None)
                
                if class_obj:
                    st.subheader(f"Grades for {selected_class}")
                    
                    enrolled_students = [u for u in users if u['email'] in class_obj.get('students', [])]
                    class_assignments = [a for a in assignments if a.get('class') == selected_class]
                    
                    if enrolled_students and class_assignments:
                        for s in enrolled_students:
                            with st.expander(f"{s['fullname']}"):
                                for a in class_assignments:
                                    col1, col2, col3 = st.columns([3, 1, 1])
                                    with col1:
                                        st.markdown(f"**{a['title']}**")
                                    with col2:
                                        grade = st.text_input("Grade", key=f"g_{s['email']}_{a['code']}", placeholder="A, B, 85, etc")
                                    with col3:
                                        if st.button("Save", key=f"sg_{s['email']}_{a['code']}"):
                                            grade_entry = {
                                                "student": s['email'],
                                                "assignment": a['code'],
                                                "assignment_title": a['title'],
                                                "class": selected_class,
                                                "grade": grade,
                                                "teacher": user['email'],
                                                "date": datetime.now().strftime("%Y-%m-%d")
                                            }
                                            grades.append(grade_entry)
                                            save_data(school['code'], "grades.json", grades)
                                            st.success("Saved!")
                    else:
                        st.info("No students or assignments in this class")
            else:
                st.warning("No classes assigned")
        
        # ---------- TEACHER PROFILE ----------
        elif menu == "👤 My Profile":
            st.title("👤 My Profile")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("Profile Picture")
                if user.get('profile_pic'):
                    st.image(user['profile_pic'], width=200)
                else:
                    st.markdown("# 👨‍🏫")
                
                uploaded_file = st.file_uploader("Upload Photo", type=['png', 'jpg', 'jpeg'], key="teacher_upload")
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
                    st.success("✅ Profile picture updated!")
                    st.rerun()
            
            with col2:
                st.subheader("Edit Profile")
                with st.form("edit_teacher_profile"):
                    fullname = st.text_input("Full Name", value=user.get('fullname', ''))
                    email = st.text_input("Email", value=user.get('email', ''), disabled=True)
                    phone = st.text_input("Phone Number", value=user.get('phone', ''))
                    bio = st.text_area("Bio", value=user.get('bio', ''), height=100)
                    
                    if st.form_submit_button("💾 Update Profile", use_container_width=True):
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
                        st.success("✅ Profile updated successfully!")
                        st.rerun()
    
    # ----- STUDENT DASHBOARD -----
    else:  # student
        if menu == "🏠 Dashboard":
            st.title(f"👨‍🎓 Welcome, {user['fullname']}")
            
            my_classes = [c for c in classes if user['email'] in c.get('students', [])]
            my_groups = [g for g in groups if user['email'] in g.get('members', [])]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📚 My Classes", len(my_classes))
            with col2:
                st.metric("👥 My Groups", len(my_groups))
            with col3:
                # Get upcoming assignments
                upcoming = [a for a in assignments if a.get('class') in [c['name'] for c in my_classes]]
                st.metric("📝 Due Soon", len(upcoming))
            
            st.divider()
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📚 My Classes")
                if my_classes:
                    for c in my_classes[:3]:
                        with st.container(border=True):
                            st.markdown(f"**{c['name']}**")
                            st.markdown(f"Teacher: {c.get('teacher_name', c['teacher'])}")
                            st.markdown(f"Room: {c.get('room', 'TBD')}")
                else:
                    st.info("You haven't joined any classes yet")
                    
                    st.markdown("### 🔑 Join a Class")
                    join_code = st.text_input("Enter Class Code")
                    if st.button("Join Class"):
                        for c in classes:
                            if c['code'] == join_code:
                                if user['email'] not in c['students']:
                                    c['students'].append(user['email'])
                                    save_data(school['code'], "classes.json", classes)
                                    st.success(f"✅ Joined {c['name']}!")
                                    st.rerun()
            
            with col2:
                st.subheader("📝 Upcoming Homework")
                if upcoming:
                    for a in upcoming[:3]:
                        with st.container(border=True):
                            st.markdown(f"**{a['title']}**")
                            st.markdown(f"Class: {a['class']}")
                            st.markdown(f"Due: {a['due']}")
                else:
                    st.info("No upcoming assignments")
        
        elif menu == "📢 Announcements":
            st.title("📢 School Announcements")
            
            my_classes = [c['name'] for c in classes if user['email'] in c.get('students', [])]
            
            # Filter announcements
            relevant_announcements = []
            for a in announcements:
                target = a.get('target_class', 'All Classes')
                if target == 'All Classes' or target in my_classes:
                    relevant_announcements.append(a)
            
            if relevant_announcements:
                for a in reversed(relevant_announcements[-20:]):
                    with st.container(border=True):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            if a.get('important'):
                                st.markdown(f"⭐ **{a['title']}**")
                            else:
                                st.markdown(f"**{a['title']}**")
                            st.markdown(a['content'])
                        with col2:
                            st.markdown(f"*{a['date']}*")
                            st.markdown(f"By: {a['author']}")
                            st.caption(f"Target: {a.get('target_class', 'All')}")
            else:
                st.info("No announcements yet")
        
        elif menu == "📚 My Classes":
            st.title("📚 My Classes")
            
            my_classes = [c for c in classes if user['email'] in c.get('students', [])]
            
            if my_classes:
                for c in my_classes:
                    with st.expander(f"📖 {c['name']} - {c['code']}", expanded=True):
                        st.markdown(f"**Teacher:** {c.get('teacher_name', c['teacher'])}")
                        st.markdown(f"**Room:** {c.get('room', 'TBD')}")
                        st.markdown(f"**Schedule:** {c.get('schedule', 'TBD')}")
                        
                        # Get class assignments
                        class_assignments = [a for a in assignments if a.get('class') == c['name']]
                        if class_assignments:
                            st.markdown("**📝 Assignments:**")
                            for a in class_assignments:
                                st.markdown(f"- {a['title']} (Due: {a['due']})")
                        
                        # Get class resources
                        class_resources = [r for r in resources if r.get('class') == c['name']]
                        if class_resources:
                            st.markdown("**📎 Resources:**")
                            for r in class_resources:
                                st.markdown(f"- {r['title']}")
            else:
                st.info("You haven't joined any classes yet.")
                
                st.markdown("### 🔑 Join a Class")
                join_code = st.text_input("Enter Class Code", key="student_join_class")
                if st.button("Join Class", key="student_join_btn"):
                    for c in classes:
                        if c['code'] == join_code:
                            if user['email'] not in c['students']:
                                c['students'].append(user['email'])
                                save_data(school['code'], "classes.json", classes)
                                st.success(f"✅ Joined {c['name']}!")
                                st.rerun()
        
        elif menu == "👥 My Groups":
            st.title("👥 My Groups")
            
            my_groups = [g for g in groups if user['email'] in g.get('members', [])]
            
            tab1, tab2 = st.tabs(["📋 My Groups", "🔍 Join Group"])
            
            with tab1:
                if my_groups:
                    for g in my_groups:
                        with st.container(border=True):
                            st.markdown(f"**{g['name']}**")
                            st.markdown(f"Leader: {g.get('leader_name', 'Unknown')}")
                            st.markdown(f"Members: {len(g.get('members', []))}/{g.get('max_members', 10)}")
                            st.caption(f"Code: {g['code']}")
                else:
                    st.info("You haven't joined any groups yet")
            
            with tab2:
                st.subheader("Join a Study Group")
                group_code = st.text_input("Enter Group Code")
                if st.button("Join Group"):
                    for g in groups:
                        if g['code'] == group_code:
                            if user['email'] not in g['members']:
                                if len(g['members']) < g.get('max_members', 10):
                                    g['members'].append(user['email'])
                                    save_data(school['code'], "groups.json", groups)
                                    st.success(f"✅ Joined {g['name']}!")
                                    st.rerun()
                                else:
                                    st.error("Group is full!")
        
        elif menu == "📝 Homework":
            st.title("📝 My Homework")
            
            my_classes = [c['name'] for c in classes if user['email'] in c.get('students', [])]
            my_assignments = [a for a in assignments if a.get('class') in my_classes]
            
            if my_assignments:
                for a in my_assignments:
                    with st.container(border=True):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**{a['title']}**")
                            st.markdown(f"Class: {a['class']}")
                            st.markdown(f"Description: {a.get('description', 'No description')}")
                        with col2:
                            st.markdown(f"📅 Due: {a['due']}")
                            st.markdown(f"📊 Points: {a.get('points', 100)}")
                            st.markdown(f"🔑 Code: `{a['code']}`")
            else:
                st.info("No homework assigned yet")
        
        elif menu == "📎 Study Materials":
            st.title("📎 Study Materials")
            
            my_classes = [c['name'] for c in classes if user['email'] in c.get('students', [])]
            my_resources = [r for r in resources if r.get('class') in my_classes or r.get('class') == 'General']
            
            if my_resources:
                for r in my_resources:
                    with st.container(border=True):
                        st.markdown(f"**{r['title']}**")
                        st.markdown(f"Class: {r['class']} | Type: {r['type']}")
                        st.markdown(r.get('description', ''))
                        st.caption(f"Uploaded by: {r.get('teacher', 'Unknown')} on {r['date']}")
                        st.button("📥 Download", key=f"dl_{r['code']}")
            else:
                st.info("No study materials available")
        
        elif menu == "💬 Discussion Board":
            st.title("💬 Discussion Board")
            
            my_classes = [c['name'] for c in classes if user['email'] in c.get('students', [])]
            class_discussions = [d for d in discussions if d.get('class') in my_classes or d.get('class') == 'General']
            
            if class_discussions:
                for d in reversed(class_discussions[-10:]):
                    with st.expander(f"💭 {d['topic']}"):
                        st.markdown(f"**{d['author']}** ({d['author_role']}) - {d['date']}")
                        st.markdown(d['message'])
                        
                        st.markdown("---")
                        st.markdown("**💬 Replies:**")
                        reply_text = st.text_input("Write a reply...", key=f"reply_{d['id']}")
                        if st.button("Post Reply", key=f"reply_btn_{d['id']}"):
                            st.success("Reply posted!")
            else:
                st.info("No discussions yet")
        
        elif menu == "📅 Events":
            st.title("📅 School Events")
            
            if events:
                for e in events:
                    with st.container(border=True):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**{e['name']}**")
                            st.markdown(f"📍 {e.get('location', 'TBD')}")
                        with col2:
                            st.markdown(f"📅 {e['date']}")
                            st.markdown(f"⏰ {e.get('time', 'TBD')}")
            else:
                st.info("No upcoming events")
        
        elif menu == "📊 My Grades":
            st.title("📊 My Grades")
            
            my_classes = [c['name'] for c in classes if user['email'] in c.get('students', [])]
            my_grades = [g for g in grades if g.get('student') == user['email']]
            
            if my_grades:
                for c in my_classes:
                    class_grades = [g for g in my_grades if g.get('class') == c]
                    if class_grades:
                        with st.expander(f"📖 {c}"):
                            for g in class_grades:
                                st.markdown(f"**{g.get('assignment_title', 'Assignment')}**: {g['grade']}")
            else:
                st.info("No grades available yet")
        
        elif menu == "👤 My Profile":
            st.title("👤 My Profile")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("Profile Picture")
                if user.get('profile_pic'):
                    st.image(user['profile_pic'], width=200)
                else:
                    st.markdown("# 👨‍🎓")
                
                uploaded_file = st.file_uploader("Upload Photo", type=['png', 'jpg', 'jpeg'], key="student_upload")
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
                    st.success("✅ Profile picture updated!")
                    st.rerun()
            
            with col2:
                st.subheader("Edit Profile")
                with st.form("edit_student_profile"):
                    fullname = st.text_input("Full Name", value=user.get('fullname', ''))
                    email = st.text_input("Email", value=user.get('email', ''), disabled=True)
                    phone = st.text_input("Phone Number", value=user.get('phone', ''))
                    bio = st.text_area("Bio", value=user.get('bio', ''), height=100)
                    
                    if st.form_submit_button("💾 Update Profile", use_container_width=True):
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
                        st.success("✅ Profile updated successfully!")
                        st.rerun()

# ----- CASE 4: LOGGED OUT BUT SCHOOL EXISTS -----
elif st.session_state.school and not st.session_state.user:
    school = st.session_state.school
    
    st.title(f"🏫 {school['name']}")
    st.markdown(f"*{school.get('motto', 'Learning Together')}*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔐 Login")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            
            if st.form_submit_button("Login", use_container_width=True):
                users = load_data(school['code'], "users.json", [])
                
                hashed_pw = hashlib.sha256(password.encode()).hexdigest()
                found_user = None
                
                for u in users:
                    if u['email'] == email and u['password'] == hashed_pw:
                        found_user = u
                        break
                
                if found_user:
                    st.session_state.user = found_user
                    st.session_state.page = 'main'
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password")
    
    with col2:
        st.markdown("### 📋 School Information")
        st.markdown(f"""
        **School Code:** `{school['code']}`
        **Principal:** {school.get('principal', school['admin']['fullname'])}
        **Established:** {school.get('established', school['founded'])}
        **Students:** {school['stats'].get('students', 0)}
        **Teachers:** {school['stats'].get('teachers', 0)}
        **Classes:** {school['stats'].get('classes', 0)}
        """)
        
        st.markdown("### 🆕 New User?")
        if st.button("🔑 Join this school", use_container_width=True):
            st.session_state.page = 'join'
            st.rerun()

else:
    # Fallback - should never reach here
    st.error("Something went wrong. Please refresh the page.")
    if st.button("Start Over"):
        st.session_state.school = None
        st.session_state.user = None
        st.session_state.page = 'main'
        st.rerun()
