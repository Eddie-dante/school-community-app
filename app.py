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
    @media (max-width: 768px) {
        .main .block-container { padding: 0.8rem !important; }
        h1 { font-size: 1.8rem !important; }
        h2 { font-size: 1.3rem !important; }
        .stButton button { font-size: 0.9rem !important; padding: 0.4rem 0.8rem !important; }
    }
    
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
    
    @media (min-width: 769px) {
        section[data-testid="stSidebar"] {
            width: 240px !important;
            min-width: 240px !important;
            transform: translateX(0) !important;
        }
        .main .block-container {
            margin-left: 240px !important;
            max-width: calc(100% - 240px) !important;
        }
        
        section[data-testid="stSidebar"] > div {
            padding: 1rem 0.8rem !important;
        }
        
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] .stRadio label,
        section[data-testid="stSidebar"] p {
            font-size: 0.9rem !important;
        }
        
        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
            padding: 0.5rem !important;
        }
        
        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
            padding: 8px 10px !important;
            margin: 4px 0 !important;
            font-size: 0.9rem !important;
        }
        
        .school-header {
            padding: 10px !important;
            margin-bottom: 10px !important;
        }
        
        .school-header h2 {
            font-size: 1.2rem !important;
        }
        
        .profile-card {
            padding: 8px !important;
            margin-bottom: 10px !important;
        }
        
        .profile-card h1 {
            font-size: 1.8rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============ KENYAN CURRICULUM DATA ============
PRIMARY_SUBJECTS = [
    "Mathematics", "English", "Kiswahili", "Science and Technology",
    "Social Studies", "CRE / IRE / HRE", "Agriculture", "Home Science",
    "Art and Craft", "Music", "Physical Education"
]

JUNIOR_SECONDARY_SUBJECTS = [
    "Mathematics", "English", "Kiswahili", "Integrated Science",
    "Social Studies", "CRE / IRE / HRE", "Business Studies",
    "Agriculture", "Home Science", "Computer Science",
    "Pre-Technical Studies", "Visual Arts", "Performing Arts",
    "Physical Education"
]

SENIOR_SECONDARY_SUBJECTS = {
    "Mathematics": ["Mathematics"],
    "English": ["English"],
    "Kiswahili": ["Kiswahili"],
    "Sciences": ["Biology", "Chemistry", "Physics", "General Science"],
    "Humanities": ["History", "Geography", "CRE", "IRE", "HRE"],
    "Technical": ["Computer Studies", "Business Studies", "Agriculture", "Home Science"],
    "Languages": ["French", "German", "Arabic", "Sign Language"]
}

KENYAN_GRADES = [
    "Grade 1 (7 subjects)", "Grade 2 (7 subjects)", "Grade 3 (7 subjects)",
    "Grade 4 (7 subjects)", "Grade 5 (7 subjects)", "Grade 6 (7 subjects)",
    "Grade 7 (12 subjects)", "Grade 8 (12 subjects)", "Grade 9 (12 subjects)",
    "Form 1 (11 subjects)", "Form 2 (11 subjects)", "Form 3 (11 subjects)", "Form 4 (11 subjects)"
]

def get_subjects_for_grade(grade):
    if "Grade" in grade and any(str(i) in grade for i in range(1, 7)):
        return PRIMARY_SUBJECTS
    elif "Grade" in grade and any(str(i) in grade for i in range(7, 10)):
        return JUNIOR_SECONDARY_SUBJECTS
    elif "Form" in grade:
        subjects = []
        for category, subj_list in SENIOR_SECONDARY_SUBJECTS.items():
            subjects.extend(subj_list)
        return subjects
    else:
        return PRIMARY_SUBJECTS

# ============ FUNCTION TO GET BACKGROUND IMAGE ============
def get_background_image():
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
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    * {{
        font-family: 'Poppins', sans-serif;
        box-sizing: border-box;
    }}
    
    .stApp {{
        background-image: url('{BG_IMAGE}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}
    
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(0,0,0,0.75), rgba(0,0,0,0.6));
        z-index: 0;
    }}
    
    .main > div, section[data-testid="stSidebar"] {{
        position: relative;
        z-index: 2;
    }}
    
    section[data-testid="stSidebar"] {{
        background: linear-gradient(135deg, rgba(75, 0, 130, 0.98), rgba(138, 43, 226, 0.98), rgba(255, 215, 0, 0.95)) !important;
        backdrop-filter: blur(15px) !important;
        border-right: 3px solid gold !important;
        box-shadow: 5px 0 20px rgba(0, 0, 0, 0.5) !important;
        overflow-y: auto !important;
        height: 100vh !important;
        transition: transform 0.3s ease !important;
    }}
    
    button[data-testid="baseButton-header"] {{
        display: none !important;
    }}
    
    section[data-testid="stSidebar"] > div {{
        background: transparent !important;
        padding: 1rem 0.8rem !important;
        width: 100% !important;
    }}
    
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
    
    .main > div {{
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 40px;
        padding: 2rem;
        margin: 1.5rem;
        border: 4px solid rgba(255, 215, 0, 0.6);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
    }}
    
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
    
    .chat-container {{
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        padding: 15px;
        margin: 10px 0;
        border: 2px solid gold;
        max-height: 400px;
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
    
    .rank-badge {{
        display: inline-block;
        background: linear-gradient(135deg, gold, #ffd700);
        color: #4B0082;
        padding: 2px 8px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 800;
        margin-left: 5px;
    }}
    
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

# ============ CHAT & FRIENDSHIP FUNCTIONS ============
def send_friend_request(school_code, from_email, to_email):
    requests = load_school_data(school_code, "friend_requests.json", [])
    if not any(r['from'] == from_email and r['to'] == to_email and r['status'] == 'pending' for r in requests):
        requests.append({
            "id": generate_id("FRQ"),
            "from": from_email,
            "to": to_email,
            "status": "pending",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        save_school_data(school_code, "friend_requests.json", requests)
        return True
    return False

def accept_friend_request(school_code, request_id):
    requests = load_school_data(school_code, "friend_requests.json", [])
    friendships = load_school_data(school_code, "friendships.json", [])
    
    for req in requests:
        if req['id'] == request_id:
            req['status'] = 'accepted'
            friendships.append({
                "user1": min(req['from'], req['to']),
                "user2": max(req['from'], req['to']),
                "since": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            break
    
    save_school_data(school_code, "friend_requests.json", requests)
    save_school_data(school_code, "friendships.json", friendships)

def get_friends(school_code, user_email):
    friendships = load_school_data(school_code, "friendships.json", [])
    friends = []
    for f in friendships:
        if f['user1'] == user_email:
            friends.append(f['user2'])
        elif f['user2'] == user_email:
            friends.append(f['user1'])
    return friends

def get_pending_requests(school_code, user_email):
    requests = load_school_data(school_code, "friend_requests.json", [])
    return [r for r in requests if r['to'] == user_email and r['status'] == 'pending']

def send_message(users, sender_email, recipient_email, message, school_code):
    messages = load_school_data(school_code, "messages.json", [])
    messages.append({
        "id": generate_id("MSG"),
        "sender": sender_email,
        "recipient": recipient_email,
        "message": message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "read": False,
        "conversation_id": f"{min(sender_email, recipient_email)}_{max(sender_email, recipient_email)}"
    })
    save_school_data(school_code, "messages.json", messages)

def get_conversations(user_email, school_code):
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
    messages = load_school_data(school_code, "messages.json", [])
    return len([m for m in messages if m['recipient'] == user_email and not m['read']])

def mark_as_read(message_id, school_code):
    messages = load_school_data(school_code, "messages.json", [])
    for msg in messages:
        if msg['id'] == message_id:
            msg['read'] = True
            break
    save_school_data(school_code, "messages.json", messages)

# ============ GROUP FUNCTIONS ============
def get_user_rank_in_group(group, user_email):
    """Determine user's rank in a group"""
    if group.get('leader') == user_email:
        return "Leader"
    elif user_email in group.get('co_leaders', []):
        return "Co-Leader"
    elif user_email in group.get('members', []):
        return "Member"
    elif user_email in group.get('pending_requests', []):
        return "Request Pending"
    return "Not a Member"

def get_all_community_members(school_code, current_user):
    """Get all users in the school community except current user"""
    users = load_school_data(school_code, "users.json", [])
    return [u for u in users if u['email'] != current_user['email']]

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
                            "stats": {"students":0, "teachers":0, "guardians":0, "classes":0, "groups":0, "announcements":0}
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
                            "school_code": code,
                            "profile_pic": None,
                            "bio": "",
                            "phone": ""
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
                        save_school_data(code, "friend_requests.json", [])
                        save_school_data(code, "friendships.json", [])
                        
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
                                    "groups": [],
                                    "profile_pic": None,
                                    "bio": "",
                                    "phone": ""
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
                                    "guardians": [],
                                    "profile_pic": None,
                                    "bio": "",
                                    "phone": ""
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
                                    "linked_students": [student_admission],
                                    "profile_pic": None,
                                    "bio": "",
                                    "phone": phone
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
    
    # Load all data
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
    pending_friend_count = len(get_pending_requests(school_code, user['email']))
    
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
        
        # Navigation based on role
        if user['role'] == 'admin':
            options = ["Dashboard", "Announcements", "Classes", "Groups", "Teachers", "Students", "Guardians", "Community", f"Chat💬{f'({unread_count})' if unread_count>0 else ''}", f"Friends{f'({pending_friend_count})' if pending_friend_count>0 else ''}", "Profile"]
        elif user['role'] == 'teacher':
            options = ["Dashboard", "Announcements", "My Classes", "Groups", "Community", f"Chat💬{f'({unread_count})' if unread_count>0 else ''}", f"Friends{f'({pending_friend_count})' if pending_friend_count>0 else ''}", "Profile"]
        elif user['role'] == 'student':
            options = ["Dashboard", "Announcements", "Browse Classes", "Groups", "Community", f"Chat💬{f'({unread_count})' if unread_count>0 else ''}", f"Friends{f'({pending_friend_count})' if pending_friend_count>0 else ''}", "Profile"]
        else:  # guardian
            options = ["Dashboard", "Announcements", "My Student", "Community", f"Chat💬{f'({unread_count})' if unread_count>0 else ''}", f"Friends{f'({pending_friend_count})' if pending_friend_count>0 else ''}", "Profile"]
        
        menu = st.radio("", options, index=st.session_state.menu_index, label_visibility="collapsed")
        st.session_state.menu_index = options.index(menu)
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.current_school = None
            st.session_state.page = 'welcome'
            st.rerun()
    
    # ============ MAIN CONTENT ============
    
    # ----- ANNOUNCEMENTS (for all roles) -----
    if menu == "Announcements":
        st.markdown("<h2 style='text-align: center;'>📢 School Announcements</h2>", unsafe_allow_html=True)
        
        # Admin and teachers can post announcements
        if user['role'] in ['admin', 'teacher']:
            with st.expander("➕ Create New Announcement"):
                with st.form("new_announcement"):
                    title = st.text_input("Title")
                    content = st.text_area("Content", height=100)
                    target = st.selectbox("Target Audience", ["Everyone", "Students Only", "Teachers Only", "Guardians Only"])
                    important = st.checkbox("⭐ Mark as Important")
                    
                    if st.form_submit_button("📢 Post Announcement", use_container_width=True):
                        if title and content:
                            announcements.append({
                                "id": generate_id("ANN"),
                                "title": title,
                                "content": content,
                                "author": user['fullname'],
                                "author_email": user['email'],
                                "author_role": user['role'],
                                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "target": target,
                                "important": important
                            })
                            save_school_data(school_code, "announcements.json", announcements)
                            school['stats']['announcements'] = school['stats'].get('announcements', 0) + 1
                            all_schools = load_all_schools()
                            all_schools[school_code] = school
                            save_all_schools(all_schools)
                            st.success("Announcement posted!")
                            st.rerun()
        
        # Display announcements
        if announcements:
            for ann in reversed(announcements[-20:]):
                # Filter based on user role and target
                show = True
                if ann['target'] == "Students Only" and user['role'] != 'student':
                    show = False
                elif ann['target'] == "Teachers Only" and user['role'] != 'teacher':
                    show = False
                elif ann['target'] == "Guardians Only" and user['role'] != 'guardian':
                    show = False
                
                if show:
                    with st.container():
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            if ann.get('important'):
                                st.markdown(f"⭐ **{ann['title']}**")
                            else:
                                st.markdown(f"**{ann['title']}**")
                            st.write(ann['content'])
                        with col2:
                            st.caption(ann['date'][:16])
                            st.caption(f"By: {ann['author']}")
                        st.divider()
        else:
            st.info("No announcements yet")
    
    # ----- CLASSES (for all roles) -----
    elif menu in ["Classes", "My Classes", "Browse Classes"]:
        st.markdown("<h2 style='text-align: center;'>📚 Classes</h2>", unsafe_allow_html=True)
        
        # Admin can create classes
        if user['role'] == 'admin' and menu == "Classes":
            with st.expander("➕ Create New Class"):
                with st.form("create_class"):
                    col1, col2 = st.columns(2)
                    with col1:
                        class_name = st.text_input("Class Name", placeholder="e.g., Mathematics 101")
                        grade = st.selectbox("Grade/Form", KENYAN_GRADES)
                        available_subjects = get_subjects_for_grade(grade)
                        subject = st.selectbox("Main Subject", available_subjects)
                    
                    with col2:
                        class_room = st.text_input("Room Number", placeholder="e.g., 201")
                        class_schedule = st.text_input("Schedule", placeholder="e.g., Mon/Wed 10:00 AM")
                        max_students = st.number_input("Max Students", min_value=1, max_value=100, value=40)
                    
                    teacher_options = []
                    for t in teachers_data:
                        if t['status'] == 'active' and t.get('used_by_list'):
                            for teacher_use in t['used_by_list']:
                                teacher_options.append(f"{teacher_use['name']} ({teacher_use['email']})")
                    
                    if teacher_options:
                        selected_teacher = st.selectbox("Assign Teacher", teacher_options)
                        teacher_email = selected_teacher.split('(')[1].rstrip(')')
                        teacher_name = selected_teacher.split('(')[0].strip()
                    else:
                        st.warning("No teachers available")
                        teacher_email = None
                    
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
                            st.success(f"Class created! Code: {class_code}")
                            st.rerun()
        
        # Display all classes (everyone can see)
        st.subheader("📋 All Classes")
        for c in classes:
            with st.expander(f"📖 {c['name']} - {c['grade']} ({c['code']})"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Subject:** {c.get('subject', 'N/A')}")
                    st.write(f"**Teacher:** {c.get('teacher_name', 'Unknown')}")
                with col2:
                    st.write(f"**Room:** {c.get('room', 'TBD')}")
                    st.write(f"**Schedule:** {c.get('schedule', 'TBD')}")
                with col3:
                    st.write(f"**Students:** {len(c.get('students', []))}/{c.get('max_students', 40)}")
                
                # Show enrolled students with ranks
                if c.get('students'):
                    st.write("**👥 Enrolled Students:**")
                    for student_email in c['students']:
                        student = next((u for u in users if u['email'] == student_email), None)
                        if student:
                            rank = "Student"
                            if c.get('teacher') == student_email:
                                rank = "Teacher"
                            st.write(f"- {student['fullname']} <span class='rank-badge'>{rank}</span>", unsafe_allow_html=True)
                
                # Request to join button for students
                if user['role'] == 'student' and user['email'] not in c.get('students', []):
                    if st.button("📝 Request to Join", key=f"join_class_{c['code']}"):
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
    
    # ----- GROUPS (for all roles) -----
    elif menu == "Groups":
        st.markdown("<h2 style='text-align: center;'>👥 Community Groups</h2>", unsafe_allow_html=True)
        
        # Admin and teachers can create groups
        if user['role'] in ['admin', 'teacher']:
            with st.expander("➕ Create New Group"):
                with st.form("create_group"):
                    group_name = st.text_input("Group Name", placeholder="e.g., Math Study Group")
                    group_description = st.text_area("Description", placeholder="What is this group about?")
                    group_type = st.selectbox("Group Type", ["Study Group", "Club", "Sports Team", "Project Team", "Other"])
                    max_members = st.number_input("Max Members", min_value=2, max_value=100, value=20)
                    
                    # Option to add co-leaders
                    co_leader_options = []
                    for u in users:
                        if u['email'] != user['email']:
                            co_leader_options.append(f"{u['fullname']} ({u['email']}) - {u['role']}")
                    
                    co_leaders = st.multiselect("Co-Leaders (Optional)", co_leader_options)
                    co_leader_emails = [opt.split('(')[1].rstrip(')').split(' -')[0] for opt in co_leaders]
                    
                    if st.form_submit_button("✅ Create Group", use_container_width=True):
                        if group_name:
                            group_code = generate_group_code()
                            groups.append({
                                "id": generate_id("GRP"),
                                "code": group_code,
                                "name": group_name,
                                "description": group_description,
                                "type": group_type,
                                "leader": user['email'],
                                "leader_name": user['fullname'],
                                "co_leaders": co_leader_emails,
                                "created": datetime.now().strftime("%Y-%m-%d"),
                                "max_members": max_members,
                                "members": [user['email']] + co_leader_emails,
                                "pending_requests": [],
                                "status": "active"
                            })
                            save_school_data(school_code, "groups.json", groups)
                            school['stats']['groups'] = school['stats'].get('groups', 0) + 1
                            all_schools = load_all_schools()
                            all_schools[school_code] = school
                            save_all_schools(all_schools)
                            st.success(f"Group created! Code: {group_code}")
                            st.rerun()
        
        # Display all groups
        st.subheader("📋 All Groups")
        for g in groups:
            with st.expander(f"👥 {g['name']} - {g.get('type', 'Group')} ({g['code']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Description:** {g.get('description', 'No description')}")
                    st.write(f"**Leader:** {g.get('leader_name', 'Unknown')}")
                    if g.get('co_leaders'):
                        co_leader_names = []
                        for email in g['co_leaders']:
                            co_leader = next((u for u in users if u['email'] == email), None)
                            if co_leader:
                                co_leader_names.append(co_leader['fullname'])
                        st.write(f"**Co-Leaders:** {', '.join(co_leader_names)}")
                with col2:
                    st.write(f"**Members:** {len(g.get('members', []))}/{g.get('max_members', 20)}")
                    st.write(f"**Created:** {g['created']}")
                
                # Show all members with ranks
                if g.get('members'):
                    st.write("**👥 Members:**")
                    for member_email in g['members']:
                        member = next((u for u in users if u['email'] == member_email), None)
                        if member:
                            rank = get_user_rank_in_group(g, member_email)
                            st.write(f"- {member['fullname']} ({member['role']}) <span class='rank-badge'>{rank}</span>", unsafe_allow_html=True)
                
                # Request to join button
                user_rank = get_user_rank_in_group(g, user['email'])
                if user_rank == "Not a Member":
                    if st.button("📝 Request to Join", key=f"join_group_{g['code']}"):
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
                        st.success("Request sent!")
                        st.rerun()
                elif user_rank == "Request Pending":
                    st.info("⏳ Your request is pending approval")
    
    # ----- COMMUNITY (see all members) -----
    elif menu == "Community":
        st.markdown("<h2 style='text-align: center;'>🌍 School Community</h2>", unsafe_allow_html=True)
        
        all_members = get_all_community_members(school_code, user)
        friends = get_friends(school_code, user['email'])
        pending_requests = get_pending_requests(school_code, user['email'])
        
        # Filter options
        filter_role = st.selectbox("Filter by Role", ["All", "Admin", "Teacher", "Student", "Guardian"])
        
        filtered_members = all_members
        if filter_role != "All":
            filtered_members = [m for m in all_members if m['role'].lower() == filter_role.lower()]
        
        st.subheader(f"👥 Members ({len(filtered_members)})")
        
        for member in filtered_members:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
                with col1:
                    emoji = "👑" if member['role'] == 'admin' else "👨‍🏫" if member['role'] == 'teacher' else "👨‍🎓" if member['role'] == 'student' else "👪"
                    st.write(f"{emoji} **{member['fullname']}**")
                with col2:
                    st.write(f"Role: {member['role'].title()}")
                with col3:
                    if member['email'] in friends:
                        st.write("✅ Friend")
                    elif any(r['from'] == user['email'] and r['to'] == member['email'] and r['status'] == 'pending' for r in load_school_data(school_code, "friend_requests.json", [])):
                        st.write("⏳ Request Sent")
                    elif any(r['from'] == member['email'] and r['to'] == user['email'] and r['status'] == 'pending' for r in load_school_data(school_code, "friend_requests.json", [])):
                        st.write("📥 Request Received")
                with col4:
                    if member['email'] not in friends and member['email'] != user['email']:
                        # Check if request already sent
                        requests = load_school_data(school_code, "friend_requests.json", [])
                        request_exists = any(
                            (r['from'] == user['email'] and r['to'] == member['email'] and r['status'] == 'pending') or
                            (r['from'] == member['email'] and r['to'] == user['email'] and r['status'] == 'pending')
                            for r in requests
                        )
                        if not request_exists:
                            if st.button("➕ Add Friend", key=f"add_{member['email']}"):
                                send_friend_request(school_code, user['email'], member['email'])
                                st.success("Friend request sent!")
                                st.rerun()
                st.divider()
    
    # ----- FRIENDS & REQUESTS -----
    elif menu.startswith("Friends"):
        st.markdown("<h2 style='text-align: center;'>🤝 Friends</h2>", unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["✅ My Friends", "📥 Friend Requests", "📤 Sent Requests"])
        
        with tab1:
            friends = get_friends(school_code, user['email'])
            if friends:
                for friend_email in friends:
                    friend = next((u for u in users if u['email'] == friend_email), None)
                    if friend:
                        with st.container():
                            col1, col2, col3 = st.columns([2, 2, 1])
                            with col1:
                                emoji = "👑" if friend['role'] == 'admin' else "👨‍🏫" if friend['role'] == 'teacher' else "👨‍🎓" if friend['role'] == 'student' else "👪"
                                st.write(f"{emoji} **{friend['fullname']}**")
                            with col2:
                                st.write(f"Role: {friend['role'].title()}")
                            with col3:
                                if st.button("💬 Chat", key=f"chat_friend_{friend_email}"):
                                    st.session_state.chat_with = friend_email
                                    st.session_state.menu_index = options.index("Chat💬")
                                    st.rerun()
                            st.divider()
            else:
                st.info("No friends yet. Go to Community to add friends!")
        
        with tab2:
            pending = get_pending_requests(school_code, user['email'])
            if pending:
                for req in pending:
                    sender = next((u for u in users if u['email'] == req['from']), None)
                    if sender:
                        with st.container():
                            col1, col2, col3 = st.columns([2, 2, 2])
                            with col1:
                                emoji = "👑" if sender['role'] == 'admin' else "👨‍🏫" if sender['role'] == 'teacher' else "👨‍🎓" if sender['role'] == 'student' else "👪"
                                st.write(f"{emoji} **{sender['fullname']}**")
                            with col2:
                                st.write(f"Requested: {req['date'][:16]}")
                            with col3:
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    if st.button("✅ Accept", key=f"accept_{req['id']}"):
                                        accept_friend_request(school_code, req['id'])
                                        st.rerun()
                                with col_b:
                                    if st.button("❌ Decline", key=f"decline_{req['id']}"):
                                        req['status'] = 'declined'
                                        save_school_data(school_code, "friend_requests.json", pending)
                                        st.rerun()
                            st.divider()
            else:
                st.info("No pending friend requests")
        
        with tab3:
            all_requests = load_school_data(school_code, "friend_requests.json", [])
            sent = [r for r in all_requests if r['from'] == user['email'] and r['status'] == 'pending']
            if sent:
                for req in sent:
                    recipient = next((u for u in users if u['email'] == req['to']), None)
                    if recipient:
                        with st.container():
                            col1, col2, col3 = st.columns([2, 2, 1])
                            with col1:
                                emoji = "👑" if recipient['role'] == 'admin' else "👨‍🏫" if recipient['role'] == 'teacher' else "👨‍🎓" if recipient['role'] == 'student' else "👪"
                                st.write(f"{emoji} **{recipient['fullname']}**")
                            with col2:
                                st.write(f"Sent: {req['date'][:16]}")
                            with col3:
                                st.write("⏳ Pending")
                            st.divider()
            else:
                st.info("No sent requests")
    
    # ----- CHAT -----
    elif menu.startswith("Chat"):
        st.markdown("<h2 style='text-align: center;'>💬 Messages</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Conversations**")
            friends = get_friends(school_code, user['email'])
            
            if friends:
                for friend_email in friends:
                    friend = next((u for u in users if u['email'] == friend_email), None)
                    if friend:
                        # Get last message
                        conv_id = f"{min(user['email'], friend_email)}_{max(user['email'], friend_email)}"
                        messages = load_school_data(school_code, "messages.json", [])
                        conv_msgs = [m for m in messages if m['conversation_id'] == conv_id]
                        conv_msgs.sort(key=lambda x: x['timestamp'])
                        
                        last_msg = conv_msgs[-1]['timestamp'][:16] if conv_msgs else ""
                        unread = len([m for m in conv_msgs if m['recipient'] == user['email'] and not m['read']])
                        
                        if st.button(f"{'👑 ' if friend['role']=='admin' else '👨‍🏫 ' if friend['role']=='teacher' else '👨‍🎓 ' if friend['role']=='student' else '👪 '}{friend['fullname']}{f' ({unread})' if unread>0 else ''}\n{last_msg}", key=f"chat_{friend_email}", use_container_width=True):
                            st.session_state.chat_with = friend_email
                            st.rerun()
            else:
                st.info("Add friends to start chatting!")
        
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
                st.info("Select a conversation to start chatting")
    
    # ----- PROFILE (for all roles) -----
    elif menu == "Profile":
        st.markdown("<h2 style='text-align: center;'>👤 My Profile</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if user.get('profile_pic'):
                st.image(user['profile_pic'], width=150)
            else:
                emoji = "👑" if user['role'] == 'admin' else "👨‍🏫" if user['role'] == 'teacher' else "👨‍🎓" if user['role'] == 'student' else "👪"
                st.markdown(f"<h1 style='font-size: 5rem; text-align: center;'>{emoji}</h1>", unsafe_allow_html=True)
            
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
                bio = st.text_area("Bio", user.get('bio', ''), height=100)
                
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
            
            if user.get('admission_number'):
                st.info(f"🎫 Admission Number: **{user['admission_number']}**")
    
    # ----- DASHBOARD (simplified for each role) -----
    elif menu == "Dashboard":
        st.markdown(f"<h2 style='text-align: center;'>Welcome, {user['fullname']}!</h2>", unsafe_allow_html=True)
        
        if user['role'] == 'admin':
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Students", school['stats'].get('students', 0))
            col2.metric("Teachers", school['stats'].get('teachers', 0))
            col3.metric("Guardians", school['stats'].get('guardians', 0))
            col4.metric("Classes", school['stats'].get('classes', 0))
            col5.metric("Groups", school['stats'].get('groups', 0))
            
            pending = len([r for r in class_requests if r['status']=='pending']) + len([r for r in group_requests if r['status']=='pending'])
            if pending > 0:
                st.warning(f"📌 {pending} pending requests")
        
        elif user['role'] == 'teacher':
            my_classes = [c for c in classes if c.get('teacher') == user['email']]
            my_groups = [g for g in groups if g.get('leader') == user['email'] or user['email'] in g.get('co_leaders', [])]
            col1, col2, col3 = st.columns(3)
            col1.metric("My Classes", len(my_classes))
            col2.metric("My Groups", len(my_groups))
            col3.metric("Assignments", len([a for a in assignments if a.get('teacher') == user['email']]))
        
        elif user['role'] == 'student':
            my_classes = [c for c in classes if user['email'] in c.get('students', [])]
            my_groups = [g for g in groups if user['email'] in g.get('members', [])]
            col1, col2, col3 = st.columns(3)
            col1.metric("My Classes", len(my_classes))
            col2.metric("My Groups", len(my_groups))
            col3.metric("Admission", user['admission_number'][:10] + "...")
        
        else:  # guardian
            st.info(f"Linked to {len(user.get('linked_students', []))} student(s)")
            for adm in user.get('linked_students', []):
                student = next((u for u in users if u.get('admission_number') == adm), None)
                if student:
                    st.write(f"**{student['fullname']}** - {adm}")

else:
    st.error("Something went wrong")
    if st.button("Restart"):
        st.session_state.page = 'welcome'
        st.rerun()
