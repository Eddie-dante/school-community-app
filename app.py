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
    
    .nav-button {{
        flex: 1;
        padding: 20px 30px;
        font-size: 1.5rem !important;
        font-weight: 900 !important;
        border: none !important;
        border-radius: 60px !important;
        cursor: pointer;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
    }}
    
    .nav-button.active {{
        transform: scale(1.05) !important;
        box-shadow: 0 20px 50px gold !important;
        border: 4px solid white !important;
    }}
    
    .hub-button {{
        background: linear-gradient(135deg, #4B0082, #8A2BE2) !important;
        color: gold !important;
        border: 4px solid gold !important;
    }}
    
    .hub-button.active {{
        background: linear-gradient(135deg, gold, #ffd700) !important;
        color: #4B0082 !important;
        border: 4px solid white !important;
    }}
    
    .management-button {{
        background: linear-gradient(135deg, #006400, #228B22) !important;
        color: #FFD700 !important;
        border: 4px solid gold !important;
    }}
    
    .management-button.active {{
        background: linear-gradient(135deg, gold, #ffd700) !important;
        color: #006400 !important;
        border: 4px solid white !important;
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

# ============ TOP NAVIGATION ============
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div class="top-nav">
        <button class="nav-button hub-button active" onclick="changeMode('hub')">🏫 School Community Hub</button>
        <button class="nav-button management-button" onclick="changeMode('management')">⚙️ School Management System</button>
    </div>
    """, unsafe_allow_html=True)
    
    # Use Streamlit buttons instead of HTML buttons for functionality
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
    else:
        st.markdown('<h1 class="radiant-title">⚙️ School Management System ⚙️</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: white; font-size: 1.5rem;">Manage • Organize • Excel</p>', unsafe_allow_html=True)
    
    st.divider()
    
    if st.session_state.app_mode == 'hub':
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
    
    else:  # MANAGEMENT MODE
        st.markdown("""
        <div style="text-align: center; padding: 50px;">
            <h2 style="color: gold;">⚙️ School Management System Coming Soon! ⚙️</h2>
            <p style="color: white; font-size: 1.2rem;">This module is under development. Features will include:</p>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 30px;">
                <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 20px; border: 2px solid gold;">
                    <h3 style="color: gold;">📊 Analytics Dashboard</h3>
                    <p style="color: white;">Real-time school performance metrics</p>
                </div>
                <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 20px; border: 2px solid gold;">
                    <h3 style="color: gold;">💰 Finance Management</h3>
                    <p style="color: white;">Fee collection, budgeting, reports</p>
                </div>
                <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 20px; border: 2px solid gold;">
                    <h3 style="color: gold;">📋 Staff Management</h3>
                    <p style="color: white;">Payroll, attendance, evaluations</p>
                </div>
                <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 20px; border: 2px solid gold;">
                    <h3 style="color: gold;">📚 Curriculum Planning</h3>
                    <p style="color: white;">Lesson plans, scheme of work</p>
                </div>
                <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 20px; border: 2px solid gold;">
                    <h3 style="color: gold;">📝 Examination Module</h3>
                    <p style="color: white;">Exam scheduling, results processing</p>
                </div>
                <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 20px; border: 2px solid gold;">
                    <h3 style="color: gold;">🏫 Inventory Management</h3>
                    <p style="color: white;">Assets, textbooks, equipment</p>
                </div>
            </div>
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
                options = ["Analytics", "Finance", "Staff", "Curriculum", "Exams", "Inventory", "Reports", "Settings"]
            elif user['role'] == 'teacher':
                options = ["My Classes", "Gradebook", "Attendance", "Lesson Plans", "Reports", "Settings"]
            elif user['role'] == 'student':
                options = ["My Grades", "Attendance", "Timetable", "Fee Statement", "Settings"]
            else:  # guardian
                options = ["Student Progress", "Fee Payments", "Reports", "Communications", "Settings"]
        
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
        # ----- MANAGEMENT MODE CONTENT (Placeholder) -----
        st.markdown(f"<h1 style='text-align: center;'>⚙️ {school['name']} Management System</h1>", unsafe_allow_html=True)
        
        if user['role'] == 'admin':
            if menu == "Analytics":
                st.markdown("### 📊 School Analytics")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Students", school['stats'].get('students', 0), "+12%")
                with col2:
                    st.metric("Avg. Performance", "78%", "+5%")
                with col3:
                    st.metric("Attendance Rate", "92%", "-2%")
                with col4:
                    st.metric("Retention Rate", "95%", "+3%")
                
                st.divider()
                st.markdown("### 📈 Performance Trends")
                st.line_chart({"Math": [65, 68, 72, 75, 78], "Science": [70, 72, 75, 73, 80], "English": [80, 82, 85, 83, 88]})
            
            elif menu == "Finance":
                st.markdown("### 💰 Financial Overview")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Fees Collected", "KSh 2.5M", "+15%")
                with col2:
                    st.metric("Pending Fees", "KSh 450K", "-8%")
                with col3:
                    st.metric("Expenses", "KSh 1.8M", "+10%")
                
                st.divider()
                st.markdown("### 📋 Recent Transactions")
                transactions = [
                    {"date": "2024-01-15", "student": "John Doe", "amount": "KSh 45,000", "status": "Paid"},
                    {"date": "2024-01-14", "student": "Jane Smith", "amount": "KSh 45,000", "status": "Paid"},
                    {"date": "2024-01-13", "student": "Bob Johnson", "amount": "KSh 22,500", "status": "Partial"},
                ]
                for t in transactions:
                    st.write(f"**{t['date']}** - {t['student']} - {t['amount']} - {t['status']}")
            
            elif menu == "Staff":
                st.markdown("### 👥 Staff Management")
                staff = [
                    {"name": "Dr. Sarah Kimani", "role": "Principal", "department": "Administration", "status": "Active"},
                    {"name": "Mr. John Omondi", "role": "Deputy Principal", "department": "Administration", "status": "Active"},
                    {"name": "Ms. Lucy Wanjiku", "role": "HOD Science", "department": "Science", "status": "Active"},
                ]
                for s in staff:
                    with st.container():
                        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                        with col1:
                            st.write(f"**{s['name']}**")
                        with col2:
                            st.write(s['role'])
                        with col3:
                            st.write(s['department'])
                        with col4:
                            st.write(f"✅ {s['status']}")
                        st.divider()
            
            elif menu == "Curriculum":
                st.markdown("### 📚 Curriculum Planning")
                st.info("Curriculum planning module coming soon!")
            
            elif menu == "Exams":
                st.markdown("### 📝 Examination Management")
                st.info("Examination module coming soon!")
            
            elif menu == "Inventory":
                st.markdown("### 📦 Inventory Management")
                st.info("Inventory module coming soon!")
            
            elif menu == "Reports":
                st.markdown("### 📊 Report Generation")
                st.info("Reports module coming soon!")
            
            elif menu == "Settings":
                st.markdown("### ⚙️ System Settings")
                st.info("Settings module coming soon!")
        
        elif user['role'] == 'teacher':
            if menu == "My Classes":
                st.markdown("### 📚 My Classes")
                st.info("Class management module coming soon!")
            elif menu == "Gradebook":
                st.markdown("### 📊 Gradebook")
                st.info("Gradebook module coming soon!")
            elif menu == "Attendance":
                st.markdown("### 📋 Attendance")
                st.info("Attendance module coming soon!")
            elif menu == "Lesson Plans":
                st.markdown("### 📝 Lesson Plans")
                st.info("Lesson plans module coming soon!")
            elif menu == "Reports":
                st.markdown("### 📊 Reports")
                st.info("Reports module coming soon!")
            elif menu == "Settings":
                st.markdown("### ⚙️ Settings")
                st.info("Settings module coming soon!")
        
        elif user['role'] == 'student':
            if menu == "My Grades":
                st.markdown("### 📊 My Grades")
                st.info("Grades module coming soon!")
            elif menu == "Attendance":
                st.markdown("### 📋 My Attendance")
                st.info("Attendance module coming soon!")
            elif menu == "Timetable":
                st.markdown("### 📅 Timetable")
                st.info("Timetable module coming soon!")
            elif menu == "Fee Statement":
                st.markdown("### 💰 Fee Statement")
                st.info("Fee statement module coming soon!")
            elif menu == "Settings":
                st.markdown("### ⚙️ Settings")
                st.info("Settings module coming soon!")
        
        elif user['role'] == 'guardian':
            if menu == "Student Progress":
                st.markdown("### 📈 Student Progress")
                st.info("Student progress module coming soon!")
            elif menu == "Fee Payments":
                st.markdown("### 💰 Fee Payments")
                st.info("Fee payments module coming soon!")
            elif menu == "Reports":
                st.markdown("### 📊 Reports")
                st.info("Reports module coming soon!")
            elif menu == "Communications":
                st.markdown("### 💬 Communications")
                st.info("Communications module coming soon!")
            elif menu == "Settings":
                st.markdown("### ⚙️ Settings")
                st.info("Settings module coming soon!")

else:
    st.error("Something went wrong. Please restart.")
    if st.button("🔄 Restart"):
        st.session_state.page = 'welcome'
        st.rerun()
