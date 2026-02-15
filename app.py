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

# ============ FUNCTION TO GET BACKGROUND IMAGE ============
def get_background_image():
    """Returns a stunning background image URL"""
    images = [
        "https://images.pexels.com/photos/207691/pexels-photo-207691.jpeg?auto=compress&cs=tinysrgb&w=1920",
        "https://images.pexels.com/photos/256417/pexels-photo-256417.jpeg?auto=compress&cs=tinysrgb&w=1920",
        "https://images.pexels.com/photos/159844/cellular-education-classroom-159844.jpeg?auto=compress&cs=tinysrgb&w=1920",
        "https://images.pexels.com/photos/301926/pexels-photo-301926.jpeg?auto=compress&cs=tinysrgb&w=1920",
        "https://images.pexels.com/photos/5212345/pexels-photo-5212345.jpeg?auto=compress&cs=tinysrgb&w=1920",
        "https://images.pexels.com/photos/3769714/pexels-photo-3769714.jpeg?auto=compress&cs=tinysrgb&w=1920",
        "https://images.pexels.com/photos/3769981/pexels-photo-3769981.jpeg?auto=compress&cs=tinysrgb&w=1920",
        "https://images.pexels.com/photos/3770018/pexels-photo-3770018.jpeg?auto=compress&cs=tinysrgb&w=1920"
    ]
    return random.choice(images)

# ============ CUSTOM CSS - PERMANENT SIDEBAR ============
BG_IMAGE = get_background_image()

