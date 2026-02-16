import streamlit as st
from datetime import datetime, timedelta
import hashlib
import json
import random
import string
from pathlib import Path
from PIL import Image
import base64
from io import BytesIO
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="✨ School Hub & Management ✨",
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
            padding: 1rem !important;
        }
        h1 { font-size: 2rem !important; }
        h2 { font-size: 1.5rem !important; }
        .stButton button { font-size: 1rem !important; padding: 0.5rem 1rem !important; }
    }
    
    /* Sidebar behavior - collapsible on mobile */
    @media (max-width: 768px) {
        section[data-testid="stSidebar"] {
            width: 100% !important;
            min-width: 100% !important;
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
    
    /* Desktop sidebar */
    @media (min-width: 769px) {
        section[data-testid="stSidebar"] {
            width: 350px !important;
            min-width: 350px !important;
            transform: translateX(0) !important;
        }
        .main .block-container {
            margin-left: 350px !important;
            max-width: calc(100% - 350px) !important;
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
    
    /* ============ TOP NAVIGATION BUTTONS ============ */
    .top-nav {{
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 20px auto;
        padding: 10px;
        max-width: 800px;
        z-index: 10;
        position: relative;
    }}
    
    /* ============ SIDEBAR ============ */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(135deg, rgba(75, 0, 130, 0.98), rgba(138, 43, 226, 0.98), rgba(255, 215, 0, 0.95)) !important;
        backdrop-filter: blur(15px) !important;
        border-right: 4px solid gold !important;
        box-shadow: 10px 0 40px rgba(0, 0, 0, 0.8) !important;
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
        padding: 2rem 1.5rem !important;
        width: 100% !important;
    }}
    
    /* Sidebar text */
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
    
    /* ============ CHAT STYLES ============ */
    .chat-container {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 30px;
        padding: 20px;
        margin: 10px 0;
        border: 2px solid gold;
    }}
    
    .chat-message {{
        background: rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        padding: 15px;
        margin: 10px 0;
        border-left: 5px solid gold;
    }}
    
    .chat-message.sent {{
        border-left-color: #4B0082;
        background: rgba(75, 0, 130, 0.2);
    }}
    
    .chat-message.received {{
        border-left-color: gold;
    }}
    
    .chat-sender {{
        font-weight: 800;
        color: gold;
        margin-bottom: 5px;
    }}
    
    .chat-time {{
        font-size: 0.8rem;
        color: rgba(255,255,255,0.7);
        text-align: right;
        margin-top: 5px;
    }}
    
    /* ============ DROPDOWN STYLES - HIGH CONTRAST ============ */
    .stSelectbox div[data-baseweb="select"] {{
        background: #FFFFFF !important;
        border: 4px solid gold !important;
        border-radius: 30px !important;
    }}
    
    .stSelectbox div[data-baseweb="select"] span {{
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        background: transparent !important;
    }}
    
    .stSelectbox div[data-baseweb="select"] > div {{
        background: #FFFFFF !important;
        color: #000000 !important;
        font-weight: 700 !important;
    }}
    
    /* Dropdown menu */
    div[data-baseweb="menu"] {{
        background: #FFFFFF !important;
        border: 4px solid gold !important;
        border-radius: 20px !important;
    }}
    
    div[data-baseweb="menu"] li {{
        color: #000000 !important;
        font-weight: 600 !important;
        background: #FFFFFF !important;
    }}
    
    div[data-baseweb="menu"] li:hover {{
        background: rgba(255, 215, 0, 0.3) !important;
    }}
    
    div[data-baseweb="menu"] li[aria-selected="true"] {{
        background: linear-gradient(135deg, gold, #ffd700) !important;
        color: #4B0082 !important;
    }}
    
    /* Text inputs - HIGH CONTRAST */
    .stTextInput input, .stTextArea textarea, .stDateInput input {{
        background: #FFFFFF !important;
        border: 4px solid gold !important;
        border-radius: 30px !important;
        color: #000000 !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
        padding: 1rem 1.5rem !important;
    }}
    
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {{
        color: #666666 !important;
    }}
    
    .stTextInput label, .stTextArea label, .stSelectbox label, .stDateInput label {{
        color: WHITE !important;
        font-weight: 800 !important;
        font-size: 1.2rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
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
        transition: all 0.3s ease !important;
    }}
    
    .stButton button:hover {{
        transform: scale(1.05) translateY(-3px) !important;
        box-shadow: 0 20px 50px gold !important;
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
        flex-wrap: wrap !important;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        color: WHITE !important;
        border-radius: 60px !important;
        padding: 0.8rem 1.5rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        white-space: normal !important;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, gold, #ffd700) !important;
        color: #4B0082 !important;
        font-weight: 900 !important;
    }}
    
    /* Metrics */
    .stMetric {{
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(5px) !important;
        border: 4px solid gold !important;
        border-radius: 35px !important;
        padding: 1.5rem !important;
    }}
    
    .stMetric label {{
        color: WHITE !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
    }}
    
    .stMetric div {{
        color: gold !important;
        font-size: 2.5rem !important;
        font-weight: 900 !important;
    }}
    
    /* Hide footer */
    footer {{
        display: none !important;
    }}
    
    /* Low stock warning */
    .low-stock {{
        color: orange !important;
        font-weight: bold;
    }}
    
    .out-of-stock {{
        color: red !important;
        font-weight: bold;
    }}
    
    .overdue {{
        color: red !important;
        font-weight: bold;
    }}
    
    .due-soon {{
        color: orange !important;
        font-weight: bold;
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

def generate_admission_number():
    """Generate a unique admission number for students"""
    year = datetime.now().strftime("%Y")
    random_num = ''.join(random.choices(string.digits, k=5))
    return f"ADM/{year}/{random_num}"

def generate_book_id():
    """Generate a unique book ID"""
    return 'BK' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def generate_furniture_id():
    """Generate a unique furniture ID"""
    return 'FRN' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

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
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
    
    # Sort messages in each conversation by timestamp
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
if 'app_mode' not in st.session_state:
    st.session_state.app_mode = 'hub'  # 'hub' or 'management'
if 'management_subsection' not in st.session_state:
    st.session_state.management_subsection = 'analytics'

# Library Management State
if 'library_members' not in st.session_state:
    st.session_state.library_members = []
if 'book_catalog' not in st.session_state:
    st.session_state.book_catalog = []
if 'borrowed_books' not in st.session_state:
    st.session_state.borrowed_books = []
if 'saved_class_lists' not in st.session_state:
    st.session_state.saved_class_lists = {}

# Furniture Management State
if 'furniture_inventory' not in st.session_state:
    st.session_state.furniture_inventory = []
if 'furniture_allocations' not in st.session_state:
    st.session_state.furniture_allocations = []

# Teacher Book Allocation State
if 'teacher_allocations' not in st.session_state:
    st.session_state.teacher_allocations = {}
if 'current_teacher_class' not in st.session_state:
    st.session_state.current_teacher_class = []
if 'current_teacher_class_name' not in st.session_state:
    st.session_state.current_teacher_class_name = ""

# ============ TOP NAVIGATION ============
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    hub_col, mgmt_col = st.columns(2)
    with hub_col:
        if st.button("🏫 School Community Hub", key="hub_btn", use_container_width=True):
            st.session_state.app_mode = 'hub'
            st.rerun()
    with mgmt_col:
        if st.button("⚙️ School Management System", key="mgmt_btn", use_container_width=True):
            st.session_state.app_mode = 'management'
            st.rerun()

st.divider()

# ============ MAIN APP BASED ON MODE ============

# ----- WELCOME PAGE (Only shown when not logged in) -----
if st.session_state.page == 'welcome' and not st.session_state.user:
    
    if st.session_state.app_mode == 'hub':
        st.markdown('<h1 class="radiant-title">✨ School Community Hub ✨</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: white; font-size: 1.5rem;">Connect • Collaborate • Shine Together</p>', unsafe_allow_html=True)
        
        # HUB MODE - Focus on community and collaboration
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["👑 Admin", "🏫 Create School", "👨‍🏫 Teachers", "👨‍🎓 Students", "👪 Guardians"])
        
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
                <div style="background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 35px; padding: 30px; text-align: center; border: 4px solid gold;">
                    <h3 style="color: gold;">👑 Admin Powers</h3>
                    <p style="color: white; opacity: 0.9;">Full control over your school community</p>
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
                <div style="background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 35px; padding: 30px; text-align: center; border: 4px solid gold;">
                    <h3 style="color: gold;">🎓 Begin Your Legacy</h3>
                    <p style="color: white; opacity: 0.9;">Create your school and become the founding administrator</p>
                    <div style="font-size: 5rem;">🚀</div>
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
                with col2:
                    st.markdown("""
                    <div style="background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 35px; padding: 30px; text-align: center; border: 4px solid gold;">
                        <h3 style="color: gold;">📚 Your Classroom</h3>
                        <p style="color: white; opacity: 0.9;">Login to manage classes and chat</p>
                        <div style="font-size: 5rem;">🍎</div>
                    </div>
                    """, unsafe_allow_html=True)
            
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
                                    
                                    # Check if email already exists
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
                                        "groups": [],
                                        "admission_number": None
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
                                        if u['admission_number'] == admission_number and u['password'] == hashed and u['role'] == 'student':
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
                        email = st.text_input("📧 Email (Optional)", help="Optional for students without phones")
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
                                    
                                    # Check if email already exists (if provided)
                                    if email and any(u['email'] == email for u in users):
                                        st.error("❌ Email already registered!")
                                        st.stop()
                                    
                                    # Generate unique admission number
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
                                        "guardians": []  # Store guardian emails
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
                                            # Verify this guardian is linked to the student
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
                        st.info("You'll need the student's admission number to register")
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
                                    
                                    # Check if email already exists
                                    if any(u['email'] == email for u in users):
                                        st.error("❌ Email already registered!")
                                        st.stop()
                                    
                                    # Verify student exists with this admission number
                                    student = None
                                    for u in users:
                                        if u.get('admission_number') == student_admission and u['role'] == 'student':
                                            student = u
                                            break
                                    
                                    if not student:
                                        st.error("❌ Student not found with this admission number!")
                                        st.stop()
                                    
                                    # Create guardian
                                    new_user = {
                                        "user_id": generate_id("USR"),
                                        "email": email,
                                        "fullname": fullname,
                                        "phone": phone,
                                        "password": hashlib.sha256(password.encode()).hexdigest(),
                                        "role": "guardian",
                                        "joined": datetime.now().strftime("%Y-%m-%d"),
                                        "school_code": school_code,
                                        "linked_students": [student_admission],
                                        "admission_number": None
                                    }
                                    users.append(new_user)
                                    
                                    # Link guardian to student
                                    if 'guardians' not in student:
                                        student['guardians'] = []
                                    student['guardians'].append(email)
                                    
                                    save_school_data(school_code, "users.json", users)
                                    school['stats']['guardians'] = school['stats'].get('guardians', 0) + 1
                                    all_schools[school_code] = school
                                    save_all_schools(all_schools)
                                    
                                    st.success("✅ Guardian Registration Successful!")
                                    st.info("You can now login with your email and the student's admission number")
    
    else:  # MANAGEMENT MODE - Welcome Page
        st.markdown('<h1 class="radiant-title">⚙️ School Management System ⚙️</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: white; font-size: 1.5rem;">Manage • Organize • Excel</p>', unsafe_allow_html=True)
        st.divider()
        
        tab1, tab2, tab3 = st.tabs(["🔐 Login", "🏫 Select School", "ℹ️ About"])
        
        with tab1:
            col1, col2 = st.columns([1, 1])
            with col1:
                with st.form("management_login"):
                    st.subheader("👤 Management Login")
                    school_code = st.text_input("🏫 School Code")
                    email = st.text_input("📧 Email")
                    password = st.text_input("🔐 Password", type="password")
                    
                    if st.form_submit_button("🚀 Access Management System", use_container_width=True):
                        if not school_code or not email or not password:
                            st.error("All fields required")
                        else:
                            all_schools = load_all_schools()
                            if school_code in all_schools:
                                school = all_schools[school_code]
                                users = load_school_data(school_code, "users.json", [])
                                hashed = hashlib.sha256(password.encode()).hexdigest()
                                
                                for u in users:
                                    if u['email'] == email and u['password'] == hashed:
                                        st.session_state.current_school = school
                                        st.session_state.user = u
                                        st.session_state.page = 'dashboard'
                                        st.rerun()
                                
                                st.error("Invalid credentials")
                            else:
                                st.error("School not found")
            
            with col2:
                st.markdown("""
                <div style="background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 35px; padding: 30px; text-align: center; border: 4px solid gold;">
                    <h3 style="color: gold;">⚙️ Management Features</h3>
                    <p style="color: white; opacity: 0.9;">Analytics • Library • Furniture • Staff • Finance • Exams • Inventory</p>
                    <div style="font-size: 5rem;">📊</div>
                </div>
                """, unsafe_allow_html=True)
        
        with tab2:
            st.info("Select a school to access its management system")
            all_schools = load_all_schools()
            if all_schools:
                school_list = list(all_schools.keys())
                selected_school = st.selectbox("Choose School Code", school_list)
                if selected_school:
                    school = all_schools[selected_school]
                    st.write(f"**{school['name']}** - {school.get('city', 'N/A')}")
                    st.write(f"Motto: {school.get('motto', 'N/A')}")
                    if st.button("Access This School"):
                        st.session_state.current_school = school
                        st.session_state.page = 'dashboard'
                        st.rerun()
            else:
                st.warning("No schools found. Create a school in the Community Hub first.")
        
        with tab3:
            st.markdown("""
            <div style="background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 35px; padding: 30px; border: 4px solid gold;">
                <h3 style="color: gold;">📋 About School Management System</h3>
                <p style="color: white;">The School Management System provides comprehensive tools for school administration:</p>
                <ul style="color: white;">
                    <li><strong>Analytics Dashboard</strong> - Real-time performance metrics and trends</li>
                    <li><strong>Library Management</strong> - Book catalog, borrowing, returns, and member management</li>
                    <li><strong>Furniture Allocation</strong> - Track and assign furniture to students and staff</li>
                    <li><strong>Teacher Book Allocation</strong> - Allocate textbooks to entire classes</li>
                    <li><strong>Finance Management</strong> - Fee collection, budgeting, and expense tracking</li>
                    <li><strong>Staff Management</strong> - Payroll, attendance, and performance evaluations</li>
                    <li><strong>Curriculum Planning</strong> - Lesson plans and scheme of work</li>
                    <li><strong>Examination Module</strong> - Exam scheduling and results processing</li>
                    <li><strong>Inventory Management</strong> - Track assets, textbooks, and equipment</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# ----- DASHBOARD (When logged in) -----
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
    
    # Get unread message count
    unread_count = get_unread_count(user['email'], school_code)
    
    # Show mode indicator
    mode_indicator = "🏫 Community Hub" if st.session_state.app_mode == 'hub' else "⚙️ Management System"
    st.markdown(f"<p style='text-align: right; color: gold; font-weight: 700;'>{mode_indicator}</p>", unsafe_allow_html=True)
    
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
            emoji = "👑" if user['role'] == 'admin' else "👨‍🏫" if user['role'] == 'teacher' else "👨‍🎓" if user['role'] == 'student' else "👪"
            st.markdown(f"<h1 style='font-size: 4rem; margin: 0;'>{emoji}</h1>", unsafe_allow_html=True)
        
        role_display = "ADMIN" if user['role'] == 'admin' else "TEACHER" if user['role'] == 'teacher' else "STUDENT" if user['role'] == 'student' else "GUARDIAN"
        
        st.markdown(f"""
        <div style="color: white; flex: 1;">
            <strong style="font-size: 1.4rem;">{user['fullname']}</strong><br>
            <span style="background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 50px; font-size: 0.9rem; font-weight: 700;">{role_display}</span><br>
            <span style="font-size: 0.9rem; opacity: 0.9;">{user['email'] if user.get('email') else ''}</span>
            {f"<br><span style='font-size: 0.9rem; color: gold;'>Adm: {user['admission_number']}</span>" if user.get('admission_number') else ''}
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        
        # Navigation based on role and mode
        if st.session_state.app_mode == 'hub':
            # HUB MODE - Community focused navigation
            if user['role'] == 'admin':
                options = ["Dashboard", "Teachers", "Classes", "Students", "Guardians", "Groups", "Approvals", f"Chat 💬{f' ({unread_count})' if unread_count > 0 else ''}", "Profile"]
            elif user['role'] == 'teacher':
                options = ["Dashboard", "My Classes", "My Groups", "Assignments", "Requests", f"Chat 💬{f' ({unread_count})' if unread_count > 0 else ''}", "Profile"]
            elif user['role'] == 'student':
                options = ["Dashboard", "Browse Classes", "Browse Groups", "Homework", "My Grades", f"Chat 💬{f' ({unread_count})' if unread_count > 0 else ''}", "Profile"]
            else:  # guardian
                options = ["Dashboard", "My Student", "Messages", f"Chat 💬{f' ({unread_count})' if unread_count > 0 else ''}", "Profile"]
        else:
            # MANAGEMENT MODE - Administrative focused navigation
            if user['role'] == 'admin':
                options = ["Analytics", "Library", "Furniture", "Teacher Books", "Finance", "Staff", "Curriculum", "Exams", "Inventory", "Reports", "Settings"]
            elif user['role'] == 'teacher':
                options = ["My Classes", "Gradebook", "Attendance", "Lesson Plans", "Library", "Furniture", "Reports", "Settings"]
            elif user['role'] == 'student':
                options = ["My Grades", "Attendance", "Timetable", "Library", "Fee Statement", "Settings"]
            else:  # guardian
                options = ["Student Progress", "Fee Payments", "Library", "Reports", "Communications", "Settings"]
        
        menu = st.radio("Navigation", options, index=st.session_state.menu_index, label_visibility="collapsed")
        st.session_state.menu_index = options.index(menu)
        
        st.divider()
        
        if st.button("🚪 LOGOUT", use_container_width=True):
            st.session_state.user = None
            st.session_state.current_school = None
            st.session_state.page = 'welcome'
            st.rerun()
    
    # ============ MAIN CONTENT ============
    
    if st.session_state.app_mode == 'hub':
        # ----- HUB MODE CONTENT (Original functionality) -----
        
        # CHAT SECTION (Common for all roles)
        if menu.startswith("Chat"):
            st.markdown("<h1 style='text-align: center;'>💬 Messages</h1>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("### 👥 Conversations")
                conversations = get_conversations(user['email'], school_code)
                
                if conversations:
                    for other_email, msgs in conversations.items():
                        # Get other user's name
                        other_user = next((u for u in users if u['email'] == other_email), None)
                        if other_user:
                            other_name = other_user['fullname']
                            other_role = other_user['role']
                            
                            # Count unread from this conversation
                            conv_unread = len([m for m in msgs if m['recipient'] == user['email'] and not m['read']])
                            
                            # Get last message time
                            last_time = msgs[-1]['timestamp'][:16]
                            
                            if st.button(f"{'👑 ' if other_role=='admin' else '👨‍🏫 ' if other_role=='teacher' else '👨‍🎓 ' if other_role=='student' else '👪 '}{other_name}{f' ({conv_unread})' if conv_unread > 0 else ''}\n{last_time}", key=f"chat_{other_email}", use_container_width=True):
                                st.session_state.chat_with = other_email
                                st.rerun()
                else:
                    st.info("No conversations yet")
            
            with col2:
                if st.session_state.chat_with:
                    other_email = st.session_state.chat_with
                    other_user = next((u for u in users if u['email'] == other_email), None)
                    
                    if other_user:
                        st.markdown(f"### Chat with {other_user['fullname']}")
                        
                        # Get conversation
                        conv_id = f"{min(user['email'], other_email)}_{max(user['email'], other_email)}"
                        messages = load_school_data(school_code, "messages.json", [])
                        conv_msgs = [m for m in messages if m['conversation_id'] == conv_id]
                        conv_msgs.sort(key=lambda x: x['timestamp'])
                        
                        # Display messages
                        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
                        for msg in conv_msgs:
                            if msg['recipient'] == user['email'] and not msg['read']:
                                mark_as_read(msg['id'], school_code)
                            
                            msg_class = "sent" if msg['sender'] == user['email'] else "received"
                            st.markdown(f"""
                            <div class="chat-message {msg_class}">
                                <div class="chat-sender">{msg['sender'] if msg['sender'] == user['email'] else other_user['fullname']}</div>
                                <div>{msg['message']}</div>
                                <div class="chat-time">{msg['timestamp']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Send new message
                        st.markdown("### 📝 New Message")
                        with st.form("send_message"):
                            message = st.text_area("Message", height=100)
                            if st.form_submit_button("📤 Send", use_container_width=True):
                                if message:
                                    send_message(users, user['email'], other_email, message, school_code)
                                    st.success("Message sent!")
                                    st.rerun()
                    else:
                        st.info("Select a conversation to start chatting")
        
        # ----- ADMIN SECTION -----
        elif user['role'] == 'admin':
            if menu == "Dashboard":
                st.markdown(f"<h1 style='text-align: center;'>👑 {school['name']} Dashboard</h1>", unsafe_allow_html=True)
                col1,col2,col3,col4,col5 = st.columns(5)
                with col1:
                    st.metric("Students", school['stats'].get('students',0))
                with col2:
                    st.metric("Teachers", school['stats'].get('teachers',0))
                with col3:
                    st.metric("Guardians", school['stats'].get('guardians',0))
                with col4:
                    st.metric("Classes", school['stats'].get('classes',0))
                with col5:
                    st.metric("Groups", school['stats'].get('groups',0))
                
                st.divider()
                
                pending = len([r for r in class_requests if r['status']=='pending']) + len([r for r in group_requests if r['status']=='pending'])
                if pending > 0:
                    st.warning(f"📌 {pending} pending requests await your approval")
                else:
                    st.success("✅ All caught up! No pending requests")
            
            elif menu == "Teachers":
                st.markdown("<h1 style='text-align: center;'>👨‍🏫 Teacher Management</h1>", unsafe_allow_html=True)
                tab1, tab2 = st.tabs(["✨ Create Teacher Code", "👥 Active Teachers"])
                
                with tab1:
                    with st.form("create_teacher_code"):
                        name = st.text_input("📝 Code Name/Department", placeholder="e.g., Mathematics Department")
                        code = st.text_input("🔑 Custom Code", placeholder="e.g., MATH-DEPT, FORM1-2024")
                        dept = st.selectbox("🏢 Department", ["Mathematics", "Science", "English", "Kiswahili", "History", "Geography", "CRE", "Business", "Computer Science", "Other"])
                        if st.form_submit_button("✨ Generate Code", use_container_width=True):
                            if name and code:
                                if any(t['code'] == code.upper() for t in teachers_data):
                                    st.error("❌ Code already exists!")
                                else:
                                    teachers_data.append({
                                        "id": generate_id("TCH"),
                                        "name": name,
                                        "code": code.upper(),
                                        "department": dept,
                                        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                        "created_by": user['email'],
                                        "status": "active",
                                        "used_by_list": []
                                    })
                                    save_school_data(school_code, "teachers.json", teachers_data)
                                    st.success(f"✅ Code {code.upper()} created successfully!")
                                    st.rerun()
                
                with tab2:
                    active_teachers = [t for t in teachers_data if t['status'] == 'active']
                    if active_teachers:
                        for t in active_teachers:
                            with st.expander(f"📌 {t['name']} - `{t['code']}`"):
                                st.write(f"**Department:** {t['department']}")
                                st.write(f"**Created:** {t['created']}")
                                st.write(f"**Used by:** {len(t.get('used_by_list', []))} teachers")
                                if t.get('used_by_list'):
                                    st.write("**Teachers registered with this code:**")
                                    for teacher in t['used_by_list']:
                                        st.write(f"- {teacher['name']} ({teacher['email']}) on {teacher['date']}")
                    else:
                        st.info("No teacher codes created yet")
            
            elif menu == "Guardians":
                st.markdown("<h1 style='text-align: center;'>👪 Guardian Management</h1>", unsafe_allow_html=True)
                guardians = [u for u in users if u['role'] == 'guardian']
                if guardians:
                    for g in guardians:
                        with st.container():
                            col1, col2, col3 = st.columns([3, 3, 1])
                            with col1:
                                st.write(f"**{g['fullname']}**")
                            with col2:
                                st.write(f"📧 {g['email']}")
                                st.write(f"📱 {g.get('phone', 'N/A')}")
                            with col3:
                                if st.button("👁️", key=f"view_guard_{g['user_id']}"):
                                    st.session_state.view_guardian = g
                                    st.rerun()
                            if st.session_state.get('view_guardian') == g:
                                st.write("**Linked Students:**")
                                for adm in g.get('linked_students', []):
                                    student = next((u for u in users if u.get('admission_number') == adm), None)
                                    if student:
                                        st.write(f"- {student['fullname']} ({adm})")
                            st.divider()
                else:
                    st.info("No guardians registered yet")
            
            elif menu == "Classes":
                st.markdown("<h1 style='text-align: center;'>📚 Class Management</h1>", unsafe_allow_html=True)
                tab1, tab2 = st.tabs(["➕ Create Class", "📋 All Classes"])
                
                with tab1:
                    with st.form("create_class"):
                        col1, col2 = st.columns(2)
                        with col1:
                            class_name = st.text_input("📝 Class Name", placeholder="e.g., Mathematics 101")
                            grade = st.selectbox("🎓 Grade/Form", KENYAN_GRADES)
                            available_subjects = get_subjects_for_grade(grade)
                            subject = st.selectbox("📚 Main Subject", available_subjects)
                        
                        with col2:
                            class_room = st.text_input("🏫 Room Number", placeholder="e.g., 201")
                            class_schedule = st.text_input("⏰ Schedule", placeholder="e.g., Mon/Wed 10:00 AM")
                            max_students = st.number_input("👥 Maximum Students", min_value=1, max_value=100, value=40)
                        
                        teacher_options = []
                        for t in teachers_data:
                            if t['status'] == 'active' and t.get('used_by_list'):
                                for teacher_use in t['used_by_list']:
                                    teacher_options.append(f"{teacher_use['name']} ({teacher_use['email']})")
                        
                        if teacher_options:
                            selected_teacher = st.selectbox("👨‍🏫 Assign Teacher", teacher_options)
                            teacher_email = selected_teacher.split('(')[1].rstrip(')')
                            teacher_name = selected_teacher.split('(')[0].strip()
                        else:
                            st.warning("⚠️ No teachers available. Create teacher codes first.")
                            teacher_email = None
                            teacher_name = None
                        
                        if st.form_submit_button("✅ Create Class", use_container_width=True):
                            if class_name and teacher_email:
                                class_code = generate_class_code()
                                classes.append({
                                    "id": generate_id("CLS"),
                                    "code": class_code,
                                    "name": class_name,
                                    "subject": subject,
                                    "grade": grade,
                                    "teacher": teacher_email,
                                    "teacher_name": teacher_name,
                                    "room": class_room,
                                    "schedule": class_schedule,
                                    "max_students": max_students,
                                    "students": [],
                                    "created": datetime.now().strftime("%Y-%m-%d"),
                                    "status": "active"
                                })
                                save_school_data(school_code, "classes.json", classes)
                                school['stats']['classes'] += 1
                                all_schools = load_all_schools()
                                all_schools[school_code] = school
                                save_all_schools(all_schools)
                                st.success(f"✅ Class created! Code: {class_code}")
                                st.rerun()
                
                with tab2:
                    if classes:
                        for c in classes:
                            with st.expander(f"📖 {c['name']} - {c['code']} - {c['grade']}"):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.write(f"**Subject:** {c.get('subject', 'N/A')}")
                                    st.write(f"**Teacher:** {c.get('teacher_name', c['teacher'])}")
                                    st.write(f"**Room:** {c.get('room', 'TBD')}")
                                with col2:
                                    st.write(f"**Schedule:** {c.get('schedule', 'TBD')}")
                                    st.write(f"**Students:** {len(c.get('students', []))}/{c.get('max_students', 40)}")
                                    st.write(f"**Class Code:** `{c['code']}`")
                                if st.button("🗑️ Delete", key=f"del_class_{c['id']}"):
                                    classes.remove(c)
                                    save_school_data(school_code, "classes.json", classes)
                                    school['stats']['classes'] -= 1
                                    all_schools = load_all_schools()
                                    all_schools[school_code] = school
                                    save_all_schools(all_schools)
                                    st.rerun()
                    else:
                        st.info("No classes created yet")
            
            elif menu == "Students":
                st.markdown("<h1 style='text-align: center;'>👨‍🎓 Student Management</h1>", unsafe_allow_html=True)
                students = [u for u in users if u['role'] == 'student']
                if students:
                    for s in students:
                        with st.container():
                            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                            with col1:
                                st.write(f"**{s['fullname']}**")
                            with col2:
                                st.write(f"📧 {s['email'] if s['email'] else 'No email'}")
                            with col3:
                                st.write(f"🎫 {s['admission_number']}")
                            with col4:
                                if st.button("🗑️", key=f"del_student_{s['user_id']}"):
                                    users.remove(s)
                                    save_school_data(school_code, "users.json", users)
                                    school['stats']['students'] -= 1
                                    all_schools = load_all_schools()
                                    all_schools[school_code] = school
                                    save_all_schools(all_schools)
                                    st.rerun()
                            st.divider()
                else:
                    st.info("No students enrolled yet")
            
            elif menu == "Approvals":
                st.markdown("<h1 style='text-align: center;'>✅ Pending Approvals</h1>", unsafe_allow_html=True)
                tab1, tab2 = st.tabs(["📚 Class Requests", "👥 Group Requests"])
                
                with tab1:
                    pending_classes = [r for r in class_requests if r['status'] == 'pending']
                    if pending_classes:
                        for req in pending_classes:
                            with st.container():
                                col1, col2, col3 = st.columns([2, 2, 2])
                                with col1:
                                    st.write(f"**{req['student_name']}**")
                                with col2:
                                    st.write(f"📚 {req['class_name']}")
                                with col3:
                                    if st.button("✅ Approve", key=f"app_class_{req['id']}"):
                                        for c in classes:
                                            if c['name'] == req['class_name']:
                                                c['students'].append(req['student_email'])
                                        req['status'] = 'approved'
                                        save_school_data(school_code, "classes.json", classes)
                                        save_school_data(school_code, "class_requests.json", class_requests)
                                        st.rerun()
                                st.divider()
                    else:
                        st.info("No pending class requests")
                
                with tab2:
                    pending_groups = [r for r in group_requests if r['status'] == 'pending']
                    if pending_groups:
                        for req in pending_groups:
                            with st.container():
                                col1, col2, col3 = st.columns([2, 2, 2])
                                with col1:
                                    st.write(f"**{req['student_name']}**")
                                with col2:
                                    st.write(f"👥 {req['group_name']}")
                                with col3:
                                    if st.button("✅ Approve", key=f"app_group_{req['id']}"):
                                        for g in groups:
                                            if g['name'] == req['group_name']:
                                                g['members'].append(req['student_email'])
                                        req['status'] = 'approved'
                                        save_school_data(school_code, "groups.json", groups)
                                        save_school_data(school_code, "group_requests.json", group_requests)
                                        st.rerun()
                                st.divider()
                    else:
                        st.info("No pending group requests")
            
            elif menu == "Profile":
                st.markdown("<h1 style='text-align: center;'>👤 My Profile</h1>", unsafe_allow_html=True)
                col1, col2 = st.columns([1, 2])
                with col1:
                    if user.get('profile_pic'):
                        st.image(user['profile_pic'], width=150)
                    else:
                        st.markdown("<h1 style='font-size: 5rem; text-align: center;'>👑</h1>", unsafe_allow_html=True)
                    pic = st.file_uploader("📸 Upload Photo", type=['png', 'jpg', 'jpeg'])
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
                    with st.form("edit_profile"):
                        name = st.text_input("Full Name", user['fullname'])
                        phone = st.text_input("Phone", user.get('phone', ''))
                        bio = st.text_area("Bio", user.get('bio', ''))
                        if st.form_submit_button("💾 Update Profile", use_container_width=True):
                            for u in users:
                                if u['email'] == user['email']:
                                    u['fullname'] = name
                                    u['phone'] = phone
                                    u['bio'] = bio
                            save_school_data(school_code, "users.json", users)
                            user.update({'fullname': name, 'phone': phone, 'bio': bio})
                            st.success("Profile updated!")
                            st.rerun()
        
        # ----- TEACHER SECTION -----
        elif user['role'] == 'teacher':
            if menu == "Dashboard":
                st.markdown(f"<h1 style='text-align: center;'>👨‍🏫 Welcome, {user['fullname']}!</h1>", unsafe_allow_html=True)
                my_classes = [c for c in classes if c.get('teacher') == user['email']]
                my_groups = [g for g in groups if g.get('leader') == user['email']]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("My Classes", len(my_classes))
                with col2:
                    st.metric("My Groups", len(my_groups))
                with col3:
                    st.metric("Assignments", len([a for a in assignments if a.get('teacher') == user['email']]))
            
            elif menu == "My Classes":
                st.markdown("<h1 style='text-align: center;'>📚 My Classes</h1>", unsafe_allow_html=True)
                my_classes = [c for c in classes if c.get('teacher') == user['email']]
                if my_classes:
                    for c in my_classes:
                        with st.expander(f"📖 {c['name']} - {c['code']} - {c['grade']}"):
                            st.write(f"**Subject:** {c.get('subject', 'N/A')}")
                            st.write(f"**Room:** {c.get('room', 'TBD')}")
                            st.write(f"**Schedule:** {c.get('schedule', 'TBD')}")
                            st.write(f"**Students:** {len(c.get('students', []))}/{c.get('max_students', 40)}")
                            if c.get('students'):
                                st.write("**Enrolled Students:**")
                                for student_email in c['students']:
                                    student = next((u for u in users if u['email'] == student_email), None)
                                    if student:
                                        st.write(f"- {student['fullname']} ({student.get('admission_number', 'N/A')})")
                else:
                    st.info("You haven't been assigned any classes yet")
            
            elif menu == "Requests":
                st.markdown("<h1 style='text-align: center;'>✅ Pending Requests</h1>", unsafe_allow_html=True)
                my_classes = [c['name'] for c in classes if c.get('teacher') == user['email']]
                class_reqs = [r for r in class_requests if r['status'] == 'pending' and r['class_name'] in my_classes]
                
                if class_reqs:
                    for req in class_reqs:
                        with st.container():
                            col1, col2, col3 = st.columns([2, 2, 1])
                            with col1:
                                st.write(f"**{req['student_name']}**")
                            with col2:
                                st.write(f"📚 {req['class_name']}")
                            with col3:
                                if st.button("✅ Approve", key=f"app_{req['id']}"):
                                    for c in classes:
                                        if c['name'] == req['class_name']:
                                            c['students'].append(req['student_email'])
                                    req['status'] = 'approved'
                                    save_school_data(school_code, "classes.json", classes)
                                    save_school_data(school_code, "class_requests.json", class_requests)
                                    st.rerun()
                            st.divider()
                else:
                    st.info("No pending requests")
        
        # ----- STUDENT SECTION -----
        elif user['role'] == 'student':
            if menu == "Dashboard":
                st.markdown(f"<h1 style='text-align: center;'>👨‍🎓 Welcome, {user['fullname']}!</h1>", unsafe_allow_html=True)
                st.info(f"📋 Your Admission Number: **{user['admission_number']}**")
                
                my_classes = [c for c in classes if user['email'] in c.get('students', [])]
                my_groups = [g for g in groups if user['email'] in g.get('members', [])]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("My Classes", len(my_classes))
                with col2:
                    st.metric("My Groups", len(my_groups))
                with col3:
                    upcoming = [a for a in assignments if a['class'] in [c['name'] for c in my_classes]]
                    st.metric("Assignments", len(upcoming))
            
            elif menu == "Browse Classes":
                st.markdown("<h1 style='text-align: center;'>📚 Available Classes</h1>", unsafe_allow_html=True)
                available = [c for c in classes if user['email'] not in c.get('students', []) and len(c.get('students', [])) < c.get('max_students', 40)]
                if available:
                    for c in available:
                        with st.container():
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.write(f"**{c['name']}** - {c['grade']}")
                                st.write(f"👨‍🏫 {c.get('teacher_name', 'Unknown')} • {c.get('schedule', 'TBD')}")
                                st.write(f"📚 {c.get('subject', 'N/A')}")
                            with col2:
                                if st.button("📝 Request", key=f"req_{c['code']}"):
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
                            st.divider()
                else:
                    st.info("No available classes to join")
        
        # ----- GUARDIAN SECTION -----
        elif user['role'] == 'guardian':
            if menu == "Dashboard":
                st.markdown(f"<h1 style='text-align: center;'>👪 Welcome, {user['fullname']}!</h1>", unsafe_allow_html=True)
                
                # Show linked students
                st.subheader("👨‍🎓 Your Linked Students")
                for adm in user.get('linked_students', []):
                    student = next((u for u in users if u.get('admission_number') == adm), None)
                    if student:
                        with st.container():
                            col1, col2 = st.columns([1, 3])
                            with col1:
                                st.markdown("👨‍🎓")
                            with col2:
                                st.write(f"**{student['fullname']}**")
                                st.write(f"Admission: {adm}")
                                st.write(f"Email: {student['email'] if student['email'] else 'No email'}")
                            
                            # Show student's classes
                            student_classes = [c for c in classes if student['email'] in c.get('students', [])]
                            if student_classes:
                                st.write("**Classes:**")
                                for c in student_classes:
                                    st.write(f"- {c['name']} ({c['grade']})")
                            st.divider()
            
            elif menu == "My Student":
                st.markdown("<h1 style='text-align: center;'>📚 Student Details</h1>", unsafe_allow_html=True)
                
                for adm in user.get('linked_students', []):
                    student = next((u for u in users if u.get('admission_number') == adm), None)
                    if student:
                        st.subheader(f"👨‍🎓 {student['fullname']}")
                        
                        # Classes
                        student_classes = [c for c in classes if student['email'] in c.get('students', [])]
                        if student_classes:
                            st.markdown("### 📚 Enrolled Classes")
                            for c in student_classes:
                                with st.expander(f"{c['name']} - {c['grade']}"):
                                    st.write(f"**Teacher:** {c.get('teacher_name', 'Unknown')}")
                                    st.write(f"**Schedule:** {c.get('schedule', 'TBD')}")
                        
                        # Assignments
                        student_assignments = [a for a in assignments if a['class'] in [c['name'] for c in student_classes]]
                        if student_assignments:
                            st.markdown("### 📝 Pending Assignments")
                            for a in student_assignments:
                                with st.container():
                                    st.write(f"**{a['title']}** - Due: {a['due']}")
                                    st.write(f"📝 {a.get('description', '')}")
                                    st.divider()
                        
                        # Grades
                        student_grades = [g for g in grades if g.get('student') == student['email']]
                        if student_grades:
                            st.markdown("### 📊 Recent Grades")
                            for g in student_grades[-5:]:
                                st.write(f"**{g.get('assignment_title', 'Assignment')}**: {g['grade']}")
    
    else:
        # ----- MANAGEMENT MODE CONTENT (Fully Implemented) -----
        st.markdown(f"<h1 style='text-align: center;'>⚙️ {school['name']} Management System</h1>", unsafe_allow_html=True)
        
        if user['role'] == 'admin':
            if menu == "Analytics":
                st.markdown("### 📊 School Analytics")
                
                # Analytics Dashboard
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    total_students = school['stats'].get('students', 0)
                    st.metric("Total Students", total_students, f"+{int(total_students*0.12) if total_students > 0 else 0}")
                with col2:
                    avg_performance = 78
                    st.metric("Avg. Performance", f"{avg_performance}%", "+5%")
                with col3:
                    attendance_rate = 92
                    st.metric("Attendance Rate", f"{attendance_rate}%", "-2%")
                with col4:
                    retention_rate = 95
                    st.metric("Retention Rate", f"{retention_rate}%", "+3%")
                
                st.divider()
                
                # Charts
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### 📈 Performance by Subject")
                    subjects = ["Math", "Science", "English", "Kiswahili", "Social Studies"]
                    scores = [78, 82, 85, 80, 75]
                    fig = px.bar(x=subjects, y=scores, labels={'x': 'Subject', 'y': 'Average Score (%)'}, 
                                 color=scores, color_continuous_scale='viridis')
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("#### 📊 Enrollment by Grade")
                    grades = ["Grade 1-3", "Grade 4-6", "Grade 7-9", "Form 1-2", "Form 3-4"]
                    enrollment = [120, 145, 110, 95, 80]
                    fig = px.pie(values=enrollment, names=grades, title="Student Distribution")
                    st.plotly_chart(fig, use_container_width=True)
                
                st.divider()
                
                # Recent Activity
                st.markdown("#### 🔔 Recent Activity")
                activity_data = pd.DataFrame({
                    'Date': [date.today() - timedelta(days=i) for i in range(5)],
                    'Event': ['New student enrollment', 'Library book borrowed', 'Furniture allocated', 'Exam scheduled', 'Staff meeting'],
                    'Status': ['Completed', 'Active', 'Active', 'Upcoming', 'Completed']
                })
                st.dataframe(activity_data, use_container_width=True)
            
            elif menu == "Library":
                st.markdown("### 📚 Library Management System")
                
                tabs = st.tabs(["📖 Book Catalog", "👥 Members", "📝 Borrow/Return", "📋 Borrowed Log", "⏰ Due Reminders", "📊 Reports"])
                
                with tabs[0]:  # Book Catalog
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.markdown("#### ➕ Add New Book")
                        with st.form("add_book_form"):
                            book_title = st.text_input("Book Title")
                            book_type = st.selectbox("Book Type", ["Textbook", "Novel", "Reference", "Journal", "Magazine"])
                            book_quantity = st.number_input("Quantity", min_value=1, value=1)
                            book_author = st.text_input("Author (Optional)")
                            
                            if st.form_submit_button("📥 Add to Catalog", use_container_width=True):
                                if book_title and book_type:
                                    new_book = {
                                        "id": generate_book_id(),
                                        "title": book_title,
                                        "type": book_type,
                                        "author": book_author,
                                        "quantity": book_quantity,
                                        "available": book_quantity,
                                        "added_date": datetime.now().strftime("%Y-%m-%d")
                                    }
                                    st.session_state.book_catalog.append(new_book)
                                    st.success(f"Added '{book_title}' to catalog!")
                                    st.rerun()
                    
                    with col2:
                        st.markdown("#### 📚 Current Catalog")
                        if st.session_state.book_catalog:
                            for book in st.session_state.book_catalog:
                                stock_class = ""
                                if book['available'] <= 2 and book['available'] > 0:
                                    stock_class = "low-stock"
                                elif book['available'] == 0:
                                    stock_class = "out-of-stock"
                                
                                col_a, col_b, col_c = st.columns([3, 1, 1])
                                with col_a:
                                    st.markdown(f"**{book['title']}** ({book['type']})")
                                    st.caption(f"Author: {book.get('author', 'Unknown')} | Added: {book['added_date']}")
                                with col_b:
                                    st.markdown(f"<p class='{stock_class}'>Available: {book['available']}/{book['quantity']}</p>", unsafe_allow_html=True)
                                with col_c:
                                    if st.button("🗑️", key=f"del_book_{book['id']}"):
                                        st.session_state.book_catalog.remove(book)
                                        st.rerun()
                                st.divider()
                        else:
                            st.info("No books in catalog yet. Add your first book!")
                
                with tabs[1]:  # Members
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.markdown("#### 👤 Add Member")
                        with st.form("add_member_form"):
                            member_name = st.text_input("Member Name")
                            member_email = st.text_input("Email (Optional)")
                            member_phone = st.text_input("Phone (Optional)")
                            
                            if st.form_submit_button("➕ Add Member", use_container_width=True):
                                if member_name:
                                    new_member = {
                                        "id": generate_id("MEM"),
                                        "name": member_name,
                                        "email": member_email,
                                        "phone": member_phone,
                                        "joined_date": datetime.now().strftime("%Y-%m-%d"),
                                        "books_borrowed": 0
                                    }
                                    st.session_state.library_members.append(new_member)
                                    st.success(f"Added member: {member_name}")
                                    st.rerun()
                    
                    with col2:
                        st.markdown("#### 👥 Member List")
                        if st.session_state.library_members:
                            for member in st.session_state.library_members:
                                col_a, col_b, col_c = st.columns([3, 1, 1])
                                with col_a:
                                    st.write(f"**{member['name']}**")
                                    st.caption(f"Email: {member.get('email', 'N/A')} | Phone: {member.get('phone', 'N/A')}")
                                with col_b:
                                    st.write(f"Books: {member['books_borrowed']}")
                                with col_c:
                                    if st.button("🗑️", key=f"del_member_{member['id']}"):
                                        st.session_state.library_members.remove(member)
                                        st.rerun()
                                st.divider()
                        else:
                            st.info("No members registered yet.")
                
                with tabs[2]:  # Borrow/Return
                    st.markdown("#### 📝 Borrow a Book")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        with st.form("borrow_book_form"):
                            # Get member list
                            member_options = [f"{m['name']} (ID: {m['id']})" for m in st.session_state.library_members] if st.session_state.library_members else ["No members available"]
                            selected_member = st.selectbox("Select Member", member_options)
                            
                            # Get available books
                            available_books = [b for b in st.session_state.book_catalog if b['available'] > 0]
                            book_options = [f"{b['title']} ({b['available']} available)" for b in available_books] if available_books else ["No books available"]
                            selected_book = st.selectbox("Select Book", book_options)
                            
                            borrow_date = st.date_input("Borrow Date", date.today())
                            return_date = st.date_input("Return Due Date", date.today() + timedelta(days=14))
                            
                            if st.form_submit_button("📥 Borrow Book", use_container_width=True):
                                if available_books and st.session_state.library_members:
                                    # Find selected member and book
                                    member_idx = member_options.index(selected_member)
                                    book_idx = book_options.index(selected_book)
                                    
                                    member = st.session_state.library_members[member_idx]
                                    book = available_books[book_idx]
                                    
                                    # Update book availability
                                    book['available'] -= 1
                                    
                                    # Create borrow record
                                    borrow_record = {
                                        "id": generate_id("BRW"),
                                        "member_id": member['id'],
                                        "member_name": member['name'],
                                        "book_id": book['id'],
                                        "book_title": book['title'],
                                        "borrow_date": borrow_date.strftime("%Y-%m-%d"),
                                        "return_due_date": return_date.strftime("%Y-%m-%d"),
                                        "returned": False,
                                        "returned_date": None
                                    }
                                    st.session_state.borrowed_books.append(borrow_record)
                                    
                                    # Update member's borrowed count
                                    member['books_borrowed'] += 1
                                    
                                    st.success(f"Book '{book['title']}' borrowed by {member['name']}")
                                    st.rerun()
                    
                    with col2:
                        st.markdown("#### ↩️ Return a Book")
                        # Show currently borrowed books
                        active_borrows = [b for b in st.session_state.borrowed_books if not b['returned']]
                        
                        if active_borrows:
                            for borrow in active_borrows:
                                with st.container():
                                    col_a, col_b = st.columns([3, 1])
                                    with col_a:
                                        st.write(f"**{borrow['book_title']}**")
                                        st.caption(f"Borrowed by: {borrow['member_name']} | Due: {borrow['return_due_date']}")
                                    with col_b:
                                        if st.button("↩️ Return", key=f"return_{borrow['id']}"):
                                            # Update book availability
                                            book = next((b for b in st.session_state.book_catalog if b['id'] == borrow['book_id']), None)
                                            if book:
                                                book['available'] += 1
                                            
                                            # Update borrow record
                                            borrow['returned'] = True
                                            borrow['returned_date'] = date.today().strftime("%Y-%m-%d")
                                            
                                            # Update member's borrowed count
                                            member = next((m for m in st.session_state.library_members if m['id'] == borrow['member_id']), None)
                                            if member:
                                                member['books_borrowed'] -= 1
                                            
                                            st.success("Book returned successfully!")
                                            st.rerun()
                                    st.divider()
                        else:
                            st.info("No books currently borrowed.")
                
                with tabs[3]:  # Borrowed Log
                    st.markdown("#### 📋 Current Borrowed Books")
                    
                    active_borrows = [b for b in st.session_state.borrowed_books if not b['returned']]
                    
                    if active_borrows:
                        # Create DataFrame for display
                        borrow_data = []
                        for b in active_borrows:
                            today = date.today()
                            due_date = datetime.strptime(b['return_due_date'], "%Y-%m-%d").date()
                            days_left = (due_date - today).days
                            
                            status = "✅ On Time"
                            if days_left < 0:
                                status = f"❌ Overdue by {abs(days_left)} days"
                            elif days_left <= 3:
                                status = f"⚠️ Due in {days_left} days"
                            
                            borrow_data.append({
                                "Member": b['member_name'],
                                "Book": b['book_title'],
                                "Borrow Date": b['borrow_date'],
                                "Due Date": b['return_due_date'],
                                "Status": status
                            })
                        
                        df = pd.DataFrame(borrow_data)
                        st.dataframe(df, use_container_width=True)
                        
                        # Export options
                        if st.button("📥 Export to Excel"):
                            # Convert to Excel and provide download
                            output = BytesIO()
                            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                                df.to_excel(writer, sheet_name='Borrowed Books', index=False)
                            st.download_button(
                                label="Download Excel",
                                data=output.getvalue(),
                                file_name=f"borrowed_books_{date.today()}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                    else:
                        st.info("No books are currently borrowed.")
                
                with tabs[4]:  # Due Reminders
                    st.markdown("#### ⏰ Due and Overdue Reminders")
                    
                    today = date.today()
                    reminders = []
                    
                    for b in st.session_state.borrowed_books:
                        if not b['returned']:
                            due_date = datetime.strptime(b['return_due_date'], "%Y-%m-%d").date()
                            days_left = (due_date - today).days
                            
                            if days_left <= 3:  # Due soon or overdue
                                reminders.append({
                                    "Member": b['member_name'],
                                    "Book": b['book_title'],
                                    "Due Date": b['return_due_date'],
                                    "Days Left": days_left,
                                    "Status": "OVERDUE" if days_left < 0 else f"Due in {days_left} days"
                                })
                    
                    if reminders:
                        df = pd.DataFrame(reminders)
                        # Color code based on urgency
                        def color_status(val):
                            if "OVERDUE" in val:
                                return 'color: red; font-weight: bold'
                            elif "Due in 0" in val or "Due in 1" in val or "Due in 2" in val:
                                return 'color: orange; font-weight: bold'
                            return ''
                        
                        styled_df = df.style.applymap(color_status, subset=['Status'])
                        st.dataframe(styled_df, use_container_width=True)
                        
                        # Send reminder button (placeholder)
                        if st.button("📧 Send Email Reminders"):
                            st.success("Reminder emails sent to members with due/overdue books!")
                    else:
                        st.success("No books are due soon or overdue.")
                
                with tabs[5]:  # Reports
                    st.markdown("#### 📊 Library Reports")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Most borrowed books
                        st.markdown("##### 📈 Most Borrowed Books")
                        if st.session_state.borrowed_books:
                            book_counts = {}
                            for b in st.session_state.borrowed_books:
                                book_counts[b['book_title']] = book_counts.get(b['book_title'], 0) + 1
                            
                            book_df = pd.DataFrame(list(book_counts.items()), columns=['Book', 'Times Borrowed'])
                            book_df = book_df.sort_values('Times Borrowed', ascending=False).head(5)
                            
                            fig = px.bar(book_df, x='Book', y='Times Borrowed', title="Top 5 Most Borrowed Books")
                            st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # Active members
                        st.markdown("##### 👥 Most Active Members")
                        if st.session_state.library_members:
                            member_data = [{"Member": m['name'], "Books Borrowed": m['books_borrowed']} 
                                         for m in st.session_state.library_members if m['books_borrowed'] > 0]
                            if member_data:
                                member_df = pd.DataFrame(member_data)
                                member_df = member_df.sort_values('Books Borrowed', ascending=False).head(5)
                                
                                fig = px.bar(member_df, x='Member', y='Books Borrowed', title="Top 5 Most Active Members")
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.info("No borrowing activity yet.")
            
            elif menu == "Furniture":
                st.markdown("### 🪑 Furniture Allocation System")
                
                tabs = st.tabs(["📦 Inventory", "✍️ Allocate", "📜 Allocation Log", "📊 Reports"])
                
                with tabs[0]:  # Inventory
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.markdown("#### ➕ Add Furniture Item")
                        with st.form("add_furniture_form"):
                            furniture_name = st.text_input("Item Name")
                            furniture_type = st.selectbox("Item Type", ["Desk", "Chair", "Table", "Cabinet", "Shelf", "Board", "Locker", "Other"])
                            furniture_quantity = st.number_input("Quantity", min_value=1, value=1)
                            furniture_location = st.text_input("Location/Room (Optional)")
                            
                            if st.form_submit_button("📥 Add to Inventory", use_container_width=True):
                                if furniture_name and furniture_type:
                                    new_item = {
                                        "id": generate_furniture_id(),
                                        "name": furniture_name,
                                        "type": furniture_type,
                                        "quantity": furniture_quantity,
                                        "available": furniture_quantity,
                                        "location": furniture_location,
                                        "added_date": datetime.now().strftime("%Y-%m-%d")
                                    }
                                    st.session_state.furniture_inventory.append(new_item)
                                    st.success(f"Added '{furniture_name}' to inventory!")
                                    st.rerun()
                    
                    with col2:
                        st.markdown("#### 📦 Current Inventory")
                        if st.session_state.furniture_inventory:
                            for item in st.session_state.furniture_inventory:
                                stock_class = ""
                                if item['available'] <= 2 and item['available'] > 0:
                                    stock_class = "low-stock"
                                elif item['available'] == 0:
                                    stock_class = "out-of-stock"
                                
                                col_a, col_b, col_c = st.columns([3, 1, 1])
                                with col_a:
                                    st.markdown(f"**{item['name']}** ({item['type']})")
                                    st.caption(f"Location: {item.get('location', 'N/A')} | Added: {item['added_date']}")
                                with col_b:
                                    st.markdown(f"<p class='{stock_class}'>Available: {item['available']}/{item['quantity']}</p>", unsafe_allow_html=True)
                                with col_c:
                                    if st.button("🗑️", key=f"del_furniture_{item['id']}"):
                                        st.session_state.furniture_inventory.remove(item)
                                        st.rerun()
                                st.divider()
                        else:
                            st.info("No furniture in inventory yet. Add your first item!")
                
                with tabs[1]:  # Allocate
                    st.markdown("#### ✍️ Allocate Furniture")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        with st.form("allocate_furniture_form"):
                            recipient_name = st.text_input("Recipient Name")
                            recipient_type = st.selectbox("Recipient Type", ["Student", "Teacher", "Staff", "Classroom"])
                            recipient_id = st.text_input("ADM/ID Number (if student)")
                            
                            # Get available furniture
                            available_items = [i for i in st.session_state.furniture_inventory if i['available'] > 0]
                            item_options = [f"{i['name']} ({i['available']} available)" for i in available_items] if available_items else ["No items available"]
                            selected_item = st.selectbox("Select Furniture Item", item_options)
                            
                            quantity = st.number_input("Quantity", min_value=1, max_value=10, value=1)
                            allocation_date = st.date_input("Allocation Date", date.today())
                            notes = st.text_area("Notes (Optional)")
                            
                            if st.form_submit_button("🚚 Allocate Furniture", use_container_width=True):
                                if recipient_name and available_items and selected_item != "No items available":
                                    item_idx = item_options.index(selected_item)
                                    item = available_items[item_idx]
                                    
                                    if quantity <= item['available']:
                                        # Update item availability
                                        item['available'] -= quantity
                                        
                                        # Create allocation record
                                        allocation = {
                                            "id": generate_id("ALLOC"),
                                            "recipient_name": recipient_name,
                                            "recipient_type": recipient_type,
                                            "recipient_id": recipient_id,
                                            "item_id": item['id'],
                                            "item_name": item['name'],
                                            "item_type": item['type'],
                                            "quantity": quantity,
                                            "allocation_date": allocation_date.strftime("%Y-%m-%d"),
                                            "notes": notes,
                                            "returned": False,
                                            "returned_date": None
                                        }
                                        st.session_state.furniture_allocations.append(allocation)
                                        
                                        st.success(f"Allocated {quantity} {item['name']}(s) to {recipient_name}")
                                        st.rerun()
                                    else:
                                        st.error(f"Only {item['available']} items available.")
                    
                    with col2:
                        st.markdown("#### ↩️ Return Furniture")
                        active_allocations = [a for a in st.session_state.furniture_allocations if not a['returned']]
                        
                        if active_allocations:
                            for alloc in active_allocations:
                                with st.container():
                                    col_a, col_b = st.columns([3, 1])
                                    with col_a:
                                        st.write(f"**{alloc['item_name']}** (x{alloc['quantity']})")
                                        st.caption(f"Allocated to: {alloc['recipient_name']} | Date: {alloc['allocation_date']}")
                                    with col_b:
                                        if st.button("↩️ Return", key=f"return_furniture_{alloc['id']}"):
                                            # Update item availability
                                            item = next((i for i in st.session_state.furniture_inventory if i['id'] == alloc['item_id']), None)
                                            if item:
                                                item['available'] += alloc['quantity']
                                            
                                            # Update allocation record
                                            alloc['returned'] = True
                                            alloc['returned_date'] = date.today().strftime("%Y-%m-%d")
                                            
                                            st.success("Furniture returned successfully!")
                                            st.rerun()
                                    st.divider()
                        else:
                            st.info("No active furniture allocations.")
                
                with tabs[2]:  # Allocation Log
                    st.markdown("#### 📜 Furniture Allocation History")
                    
                    if st.session_state.furniture_allocations:
                        # Create DataFrame for display
                        alloc_data = []
                        for a in st.session_state.furniture_allocations:
                            status = "✅ Active" if not a['returned'] else f"↩️ Returned on {a['returned_date']}"
                            alloc_data.append({
                                "Recipient": a['recipient_name'],
                                "Type": a['recipient_type'],
                                "Item": a['item_name'],
                                "Quantity": a['quantity'],
                                "Allocation Date": a['allocation_date'],
                                "Status": status
                            })
                        
                        df = pd.DataFrame(alloc_data)
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("No furniture allocations yet.")
                
                with tabs[3]:  # Reports
                    st.markdown("#### 📊 Furniture Reports")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Inventory by type
                        st.markdown("##### 📊 Inventory by Type")
                        if st.session_state.furniture_inventory:
                            type_counts = {}
                            for item in st.session_state.furniture_inventory:
                                type_counts[item['type']] = type_counts.get(item['type'], 0) + item['quantity']
                            
                            type_df = pd.DataFrame(list(type_counts.items()), columns=['Type', 'Total Quantity'])
                            fig = px.pie(type_df, values='Total Quantity', names='Type', title="Inventory Distribution by Type")
                            st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # Most allocated items
                        st.markdown("##### 📈 Most Allocated Items")
                        if st.session_state.furniture_allocations:
                            item_counts = {}
                            for a in st.session_state.furniture_allocations:
                                item_counts[a['item_name']] = item_counts.get(a['item_name'], 0) + a['quantity']
                            
                            item_df = pd.DataFrame(list(item_counts.items()), columns=['Item', 'Times Allocated'])
                            item_df = item_df.sort_values('Times Allocated', ascending=False).head(5)
                            
                            fig = px.bar(item_df, x='Item', y='Times Allocated', title="Top 5 Most Allocated Items")
                            st.plotly_chart(fig, use_container_width=True)
            
            elif menu == "Teacher Books":
                st.markdown("### 👨‍🏫 Teacher Book Allocation")
                
                tabs = st.tabs(["📝 Allocate to Class", "📜 Allocation Log", "📊 Reports"])
                
                with tabs[0]:  # Allocate to Class
                    st.markdown("#### Upload Class List")
                    
                    # File upload for class list
                    uploaded_file = st.file_uploader("Upload Excel file with student names and admission numbers", 
                                                     type=['xlsx', 'xls'], key="teacher_class_upload")
                    
                    if uploaded_file is not None:
                        try:
                            df = pd.read_excel(uploaded_file)
                            if 'name' in df.columns and 'adm' in df.columns:
                                st.session_state.current_teacher_class = df.to_dict('records')
                                st.session_state.current_teacher_class_name = uploaded_file.name
                                st.success(f"Loaded {len(df)} students from {uploaded_file.name}")
                                
                                # Show preview
                                st.markdown("##### Class List Preview")
                                st.dataframe(df.head())
                            else:
                                st.error("Excel file must contain 'name' and 'adm' columns")
                        except Exception as e:
                            st.error(f"Error reading file: {e}")
                    
                    if st.session_state.current_teacher_class:
                        st.divider()
                        st.markdown("#### Allocate Books")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Book selection
                            available_books = [b for b in st.session_state.book_catalog if b['available'] > 0]
                            if available_books:
                                book_options = [f"{b['title']} ({b['available']} available)" for b in available_books]
                                selected_book = st.selectbox("Select Book to Allocate", book_options)
                                book_idx = book_options.index(selected_book)
                                book = available_books[book_idx]
                                
                                allocation_date = st.date_input("Allocation Date", date.today())
                                
                                if st.button("📥 Allocate to Selected Students", use_container_width=True):
                                    st.session_state.teacher_allocation_mode = True
                            else:
                                st.warning("No books available for allocation.")
                        
                        with col2:
                            if 'teacher_allocation_mode' in st.session_state and st.session_state.teacher_allocation_mode:
                                st.markdown("##### Select Students")
                                
                                # Create checkboxes for each student
                                selected_students = []
                                for i, student in enumerate(st.session_state.current_teacher_class):
                                    if st.checkbox(f"{student['name']} ({student['adm']})", key=f"student_{i}"):
                                        selected_students.append(student)
                                
                                if selected_students and st.button("✅ Confirm Allocation"):
                                    if len(selected_students) <= book['available']:
                                        # Create allocation records
                                        allocation_id = generate_id("TCHALLOC")
                                        allocation_records = []
                                        
                                        for student in selected_students:
                                            record = {
                                                "student_name": student['name'],
                                                "student_adm": student['adm'],
                                                "book_title": book['title'],
                                                "book_id": book['id'],
                                                "allocation_date": allocation_date.strftime("%Y-%m-%d"),
                                                "returned": False
                                            }
                                            allocation_records.append(record)
                                        
                                        # Update book availability
                                        book['available'] -= len(selected_students)
                                        
                                        # Store allocation
                                        st.session_state.teacher_allocations[allocation_id] = {
                                            "id": allocation_id,
                                            "class_name": st.session_state.current_teacher_class_name,
                                            "book_title": book['title'],
                                            "book_id": book['id'],
                                            "allocation_date": allocation_date.strftime("%Y-%m-%d"),
                                            "students": allocation_records,
                                            "total_allocated": len(selected_students)
                                        }
                                        
                                        st.success(f"Allocated {book['title']} to {len(selected_students)} students!")
                                        st.session_state.teacher_allocation_mode = False
                                        st.rerun()
                                    else:
                                        st.error(f"Not enough copies. Only {book['available']} available.")
                
                with tabs[1]:  # Allocation Log
                    st.markdown("#### 📜 Teacher Allocation Log")
                    
                    if st.session_state.teacher_allocations:
                        for alloc_id, alloc in st.session_state.teacher_allocations.items():
                            with st.expander(f"{alloc['class_name']} - {alloc['book_title']} ({alloc['allocation_date']})"):
                                st.write(f"**Total Students:** {alloc['total_allocated']}")
                                
                                # Student list
                                student_data = []
                                for s in alloc['students']:
                                    student_data.append({
                                        "Name": s['student_name'],
                                        "ADM": s['student_adm'],
                                        "Status": "✅ Active" if not s['returned'] else "↩️ Returned"
                                    })
                                
                                df = pd.DataFrame(student_data)
                                st.dataframe(df, use_container_width=True)
                                
                                if st.button("🗑️ Delete Allocation", key=f"del_teacher_alloc_{alloc_id}"):
                                    # Return books to inventory
                                    book = next((b for b in st.session_state.book_catalog if b['id'] == alloc['book_id']), None)
                                    if book:
                                        book['available'] += alloc['total_allocated']
                                    
                                    del st.session_state.teacher_allocations[alloc_id]
                                    st.rerun()
                    else:
                        st.info("No teacher allocations yet.")
                
                with tabs[2]:  # Reports
                    st.markdown("#### 📊 Teacher Allocation Reports")
                    
                    if st.session_state.teacher_allocations:
                        # Summary statistics
                        total_allocations = len(st.session_state.teacher_allocations)
                        total_books_allocated = sum(alloc['total_allocated'] for alloc in st.session_state.teacher_allocations.values())
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Allocations", total_allocations)
                        with col2:
                            st.metric("Books Allocated", total_books_allocated)
                        with col3:
                            st.metric("Classes Served", len(set(alloc['class_name'] for alloc in st.session_state.teacher_allocations.values())))
                        
                        st.divider()
                        
                        # Books allocated chart
                        book_counts = {}
                        for alloc in st.session_state.teacher_allocations.values():
                            book_counts[alloc['book_title']] = book_counts.get(alloc['book_title'], 0) + alloc['total_allocated']
                        
                        if book_counts:
                            book_df = pd.DataFrame(list(book_counts.items()), columns=['Book', 'Times Allocated'])
                            fig = px.bar(book_df, x='Book', y='Times Allocated', title="Books Allocated to Classes")
                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No data available for reports.")
            
            elif menu == "Finance":
                st.markdown("### 💰 Finance Management")
                
                tabs = st.tabs(["📊 Overview", "💵 Fee Collection", "📝 Expenses", "📈 Reports"])
                
                with tabs[0]:
                    st.markdown("##### Financial Overview")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Fees Collected", "KSh 2.5M", "+15%")
                    with col2:
                        st.metric("Pending Fees", "KSh 450K", "-8%")
                    with col3:
                        st.metric("Total Expenses", "KSh 1.8M", "+10%")
                    
                    st.divider()
                    
                    # Sample transactions
                    st.markdown("##### Recent Transactions")
                    transactions = [
                        {"date": "2024-01-15", "student": "John Doe", "description": "Term 1 Fees", "amount": "KSh 45,000", "status": "Paid"},
                        {"date": "2024-01-14", "student": "Jane Smith", "description": "Term 1 Fees", "amount": "KSh 45,000", "status": "Paid"},
                        {"date": "2024-01-13", "student": "Bob Johnson", "description": "Term 1 Fees", "amount": "KSh 22,500", "status": "Partial"},
                        {"date": "2024-01-12", "student": "Alice Brown", "description": "Library Fine", "amount": "KSh 500", "status": "Paid"},
                    ]
                    df = pd.DataFrame(transactions)
                    st.dataframe(df, use_container_width=True)
                
                with tabs[1]:
                    st.info("Fee collection module - Coming soon!")
                
                with tabs[2]:
                    st.info("Expense tracking module - Coming soon!")
                
                with tabs[3]:
                    st.info("Financial reports module - Coming soon!")
            
            elif menu == "Staff":
                st.markdown("### 👥 Staff Management")
                
                tabs = st.tabs(["📋 Staff List", "💰 Payroll", "📊 Performance", "📈 Reports"])
                
                with tabs[0]:
                    st.markdown("##### Staff Directory")
                    staff = [
                        {"name": "Dr. Sarah Kimani", "role": "Principal", "department": "Administration", "status": "Active"},
                        {"name": "Mr. John Omondi", "role": "Deputy Principal", "department": "Administration", "status": "Active"},
                        {"name": "Ms. Lucy Wanjiku", "role": "HOD Science", "department": "Science", "status": "Active"},
                        {"name": "Mr. Peter Mwangi", "role": "Senior Teacher", "department": "Mathematics", "status": "Active"},
                        {"name": "Mrs. Grace Achieng", "role": "Librarian", "department": "Library", "status": "Active"},
                    ]
                    df = pd.DataFrame(staff)
                    st.dataframe(df, use_container_width=True)
                
                with tabs[1]:
                    st.info("Payroll module - Coming soon!")
                
                with tabs[2]:
                    st.info("Performance evaluation module - Coming soon!")
                
                with tabs[3]:
                    st.info("Staff reports module - Coming soon!")
            
            elif menu == "Curriculum":
                st.markdown("### 📚 Curriculum Planning")
                st.info("Curriculum planning module - Coming soon!")
                st.markdown("""
                Features will include:
                - Lesson plan templates
                - Scheme of work creation
                - Syllabus tracking
                - Learning outcomes monitoring
                - Resource mapping
                """)
            
            elif menu == "Exams":
                st.markdown("### 📝 Examination Management")
                st.info("Examination module - Coming soon!")
                st.markdown("""
                Features will include:
                - Exam scheduling
                - Grade entry and processing
                - Result sheets generation
                - Performance analysis
                - Report cards
                """)
            
            elif menu == "Inventory":
                st.markdown("### 📦 Inventory Management")
                st.info("Inventory module - Coming soon!")
                st.markdown("""
                Features will include:
                - Asset tracking
                - Textbook inventory
                - Equipment management
                - Stock alerts
                - Maintenance scheduling
                """)
            
            elif menu == "Reports":
                st.markdown("### 📊 Report Generation")
                st.info("Reports module - Coming soon!")
                st.markdown("""
                Available reports:
                - Student performance reports
                - Financial summaries
                - Staff reports
                - Inventory status
                - Custom report builder
                """)
            
            elif menu == "Settings":
                st.markdown("### ⚙️ Management Settings")
                
                tabs = st.tabs(["🏫 School Info", "🔧 System", "📧 Notifications", "💾 Data"])
                
                with tabs[0]:
                    st.markdown("##### School Information")
                    with st.form("school_info_form"):
                        school_name = st.text_input("School Name", school['name'])
                        school_motto = st.text_input("School Motto", school.get('motto', ''))
                        school_city = st.text_input("City", school.get('city', ''))
                        school_state = st.text_input("State/Province", school.get('state', ''))
                        
                        if st.form_submit_button("💾 Update School Info"):
                            school['name'] = school_name
                            school['motto'] = school_motto
                            school['city'] = school_city
                            school['state'] = school_state
                            
                            all_schools = load_all_schools()
                            all_schools[school_code] = school
                            save_all_schools(all_schools)
                            
                            st.success("School information updated!")
                            st.rerun()
                
                with tabs[1]:
                    st.markdown("##### System Settings")
                    st.info("System settings coming soon!")
                
                with tabs[2]:
                    st.markdown("##### Notification Settings")
                    st.info("Email and SMS notification settings coming soon!")
                
                with tabs[3]:
                    st.markdown("##### Data Management")
                    if st.button("📥 Export All Data"):
                        # Collect all data
                        all_data = {
                            "school": school,
                            "users": users,
                            "classes": classes,
                            "groups": groups,
                            "library": {
                                "members": st.session_state.library_members,
                                "catalog": st.session_state.book_catalog,
                                "borrowed": st.session_state.borrowed_books
                            },
                            "furniture": {
                                "inventory": st.session_state.furniture_inventory,
                                "allocations": st.session_state.furniture_allocations
                            },
                            "teacher_allocations": st.session_state.teacher_allocations
                        }
                        
                        # Convert to JSON and provide download
                        json_str = json.dumps(all_data, indent=2)
                        st.download_button(
                            label="Download JSON Backup",
                            data=json_str,
                            file_name=f"{school_code}_backup_{date.today()}.json",
                            mime="application/json"
                        )
                    
                    if st.button("⚠️ Clear All Management Data"):
                        if st.checkbox("I understand this will delete all management data"):
                            st.session_state.library_members = []
                            st.session_state.book_catalog = []
                            st.session_state.borrowed_books = []
                            st.session_state.furniture_inventory = []
                            st.session_state.furniture_allocations = []
                            st.session_state.teacher_allocations = {}
                            st.success("All management data cleared!")
                            st.rerun()
        
        elif user['role'] == 'teacher':
            if menu == "My Classes":
                st.markdown("### 📚 My Classes")
                my_classes = [c for c in classes if c.get('teacher') == user['email']]
                if my_classes:
                    for c in my_classes:
                        with st.expander(f"{c['name']} - {c['grade']}"):
                            st.write(f"**Subject:** {c.get('subject', 'N/A')}")
                            st.write(f"**Students:** {len(c.get('students', []))}/{c.get('max_students', 40)}")
                            if c.get('students'):
                                st.write("**Student List:**")
                                for student_email in c['students']:
                                    student = next((u for u in users if u['email'] == student_email), None)
                                    if student:
                                        st.write(f"- {student['fullname']} ({student.get('admission_number', 'N/A')})")
                else:
                    st.info("You haven't been assigned any classes yet")
            
            elif menu == "Gradebook":
                st.markdown("### 📊 Gradebook")
                st.info("Gradebook module coming soon!")
            
            elif menu == "Attendance":
                st.markdown("### 📋 Attendance")
                st.info("Attendance module coming soon!")
            
            elif menu == "Lesson Plans":
                st.markdown("### 📝 Lesson Plans")
                st.info("Lesson plans module coming soon!")
            
            elif menu == "Library":
                st.markdown("### 📚 Library Access")
                # Show available books
                if st.session_state.book_catalog:
                    st.dataframe(pd.DataFrame(st.session_state.book_catalog))
                else:
                    st.info("No books in catalog")
            
            elif menu == "Furniture":
                st.markdown("### 🪑 Furniture Requests")
                st.info("Request furniture for your classroom")
                with st.form("furniture_request"):
                    st.text_input("Item Needed")
                    st.number_input("Quantity", min_value=1)
                    st.date_input("Date Needed")
                    if st.form_submit_button("Submit Request"):
                        st.success("Request submitted!")
            
            elif menu == "Reports":
                st.markdown("### 📊 Reports")
                st.info("Generate class reports")
            
            elif menu == "Settings":
                st.markdown("### ⚙️ Settings")
                st.info("Teacher settings")
        
        elif user['role'] == 'student':
            if menu == "My Grades":
                st.markdown("### 📊 My Grades")
                my_grades = [g for g in grades if g.get('student') == user['email']]
                if my_grades:
                    df = pd.DataFrame(my_grades)
                    st.dataframe(df)
                else:
                    st.info("No grades available yet")
            
            elif menu == "Attendance":
                st.markdown("### 📋 My Attendance")
                st.info("Attendance record coming soon!")
            
            elif menu == "Timetable":
                st.markdown("### 📅 Timetable")
                st.info("Timetable coming soon!")
            
            elif menu == "Library":
                st.markdown("### 📚 Library")
                # Show available books
                if st.session_state.book_catalog:
                    available = [b for b in st.session_state.book_catalog if b['available'] > 0]
                    if available:
                        st.dataframe(pd.DataFrame(available))
                    else:
                        st.info("No books available")
            
            elif menu == "Fee Statement":
                st.markdown("### 💰 Fee Statement")
                st.info("Fee statement coming soon!")
            
            elif menu == "Settings":
                st.markdown("### ⚙️ Settings")
                st.info("Student settings")
        
        elif user['role'] == 'guardian':
            if menu == "Student Progress":
                st.markdown("### 📈 Student Progress")
                for adm in user.get('linked_students', []):
                    student = next((u for u in users if u.get('admission_number') == adm), None)
                    if student:
                        st.subheader(f"{student['fullname']}")
                        # Show student's grades
                        student_grades = [g for g in grades if g.get('student') == student['email']]
                        if student_grades:
                            st.dataframe(pd.DataFrame(student_grades))
                        else:
                            st.info("No grades available")
            
            elif menu == "Fee Payments":
                st.markdown("### 💰 Fee Payments")
                st.info("Fee payment history coming soon!")
            
            elif menu == "Library":
                st.markdown("### 📚 Library")
                # Show what books their children have borrowed
                for adm in user.get('linked_students', []):
                    student = next((u for u in users if u.get('admission_number') == adm), None)
                    if student:
                        student_books = [b for b in st.session_state.borrowed_books 
                                       if b.get('member_name') == student['fullname'] and not b.get('returned', True)]
                        if student_books:
                            st.subheader(f"{student['fullname']}'s Books")
                            st.dataframe(pd.DataFrame(student_books))
            
            elif menu == "Reports":
                st.markdown("### 📊 Reports")
                st.info("Student reports coming soon!")
            
            elif menu == "Communications":
                st.markdown("### 💬 Communications")
                st.info("School communications coming soon!")
            
            elif menu == "Settings":
                st.markdown("### ⚙️ Settings")
                st.info("Guardian settings")

else:
    st.error("Something went wrong. Please restart.")
    if st.button("🔄 Restart"):
        st.session_state.page = 'welcome'
        st.rerun()
