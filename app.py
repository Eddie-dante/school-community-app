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

# ============ CUSTOM CSS - STUNNING BACKGROUND IMAGES & VISIBLE SIDEBAR ============
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main container with background image */
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1523050854058-8df90110c9f1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
        min-height: 100vh;
    }
    
    /* Overlay to make content readable */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.6);
        z-index: -1;
    }
    
    /* Main content area */
    .main > div {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 30px;
        padding: 2rem;
        margin: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* SIDEBAR - COMPLETELY VISIBLE AND STUNNING */
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.05)) !important;
        backdrop-filter: blur(15px) !important;
        border-right: 2px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 10px 0 30px rgba(0, 0, 0, 0.3) !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent !important;
    }
    
    /* Sidebar content */
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stRadio label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5) !important;
    }
    
    /* Sidebar radio buttons - beautiful cards */
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(5px) !important;
        border-radius: 20px !important;
        padding: 1rem !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        padding: 12px 15px !important;
        margin: 5px 0 !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        transition: all 0.3s ease !important;
        color: white !important;
        font-weight: 500 !important;
    }
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.3) !important;
        transform: translateX(5px) !important;
        border-color: rgba(255, 255, 255, 0.8) !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3) !important;
    }
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        border: 2px solid gold !important;
        box-shadow: 0 0 20px gold !important;
    }
    
    /* Sidebar buttons */
    section[data-testid="stSidebar"] .stButton button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.5) !important;
        border-radius: 50px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    section[data-testid="stSidebar"] .stButton button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 8px 25px gold !important;
        border-color: gold !important;
    }
    
    /* School header in sidebar */
    .school-header {
        background: linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.05));
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255,255,255,0.3);
        border-radius: 30px;
        padding: 20px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        animation: glow 3s infinite;
    }
    
    @keyframes glow {
        0%, 100% { border-color: rgba(255,255,255,0.3); }
        50% { border-color: gold; box-shadow: 0 0 30px gold; }
    }
    
    .school-header h2 {
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin: 0;
    }
    
    .school-code {
        background: rgba(0,0,0,0.3);
        padding: 8px;
        border-radius: 50px;
        margin-top: 10px;
        font-size: 1.2rem;
        font-weight: bold;
        color: gold;
        border: 1px solid gold;
    }
    
    /* User profile card */
    .profile-card {
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(5px);
        border-radius: 20px;
        padding: 15px;
        border: 1px solid rgba(255,255,255,0.3);
        margin-bottom: 20px;
    }
    
    /* Glass cards for main content */
    .glass-card {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 30px !important;
        padding: 1.5rem !important;
        color: white !important;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37) !important;
        transition: all 0.3s ease !important;
    }
    
    .glass-card:hover {
        transform: translateY(-5px) !important;
        border-color: gold !important;
        box-shadow: 0 12px 48px gold !important;
    }
    
    /* Headers with glow */
    h1, h2, h3 {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5), 0 0 20px rgba(255,215,0,0.5) !important;
        font-weight: 600 !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 50px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
    }
    
    .stButton button:hover {
        transform: scale(1.05) !important;
        border-color: gold !important;
        box-shadow: 0 8px 25px gold !important;
    }
    
    /* Text inputs */
    .stTextInput input, .stTextArea textarea, .stSelectbox div, .stDateInput input {
        background: rgba(255, 255, 255, 0.15) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 20px !important;
        color: white !important;
        padding: 0.75rem !important;
        backdrop-filter: blur(5px) !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: gold !important;
        box-shadow: 0 0 20px gold !important;
    }
    
    /* Labels */
    .stTextInput label, .stTextArea label, .stSelectbox label {
        color: white !important;
        font-weight: 500 !important;
        text-shadow: 1px 1px 2px black !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 50px !important;
        padding: 0.5rem !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: white !important;
        border-radius: 50px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 500 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        border: 2px solid gold !important;
    }
    
    /* Metrics */
    .stMetric {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 30px !important;
        padding: 1.5rem !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        color: white !important;
    }
    
    .stMetric label {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    .stMetric div {
        color: gold !important;
        text-shadow: 0 0 10px gold !important;
    }
    
    /* Success/Warning/Error messages */
    .stAlert {
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 20px !important;
        color: white !important;
        border-left: 5px solid !important;
    }
    
    .stAlert-success {
        border-left-color: #00ff88 !important;
    }
    
    .stAlert-error {
        border-left-color: #ff4757 !important;
    }
    
    .stAlert-warning {
        border-left-color: #ffa502 !important;
    }
    
    .stAlert-info {
        border-left-color: #00d2ff !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(5px) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        color: white !important;
    }
    
    /* Code blocks */
    code {
        background: rgba(0, 0, 0, 0.3) !important;
        color: gold !important;
        border-radius: 10px !important;
        padding: 0.2rem 0.5rem !important;
    }
    
    /* Hide footer */
    footer {
        display: none !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        background: rgba(255,255,255,0.1);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    /* Animated title */
    .radiant-title {
        text-align: center;
        font-size: 4rem;
        font-weight: 700;
        background: linear-gradient(90deg, gold, #ff6b6b, #667eea, #00ff88);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: title-pulse 3s infinite;
        text-shadow: 0 0 30px rgba(255,215,0,0.5);
    }
    
    @keyframes title-pulse {
        0%, 100% { filter: drop-shadow(0 0 20px gold); }
        50% { filter: drop-shadow(0 0 40px #667eea); }
    }
    
    /* Subtitle */
    .radiant-subtitle {
        text-align: center;
        color: white;
        font-size: 1.5rem;
        font-weight: 300;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        animation: fade-in 2s;
    }
    
    @keyframes fade-in {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
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
    # Animated Title
    st.markdown('<h1 class="radiant-title">✨ School Community Hub ✨</h1>', unsafe_allow_html=True)
    st.markdown('<p class="radiant-subtitle">Connect • Collaborate • Shine Together</p>', unsafe_allow_html=True)
    st.divider()
    
    # Beautiful Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["👑 **Admin Portal**", "🏫 **Create School**", "👨‍🏫 **Teacher Space**", "👨‍🎓 **Student World**"])
    
    # ---------- TAB 1: ADMIN LOGIN ----------
    with tab1:
        col1, col2 = st.columns([1,1])
        with col1:
            with st.form("admin_login", clear_on_submit=True):
                st.subheader("🌟 Welcome Back, Admin")
                school_code = st.text_input("🏫 School Code", placeholder="Enter your school code")
                email = st.text_input("📧 Email", placeholder="admin@school.edu")
                password = st.text_input("🔐 Password", type="password", placeholder="••••••••")
                if st.form_submit_button("✨ LOGIN ✨", use_container_width=True):
                    if not school_code or not email or not password:
                        st.error("Please fill all fields")
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
            st.markdown("""
            <div class="glass-card" style="text-align: center;">
                <h3 style="color: white;">👑 Admin Powers</h3>
                <p style="color: white; opacity: 0.9;">Full control over your school community</p>
                <div style="font-size: 5rem;">✨</div>
            </div>
            """, unsafe_allow_html=True)
    
    # ---------- TAB 2: CREATE SCHOOL ----------
    with tab2:
        col1, col2 = st.columns([1,1])
        with col1:
            with st.form("create_school", clear_on_submit=True):
                st.subheader("🚀 Start Your Journey")
                school_name = st.text_input("🏫 School Name", placeholder="e.g., Nqatho Sec Sch")
                admin_name = st.text_input("👤 Your Full Name", placeholder="e.g., Wanjiku Edwin Guchu")
                admin_email = st.text_input("📧 Your Email", placeholder="you@school.edu")
                password = st.text_input("🔐 Password", type="password", placeholder="Create password")
                confirm = st.text_input("🔐 Confirm Password", type="password", placeholder="Confirm password")
                city = st.text_input("🏙️ City", placeholder="Nairobi")
                state = st.text_input("🗺️ State/Province", placeholder="Nairobi")
                motto = st.text_input("✨ School Motto", placeholder="e.g., DTS")
                
                if st.form_submit_button("🌟 CREATE SCHOOL 🌟", use_container_width=True):
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
                        st.success(f"✨ School Created! Your Code: **{code}**")
                        st.rerun()
        with col2:
            st.markdown("""
            <div class="glass-card" style="text-align: center;">
                <h3 style="color: white;">🎓 Begin Your Legacy</h3>
                <p style="color: white; opacity: 0.9;">Create your school and become the founding administrator</p>
                <div style="font-size: 5rem;">🚀</div>
            </div>
            """, unsafe_allow_html=True)
    
    # ---------- TAB 3: TEACHER LOGIN & REGISTER ----------
    with tab3:
        subtab1, subtab2 = st.tabs(["🔐 **Teacher Login**", "📝 **New Teacher**"])
        
        with subtab1:
            col1, col2 = st.columns([1,1])
            with col1:
                with st.form("teacher_login", clear_on_submit=True):
                    st.subheader("👨‍🏫 Welcome Back")
                    school_code = st.text_input("🏫 School Code", placeholder="Enter school code")
                    email = st.text_input("📧 Email", placeholder="teacher@school.edu")
                    password = st.text_input("🔐 Password", type="password", placeholder="••••••••")
                    if st.form_submit_button("✨ LOGIN ✨", use_container_width=True):
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
                st.markdown("""
                <div class="glass-card" style="text-align: center;">
                    <h3 style="color: white;">📚 Your Classroom Awaits</h3>
                    <p style="color: white; opacity: 0.9;">Login to manage classes and inspire students</p>
                    <div style="font-size: 5rem;">🍎</div>
                </div>
                """, unsafe_allow_html=True)
        
        with subtab2:
            col1, col2 = st.columns([1,1])
            with col1:
                with st.form("teacher_register", clear_on_submit=True):
                    st.subheader("🌟 Join as Teacher")
                    school_code = st.text_input("🏫 School Code", placeholder="Enter school code", key="reg_school")
                    teacher_code = st.text_input("🔑 Teacher Code", placeholder="e.g., MATH-DEPT, MR-JOHNSON")
                    fullname = st.text_input("👤 Full Name", placeholder="Your full name")
                    email = st.text_input("📧 Email", placeholder="teacher@school.edu", key="reg_email")
                    password = st.text_input("🔐 Password", type="password", placeholder="Create password", key="reg_pass")
                    confirm = st.text_input("🔐 Confirm Password", type="password", placeholder="Confirm password", key="reg_confirm")
                    
                    if st.form_submit_button("🌟 REGISTER NOW 🌟", use_container_width=True):
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
                                st.success("✨ Registration Successful!")
                                st.rerun()
            with col2:
                st.markdown("""
                <div class="glass-card" style="text-align: center;">
                    <h3 style="color: white;">🎯 Start Your Journey</h3>
                    <p style="color: white; opacity: 0.9;">Use your teacher code to join your school community</p>
                    <div style="font-size: 5rem;">✨</div>
                </div>
                """, unsafe_allow_html=True)
    
    # ---------- TAB 4: STUDENT LOGIN & REGISTER ----------
    with tab4:
        subtab1, subtab2 = st.tabs(["🔐 **Student Login**", "📝 **New Student**"])
        
        with subtab1:
            col1, col2 = st.columns([1,1])
            with col1:
                with st.form("student_login", clear_on_submit=True):
                    st.subheader("👨‍🎓 Welcome Back")
                    school_code = st.text_input("🏫 School Code", placeholder="Enter school code")
                    email = st.text_input("📧 Email", placeholder="student@school.edu")
                    password = st.text_input("🔐 Password", type="password", placeholder="••••••••")
                    if st.form_submit_button("✨ LOGIN ✨", use_container_width=True):
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
                st.markdown("""
                <div class="glass-card" style="text-align: center;">
                    <h3 style="color: white;">📚 Your Learning Hub</h3>
                    <p style="color: white; opacity: 0.9;">Access classes, homework, and connect with peers</p>
                    <div style="font-size: 5rem;">📖</div>
                </div>
                """, unsafe_allow_html=True)
        
        with subtab2:
            col1, col2 = st.columns([1,1])
            with col1:
                with st.form("student_register", clear_on_submit=True):
                    st.subheader("🌟 Join as Student")
                    school_code = st.text_input("🏫 School Code", placeholder="Enter school code", key="stud_reg_school")
                    fullname = st.text_input("👤 Full Name", placeholder="Your full name")
                    email = st.text_input("📧 Email", placeholder="student@school.edu", key="stud_reg_email")
                    password = st.text_input("🔐 Password", type="password", placeholder="Create password", key="stud_reg_pass")
                    confirm = st.text_input("🔐 Confirm Password", type="password", placeholder="Confirm password", key="stud_reg_confirm")
                    
                    if st.form_submit_button("🌟 REGISTER NOW 🌟", use_container_width=True):
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
                                    st.success("✨ Registration Successful!")
                                    st.rerun()
            with col2:
                st.markdown("""
                <div class="glass-card" style="text-align: center;">
                    <h3 style="color: white;">🎓 Begin Your Adventure</h3>
                    <p style="color: white; opacity: 0.9;">Join your school and start your learning journey</p>
                    <div style="font-size: 5rem;">🚀</div>
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
    
    # ============ SIDEBAR ============
    with st.sidebar:
        # School Header with Glow
        st.markdown(f"""
        <div class="school-header">
            <h2>{school['name']}</h2>
            <p style="color: rgba(255,255,255,0.9); font-style: italic; margin: 5px 0;">✨ {school.get('motto','')} ✨</p>
            <div class="school-code">
                <code style="background: transparent; color: gold; font-size: 1.1rem;">{school['code']}</code>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # User Profile Card
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        col1, col2 = st.columns([1,2])
        with col1:
            if user.get('profile_pic'):
                st.image(user['profile_pic'], width=70)
            else:
                emoji = "👑" if user['role'] == 'admin' else "👨‍🏫" if user['role'] == 'teacher' else "👨‍🎓"
                st.markdown(f"<h1 style='font-size: 4rem; text-align: center; margin: 0;'>{emoji}</h1>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="color: white;">
                <strong style="font-size: 1.2rem;">{user['fullname']}</strong><br>
                <span style="background: rgba(255,255,255,0.2); padding: 3px 10px; border-radius: 50px; font-size: 0.8rem;">{user['role'].upper()}</span><br>
                <span style="font-size: 0.8rem; opacity: 0.8;">{user['email']}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        
        # Navigation Menu
        if user['role'] == 'admin':
            menu_options = ["Dashboard", "Announcements", "Teachers", "Classes", "Students", "Groups", "Approvals", "Codes", "Reports", "Settings", "Profile"]
            icons = ["👑", "📢", "👨‍🏫", "📚", "👨‍🎓", "👥", "✅", "🔑", "📊", "⚙️", "👤"]
        elif user['role'] == 'teacher':
            menu_options = ["Dashboard", "Announcements", "My Classes", "My Groups", "Assignments", "Requests", "Resources", "Discussions", "Gradebook", "Profile"]
            icons = ["👨‍🏫", "📢", "📚", "👥", "📝", "✅", "📎", "💬", "📊", "👤"]
        else:
            menu_options = ["Dashboard", "Announcements", "Browse Classes", "Browse Groups", "Homework", "Study Materials", "Discussions", "My Grades", "Profile"]
            icons = ["👨‍🎓", "📢", "📚", "👥", "📝", "📎", "💬", "📊", "👤"]
        
        # Create styled radio with icons
        menu_html = ""
        for i, (opt, icon) in enumerate(zip(menu_options, icons)):
            selected_class = "selected" if i == st.session_state.menu_index else ""
            menu_html += f"""
            <div style="margin: 8px 0; padding: 12px 15px; border-radius: 15px; 
                        background: {'linear-gradient(135deg, #667eea, #764ba2)' if i==st.session_state.menu_index else 'rgba(255,255,255,0.1)'};
                        border: 2px solid {'gold' if i==st.session_state.menu_index else 'rgba(255,255,255,0.2)'};
                        box-shadow: {'0 0 20px gold' if i==st.session_state.menu_index else 'none'};
                        transition: all 0.3s; cursor: pointer;"
                 onclick="document.querySelectorAll('.stRadio input[type=radio]')[{i}].click();">
                <span style="font-size: 1.3rem; margin-right: 12px;">{icon}</span>
                <span style="color: white; font-weight: {600 if i==st.session_state.menu_index else 400};">{opt}</span>
            </div>
            """
        st.markdown(menu_html, unsafe_allow_html=True)
        
        # Hidden radio for functionality
        menu = st.radio("", menu_options, label_visibility="collapsed", index=st.session_state.menu_index)
        
        st.divider()
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.current_school = None
            st.session_state.page = 'welcome'
            st.rerun()
    
    # ============ MAIN CONTENT ============
    with st.container():
        st.markdown('<div class="main-content">', unsafe_allow_html=True)
        
        # ----- ADMIN -----
        if user['role'] == 'admin':
            if menu == "Dashboard":
                st.markdown(f"<h1 style='color: white; text-align: center;'>👑 {school['name']} Dashboard</h1>", unsafe_allow_html=True)
                
                col1,col2,col3,col4 = st.columns(4)
                with col1:
                    st.metric("Students", school['stats'].get('students',0))
                with col2:
                    st.metric("Teachers", school['stats'].get('teachers',0))
                with col3:
                    st.metric("Classes", school['stats'].get('classes',0))
                with col4:
                    st.metric("Groups", school['stats'].get('groups',0))
                
                st.divider()
                
                pending = len([r for r in class_requests if r['status']=='pending']) + \
                         len([r for r in group_requests if r['status']=='pending'])
                if pending:
                    st.warning(f"✨ {pending} pending requests await your approval")
                else:
                    st.success("🌟 All caught up! No pending requests")
            
            elif menu == "Teachers":
                st.markdown("<h1 style='color: white; text-align: center;'>👨‍🏫 Teacher Management</h1>", unsafe_allow_html=True)
                tab1, tab2 = st.tabs(["✨ Create Teacher Codes", "👥 Active Teachers"])
                
                with tab1:
                    with st.form("create_teacher_code"):
                        name = st.text_input("📝 Code Name", placeholder="e.g., Mathematics Department")
                        code = st.text_input("🔑 Custom Code", placeholder="e.g., MATH-DEPT, FORM1-2024")
                        dept = st.selectbox("🏢 Department", ["Mathematics","Science","English","History","Computer Science","Other"])
                        if st.form_submit_button("✨ Create Magical Code ✨", use_container_width=True):
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
                                    st.success(f"✨ Code {code.upper()} created!")
                                    st.rerun()
                
                with tab2:
                    for t in teachers_data:
                        with st.container():
                            col1, col2 = st.columns([3,1])
                            with col1:
                                st.markdown(f"**{t['name']}**")
                                st.caption(f"Code: `{t['code']}`")
                            with col2:
                                st.markdown(f"**{len(t.get('used_by_list',[]))}** teachers")
            
            elif menu == "Approvals":
                st.markdown("<h1 style='color: white; text-align: center;'>✅ Admin Veto Power</h1>", unsafe_allow_html=True)
                tab1, tab2 = st.tabs(["📚 Class Requests", "👥 Group Requests"])
                
                with tab1:
                    for req in [r for r in class_requests if r['status']=='pending']:
                        with st.container():
                            col1,col2,col3 = st.columns([2,2,2])
                            col1.markdown(f"**{req['student_name']}**")
                            col2.markdown(f"*{req['class_name']}*")
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
                        with st.container():
                            col1,col2,col3 = st.columns([2,2,2])
                            col1.markdown(f"**{req['student_name']}**")
                            col2.markdown(f"*{req['group_name']}*")
                            if col3.button("✅ Approve", key=f"app_g_{req['id']}"):
                                for g in groups:
                                    if g['name'] == req['group_name']:
                                        g['members'].append(req['student_email'])
                                req['status'] = 'approved'
                                req['approved_by'] = user['email'] + " (Veto)"
                                save_school_data(school_code, "groups.json", groups)
                                save_school_data(school_code, "group_requests.json", group_requests)
                                st.rerun()
            
            elif menu == "Profile":
                st.markdown("<h1 style='color: white; text-align: center;'>👤 My Profile</h1>", unsafe_allow_html=True)
                col1,col2 = st.columns([1,2])
                with col1:
                    if user.get('profile_pic'):
                        st.image(user['profile_pic'], width=200)
                    else:
                        st.markdown("<h1 style='font-size: 8rem; text-align: center;'>👑</h1>", unsafe_allow_html=True)
                    pic = st.file_uploader("✨ Upload Photo", type=['png','jpg','jpeg'])
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
                        if st.form_submit_button("✨ Update Profile ✨", use_container_width=True):
                            for u in users:
                                if u['email'] == user['email']:
                                    u['fullname'] = name
                                    u['phone'] = phone
                                    u['bio'] = bio
                            save_school_data(school_code, "users.json", users)
                            user.update({'fullname':name,'phone':phone,'bio':bio})
                            st.success("Profile updated!")
                            st.rerun()
        
        # ----- TEACHER -----
        elif user['role'] == 'teacher':
            if menu == "Dashboard":
                st.markdown(f"<h1 style='color: white; text-align: center;'>👨‍🏫 Welcome, {user['fullname']}!</h1>", unsafe_allow_html=True)
                my_classes = [c for c in classes if c.get('teacher') == user['email']]
                my_groups = [g for g in groups if g.get('leader') == user['email']]
                
                col1,col2,col3 = st.columns(3)
                col1.metric("My Classes", len(my_classes))
                col2.metric("My Groups", len(my_groups))
                col3.metric("Assignments", len([a for a in assignments if a.get('teacher')==user['email']]))
            
            elif menu == "Profile":
                st.markdown("<h1 style='color: white; text-align: center;'>👤 My Profile</h1>", unsafe_allow_html=True)
                col1,col2 = st.columns([1,2])
                with col1:
                    if user.get('profile_pic'):
                        st.image(user['profile_pic'], width=200)
                    else:
                        st.markdown("<h1 style='font-size: 8rem; text-align: center;'>👨‍🏫</h1>", unsafe_allow_html=True)
                    pic = st.file_uploader("✨ Upload Photo", type=['png','jpg','jpeg'], key="teacher_pic")
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
                        if st.form_submit_button("✨ Update Profile ✨", use_container_width=True):
                            for u in users:
                                if u['email'] == user['email']:
                                    u['fullname'] = name
                                    u['phone'] = phone
                                    u['bio'] = bio
                            save_school_data(school_code, "users.json", users)
                            user.update({'fullname':name,'phone':phone,'bio':bio})
                            st.success("Profile updated!")
                            st.rerun()
        
        # ----- STUDENT -----
        else:
            if menu == "Dashboard":
                st.markdown(f"<h1 style='color: white; text-align: center;'>👨‍🎓 Welcome, {user['fullname']}!</h1>", unsafe_allow_html=True)
                my_classes = [c for c in classes if user['email'] in c.get('students',[])]
                my_groups = [g for g in groups if user['email'] in g.get('members',[])]
                
                col1,col2,col3 = st.columns(3)
                col1.metric("My Classes", len(my_classes))
                col2.metric("My Groups", len(my_groups))
                col3.metric("Assignments", len([a for a in assignments if a['class'] in [c['name'] for c in my_classes]]))
            
            elif menu == "Browse Classes":
                st.markdown("<h1 style='color: white; text-align: center;'>📚 Available Classes</h1>", unsafe_allow_html=True)
                available = [c for c in classes if user['email'] not in c.get('students',[]) and len(c.get('students',[])) < c.get('max_students',30)]
                for c in available:
                    with st.container():
                        col1,col2 = st.columns([3,1])
                        col1.markdown(f"**{c['name']}**")
                        col1.write(f"👨‍🏫 {c.get('teacher_name','')} • {c.get('schedule','')}")
                        if col2.button("✨ Request", key=f"req_{c['code']}"):
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
                            st.success("Request sent!")
                            st.rerun()
            
            elif menu == "Profile":
                st.markdown("<h1 style='color: white; text-align: center;'>👤 My Profile</h1>", unsafe_allow_html=True)
                col1,col2 = st.columns([1,2])
                with col1:
                    if user.get('profile_pic'):
                        st.image(user['profile_pic'], width=200)
                    else:
                        st.markdown("<h1 style='font-size: 8rem; text-align: center;'>👨‍🎓</h1>", unsafe_allow_html=True)
                    pic = st.file_uploader("✨ Upload Photo", type=['png','jpg','jpeg'], key="student_pic")
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
                        if st.form_submit_button("✨ Update Profile ✨", use_container_width=True):
                            for u in users:
                                if u['email'] == user['email']:
                                    u['fullname'] = name
                                    u['phone'] = phone
                                    u['bio'] = bio
                            save_school_data(school_code, "users.json", users)
                            user.update({'fullname':name,'phone':phone,'bio':bio})
                            st.success("Profile updated!")
                            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.error("Something went wrong. Please restart.")
    if st.button("Restart"):
        st.session_state.page = 'welcome'
        st.rerun()
