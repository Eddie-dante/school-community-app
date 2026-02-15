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
    page_title="✨ School Community Hub ✨",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ CUSTOM CSS - SOLID BACKGROUND WITH MAXIMUM VISIBILITY ============
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* SOLID DARK BACKGROUND - NO TRANSPARENCY ISSUES */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        min-height: 100vh;
    }
    
    /* MAIN CONTENT AREA - SOLID BACKGROUND */
    .main > div {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        border: 2px solid gold;
    }
    
    /* ============ SIDEBAR - ULTRA VISIBLE ============ */
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #0f3460, #1a1a2e, #16213e) !important;
        border-right: 4px solid gold !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent !important;
        padding: 1.5rem 1rem !important;
    }
    
    /* ALL SIDEBAR TEXT - MAX VISIBILITY */
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stRadio label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] .st-emotion-cache-16idsys p,
    section[data-testid="stSidebar"] .st-emotion-cache-1dj0hjr,
    section[data-testid="stSidebar"] .st-emotion-cache-1v0mbdj {
        color: WHITE !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        text-shadow: 2px 2px 4px BLACK !important;
    }
    
    /* Sidebar radio buttons */
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
        background: rgba(255, 255, 255, 0.15) !important;
        border-radius: 15px !important;
        padding: 1rem !important;
        border: 2px solid gold !important;
    }
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        background: rgba(0, 0, 0, 0.5) !important;
        border-radius: 10px !important;
        padding: 12px !important;
        margin: 5px 0 !important;
        border: 1px solid gold !important;
        color: WHITE !important;
        font-weight: 600 !important;
    }
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
        background: rgba(255, 215, 0, 0.3) !important;
        border-color: white !important;
    }
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] {
        background: gold !important;
        color: BLACK !important;
        font-weight: 800 !important;
        border: 2px solid white !important;
    }
    
    /* Sidebar button */
    section[data-testid="stSidebar"] .stButton button {
        background: gold !important;
        color: BLACK !important;
        border: 2px solid white !important;
        border-radius: 10px !important;
        padding: 12px !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
    }
    
    /* School header */
    .school-header {
        background: rgba(0, 0, 0, 0.7);
        border: 3px solid gold;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .school-header h2 {
        color: WHITE !important;
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0;
    }
    
    .school-code {
        background: rgba(0, 0, 0, 0.8);
        padding: 10px;
        border-radius: 10px;
        margin-top: 10px;
        border: 2px solid gold;
    }
    
    .school-code code {
        color: gold !important;
        font-size: 1.2rem;
        font-weight: 700;
    }
    
    /* Profile card */
    .profile-card {
        background: rgba(0, 0, 0, 0.7);
        border: 3px solid gold;
        border-radius: 20px;
        padding: 15px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    /* ============ MAIN CONTENT - MAX VISIBILITY ============ */
    /* ALL TEXT WHITE WITH BLACK BACKGROUND */
    h1, h2, h3, h4, h5, h6,
    p, span, div, label,
    .stMarkdown, .stText, 
    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: WHITE !important;
        font-weight: 500 !important;
    }
    
    /* Headers extra bold */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        text-align: center;
        color: gold !important;
        text-shadow: 2px 2px 4px black;
    }
    
    h2 {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: gold !important;
    }
    
    h3 {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
    }
    
    /* FORM ELEMENTS - COMPLETELY VISIBLE */
    .stTextInput label, .stTextArea label, .stSelectbox label, .stDateInput label {
        color: WHITE !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stTextInput input, .stTextArea textarea, .stSelectbox div, .stDateInput input {
        background: rgba(0, 0, 0, 0.8) !important;
        border: 3px solid gold !important;
        border-radius: 10px !important;
        color: WHITE !important;
        font-weight: 500 !important;
        font-size: 1.1rem !important;
        padding: 0.8rem !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: white !important;
        box-shadow: 0 0 15px gold !important;
    }
    
    /* Placeholder text */
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: rgba(255, 255, 255, 0.7) !important;
        font-style: italic;
    }
    
    /* Buttons */
    .stButton button {
        background: gold !important;
        color: BLACK !important;
        border: 3px solid white !important;
        border-radius: 10px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 25px gold;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(0, 0, 0, 0.8) !important;
        border-radius: 10px !important;
        padding: 0.5rem !important;
        border: 2px solid gold !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: WHITE !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        padding: 0.8rem 2rem !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: gold !important;
        color: BLACK !important;
        font-weight: 800 !important;
        border-radius: 8px !important;
    }
    
    /* Metrics */
    .stMetric {
        background: rgba(0, 0, 0, 0.8) !important;
        border: 3px solid gold !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
    }
    
    .stMetric label {
        color: WHITE !important;
        font-size: 1.1rem !important;
    }
    
    .stMetric div {
        color: gold !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(0, 0, 0, 0.8) !important;
        border: 2px solid gold !important;
        border-radius: 10px !important;
        color: WHITE !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    
    /* Alerts */
    .stAlert {
        background: rgba(0, 0, 0, 0.9) !important;
        border-left: 6px solid !important;
        border-radius: 10px !important;
        color: WHITE !important;
        font-weight: 600 !important;
    }
    
    .stAlert-success {
        border-left-color: #00ff88 !important;
    }
    
    .stAlert-error {
        border-left-color: #ff4757 !important;
    }
    
    /* Dividers */
    hr {
        border: none !important;
        height: 3px !important;
        background: linear-gradient(90deg, transparent, gold, white, gold, transparent) !important;
        margin: 2rem 0 !important;
    }
    
    /* Code */
    code {
        background: rgba(0, 0, 0, 0.8) !important;
        color: gold !important;
        border: 2px solid gold !important;
        border-radius: 8px !important;
        padding: 0.2rem 0.5rem !important;
        font-weight: 700 !important;
    }
    
    /* Cards */
    .glass-card {
        background: rgba(0, 0, 0, 0.8) !important;
        border: 3px solid gold !important;
        border-radius: 20px !important;
        padding: 2rem !important;
    }
    
    .glass-card * {
        color: WHITE !important;
    }
    
    /* Title */
    .radiant-title {
        text-align: center;
        font-size: 4rem;
        font-weight: 900;
        color: gold !important;
        text-shadow: 4px 4px 8px black, 0 0 25px gold;
        margin-bottom: 0.5rem;
    }
    
    .radiant-subtitle {
        text-align: center;
        color: WHITE !important;
        font-size: 1.8rem;
        font-weight: 500;
        text-shadow: 2px 2px 4px black;
        margin-bottom: 2rem;
    }
    
    /* Hide footer */
    footer {
        display: none !important;
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
    st.markdown('<h1 class="radiant-title">✨ School Community Hub ✨</h1>', unsafe_allow_html=True)
    st.markdown('<p class="radiant-subtitle">Connect • Collaborate • Shine Together</p>', unsafe_allow_html=True)
    st.divider()
    
    tab1, tab2, tab3, tab4 = st.tabs(["👑 Admin", "🏫 Create", "👨‍🏫 Teachers", "👨‍🎓 Students"])
    
    # TAB 1: ADMIN LOGIN
    with tab1:
        col1, col2 = st.columns([1,1])
        with col1:
            st.subheader("🔐 Admin Login")
            with st.form("admin_login"):
                school = st.text_input("School Code", placeholder="Enter school code")
                email = st.text_input("Email", placeholder="admin@school.edu")
                pwd = st.text_input("Password", type="password", placeholder="••••••••")
                if st.form_submit_button("Login", use_container_width=True):
                    if not school or not email or not pwd:
                        st.error("All fields required")
                    else:
                        schools = load_all_schools()
                        if school in schools:
                            s = schools[school]
                            if s['admin_email'] == email:
                                users = load_school_data(school, "users.json", [])
                                hashed = hashlib.sha256(pwd.encode()).hexdigest()
                                for u in users:
                                    if u['email'] == email and u['password'] == hashed and u['role'] == 'admin':
                                        st.session_state.current_school = s
                                        st.session_state.user = u
                                        st.session_state.page = 'dashboard'
                                        st.rerun()
                                st.error("Wrong password")
                            else:
                                st.error("Not admin email")
                        else:
                            st.error("School not found")
        with col2:
            st.markdown("""
            <div style="background: rgba(0,0,0,0.8); border: 3px solid gold; border-radius: 20px; padding: 2rem; text-align: center;">
                <h3 style="color: gold;">👑 Admin Powers</h3>
                <p style="color: white;">Full control over your school</p>
                <h1 style="font-size: 5rem; color: gold;">✨</h1>
            </div>
            """, unsafe_allow_html=True)
    
    # TAB 2: CREATE SCHOOL
    with tab2:
        col1, col2 = st.columns([1,1])
        with col1:
            st.subheader("🚀 Create School")
            with st.form("create_school"):
                name = st.text_input("School Name", placeholder="e.g., Nqatho Sec Sch")
                admin = st.text_input("Your Full Name", placeholder="Wanjiku Edwin Guchu")
                email = st.text_input("Your Email", placeholder="you@school.edu")
                pwd = st.text_input("Password", type="password", placeholder="Create password")
                confirm = st.text_input("Confirm Password", type="password", placeholder="Confirm password")
                city = st.text_input("City", placeholder="Nairobi")
                state = st.text_input("State", placeholder="Nairobi")
                motto = st.text_input("Motto", placeholder="DTS")
                
                if st.form_submit_button("Create School", use_container_width=True):
                    if not name or not email or not pwd:
                        st.error("Required fields missing")
                    elif pwd != confirm:
                        st.error("Passwords don't match")
                    else:
                        schools = load_all_schools()
                        code = generate_school_code()
                        while code in schools:
                            code = generate_school_code()
                        
                        new = {
                            "code": code,
                            "name": name,
                            "city": city,
                            "state": state,
                            "motto": motto,
                            "created": datetime.now().strftime("%Y-%m-%d"),
                            "admin_email": email,
                            "admin_name": admin,
                            "stats": {"students":0, "teachers":0, "classes":0, "groups":0}
                        }
                        schools[code] = new
                        save_all_schools(schools)
                        
                        users = [{
                            "user_id": generate_id("USR"),
                            "email": email,
                            "fullname": admin,
                            "password": hashlib.sha256(pwd.encode()).hexdigest(),
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
                        
                        st.session_state.current_school = new
                        st.session_state.user = users[0]
                        st.session_state.page = 'dashboard'
                        st.success(f"School created! Code: {code}")
                        st.rerun()
        with col2:
            st.markdown("""
            <div style="background: rgba(0,0,0,0.8); border: 3px solid gold; border-radius: 20px; padding: 2rem; text-align: center;">
                <h3 style="color: gold;">🎓 Begin Your Legacy</h3>
                <p style="color: white;">Start your own school community</p>
                <h1 style="font-size: 5rem; color: gold;">🚀</h1>
            </div>
            """, unsafe_allow_html=True)
    
    # TAB 3: TEACHER
    with tab3:
        subtab1, subtab2 = st.tabs(["Login", "Register"])
        
        with subtab1:
            col1, col2 = st.columns([1,1])
            with col1:
                st.subheader("👨‍🏫 Teacher Login")
                with st.form("teacher_login"):
                    school = st.text_input("School Code")
                    email = st.text_input("Email")
                    pwd = st.text_input("Password", type="password")
                    if st.form_submit_button("Login", use_container_width=True):
                        if not school or not email or not pwd:
                            st.error("All fields required")
                        else:
                            schools = load_all_schools()
                            if school in schools:
                                s = schools[school]
                                users = load_school_data(school, "users.json", [])
                                hashed = hashlib.sha256(pwd.encode()).hexdigest()
                                for u in users:
                                    if u['email'] == email and u['password'] == hashed and u['role'] == 'teacher':
                                        st.session_state.current_school = s
                                        st.session_state.user = u
                                        st.session_state.page = 'dashboard'
                                        st.rerun()
                                st.error("Invalid credentials")
                            else:
                                st.error("School not found")
            with col2:
                st.markdown("""
                <div style="background: rgba(0,0,0,0.8); border: 3px solid gold; border-radius: 20px; padding: 2rem; text-align: center;">
                    <h3 style="color: gold;">📚 Your Classroom</h3>
                    <p style="color: white;">Login to manage classes</p>
                    <h1 style="font-size: 5rem; color: gold;">🍎</h1>
                </div>
                """, unsafe_allow_html=True)
        
        with subtab2:
            col1, col2 = st.columns([1,1])
            with col1:
                st.subheader("📝 New Teacher")
                with st.form("teacher_register"):
                    school = st.text_input("School Code", key="reg_school")
                    teacher_code = st.text_input("Teacher Code", placeholder="e.g., MATH-DEPT")
                    name = st.text_input("Full Name")
                    email = st.text_input("Email", key="reg_email")
                    pwd = st.text_input("Password", type="password", key="reg_pass")
                    confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
                    
                    if st.form_submit_button("Register", use_container_width=True):
                        if not all([school, teacher_code, name, email, pwd]):
                            st.error("All fields required")
                        elif pwd != confirm:
                            st.error("Passwords don't match")
                        else:
                            schools = load_all_schools()
                            if school in schools:
                                s = schools[school]
                                teachers = load_school_data(school, "teachers.json", [])
                                valid = False
                                record = None
                                for t in teachers:
                                    if t['code'] == teacher_code.upper() and t['status'] == 'active':
                                        valid = True
                                        record = t
                                        t.setdefault('used_by_list', []).append({
                                            "email": email,
                                            "name": name,
                                            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                                        })
                                        t['last_used'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                                        t['last_used_by'] = email
                                        break
                                if not valid:
                                    st.error("Invalid teacher code")
                                    st.stop()
                                
                                users = load_school_data(school, "users.json", [])
                                if any(u['email'] == email for u in users):
                                    st.error("Email already exists")
                                    st.stop()
                                
                                new_user = {
                                    "user_id": generate_id("USR"),
                                    "email": email,
                                    "fullname": name,
                                    "password": hashlib.sha256(pwd.encode()).hexdigest(),
                                    "role": "teacher",
                                    "joined": datetime.now().strftime("%Y-%m-%d"),
                                    "school_code": school,
                                    "teacher_code_used": teacher_code.upper(),
                                    "classes": [],
                                    "groups": []
                                }
                                users.append(new_user)
                                save_school_data(school, "users.json", users)
                                save_school_data(school, "teachers.json", teachers)
                                s['stats']['teachers'] += 1
                                schools[school] = s
                                save_all_schools(schools)
                                
                                st.session_state.current_school = s
                                st.session_state.user = new_user
                                st.session_state.page = 'dashboard'
                                st.success("Registration successful!")
                                st.rerun()
                            else:
                                st.error("School not found")
            with col2:
                st.markdown("""
                <div style="background: rgba(0,0,0,0.8); border: 3px solid gold; border-radius: 20px; padding: 2rem; text-align: center;">
                    <h3 style="color: gold;">✨ Join as Teacher</h3>
                    <p style="color: white;">Use your teacher code</p>
                    <h1 style="font-size: 5rem; color: gold;">📝</h1>
                </div>
                """, unsafe_allow_html=True)
    
    # TAB 4: STUDENT
    with tab4:
        subtab1, subtab2 = st.tabs(["Login", "Register"])
        
        with subtab1:
            col1, col2 = st.columns([1,1])
            with col1:
                st.subheader("👨‍🎓 Student Login")
                with st.form("student_login"):
                    school = st.text_input("School Code")
                    email = st.text_input("Email")
                    pwd = st.text_input("Password", type="password")
                    if st.form_submit_button("Login", use_container_width=True):
                        if not school or not email or not pwd:
                            st.error("All fields required")
                        else:
                            schools = load_all_schools()
                            if school in schools:
                                s = schools[school]
                                users = load_school_data(school, "users.json", [])
                                hashed = hashlib.sha256(pwd.encode()).hexdigest()
                                for u in users:
                                    if u['email'] == email and u['password'] == hashed and u['role'] == 'student':
                                        st.session_state.current_school = s
                                        st.session_state.user = u
                                        st.session_state.page = 'dashboard'
                                        st.rerun()
                                st.error("Invalid credentials")
                            else:
                                st.error("School not found")
            with col2:
                st.markdown("""
                <div style="background: rgba(0,0,0,0.8); border: 3px solid gold; border-radius: 20px; padding: 2rem; text-align: center;">
                    <h3 style="color: gold;">📖 Your Learning Hub</h3>
                    <p style="color: white;">Access classes and homework</p>
                    <h1 style="font-size: 5rem; color: gold;">📚</h1>
                </div>
                """, unsafe_allow_html=True)
        
        with subtab2:
            col1, col2 = st.columns([1,1])
            with col1:
                st.subheader("🆕 New Student")
                with st.form("student_register"):
                    school = st.text_input("School Code", key="stud_school")
                    name = st.text_input("Full Name")
                    email = st.text_input("Email", key="stud_email")
                    pwd = st.text_input("Password", type="password", key="stud_pass")
                    confirm = st.text_input("Confirm Password", type="password", key="stud_confirm")
                    
                    if st.form_submit_button("Register", use_container_width=True):
                        if not all([school, name, email, pwd]):
                            st.error("All fields required")
                        elif pwd != confirm:
                            st.error("Passwords don't match")
                        else:
                            schools = load_all_schools()
                            if school in schools:
                                s = schools[school]
                                users = load_school_data(school, "users.json", [])
                                if any(u['email'] == email for u in users):
                                    st.error("Email already exists")
                                else:
                                    new_user = {
                                        "user_id": generate_id("USR"),
                                        "email": email,
                                        "fullname": name,
                                        "password": hashlib.sha256(pwd.encode()).hexdigest(),
                                        "role": "student",
                                        "joined": datetime.now().strftime("%Y-%m-%d"),
                                        "school_code": school,
                                        "classes": [],
                                        "groups": []
                                    }
                                    users.append(new_user)
                                    save_school_data(school, "users.json", users)
                                    s['stats']['students'] += 1
                                    schools[school] = s
                                    save_all_schools(schools)
                                    
                                    st.session_state.current_school = s
                                    st.session_state.user = new_user
                                    st.session_state.page = 'dashboard'
                                    st.success("Registration successful!")
                                    st.rerun()
                            else:
                                st.error("School not found")
            with col2:
                st.markdown("""
                <div style="background: rgba(0,0,0,0.8); border: 3px solid gold; border-radius: 20px; padding: 2rem; text-align: center;">
                    <h3 style="color: gold;">🎓 Begin Your Journey</h3>
                    <p style="color: white;">Join your school community</p>
                    <h1 style="font-size: 5rem; color: gold;">🌟</h1>
                </div>
                """, unsafe_allow_html=True)

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
    
    # SIDEBAR
    with st.sidebar:
        st.markdown(f"""
        <div class="school-header">
            <h2>{school['name']}</h2>
            <p style="color: white;">✨ {school.get('motto','')} ✨</p>
            <div class="school-code">
                <code>{school['code']}</code>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        if user.get('profile_pic'):
            st.image(user['profile_pic'], width=70)
        else:
            emoji = "👑" if user['role'] == 'admin' else "👨‍🏫" if user['role'] == 'teacher' else "👨‍🎓"
            st.markdown(f"<h1 style='font-size: 3rem; margin: 0;'>{emoji}</h1>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="color: white;">
            <strong>{user['fullname']}</strong><br>
            <span style="background: gold; color: black; padding: 2px 8px; border-radius: 10px;">{user['role'].upper()}</span><br>
            <small>{user['email']}</small>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        
        # Navigation
        if user['role'] == 'admin':
            options = ["Dashboard", "Teachers", "Classes", "Students", "Groups", "Approvals", "Profile"]
        elif user['role'] == 'teacher':
            options = ["Dashboard", "My Classes", "My Groups", "Assignments", "Requests", "Profile"]
        else:
            options = ["Dashboard", "Browse Classes", "Browse Groups", "Homework", "My Grades", "Profile"]
        
        menu = st.radio("Menu", options, index=st.session_state.menu_index)
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.current_school = None
            st.session_state.page = 'welcome'
            st.rerun()
    
    # MAIN CONTENT - Simplified for visibility
    st.markdown(f"<h1>Welcome, {user['fullname']}!</h1>", unsafe_allow_html=True)
    
    if user['role'] == 'admin' and menu == "Dashboard":
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Students", school['stats'].get('students',0))
        col2.metric("Teachers", school['stats'].get('teachers',0))
        col3.metric("Classes", school['stats'].get('classes',0))
        col4.metric("Groups", school['stats'].get('groups',0))
        
        pending = len([r for r in class_requests if r['status']=='pending']) + len([r for r in group_requests if r['status']=='pending'])
        if pending:
            st.warning(f"{pending} pending requests")

else:
    st.error("Something went wrong")
    if st.button("Restart"):
        st.session_state.page = 'welcome'
        st.rerun()
