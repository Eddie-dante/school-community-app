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
    page_title="Multi-School Community System",
    page_icon="🏫",
    layout="wide"
)

# ============ CODE GENERATOR ============
def generate_id(prefix, length=8):
    """Generate unique ID"""
    chars = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choices(chars, k=length))
    return f"{prefix}{random_part}"

def generate_school_code():
    """Generate unique school code"""
    chars = string.ascii_uppercase + string.digits
    return 'SCH' + ''.join(random.choices(chars, k=6))

def generate_class_code():
    """Generate class code"""
    return 'CLS' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def generate_group_code():
    """Generate group code"""
    return 'GRP' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# ============ DATA STORAGE ============
DATA_DIR = Path("school_data")
DATA_DIR.mkdir(exist_ok=True)

# SCHOOLS FILE - Stores all schools
SCHOOLS_FILE = DATA_DIR / "all_schools.json"

def load_all_schools():
    """Load all schools from file"""
    if SCHOOLS_FILE.exists():
        with open(SCHOOLS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_all_schools(schools):
    """Save all schools to file"""
    with open(SCHOOLS_FILE, 'w') as f:
        json.dump(schools, f, indent=2)

def load_school_data(school_code, filename, default):
    """Load data for specific school"""
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

def save_school_data(school_code, filename, data):
    """Save data for specific school"""
    if school_code:
        with open(DATA_DIR / f"{school_code}_{filename}", 'w') as f:
            json.dump(data, f, indent=2)

# ============ SESSION STATE ============
if 'user' not in st.session_state:
    st.session_state.user = None
if 'current_school' not in st.session_state:
    st.session_state.current_school = None
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'menu_index' not in st.session_state:
    st.session_state.menu_index = 0

# ============ MAIN APP ============

# ----- WELCOME PAGE -----
if st.session_state.page == 'welcome':
    st.title("🏫 Multi-School Community System")
    
    tab1, tab2, tab3, tab4 = st.tabs(["👑 Admin Login", "🏫 Create School", "👨‍🏫 Teacher Login", "👨‍🎓 Student Login"])
    
    # ---------- TAB 1: ADMIN LOGIN ----------
    with tab1:
        st.markdown("""
        ### 👑 Administrator Login
        
        Login to manage your existing school.
        """)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            with st.form("admin_login_form"):
                st.markdown("#### 🔐 School Admin Access")
                
                school_code = st.text_input("🏫 School Code", placeholder="e.g., SCHABC123", 
                                          help="Your school's unique code")
                
                admin_email = st.text_input("📧 Admin Email", placeholder="admin@school.edu")
                admin_password = st.text_input("🔐 Password", type="password")
                
                if st.form_submit_button("🔑 LOGIN AS ADMIN", use_container_width=True):
                    if not school_code or not admin_email or not admin_password:
                        st.error("❌ Please fill all fields")
                    else:
                        # Check if school exists
                        all_schools = load_all_schools()
                        
                        if school_code in all_schools:
                            school = all_schools[school_code]
                            
                            # Verify it's the admin
                            if school['admin_email'] == admin_email:
                                # Load users
                                users = load_school_data(school_code, "users.json", [])
                                
                                # Find admin user
                                hashed_pw = hashlib.sha256(admin_password.encode()).hexdigest()
                                admin_user = None
                                
                                for u in users:
                                    if u['email'] == admin_email and u['password'] == hashed_pw and u['role'] == 'admin':
                                        admin_user = u
                                        break
                                
                                if admin_user:
                                    st.session_state.current_school = school
                                    st.session_state.user = admin_user
                                    st.session_state.page = 'school_dashboard'
                                    st.success(f"✅ Welcome back, {admin_user['fullname']}!")
                                    st.rerun()
                                else:
                                    st.error("❌ Invalid admin password")
                            else:
                                st.error("❌ This email is not the school administrator")
                        else:
                            st.error("❌ School not found! Check your school code.")
        
        with col2:
            st.markdown("""
            ### 📋 Admin Access Only
            
            This login is for **SCHOOL ADMINISTRATORS** only.
            
            **You are the admin if:**
            - You created the school
            - You have the admin email
            - You manage teachers and classes
            
            **Don't have a school?**
            Go to the **Create School** tab to start your own school community.
            """)
            
            st.info("""
            **Demo Admin Login:**
            - School Code: Your school code
            - Email: The email you used to create the school
            - Password: The password you set
            """)
    
    # ---------- TAB 2: CREATE SCHOOL ----------
    with tab2:
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            st.markdown("""
            ### 👑 Create New School
            
            Start your own school community.
            You become the **Administrator**.
            """)
            
            with st.form("create_new_school"):
                school_name = st.text_input("🏫 School Name", placeholder="e.g., Nqatho Sec Sch")
                admin_fullname = st.text_input("👤 Your Full Name", placeholder="e.g., Wanjiku Edwin Guchu")
                admin_email = st.text_input("📧 Your Email", placeholder="eddiegucci08@gmail.com")
                admin_password = st.text_input("🔐 Create Password", type="password")
                confirm_password = st.text_input("🔐 Confirm Password", type="password")
                
                col1_1, col1_2 = st.columns(2)
                with col1_1:
                    city = st.text_input("City", placeholder="Nairobi")
                with col1_2:
                    state = st.text_input("State/Province", placeholder="Nairobi")
                
                school_motto = st.text_input("✨ School Motto", placeholder="DTS")
                
                if st.form_submit_button("🚀 CREATE SCHOOL", use_container_width=True):
                    if not school_name or not admin_email or not admin_password:
                        st.error("❌ Please fill all required fields")
                    elif admin_password != confirm_password:
                        st.error("❌ Passwords do not match")
                    else:
                        # Load all schools
                        all_schools = load_all_schools()
                        
                        # Generate unique school code
                        school_code = generate_school_code()
                        while school_code in all_schools:
                            school_code = generate_school_code()
                        
                        # Create school
                        new_school = {
                            "code": school_code,
                            "name": school_name,
                            "city": city,
                            "state": state,
                            "motto": school_motto,
                            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "created_by": admin_email,
                            "admin_name": admin_fullname,
                            "admin_email": admin_email,
                            "stats": {
                                "students": 0,
                                "teachers": 0,
                                "classes": 0,
                                "groups": 0,
                                "pending_requests": 0
                            }
                        }
                        
                        all_schools[school_code] = new_school
                        save_all_schools(all_schools)
                        
                        # Create admin user
                        users = [{
                            "user_id": generate_id("USR"),
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
                        save_school_data(school_code, "users.json", users)
                        
                        # Initialize all school data
                        save_school_data(school_code, "teachers.json", [])
                        save_school_data(school_code, "students.json", [])
                        save_school_data(school_code, "classes.json", [])
                        save_school_data(school_code, "groups.json", [])
                        save_school_data(school_code, "announcements.json", [])
                        save_school_data(school_code, "assignments.json", [])
                        save_school_data(school_code, "resources.json", [])
                        save_school_data(school_code, "events.json", [])
                        save_school_data(school_code, "discussions.json", [])
                        save_school_data(school_code, "grades.json", [])
                        save_school_data(school_code, "class_requests.json", [])
                        save_school_data(school_code, "group_requests.json", [])
                        
                        st.session_state.current_school = new_school
                        st.session_state.user = users[0]
                        st.session_state.page = 'school_dashboard'
                        st.success(f"✅ School created! Your school code is: **{school_code}**")
                        st.rerun()
        
        with col2:
            st.markdown("""
            ### 📋 Your School Credentials
            
            **After creation, you will receive:**
            
            ```
            🔑 SCHOOL CODE: SCH7K9M2B4
            👑 ADMIN EMAIL: your@email.com
            ```
            
            ### 🎯 Save This Code!
            
            You will need your school code to:
            - Login as admin
            - Give to teachers
            - Give to students
            
            **Write it down or copy it now!**
            """)
    
    # ---------- TAB 3: TEACHER LOGIN (PERMANENT CODES) ----------
    with tab3:
        st.markdown("""
        ### 👨‍🏫 Teacher Login
        
        Enter your **School Code** and **Teacher Code** to access your account.
        **Teacher codes are PERMANENT and NEVER EXPIRE.**
        """)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            with st.form("teacher_login_form"):
                st.markdown("#### 🔐 Login with Teacher Code")
                
                school_code = st.text_input("🏫 School Code", placeholder="e.g., SCH7K9M2B4", 
                                          help="Get this from your school administrator")
                
                teacher_code = st.text_input("🔑 Teacher Code", placeholder="e.g., MATH-DEPT, FORM1-2024, MR-JOHNSON", 
                                           help="Your custom teacher code from admin - NEVER EXPIRES")
                
                st.markdown("---")
                st.markdown("#### 👤 Your Information")
                
                fullname = st.text_input("📝 Your Full Name", placeholder="e.g., John Smith")
                email = st.text_input("📧 Your Email", placeholder="teacher@school.edu")
                password = st.text_input("🔐 Create Password", type="password")
                confirm_password = st.text_input("🔐 Confirm Password", type="password")
                
                submitted = st.form_submit_button("✅ REGISTER AS TEACHER", use_container_width=True)
                
                if submitted:
                    if not school_code or not teacher_code or not fullname or not email or not password:
                        st.error("❌ Please fill all fields")
                    elif password != confirm_password:
                        st.error("❌ Passwords do not match")
                    else:
                        # Check if school exists
                        all_schools = load_all_schools()
                        
                        if school_code in all_schools:
                            school = all_schools[school_code]
                            
                            # Load teacher codes for this school
                            teachers_data = load_school_data(school_code, "teachers.json", [])
                            
                            # VERIFY TEACHER CODE - ANY CUSTOM CODE, PERMANENT, NEVER EXPIRES
                            valid_code = False
                            teacher_record = None
                            
                            for t in teachers_data:
                                if t['code'] == teacher_code.upper() and t['status'] == 'active':
                                    valid_code = True
                                    teacher_record = t
                                    
                                    # Initialize used_by_list if not exists
                                    if 'used_by_list' not in t:
                                        t['used_by_list'] = []
                                    
                                    # Add this teacher to the list of users
                                    t['used_by_list'].append({
                                        "email": email,
                                        "name": fullname,
                                        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                                    })
                                    
                                    # Update last used info
                                    t['last_used'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                                    t['last_used_by'] = email
                                    
                                    # Keep status ACTIVE - never change to used/expired
                                    t['status'] = 'active'
                                    break
                            
                            if not valid_code:
                                st.error("❌ Invalid teacher code! Please check with your administrator.")
                                st.info("💡 Teacher codes are created by your administrator. They can be anything like: MATH-DEPT, FORM1-TEACHERS, MR-JOHNSON, etc.")
                                st.stop()
                            
                            # Load users
                            users = load_school_data(school_code, "users.json", [])
                            
                            # Check if email exists
                            if any(u['email'] == email for u in users):
                                st.error("❌ This email is already registered!")
                                st.stop()
                            
                            # Create teacher user
                            new_user = {
                                "user_id": generate_id("USR"),
                                "email": email,
                                "fullname": fullname,
                                "password": hashlib.sha256(password.encode()).hexdigest(),
                                "role": "teacher",
                                "title": f"Teacher - {teacher_record.get('department', 'General')}",
                                "profile_pic": None,
                                "bio": "",
                                "phone": "",
                                "joined": datetime.now().strftime("%Y-%m-%d"),
                                "status": "active",
                                "school_code": school_code,
                                "teacher_code_used": teacher_code.upper(),
                                "classes": [],
                                "groups": []
                            }
                            
                            users.append(new_user)
                            save_school_data(school_code, "users.json", users)
                            save_school_data(school_code, "teachers.json", teachers_data)
                            
                            # Update school stats
                            school['stats']['teachers'] = school['stats'].get('teachers', 0) + 1
                            all_schools[school_code] = school
                            save_all_schools(all_schools)
                            
                            st.session_state.current_school = school
                            st.session_state.user = new_user
                            st.session_state.page = 'school_dashboard'
                            st.success(f"✅ Welcome, {fullname}! You are now registered as a teacher.")
                            st.info("ℹ️ This teacher code is PERMANENT and can be used by other teachers too.")
                            st.rerun()
                        else:
                            st.error("❌ School not found! Check your school code.")
        
        with col2:
            st.markdown("""
            ### 📋 How to Register as Teacher
            
            **1. Get Your Custom Teacher Code**
            - School administrator gives you a **code they created**
            - Examples: `MATH-DEPT`, `FORM1-2024`, `MR-JOHNSON`
            - **Same code works for ALL teachers in your department**
            
            **2. Fill the Form**
            - Enter your school code
            - Enter your teacher code
            - Create your account
            
            **3. Start Teaching**
            - Access your classes
            - Post announcements
            - Create assignments
            - Grade students
            
            ### ⚠️ Important
            Teacher codes are **PERMANENT** and **NEVER EXPIRE**.
            One code can be used by **multiple teachers**.
            Keep your login credentials safe!
            """)
    
    # ---------- TAB 4: STUDENT LOGIN ----------
    with tab4:
        st.markdown("""
        ### 👨‍🎓 Student Login
        
        Enter your **School Code** to join or login.
        """)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            tab_login, tab_register = st.tabs(["🔐 Login", "🆕 New Student"])
            
            with tab_login:
                with st.form("student_login_form"):
                    st.markdown("#### Existing Student Login")
                    
                    school_code = st.text_input("🏫 School Code", placeholder="e.g., SCH7K9M2B4", 
                                              help="Get this from your school administrator", key="student_login_school")
                    
                    email = st.text_input("📧 Email", placeholder="student@example.com", key="student_login_email")
                    password = st.text_input("🔐 Password", type="password", key="student_login_password")
                    
                    if st.form_submit_button("🔐 LOGIN", use_container_width=True):
                        if not school_code or not email or not password:
                            st.error("❌ Please fill all fields")
                        else:
                            # Check if school exists
                            all_schools = load_all_schools()
                            
                            if school_code in all_schools:
                                school = all_schools[school_code]
                                
                                # Load users
                                users = load_school_data(school_code, "users.json", [])
                                
                                # Check credentials
                                hashed_pw = hashlib.sha256(password.encode()).hexdigest()
                                found_user = None
                                
                                for u in users:
                                    if u['email'] == email and u['password'] == hashed_pw and u['role'] == 'student':
                                        found_user = u
                                        break
                                
                                if found_user:
                                    st.session_state.current_school = school
                                    st.session_state.user = found_user
                                    st.session_state.page = 'school_dashboard'
                                    st.success(f"✅ Welcome back, {found_user['fullname']}!")
                                    st.rerun()
                                else:
                                    st.error("❌ Invalid email or password")
                            else:
                                st.error("❌ School not found! Check your school code.")
            
            with tab_register:
                with st.form("student_register_form"):
                    st.markdown("#### New Student Registration")
                    
                    school_code = st.text_input("🏫 School Code", placeholder="e.g., SCH7K9M2B4", 
                                              help="Get this from your school administrator", key="student_register_school")
                    
                    st.markdown("---")
                    st.markdown("#### 👤 Your Information")
                    
                    fullname = st.text_input("📝 Your Full Name", placeholder="e.g., John Smith", key="student_reg_name")
                    email = st.text_input("📧 Your Email", placeholder="student@example.com", key="student_reg_email")
                    password = st.text_input("🔐 Create Password", type="password", key="student_reg_pass")
                    confirm_password = st.text_input("🔐 Confirm Password", type="password", key="student_reg_confirm")
                    
                    if st.form_submit_button("✅ REGISTER AS STUDENT", use_container_width=True):
                        if not school_code or not fullname or not email or not password:
                            st.error("❌ Please fill all fields")
                        elif password != confirm_password:
                            st.error("❌ Passwords do not match")
                        else:
                            # Check if school exists
                            all_schools = load_all_schools()
                            
                            if school_code in all_schools:
                                school = all_schools[school_code]
                                
                                # Load users
                                users = load_school_data(school_code, "users.json", [])
                                
                                # Check if email exists
                                if any(u['email'] == email for u in users):
                                    st.error("❌ This email is already registered!")
                                else:
                                    # Create student user
                                    new_user = {
                                        "user_id": generate_id("USR"),
                                        "email": email,
                                        "fullname": fullname,
                                        "password": hashlib.sha256(password.encode()).hexdigest(),
                                        "role": "student",
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
                                    save_school_data(school_code, "users.json", users)
                                    
                                    # Update school stats
                                    school['stats']['students'] = school['stats'].get('students', 0) + 1
                                    all_schools[school_code] = school
                                    save_all_schools(all_schools)
                                    
                                    st.session_state.current_school = school
                                    st.session_state.user = new_user
                                    st.session_state.page = 'school_dashboard'
                                    st.success(f"✅ Welcome, {fullname}! Your account has been created.")
                                    st.rerun()
                            else:
                                st.error("❌ School not found! Check your school code.")
        
        with col2:
            st.markdown("""
            ### 📋 How to Join as Student
            
            **1. Get Your School Code**
            - Ask your teacher or administrator
            - Format: `SCH7K9M2B4`
            
            **2. Choose Your Path**
            
            **🔐 Existing Student:**
            - Login with your email and password
            
            **🆕 New Student:**
            - Register with your full name
            - Create your account
            - Start joining classes!
            
            ### 🎯 After Registration
            
            - Browse available classes
            - Request to join classes
            - Join study groups
            - View homework and grades
            """)

# ----- SCHOOL DASHBOARD -----
elif st.session_state.page == 'school_dashboard' and st.session_state.current_school and st.session_state.user:
    school = st.session_state.current_school
    user = st.session_state.user
    school_code = school['code']
    
    # Load school data
    users = load_school_data(school_code, "users.json", [])
    teachers_data = load_school_data(school_code, "teachers.json", [])
    classes = load_school_data(school_code, "classes.json", [])
    groups = load_school_data(school_code, "groups.json", [])
    announcements = load_school_data(school_code, "announcements.json", [])
    assignments = load_school_data(school_code, "assignments.json", [])
    resources = load_school_data(school_code, "resources.json", [])
    events = load_school_data(school_code, "events.json", [])
    discussions = load_school_data(school_code, "discussions.json", [])
    grades = load_school_data(school_code, "grades.json", [])
    class_requests = load_school_data(school_code, "class_requests.json", [])
    group_requests = load_school_data(school_code, "group_requests.json", [])
    
    # ============ SIDEBAR ============
    with st.sidebar:
        st.markdown(f"""
        # 🏫 {school['name']}
        *{school.get('motto', 'Learning Together')}*
        
        **School Code:** `{school['code']}`
        ---
        """)
        
        # User Profile
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
        
        st.markdown("---")
        
        # ============ NAVIGATION MENUS ============
        
        # ADMIN MENU
        if user['role'] == 'admin':
            menu_options = [
                "🏠 Dashboard",
                "📢 Announcements",
                "👥 Manage Teachers",
                "📚 Manage Classes",
                "👨‍🎓 Manage Students",
                "👥 Manage Groups",
                "✅ Approval Requests",
                "🔑 Generate Codes",
                "📊 Reports",
                "⚙️ School Settings",
                "👤 My Profile"
            ]
            
            # Count pending requests
            pending_count = len([r for r in class_requests if r['status'] == 'pending']) + \
                          len([r for r in group_requests if r['status'] == 'pending'])
            if pending_count > 0:
                menu_options[6] = f"✅ Approval Requests ({pending_count})"
            
            menu = st.radio("", menu_options, index=st.session_state.menu_index, key="admin_menu")
        
        # TEACHER MENU
        elif user['role'] == 'teacher':
            menu_options = [
                "🏠 Dashboard",
                "📢 My Announcements",
                "📚 My Classes",
                "👥 My Groups",
                "📝 Assignments",
                "✅ Approve Requests",
                "📎 Resources",
                "💬 Discussions",
                "📊 Grade Book",
                "👤 My Profile"
            ]
            
            # Count pending requests for teacher
            my_classes = [c['name'] for c in classes if c.get('teacher') == user['email']]
            my_groups = [g['name'] for g in groups if g.get('leader') == user['email']]
            
            teacher_pending = len([r for r in class_requests if r['status'] == 'pending' and r.get('class_name') in my_classes]) + \
                            len([r for r in group_requests if r['status'] == 'pending' and r.get('group_name') in my_groups])
            
            if teacher_pending > 0:
                menu_options[5] = f"✅ Approve Requests ({teacher_pending})"
            
            menu = st.radio("", menu_options, index=st.session_state.menu_index, key="teacher_menu")
        
        # STUDENT MENU
        else:
            menu_options = [
                "🏠 Dashboard",
                "📢 Announcements",
                "📚 Browse Classes",
                "👥 Browse Groups",
                "📝 My Homework",
                "📎 Study Materials",
                "💬 Discussion Board",
                "📊 My Grades",
                "👤 My Profile"
            ]
            menu = st.radio("", menu_options, index=st.session_state.menu_index, key="student_menu")
        
        st.markdown("---")
        
        # Logout
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.current_school = None
            st.session_state.page = 'welcome'
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
                st.metric("👨‍🎓 Students", school['stats'].get('students', 0))
            with col2:
                st.metric("👨‍🏫 Teachers", school['stats'].get('teachers', 0))
            with col3:
                st.metric("📚 Classes", school['stats'].get('classes', 0))
            with col4:
                st.metric("👥 Groups", school['stats'].get('groups', 0))
            
            st.divider()
            
            # Pending Requests
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("✅ Pending Requests")
                pending_class = [r for r in class_requests if r['status'] == 'pending']
                pending_group = [r for r in group_requests if r['status'] == 'pending']
                
                if pending_class or pending_group:
                    st.warning(f"**{len(pending_class)}** class join requests | **{len(pending_group)}** group join requests")
                    if st.button("Go to Approval Requests"):
                        st.session_state.menu_index = 6
                        st.rerun()
                else:
                    st.success("No pending requests")
            
            with col2:
                st.subheader("📊 Quick Stats")
                total_users = len([u for u in users if u['status'] == 'active'])
                st.metric("Active Users", total_users)
            
            st.divider()
            
            # Recent Activity
            st.subheader("📋 Recent Activity")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**📢 Latest Announcements**")
                recent_ann = announcements[-3:] if announcements else []
                if recent_ann:
                    for a in reversed(recent_ann):
                        st.markdown(f"- **{a['title']}** - {a['date'][:10]}")
                else:
                    st.info("No announcements yet")
            
            with col2:
                st.markdown("**👥 Recently Joined**")
                recent_users = [u for u in users if u['joined'] == datetime.now().strftime("%Y-%m-%d")][-3:]
                if recent_users:
                    for u in recent_users:
                        st.markdown(f"- **{u['fullname']}** ({u['role']})")
                else:
                    st.info("No new users today")
        
        # ---------- ANNOUNCEMENTS ----------
        elif menu == "📢 Announcements":
            st.title("📢 School Announcements")
            
            col1, col2 = st.columns([1.5, 1])
            
            with col1:
                st.subheader("📝 Create Announcement")
                with st.form("admin_announcement"):
                    title = st.text_input("Title")
                    content = st.text_area("Content", height=150)
                    
                    col_a1, col_a2 = st.columns(2)
                    with col_a1:
                        audience = st.multiselect(
                            "Target",
                            ["All", "Students", "Teachers"],
                            default=["All"]
                        )
                    with col_a2:
                        important = st.checkbox("⭐ Important")
                        pinned = st.checkbox("📌 Pin")
                    
                    if st.form_submit_button("📢 Post Announcement", use_container_width=True):
                        if title and content:
                            new_ann = {
                                "id": generate_id("ANN"),
                                "title": title,
                                "content": content,
                                "author": user['fullname'],
                                "author_email": user['email'],
                                "author_role": "admin",
                                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "audience": audience,
                                "important": important,
                                "pinned": pinned
                            }
                            announcements.append(new_ann)
                            save_school_data(school_code, "announcements.json", announcements)
                            st.success("✅ Announcement posted!")
                            st.rerun()
            
            with col2:
                st.subheader("📋 Stats")
                st.metric("Total Announcements", len(announcements))
                st.metric("This Month", len([a for a in announcements if a['date'].startswith(datetime.now().strftime("%Y-%m"))]))
            
            st.divider()
            st.subheader("📋 All Announcements")
            
            if announcements:
                for a in reversed(announcements[-20:]):
                    with st.container(border=True):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            if a.get('pinned'):
                                st.markdown(f"📌 **{a['title']}**" + (" ⭐" if a.get('important') else ""))
                            else:
                                st.markdown(f"**{a['title']}**" + (" ⭐" if a.get('important') else ""))
                            st.markdown(a['content'])
                        with col2:
                            st.caption(f"By: {a['author']}")
                            st.caption(f"Date: {a['date'][:16]}")
                            st.caption(f"Target: {', '.join(a.get('audience', ['All']))}")
                            
                            if st.button("🗑️", key=f"del_ann_{a['id']}"):
                                announcements.remove(a)
                                save_school_data(school_code, "announcements.json", announcements)
                                st.rerun()
            else:
                st.info("No announcements yet")
        
        # ---------- MANAGE TEACHERS (CUSTOM CODES) ----------
        elif menu == "👥 Manage Teachers":
            st.title("👨‍🏫 Teacher Management - CUSTOM CODES")
            st.success("✅ You can create ANY teacher code you want! Codes are PERMANENT and NEVER expire.")
            
            tab1, tab2, tab3 = st.tabs(["🔑 Create Custom Codes", "✅ Active Teachers", "📋 Code Usage History"])
            
            with tab1:
                st.subheader("🔑 Create Your Own Teacher Codes")
                st.info("ℹ️ Create ANY code you want. These codes NEVER expire and can be used by MULTIPLE teachers.")
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    with st.form("create_custom_teacher_code"):
                        st.markdown("#### ✏️ Create Custom Code")
                        
                        code_name = st.text_input("📝 Code Name/Description", placeholder="e.g., Mathematics Department, Form 1 Teachers, John Smith")
                        custom_code = st.text_input("🔑 Custom Teacher Code", placeholder="e.g., MATH-DEPT, FORM1-2024, MR-JOHNSON",
                                                  help="Create any code you want! Use letters, numbers, and hyphens.")
                        
                        teacher_department = st.selectbox(
                            "🏢 Department",
                            ["Mathematics", "Science", "English", "History", "Computer Science", 
                             "Physical Education", "Arts", "Administration", "Form 1", "Form 2", 
                             "Form 3", "Form 4", "Board of Governors", "PTA", "Other"]
                        )
                        
                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            submitted = st.form_submit_button("✅ CREATE CUSTOM CODE", use_container_width=True)
                        
                        if submitted:
                            if not code_name:
                                st.error("❌ Please enter a code name/description")
                            elif not custom_code:
                                st.error("❌ Please enter your custom code")
                            else:
                                # Check if code already exists
                                code_exists = False
                                for t in teachers_data:
                                    if t['code'] == custom_code.upper():
                                        code_exists = True
                                        break
                                
                                if code_exists:
                                    st.error(f"❌ Code '{custom_code.upper()}' already exists! Please choose another one.")
                                else:
                                    teachers_data.append({
                                        "id": generate_id("TCH"),
                                        "name": code_name,
                                        "code": custom_code.upper(),
                                        "department": teacher_department,
                                        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                        "created_by": user['email'],
                                        "status": "active",
                                        "used_by": None,
                                        "used_by_name": None,
                                        "used_by_list": [],
                                        "is_permanent": True,
                                        "can_be_reused": True,
                                        "is_custom": True
                                    })
                                    
                                    save_school_data(school_code, "teachers.json", teachers_data)
                                    st.success(f"✅ Custom teacher code created: **{custom_code.upper()}**")
                                    st.info(f"ℹ️ This code is for: {code_name} | Department: {teacher_department}")
                                    st.balloons()
                                    st.rerun()
                
                with col2:
                    st.markdown("""
                    ### 📋 Code Creation Examples
                    
                    **You can create ANY code like:**
                    
                    ```
                    📌 By Department:
                    • MATH-DEPT
                    • SCIENCE-2024
                    • ENGLISH-TEAM
                    • KISWAHILI
                    
                    📌 By Teacher Name:
                    • MR-OTIENO
                    • MS-AKINYI
                    • DR-ODHIAMBO
                    • MADAM-JANE
                    
                    📌 By Form/Class:
                    • FORM1-2024
                    • FORM2-TEACHERS
                    • FORM4-CLASS
                    • GRADUATE-2025
                    
                    📌 By Role:
                    • HOD-MATHEMATICS
                    • SENIOR-TEACHER
                    • BOARD-MEMBER
                    • PTA-CHAIR
                    ```
                    
                    ### ✅ Benefits:
                    - **Easy to remember** - Use department names
                    - **Share with everyone** - One code for all math teachers
                    - **Never expires** - Works forever
                    - **Track usage** - See who used which code
                    """)
                
                st.divider()
                
                # Show existing custom codes
                st.subheader("📋 Your Custom Teacher Codes")
                custom_codes = [t for t in teachers_data if t.get('is_custom', False) or t['status'] == 'active']
                
                if custom_codes:
                    for t in custom_codes:
                        with st.container(border=True):
                            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                            with col1:
                                st.markdown(f"**{t['name']}**")
                                st.markdown(f"Dept: {t.get('department', 'N/A')}")
                                if t.get('is_custom'):
                                    st.markdown("**✨ CUSTOM CODE**")
                            with col2:
                                st.code(t['code'], language=None)
                                st.caption(f"Created: {t['created'][:16]}")
                            with col3:
                                used_count = len(t.get('used_by_list', []))
                                st.markdown(f"**Used by:** {used_count} teacher(s)")
                                if t.get('used_by_list'):
                                    last_used = t['used_by_list'][-1]['date'][:16]
                                    st.caption(f"Last used: {last_used}")
                                else:
                                    st.caption("Not used yet")
                            with col4:
                                if st.button("🗑️", key=f"del_custom_{t['id']}"):
                                    teachers_data.remove(t)
                                    save_school_data(school_code, "teachers.json", teachers_data)
                                    st.rerun()
                else:
                    st.info("No custom teacher codes created yet. Create your first one above!")
            
            with tab2:
                st.subheader("✅ Active Teachers")
                
                active_teachers = [t for t in teachers_data if t['status'] == 'active']
                teacher_users = [u for u in users if u['role'] == 'teacher']
                
                if active_teachers or teacher_users:
                    # Show teacher codes
                    for t in active_teachers:
                        with st.container(border=True):
                            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                            with col1:
                                st.markdown(f"**{t['name']}**")
                                st.markdown(f"Dept: {t.get('department', 'N/A')}")
                            with col2:
                                st.markdown(f"**PERMANENT CODE** ✅")
                                st.markdown(f"Never expires")
                            with col3:
                                st.code(t['code'])
                                if t.get('used_by_list'):
                                    st.caption(f"Used by: {len(t['used_by_list'])} teacher(s)")
                                    if t.get('last_used_by'):
                                        st.caption(f"Last: {t['last_used_by']}")
                                else:
                                    st.caption("Not used yet")
                            with col4:
                                if st.button("🗑️", key=f"del_teacher_code_{t['id']}"):
                                    teachers_data.remove(t)
                                    save_school_data(school_code, "teachers.json", teachers_data)
                                    st.rerun()
                    
                    # Show teacher users
                    for u in teacher_users:
                        if not any(t.get('last_used_by') == u['email'] for t in active_teachers):
                            with st.container(border=True):
                                col1, col2, col3 = st.columns([2, 2, 1])
                                with col1:
                                    st.markdown(f"**{u['fullname']}**")
                                    st.markdown(f"📧 {u['email']}")
                                with col2:
                                    st.markdown(f"**Joined:** {u['joined']}")
                                    if u.get('teacher_code_used'):
                                        st.caption(f"Code: {u['teacher_code_used']}")
                                with col3:
                                    if st.button("🗑️", key=f"del_teacher_user_{u['user_id']}"):
                                        users.remove(u)
                                        save_school_data(school_code, "users.json", users)
                                        school['stats']['teachers'] -= 1
                                        all_schools = load_all_schools()
                                        all_schools[school_code] = school
                                        save_all_schools(all_schools)
                                        st.rerun()
                else:
                    st.info("No active teachers yet")
            
            with tab3:
                st.subheader("📋 Teacher Code Usage History")
                
                codes_with_usage = [t for t in teachers_data if t.get('used_by_list')]
                
                if codes_with_usage:
                    for t in codes_with_usage:
                        with st.expander(f"📊 {t['code']} - {t['name']}"):
                            st.markdown(f"**Department:** {t.get('department', 'N/A')}")
                            st.markdown(f"**Created:** {t['created']}")
                            st.markdown(f"**Total Teachers Used:** {len(t.get('used_by_list', []))}")
                            st.markdown("**Teachers who used this code:**")
                            for teacher in t.get('used_by_list', []):
                                st.markdown(f"- **{teacher['name']}** ({teacher['email']}) - {teacher['date']}")
                else:
                    st.info("No teacher codes have been used yet")
        
        # ---------- MANAGE CLASSES ----------
        elif menu == "📚 Manage Classes":
            st.title("📚 Class Management")
            
            tab1, tab2 = st.tabs(["➕ Create Class", "📋 All Classes"])
            
            with tab1:
                st.subheader("Create New Class")
                
                with st.form("create_class"):
                    class_name = st.text_input("Class Name", placeholder="e.g., Mathematics 101")
                    class_subject = st.text_input("Subject", placeholder="Mathematics")
                    class_grade = st.selectbox("Grade Level", ["9", "10", "11", "12", "College"])
                    
                    # Get active teachers
                    active_teachers_list = []
                    for t in teachers_data:
                        if t['status'] == 'active' and t.get('used_by_list'):
                            for teacher_use in t.get('used_by_list', []):
                                teacher_email = teacher_use['email']
                                teacher_user = next((u for u in users if u['email'] == teacher_email), None)
                                if teacher_user:
                                    display_name = f"{teacher_user['fullname']} ({teacher_email})"
                                    active_teachers_list.append({"display": display_name, "email": teacher_email})
                    
                    for u in users:
                        if u['role'] == 'teacher' and not any(t.get('last_used_by') == u['email'] for t in teachers_data):
                            active_teachers_list.append({"display": f"{u['fullname']} ({u['email']})", "email": u['email']})
                    
                    if active_teachers_list:
                        teacher_options = [t['display'] for t in active_teachers_list]
                        selected_teacher = st.selectbox("Assign Teacher", teacher_options)
                        teacher_email = next(t['email'] for t in active_teachers_list if t['display'] == selected_teacher)
                        teacher_name = selected_teacher.split("(")[0].strip()
                    else:
                        st.warning("⚠️ No teachers available. Create teacher codes first.")
                        teacher_email = None
                        teacher_name = None
                    
                    class_room = st.text_input("Room Number", placeholder="201")
                    class_schedule = st.text_input("Schedule", placeholder="Mon/Wed 10:00 AM")
                    max_students = st.number_input("Maximum Students", min_value=1, max_value=100, value=30)
                    
                    if st.form_submit_button("✅ Create Class", use_container_width=True):
                        if class_name and teacher_email:
                            class_code = generate_class_code()
                            
                            new_class = {
                                "id": generate_id("CLS"),
                                "code": class_code,
                                "name": class_name,
                                "subject": class_subject,
                                "grade": class_grade,
                                "teacher": teacher_email,
                                "teacher_name": teacher_name,
                                "room": class_room,
                                "schedule": class_schedule,
                                "max_students": max_students,
                                "students": [],
                                "created": datetime.now().strftime("%Y-%m-%d"),
                                "created_by": user['email'],
                                "status": "active"
                            }
                            
                            classes.append(new_class)
                            save_school_data(school_code, "classes.json", classes)
                            school['stats']['classes'] = school['stats'].get('classes', 0) + 1
                            
                            all_schools = load_all_schools()
                            all_schools[school_code] = school
                            save_all_schools(all_schools)
                            
                            st.success(f"✅ Class created! Code: **{class_code}**")
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
                                st.markdown(f"**Code:** `{c['code']}`")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("🗑️ Delete Class", key=f"del_class_{c['id']}"):
                                    classes.remove(c)
                                    save_school_data(school_code, "classes.json", classes)
                                    school['stats']['classes'] -= 1
                                    all_schools = load_all_schools()
                                    all_schools[school_code] = school
                                    save_all_schools(all_schools)
                                    st.rerun()
                            with col2:
                                st.markdown(f"**Join Code:** `{c['code']}`")
                else:
                    st.info("No classes created yet")
        
        # ---------- MANAGE STUDENTS ----------
        elif menu == "👨‍🎓 Manage Students":
            st.title("👨‍🎓 Student Management")
            
            tab1, tab2 = st.tabs(["📋 All Students", "➕ Add Student"])
            
            with tab1:
                st.subheader("All Enrolled Students")
                
                student_users = [u for u in users if u['role'] == 'student']
                
                if student_users:
                    for s in student_users:
                        with st.container(border=True):
                            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                            with col1:
                                if s.get('profile_pic'):
                                    st.image(s['profile_pic'], width=40)
                                st.markdown(f"**{s['fullname']}**")
                            with col2:
                                st.markdown(f"📧 {s['email']}")
                                st.markdown(f"📅 Joined: {s['joined']}")
                            with col3:
                                # Get student's classes
                                student_classes = [c['name'] for c in classes if s['email'] in c.get('students', [])]
                                st.markdown(f"📚 Classes: {len(student_classes)}")
                                if student_classes:
                                    st.caption(", ".join(student_classes[:2]))
                            with col4:
                                if st.button("🗑️", key=f"del_student_{s['user_id']}"):
                                    # Remove from users
                                    users.remove(s)
                                    save_school_data(school_code, "users.json", users)
                                    
                                    # Remove from classes
                                    for c in classes:
                                        if s['email'] in c.get('students', []):
                                            c['students'].remove(s['email'])
                                    save_school_data(school_code, "classes.json", classes)
                                    
                                    # Update stats
                                    school['stats']['students'] -= 1
                                    all_schools = load_all_schools()
                                    all_schools[school_code] = school
                                    save_all_schools(all_schools)
                                    
                                    st.success(f"✅ Student {s['fullname']} removed")
                                    st.rerun()
                else:
                    st.info("No students enrolled yet")
            
            with tab2:
                st.subheader("Manually Add Student")
                
                with st.form("add_student"):
                    student_fullname = st.text_input("Full Name")
                    student_email = st.text_input("Email")
                    student_password = st.text_input("Temporary Password", type="password")
                    
                    if st.form_submit_button("➕ Add Student", use_container_width=True):
                        if student_fullname and student_email and student_password:
                            # Check if email exists
                            if any(u['email'] == student_email for u in users):
                                st.error("❌ Email already exists!")
                            else:
                                new_student = {
                                    "user_id": generate_id("USR"),
                                    "email": student_email,
                                    "fullname": student_fullname,
                                    "password": hashlib.sha256(student_password.encode()).hexdigest(),
                                    "role": "student",
                                    "profile_pic": None,
                                    "bio": "",
                                    "phone": "",
                                    "joined": datetime.now().strftime("%Y-%m-%d"),
                                    "status": "active",
                                    "school_code": school_code,
                                    "classes": [],
                                    "groups": []
                                }
                                users.append(new_student)
                                save_school_data(school_code, "users.json", users)
                                
                                school['stats']['students'] = school['stats'].get('students', 0) + 1
                                all_schools = load_all_schools()
                                all_schools[school_code] = school
                                save_all_schools(all_schools)
                                
                                st.success(f"✅ Student {student_fullname} added successfully!")
                                st.rerun()
        
        # ---------- MANAGE GROUPS ----------
        elif menu == "👥 Manage Groups":
            st.title("👥 Group Management")
            
            tab1, tab2 = st.tabs(["➕ Create Group", "📋 All Groups"])
            
            with tab1:
                st.subheader("Create New Group")
                
                with st.form("create_group"):
                    group_name = st.text_input("Group Name", placeholder="e.g., Math Study Group")
                    group_description = st.text_area("Description", placeholder="What will this group focus on?")
                    
                    # Select class
                    class_options = [c['name'] for c in classes]
                    related_class = st.selectbox("Related Class", ["None"] + class_options) if class_options else "None"
                    
                    # Select teacher leader
                    teacher_users = [u for u in users if u['role'] == 'teacher']
                    teacher_options = [f"{t['fullname']} ({t['email']})" for t in teacher_users]
                    
                    if teacher_options:
                        group_leader = st.selectbox("Group Leader", teacher_options)
                        leader_email = teacher_users[teacher_options.index(group_leader)]['email']
                        leader_name = group_leader.split("(")[0].strip()
                    else:
                        leader_email = user['email']
                        leader_name = user['fullname']
                        st.info("No teachers available. Admin will be group leader.")
                    
                    max_members = st.number_input("Maximum Members", min_value=2, max_value=50, value=10)
                    
                    if st.form_submit_button("✅ Create Group", use_container_width=True):
                        if group_name:
                            group_code = generate_group_code()
                            
                            new_group = {
                                "id": generate_id("GRP"),
                                "code": group_code,
                                "name": group_name,
                                "description": group_description,
                                "class": None if related_class == "None" else related_class,
                                "leader": leader_email,
                                "leader_name": leader_name,
                                "created_by": user['email'],
                                "created_by_name": user['fullname'],
                                "created": datetime.now().strftime("%Y-%m-%d"),
                                "max_members": max_members,
                                "members": [leader_email],
                                "pending_requests": [],
                                "status": "active"
                            }
                            
                            groups.append(new_group)
                            save_school_data(school_code, "groups.json", groups)
                            school['stats']['groups'] = school['stats'].get('groups', 0) + 1
                            
                            all_schools = load_all_schools()
                            all_schools[school_code] = school
                            save_all_schools(all_schools)
                            
                            st.success(f"✅ Group created! Code: **{group_code}**")
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
                                st.markdown(f"**Code:** `{g['code']}`")
                            
                            if st.button("🗑️ Delete Group", key=f"del_group_{g['id']}"):
                                groups.remove(g)
                                save_school_data(school_code, "groups.json", groups)
                                school['stats']['groups'] -= 1
                                all_schools = load_all_schools()
                                all_schools[school_code] = school
                                save_all_schools(all_schools)
                                st.rerun()
                else:
                    st.info("No groups created yet")
        
        # ---------- APPROVAL REQUESTS ----------
        elif menu.startswith("✅ Approval Requests"):
            st.title("✅ Approval Requests")
            
            tab1, tab2 = st.tabs(["📚 Class Join Requests", "👥 Group Join Requests"])
            
            with tab1:
                st.subheader("Class Join Requests")
                
                pending_class = [r for r in class_requests if r['status'] == 'pending']
                
                if pending_class:
                    for req in pending_class:
                        with st.container(border=True):
                            col1, col2, col3 = st.columns([2, 2, 2])
                            with col1:
                                st.markdown(f"**Student:** {req['student_name']}")
                                st.markdown(f"📧 {req['student_email']}")
                            with col2:
                                st.markdown(f"**Class:** {req['class_name']}")
                                st.markdown(f"📅 Requested: {req['date']}")
                            with col3:
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    if st.button("✅ Approve", key=f"app_class_{req['id']}"):
                                        # Add student to class
                                        for c in classes:
                                            if c['name'] == req['class_name']:
                                                if req['student_email'] not in c['students']:
                                                    c['students'].append(req['student_email'])
                                        save_school_data(school_code, "classes.json", classes)
                                        
                                        # Update request status
                                        req['status'] = 'approved'
                                        req['approved_by'] = user['email']
                                        req['approved_date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                                        save_school_data(school_code, "class_requests.json", class_requests)
                                        
                                        st.success("✅ Approved!")
                                        st.rerun()
                                with col_b:
                                    if st.button("❌ Deny", key=f"deny_class_{req['id']}"):
                                        req['status'] = 'denied'
                                        req['denied_by'] = user['email']
                                        req['denied_date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                                        save_school_data(school_code, "class_requests.json", class_requests)
                                        st.rerun()
                else:
                    st.info("No pending class join requests")
            
            with tab2:
                st.subheader("Group Join Requests")
                
                pending_group = [r for r in group_requests if r['status'] == 'pending']
                
                if pending_group:
                    for req in pending_group:
                        with st.container(border=True):
                            col1, col2, col3 = st.columns([2, 2, 2])
                            with col1:
                                st.markdown(f"**Student:** {req['student_name']}")
                                st.markdown(f"📧 {req['student_email']}")
                            with col2:
                                st.markdown(f"**Group:** {req['group_name']}")
                                st.markdown(f"📅 Requested: {req['date']}")
                            with col3:
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    if st.button("✅ Approve", key=f"app_group_{req['id']}"):
                                        # Add student to group
                                        for g in groups:
                                            if g['name'] == req['group_name']:
                                                if req['student_email'] not in g['members']:
                                                    g['members'].append(req['student_email'])
                                        save_school_data(school_code, "groups.json", groups)
                                        
                                        # Update request status
                                        req['status'] = 'approved'
                                        req['approved_by'] = user['email']
                                        req['approved_date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                                        save_school_data(school_code, "group_requests.json", group_requests)
                                        
                                        st.success("✅ Approved!")
                                        st.rerun()
                                with col_b:
                                    if st.button("❌ Deny", key=f"deny_group_{req['id']}"):
                                        req['status'] = 'denied'
                                        req['denied_by'] = user['email']
                                        req['denied_date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                                        save_school_data(school_code, "group_requests.json", group_requests)
                                        st.rerun()
                else:
                    st.info("No pending group join requests")
        
        # ---------- GENERATE CODES ----------
        elif menu == "🔑 Generate Codes":
            st.title("🔑 Code Generation Center")
            
            tab1, tab2, tab3 = st.tabs(["👨‍🏫 Custom Teacher Codes", "📚 Class Codes", "👥 Group Codes"])
            
            with tab1:
                st.subheader("🔑 Create Custom Teacher Codes")
                st.success("✅ Create ANY code you want! These codes NEVER expire.")
                
                with st.form("gen_custom_teacher_codes"):
                    code_name = st.text_input("📝 Code Name/Description", placeholder="e.g., Mathematics Department")
                    custom_code = st.text_input("🔑 Custom Teacher Code", placeholder="e.g., MATH-DEPT, FORM1-2024")
                    teacher_dept = st.selectbox("Department", ["Mathematics", "Science", "English", "History", "Computer Science", "Administration", "Other"])
                    
                    if st.form_submit_button("✅ CREATE CUSTOM CODE", use_container_width=True):
                        if code_name and custom_code:
                            # Check if code already exists
                            code_exists = False
                            for t in teachers_data:
                                if t['code'] == custom_code.upper():
                                    code_exists = True
                                    break
                            
                            if code_exists:
                                st.error(f"❌ Code '{custom_code.upper()}' already exists!")
                            else:
                                teachers_data.append({
                                    "id": generate_id("TCH"),
                                    "name": code_name,
                                    "code": custom_code.upper(),
                                    "department": teacher_dept,
                                    "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                    "status": "active",
                                    "used_by_list": [],
                                    "is_permanent": True,
                                    "is_custom": True
                                })
                                save_school_data(school_code, "teachers.json", teachers_data)
                                st.success(f"✅ Custom code created: **{custom_code.upper()}**")
                                st.rerun()
            
            with tab2:
                st.subheader("Active Class Codes")
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
                st.subheader("Active Group Codes")
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
        
        # ---------- REPORTS ----------
        elif menu == "📊 Reports":
            st.title("📊 School Reports")
            
            tab1, tab2, tab3 = st.tabs(["📈 Overview", "👨‍🎓 Student Report", "👨‍🏫 Teacher Report"])
            
            with tab1:
                st.subheader("School Overview")
                
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
                
                # Class size distribution
                st.subheader("📊 Class Size Distribution")
                if classes:
                    class_sizes = [len(c.get('students', [])) for c in classes]
                    avg_size = sum(class_sizes) / len(class_sizes) if class_sizes else 0
                    st.metric("Average Class Size", round(avg_size, 1))
                    st.metric("Largest Class", max(class_sizes) if class_sizes else 0)
                    st.metric("Smallest Class", min(class_sizes) if class_sizes else 0)
                else:
                    st.info("No class data available")
            
            with tab2:
                st.subheader("Student Report")
                
                student_users = [u for u in users if u['role'] == 'student']
                
                if student_users:
                    report_data = []
                    for s in student_users:
                        student_classes = len([c for c in classes if s['email'] in c.get('students', [])])
                        student_groups = len([g for g in groups if s['email'] in g.get('members', [])])
                        
                        report_data.append({
                            "Name": s['fullname'],
                            "Email": s['email'],
                            "Joined": s['joined'],
                            "Classes": student_classes,
                            "Groups": student_groups
                        })
                    
                    st.dataframe(report_data, use_container_width=True)
                else:
                    st.info("No student data available")
            
            with tab3:
                st.subheader("Teacher Report")
                
                teacher_users = [u for u in users if u['role'] == 'teacher']
                
                if teacher_users:
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
        
        # ---------- SCHOOL SETTINGS ----------
        elif menu == "⚙️ School Settings":
            st.title("⚙️ School Settings")
            
            with st.form("school_settings"):
                school_name = st.text_input("School Name", value=school.get('name', ''))
                school_motto = st.text_input("School Motto", value=school.get('motto', ''))
                school_city = st.text_input("City", value=school.get('city', ''))
                school_state = st.text_input("State", value=school.get('state', ''))
                
                col1, col2 = st.columns(2)
                with col1:
                    admin_name = st.text_input("Admin Name", value=school.get('admin_name', user['fullname']))
                with col2:
                    admin_email = st.text_input("Admin Email", value=school.get('admin_email', user['email']), disabled=True)
                
                if st.form_submit_button("💾 Save Settings", use_container_width=True):
                    school['name'] = school_name
                    school['motto'] = school_motto
                    school['city'] = school_city
                    school['state'] = school_state
                    school['admin_name'] = admin_name
                    
                    all_schools = load_all_schools()
                    all_schools[school_code] = school
                    save_all_schools(all_schools)
                    
                    st.success("✅ School settings saved!")
                    st.rerun()
        
        # ---------- ADMIN PROFILE ----------
        elif menu == "👤 My Profile":
            st.title("👤 My Profile")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("Profile Picture")
                if user.get('profile_pic'):
                    st.image(user['profile_pic'], width=200)
                else:
                    st.markdown("# 👑")
                
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
                    
                    save_school_data(school_code, "users.json", users)
                    user['profile_pic'] = f"data:image/png;base64,{img_str}"
                    st.success("✅ Profile picture updated!")
                    st.rerun()
            
            with col2:
                st.subheader("Edit Profile")
                with st.form("edit_admin_profile"):
                    fullname = st.text_input("Full Name", value=user.get('fullname', ''))
                    email = st.text_input("Email", value=user.get('email', ''), disabled=True)
                    phone = st.text_input("Phone Number", value=user.get('phone', ''))
                    title = st.text_input("Title", value=user.get('title', 'School Administrator'))
                    bio = st.text_area("Bio", value=user.get('bio', ''), height=100)
                    
                    if st.form_submit_button("💾 Update Profile", use_container_width=True):
                        for u in users:
                            if u['email'] == user['email']:
                                u['fullname'] = fullname
                                u['phone'] = phone
                                u['title'] = title
                                u['bio'] = bio
                                break
                        
                        save_school_data(school_code, "users.json", users)
                        user['fullname'] = fullname
                        user['phone'] = phone
                        user['title'] = title
                        user['bio'] = bio
                        st.success("✅ Profile updated!")
                        st.rerun()
    
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
                st.metric("📝 Assignments", len([a for a in assignments if a.get('teacher') == user['email']]))
            
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
                    st.info("You haven't been assigned any classes")
            
            with col2:
                st.subheader("✅ Pending Requests")
                teacher_pending = [r for r in class_requests if r['status'] == 'pending' and r.get('class_name') in [c['name'] for c in my_classes]]
                if teacher_pending:
                    st.warning(f"{len(teacher_pending)} pending request(s)")
                    if st.button("Review Requests"):
                        st.session_state.menu_index = 5
                        st.rerun()
                else:
                    st.success("No pending requests")
        
        # ---------- TEACHER ANNOUNCEMENTS ----------
        elif menu == "📢 My Announcements":
            st.title("📢 Post Announcement")
            
            with st.form("teacher_announcement"):
                title = st.text_input("Title")
                content = st.text_area("Content", height=150)
                
                my_classes = [c['name'] for c in classes if c.get('teacher') == user['email']]
                target = st.selectbox("Target Class", ["All Classes"] + my_classes) if my_classes else "All Classes"
                
                col1, col2 = st.columns(2)
                with col1:
                    important = st.checkbox("⭐ Important")
                
                if st.form_submit_button("📢 Post", use_container_width=True):
                    if title and content:
                        new_ann = {
                            "id": generate_id("ANN"),
                            "title": title,
                            "content": content,
                            "author": user['fullname'],
                            "author_email": user['email'],
                            "author_role": "teacher",
                            "target_class": target,
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "important": important
                        }
                        announcements.append(new_ann)
                        save_school_data(school_code, "announcements.json", announcements)
                        st.success("✅ Announcement posted!")
                        st.rerun()
            
            st.divider()
            st.subheader("📋 My Recent Announcements")
            my_anns = [a for a in announcements if a.get('author_email') == user['email']][-5:]
            if my_anns:
                for a in reversed(my_anns):
                    with st.container(border=True):
                        st.markdown(f"**{a['title']}**")
                        st.markdown(a['content'])
                        st.caption(f"{a['date']} | Target: {a.get('target_class', 'All')}")
            else:
                st.info("No announcements yet")
        
        # ---------- MY CLASSES ----------
        elif menu == "📚 My Classes":
            st.title("📚 My Classes")
            
            my_classes = [c for c in classes if c.get('teacher') == user['email']]
            
            if my_classes:
                for c in my_classes:
                    with st.expander(f"📖 {c['name']} - {c['code']}", expanded=True):
                        tab1, tab2, tab3 = st.tabs(["📝 Info", "👥 Students", "📊 Grades"])
                        
                        with tab1:
                            st.markdown(f"**Class Code:** `{c['code']}`")
                            st.markdown(f"**Subject:** {c.get('subject', 'N/A')}")
                            st.markdown(f"**Room:** {c.get('room', 'TBD')}")
                            st.markdown(f"**Schedule:** {c.get('schedule', 'TBD')}")
                            st.markdown(f"**Students:** {len(c.get('students', []))}/{c.get('max_students', 30)}")
                        
                        with tab2:
                            st.subheader("Enrolled Students")
                            enrolled = [u for u in users if u['email'] in c.get('students', [])]
                            
                            if enrolled:
                                for s in enrolled:
                                    col1, col2, col3 = st.columns([2, 2, 1])
                                    with col1:
                                        st.markdown(f"**{s['fullname']}**")
                                    with col2:
                                        st.markdown(f"📧 {s['email']}")
                                    with col3:
                                        if st.button("🗑️", key=f"remove_{c['code']}_{s['email']}"):
                                            c['students'].remove(s['email'])
                                            save_school_data(school_code, "classes.json", classes)
                                            st.rerun()
                                    st.divider()
                            else:
                                st.info("No students enrolled")
                        
                        with tab3:
                            st.subheader("Grade Book")
                            enrolled = [u for u in users if u['email'] in c.get('students', [])]
                            
                            if enrolled:
                                for s in enrolled:
                                    col1, col2 = st.columns([2, 1])
                                    with col1:
                                        st.markdown(f"**{s['fullname']}**")
                                    with col2:
                                        grade = st.selectbox(
                                            "Grade",
                                            ["A", "B", "C", "D", "F", "I", "N/A"],
                                            key=f"grade_{c['code']}_{s['email']}"
                                        )
                                        if st.button("Save", key=f"save_{c['code']}_{s['email']}"):
                                            grade_entry = {
                                                "student": s['email'],
                                                "student_name": s['fullname'],
                                                "class": c['name'],
                                                "grade": grade,
                                                "teacher": user['email'],
                                                "date": datetime.now().strftime("%Y-%m-%d")
                                            }
                                            grades.append(grade_entry)
                                            save_school_data(school_code, "grades.json", grades)
                                            st.success("Saved!")
                            else:
                                st.info("No students to grade")
            else:
                st.warning("You haven't been assigned to any classes yet")
        
        # ---------- MY GROUPS ----------
        elif menu == "👥 My Groups":
            st.title("👥 My Groups")
            
            my_groups = [g for g in groups if g.get('leader') == user['email']]
            
            tab1, tab2 = st.tabs(["➕ Create Group", "📋 My Groups"])
            
            with tab1:
                st.subheader("Create New Group")
                
                with st.form("teacher_create_group"):
                    group_name = st.text_input("Group Name")
                    group_description = st.text_area("Description")
                    
                    my_classes = [c['name'] for c in classes if c.get('teacher') == user['email']]
                    related_class = st.selectbox("Related Class", ["None"] + my_classes) if my_classes else "None"
                    
                    max_members = st.number_input("Max Members", min_value=2, max_value=50, value=10)
                    
                    if st.form_submit_button("✅ Create", use_container_width=True):
                        if group_name:
                            group_code = generate_group_code()
                            new_group = {
                                "id": generate_id("GRP"),
                                "code": group_code,
                                "name": group_name,
                                "description": group_description,
                                "class": None if related_class == "None" else related_class,
                                "leader": user['email'],
                                "leader_name": user['fullname'],
                                "created": datetime.now().strftime("%Y-%m-%d"),
                                "max_members": max_members,
                                "members": [user['email']],
                                "pending_requests": [],
                                "status": "active"
                            }
                            groups.append(new_group)
                            save_school_data(school_code, "groups.json", groups)
                            school['stats']['groups'] = school['stats'].get('groups', 0) + 1
                            
                            all_schools = load_all_schools()
                            all_schools[school_code] = school
                            save_all_schools(all_schools)
                            
                            st.success(f"✅ Group created! Code: {group_code}")
                            st.rerun()
            
            with tab2:
                if my_groups:
                    for g in my_groups:
                        with st.expander(f"👥 {g['name']} - {g['code']}"):
                            st.markdown(f"**Description:** {g.get('description', 'No description')}")
                            st.markdown(f"**Members:** {len(g.get('members', []))}/{g.get('max_members', 10)}")
                            st.markdown(f"**Code:** `{g['code']}`")
                            
                            # Show members
                            st.markdown("**Members:**")
                            for member_email in g.get('members', []):
                                member = next((u for u in users if u['email'] == member_email), None)
                                if member:
                                    st.markdown(f"- {member['fullname']} ({member['role']})")
                            
                            if st.button("🗑️ Delete", key=f"del_teacher_group_{g['id']}"):
                                groups.remove(g)
                                save_school_data(school_code, "groups.json", groups)
                                school['stats']['groups'] -= 1
                                all_schools = load_all_schools()
                                all_schools[school_code] = school
                                save_all_schools(all_schools)
                                st.rerun()
                else:
                    st.info("You haven't created any groups yet")
        
        # ---------- ASSIGNMENTS ----------
        elif menu == "📝 Assignments":
            st.title("📝 Create Assignment")
            
            my_classes = [c['name'] for c in classes if c.get('teacher') == user['email']]
            
            if my_classes:
                with st.form("create_assignment"):
                    class_name = st.selectbox("Class", my_classes)
                    title = st.text_input("Assignment Title")
                    description = st.text_area("Description")
                    due_date = st.date_input("Due Date")
                    total_points = st.number_input("Total Points", min_value=1, value=100)
                    
                    assignment_code = generate_id("ASN")
                    
                    if st.form_submit_button("✅ Create", use_container_width=True):
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
                        save_school_data(school_code, "assignments.json", assignments)
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
                st.warning("You need to be assigned to a class first")
        
        # ---------- APPROVE REQUESTS ----------
        elif menu.startswith("✅ Approve Requests"):
            st.title("✅ Approve Join Requests")
            
            my_classes = [c['name'] for c in classes if c.get('teacher') == user['email']]
            my_groups = [g['name'] for g in groups if g.get('leader') == user['email']]
            
            tab1, tab2 = st.tabs(["📚 Class Requests", "👥 Group Requests"])
            
            with tab1:
                class_reqs = [r for r in class_requests if r['status'] == 'pending' and r.get('class_name') in my_classes]
                
                if class_reqs:
                    for req in class_reqs:
                        with st.container(border=True):
                            col1, col2, col3 = st.columns([2, 2, 2])
                            with col1:
                                st.markdown(f"**{req['student_name']}**")
                                st.markdown(f"📧 {req['student_email']}")
                            with col2:
                                st.markdown(f"**Class:** {req['class_name']}")
                                st.markdown(f"📅 {req['date']}")
                            with col3:
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    if st.button("✅", key=f"app_class_t_{req['id']}"):
                                        for c in classes:
                                            if c['name'] == req['class_name']:
                                                if req['student_email'] not in c['students']:
                                                    c['students'].append(req['student_email'])
                                        save_school_data(school_code, "classes.json", classes)
                                        
                                        req['status'] = 'approved'
                                        req['approved_by'] = user['email']
                                        req['approved_date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                                        save_school_data(school_code, "class_requests.json", class_requests)
                                        st.rerun()
                                with col_b:
                                    if st.button("❌", key=f"deny_class_t_{req['id']}"):
                                        req['status'] = 'denied'
                                        req['denied_by'] = user['email']
                                        req['denied_date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                                        save_school_data(school_code, "class_requests.json", class_requests)
                                        st.rerun()
                else:
                    st.info("No pending class requests")
            
            with tab2:
                group_reqs = [r for r in group_requests if r['status'] == 'pending' and r.get('group_name') in my_groups]
                
                if group_reqs:
                    for req in group_reqs:
                        with st.container(border=True):
                            col1, col2, col3 = st.columns([2, 2, 2])
                            with col1:
                                st.markdown(f"**{req['student_name']}**")
                                st.markdown(f"📧 {req['student_email']}")
                            with col2:
                                st.markdown(f"**Group:** {req['group_name']}")
                                st.markdown(f"📅 {req['date']}")
                            with col3:
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    if st.button("✅", key=f"app_group_t_{req['id']}"):
                                        for g in groups:
                                            if g['name'] == req['group_name']:
                                                if req['student_email'] not in g['members']:
                                                    g['members'].append(req['student_email'])
                                        save_school_data(school_code, "groups.json", groups)
                                        
                                        req['status'] = 'approved'
                                        req['approved_by'] = user['email']
                                        req['approved_date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                                        save_school_data(school_code, "group_requests.json", group_requests)
                                        st.rerun()
                                with col_b:
                                    if st.button("❌", key=f"deny_group_t_{req['id']}"):
                                        req['status'] = 'denied'
                                        req['denied_by'] = user['email']
                                        req['denied_date'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                                        save_school_data(school_code, "group_requests.json", group_requests)
                                        st.rerun()
                else:
                    st.info("No pending group requests")
        
        # ---------- RESOURCES ----------
        elif menu == "📎 Resources":
            st.title("📎 Resources")
            
            with st.form("upload_resource"):
                my_classes = [c['name'] for c in classes if c.get('teacher') == user['email']]
                class_name = st.selectbox("Class", my_classes) if my_classes else "General"
                
                title = st.text_input("Resource Title")
                description = st.text_area("Description")
                resource_type = st.selectbox("Type", ["Notes", "Worksheet", "Presentation", "Video", "Link"])
                
                if st.form_submit_button("📤 Upload", use_container_width=True):
                    if title:
                        new_resource = {
                            "id": generate_id("RES"),
                            "class": class_name,
                            "title": title,
                            "description": description,
                            "type": resource_type,
                            "teacher": user['fullname'],
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "downloads": 0
                        }
                        resources.append(new_resource)
                        save_school_data(school_code, "resources.json", resources)
                        st.success("✅ Resource uploaded!")
                        st.rerun()
        
        # ---------- DISCUSSIONS ----------
        elif menu == "💬 Discussions":
            st.title("💬 Discussions")
            
            with st.form("start_discussion"):
                topic = st.text_input("Topic")
                message = st.text_area("Message")
                
                if st.form_submit_button("💬 Post", use_container_width=True):
                    new_discussion = {
                        "id": generate_id("DIS"),
                        "topic": topic,
                        "message": message,
                        "author": user['fullname'],
                        "author_role": "teacher",
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "replies": []
                    }
                    discussions.append(new_discussion)
                    save_school_data(school_code, "discussions.json", discussions)
                    st.success("Discussion posted!")
                    st.rerun()
        
        # ---------- GRADE BOOK ----------
        elif menu == "📊 Grade Book":
            st.title("📊 Grade Book")
            
            my_classes = [c['name'] for c in classes if c.get('teacher') == user['email']]
            
            if my_classes:
                selected_class = st.selectbox("Select Class", my_classes)
                class_obj = next((c for c in classes if c['name'] == selected_class), None)
                
                if class_obj:
                    st.subheader(f"Grades - {selected_class}")
                    
                    enrolled = [u for u in users if u['email'] in class_obj.get('students', [])]
                    class_assignments = [a for a in assignments if a.get('class') == selected_class]
                    
                    if enrolled and class_assignments:
                        for s in enrolled:
                            with st.expander(s['fullname']):
                                for a in class_assignments:
                                    col1, col2 = st.columns([3, 1])
                                    with col1:
                                        st.markdown(f"**{a['title']}**")
                                    with col2:
                                        grade = st.text_input("Grade", key=f"g_{s['email']}_{a['code']}", placeholder="A, B, 85")
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
                                            save_school_data(school_code, "grades.json", grades)
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
                    
                    save_school_data(school_code, "users.json", users)
                    user['profile_pic'] = f"data:image/png;base64,{img_str}"
                    st.success("✅ Profile picture updated!")
                    st.rerun()
            
            with col2:
                st.subheader("Edit Profile")
                with st.form("edit_teacher_profile"):
                    fullname = st.text_input("Full Name", value=user.get('fullname', ''))
                    email = st.text_input("Email", value=user.get('email', ''), disabled=True)
                    phone = st.text_input("Phone", value=user.get('phone', ''))
                    bio = st.text_area("Bio", value=user.get('bio', ''), height=100)
                    
                    if st.form_submit_button("💾 Update", use_container_width=True):
                        for u in users:
                            if u['email'] == user['email']:
                                u['fullname'] = fullname
                                u['phone'] = phone
                                u['bio'] = bio
                                break
                        
                        save_school_data(school_code, "users.json", users)
                        user['fullname'] = fullname
                        user['phone'] = phone
                        user['bio'] = bio
                        st.success("✅ Profile updated!")
                        st.rerun()
    
    # ----- STUDENT DASHBOARD -----
    else:
        
        # ---------- STUDENT DASHBOARD ----------
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
                upcoming = [a for a in assignments if a.get('class') in [c['name'] for c in my_classes]]
                st.metric("📝 Assignments", len(upcoming))
            
            st.divider()
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📚 My Classes")
                if my_classes:
                    for c in my_classes[:3]:
                        with st.container(border=True):
                            st.markdown(f"**{c['name']}**")
                            st.markdown(f"Teacher: {c.get('teacher_name', c['teacher'])}")
                else:
                    st.info("You haven't joined any classes yet")
            
            with col2:
                st.subheader("📢 Recent Announcements")
                relevant = [a for a in announcements if a.get('target_class') in ['All Classes'] + [c['name'] for c in my_classes]][:3]
                if relevant:
                    for a in relevant:
                        st.markdown(f"- **{a['title']}**")
                else:
                    st.info("No recent announcements")
        
        # ---------- STUDENT ANNOUNCEMENTS ----------
        elif menu == "📢 Announcements":
            st.title("📢 Announcements")
            
            my_classes = [c['name'] for c in classes if user['email'] in c.get('students', [])]
            relevant = [a for a in announcements if a.get('target_class') in ['All Classes'] + my_classes]
            
            if relevant:
                for a in reversed(relevant[-20:]):
                    with st.container(border=True):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**{a['title']}**" + (" ⭐" if a.get('important') else ""))
                            st.markdown(a['content'])
                        with col2:
                            st.caption(f"By: {a['author']}")
                            st.caption(a['date'][:16])
            else:
                st.info("No announcements")
        
        # ---------- BROWSE CLASSES ----------
        elif menu == "📚 Browse Classes":
            st.title("📚 Browse Available Classes")
            
            my_classes = [c['name'] for c in classes if user['email'] in c.get('students', [])]
            available = [c for c in classes if user['email'] not in c.get('students', []) and len(c.get('students', [])) < c.get('max_students', 30)]
            
            if available:
                st.subheader(f"Available Classes ({len(available)})")
                
                for c in available:
                    with st.container(border=True):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**{c['name']}**")
                            st.markdown(f"Teacher: {c.get('teacher_name', c['teacher'])}")
                            st.markdown(f"Schedule: {c.get('schedule', 'TBD')}")
                            st.markdown(f"Students: {len(c.get('students', []))}/{c.get('max_students', 30)}")
                        with col2:
                            if st.button("📝 Request to Join", key=f"req_class_{c['code']}"):
                                # Create join request
                                request = {
                                    "id": generate_id("REQ"),
                                    "student_email": user['email'],
                                    "student_name": user['fullname'],
                                    "class_name": c['name'],
                                    "class_code": c['code'],
                                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                    "status": "pending"
                                }
                                class_requests.append(request)
                                save_school_data(school_code, "class_requests.json", class_requests)
                                st.success("✅ Request sent to teacher!")
                                st.rerun()
            else:
                st.info("No available classes to join")
            
            st.divider()
            st.subheader("📋 My Classes")
            if my_classes:
                for c in my_classes:
                    with st.container(border=True):
                        st.markdown(f"**{c}** - Enrolled")
            else:
                st.info("You haven't joined any classes yet")
        
        # ---------- BROWSE GROUPS ----------
        elif menu == "👥 Browse Groups":
            st.title("👥 Browse Available Groups")
            
            my_groups = [g['name'] for g in groups if user['email'] in g.get('members', [])]
            available = [g for g in groups if user['email'] not in g.get('members', []) and len(g.get('members', [])) < g.get('max_members', 10)]
            
            if available:
                st.subheader(f"Available Groups ({len(available)})")
                
                for g in available:
                    with st.container(border=True):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**{g['name']}**")
                            st.markdown(f"Leader: {g.get('leader_name', 'Unknown')}")
                            st.markdown(f"Class: {g.get('class', 'General')}")
                            st.markdown(f"Members: {len(g.get('members', []))}/{g.get('max_members', 10)}")
                        with col2:
                            if st.button("📝 Request to Join", key=f"req_group_{g['code']}"):
                                request = {
                                    "id": generate_id("REQ"),
                                    "student_email": user['email'],
                                    "student_name": user['fullname'],
                                    "group_name": g['name'],
                                    "group_code": g['code'],
                                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                    "status": "pending"
                                }
                                group_requests.append(request)
                                save_school_data(school_code, "group_requests.json", group_requests)
                                st.success("✅ Request sent to group leader!")
                                st.rerun()
            else:
                st.info("No available groups to join")
            
            st.divider()
            st.subheader("👥 My Groups")
            if my_groups:
                for g in my_groups:
                    with st.container(border=True):
                        st.markdown(f"**{g}** - Member")
            else:
                st.info("You haven't joined any groups yet")
        
        # ---------- HOMEWORK ----------
        elif menu == "📝 My Homework":
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
                            if st.button("✓ Mark Complete", key=f"hw_{a['code']}"):
                                st.success("Good job!")
            else:
                st.info("No homework assigned")
        
        # ---------- STUDY MATERIALS ----------
        elif menu == "📎 Study Materials":
            st.title("📎 Study Materials")
            
            my_classes = [c['name'] for c in classes if user['email'] in c.get('students', [])]
            my_resources = [r for r in resources if r.get('class') in my_classes]
            
            if my_resources:
                for r in my_resources:
                    with st.container(border=True):
                        st.markdown(f"**{r['title']}**")
                        st.markdown(f"Class: {r['class']} | Type: {r['type']}")
                        st.markdown(r.get('description', ''))
                        st.caption(f"Uploaded by: {r.get('teacher', 'Unknown')} on {r['date']}")
                        st.button("📥 Download", key=f"dl_{r['id']}")
            else:
                st.info("No study materials available")
        
        # ---------- DISCUSSION BOARD ----------
        elif menu == "💬 Discussion Board":
            st.title("💬 Discussion Board")
            
            if discussions:
                for d in reversed(discussions[-10:]):
                    with st.expander(f"💭 {d['topic']}"):
                        st.markdown(f"**{d['author']}** ({d['author_role']}) - {d['date']}")
                        st.markdown(d['message'])
                        
                        st.markdown("---")
                        reply = st.text_input("Write a reply...", key=f"reply_{d['id']}")
                        if st.button("Post Reply", key=f"reply_btn_{d['id']}"):
                            st.success("Reply posted!")
            else:
                st.info("No discussions yet")
        
        # ---------- MY GRADES ----------
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
        
        # ---------- STUDENT PROFILE ----------
        elif menu == "👤 My Profile":
            st.title("👤 My Profile")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("Profile Picture")
                if user.get('profile_pic'):
                    st.image(user['profile_pic'], width=200)
                else:
                    st.markdown("# 👨‍🎓")
                
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
                    
                    save_school_data(school_code, "users.json", users)
                    user['profile_pic'] = f"data:image/png;base64,{img_str}"
                    st.success("✅ Profile picture updated!")
                    st.rerun()
            
            with col2:
                st.subheader("Edit Profile")
                with st.form("edit_student_profile"):
                    fullname = st.text_input("Full Name", value=user.get('fullname', ''))
                    email = st.text_input("Email", value=user.get('email', ''), disabled=True)
                    phone = st.text_input("Phone", value=user.get('phone', ''))
                    bio = st.text_area("Bio", value=user.get('bio', ''), height=100)
                    
                    if st.form_submit_button("💾 Update", use_container_width=True):
                        for u in users:
                            if u['email'] == user['email']:
                                u['fullname'] = fullname
                                u['phone'] = phone
                                u['bio'] = bio
                                break
                        
                        save_school_data(school_code, "users.json", users)
                        user['fullname'] = fullname
                        user['phone'] = phone
                        user['bio'] = bio
                        st.success("✅ Profile updated!")
                        st.rerun()

# ----- FALLBACK -----
else:
    st.error("Something went wrong. Please refresh the page.")
    if st.button("Start Over"):
        st.session_state.school = None
        st.session_state.user = None
        st.session_state.page = 'welcome'
        st.rerun()
