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

# ============ RESPONSIVE DESIGN META TAG ============
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
<style>
    /* Responsive Design */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 0.8rem !important;
        }
        h1 { font-size: 1.8rem !important; }
        h2 { font-size: 1.3rem !important; }
        .stButton button { font-size: 0.9rem !important; padding: 0.4rem 0.8rem !important; }
    }
    
    /* Sidebar behavior - thin on desktop, collapsible on mobile */
    @media (max-width: 768px) {
        section[data-testid="stSidebar"] {
            width: 85% !important;
            min-width: 85% !important;
            transform: translateX(-100%) !important;
            transition: transform 0.3s ease !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] {
            transform: translateX(0) !important;
        }
        .main .block-container {
            margin-left: 0 !important;
            max-width: 100% !important;
        }
    }
    
    /* Desktop sidebar - THIN */
    @media (min-width: 769px) {
        section[data-testid="stSidebar"] {
            width: 220px !important;
            min-width: 220px !important;
            transform: translateX(0) !important;
        }
        .main .block-container {
            margin-left: 220px !important;
            max-width: calc(100% - 220px) !important;
        }
        
        /* Make sidebar content more compact */
        section[data-testid="stSidebar"] > div {
            padding: 1rem 0.8rem !important;
        }
        
        /* Smaller text in sidebar */
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] .stRadio label,
        section[data-testid="stSidebar"] p {
            font-size: 0.9rem !important;
        }
        
        /* Compact radio buttons */
        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
            padding: 0.5rem !important;
        }
        
        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
            padding: 8px 10px !important;
            margin: 5px 0 !important;
            font-size: 0.9rem !important;
        }
        
        /* Compact school header */
        .school-header {
            padding: 12px !important;
            margin-bottom: 10px !important;
        }
        
        .school-header h2 {
            font-size: 1.3rem !important;
        }
        
        .school-code {
            padding: 5px !important;
            margin-top: 8px !important;
        }
        
        .school-code code {
            font-size: 0.9rem !important;
        }
        
        /* Compact profile card */
        .profile-card {
            padding: 10px !important;
            margin-bottom: 10px !important;
            gap: 8px !important;
        }
        
        .profile-card h1 {
            font-size: 2rem !important;
        }
        
        .profile-card strong {
            font-size: 1rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============ KENYAN CURRICULUM DATA ============
# Primary School (Grade 1-6) - 7 subjects
PRIMARY_SUBJECTS = [
    "Mathematics",
    "English",
    "Kiswahili",
    "Science and Technology",
    "Social Studies",
    "CRE / IRE / HRE",
    "Agriculture",
    "Home Science",
    "Art and Craft",
    "Music",
    "Physical Education"
]

# Junior Secondary (Grade 7-9) - 12 subjects
JUNIOR_SECONDARY_SUBJECTS = [
    "Mathematics",
    "English",
    "Kiswahili",
    "Integrated Science",
    "Social Studies",
    "CRE / IRE / HRE",
    "Business Studies",
    "Agriculture",
    "Home Science",
    "Computer Science",
    "Pre-Technical Studies",
    "Visual Arts",
    "Performing Arts",
    "Physical Education"
]

# Senior Secondary (Form 1-4) - 11 subjects (grouped)
SENIOR_SECONDARY_SUBJECTS = {
    "Mathematics": ["Mathematics"],
    "English": ["English"],
    "Kiswahili": ["Kiswahili"],
    "Sciences": ["Biology", "Chemistry", "Physics", "General Science"],
    "Humanities": ["History", "Geography", "CRE", "IRE", "HRE"],
    "Technical": ["Computer Studies", "Business Studies", "Agriculture", "Home Science"],
    "Languages": ["French", "German", "Arabic", "Sign Language"]
}

# Grade/Form list with subject counts
KENYAN_GRADES = [
    "Grade 1 (7 subjects)",
    "Grade 2 (7 subjects)",
    "Grade 3 (7 subjects)",
    "Grade 4 (7 subjects)",
    "Grade 5 (7 subjects)",
    "Grade 6 (7 subjects)",
    "Grade 7 (12 subjects)",
    "Grade 8 (12 subjects)",
    "Grade 9 (12 subjects)",
    "Form 1 (11 subjects)",
    "Form 2 (11 subjects)",
    "Form 3 (11 subjects)",
    "Form 4 (11 subjects)"
]

# ============ FUNCTION TO GET SUBJECTS BASED ON GRADE ============
def get_subjects_for_grade(grade):
    """Returns appropriate subjects based on grade level"""
    if "Grade" in grade and any(str(i) in grade for i in range(1, 7)):
        return PRIMARY_SUBJECTS
    elif "Grade" in grade and any(str(i) in grade for i in range(7, 10)):
        return JUNIOR_SECONDARY_SUBJECTS
    elif "Form" in grade:
        # Flatten senior secondary subjects
        subjects = []
        for category, subj_list in SENIOR_SECONDARY_SUBJECTS.items():
            subjects.extend(subj_list)
        return subjects
    else:
        return PRIMARY_SUBJECTS

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

# ============ CUSTOM CSS ============
BG_IMAGE = get_background_image()

st.markdown(f"""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    * {{
        font-family: 'Poppins', sans-serif;
        box-sizing: border-box;
    }}
    
    /* STUNNING BACKGROUND IMAGE */
    .stApp {{
        background-image: url('{BG_IMAGE}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
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
    
    /* ============ SIDEBAR - THIN ============ */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(135deg, rgba(75, 0, 130, 0.98), rgba(138, 43, 226, 0.98), rgba(255, 215, 0, 0.95)) !important;
        backdrop-filter: blur(15px) !important;
        border-right: 3px solid gold !important;
        box-shadow: 5px 0 20px rgba(0, 0, 0, 0.5) !important;
        overflow-y: auto !important;
        height: 100vh !important;
        transition: transform 0.3s ease !important;
    }}
    
    /* Hide collapse button styling */
    button[data-testid="baseButton-header"] {{
        display: none !important;
    }}
    
    section[data-testid="stSidebar"] > div {{
        background: transparent !important;
        padding: 1rem 0.8rem !important;
        width: 100% !important;
    }}
    
    /* Sidebar text - compact */
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stRadio label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {{
        color: WHITE !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }}
    
    /* Sidebar radio buttons - compact */
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {{
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(5px) !important;
        border-radius: 15px !important;
        padding: 0.5rem !important;
        border: 2px solid gold !important;
        margin: 0.8rem 0 !important;
    }}
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {{
        background: rgba(0, 0, 0, 0.3) !important;
        border-radius: 12px !important;
        padding: 8px 10px !important;
        margin: 4px 0 !important;
        border: 1px solid transparent !important;
        transition: all 0.2s ease !important;
        color: WHITE !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
    }}
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {{
        background: rgba(255, 215, 0, 0.3) !important;
        transform: translateX(3px) !important;
        border-color: gold !important;
    }}
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] {{
        background: linear-gradient(135deg, gold, #ffd700) !important;
        border: 2px solid white !important;
        box-shadow: 0 0 15px gold !important;
        color: #4B0082 !important;
        font-weight: 800 !important;
    }}
    
    /* Sidebar button - compact */
    section[data-testid="stSidebar"] .stButton button {{
        background: linear-gradient(135deg, gold, #ffd700) !important;
        color: #4B0082 !important;
        border: 2px solid white !important;
        border-radius: 40px !important;
        padding: 8px 12px !important;
        font-weight: 800 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3) !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        margin: 0.8rem 0 !important;
    }}
    
    section[data-testid="stSidebar"] .stButton button:hover {{
        transform: scale(1.02) !important;
        box-shadow: 0 8px 20px gold !important;
    }}
    
    /* School header - compact */
    .school-header {{
        background: linear-gradient(135deg, rgba(75, 0, 130, 0.9), rgba(138, 43, 226, 0.9));
        backdrop-filter: blur(10px);
        border: 3px solid gold;
        border-radius: 25px;
        padding: 12px;
        margin-bottom: 12px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
        animation: header-glow 3s infinite;
    }}
    
    @keyframes header-glow {{
        0%, 100% {{ border-color: gold; box-shadow: 0 0 20px gold; }}
        50% {{ border-color: white; box-shadow: 0 0 30px white; }}
    }}
    
    .school-header h2 {{
        color: WHITE !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin: 0;
        font-size: 1.3rem;
        font-weight: 800;
    }}
    
    .school-code {{
        background: rgba(0,0,0,0.4);
        padding: 5px;
        border-radius: 30px;
        margin-top: 8px;
        border: 2px solid gold;
    }}
    
    .school-code code {{
        background: transparent !important;
        color: gold !important;
        font-size: 0.9rem;
        font-weight: 700;
    }}
    
    /* Profile card - compact */
    .profile-card {{
        background: linear-gradient(135deg, rgba(75, 0, 130, 0.9), rgba(138, 43, 226, 0.9));
        backdrop-filter: blur(10px);
        border: 3px solid gold;
        border-radius: 25px;
        padding: 10px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.4);
    }}
    
    .profile-card h1 {{
        color: WHITE !important;
        margin: 0;
        font-size: 2rem;
    }}
    
    /* Main content */
    .main > div {{
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 40px;
        padding: 2rem;
        margin: 1.5rem;
        border: 4px solid rgba(255, 215, 0, 0.6);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
    }}
    
    /* Headers */
    h1 {{
        background: linear-gradient(135deg, gold, #ffd700, #fff5b0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        font-weight: 900 !important;
        text-align: center;
        margin-bottom: 1.5rem !important;
    }}
    
    h2, h3 {{
        color: WHITE !important;
        font-weight: 800 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.6);
    }}
    
    /* ============ CHAT STYLES ============ */
    .chat-container {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        padding: 15px;
        margin: 10px 0;
        border: 2px solid gold;
        max-height: 500px;
        overflow-y: auto;
    }}
    
    .chat-message {{
        background: rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 10px;
        margin: 8px 0;
        border-left: 4px solid gold;
    }}
    
    .chat-message.sent {{
        border-left-color: #4B0082;
        background: rgba(75, 0, 130, 0.2);
    }}
    
    .chat-sender {{
        font-weight: 700;
        color: gold;
        margin-bottom: 3px;
        font-size: 0.9rem;
    }}
    
    .chat-time {{
        font-size: 0.7rem;
        color: rgba(255,255,255,0.6);
        text-align: right;
        margin-top: 3px;
    }}
    
    /* ============ DROPDOWN STYLES ============ */
    .stSelectbox div[data-baseweb="select"] {{
        background: #FFFFFF !important;
        border: 3px solid gold !important;
        border-radius: 25px !important;
    }}
    
    .stSelectbox div[data-baseweb="select"] span {{
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }}
    
    .stSelectbox div[data-baseweb="select"] > div {{
        background: #FFFFFF !important;
        color: #000000 !important;
    }}
    
    div[data-baseweb="menu"] {{
        background: #FFFFFF !important;
        border: 3px solid gold !important;
        border-radius: 15px !important;
    }}
    
    div[data-baseweb="menu"] li {{
        color: #000000 !important;
        font-weight: 500 !important;
    }}
    
    /* Text inputs */
    .stTextInput input, .stTextArea textarea, .stDateInput input {{
        background: #FFFFFF !important;
        border: 3px solid gold !important;
        border-radius: 25px !important;
        color: #000000 !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        padding: 0.8rem 1.2rem !important;
    }}
    
    .stTextInput label, .stTextArea label, .stSelectbox label, .stDateInput label {{
        color: WHITE !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }}
    
    /* Buttons */
    .stButton button {{
        background: linear-gradient(135deg, gold, #ffd700) !important;
        color: #4B0082 !important;
        border: 3px solid white !important;
        border-radius: 50px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase !important;
        transition: all 0.3s ease !important;
    }}
    
    .stButton button:hover {{
        transform: scale(1.02) !important;
        box-shadow: 0 10px 30px gold !important;
    }}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 50px !important;
        padding: 0.5rem !important;
        border: 3px solid gold !important;
        gap: 0.5rem;
        margin-bottom: 2rem !important;
        flex-wrap: wrap !important;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        color: WHITE !important;
        border-radius: 40px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, gold, #ffd700) !important;
        color: #4B0082 !important;
        font-weight: 800 !important;
    }}
    
    /* Metrics */
    .stMetric {{
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(5px) !important;
        border: 3px solid gold !important;
        border-radius: 25px !important;
        padding: 1rem !important;
    }}
    
    .stMetric label {{
        color: WHITE !important;
        font-size: 0.9rem !important;
    }}
    
    .stMetric div {{
        color: gold !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
    }}
    
    /* Hide footer */
    footer {{
        display: none !important;
    }}
</style>
""", unsafe_allow_html=True)

# ============ CODE GENERATOR ============
def generate_id(prefix, length=6):
    chars = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choices(chars, k=length))
    return f"{prefix}{random_part}"