st.markdown(f"""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    * {{
        font-family: 'Poppins', sans-serif;
    }}
    
    /* STUNNING BACKGROUND IMAGE */
    .stApp {{
        background-image: url('{BG_IMAGE}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
        animation: zoom 30s infinite alternate;
    }}
    
    @keyframes zoom {{
        0% {{ transform: scale(1); }}
        100% {{ transform: scale(1.1); }}
    }}
    
    /* Dark overlay */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(0,0,0,0.7), rgba(0,0,0,0.5));
        z-index: 0;
    }}
    
    /* Ensure content above overlay */
    .main > div, section[data-testid="stSidebar"] {{
        position: relative;
        z-index: 2;
    }}
    
    /* ============ SIDEBAR - PERMANENTLY OPEN & NEVER COLLAPSIBLE ============ */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(135deg, rgba(75, 0, 130, 0.98), rgba(138, 43, 226, 0.98), rgba(255, 215, 0, 0.95)) !important;
        backdrop-filter: blur(15px) !important;
        border-right: 4px solid gold !important;
        box-shadow: 10px 0 40px rgba(0, 0, 0, 0.8) !important;
        width: 350px !important;
        min-width: 350px !important;
        max-width: 350px !important;
        flex-shrink: 0 !important;
        overflow-y: auto !important;
        height: 100vh !important;
        position: fixed !important;
        left: 0 !important;
        top: 0 !important;
    }}
    
    /* Force sidebar to always be expanded */
    .css-1d391kg, .st-emotion-cache-1d391kg {{
        width: 350px !important;
        min-width: 350px !important;
        max-width: 350px !important;
        flex-shrink: 0 !important;
        margin-left: 0 !important;
        transform: translateX(0) !important;
    }}
    
    /* Hide collapse button completely */
    button[data-testid="collapsed-control"] {{
        display: none !important;
    }}
    
    /* Adjust main content for fixed sidebar */
    .main .block-container {{
        margin-left: 350px !important;
        max-width: calc(100% - 350px) !important;
        padding: 2rem !important;
    }}
    
    section[data-testid="stSidebar"] > div {{
        background: transparent !important;
        padding: 2rem 1.5rem !important;
        width: 100% !important;
    }}
    
    /* Sidebar text - white & bold */
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
    section[data-testid="stSidebar"] .st-emotion-cache-1v0mbdj {{
        color: WHITE !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }}
    
    /* Sidebar radio buttons */
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {{
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(5px) !important;
        border-radius: 25px !important;
        padding: 1.2rem !important;
        border: 3px solid gold !important;
        margin: 1.5rem 0 !important;
    }}
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {{
        background: rgba(0, 0, 0, 0.4) !important;
        border-radius: 20px !important;
        padding: 15px 20px !important;
        margin: 10px 0 !important;
        border: 2px solid transparent !important;
        transition: all 0.3s ease !important;
        color: WHITE !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        display: flex !important;
        align-items: center !important;
        gap: 15px !important;
    }}
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {{
        background: rgba(255, 215, 0, 0.4) !important;
        transform: translateX(10px) !important;
        border-color: gold !important;
        box-shadow: 0 5px 20px rgba(255, 215, 0, 0.6) !important;
    }}
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] {{
        background: linear-gradient(135deg, gold, #ffd700) !important;
        border: 3px solid white !important;
        box-shadow: 0 0 30px gold !important;
        color: #4B0082 !important;
        font-weight: 900 !important;
    }}
    
    /* Sidebar button */
    section[data-testid="stSidebar"] .stButton button {{
        background: linear-gradient(135deg, gold, #ffd700) !important;
        color: #4B0082 !important;
        border: 4px solid white !important;
        border-radius: 60px !important;
        padding: 18px 25px !important;
        font-weight: 900 !important;
        font-size: 1.3rem !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.5) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin: 1.5rem 0 !important;
    }}
    
    section[data-testid="stSidebar"] .stButton button:hover {{
        transform: scale(1.05) !important;
        box-shadow: 0 15px 40px gold !important;
        border-color: gold !important;
    }}
    
    /* School header */
    .school-header {{
        background: linear-gradient(135deg, rgba(75, 0, 130, 0.95), rgba(138, 43, 226, 0.95));
        backdrop-filter: blur(10px);
        border: 5px solid gold;
        border-radius: 40px;
        padding: 30px;
        margin-bottom: 25px;
        text-align: center;
        box-shadow: 0 15px 45px rgba(0,0,0,0.6);
        animation: header-glow 3s infinite;
    }}
    
    @keyframes header-glow {{
        0%, 100% {{ border-color: gold; box-shadow: 0 0 40px gold; }}
        50% {{ border-color: white; box-shadow: 0 0 60px white; }}
    }}
    
    .school-header h2 {{
        color: WHITE !important;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
        margin: 0;
        font-size: 2.2rem;
        font-weight: 900;
    }}
    
    .school-code {{
        background: rgba(0,0,0,0.5);
        padding: 15px;
        border-radius: 50px;
        margin-top: 15px;
        border: 3px solid gold;
    }}
    
    .school-code code {{
        background: transparent !important;
        color: gold !important;
        font-size: 1.5rem;
        font-weight: 800;
    }}
    
    /* Profile card */
    .profile-card {{
        background: linear-gradient(135deg, rgba(75, 0, 130, 0.95), rgba(138, 43, 226, 0.95));
        backdrop-filter: blur(10px);
        border: 4px solid gold;
        border-radius: 35px;
        padding: 25px;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        gap: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    }}
    
    .profile-card h1 {{
        color: WHITE !important;
        margin: 0;
        font-size: 4rem;
    }}
    
    /* Main content */
    .main > div {{
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 50px;
        padding: 2.5rem;
        margin: 1.5rem;
        border: 4px solid rgba(255, 215, 0, 0.6);
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6);
        animation: float 6s ease-in-out infinite;
    }}
    
    @keyframes float {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-5px); }}
    }}
    
    /* Headers */
    h1 {{
        background: linear-gradient(135deg, gold, #ffd700, #fff5b0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        text-align: center;
        animation: title-glow 3s infinite;
        margin-bottom: 2rem !important;
    }}
    
    @keyframes title-glow {{
        0%, 100% {{ filter: drop-shadow(0 0 30px gold); }}
        50% {{ filter: drop-shadow(0 0 50px white); }}
    }}
    
    h2, h3 {{
        color: WHITE !important;
        font-weight: 800 !important;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.6);
        font-size: 2rem !important;
    }}
    
    /* White text boxes with black text */
    .stTextInput input, .stTextArea textarea, .stSelectbox div, .stDateInput input {{
        background: WHITE !important;
        border: 4px solid gold !important;
        border-radius: 30px !important;
        color: BLACK !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
        padding: 1rem 1.5rem !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease !important;
    }}
    
    .stTextInput input:focus, .stTextArea textarea:focus {{
        border-color: #4B0082 !important;
        box-shadow: 0 0 40px gold !important;
        transform: scale(1.02) !important;
    }}
    
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {{
        color: #666666 !important;
        font-style: italic;
        font-weight: 500 !important;
    }}
    
    .stTextInput label, .stTextArea label, .stSelectbox label, .stDateInput label {{
        color: WHITE !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
        margin-bottom: 0.8rem !important;
    }}
    
    .stSelectbox div[data-baseweb="select"] > div {{
        background: WHITE !important;
        color: BLACK !important;
    }}
    
    .stDateInput input {{
        color: BLACK !important;
    }}
    
    /* Buttons */
    .stButton button {{
        background: linear-gradient(135deg, gold, #ffd700, #fff5b0) !important;
        color: #4B0082 !important;
        border: 5px solid white !important;
        border-radius: 70px !important;
        padding: 1rem 3rem !important;
        font-weight: 900 !important;
        font-size: 1.3rem !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.4) !important;
        transition: all 0.3s ease !important;
    }}
    
    .stButton button:hover {{
        transform: scale(1.05) translateY(-3px) !important;
        box-shadow: 0 20px 50px gold !important;
        border-color: gold !important;
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 70px !important;
        padding: 0.8rem !important;
        border: 4px solid gold !important;
        gap: 0.8rem;
        margin-bottom: 2.5rem !important;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        color: WHITE !important;
        border-radius: 60px !important;
        padding: 1rem 2.5rem !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        transition: all 0.3s ease !important;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, gold, #ffd700) !important;
        color: #4B0082 !important;
        font-weight: 900 !important;
        border: 3px solid white !important;
        box-shadow: 0 0 40px gold !important;
    }}
    
    /* Metrics */
    .stMetric {{
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(5px) !important;
        border: 4px solid gold !important;
        border-radius: 35px !important;
        padding: 2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3) !important;
    }}
    
    .stMetric:hover {{
        transform: translateY(-8px) !important;
        box-shadow: 0 20px 50px gold !important;
    }}
    
    .stMetric label {{
        color: WHITE !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }}
    
    .stMetric div {{
        color: gold !important;
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        text-shadow: 0 0 30px gold !important;
    }}
    
    /* Expanders */
    .streamlit-expanderHeader {{
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(5px) !important;
        border: 4px solid gold !important;
        border-radius: 30px !important;
        color: WHITE !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
        padding: 1.2rem !important;
    }}
    
    /* Alerts */
    .stAlert {{
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 25px !important;
        color: WHITE !important;
        font-weight: 700 !important;
        border-left: 8px solid !important;
        padding: 1.5rem !important;
        font-size: 1.1rem !important;
    }}
    
    .stAlert-success {{ border-left-color: #00ff88 !important; box-shadow: 0 0 25px #00ff88 !important; }}
    .stAlert-error {{ border-left-color: #ff4757 !important; box-shadow: 0 0 25px #ff4757 !important; }}
    .stAlert-warning {{ border-left-color: gold !important; box-shadow: 0 0 25px gold !important; }}
    
    /* Dividers */
    hr {{
        border: none !important;
        height: 4px !important;
        background: linear-gradient(90deg, transparent, gold, white, gold, transparent) !important;
        margin: 2.5rem 0 !important;
    }}
    
    /* Code blocks */
    code {{
        background: rgba(0, 0, 0, 0.5) !important;
        color: gold !important;
        border: 3px solid gold !important;
        border-radius: 20px !important;
        padding: 0.4rem 1rem !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
    }}
    
    /* Glass cards */
    .glass-card {{
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        border: 5px solid gold !important;
        border-radius: 45px !important;
        padding: 2.5rem !important;
        box-shadow: 0 25px 60px rgba(0,0,0,0.4) !important;
        transition: all 0.3s ease !important;
    }}
    
    .glass-card:hover {{
        transform: translateY(-8px) !important;
        box-shadow: 0 30px 70px gold !important;
    }}
    
    .glass-card * {{
        color: WHITE !important;
    }}
    
    /* Title */
    .radiant-title {{
        text-align: center;
        font-size: 5.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, gold, #ffd700, #fff5b0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: title-float 3s infinite, title-glow 3s infinite;
        margin-bottom: 1rem;
        text-shadow: 0 0 50px rgba(255, 215, 0, 0.6);
    }}
    
    @keyframes title-float {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-10px); }}
    }}
    
    .radiant-subtitle {{
        text-align: center;
        color: WHITE !important;
        font-size: 2.2rem;
        font-weight: 400;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.6);
        margin-bottom: 2.5rem;
        animation: subtitle-pulse 3s infinite;
    }}
    
    @keyframes subtitle-pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.8; }}
    }}
    
    /* Hide footer */
    footer {{
        display: none !important;
    }}
    
    /* Scrollbar */
    ::-webkit-scrollbar {{
        width: 14px;
        background: rgba(255,255,255,0.1);
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(135deg, gold, #ffd700);
        border-radius: 10px;
        border: 3px solid white;
    }}
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
    
    tab1, tab2, tab3, tab4 = st.tabs(["👑 **Admin Login**", "🏫 **Create School**", "👨‍🏫 **Teacher Login**", "👨‍🎓 **Student Login**"])
    
    # TAB 1: ADMIN LOGIN
    with tab1:
        col1, col2 = st.columns([1,1])
        with col1:
            with st.form("admin_login", clear_on_submit=True):
                st.subheader("🌟 Admin Login")
                school_code = st.text_input("🏫 School Code", placeholder="Enter your school code")
                admin_email = st.text_input("📧 Email", placeholder="admin@school.edu")
                admin_password = st.text_input("🔐 Password", type="password", placeholder="••••••••")
                if st.form_submit_button("✨ LOGIN ✨", use_container_width=True):
                    if not school_code or not admin_email or not admin_password:
                        st.error("Please fill all fields")
                    else:
                        all_schools = load_all_schools()
                        if school_code in all_schools:
                            school = all_schools[school_code]
                            if school['admin_email'] == admin_email:
                                users = load_school_data(school_code, "users.json", [])
                                hashed = hashlib.sha256(admin_password.encode()).hexdigest()
                                for u in users:
                                    if u['email'] == admin_email and u['password'] == hashed and u['role'] == 'admin':
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
                <h3>👑 Admin Powers</h3>
                <p style="opacity: 0.9;">Full control over your school community</p>
                <div style="font-size: 5rem;">✨</div>
            </div>
            """, unsafe_allow_html=True)
    
    # TAB 2: CREATE SCHOOL
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
                <h3>🎓 Begin Your Legacy</h3>
                <p style="opacity: 0.9;">Create your school and become the founding administrator</p>
                <div style="font-size: 5rem;">🚀</div>
            </div>
            """, unsafe_allow_html=True)
    
    # TAB 3: TEACHER
    with tab3:
        subtab1, subtab2 = st.tabs(["🔐 **Teacher Login**", "📝 **New Teacher**"])
        
        with subtab1:
            col1, col2 = st.columns([1,1])
            with col1:
                with st.form("teacher_login", clear_on_submit=True):
                    st.subheader("👨‍🏫 Teacher Login")
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
                    <h3>📚 Your Classroom Awaits</h3>
                    <p style="opacity: 0.9;">Login to manage classes and inspire students</p>
                    <div style="font-size: 5rem;">🍎</div>
                </div>
                """, unsafe_allow_html=True)
        
        with subtab2:
            col1, col2 = st.columns([1,1])
            with col1:
                with st.form("teacher_register", clear_on_submit=True):
                    st.subheader("🌟 New Teacher Registration")
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
                                school['stats']['teachers'] += 1
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
                    <h3>🎯 Start Your Journey</h3>
                    <p style="opacity: 0.9;">Use your teacher code to join your school community</p>
                    <div style="font-size: 5rem;">✨</div>
                </div>
                """, unsafe_allow_html=True)
    
    # TAB 4: STUDENT
    with tab4:
        subtab1, subtab2 = st.tabs(["🔐 **Student Login**", "📝 **New Student**"])
        
        with subtab1:
            col1, col2 = st.columns([1,1])
            with col1:
                with st.form("student_login", clear_on_submit=True):
                    st.subheader("👨‍🎓 Student Login")
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
                    <h3>📚 Your Learning Hub</h3>
                    <p style="opacity: 0.9;">Access classes, homework, and connect with peers</p>
                    <div style="font-size: 5rem;">📖</div>
                </div>
                """, unsafe_allow_html=True)
        
        with subtab2:
            col1, col2 = st.columns([1,1])
            with col1:
                with st.form("student_register", clear_on_submit=True):
                    st.subheader("🌟 New Student Registration")
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
                                    school['stats']['students'] += 1
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
                    <h3>🎓 Begin Your Adventure</h3>
                    <p style="opacity: 0.9;">Join your school and start your learning journey</p>
                    <div style="font-size: 5rem;">🚀</div>
                </div>
                """, unsafe_allow_html=True)

# ----- DASHBOARD -----
elif st.session_state.page == 'dashboard' and st.session_state.current_school and st.session_state.user:
    school = st.session_state.current_school
    user = st.session_state.user
    school_code = school['code']
    
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
        <div class="school-header">
            <h2>{school['name']}</h2>
            <p style="color: rgba(255,255,255,0.9); font-style: italic; margin: 5px 0;">✨ {school.get('motto','')} ✨</p>
            <div class="school-code">
                <code>{school['code']}</code>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        if user.get('profile_pic'):
            st.image(user['profile_pic'], width=80)
        else:
            emoji = "👑" if user['role'] == 'admin' else "👨‍🏫" if user['role'] == 'teacher' else "👨‍🎓"
            st.markdown(f"<h1 style='font-size: 4rem; margin: 0;'>{emoji}</h1>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="color: white; flex: 1;">
            <strong style="font-size: 1.4rem;">{user['fullname']}</strong><br>
            <span style="background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 50px; font-size: 0.9rem; font-weight: 700;">{user['role'].upper()}</span><br>
            <span style="font-size: 0.9rem; opacity: 0.9;">{user['email']}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        
        if user['role'] == 'admin':
            options = ["Dashboard", "Teachers", "Classes", "Students", "Groups", "Approvals", "Profile"]
        elif user['role'] == 'teacher':
            options = ["Dashboard", "My Classes", "My Groups", "Assignments", "Requests", "Profile"]
        else:
            options = ["Dashboard", "Browse Classes", "Browse Groups", "Homework", "My Grades", "Profile"]
        
        menu = st.radio("Navigation", options, index=st.session_state.menu_index, label_visibility="collapsed")
        
        st.divider()
        
        if st.button("🚪 LOGOUT", use_container_width=True):
            st.session_state.user = None
            st.session_state.current_school = None
            st.session_state.page = 'welcome'
            st.rerun()
    
    # ============ MAIN CONTENT ============
    if user['role'] == 'admin' and menu == "Dashboard":
        st.markdown(f"<h1 style='text-align: center;'>👑 {school['name']} Dashboard</h1>", unsafe_allow_html=True)
        col1,col2,col3,col4 = st.columns(4)
        col1.metric("Students", school['stats'].get('students',0))
        col2.metric("Teachers", school['stats'].get('teachers',0))
        col3.metric("Classes", school['stats'].get('classes',0))
        col4.metric("Groups", school['stats'].get('groups',0))

else:
    st.error("Something went wrong. Please restart.")
    if st.button("🔄 Restart"):
        st.session_state.page = 'welcome'
        st.rerun()
