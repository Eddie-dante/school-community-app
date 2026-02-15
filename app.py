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

# ============ CUSTOM CSS - VIBRANT & BEAUTIFUL ============
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* VIBRANT GRADIENT BACKGROUND */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #ff6b6b 100%);
        min-height: 100vh;
    }
    
    /* MAIN CONTENT AREA - GLASS EFFECT */
    .main > div {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 30px;
        padding: 2rem;
        margin: 1rem;
        border: 3px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* ============ SIDEBAR - VIBRANT PURPLE ============ */
    section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #4834d4 0%, #686de0 50%, #7ed6df 100%) !important;
        border-right: 4px solid #f9ca24 !important;
        box-shadow: 10px 0 30px rgba(0,0,0,0.3) !important;
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent !important;
        padding: 1.5rem 1rem !important;
    }
    
    /* SIDEBAR TEXT - BRIGHT AND BEAUTIFUL */
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stRadio label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: WHITE !important;
        font-weight: 600 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
    }
    
    /* SIDEBAR RADIO BUTTONS - BEAUTIFUL CARDS */
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(5px) !important;
        border-radius: 20px !important;
        padding: 1rem !important;
        border: 2px solid #f9ca24 !important;
    }
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        background: rgba(0, 0, 0, 0.3) !important;
        border-radius: 15px !important;
        padding: 12px 18px !important;
        margin: 8px 0 !important;
        border: 2px solid transparent !important;
        transition: all 0.3s ease !important;
        color: WHITE !important;
        font-weight: 600 !important;
    }
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
        background: rgba(249, 202, 36, 0.3) !important;
        border-color: #f9ca24 !important;
        transform: translateX(5px) !important;
    }
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] {
        background: linear-gradient(135deg, #f9ca24, #f6e58d) !important;
        border: 2px solid white !important;
        color: #4834d4 !important;
        font-weight: 800 !important;
        box-shadow: 0 0 20px #f9ca24 !important;
    }
    
    /* SIDEBAR BUTTON */
    section[data-testid="stSidebar"] .stButton button {
        background: linear-gradient(135deg, #f9ca24, #f6e58d) !important;
        color: #4834d4 !important;
        border: 3px solid white !important;
        border-radius: 50px !important;
        padding: 12px 24px !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    section[data-testid="stSidebar"] .stButton button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 8px 25px #f9ca24 !important;
    }
    
    /* SCHOOL HEADER - VIBRANT */
    .school-header {
        background: linear-gradient(135deg, rgba(72, 52, 212, 0.9), rgba(126, 214, 223, 0.9));
        backdrop-filter: blur(10px);
        border: 4px solid #f9ca24;
        border-radius: 30px;
        padding: 25px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        animation: glow 3s infinite;
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 30px #f9ca24; }
        50% { box-shadow: 0 0 50px #7ed6df; }
    }
    
    .school-header h2 {
        color: WHITE !important;
        font-size: 2rem;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin: 0;
    }
    
    .school-code {
        background: rgba(0, 0, 0, 0.4);
        padding: 12px;
        border-radius: 50px;
        margin-top: 15px;
        border: 2px solid #f9ca24;
    }
    
    .school-code code {
        color: #f9ca24 !important;
        font-size: 1.3rem;
        font-weight: 700;
        background: transparent !important;
    }
    
    /* PROFILE CARD */
    .profile-card {
        background: linear-gradient(135deg, rgba(72, 52, 212, 0.8), rgba(126, 214, 223, 0.8));
        backdrop-filter: blur(10px);
        border: 3px solid #f9ca24;
        border-radius: 25px;
        padding: 20px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .profile-card h1 {
        color: WHITE !important;
        font-size: 3rem;
        margin: 0;
    }
    
    /* ============ MAIN CONTENT - VIBRANT ============ */
    /* HEADERS - BEAUTIFUL GRADIENT */
    h1 {
        background: linear-gradient(135deg, #f9ca24, #f6e58d, #7ed6df, #686de0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        font-weight: 800 !important;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        animation: title-glow 3s infinite;
    }
    
    @keyframes title-glow {
        0%, 100% { filter: drop-shadow(0 0 20px #f9ca24); }
        50% { filter: drop-shadow(0 0 40px #7ed6df); }
    }
    
    h2, h3 {
        color: WHITE !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* FORM ELEMENTS - BEAUTIFUL */
    .stTextInput label, .stTextArea label, .stSelectbox label, .stDateInput label {
        color: WHITE !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    .stTextInput input, .stTextArea textarea, .stSelectbox div, .stDateInput input {
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(5px) !important;
        border: 3px solid #f9ca24 !important;
        border-radius: 15px !important;
        color: WHITE !important;
        font-weight: 500 !important;
        font-size: 1.1rem !important;
        padding: 0.8rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #7ed6df !important;
        box-shadow: 0 0 25px #f9ca24 !important;
        background: rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Placeholder text */
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: rgba(255, 255, 255, 0.7) !important;
        font-style: italic;
    }
    
    /* BUTTONS - VIBRANT GRADIENT */
    .stButton button {
        background: linear-gradient(135deg, #f9ca24, #f6e58d, #7ed6df, #686de0) !important;
        background-size: 300% 300% !important;
        animation: gradient-shift 5s ease infinite !important;
        color: #4834d4 !important;
        border: 3px solid white !important;
        border-radius: 50px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    @keyframes gradient-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stButton button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 8px 30px #f9ca24 !important;
        border-color: #f9ca24 !important;
    }
    
    /* TABS - BEAUTIFUL */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(5px) !important;
        border-radius: 50px !important;
        padding: 0.5rem !important;
        border: 3px solid #f9ca24 !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: WHITE !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        padding: 0.8rem 2rem !important;
        border-radius: 50px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #f9ca24, #f6e58d) !important;
        color: #4834d4 !important;
        font-weight: 800 !important;
        border: 2px solid white !important;
    }
    
    /* METRICS - BEAUTIFUL CARDS */
    .stMetric {
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(5px) !important;
        border: 3px solid #f9ca24 !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stMetric:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 10px 30px #f9ca24 !important;
    }
    
    .stMetric label {
        color: WHITE !important;
        font-size: 1.1rem !important;
    }
    
    .stMetric div {
        color: #f9ca24 !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        text-shadow: 0 0 15px #f9ca24 !important;
    }
    
    /* EXPANDERS */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(5px) !important;
        border: 3px solid #f9ca24 !important;
        border-radius: 15px !important;
        color: WHITE !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }
    
    /* ALERTS - VIBRANT */
    .stAlert {
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(5px) !important;
        border-left: 6px solid !important;
        border-radius: 15px !important;
        color: WHITE !important;
        font-weight: 600 !important;
    }
    
    .stAlert-success {
        border-left-color: #00ff88 !important;
    }
    
    .stAlert-error {
        border-left-color: #ff4757 !important;
    }
    
    .stAlert-warning {
        border-left-color: #f9ca24 !important;
    }
    
    /* DIVIDERS - BEAUTIFUL */
    hr {
        border: none !important;
        height: 4px !important;
        background: linear-gradient(90deg, transparent, #f9ca24, #7ed6df, #686de0, #f9ca24, transparent) !important;
        margin: 2rem 0 !important;
    }
    
    /* CODE */
    code {
        background: rgba(0, 0, 0, 0.4) !important;
        color: #f9ca24 !important;
        border: 2px solid #f9ca24 !important;
        border-radius: 10px !important;
        padding: 0.2rem 0.5rem !important;
        font-weight: 700 !important;
    }
    
    /* CARDS */
    .glass-card {
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        border: 4px solid #f9ca24 !important;
        border-radius: 30px !important;
        padding: 2rem !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .glass-card:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 15px 40px #f9ca24 !important;
    }
    
    .glass-card * {
        color: WHITE !important;
    }
    
    /* TITLE */
    .radiant-title {
        text-align: center;
        font-size: 4.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #f9ca24, #f6e58d, #7ed6df, #686de0, #ff6b6b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: title-float 3s infinite;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(249, 202, 36, 0.5);
    }
    
    @keyframes title-float {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }
    
    .radiant-subtitle {
        text-align: center;
        color: WHITE !important;
        font-size: 2rem;
        font-weight: 400;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
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
    
    tab1, tab2, tab3, tab4 = st.tabs(["👑 Admin Portal", "🏫 Create School", "👨‍🏫 Teacher Space", "👨‍🎓 Student World"])
    
    # TAB 1: ADMIN LOGIN
    with tab1:
        col1, col2 = st.columns([1,1])
        with col1:
            st.subheader("🔐 Admin Login")
            with st.form("admin_login"):
                school = st.text_input("🏫 School Code", placeholder="Enter your school code")
                email = st.text_input("📧 Email", placeholder="admin@school.edu")
                pwd = st.text_input("🔑 Password", type="password", placeholder="••••••••")
                if st.form_submit_button("✨ Login Now ✨", use_container_width=True):
                    if not school or not email or not pwd:
                        st.error("Please fill all fields")
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
                                st.error("Invalid password")
                            else:
                                st.error("Not admin email")
                        else:
                            st.error("School not found")
        with col2:
            st.markdown("""
            <div class="glass-card" style="text-align: center;">
                <h3 style="color: #f9ca24;">👑 Admin Powers</h3>
                <p style="color: white;">Full control over your school community</p>
                <h1 style="font-size: 5rem; color: #f9ca24;">✨</h1>
            </div>
            """, unsafe_allow_html=True)
    
    # TAB 2: CREATE SCHOOL
    with tab2:
        col1, col2 = st.columns([1,1])
        with col1:
            st.subheader("🚀 Create New School")
            with st.form("create_school"):
                name = st.text_input("🏫 School Name", placeholder="e.g., Nqatho Sec Sch")
                admin = st.text_input("👤 Your Full Name", placeholder="Wanjiku Edwin Guchu")
                email = st.text_input("📧 Your Email", placeholder="you@school.edu")
                pwd = st.text_input("🔐 Password", type="password", placeholder="Create strong password")
                confirm = st.text_input("🔐 Confirm Password", type="password", placeholder="Confirm password")
                city = st.text_input("🏙️ City", placeholder="Nairobi")
                state = st.text_input("🗺️ State", placeholder="Nairobi")
                motto = st.text_input("✨ School Motto", placeholder="DTS")
                
                if st.form_submit_button("🌟 Create School 🌟", use_container_width=True):
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
                        st.success(f"✨ School Created! Code: **{code}**")
                        st.rerun()
        with col2:
            st.markdown("""
            <div class="glass-card" style="text-align: center;">
                <h3 style="color: #f9ca24;">🎓 Begin Your Legacy</h3>
                <p style="color: white;">Start your own school community</p>
                <h1 style="font-size: 5rem; color: #f9ca24;">🚀</h1>
            </div>
            """, unsafe_allow_html=True)
    
    # TAB 3: TEACHER
    with tab3:
        subtab1, subtab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with subtab1:
            col1, col2 = st.columns([1,1])
            with col1:
                st.subheader("👨‍🏫 Teacher Login")
                with st.form("teacher_login"):
                    school = st.text_input("🏫 School Code")
                    email = st.text_input("📧 Email")
                    pwd = st.text_input("🔑 Password", type="password")
                    if st.form_submit_button("✨ Login ✨", use_container_width=True):
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
                <div class="glass-card" style="text-align: center;">
                    <h3 style="color: #f9ca24;">📚 Your Classroom</h3>
                    <p style="color: white;">Login to manage classes</p>
                    <h1 style="font-size: 5rem; color: #f9ca24;">🍎</h1>
                </div>
                """, unsafe_allow_html=True)
        
        with subtab2:
            col1, col2 = st.columns([1,1])
            with col1:
                st.subheader("📝 New Teacher")
                with st.form("teacher_register"):
                    school = st.text_input("🏫 School Code", key="reg_school")
                    teacher_code = st.text_input("🔑 Teacher Code", placeholder="e.g., MATH-DEPT")
                    name = st.text_input("👤 Full Name")
                    email = st.text_input("📧 Email", key="reg_email")
                    pwd = st.text_input("🔐 Password", type="password", key="reg_pass")
                    confirm = st.text_input("🔐 Confirm Password", type="password", key="reg_confirm")
                    
                    if st.form_submit_button("🌟 Register Now 🌟", use_container_width=True):
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
                                st.success("✨ Registration successful!")
                                st.rerun()
                            else:
                                st.error("School not found")
            with col2:
                st.markdown("""
                <div class="glass-card" style="text-align: center;">
                    <h3 style="color: #f9ca24;">✨ Join the Team</h3>
                    <p style="color: white;">Use your teacher code</p>
                    <h1 style="font-size: 5rem; color: #f9ca24;">📝</h1>
                </div>
                """, unsafe_allow_html=True)
    
    # TAB 4: STUDENT
    with tab4:
        subtab1, subtab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with subtab1:
            col1, col2 = st.columns([1,1])
            with col1:
                st.subheader("👨‍🎓 Student Login")
                with st.form("student_login"):
                    school = st.text_input("🏫 School Code")
                    email = st.text_input("📧 Email")
                    pwd = st.text_input("🔑 Password", type="password")
                    if st.form_submit_button("✨ Login ✨", use_container_width=True):
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
                <div class="glass-card" style="text-align: center;">
                    <h3 style="color: #f9ca24;">📖 Your Learning Hub</h3>
                    <p style="color: white;">Access classes and homework</p>
                    <h1 style="font-size: 5rem; color: #f9ca24;">📚</h1>
                </div>
                """, unsafe_allow_html=True)
        
        with subtab2:
            col1, col2 = st.columns([1,1])
            with col1:
                st.subheader("🆕 New Student")
                with st.form("student_register"):
                    school = st.text_input("🏫 School Code", key="stud_school")
                    name = st.text_input("👤 Full Name")
                    email = st.text_input("📧 Email", key="stud_email")
                    pwd = st.text_input("🔐 Password", type="password", key="stud_pass")
                    confirm = st.text_input("🔐 Confirm Password", type="password", key="stud_confirm")
                    
                    if st.form_submit_button("🌟 Register Now 🌟", use_container_width=True):
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
                                    st.success("✨ Registration successful!")
                                    st.rerun()
                            else:
                                st.error("School not found")
            with col2:
                st.markdown("""
                <div class="glass-card" style="text-align: center;">
                    <h3 style="color: #f9ca24;">🎓 Begin Your Journey</h3>
                    <p style="color: white;">Join your school community</p>
                    <h1 style="font-size: 5rem; color: #f9ca24;">🌟</h1>
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
            <strong style="font-size: 1.2rem;">{user['fullname']}</strong><br>
            <span style="background: #f9ca24; color: #4834d4; padding: 3px 12px; border-radius: 20px; font-weight: 700;">{user['role'].upper()}</span><br>
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
        
        menu = st.radio("📌 Navigation", options, index=st.session_state.menu_index)
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.current_school = None
            st.session_state.page = 'welcome'
            st.rerun()
    
    # MAIN CONTENT
    if user['role'] == 'admin':
        if menu == "Dashboard":
            st.markdown(f"<h1>👑 {school['name']} Dashboard</h1>", unsafe_allow_html=True)
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("🎓 Students", school['stats'].get('students',0))
            col2.metric("👨‍🏫 Teachers", school['stats'].get('teachers',0))
            col3.metric("📚 Classes", school['stats'].get('classes',0))
            col4.metric("👥 Groups", school['stats'].get('groups',0))
            
            pending = len([r for r in class_requests if r['status']=='pending']) + len([r for r in group_requests if r['status']=='pending'])
            if pending:
                st.warning(f"✨ {pending} pending requests")
            else:
                st.success("✨ All caught up!")
        
        elif menu == "Teachers":
            st.markdown("<h1>👨‍🏫 Teacher Management</h1>", unsafe_allow_html=True)
            tab1, tab2 = st.tabs(["✨ Create Codes", "👥 Active Teachers"])
            
            with tab1:
                with st.form("create_code"):
                    name = st.text_input("Code Name", placeholder="e.g., Mathematics Department")
                    code = st.text_input("Custom Code", placeholder="e.g., MATH-DEPT")
                    dept = st.selectbox("Department", ["Math","Science","English","History","Other"])
                    if st.form_submit_button("✨ Create Code", use_container_width=True):
                        if name and code:
                            if any(t['code']==code.upper() for t in teachers_data):
                                st.error("Code exists")
                            else:
                                teachers_data.append({
                                    "id": generate_id("TCH"),
                                    "name": name,
                                    "code": code.upper(),
                                    "department": dept,
                                    "created": datetime.now().strftime("%Y-%m-%d"),
                                    "status": "active",
                                    "used_by_list": []
                                })
                                save_school_data(school_code, "teachers.json", teachers_data)
                                st.success(f"Code {code.upper()} created!")
                                st.rerun()
            
            with tab2:
                for t in teachers_data:
                    with st.expander(f"{t['name']} - `{t['code']}`"):
                        st.write(f"Used by: {len(t.get('used_by_list',[]))} teachers")
        
        elif menu == "Approvals":
            st.markdown("<h1>✅ Admin Approvals</h1>", unsafe_allow_html=True)
            for req in [r for r in class_requests if r['status']=='pending']:
                col1,col2,col3 = st.columns([2,2,1])
                col1.write(req['student_name'])
                col2.write(req['class_name'])
                if col3.button("Approve", key=f"app_{req['id']}"):
                    for c in classes:
                        if c['name'] == req['class_name']:
                            c['students'].append(req['student_email'])
                    req['status'] = 'approved'
                    save_school_data(school_code, "classes.json", classes)
                    save_school_data(school_code, "class_requests.json", class_requests)
                    st.rerun()
        
        elif menu == "Profile":
            st.markdown("<h1>👤 My Profile</h1>", unsafe_allow_html=True)
            col1,col2 = st.columns([1,2])
            with col1:
                if user.get('profile_pic'):
                    st.image(user['profile_pic'], width=150)
                else:
                    st.markdown("<h1 style='font-size: 5rem;'>👑</h1>", unsafe_allow_html=True)
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
                    if st.form_submit_button("✨ Update Profile", use_container_width=True):
                        for u in users:
                            if u['email'] == user['email']:
                                u['fullname'] = name
                                u['phone'] = phone
                                u['bio'] = bio
                        save_school_data(school_code, "users.json", users)
                        user.update({'fullname':name,'phone':phone,'bio':bio})
                        st.success("Profile updated!")
                        st.rerun()
    
    elif user['role'] == 'teacher':
        if menu == "Dashboard":
            st.markdown(f"<h1>👨‍🏫 Welcome, {user['fullname']}!</h1>", unsafe_allow_html=True)
            my_classes = [c for c in classes if c.get('teacher') == user['email']]
            col1,col2,col3 = st.columns(3)
            col1.metric("My Classes", len(my_classes))
            col2.metric("My Groups", len([g for g in groups if g.get('leader')==user['email']]))
            col3.metric("Assignments", len([a for a in assignments if a.get('teacher')==user['email']]))
    
    else:  # student
        if menu == "Dashboard":
            st.markdown(f"<h1>👨‍🎓 Welcome, {user['fullname']}!</h1>", unsafe_allow_html=True)
            my_classes = [c for c in classes if user['email'] in c.get('students',[])]
            col1,col2,col3 = st.columns(3)
            col1.metric("My Classes", len(my_classes))
            col2.metric("My Groups", len([g for g in groups if user['email'] in g.get('members',[])]))
            col3.metric("Assignments", len([a for a in assignments if a['class'] in [c['name'] for c in my_classes]]))

else:
    st.error("Something went wrong")
    if st.button("🔄 Restart"):
        st.session_state.page = 'welcome'
        st.rerun()