def generate_school_code():
    chars = string.ascii_uppercase + string.digits
    return 'SCH' + ''.join(random.choices(chars, k=5))

def generate_class_code():
    return 'CLS' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

def generate_group_code():
    return 'GRP' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

def generate_admission_number():
    """Generate a unique admission number for students"""
    year = datetime.now().strftime("%y")
    random_num = ''.join(random.choices(string.digits, k=4))
    return f"ADM/{year}/{random_num}"

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

# ============ CHAT FUNCTIONS ============
def send_message(users, user_email, recipient_email, message, school_code):
    """Send a message to another user"""
    messages = load_school_data(school_code, "messages.json", [])
    
    new_message = {
        "id": generate_id("MSG"),
        "sender": user_email,
        "recipient": recipient_email,
        "message": message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "read": False,
        "conversation_id": f"{min(user_email, recipient_email)}_{max(user_email, recipient_email)}"
    }
    
    messages.append(new_message)
    save_school_data(school_code, "messages.json", messages)
    return new_message

def get_conversations(user_email, school_code):
    """Get all conversations for a user"""
    messages = load_school_data(school_code, "messages.json", [])
    conversations = {}
    
    for msg in messages:
        if msg['sender'] == user_email or msg['recipient'] == user_email:
            other = msg['recipient'] if msg['sender'] == user_email else msg['sender']
            if other not in conversations:
                conversations[other] = []
            conversations[other].append(msg)
    
    for conv in conversations:
        conversations[conv].sort(key=lambda x: x['timestamp'])
    
    return conversations

