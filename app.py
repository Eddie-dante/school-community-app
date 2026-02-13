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

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="School Community Hub",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ CUSTOM CSS ============
st.markdown("""
<style>
    /* Main container */
    .main {
        padding: 1rem 2rem;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1e3c72;
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102,126,234,0.4);
    }
    
    /* Cards */
    .css-1r6slb0, .st-b7 {
        border-radius: 12px;
        padding: 1.5rem;
        background: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid #f0f2f5;
    }
    
    /* Metrics */
    .stMetric {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8faff 0%, #ffffff 100%);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: white;
        padding: 0.5rem;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: #667eea;
        color: white !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: white;
        border-radius: 8px;
        border: 1px solid #e0e7ff;
    }
    
    /* Success/Warning/Error boxes */
    .stAlert {
        border-radius: 10px;
        border-left-width: 4px;
    }
    
    /* Footer */
    footer {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# ============ CODE GENERATOR ============
def generate_id(prefix, length=8):
    chars = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choices(chars, k=length))
    return f"{prefix}{random_part}"

def generate_school_code():
    chars = string.ascii_uppercase + string.digits
    return 'SCH' + ''.join(random.choices(chars, k=6))

def generate_class_code():
    return 'CLS' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def generate_group_code():
    return 'GRP' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# ============ DATA STORAGE ============
DATA_DIR = Path("school_data")
DATA_DIR.mkdir(exist_ok=True)

SCHOOLS_FILE = DATA_DIR / "all_schools.json"

def load_all_schools():
    if SCHOOLS_FILE.exists():
        with open(SCHOOLS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_all_schools(schools):
    with open(SCHOOLS_FILE, 'w') as f:
        json.dump(schools, f, indent=2)

def load_school_data(school_code, filename, default):
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
    st.markdown("<h1 style='text-align: center; color: #1e3c72;'>🎓 School Community Hub</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #4a5568; font-size: 1.2rem;'>Connect • Collaborate • Grow</p>", unsafe_allow_html=True)
    st.divider()
    
    tab1, tab2, tab3, tab4 = st.tabs(["👑 Admin", "🏫 New School", "👨‍🏫 Teachers", "👨‍🎓 Students"])
    
    # ---------- TAB 1: ADMIN LOGIN ----------
    with tab1:
        col1, col2 = st.columns([1,1])
        with col1:
            with st.form("admin_login"):
                st.subheader("🔐 Admin Login")
                school_code = st.text_input("School Code")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                if st.form_submit_button("Login", use_container_width=True):
                    if not school_code or not email or not password:
                        st.error("All fields required")
                    else:
                        all_schools = load_all_schools()
                        if school_code in all_schools:
                            school = all_schools[school_code]
                            if school['admin_email'] == email:
                                users = load_school_data(school_code, "users.json", [])
                                hashed = hashlib.sha256(password.encode()).hexdigest()
                                for u in users:
                                    if u['email'] == email and u['password'] == hashed and u['role'] == 'admin':
                                        st.session_state.current_school = school
                                        st.session_state.user = u
                                        st.session_state.page = 'dashboard'
                                        st.rerun()
                                st.error("Invalid password")
                            else:
                                st.error("Not the admin email")
                        else:
                            st.error("School not found")
        with col2:
            st.markdown("### 👑 Admin Access")
            st.info("Login with your school code and admin credentials.")
    
    # ---------- TAB 2: CREATE SCHOOL ----------
    with tab2:
        col1, col2 = st.columns([1,1])
        with col1:
            with st.form("create_school"):
                st.subheader("🏫 Create Your School")
                school_name = st.text_input("School Name")
                admin_name = st.text_input("Your Full Name")
                admin_email = st.text_input("Your Email")
                password = st.text_input("Password", type="password")
                confirm = st.text_input("Confirm Password", type="password")
                city = st.text_input("City")
                state = st.text_input("State/Province")
                motto = st.text_input("School Motto")
                
                if st.form_submit_button("Create School", use_container_width=True):
                    if not school_name or not admin_email or not password:
                        st.error("Required fields missing")
                    elif password != confirm:
                        st.error("Passwords do not match")
                    else:
                        all_schools = load_all_schools()
                        code = generate_school_code()
                        while code in all_schools:
                            code = generate_school_code()
                        
                        new_school = {
                            "code": code,
                            "name": school_name,
                            "city": city,
                            "state": state,
                            "motto": motto,
                            "created": datetime.now().strftime("%Y-%m-%d"),
                            "admin_email": admin_email,
                            "admin_name": admin_name,
                            "stats": {"students":0, "teachers":0, "classes":0, "groups":0}
                        }
                        all_schools[code] = new_school
                        save_all_schools(all_schools)
                        
                        users = [{
                            "user_id": generate_id("USR"),
                            "email": admin_email,
                            "fullname": admin_name,
                            "password": hashlib.sha256(password.encode()).hexdigest(),
                            "role": "admin",
                            "joined": datetime.now().strftime("%Y-%m-%d"),
                            "school_code": code
                        }]
                        save_school_data(code, "users.json", users)
                        save_school_data(code, "teachers.json", [])
                        save_school_data(code, "classes.json", [])
                        save_school_data(code, "groups.json", [])
                        save_school_data(code, "announcements.json", [])
                        save_school_data(code, "assignments.json", [])
                        save_school_data(code, "resources.json", [])
                        save_school_data(code, "events.json", [])
                        save_school_data(code, "discussions.json", [])
                        save_school_data(code, "grades.json", [])
                        save_school_data(code, "class_requests.json", [])
                        save_school_data(code, "group_requests.json", [])
                        
                        st.session_state.current_school = new_school
                        st.session_state.user = users[0]
                        st.session_state.page = 'dashboard'
                        st.success(f"School created! Code: {code}")
                        st.rerun()
        with col2:
            st.markdown("### 🎓 Start Your Community")
            st.info("Create a new school and become its administrator.")
    
    # ---------- TAB 3: TEACHER LOGIN & REGISTER ----------
    with tab3:
        subtab1, subtab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with subtab1:
            col1, col2 = st.columns([1,1])
            with col1:
                with st.form("teacher_login"):
                    st.subheader("Teacher Login")
                    school_code = st.text_input("School Code")
                    email = st.text_input("Email")
                    password = st.text_input("Password", type="password")
                    if st.form_submit_button("Login", use_container_width=True):
                        if not school_code or not email or not password:
                            st.error("All fields required")
                        else:
                            all_schools = load_all_schools()
                            if school_code in all_schools:
                                school = all_schools[school_code]
                                users = load_school_data(school_code, "users.json", [])
                                hashed = hashlib.sha256(password.encode()).hexdigest()
                                for u in users:
                                    if u['email'] == email and u['password'] == hashed and u['role'] == 'teacher':
                                        st.session_state.current_school = school
                                        st.session_state.user = u
                                        st.session_state.page = 'dashboard'
                                        st.rerun()
                                st.error("Invalid credentials")
                            else:
                                st.error("School not found")
            with col2:
                st.markdown("### 👨‍🏫 Existing Teachers")
                st.info("Login with your email and password.")
        
        with subtab2:
            col1, col2 = st.columns([1,1])
            with col1:
                with st.form("teacher_register"):
                    st.subheader("New Teacher Registration")
                    school_code = st.text_input("School Code", key="reg_school")
                    teacher_code = st.text_input("Teacher Code")
                    fullname = st.text_input("Full Name")
                    email = st.text_input("Email", key="reg_email")
                    password = st.text_input("Password", type="password", key="reg_pass")
                    confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
                    
                    if st.form_submit_button("Register", use_container_width=True):
                        if not all([school_code, teacher_code, fullname, email, password]):
                            st.error("All fields required")
                        elif password != confirm:
                            st.error("Passwords do not match")
                        else:
                            all_schools = load_all_schools()
                            if school_code not in all_schools:
                                st.error("School not found")
                            else:
                                school = all_schools[school_code]
                                teachers_data = load_school_data(school_code, "teachers.json", [])
                                # Verify teacher code
                                valid = False
                                record = None
                                for t in teachers_data:
                                    if t['code'] == teacher_code.upper() and t['status'] == 'active':
                                        valid = True
                                        record = t
                                        t.setdefault('used_by_list', []).append({
                                            "email": email,
                                            "name": fullname,
                                            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                                        })
                                        t['last_used'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                                        t['last_used_by'] = email
                                        break
                                if not valid:
                                    st.error("Invalid teacher code")
                                    st.stop()
                                
                                users = load_school_data(school_code, "users.json", [])
                                if any(u['email'] == email for u in users):
                                    st.error("Email already registered")
                                    st.stop()
                                
                                new_user = {
                                    "user_id": generate_id("USR"),
                                    "email": email,
                                    "fullname": fullname,
                                    "password": hashlib.sha256(password.encode()).hexdigest(),
                                    "role": "teacher",
                                    "title": f"Teacher - {record.get('department','General')}",
                                    "joined": datetime.now().strftime("%Y-%m-%d"),
                                    "school_code": school_code,
                                    "teacher_code_used": teacher_code.upper(),
                                    "classes": [],
                                    "groups": []
                                }
                                users.append(new_user)
                                save_school_data(school_code, "users.json", users)
                                save_school_data(school_code, "teachers.json", teachers_data)
                                
                                school['stats']['teachers'] = school['stats'].get('teachers',0)+1
                                all_schools[school_code] = school
                                save_all_schools(all_schools)
                                
                                st.session_state.current_school = school
                                st.session_state.user = new_user
                                st.session_state.page = 'dashboard'
                                st.success("Registration successful!")
                                st.rerun()
            with col2:
                st.markdown("### 🆕 New Teacher")
                st.info("Use the teacher code provided by your admin.")
    
    # ---------- TAB 4: STUDENT LOGIN & REGISTER ----------
    with tab4:
        subtab1, subtab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with subtab1:
            col1, col2 = st.columns([1,1])
            with col1:
                with st.form("student_login"):
                    st.subheader("Student Login")
                    school_code = st.text_input("School Code")
                    email = st.text_input("Email")
                    password = st.text_input("Password", type="password")
                    if st.form_submit_button("Login", use_container_width=True):
                        if not school_code or not email or not password:
                            st.error("All fields required")
                        else:
                            all_schools = load_all_schools()
                            if school_code in all_schools:
                                school = all_schools[school_code]
                                users = load_school_data(school_code, "users.json", [])
                                hashed = hashlib.sha256(password.encode()).hexdigest()
                                for u in users:
                                    if u['email'] == email and u['password'] == hashed and u['role'] == 'student':
                                        st.session_state.current_school = school
                                        st.session_state.user = u
                                        st.session_state.page = 'dashboard'
                                        st.rerun()
                                st.error("Invalid credentials")
                            else:
                                st.error("School not found")
            with col2:
                st.markdown("### 👨‍🎓 Existing Students")
                st.info("Login with your email and password.")
        
        with subtab2:
            col1, col2 = st.columns([1,1])
            with col1:
                with st.form("student_register"):
                    st.subheader("New Student Registration")
                    school_code = st.text_input("School Code", key="stud_reg_school")
                    fullname = st.text_input("Full Name")
                    email = st.text_input("Email", key="stud_reg_email")
                    password = st.text_input("Password", type="password", key="stud_reg_pass")
                    confirm = st.text_input("Confirm Password", type="password", key="stud_reg_confirm")
                    
                    if st.form_submit_button("Register", use_container_width=True):
                        if not all([school_code, fullname, email, password]):
                            st.error("All fields required")
                        elif password != confirm:
                            st.error("Passwords do not match")
                        else:
                            all_schools = load_all_schools()
                            if school_code not in all_schools:
                                st.error("School not found")
                            else:
                                school = all_schools[school_code]
                                users = load_school_data(school_code, "users.json", [])
                                if any(u['email'] == email for u in users):
                                    st.error("Email already registered")
                                else:
                                    new_user = {
                                        "user_id": generate_id("USR"),
                                        "email": email,
                                        "fullname": fullname,
                                        "password": hashlib.sha256(password.encode()).hexdigest(),
                                        "role": "student",
                                        "joined": datetime.now().strftime("%Y-%m-%d"),
                                        "school_code": school_code,
                                        "classes": [],
                                        "groups": []
                                    }
                                    users.append(new_user)
                                    save_school_data(school_code, "users.json", users)
                                    school['stats']['students'] = school['stats'].get('students',0)+1
                                    all_schools[school_code] = school
                                    save_all_schools(all_schools)
                                    
                                    st.session_state.current_school = school
                                    st.session_state.user = new_user
                                    st.session_state.page = 'dashboard'
                                    st.success("Registration successful!")
                                    st.rerun()
            with col2:
                st.markdown("### 🆕 New Student")
                st.info("Register using your school code.")

# ----- DASHBOARD -----
elif st.session_state.page == 'dashboard' and st.session_state.current_school and st.session_state.user:
    school = st.session_state.current_school
    user = st.session_state.user
    school_code = school['code']
    
    # Load data
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
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px; color: white; text-align: center;">
            <h2 style="color: white; margin-bottom: 0;">{school['name']}</h2>
            <p style="color: #e0e7ff; font-size: 0.9rem;">{school.get('motto','')}</p>
            <p style="background: rgba(255,255,255,0.2); padding: 5px; border-radius: 20px; font-size: 0.8rem;">Code: {school['code']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # User profile card
        col1, col2 = st.columns([1,2])
        with col1:
            if user.get('profile_pic'):
                st.image(user['profile_pic'], width=60)
            else:
                if user['role'] == 'admin':
                    st.markdown("<h1 style='font-size: 3rem;'>👑</h1>", unsafe_allow_html=True)
                elif user['role'] == 'teacher':
                    st.markdown("<h1 style='font-size: 3rem;'>👨‍🏫</h1>", unsafe_allow_html=True)
                else:
                    st.markdown("<h1 style='font-size: 3rem;'>👨‍🎓</h1>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"**{user['fullname']}**")
            st.caption(f"{user['role'].title()}")
            st.caption(f"{user['email']}")
        
        st.markdown("---")
        
        # Navigation
        if user['role'] == 'admin':
            menu = st.radio("Menu", [
                "Dashboard", "Announcements", "Teachers", "Classes", 
                "Students", "Groups", "Approvals", "Codes", "Reports", "Settings", "Profile"
            ])
        elif user['role'] == 'teacher':
            menu = st.radio("Menu", [
                "Dashboard", "Announcements", "My Classes", "My Groups",
                "Assignments", "Requests", "Resources", "Discussions", "Gradebook", "Profile"
            ])
        else:
            menu = st.radio("Menu", [
                "Dashboard", "Announcements", "Browse Classes", "Browse Groups",
                "Homework", "Study Materials", "Discussions", "My Grades", "Profile"
            ])
        
        st.markdown("---")
        if st.button("Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.current_school = None
            st.session_state.page = 'welcome'
            st.rerun()
    
    # ============ MAIN CONTENT ============
    
    # ----- ADMIN -----
    if user['role'] == 'admin':
        if menu == "Dashboard":
            st.header(f"👑 {school['name']}")
            col1,col2,col3,col4 = st.columns(4)
            col1.metric("Students", school['stats'].get('students',0))
            col2.metric("Teachers", school['stats'].get('teachers',0))
            col3.metric("Classes", school['stats'].get('classes',0))
            col4.metric("Groups", school['stats'].get('groups',0))
            
            st.divider()
            pending = len([r for r in class_requests if r['status']=='pending']) + \
                     len([r for r in group_requests if r['status']=='pending'])
            if pending:
                st.warning(f"{pending} pending approval requests")
            else:
                st.success("No pending requests")
        
        elif menu == "Teachers":
            st.header("👨‍🏫 Teacher Management")
            tab1, tab2 = st.tabs(["Create Codes", "Active Teachers"])
            with tab1:
                with st.form("create_teacher_code"):
                    name = st.text_input("Code Name/Department")
                    code = st.text_input("Custom Teacher Code (e.g., MATH-DEPT)")
                    dept = st.selectbox("Department", ["Mathematics","Science","English","History","CS","Other"])
                    if st.form_submit_button("Create Code"):
                        if name and code:
                            exists = any(t['code']==code.upper() for t in teachers_data)
                            if exists:
                                st.error("Code already exists")
                            else:
                                teachers_data.append({
                                    "id": generate_id("TCH"),
                                    "name": name,
                                    "code": code.upper(),
                                    "department": dept,
                                    "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                    "status": "active",
                                    "used_by_list": []
                                })
                                save_school_data(school_code, "teachers.json", teachers_data)
                                st.success(f"Code {code.upper()} created")
                                st.rerun()
            with tab2:
                for t in teachers_data:
                    with st.container(border=True):
                        st.write(f"**{t['name']}** - `{t['code']}`")
                        st.caption(f"Used by: {len(t.get('used_by_list',[]))} teachers")
        
        elif menu == "Classes":
            st.header("📚 Classes")
            # Simplified: just create class
            with st.form("create_class"):
                name = st.text_input("Class Name")
                subject = st.text_input("Subject")
                grade = st.selectbox("Grade", ["9","10","11","12"])
                # teacher selection
                teacher_opts = []
                for t in teachers_data:
                    for u in t.get('used_by_list',[]):
                        teacher_opts.append(f"{u['name']} ({u['email']})")
                teacher = st.selectbox("Teacher", teacher_opts) if teacher_opts else None
                room = st.text_input("Room")
                schedule = st.text_input("Schedule")
                if st.form_submit_button("Create"):
                    if name and teacher:
                        code = generate_class_code()
                        classes.append({
                            "id": generate_id("CLS"),
                            "code": code,
                            "name": name,
                            "subject": subject,
                            "grade": grade,
                            "teacher": teacher.split('(')[1].strip(')') if teacher else "",
                            "teacher_name": teacher.split('(')[0].strip() if teacher else "",
                            "room": room,
                            "schedule": schedule,
                            "students": []
                        })
                        save_school_data(school_code, "classes.json", classes)
                        school['stats']['classes'] += 1
                        save_all_schools(load_all_schools())
                        st.success(f"Class created: {code}")
                        st.rerun()
        
        elif menu == "Students":
            st.header("👨‍🎓 Students")
            students = [u for u in users if u['role']=='student']
            for s in students:
                with st.container(border=True):
                    col1,col2,col3 = st.columns([3,3,1])
                    col1.write(f"**{s['fullname']}**")
                    col2.write(s['email'])
                    if col3.button("🗑️", key=f"del_{s['user_id']}"):
                        users.remove(s)
                        save_school_data(school_code, "users.json", users)
                        school['stats']['students'] -= 1
                        save_all_schools(load_all_schools())
                        st.rerun()
        
        elif menu == "Groups":
            st.header("👥 Groups")
            # Simplified group management with veto power
            st.subheader("All Groups")
            for g in groups:
                with st.expander(f"{g['name']} - {g['code']}"):
                    st.write(f"Leader: {g['leader_name']}")
                    st.write(f"Members: {len(g['members'])}/{g['max_members']}")
                    if st.button("Delete", key=f"delg_{g['id']}"):
                        groups.remove(g)
                        save_school_data(school_code, "groups.json", groups)
                        st.rerun()
        
        elif menu == "Approvals":
            st.header("✅ Admin Veto Power")
            tab1, tab2 = st.tabs(["Class Requests", "Group Requests"])
            with tab1:
                for req in [r for r in class_requests if r['status']=='pending']:
                    col1,col2,col3 = st.columns([2,2,2])
                    col1.write(req['student_name'])
                    col2.write(req['class_name'])
                    if col3.button("✅ Approve", key=f"app_c_{req['id']}"):
                        for c in classes:
                            if c['name'] == req['class_name']:
                                c['students'].append(req['student_email'])
                        req['status'] = 'approved'
                        req['approved_by'] = user['email'] + " (Veto)"
                        save_school_data(school_code, "classes.json", classes)
                        save_school_data(school_code, "class_requests.json", class_requests)
                        st.rerun()
            with tab2:
                for req in [r for r in group_requests if r['status']=='pending']:
                    col1,col2,col3 = st.columns([2,2,2])
                    col1.write(req['student_name'])
                    col2.write(req['group_name'])
                    if col3.button("✅ Approve", key=f"app_g_{req['id']}"):
                        for g in groups:
                            if g['name'] == req['group_name']:
                                g['members'].append(req['student_email'])
                        req['status'] = 'approved'
                        req['approved_by'] = user['email'] + " (Veto)"
                        save_school_data(school_code, "groups.json", groups)
                        save_school_data(school_code, "group_requests.json", group_requests)
                        st.rerun()
        
        elif menu == "Codes":
            st.header("🔑 Code Generation")
            # Already in Teachers tab
        
        elif menu == "Reports":
            st.header("📊 Reports")
            st.metric("Total Students", len([u for u in users if u['role']=='student']))
            st.metric("Total Teachers", len([u for u in users if u['role']=='teacher']))
        
        elif menu == "Settings":
            st.header("⚙️ Settings")
            with st.form("school_settings"):
                name = st.text_input("School Name", school['name'])
                motto = st.text_input("Motto", school.get('motto',''))
                city = st.text_input("City", school.get('city',''))
                state = st.text_input("State", school.get('state',''))
                if st.form_submit_button("Update"):
                    school['name'] = name
                    school['motto'] = motto
                    school['city'] = city
                    school['state'] = state
                    all_schools = load_all_schools()
                    all_schools[school_code] = school
                    save_all_schools(all_schools)
                    st.success("Updated")
                    st.rerun()
        
        elif menu == "Profile":
            st.header("👤 My Profile")
            col1,col2 = st.columns([1,2])
            with col1:
                if user.get('profile_pic'):
                    st.image(user['profile_pic'], width=150)
                else:
                    st.markdown("# 👑")
                pic = st.file_uploader("Upload Photo", type=['png','jpg','jpeg'])
                if pic:
                    img = Image.open(pic)
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")
                    b64 = base64.b64encode(buffered.getvalue()).decode()
                    for u in users:
                        if u['email'] == user['email']:
                            u['profile_pic'] = f"data:image/png;base64,{b64}"
                    save_school_data(school_code, "users.json", users)
                    user['profile_pic'] = f"data:image/png;base64,{b64}"
                    st.rerun()
            with col2:
                with st.form("profile_edit"):
                    name = st.text_input("Full Name", user['fullname'])
                    phone = st.text_input("Phone", user.get('phone',''))
                    bio = st.text_area("Bio", user.get('bio',''))
                    if st.form_submit_button("Update"):
                        for u in users:
                            if u['email'] == user['email']:
                                u['fullname'] = name
                                u['phone'] = phone
                                u['bio'] = bio
                        save_school_data(school_code, "users.json", users)
                        user.update({'fullname':name,'phone':phone,'bio':bio})
                        st.success("Profile updated")
                        st.rerun()
    
    # ----- TEACHER -----
    elif user['role'] == 'teacher':
        if menu == "Dashboard":
            st.header(f"👨‍🏫 {user['fullname']}")
            my_classes = [c for c in classes if c.get('teacher') == user['email']]
            my_groups = [g for g in groups if g.get('leader') == user['email']]
            col1,col2,col3 = st.columns(3)
            col1.metric("My Classes", len(my_classes))
            col2.metric("My Groups", len(my_groups))
            col3.metric("Assignments", len([a for a in assignments if a.get('teacher')==user['email']]))
        
        elif menu == "Announcements":
            st.header("📢 Post Announcement")
            with st.form("teacher_announce"):
                title = st.text_input("Title")
                content = st.text_area("Content")
                target = st.selectbox("Target Class", ["All"] + [c['name'] for c in classes if c.get('teacher')==user['email']])
                if st.form_submit_button("Post"):
                    announcements.append({
                        "id": generate_id("ANN"),
                        "title": title,
                        "content": content,
                        "author": user['fullname'],
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "target": target
                    })
                    save_school_data(school_code, "announcements.json", announcements)
                    st.success("Posted")
                    st.rerun()
        
        elif menu == "My Classes":
            st.header("📚 My Classes")
            my_classes = [c for c in classes if c.get('teacher') == user['email']]
            for c in my_classes:
                with st.expander(f"{c['name']} - {c['code']}"):
                    st.write(f"Room: {c.get('room','')} | Schedule: {c.get('schedule','')}")
                    st.write(f"Students: {len(c.get('students',[]))}")
        
        elif menu == "My Groups":
            st.header("👥 My Groups")
            my_groups = [g for g in groups if g.get('leader') == user['email']]
            for g in my_groups:
                with st.expander(f"{g['name']}"):
                    st.write(f"Members: {len(g['members'])}")
        
        elif menu == "Assignments":
            st.header("📝 Assignments")
            my_classes = [c['name'] for c in classes if c.get('teacher') == user['email']]
            with st.form("create_assignment"):
                class_name = st.selectbox("Class", my_classes)
                title = st.text_input("Title")
                desc = st.text_area("Description")
                due = st.date_input("Due Date")
                if st.form_submit_button("Create"):
                    code = generate_id("ASN")
                    assignments.append({
                        "code": code,
                        "class": class_name,
                        "teacher": user['email'],
                        "title": title,
                        "description": desc,
                        "due": due.strftime("%Y-%m-%d"),
                        "created": datetime.now().strftime("%Y-%m-%d")
                    })
                    save_school_data(school_code, "assignments.json", assignments)
                    st.success(f"Created: {code}")
                    st.rerun()
        
        elif menu == "Requests":
            st.header("✅ Approve Requests")
            my_classes = [c['name'] for c in classes if c.get('teacher') == user['email']]
            for req in [r for r in class_requests if r['status']=='pending' and r['class_name'] in my_classes]:
                col1,col2,col3 = st.columns(3)
                col1.write(req['student_name'])
                col2.write(req['class_name'])
                if col3.button("Approve", key=f"tc_{req['id']}"):
                    for c in classes:
                        if c['name'] == req['class_name']:
                            c['students'].append(req['student_email'])
                    req['status'] = 'approved'
                    save_school_data(school_code, "classes.json", classes)
                    save_school_data(school_code, "class_requests.json", class_requests)
                    st.rerun()
        
        elif menu == "Profile":
            st.header("👤 My Profile")
            # similar to admin profile, with teacher icon
            col1,col2 = st.columns([1,2])
            with col1:
                if user.get('profile_pic'):
                    st.image(user['profile_pic'], width=150)
                else:
                    st.markdown("# 👨‍🏫")
                pic = st.file_uploader("Upload Photo", type=['png','jpg','jpeg'], key="teacher_pic")
                if pic:
                    img = Image.open(pic)
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")
                    b64 = base64.b64encode(buffered.getvalue()).decode()
                    for u in users:
                        if u['email'] == user['email']:
                            u['profile_pic'] = f"data:image/png;base64,{b64}"
                    save_school_data(school_code, "users.json", users)
                    user['profile_pic'] = f"data:image/png;base64,{b64}"
                    st.rerun()
            with col2:
                with st.form("teacher_profile_edit"):
                    name = st.text_input("Full Name", user['fullname'])
                    phone = st.text_input("Phone", user.get('phone',''))
                    bio = st.text_area("Bio", user.get('bio',''))
                    if st.form_submit_button("Update"):
                        for u in users:
                            if u['email'] == user['email']:
                                u['fullname'] = name
                                u['phone'] = phone
                                u['bio'] = bio
                        save_school_data(school_code, "users.json", users)
                        user.update({'fullname':name,'phone':phone,'bio':bio})
                        st.success("Updated")
                        st.rerun()
    
    # ----- STUDENT -----
    else:
        if menu == "Dashboard":
            st.header(f"👨‍🎓 {user['fullname']}")
            my_classes = [c for c in classes if user['email'] in c.get('students',[])]
            my_groups = [g for g in groups if user['email'] in g.get('members',[])]
            col1,col2,col3 = st.columns(3)
            col1.metric("My Classes", len(my_classes))
            col2.metric("My Groups", len(my_groups))
            col3.metric("Assignments", len([a for a in assignments if a['class'] in [c['name'] for c in my_classes]]))
        
        elif menu == "Announcements":
            st.header("📢 Announcements")
            my_classes = [c['name'] for c in classes if user['email'] in c.get('students',[])]
            relevant = [a for a in announcements if a.get('target','All') in ['All']+my_classes]
            for a in relevant[-10:]:
                with st.container(border=True):
                    st.markdown(f"**{a['title']}**")
                    st.write(a['content'])
                    st.caption(a['date'])
        
        elif menu == "Browse Classes":
            st.header("📚 Available Classes")
            available = [c for c in classes if user['email'] not in c.get('students',[]) and len(c.get('students',[])) < c.get('max_students',30)]
            for c in available:
                with st.container(border=True):
                    col1,col2 = st.columns([3,1])
                    col1.markdown(f"**{c['name']}**")
                    col1.write(f"{c.get('teacher_name','')} • {c.get('schedule','')}")
                    if col2.button("Request", key=f"req_{c['code']}"):
                        class_requests.append({
                            "id": generate_id("REQ"),
                            "student_email": user['email'],
                            "student_name": user['fullname'],
                            "class_name": c['name'],
                            "class_code": c['code'],
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "status": "pending"
                        })
                        save_school_data(school_code, "class_requests.json", class_requests)
                        st.success("Request sent")
                        st.rerun()
        
        elif menu == "Browse Groups":
            st.header("👥 Available Groups")
            available = [g for g in groups if user['email'] not in g.get('members',[]) and len(g.get('members',[])) < g.get('max_members',10)]
            for g in available:
                with st.container(border=True):
                    col1,col2 = st.columns([3,1])
                    col1.markdown(f"**{g['name']}**")
                    col1.write(f"Leader: {g['leader_name']} • {g.get('class','General')}")
                    if col2.button("Join", key=f"reqg_{g['code']}"):
                        group_requests.append({
                            "id": generate_id("REQ"),
                            "student_email": user['email'],
                            "student_name": user['fullname'],
                            "group_name": g['name'],
                            "group_code": g['code'],
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "status": "pending"
                        })
                        save_school_data(school_code, "group_requests.json", group_requests)
                        st.success("Request sent")
                        st.rerun()
        
        elif menu == "Homework":
            st.header("📝 Homework")
            my_classes = [c['name'] for c in classes if user['email'] in c.get('students',[])]
            hw = [a for a in assignments if a.get('class') in my_classes]
            for a in hw:
                with st.container(border=True):
                    st.markdown(f"**{a['title']}**")
                    st.write(a.get('description',''))
                    st.caption(f"Due: {a['due']}")
        
        elif menu == "My Grades":
            st.header("📊 My Grades")
            my_grades = [g for g in grades if g.get('student') == user['email']]
            if my_grades:
                for g in my_grades:
                    st.write(f"{g.get('assignment_title','')}: {g['grade']}")
            else:
                st.info("No grades yet")
        
        elif menu == "Profile":
            st.header("👤 My Profile")
            col1,col2 = st.columns([1,2])
            with col1:
                if user.get('profile_pic'):
                    st.image(user['profile_pic'], width=150)
                else:
                    st.markdown("# 👨‍🎓")
                pic = st.file_uploader("Upload Photo", type=['png','jpg','jpeg'], key="student_pic")
                if pic:
                    img = Image.open(pic)
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")
                    b64 = base64.b64encode(buffered.getvalue()).decode()
                    for u in users:
                        if u['email'] == user['email']:
                            u['profile_pic'] = f"data:image/png;base64,{b64}"
                    save_school_data(school_code, "users.json", users)
                    user['profile_pic'] = f"data:image/png;base64,{b64}"
                    st.rerun()
            with col2:
                with st.form("student_profile_edit"):
                    name = st.text_input("Full Name", user['fullname'])
                    phone = st.text_input("Phone", user.get('phone',''))
                    bio = st.text_area("Bio", user.get('bio',''))
                    if st.form_submit_button("Update"):
                        for u in users:
                            if u['email'] == user['email']:
                                u['fullname'] = name
                                u['phone'] = phone
                                u['bio'] = bio
                        save_school_data(school_code, "users.json", users)
                        user.update({'fullname':name,'phone':phone,'bio':bio})
                        st.success("Updated")
                        st.rerun()

else:
    st.error("Something went wrong. Please restart.")
    if st.button("Restart"):
        st.session_state.page = 'welcome'
        st.rerun()