def get_unread_count(user_email, school_code):
    """Get number of unread messages for a user"""
    messages = load_school_data(school_code, "messages.json", [])
    return len([m for m in messages if m['recipient'] == user_email and not m['read']])

def mark_as_read(message_id, school_code):
    """Mark a message as read"""
    messages = load_school_data(school_code, "messages.json", [])
    for msg in messages:
        if msg['id'] == message_id:
            msg['read'] = True
            break
    save_school_data(school_code, "messages.json", messages)

# ============ SESSION STATE ============
if 'user' not in st.session_state:
    st.session_state.user = None
if 'current_school' not in st.session_state:
    st.session_state.current_school = None
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'menu_index' not in st.session_state:
    st.session_state.menu_index = 0
if 'chat_with' not in st.session_state:
    st.session_state.chat_with = None

# ============ MAIN APP ============

# ----- WELCOME PAGE -----
if st.session_state.page == 'welcome':
    st.markdown('<h1 class="radiant-title">✨ School Community Hub ✨</h1>', unsafe_allow_html=True)
    st.markdown('<p class="radiant-subtitle">Connect • Collaborate • Shine Together</p>', unsafe_allow_html=True)
    st.divider()
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["👑 Admin", "🏫 Create", "👨‍🏫 Teachers", "👨‍🎓 Students", "👪 Guardians"])
    
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
            <div style="background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border: 3px solid gold; border-radius: 30px; padding: 2rem; text-align: center;">
                <h3 style="color: gold;">👑 Admin Powers</h3>
                <p style="color: white;">Full control over your school</p>
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
                            "stats": {"students":0, "teachers":0, "guardians":0, "classes":0, "groups":0}
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
                        save_school_data(code, "guardians.json", [])
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
                        save_school_data(code, "messages.json", [])
                        
                        st.session_state.current_school = new_school
                        st.session_state.user = users[0]
                        st.session_state.page = 'dashboard'
                        st.success(f"✨ School Created! Your Code: **{code}**")
                        st.rerun()
        with col2:
            st.markdown("""
            <div style="background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border: 3px solid gold; border-radius: 30px; padding: 2rem; text-align: center;">
                <h3 style="color: gold;">🎓 Begin Your Legacy</h3>
                <p style="color: white;">Create your school community</p>
            </div>
            """, unsafe_allow_html=True)
    
    # TAB 3: TEACHER LOGIN & REGISTER
    with tab3:
        subtab1, subtab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with subtab1:
            col1, col2 = st.columns([1,1])
            with col1:
                with st.form("teacher_login"):
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
        
        with subtab2:
            col1, col2 = st.columns([1,1])
            with col1:
                with st.form("teacher_register"):
                    st.subheader("📝 New Teacher")
                    school_code = st.text_input("🏫 School Code", key="reg_school")
                    teacher_code = st.text_input("🔑 Teacher Code", placeholder="e.g., MATH-DEPT")
                    fullname = st.text_input("👤 Full Name")
                    email = st.text_input("📧 Email", key="reg_email")
                    password = st.text_input("🔐 Password", type="password", key="reg_pass")
                    confirm = st.text_input("🔐 Confirm", type="password", key="reg_confirm")
                    
                    if st.form_submit_button("✅ REGISTER", use_container_width=True):
                        if not all([school_code, teacher_code, fullname, email, password]):
                            st.error("All fields required")
                        elif password != confirm:
                            st.error("Passwords don't match")
                        else:
                            all_schools = load_all_schools()
                            if school_code not in all_schools:
                                st.error("School not found")
                            else:
                                school = all_schools[school_code]
                                users = load_school_data(school_code, "users.json", [])
                                
                                if any(u['email'] == email for u in users):
                                    st.error("❌ Email already registered!")
                                    st.stop()
                                
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
                                
                                new_user = {
                                    "user_id": generate_id("USR"),
                                    "email": email,
                                    "fullname": fullname,
                                    "password": hashlib.sha256(password.encode()).hexdigest(),
                                    "role": "teacher",
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
                                st.success("✅ Registration Successful!")
                                st.rerun()
    
    # TAB 4: STUDENT LOGIN & REGISTER
    with tab4:
        subtab1, subtab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with subtab1:
            col1, col2 = st.columns([1,1])
            with col1:
                with st.form("student_login"):
                    st.subheader("👨‍🎓 Student Login")
                    school_code = st.text_input("🏫 School Code")
                    admission_number = st.text_input("🎫 Admission Number")
                    password = st.text_input("🔐 Password", type="password")
                    if st.form_submit_button("✨ LOGIN ✨", use_container_width=True):
                        if not school_code or not admission_number or not password:
                            st.error("All fields required")
                        else:
                            all_schools = load_all_schools()
                            if school_code in all_schools:
                                school = all_schools[school_code]
                                users = load_school_data(school_code, "users.json", [])
                                hashed = hashlib.sha256(password.encode()).hexdigest()
                                for u in users:
                                    if u.get('admission_number') == admission_number and u['password'] == hashed and u['role'] == 'student':
                                        st.session_state.current_school = school
                                        st.session_state.user = u
                                        st.session_state.page = 'dashboard'
                                        st.rerun()
                                st.error("Invalid admission number or password")
                            else:
                                st.error("School not found")
        
        with subtab2:
            col1, col2 = st.columns([1,1])
            with col1:
                with st.form("student_register"):
                    st.subheader("📝 New Student")
                    school_code = st.text_input("🏫 School Code", key="stud_school")
                    fullname = st.text_input("👤 Full Name")
                    email = st.text_input("📧 Email (Optional)")
                    password = st.text_input("🔐 Password", type="password", key="stud_pass")
                    confirm = st.text_input("🔐 Confirm", type="password", key="stud_confirm")
                    
                    if st.form_submit_button("✅ REGISTER", use_container_width=True):
                        if not all([school_code, fullname, password]):
                            st.error("School code, name and password required")
                        elif password != confirm:
                            st.error("Passwords don't match")
                        else:
                            all_schools = load_all_schools()
                            if school_code not in all_schools:
                                st.error("School not found")
                            else:
                                school = all_schools[school_code]
                                users = load_school_data(school_code, "users.json", [])
                                
                                if email and any(u['email'] == email for u in users):
                                    st.error("❌ Email already registered!")
                                    st.stop()
                                
                                admission_number = generate_admission_number()
                                while any(u.get('admission_number') == admission_number for u in users):
                                    admission_number = generate_admission_number()
                                
                                new_user = {
                                    "user_id": generate_id("USR"),
                                    "email": email if email else "",
                                    "fullname": fullname,
                                    "password": hashlib.sha256(password.encode()).hexdigest(),
                                    "role": "student",
                                    "joined": datetime.now().strftime("%Y-%m-%d"),
                                    "school_code": school_code,
                                    "classes": [],
                                    "groups": [],
                                    "admission_number": admission_number,
                                    "guardians": []
                                }
                                users.append(new_user)
                                save_school_data(school_code, "users.json", users)
                                school['stats']['students'] += 1
                                all_schools[school_code] = school
                                save_all_schools(all_schools)
                                
                                st.success(f"✅ Registered! Your Admission Number: **{admission_number}**")
                                st.info("📝 Save this number - you'll need it to login!")
    
    # TAB 5: GUARDIAN LOGIN & REGISTER
    with tab5:
        subtab1, subtab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with subtab1:
            col1, col2 = st.columns([1,1])
            with col1:
                with st.form("guardian_login"):
                    st.subheader("👪 Guardian Login")
                    school_code = st.text_input("🏫 School Code")
                    student_admission = st.text_input("🎫 Student's Admission Number")
                    email = st.text_input("📧 Your Email")
                    password = st.text_input("🔐 Password", type="password")
                    if st.form_submit_button("✨ LOGIN ✨", use_container_width=True):
                        if not school_code or not student_admission or not email or not password:
                            st.error("All fields required")
                        else:
                            all_schools = load_all_schools()
                            if school_code in all_schools:
                                school = all_schools[school_code]
                                users = load_school_data(school_code, "users.json", [])
                                hashed = hashlib.sha256(password.encode()).hexdigest()
                                for u in users:
                                    if u['role'] == 'guardian' and u['email'] == email and u['password'] == hashed:
                                        if student_admission in u.get('linked_students', []):
                                            st.session_state.current_school = school
                                            st.session_state.user = u
                                            st.session_state.page = 'dashboard'
                                            st.rerun()
                                        else:
                                            st.error("You are not linked to this student")
                                            break
                                st.error("Invalid credentials")
                            else:
                                st.error("School not found")
        
        with subtab2:
            col1, col2 = st.columns([1,1])
            with col1:
                with st.form("guardian_register"):
                    st.subheader("📝 New Guardian")
                    st.info("You'll need the student's admission number")
                    school_code = st.text_input("🏫 School Code", key="guard_school")
                    student_admission = st.text_input("🎫 Student's Admission Number")
                    fullname = st.text_input("👤 Your Full Name")
                    email = st.text_input("📧 Your Email")
                    phone = st.text_input("📱 Phone Number")
                    password = st.text_input("🔐 Password", type="password", key="guard_pass")
                    confirm = st.text_input("🔐 Confirm", type="password", key="guard_confirm")
                    
                    if st.form_submit_button("✅ REGISTER", use_container_width=True):
                        if not all([school_code, student_admission, fullname, email, password]):
                            st.error("All fields required")
                        elif password != confirm:
                            st.error("Passwords don't match")
                        else:
                            all_schools = load_all_schools()
                            if school_code not in all_schools:
                                st.error("School not found")
                            else:
                                school = all_schools[school_code]
                                users = load_school_data(school_code, "users.json", [])
                                
                                if any(u['email'] == email for u in users):
                                    st.error("❌ Email already registered!")
                                    st.stop()
                                
                                student = None
                                for u in users:
                                    if u.get('admission_number') == student_admission and u['role'] == 'student':
                                        student = u
                                        break
                                
                                if not student:
                                    st.error("❌ Student not found with this admission number!")
                                    st.stop()
                                
                                new_user = {
                                    "user_id": generate_id("USR"),
                                    "email": email,
                                    "fullname": fullname,
                                    "phone": phone,
                                    "password": hashlib.sha256(password.encode()).hexdigest(),
                                    "role": "guardian",
                                    "joined": datetime.now().strftime("%Y-%m-%d"),
                                    "school_code": school_code,
                                    "linked_students": [student_admission]
                                }
                                users.append(new_user)
                                
                                if 'guardians' not in student:
                                    student['guardians'] = []
                                student['guardians'].append(email)
                                
                                save_school_data(school_code, "users.json", users)
                                school['stats']['guardians'] = school['stats'].get('guardians', 0) + 1
                                all_schools[school_code] = school
                                save_all_schools(all_schools)
                                
                                st.success("✅ Guardian Registration Successful!")

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
    
    unread_count = get_unread_count(user['email'], school_code)
    
    # ============ SIDEBAR ============
    with st.sidebar:
        st.markdown(f"""
        <div class="school-header">
            <h2>{school['name']}</h2>
            <div class="school-code">
                <code>{school['code']}</code>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        if user.get('profile_pic'):
            st.image(user['profile_pic'], width=50)
        else:
            emoji = "👑" if user['role'] == 'admin' else "👨‍🏫" if user['role'] == 'teacher' else "👨‍🎓" if user['role'] == 'student' else "👪"
            st.markdown(f"<h1 style='font-size: 2rem; margin: 0;'>{emoji}</h1>", unsafe_allow_html=True)
        
        role_display = "ADMIN" if user['role'] == 'admin' else "TEACHER" if user['role'] == 'teacher' else "STUDENT" if user['role'] == 'student' else "GUARDIAN"
        
        st.markdown(f"""
        <div style="color: white; flex: 1;">
            <strong>{user['fullname']}</strong><br>
            <span style="background: rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 20px; font-size: 0.7rem;">{role_display}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        
        # Navigation
        if user['role'] == 'admin':
            options = ["Dashboard", "Teachers", "Classes", "Students", "Guardians", f"Chat💬{f'({unread_count})' if unread_count>0 else ''}", "Profile"]
        elif user['role'] == 'teacher':
            options = ["Dashboard", "My Classes", "Assignments", f"Chat💬{f'({unread_count})' if unread_count>0 else ''}", "Profile"]
        elif user['role'] == 'student':
            options = ["Dashboard", "Browse Classes", "Homework", f"Chat💬{f'({unread_count})' if unread_count>0 else ''}", "Profile"]
        else:
            options = ["Dashboard", "My Student", f"Chat💬{f'({unread_count})' if unread_count>0 else ''}", "Profile"]
        
        menu = st.radio("", options, index=st.session_state.menu_index, label_visibility="collapsed")
        st.session_state.menu_index = options.index(menu)
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.current_school = None
            st.session_state.page = 'welcome'
            st.rerun()
    
    # ============ MAIN CONTENT ============
    
    # ----- CHAT SECTION -----
    if menu.startswith("Chat"):
        st.markdown("<h2 style='text-align: center;'>💬 Messages</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Conversations**")
            conversations = get_conversations(user['email'], school_code)
            
            if conversations:
                for other_email, msgs in conversations.items():
                    other_user = next((u for u in users if u['email'] == other_email), None)
                    if other_user:
                        other_name = other_user['fullname']
                        other_role = other_user['role']
                        conv_unread = len([m for m in msgs if m['recipient'] == user['email'] and not m['read']])
                        
                        if st.button(f"{'👑 ' if other_role=='admin' else '👨‍🏫 ' if other_role=='teacher' else '👨‍🎓 ' if other_role=='student' else '👪 '}{other_name}{f' ({conv_unread})' if conv_unread>0 else ''}", key=f"chat_{other_email}", use_container_width=True):
                            st.session_state.chat_with = other_email
                            st.rerun()
            else:
                st.info("No conversations")
        
        with col2:
            if st.session_state.chat_with:
                other_email = st.session_state.chat_with
                other_user = next((u for u in users if u['email'] == other_email), None)
                
                if other_user:
                    st.markdown(f"**Chat with {other_user['fullname']}**")
                    
                    conv_id = f"{min(user['email'], other_email)}_{max(user['email'], other_email)}"
                    messages = load_school_data(school_code, "messages.json", [])
                    conv_msgs = [m for m in messages if m['conversation_id'] == conv_id]
                    conv_msgs.sort(key=lambda x: x['timestamp'])
                    
                    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
                    for msg in conv_msgs:
                        if msg['recipient'] == user['email'] and not msg['read']:
                            mark_as_read(msg['id'], school_code)
                        
                        msg_class = "sent" if msg['sender'] == user['email'] else "received"
                        st.markdown(f"""
                        <div class="chat-message {msg_class}">
                            <div class="chat-sender">{'You' if msg['sender'] == user['email'] else other_user['fullname']}</div>
                            <div>{msg['message']}</div>
                            <div class="chat-time">{msg['timestamp']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    with st.form("send_message"):
                        message = st.text_area("Message", height=80)
                        if st.form_submit_button("📤 Send", use_container_width=True):
                            if message:
                                send_message(users, user['email'], other_email, message, school_code)
                                st.rerun()
            else:
                st.info("Select a conversation")
    
    # ----- ADMIN -----
    elif user['role'] == 'admin':
        if menu == "Dashboard":
            st.markdown(f"<h2 style='text-align: center;'>👑 {school['name']}</h2>", unsafe_allow_html=True)
            col1,col2,col3,col4 = st.columns(4)
            col1.metric("Students", school['stats'].get('students',0))
            col2.metric("Teachers", school['stats'].get('teachers',0))
            col3.metric("Guardians", school['stats'].get('guardians',0))
            col4.metric("Classes", school['stats'].get('classes',0))
            
            pending = len([r for r in class_requests if r['status']=='pending']) + len([r for r in group_requests if r['status']=='pending'])
            if pending > 0:
                st.warning(f"📌 {pending} pending requests")
        
        elif menu == "Teachers":
            st.markdown("<h2 style='text-align: center;'>👨‍🏫 Teachers</h2>", unsafe_allow_html=True)
            with st.form("create_teacher_code"):
                name = st.text_input("Code Name", placeholder="Mathematics Dept")
                code = st.text_input("Custom Code", placeholder="MATH-DEPT")
                if st.form_submit_button("✨ Create"):
                    if name and code:
                        if any(t['code'] == code.upper() for t in teachers_data):
                            st.error("Code exists")
                        else:
                            teachers_data.append({
                                "id": generate_id("TCH"),
                                "name": name,
                                "code": code.upper(),
                                "created": datetime.now().strftime("%Y-%m-%d"),
                                "status": "active",
                                "used_by_list": []
                            })
                            save_school_data(school_code, "teachers.json", teachers_data)
                            st.success(f"Code {code.upper()} created")
                            st.rerun()
    
    # ----- TEACHER -----
    elif user['role'] == 'teacher':
        if menu == "Dashboard":
            st.markdown(f"<h2 style='text-align: center;'>👨‍🏫 {user['fullname']}</h2>", unsafe_allow_html=True)
            my_classes = [c for c in classes if c.get('teacher') == user['email']]
            st.metric("My Classes", len(my_classes))
    
    # ----- STUDENT -----
    elif user['role'] == 'student':
        if menu == "Dashboard":
            st.markdown(f"<h2 style='text-align: center;'>👨‍🎓 {user['fullname']}</h2>", unsafe_allow_html=True)
            st.info(f"Admission: **{user['admission_number']}**")
            
            my_classes = [c for c in classes if user['email'] in c.get('students', [])]
            st.metric("My Classes", len(my_classes))
    
    # ----- GUARDIAN -----
    else:
        if menu == "Dashboard":
            st.markdown(f"<h2 style='text-align: center;'>👪 {user['fullname']}</h2>", unsafe_allow_html=True)
            for adm in user.get('linked_students', []):
                student = next((u for u in users if u.get('admission_number') == adm), None)
                if student:
                    st.write(f"**{student['fullname']}**")

else:
    st.error("Something went wrong")
    if st.button("Restart"):
        st.session_state.page = 'welcome'
        st.rerun()
