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
import time

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="✨ Golden School Community Hub ✨",
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

# ============ GOLDEN GRADIENT BACKGROUND ============
def get_golden_gradient():
    """Returns a beautiful golden gradient for sidebar"""
    return """
    background: linear-gradient(135deg, 
        #cfa668, #e5b873, #f5d742, #e6be5a, #d4a545, #c1933a, #ad7e2e
    );
    background-size: 300% 300%;
    animation: golden-shimmer 8s ease infinite;
    """

def get_main_gradient():
    """Returns main background gradient"""
    return """
    background: linear-gradient(-45deg, 
        #2b2b2b, #3d2b1a, #4a3723, #3d2b1a, #2b2b2b
    );
    background-size: 400% 400%;
    animation: gradient 15s ease infinite;
    """

# ============ CUSTOM CSS WITH GOLDEN SIDEBAR ============
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    * {{
        font-family: 'Poppins', sans-serif;
        box-sizing: border-box;
    }}
    
    @keyframes gradient {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    
    @keyframes golden-shimmer {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
    
    /* Main background */
    body {{
        {get_main_gradient()}
        margin: 0;
        padding: 0;
        min-height: 100vh;
    }}
    
    .stApp {{
        background: transparent !important;
    }}
    
    /* Main content area */
    .main .block-container {{
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 215, 0, 0.3);
        position: relative;
        z-index: 10;
    }}
    
    /* Golden Sidebar */
    section[data-testid="stSidebar"] {{
        {get_golden_gradient()}
        backdrop-filter: blur(5px) !important;
        border-right: 2px solid rgba(255, 215, 0, 0.4) !important;
        box-shadow: 5px 0 30px rgba(218, 165, 32, 0.4) !important;
        z-index: 20;
    }}
    
    section[data-testid="stSidebar"] > div {{
        background: rgba(0, 0, 0, 0.2) !important;
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
        color: #FFD700 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
        font-weight: 600 !important;
    }}
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {{
        background: rgba(0, 0, 0, 0.3) !important;
        border-radius: 12px !important;
        padding: 0.5rem !important;
        border: 1px solid rgba(255, 215, 0, 0.3) !important;
        margin: 0.8rem 0 !important;
    }}
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {{
        background: transparent !important;
        border-radius: 8px !important;
        padding: 8px 10px !important;
        margin: 2px 0 !important;
        transition: all 0.2s ease !important;
        color: #FFD700 !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
    }}
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {{
        background: rgba(255, 215, 0, 0.2) !important;
        transform: translateX(5px) !important;
    }}
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] {{
        background: rgba(255, 215, 0, 0.3) !important;
        border-left: 4px solid #FFD700 !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 10px rgba(255, 215, 0, 0.3) !important;
    }}
    
    section[data-testid="stSidebar"] .stButton button {{
        background: linear-gradient(135deg, #FFD700, #DAA520) !important;
        color: #2b2b2b !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        margin: 0.5rem 0 !important;
        box-shadow: 0 4px 15px rgba(218, 165, 32, 0.4) !important;
    }}
    
    section[data-testid="stSidebar"] .stButton button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.6) !important;
    }}
    
    /* School header in sidebar */
    .school-header {{
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid #FFD700;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 12px;
        text-align: center;
    }}
    
    .school-header h2 {{
        color: #FFD700 !important;
        margin: 0;
        font-size: 1.3rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }}
    
    .school-code {{
        background: rgba(0, 0, 0, 0.3);
        padding: 4px;
        border-radius: 20px;
        margin-top: 5px;
        border: 1px solid #FFD700;
    }}
    
    .school-code code {{
        background: transparent !important;
        color: #FFD700 !important;
        font-size: 0.8rem;
        font-weight: 700;
    }}
    
    /* Profile card in sidebar */
    .profile-card {{
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid #FFD700;
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    
    /* Input field styling */
    .stSelectbox div[data-baseweb="select"] {{
        background: white !important;
        border: 2px solid #FFD700 !important;
        border-radius: 10px !important;
        color: #000000 !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }}
    
    .stSelectbox div[data-baseweb="select"]:hover {{
        border-color: #DAA520 !important;
        box-shadow: 0 0 15px rgba(218, 165, 32, 0.3) !important;
    }}
    
    .stSelectbox div[data-baseweb="select"] span {{
        color: #000000 !important;
        font-weight: 500 !important;
    }}
    
    .stSelectbox div[role="listbox"] {{
        background: white !important;
        border: 2px solid #FFD700 !important;
        border-radius: 10px !important;
        box-shadow: 0 5px 20px rgba(0,0,0,0.2) !important;
    }}
    
    .stSelectbox div[role="listbox"] div {{
        color: #000000 !important;
        font-weight: 500 !important;
        padding: 8px 12px !important;
    }}
    
    .stSelectbox div[role="listbox"] div:hover {{
        background: linear-gradient(135deg, #FFD70020, #DAA52020) !important;
    }}
    
    .stTextInput input, 
    .stTextArea textarea, 
    .stDateInput input,
    .stNumberInput input {{
        background: white !important;
        border: 2px solid #FFD700 !important;
        border-radius: 10px !important;
        padding: 0.6rem 1rem !important;
        font-size: 0.95rem !important;
        color: #000000 !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }}
    
    .stTextInput input:focus, 
    .stTextArea textarea:focus,
    .stDateInput input:focus,
    .stNumberInput input:focus {{
        border-color: #DAA520 !important;
        box-shadow: 0 0 15px rgba(218, 165, 32, 0.3) !important;
    }}
    
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label,
    .stDateInput label,
    .stNumberInput label {{
        color: #333333 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }}
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {{
        background: linear-gradient(135deg, #FFD700, #DAA520) !important;
        border-radius: 12px !important;
        padding: 0.3rem !important;
        gap: 0.3rem;
        margin-bottom: 1.5rem !important;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        color: #2b2b2b !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: rgba(0, 0, 0, 0.2) !important;
        color: #000000 !important;
    }}
    
    /* Headers */
    h1 {{
        background: linear-gradient(135deg, #FFD700, #DAA520, #b8860b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        text-align: center;
        margin-bottom: 1.5rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }}
    
    /* Golden cards */
    .golden-card {{
        background: linear-gradient(135deg, #ffffff, #fff8e7);
        border-left: 6px solid #FFD700;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(218, 165, 32, 0.2);
    }}
    
    /* Performance badges */
    .performance-excellent {{
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
        display: inline-block;
    }}
    
    .performance-good {{
        background: linear-gradient(135deg, #17a2b8, #6f42c1);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
        display: inline-block;
    }}
    
    .performance-average {{
        background: linear-gradient(135deg, #ffc107, #fd7e14);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
        display: inline-block;
    }}
    
    .performance-needs-improvement {{
        background: linear-gradient(135deg, #dc3545, #c82333);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.8rem;
        display: inline-block;
    }}
    
    /* Chat styling */
    .chat-container {{
        background: rgba(255, 255, 255, 0.8);
        border-radius: 16px;
        padding: 20px;
        height: 400px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 15px;
        border: 1px solid #FFD700;
    }}
    
    .chat-message-wrapper {{
        display: flex;
        margin-bottom: 10px;
        animation: fadeIn 0.3s ease;
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .chat-message-sent {{
        justify-content: flex-end;
    }}
    
    .chat-message-received {{
        justify-content: flex-start;
    }}
    
    .chat-bubble {{
        max-width: 70%;
        padding: 12px 16px;
        border-radius: 20px;
        position: relative;
        word-wrap: break-word;
    }}
    
    .chat-bubble-sent {{
        background: linear-gradient(135deg, #FFD700, #DAA520);
        color: #2b2b2b;
        border-bottom-right-radius: 4px;
    }}
    
    .chat-bubble-received {{
        background: rgba(255, 255, 255, 0.9);
        color: #333333;
        border-bottom-left-radius: 4px;
        border: 1px solid #FFD700;
    }}
    
    .chat-sender-info {{
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 4px;
    }}
    
    .chat-sender-name {{
        font-size: 0.8rem;
        color: #DAA520;
        font-weight: 600;
    }}
    
    .chat-time {{
        font-size: 0.65rem;
        color: rgba(51, 51, 51, 0.5);
        margin-top: 4px;
        text-align: right;
    }}
    
    /* Main navigation buttons */
    .main-nav-button {{
        background: linear-gradient(135deg, #FFD700, #DAA520);
        color: #2b2b2b;
        border: none;
        border-radius: 15px;
        padding: 20px;
        font-size: 1.2rem;
        font-weight: 700;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(218, 165, 32, 0.3);
        margin: 10px 0;
    }}
    
    .main-nav-button:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(255, 215, 0, 0.4);
    }}
    
    /* Class cards */
    .class-card {{
        background: white;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        border-left: 4px solid #FFD700;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    
    /* Member cards */
    .member-card {{
        background: white;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 15px;
        border: 1px solid #FFD700;
    }}
    
    .member-pic {{
        width: 50px;
        height: 50px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #FFD700;
    }}
    
    /* Badges */
    .request-badge {{
        background: #FFD700;
        color: #2b2b2b;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-left: 8px;
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
    year = datetime.now().strftime("%y")
    random_num = ''.join(random.choices(string.digits, k=4))
    return f"ADM/{year}/{random_num}"

# ============ DATA STORAGE ============
DATA_DIR = Path("golden_school_data")
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

def decline_friend_request(school_code, request_id):
    requests = load_school_data(school_code, "friend_requests.json", [])
    for req in requests:
        if req['id'] == request_id:
            req['status'] = 'declined'
            break
    save_school_data(school_code, "friend_requests.json", requests)

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

def get_sent_requests(school_code, user_email):
    requests = load_school_data(school_code, "friend_requests.json", [])
    return [r for r in requests if r['from'] == user_email and r['status'] == 'pending']

def send_message(school_code, sender_email, recipient_email, message, attachment=None):
    messages = load_school_data(school_code, "messages.json", [])
    messages.append({
        "id": generate_id("MSG"),
        "sender": sender_email,
        "recipient": recipient_email,
        "message": message,
        "attachment": attachment,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "read": False,
        "deleted": False,
        "conversation_id": f"{min(sender_email, recipient_email)}_{max(sender_email, recipient_email)}"
    })
    save_school_data(school_code, "messages.json", messages)

def mark_as_read(message_id, school_code):
    messages = load_school_data(school_code, "messages.json", [])
    for msg in messages:
        if msg['id'] == message_id:
            msg['read'] = True
            break
    save_school_data(school_code, "messages.json", messages)

def get_unread_count(user_email, school_code):
    messages = load_school_data(school_code, "messages.json", [])
    return len([m for m in messages if m['recipient'] == user_email and not m.get('read', False) and not m.get('deleted', False)])

# ============ GROUP CHAT FUNCTIONS ============
def create_group_chat(school_code, group_name, created_by, members):
    group_chats = load_school_data(school_code, "group_chats.json", [])
    group_chat = {
        "id": generate_id("GPC"),
        "name": group_name,
        "created_by": created_by,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "members": members,
        "messages": [],
        "admins": [created_by]
    }
    group_chats.append(group_chat)
    save_school_data(school_code, "group_chats.json", group_chats)
    return group_chat['id']

def send_group_message(school_code, group_id, sender_email, message, attachment=None):
    group_chats = load_school_data(school_code, "group_chats.json", [])
    for group in group_chats:
        if group['id'] == group_id:
            group['messages'].append({
                "id": generate_id("GPM"),
                "sender": sender_email,
                "message": message,
                "attachment": attachment,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "read_by": [sender_email]
            })
            break
    save_school_data(school_code, "group_chats.json", group_chats)

def get_user_groups(school_code, user_email):
    groups = load_school_data(school_code, "groups.json", [])
    group_chats = load_school_data(school_code, "group_chats.json", [])
    user_groups = []
    
    for group in groups:
        if user_email in group.get('members', []):
            user_groups.append({
                "id": group['code'],
                "name": group['name'],
                "type": "regular",
                "members": group.get('members', []),
                "chat_id": None
            })
    
    for chat in group_chats:
        if user_email in chat.get('members', []):
            user_groups.append({
                "id": chat['id'],
                "name": chat['name'],
                "type": "chat",
                "members": chat.get('members', []),
                "chat_id": chat['id']
            })
    
    return user_groups

# ============ ATTACHMENT FUNCTIONS ============
def save_attachment(uploaded_file):
    if uploaded_file:
        bytes_data = uploaded_file.getvalue()
        b64 = base64.b64encode(bytes_data).decode()
        return {
            "name": uploaded_file.name,
            "type": uploaded_file.type,
            "data": b64,
            "size": len(bytes_data)
        }
    return None

def display_attachment(attachment):
    if attachment:
        file_ext = attachment['name'].split('.')[-1].lower()
        if file_ext in ['jpg', 'jpeg', 'png', 'gif']:
            st.image(f"data:{attachment['type']};base64,{attachment['data']}", width=200)
        else:
            st.markdown(f"📎 [{attachment['name']}](data:{attachment['type']};base64,{attachment['data']} \"{attachment['name']}\")")

# ============ SCHOOL MANAGEMENT FUNCTIONS ============
def calculate_student_performance(grades, student_email):
    student_grades = [g for g in grades if g['student_email'] == student_email]
    if not student_grades:
        return {"average": 0, "subjects": {}, "rank": "N/A"}
    
    subjects = {}
    total = 0
    for grade in student_grades:
        subjects[grade['subject']] = grade['score']
        total += grade['score']
    
    avg = total / len(student_grades)
    
    if avg >= 80:
        rank = "Excellent"
    elif avg >= 70:
        rank = "Good"
    elif avg >= 50:
        rank = "Average"
    else:
        rank = "Needs Improvement"
    
    return {"average": round(avg, 2), "subjects": subjects, "rank": rank}

def add_academic_record(school_code, student_email, subject, score, term, year, teacher_email):
    grades = load_school_data(school_code, "academic_records.json", [])
    grades.append({
        "id": generate_id("GRD"),
        "student_email": student_email,
        "subject": subject,
        "score": score,
        "term": term,
        "year": year,
        "teacher_email": teacher_email,
        "date": datetime.now().strftime("%Y-%m-%d")
    })
    save_school_data(school_code, "academic_records.json", grades)

def add_attendance_record(school_code, student_email, date, status, remarks=""):
    attendance = load_school_data(school_code, "attendance.json", [])
    attendance.append({
        "id": generate_id("ATT"),
        "student_email": student_email,
        "date": date,
        "status": status,
        "remarks": remarks,
        "recorded_by": st.session_state.user['email'],
        "recorded_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    save_school_data(school_code, "attendance.json", attendance)

def add_fee_record(school_code, student_email, amount, date, type_, status, receipt_no=None):
    fees = load_school_data(school_code, "fees.json", [])
    fees.append({
        "id": generate_id("FEE"),
        "student_email": student_email,
        "amount": amount,
        "date": date,
        "type": type_,
        "status": status,
        "receipt_no": receipt_no or generate_id("RCP"),
        "recorded_by": st.session_state.user['email']
    })
    save_school_data(school_code, "fees.json", fees)

def add_disciplinary_record(school_code, student_email, incident, action, date, recorded_by):
    discipline = load_school_data(school_code, "discipline.json", [])
    discipline.append({
        "id": generate_id("DSC"),
        "student_email": student_email,
        "incident": incident,
        "action_taken": action,
        "date": date,
        "recorded_by": recorded_by,
        "recorded_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    save_school_data(school_code, "discipline.json", discipline)

def add_teacher_review(school_code, teacher_email, student_email, review_text, rating, date):
    reviews = load_school_data(school_code, "teacher_reviews.json", [])
    reviews.append({
        "id": generate_id("REV"),
        "teacher_email": teacher_email,
        "student_email": student_email,
        "review_text": review_text,
        "rating": rating,
        "date": date,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    save_school_data(school_code, "teacher_reviews.json", reviews)

def add_parent_feedback(school_code, guardian_email, student_email, feedback_text, date):
    feedback = load_school_data(school_code, "parent_feedback.json", [])
    feedback.append({
        "id": generate_id("FDB"),
        "guardian_email": guardian_email,
        "student_email": student_email,
        "feedback_text": feedback_text,
        "date": date,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    save_school_data(school_code, "parent_feedback.json", feedback)

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
if 'group_chat_with' not in st.session_state:
    st.session_state.group_chat_with = None
if 'main_nav' not in st.session_state:
    st.session_state.main_nav = 'School Community'

# ============ MAIN APP ============

# ----- WELCOME PAGE -----
if st.session_state.page == 'welcome':
    st.markdown('<h1>✨ Golden School Community Hub ✨</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #333333; font-size: 1.2rem;">Connect • Collaborate • Shine Together</p>', unsafe_allow_html=True)
    st.divider()
    
    # MAIN NAVIGATION BUTTONS
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="main-nav-button">
            🏫 School Community
        </div>
        """, unsafe_allow_html=True)
        if st.button("🏫 School Community", key="nav_community", use_container_width=True):
            st.session_state.main_nav = 'School Community'
    
    with col2:
        st.markdown("""
        <div class="main-nav-button">
            📊 School Management
        </div>
        """, unsafe_allow_html=True)
        if st.button("📊 School Management", key="nav_management", use_container_width=True):
            st.session_state.main_nav = 'School Management'
    
    with col3:
        st.markdown("""
        <div class="main-nav-button">
            👤 Personal Dashboard
        </div>
        """, unsafe_allow_html=True)
        if st.button("👤 Personal Dashboard", key="nav_personal", use_container_width=True):
            st.session_state.main_nav = 'Personal Dashboard'
    
    st.divider()
    
    if st.session_state.main_nav == 'School Community':
        st.markdown("""
        <div class="golden-card" style="text-align: center;">
            <h3>🏫 School Community</h3>
            <p>Connect with teachers, students, and guardians. Join groups, chat, and collaborate!</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["👑 Admin", "🏫 Create", "👨‍🏫 Teachers", "👨‍🎓 Students", "👪 Guardians"])
        
        with tab1:
            col1, col2 = st.columns([1,1])
            with col1:
                with st.form("admin_login"):
                    st.subheader("🌟 Admin Login")
                    school_code = st.text_input("🏫 School Code")
                    admin_email = st.text_input("📧 Email")
                    admin_password = st.text_input("🔐 Password", type="password")
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
        
        with tab2:
            col1, col2 = st.columns([1,1])
            with col1:
                with st.form("create_school"):
                    st.subheader("🚀 Start Your Journey")
                    school_name = st.text_input("🏫 School Name")
                    admin_name = st.text_input("👤 Your Full Name")
                    admin_email = st.text_input("📧 Your Email")
                    password = st.text_input("🔐 Password", type="password")
                    confirm = st.text_input("🔐 Confirm Password", type="password")
                    city = st.text_input("🏙️ City")
                    state = st.text_input("🗺️ State/Province")
                    motto = st.text_input("✨ School Motto")
                    
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
                            save_school_data(code, "group_chats.json", [])
                            save_school_data(code, "academic_records.json", [])
                            save_school_data(code, "attendance.json", [])
                            save_school_data(code, "fees.json", [])
                            save_school_data(code, "discipline.json", [])
                            save_school_data(code, "teacher_reviews.json", [])
                            save_school_data(code, "parent_feedback.json", [])
                            
                            st.session_state.current_school = new_school
                            st.session_state.user = users[0]
                            st.session_state.page = 'dashboard'
                            st.success(f"✨ School Created! Your Code: **{code}**")
                            st.rerun()
        
        with tab3:
            subtab1, subtab2 = st.tabs(["🔐 Login", "📝 Register"])
            
            with subtab1:
                with st.form("teacher_login"):
                    st.subheader("👨‍🏫 Teacher Login")
                    school_code = st.text_input("🏫 School Code")
                    email = st.text_input("📧 Email")
                    password = st.text_input("🔐 Password", type="password")
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
                with st.form("teacher_register"):
                    st.subheader("📝 New Teacher")
                    school_code = st.text_input("🏫 School Code")
                    teacher_code = st.text_input("🔑 Teacher Code")
                    fullname = st.text_input("👤 Full Name")
                    email = st.text_input("📧 Email")
                    password = st.text_input("🔐 Password", type="password")
                    confirm = st.text_input("🔐 Confirm", type="password")
                    
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
                                for t in teachers_data:
                                    if t['code'] == teacher_code.upper() and t['status'] == 'active':
                                        valid = True
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
        
        with tab4:
            subtab1, subtab2 = st.tabs(["🔐 Login", "📝 Register"])
            
            with subtab1:
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
                with st.form("student_register"):
                    st.subheader("📝 New Student")
                    school_code = st.text_input("🏫 School Code")
                    fullname = st.text_input("👤 Full Name")
                    email = st.text_input("📧 Email (Optional)")
                    password = st.text_input("🔐 Password", type="password")
                    confirm = st.text_input("🔐 Confirm", type="password")
                    
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
        
        with tab5:
            subtab1, subtab2 = st.tabs(["🔐 Login", "📝 Register"])
            
            with subtab1:
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
                with st.form("guardian_register"):
                    st.subheader("📝 New Guardian")
                    st.info("You'll need the student's admission number")
                    school_code = st.text_input("🏫 School Code")
                    student_admission = st.text_input("🎫 Student's Admission Number")
                    fullname = st.text_input("👤 Your Full Name")
                    email = st.text_input("📧 Your Email")
                    phone = st.text_input("📱 Phone Number")
                    password = st.text_input("🔐 Password", type="password")
                    confirm = st.text_input("🔐 Confirm", type="password")
                    
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
    
    elif st.session_state.main_nav == 'School Management':
        st.markdown("""
        <div class="golden-card" style="text-align: center;">
            <h3>📊 School Management System</h3>
            <p>Complete school administration - Academics, Finance, Discipline, and more!</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.user and st.session_state.current_school:
            mgmt_tab1, mgmt_tab2, mgmt_tab3, mgmt_tab4, mgmt_tab5 = st.tabs([
                "🏫 Academic Records", "💰 Finance", "📋 Discipline", "📊 Reports", "⚙️ Administration"
            ])
            
            school_code = st.session_state.current_school['code']
            users = load_school_data(school_code, "users.json", [])
            students = [u for u in users if u['role'] == 'student']
            
            with mgmt_tab1:
                st.subheader("📚 Academic Records Management")
                
                academic_records = load_school_data(school_code, "academic_records.json", [])
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown("### ➕ Add Academic Record")
                    with st.form("add_academic_record"):
                        if students:
                            student = st.selectbox("Select Student", 
                                                 [f"{s['fullname']} ({s.get('admission_number', 'N/A')})" for s in students])
                            subject = st.selectbox("Subject", PRIMARY_SUBJECTS)
                            score = st.number_input("Score/Grade", min_value=0, max_value=100, value=0)
                            term = st.selectbox("Term", ["Term 1", "Term 2", "Term 3"])
                            year = st.number_input("Year", value=datetime.now().year, min_value=2020, max_value=2030)
                            
                            if st.form_submit_button("📝 Save Record"):
                                student_email = student.split('(')[1].rstrip(')') if '(' in student else student
                                add_academic_record(
                                    school_code, 
                                    student_email, 
                                    subject, 
                                    score, 
                                    term, 
                                    str(year), 
                                    st.session_state.user['email']
                                )
                                st.success("Academic record added successfully!")
                                st.rerun()
                
                with col2:
                    st.markdown("### 📊 Performance Overview")
                    if academic_records:
                        perf_data = []
                        for record in academic_records[-50:]:
                            student = next((s for s in students if s['email'] == record['student_email']), None)
                            if student:
                                perf_data.append({
                                    "Student": student['fullname'][:15] + "...",
                                    "Subject": record['subject'],
                                    "Score": record['score'],
                                    "Term": record['term']
                                })
                        
                        if perf_data:
                            df = pd.DataFrame(perf_data)
                            fig = px.bar(df, x="Student", y="Score", color="Subject", 
                                        title="Recent Academic Performance",
                                        color_discrete_sequence=px.colors.sequential.YlOrRd)
                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No academic records yet")
                
                st.markdown("### 📋 Recent Academic Records")
                if academic_records:
                    for record in reversed(academic_records[-10:]):
                        student = next((s for s in students if s['email'] == record['student_email']), None)
                        if student:
                            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                            with col1:
                                st.write(f"**{student['fullname']}**")
                            with col2:
                                st.write(record['subject'])
                            with col3:
                                st.write(f"Score: {record['score']}")
                            with col4:
                                st.write(record['term'])
                            st.divider()
                else:
                    st.info("No academic records available")
            
            with mgmt_tab2:
                st.subheader("💰 Finance Management")
                
                fees = load_school_data(school_code, "fees.json", [])
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown("### ➕ Add Fee Record")
                    with st.form("add_fee_record"):
                        if students:
                            student = st.selectbox("Select Student", 
                                                 [f"{s['fullname']} ({s.get('admission_number', 'N/A')})" for s in students])
                            amount = st.number_input("Amount (KES)", min_value=0.0, value=0.0, step=100.0)
                            fee_type = st.selectbox("Fee Type", ["Tuition", "Transport", "Lunch", "Development", "Uniform", "Other"])
                            status = st.selectbox("Payment Status", ["Paid", "Pending", "Overdue", "Partial"])
                            receipt_no = st.text_input("Receipt Number (Optional)")
                            
                            if st.form_submit_button("💾 Save Fee Record"):
                                student_email = student.split('(')[1].rstrip(')') if '(' in student else student
                                add_fee_record(
                                    school_code,
                                    student_email,
                                    amount,
                                    datetime.now().strftime("%Y-%m-%d"),
                                    fee_type,
                                    status,
                                    receipt_no if receipt_no else None
                                )
                                st.success("Fee record added successfully!")
                                st.rerun()
                
                with col2:
                    st.markdown("### 📊 Financial Summary")
                    if fees:
                        total_collected = sum([f['amount'] for f in fees if f['status'] == 'Paid'])
                        total_pending = sum([f['amount'] for f in fees if f['status'] in ['Pending', 'Overdue']])
                        
                        st.metric("Total Collected", f"KES {total_collected:,.0f}")
                        st.metric("Total Pending", f"KES {total_pending:,.0f}")
                        
                        fee_by_type = {}
                        for fee in fees:
                            fee_by_type[fee['type']] = fee_by_type.get(fee['type'], 0) + fee['amount']
                        
                        if fee_by_type:
                            df = pd.DataFrame(list(fee_by_type.items()), columns=['Type', 'Amount'])
                            fig = px.pie(df, values='Amount', names='Type', 
                                        title='Fees by Type',
                                        color_discrete_sequence=px.colors.sequential.YlOrRd)
                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No fee records yet")
                
                st.markdown("### 📋 Recent Fee Records")
                if fees:
                    for fee in reversed(fees[-10:]):
                        student = next((s for s in students if s['email'] == fee['student_email']), None)
                        if student:
                            col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
                            with col1:
                                st.write(f"**{student['fullname']}**")
                            with col2:
                                st.write(f"KES {fee['amount']:,.0f}")
                            with col3:
                                status_color = "🟢" if fee['status'] == "Paid" else "🟡" if fee['status'] == "Pending" else "🔴"
                                st.write(f"{status_color} {fee['status']}")
                            with col4:
                                st.write(f"Receipt: {fee.get('receipt_no', 'N/A')}")
                            st.divider()
                else:
                    st.info("No fee records available")
            
            with mgmt_tab3:
                st.subheader("📋 Discipline Management")
                
                discipline = load_school_data(school_code, "discipline.json", [])
                
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown("### ➕ Add Discipline Record")
                    with st.form("add_discipline_record"):
                        if students:
                            student = st.selectbox("Select Student", 
                                                 [f"{s['fullname']} ({s.get('admission_number', 'N/A')})" for s in students])
                            incident = st.text_area("Incident Description", height=100)
                            action_taken = st.text_area("Action Taken", height=100)
                            
                            if st.form_submit_button("📝 Save Record"):
                                student_email = student.split('(')[1].rstrip(')') if '(' in student else student
                                add_disciplinary_record(
                                    school_code,
                                    student_email,
                                    incident,
                                    action_taken,
                                    datetime.now().strftime("%Y-%m-%d"),
                                    st.session_state.user['email']
                                )
                                st.success("Discipline record added successfully!")
                                st.rerun()
                
                with col2:
                    st.markdown("### 📊 Discipline Summary")
                    if discipline:
                        total_cases = len(discipline)
                        unique_students = len(set([d['student_email'] for d in discipline]))
                        
                        st.metric("Total Cases", total_cases)
                        st.metric("Students Involved", unique_students)
                        
                        cases_by_month = {}
                        for d in discipline:
                            month = d['date'][:7]
                            cases_by_month[month] = cases_by_month.get(month, 0) + 1
                        
                        if cases_by_month:
                            df = pd.DataFrame(list(cases_by_month.items()), columns=['Month', 'Cases'])
                            fig = px.line(df, x='Month', y='Cases', 
                                         title='Disciplinary Cases Over Time',
                                         color_discrete_sequence=['#FFD700'])
                            st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No discipline records yet")
                
                st.markdown("### 📋 Recent Discipline Records")
                if discipline:
                    for disc in reversed(discipline[-10:]):
                        student = next((s for s in students if s['email'] == disc['student_email']), None)
                        if student:
                            with st.expander(f"Case: {disc['date']} - {student['fullname']}"):
                                st.write(f"**Incident:** {disc['incident']}")
                                st.write(f"**Action Taken:** {disc['action_taken']}")
                                st.write(f"**Recorded By:** {disc.get('recorded_by', 'Unknown')}")
                else:
                    st.info("No discipline records available")
            
            with mgmt_tab4:
                st.subheader("📊 Reports & Analytics")
                
                report_type = st.selectbox("Select Report Type", 
                                          ["Academic Performance", "Attendance Summary", "Financial Report", "Discipline Report"])
                
                if report_type == "Academic Performance":
                    if students:
                        selected_student = st.selectbox("Select Student for Detailed Report",
                                                       [f"{s['fullname']} ({s.get('admission_number', 'N/A')})" for s in students])
                        
                        if selected_student:
                            student_email = selected_student.split('(')[1].rstrip(')') if '(' in selected_student else selected_student
                            academic_records = load_school_data(school_code, "academic_records.json", [])
                            performance = calculate_student_performance(academic_records, student_email)
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Average Score", f"{performance['average']}%")
                            with col2:
                                st.metric("Rank", performance['rank'])
                            with col3:
                                st.metric("Subjects", len(performance['subjects']))
                            
                            if performance['subjects']:
                                subjects_data = [{"Subject": s, "Score": sc} for s, sc in performance['subjects'].items()]
                                df = pd.DataFrame(subjects_data)
                                fig = px.bar(df, x='Subject', y='Score', 
                                            title="Performance by Subject",
                                            color='Score',
                                            color_continuous_scale='YlOrRd')
                                st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No students available")
                
                elif report_type == "Financial Report":
                    fees = load_school_data(school_code, "fees.json", [])
                    
                    if fees:
                        col1, col2 = st.columns(2)
                        with col1:
                            start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
                        with col2:
                            end_date = st.date_input("End Date", datetime.now())
                        
                        filtered_fees = []
                        for fee in fees:
                            fee_date = datetime.strptime(fee['date'], "%Y-%m-%d").date()
                            if start_date <= fee_date <= end_date:
                                filtered_fees.append(fee)
                        
                        if filtered_fees:
                            total_revenue = sum([f['amount'] for f in filtered_fees if f['status'] == 'Paid'])
                            total_outstanding = sum([f['amount'] for f in filtered_fees if f['status'] in ['Pending', 'Overdue']])
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Total Revenue", f"KES {total_revenue:,.0f}")
                            with col2:
                                st.metric("Outstanding", f"KES {total_outstanding:,.0f}")
                            
                            daily_revenue = {}
                            for fee in filtered_fees:
                                if fee['status'] == 'Paid':
                                    daily_revenue[fee['date']] = daily_revenue.get(fee['date'], 0) + fee['amount']
                            
                            if daily_revenue:
                                df = pd.DataFrame(list(daily_revenue.items()), columns=['Date', 'Amount'])
                                fig = px.line(df, x='Date', y='Amount', 
                                             title='Daily Revenue',
                                             color_discrete_sequence=['#FFD700'])
                                st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No financial data available")
            
            with mgmt_tab5:
                st.subheader("⚙️ Administration")
                
                admin_tab1, admin_tab2, admin_tab3 = st.tabs(["👥 User Management", "🏫 School Settings", "📅 Academic Calendar"])
                
                with admin_tab1:
                    st.markdown("### User Management")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Users", len(users))
                    with col2:
                        st.metric("Students", len([u for u in users if u['role'] == 'student']))
                    with col3:
                        st.metric("Teachers", len([u for u in users if u['role'] == 'teacher']))
                    with col4:
                        st.metric("Guardians", len([u for u in users if u['role'] == 'guardian']))
                    
                    st.markdown("#### User Directory")
                    for user_entry in users[:20]:
                        with st.container():
                            col1, col2, col3 = st.columns([2, 1, 2])
                            with col1:
                                st.write(f"**{user_entry['fullname']}**")
                            with col2:
                                role_badge = "👑" if user_entry['role'] == 'admin' else "👨‍🏫" if user_entry['role'] == 'teacher' else "👨‍🎓" if user_entry['role'] == 'student' else "👪"
                                st.write(f"{role_badge} {user_entry['role'].title()}")
                            with col3:
                                st.write(user_entry['email'])
                            st.divider()
                
                with admin_tab2:
                    st.markdown("### School Settings")
                    
                    school = st.session_state.current_school
                    
                    with st.form("school_settings"):
                        school_name = st.text_input("School Name", school['name'])
                        motto = st.text_input("School Motto", school.get('motto', ''))
                        city = st.text_input("City", school.get('city', ''))
                        state = st.text_input("State/Province", school.get('state', ''))
                        
                        if st.form_submit_button("💾 Update Settings"):
                            all_schools = load_all_schools()
                            all_schools[school_code]['name'] = school_name
                            all_schools[school_code]['motto'] = motto
                            all_schools[school_code]['city'] = city
                            all_schools[school_code]['state'] = state
                            save_all_schools(all_schools)
                            
                            st.session_state.current_school = all_schools[school_code]
                            st.success("School settings updated!")
                            st.rerun()
                    
                    st.markdown(f"**School Code:** {school['code']}")
                    st.markdown(f"**Created:** {school.get('created', 'N/A')}")
                
                with admin_tab3:
                    st.markdown("### Academic Calendar")
                    
                    events = load_school_data(school_code, "events.json", [])
                    
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        with st.form("add_event"):
                            st.markdown("#### Add Event")
                            event_name = st.text_input("Event Name")
                            event_date = st.date_input("Date")
                            event_type = st.selectbox("Type", ["Holiday", "Exam", "Meeting", "Sports Day", "Other"])
                            description = st.text_area("Description")
                            
                            if st.form_submit_button("➕ Add Event"):
                                if event_name:
                                    events.append({
                                        "id": generate_id("EVT"),
                                        "name": event_name,
                                        "date": event_date.strftime("%Y-%m-%d"),
                                        "type": event_type,
                                        "description": description,
                                        "created_by": st.session_state.user['email']
                                    })
                                    save_school_data(school_code, "events.json", events)
                                    st.success("Event added!")
                                    st.rerun()
                    
                    with col2:
                        st.markdown("#### Upcoming Events")
                        if events:
                            events.sort(key=lambda x: x['date'])
                            for event in events[:10]:
                                event_date = datetime.strptime(event['date'], "%Y-%m-%d")
                                days_until = (event_date - datetime.now()).days
                                
                                if days_until >= 0:
                                    st.markdown(f"""
                                    <div class="golden-card">
                                        <strong>{event['name']}</strong><br>
                                        📅 {event['date']} ({days_until} days away)<br>
                                        📋 Type: {event['type']}
                                    </div>
                                    """, unsafe_allow_html=True)
                        else:
                            st.info("No events scheduled")
        else:
            st.warning("Please log in to access the School Management System")
    
    elif st.session_state.main_nav == 'Personal Dashboard':
        st.markdown("""
        <div class="golden-card" style="text-align: center;">
            <h3>👤 Personal Dashboard</h3>
            <p>Your personal information, performance, reviews, and achievements!</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.user and st.session_state.current_school:
            user = st.session_state.user
            school_code = st.session_state.current_school['code']
            users = load_school_data(school_code, "users.json", [])
            
            personal_tab1, personal_tab2, personal_tab3, personal_tab4 = st.tabs([
                "👤 Profile", "📊 My Performance", "⭐ Reviews & Feedback", "🏆 Achievements"
            ])
            
            with personal_tab1:
                st.markdown("### Personal Information")
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    if user.get('profile_pic'):
                        st.image(user['profile_pic'], width=150)
                    else:
                        emoji = "👑" if user['role'] == 'admin' else "👨‍🏫" if user['role'] == 'teacher' else "👨‍🎓" if user['role'] == 'student' else "👪"
                        st.markdown(f"<h1 style='font-size: 5rem; text-align: center;'>{emoji}</h1>", unsafe_allow_html=True)
                    
                    pic = st.file_uploader("📸 Update Photo", type=['png', 'jpg', 'jpeg'])
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
                    with st.form("update_personal_info"):
                        fullname = st.text_input("Full Name", user['fullname'])
                        email = st.text_input("Email", user['email'], disabled=True)
                        phone = st.text_input("Phone", user.get('phone', ''))
                        bio = st.text_area("Bio", user.get('bio', ''), height=100)
                        
                        if user['role'] == 'student':
                            st.info(f"🎫 Admission Number: {user.get('admission_number', 'N/A')}")
                        elif user['role'] == 'guardian':
                            linked_students = user.get('linked_students', [])
                            st.info(f"👪 Linked Students: {', '.join(linked_students)}")
                        
                        if st.form_submit_button("💾 Update Profile"):
                            for u in users:
                                if u['email'] == user['email']:
                                    u['fullname'] = fullname
                                    u['phone'] = phone
                                    u['bio'] = bio
                            save_school_data(school_code, "users.json", users)
                            user.update({'fullname': fullname, 'phone': phone, 'bio': bio})
                            st.success("Profile updated!")
                            st.rerun()
            
            with personal_tab2:
                st.markdown("### My Performance")
                
                if user['role'] == 'student':
                    academic_records = load_school_data(school_code, "academic_records.json", [])
                    attendance = load_school_data(school_code, "attendance.json", [])
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        performance = calculate_student_performance(academic_records, user['email'])
                        st.metric("Overall Average", f"{performance['average']}%")
                        
                        rank_class = "performance-excellent" if performance['average'] >= 80 else \
                                     "performance-good" if performance['average'] >= 70 else \
                                     "performance-average" if performance['average'] >= 50 else \
                                     "performance-needs-improvement"
                        st.markdown(f"<div class='{rank_class}' style='padding:10px; text-align:center;'>{performance['rank']}</div>", 
                                   unsafe_allow_html=True)
                        
                        if performance['subjects']:
                            subjects_df = pd.DataFrame(list(performance['subjects'].items()), 
                                                      columns=['Subject', 'Score'])
                            fig = px.bar(subjects_df, x='Subject', y='Score',
                                        title='Subject Performance',
                                        color='Score',
                                        color_continuous_scale='YlOrRd')
                            st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        student_attendance = [a for a in attendance if a['student_email'] == user['email']]
                        if student_attendance:
                            present = len([a for a in student_attendance if a['status'] == 'Present'])
                            absent = len([a for a in student_attendance if a['status'] == 'Absent'])
                            late = len([a for a in student_attendance if a['status'] == 'Late'])
                            
                            attendance_data = pd.DataFrame({
                                'Status': ['Present', 'Absent', 'Late'],
                                'Count': [present, absent, late]
                            })
                            
                            fig = px.pie(attendance_data, values='Count', names='Status',
                                        title='Attendance Summary',
                                        color_discrete_sequence=['#28a745', '#dc3545', '#ffc107'])
                            st.plotly_chart(fig, use_container_width=True)
                            
                            attendance_rate = (present / len(student_attendance)) * 100 if student_attendance else 0
                            st.metric("Attendance Rate", f"{attendance_rate:.1f}%")
                        else:
                            st.info("No attendance records yet")
                
                elif user['role'] == 'teacher':
                    classes = load_school_data(school_code, "classes.json", [])
                    my_classes = [c for c in classes if c.get('teacher') == user['email']]
                    
                    st.metric("Classes Taught", len(my_classes))
                    
                    if my_classes:
                        st.markdown("#### My Classes")
                        for c in my_classes:
                            students_count = len(c.get('students', []))
                            st.info(f"📚 {c['name']} - {students_count} students")
                    
                    reviews = load_school_data(school_code, "teacher_reviews.json", [])
                    my_reviews = [r for r in reviews if r['teacher_email'] == user['email']]
                    
                    if my_reviews:
                        avg_rating = sum([r['rating'] for r in my_reviews]) / len(my_reviews)
                        st.metric("Average Rating", f"{avg_rating:.1f}/5.0")
                
                elif user['role'] == 'guardian':
                    linked_students = user.get('linked_students', [])
                    
                    if linked_students:
                        academic_records = load_school_data(school_code, "academic_records.json", [])
                        
                        for adm in linked_students:
                            student = next((u for u in users if u.get('admission_number') == adm), None)
                            if student:
                                st.markdown(f"### {student['fullname']}")
                                performance = calculate_student_performance(academic_records, student['email'])
                                
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.metric("Average", f"{performance['average']}%")
                                with col2:
                                    rank_class = "performance-excellent" if performance['average'] >= 80 else \
                                                 "performance-good" if performance['average'] >= 70 else \
                                                 "performance-average" if performance['average'] >= 50 else \
                                                 "performance-needs-improvement"
                                    st.markdown(f"<div class='{rank_class}' style='padding:5px; text-align:center;'>{performance['rank']}</div>", 
                                               unsafe_allow_html=True)
                                st.divider()
                    else:
                        st.info("No linked students")
            
            with personal_tab3:
                st.markdown("### Reviews & Feedback")
                
                if user['role'] == 'student':
                    reviews = load_school_data(school_code, "teacher_reviews.json", [])
                    my_reviews = [r for r in reviews if r['student_email'] == user['email']]
                    
                    if my_reviews:
                        for review in reversed(my_reviews):
                            teacher = next((u for u in users if u['email'] == review['teacher_email']), None)
                            teacher_name = teacher['fullname'] if teacher else review['teacher_email']
                            
                            st.markdown(f"""
                            <div class="golden-card">
                                <strong>From: {teacher_name}</strong><br>
                                ⭐ Rating: {'⭐' * review['rating']}{'☆' * (5-review['rating'])}<br>
                                📅 {review['date']}<br>
                                💬 {review['review_text']}
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No reviews yet")
                
                elif user['role'] == 'teacher':
                    tab_a, tab_b = st.tabs(["Give Reviews", "Parent Feedback"])
                    
                    with tab_a:
                        st.markdown("#### Give Student Review")
                        
                        students = [u for u in users if u['role'] == 'student']
                        
                        with st.form("give_review"):
                            if students:
                                student = st.selectbox("Select Student", 
                                                     [f"{s['fullname']} ({s.get('admission_number', 'N/A')})" for s in students])
                                rating = st.slider("Rating", 1, 5, 3)
                                review_text = st.text_area("Review", height=100)
                                
                                if st.form_submit_button("📝 Submit Review"):
                                    student_email = student.split('(')[1].rstrip(')') if '(' in student else student
                                    add_teacher_review(
                                        school_code,
                                        user['email'],
                                        student_email,
                                        review_text,
                                        rating,
                                        datetime.now().strftime("%Y-%m-%d")
                                    )
                                    st.success("Review submitted!")
                                    st.rerun()
                    
                    with tab_b:
                        st.markdown("#### Parent Feedback")
                        
                        feedback = load_school_data(school_code, "parent_feedback.json", [])
                        if feedback:
                            for fb in reversed(feedback[-10:]):
                                guardian = next((u for u in users if u['email'] == fb['guardian_email']), None)
                                guardian_name = guardian['fullname'] if guardian else fb['guardian_email']
                                
                                st.markdown(f"""
                                <div class="golden-card">
                                    <strong>From: {guardian_name}</strong><br>
                                    📅 {fb['date']}<br>
                                    💬 {fb['feedback_text']}
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("No feedback yet")
                
                elif user['role'] == 'guardian':
                    st.markdown("#### Give Feedback")
                    
                    linked_students = [u for u in users if u.get('admission_number') in user.get('linked_students', [])]
                    
                    if linked_students:
                        with st.form("give_feedback"):
                            student = st.selectbox("Select Student", 
                                                 [f"{s['fullname']} ({s.get('admission_number', 'N/A')})" for s in linked_students])
                            feedback_text = st.text_area("Your Feedback", height=100)
                            
                            if st.form_submit_button("📝 Submit Feedback"):
                                student_email = student.split('(')[1].rstrip(')') if '(' in student else student
                                add_parent_feedback(
                                    school_code,
                                    user['email'],
                                    student_email,
                                    feedback_text,
                                    datetime.now().strftime("%Y-%m-%d")
                                )
                                st.success("Feedback submitted!")
                                st.rerun()
                    else:
                        st.info("No linked students")
            
            with personal_tab4:
                st.markdown("### 🏆 Achievements & Recognition")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("""
                    <div class="golden-card" style="text-align: center;">
                        <h1>📅</h1>
                        <h4>Perfect Attendance</h4>
                        <p>Term 1, 2024</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div class="golden-card" style="text-align: center;">
                        <h1>📚</h1>
                        <h4>Academic Excellence</h4>
                        <p>Term 2, 2024</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown("""
                    <div class="golden-card" style="text-align: center;">
                        <h1>🤝</h1>
                        <h4>Community Service</h4>
                        <p>Term 1, 2024</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("### 📊 Skill Development")
                
                skills = {
                    "Leadership": 80,
                    "Communication": 75,
                    "Teamwork": 90,
                    "Problem Solving": 70,
                    "Creativity": 85
                }
                
                for skill, level in skills.items():
                    st.markdown(f"**{skill}**")
                    st.progress(level/100, text=f"{level}%")
        else:
            st.warning("Please log in to view your personal dashboard")

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
    group_chats = load_school_data(school_code, "group_chats.json", [])
    class_requests = load_school_data(school_code, "class_requests.json", [])
    group_requests = load_school_data(school_code, "group_requests.json", [])
    
    unread_count = get_unread_count(user['email'], school_code)
    pending_friend_count = len(get_pending_requests(school_code, user['email']))
    
    # ============ GOLDEN SIDEBAR ============
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
            if user['role'] == 'admin':
                st.markdown("<h1 style='font-size: 2rem; margin: 0;'>👑</h1>", unsafe_allow_html=True)
            elif user['role'] == 'teacher':
                st.markdown("<h1 style='font-size: 2rem; margin: 0;'>👨‍🏫</h1>", unsafe_allow_html=True)
            elif user['role'] == 'student':
                st.markdown("<h1 style='font-size: 2rem; margin: 0;'>👨‍🎓</h1>", unsafe_allow_html=True)
            else:
                st.markdown("<h1 style='font-size: 2rem; margin: 0;'>👪</h1>", unsafe_allow_html=True)
        
        role_display = "ADMIN" if user['role'] == 'admin' else "TEACHER" if user['role'] == 'teacher' else "STUDENT" if user['role'] == 'student' else "GUARDIAN"
        
        st.markdown(f"""
        <div style="color: #FFD700; flex: 1; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
            <strong>{user['fullname']}</strong><br>
            <span style="background: rgba(0,0,0,0.3); color: #FFD700; padding: 2px 8px; border-radius: 12px; font-size: 0.7rem; border: 1px solid #FFD700;">{role_display}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        
        if user['role'] == 'admin':
            options = ["Dashboard", "Announcements", "Classes", "Groups", "Teachers", "Students", "Guardians", "Assignments", "Community", f"Chat 💬{f' ({unread_count})' if unread_count>0 else ''}", f"Group Chats 👥", f"Friends 🤝{f' ({pending_friend_count})' if pending_friend_count>0 else ''}", "Profile"]
        elif user['role'] == 'teacher':
            options = ["Dashboard", "Announcements", "My Classes", "Groups", "Assignments", "Community", f"Chat 💬{f' ({unread_count})' if unread_count>0 else ''}", f"Group Chats 👥", f"Friends 🤝{f' ({pending_friend_count})' if pending_friend_count>0 else ''}", "Profile"]
        elif user['role'] == 'student':
            options = ["Dashboard", "Announcements", "Browse Classes", "My Classes", "Groups", "Assignments", "Community", f"Chat 💬{f' ({unread_count})' if unread_count>0 else ''}", f"Group Chats 👥", f"Friends 🤝{f' ({pending_friend_count})' if pending_friend_count>0 else ''}", "Profile"]
        else:
            options = ["Dashboard", "Announcements", "My Student", "Assignments", "Community", f"Chat 💬{f' ({unread_count})' if unread_count>0 else ''}", f"Group Chats 👥", f"Friends 🤝{f' ({pending_friend_count})' if pending_friend_count>0 else ''}", "Profile"]
        
        if st.session_state.menu_index >= len(options):
            st.session_state.menu_index = 0
            
        menu = st.radio("", options, index=st.session_state.menu_index, label_visibility="collapsed")
        st.session_state.menu_index = options.index(menu)
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.current_school = None
            st.session_state.page = 'welcome'
            st.rerun()
    
    # ============ MAIN CONTENT ============
    
    if menu == "Dashboard":
        st.markdown(f"<h2 style='text-align: center;'>Welcome, {user['fullname']}!</h2>", unsafe_allow_html=True)
        
        if user['role'] == 'admin':
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("👨‍🎓 Students", school['stats'].get('students', 0))
            with col2:
                st.metric("👨‍🏫 Teachers", school['stats'].get('teachers', 0))
            with col3:
                st.metric("👪 Guardians", school['stats'].get('guardians', 0))
            with col4:
                st.metric("📚 Classes", school['stats'].get('classes', 0))
            with col5:
                st.metric("👥 Groups", school['stats'].get('groups', 0))
            
            st.subheader("📋 Recent Activity")
            recent_announcements = announcements[-3:] if announcements else []
            for ann in recent_announcements:
                st.info(f"📢 {ann['title']} - {ann['date'][:16]}")
            
            pending = len([r for r in class_requests if r['status']=='pending']) + len([r for r in group_requests if r['status']=='pending'])
            if pending > 0:
                st.warning(f"📌 You have {pending} pending requests to review")
        
        elif user['role'] == 'teacher':
            my_classes = [c for c in classes if c.get('teacher') == user['email']]
            my_groups = [g for g in groups if g.get('leader') == user['email'] or user['email'] in g.get('co_leaders', [])]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📚 My Classes", len(my_classes))
            with col2:
                st.metric("👥 My Groups", len(my_groups))
            with col3:
                my_assignments = len([a for a in assignments if a.get('created_by') == user['email']])
                st.metric("📝 My Assignments", my_assignments)
        
        elif user['role'] == 'student':
            my_classes = [c for c in classes if user['email'] in c.get('students', [])]
            my_groups = [g for g in groups if user['email'] in g.get('members', [])]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📚 My Classes", len(my_classes))
            with col2:
                st.metric("👥 My Groups", len(my_groups))
            with col3:
                st.metric("🎫 Admission", user['admission_number'][:10] + "...")
        
        else:
            st.info(f"👪 Linked to {len(user.get('linked_students', []))} student(s)")
            for adm in user.get('linked_students', []):
                student = next((u for u in users if u.get('admission_number') == adm), None)
                if student:
                    st.write(f"**{student['fullname']}** - {adm}")
    
    elif menu == "Announcements":
        st.markdown("<h2 style='text-align: center;'>📢 School Announcements</h2>", unsafe_allow_html=True)
        
        if user['role'] in ['admin', 'teacher']:
            with st.expander("➕ Create New Announcement"):
                with st.form("new_announcement"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        title = st.text_input("Title")
                        content = st.text_area("Content", height=100)
                        target = st.selectbox("Target Audience", ["Everyone", "Students Only", "Teachers Only", "Guardians Only"])
                    with col2:
                        important = st.checkbox("⭐ Mark as Important")
                        attachment = st.file_uploader("📎 Attachment", type=['pdf', 'docx', 'txt', 'jpg', 'png'])
                    
                    if st.form_submit_button("📢 Post Announcement", use_container_width=True):
                        if title and content:
                            attachment_data = save_attachment(attachment) if attachment else None
                            announcements.append({
                                "id": generate_id("ANN"),
                                "title": title,
                                "content": content,
                                "author": user['fullname'],
                                "author_email": user['email'],
                                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "target": target,
                                "important": important,
                                "attachment": attachment_data
                            })
                            save_school_data(school_code, "announcements.json", announcements)
                            st.success("Announcement posted!")
                            st.rerun()
        
        if announcements:
            for ann in reversed(announcements[-20:]):
                show = True
                if ann['target'] == "Students Only" and user['role'] != 'student':
                    show = False
                elif ann['target'] == "Teachers Only" and user['role'] != 'teacher':
                    show = False
                elif ann['target'] == "Guardians Only" and user['role'] != 'guardian':
                    show = False
                
                if show:
                    with st.container():
                        st.markdown(f"""
                        <div class="golden-card">
                            <h4>{ann['title']}{' ⭐' if ann.get('important') else ''}</h4>
                            <p><small>By {ann['author']} • {ann['date'][:16]}</small></p>
                            <p>{ann['content']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if ann.get('attachment'):
                            st.markdown("**📎 Attachment:**")
                            display_attachment(ann['attachment'])
        else:
            st.info("No announcements yet")
    
    elif menu == "Assignments":
        st.markdown("<h2 style='text-align: center;'>📝 Assignments</h2>", unsafe_allow_html=True)
        
        if user['role'] in ['admin', 'teacher']:
            with st.expander("➕ Create New Assignment"):
                with st.form("new_assignment"):
                    col1, col2 = st.columns(2)
                    with col1:
                        title = st.text_input("Assignment Title")
                        subject = st.selectbox("Subject", PRIMARY_SUBJECTS)
                        target_class = st.selectbox("Target Class", ["All Classes"] + [c['name'] for c in classes])
                    with col2:
                        due_date = st.date_input("Due Date")
                        total_points = st.number_input("Total Points", min_value=1, value=100)
                        attachment = st.file_uploader("📎 Attachment", type=['pdf', 'docx', 'txt', 'jpg', 'png'])
                    
                    description = st.text_area("Description", height=100)
                    
                    if st.form_submit_button("📝 Create Assignment", use_container_width=True):
                        if title and description:
                            attachment_data = save_attachment(attachment) if attachment else None
                            assignments.append({
                                "id": generate_id("ASN"),
                                "title": title,
                                "description": description,
                                "subject": subject,
                                "target_class": target_class,
                                "due_date": due_date.strftime("%Y-%m-%d"),
                                "total_points": total_points,
                                "created_by": user['email'],
                                "created_by_name": user['fullname'],
                                "created_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "attachment": attachment_data,
                                "submissions": []
                            })
                            save_school_data(school_code, "assignments.json", assignments)
                            st.success("Assignment created!")
                            st.rerun()
        
        st.subheader("📋 Current Assignments")
        
        user_assignments = []
        if user['role'] == 'student':
            my_classes = [c['name'] for c in classes if user['email'] in c.get('students', [])]
            user_assignments = [a for a in assignments if a.get('target_class') in ['All Classes'] + my_classes]
        elif user['role'] == 'teacher':
            user_assignments = [a for a in assignments if a.get('created_by') == user['email']]
        elif user['role'] == 'guardian':
            linked_adms = user.get('linked_students', [])
            linked_students = [u for u in users if u.get('admission_number') in linked_adms]
            student_classes = []
            for s in linked_students:
                student_classes.extend([c['name'] for c in classes if s['email'] in c.get('students', [])])
            user_assignments = [a for a in assignments if a.get('target_class') in ['All Classes'] + list(set(student_classes))]
        else:
            user_assignments = assignments
        
        if user_assignments:
            for a in user_assignments:
                with st.container():
                    st.markdown(f"""
                    <div class="golden-card">
                        <div style="display: flex; justify-content: space-between;">
                            <div>
                                <strong>{a['title']}</strong>
                                <span style="color: rgba(51,51,51,0.5); margin-left: 10px;">{a['subject']}</span>
                            </div>
                            <div style="color: {'#ff4444' if datetime.strptime(a['due_date'], '%Y-%m-%d') < datetime.now() else '#00d2ff'}">
                                Due: {a['due_date']}
                            </div>
                        </div>
                        <div style="margin: 10px 0;">{a['description']}</div>
                        <div style="display: flex; gap: 20px; font-size: 0.9rem;">
                            <span>Points: {a['total_points']}</span>
                            <span>Target: {a['target_class']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if a.get('attachment'):
                        st.markdown("**📎 Attachment:**")
                        display_attachment(a['attachment'])
        else:
            st.info("No assignments available")
    
    elif menu == "Community":
        st.markdown("<h2 style='text-align: center;'>🌍 School Community</h2>", unsafe_allow_html=True)
        
        all_members = [u for u in users if u['email'] != user['email']]
        friends = get_friends(school_code, user['email'])
        pending_requests = get_pending_requests(school_code, user['email'])
        sent_requests = get_sent_requests(school_code, user['email'])
        
        col1, col2 = st.columns([2, 1])
        with col1:
            filter_role = st.selectbox("Filter by Role", ["All", "Admin", "Teacher", "Student", "Guardian"])
        with col2:
            search_term = st.text_input("🔍 Search by name")
        
        filtered_members = all_members
        if filter_role != "All":
            filtered_members = [m for m in all_members if m['role'].lower() == filter_role.lower()]
        if search_term:
            filtered_members = [m for m in filtered_members if search_term.lower() in m['fullname'].lower()]
        
        st.subheader(f"👥 Members ({len(filtered_members)})")
        
        for member in filtered_members:
            is_friend = member['email'] in friends
            request_sent = any(r['to'] == member['email'] for r in sent_requests)
            request_received = any(r['from'] == member['email'] for r in pending_requests)
            
            with st.container():
                col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
                
                with col1:
                    if member.get('profile_pic'):
                        st.image(member['profile_pic'], width=40)
                    else:
                        emoji = "👑" if member['role'] == 'admin' else "👨‍🏫" if member['role'] == 'teacher' else "👨‍🎓" if member['role'] == 'student' else "👪"
                        st.markdown(f"<span style='font-size: 1.5rem;'>{emoji}</span>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"**{member['fullname']}**")
                    st.markdown(f"<span style='color: #FFD700; font-size: 0.8rem;'>{member['role'].title()}</span>", unsafe_allow_html=True)
                
                with col3:
                    if is_friend:
                        st.markdown("<span style='color: #28a745;'>✅ Friend</span>", unsafe_allow_html=True)
                    elif request_sent:
                        st.markdown("<span style='color: #ffc107;'>⏳ Request Sent</span>", unsafe_allow_html=True)
                    elif request_received:
                        st.markdown("<span style='color: #17a2b8;'>📥 Request Received</span>", unsafe_allow_html=True)
                    else:
                        st.markdown("<span style='color: rgba(51,51,51,0.5);'>Not Connected</span>", unsafe_allow_html=True)
                
                with col4:
                    if not is_friend and not request_sent and not request_received and member['email'] != user['email']:
                        if st.button("➕ Add Friend", key=f"add_{member['email']}"):
                            send_friend_request(school_code, user['email'], member['email'])
                            st.success("Friend request sent!")
                            st.rerun()
                    elif request_received:
                        if st.button("✅ Accept", key=f"accept_{member['email']}"):
                            req = next(r for r in pending_requests if r['from'] == member['email'])
                            accept_friend_request(school_code, req['id'])
                            st.success("Friend request accepted!")
                            st.rerun()
                    elif is_friend:
                        if st.button("💬 Chat", key=f"chat_{member['email']}"):
                            st.session_state.chat_with = member['email']
                            chat_options = [opt for opt in options if "Chat" in opt]
                            if chat_options:
                                st.session_state.menu_index = options.index(chat_options[0])
                                st.rerun()
                
                st.divider()
    
    elif menu.startswith("Friends"):
        st.markdown("<h2 style='text-align: center;'>🤝 Friends</h2>", unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["✅ My Friends", "📥 Received Requests", "📤 Sent Requests"])
        
        with tab1:
            friends = get_friends(school_code, user['email'])
            if friends:
                for friend_email in friends:
                    friend = next((u for u in users if u['email'] == friend_email), None)
                    if friend:
                        with st.container():
                            col1, col2, col3 = st.columns([1, 3, 1])
                            with col1:
                                if friend.get('profile_pic'):
                                    st.image(friend['profile_pic'], width=40)
                                else:
                                    emoji = "👑" if friend['role'] == 'admin' else "👨‍🏫" if friend['role'] == 'teacher' else "👨‍🎓" if friend['role'] == 'student' else "👪"
                                    st.markdown(f"<span style='font-size: 1.5rem;'>{emoji}</span>", unsafe_allow_html=True)
                            with col2:
                                st.markdown(f"**{friend['fullname']}**")
                            with col3:
                                if st.button("💬 Chat", key=f"chat_friend_{friend_email}"):
                                    st.session_state.chat_with = friend_email
                                    chat_options = [opt for opt in options if "Chat" in opt]
                                    if chat_options:
                                        st.session_state.menu_index = options.index(chat_options[0])
                                        st.rerun()
                            st.divider()
            else:
                st.info("No friends yet")
        
        with tab2:
            pending = get_pending_requests(school_code, user['email'])
            if pending:
                for req in pending:
                    sender = next((u for u in users if u['email'] == req['from']), None)
                    if sender:
                        with st.container():
                            col1, col2, col3 = st.columns([1, 3, 2])
                            with col1:
                                if sender.get('profile_pic'):
                                    st.image(sender['profile_pic'], width=40)
                                else:
                                    emoji = "👑" if sender['role'] == 'admin' else "👨‍🏫" if sender['role'] == 'teacher' else "👨‍🎓" if sender['role'] == 'student' else "👪"
                                    st.markdown(f"<span style='font-size: 1.5rem;'>{emoji}</span>", unsafe_allow_html=True)
                            with col2:
                                st.markdown(f"**{sender['fullname']}**")
                                st.markdown(f"<small>{req['date']}</small>", unsafe_allow_html=True)
                            with col3:
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    if st.button("✅ Accept", key=f"accept_{req['id']}"):
                                        accept_friend_request(school_code, req['id'])
                                        st.rerun()
                                with col_b:
                                    if st.button("❌ Decline", key=f"decline_{req['id']}"):
                                        decline_friend_request(school_code, req['id'])
                                        st.rerun()
                            st.divider()
            else:
                st.info("No pending friend requests")
        
        with tab3:
            sent = get_sent_requests(school_code, user['email'])
            if sent:
                for req in sent:
                    recipient = next((u for u in users if u['email'] == req['to']), None)
                    if recipient:
                        with st.container():
                            col1, col2, col3 = st.columns([1, 3, 1])
                            with col1:
                                if recipient.get('profile_pic'):
                                    st.image(recipient['profile_pic'], width=40)
                                else:
                                    emoji = "👑" if recipient['role'] == 'admin' else "👨‍🏫" if recipient['role'] == 'teacher' else "👨‍🎓" if recipient['role'] == 'student' else "👪"
                                    st.markdown(f"<span style='font-size: 1.5rem;'>{emoji}</span>", unsafe_allow_html=True)
                            with col2:
                                st.markdown(f"**{recipient['fullname']}**")
                                st.markdown(f"<small>Sent: {req['date']}</small>", unsafe_allow_html=True)
                            with col3:
                                st.markdown("<span style='color: #ffc107;'>⏳ Pending</span>", unsafe_allow_html=True)
                            st.divider()
            else:
                st.info("No sent requests")
    
    elif menu.startswith("Chat"):
        st.markdown("<h2 style='text-align: center;'>💬 Messages</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### Chats")
            friends = get_friends(school_code, user['email'])
            
            if friends:
                for friend_email in friends:
                    friend = next((u for u in users if u['email'] == friend_email), None)
                    if friend:
                        conv_id = f"{min(user['email'], friend_email)}_{max(user['email'], friend_email)}"
                        messages = load_school_data(school_code, "messages.json", [])
                        conv_msgs = [m for m in messages if m['conversation_id'] == conv_id and not m.get('deleted', False)]
                        last_msg = conv_msgs[-1]['message'][:20] + "..." if conv_msgs else ""
                        unread = len([m for m in conv_msgs if m['recipient'] == user['email'] and not m.get('read', False)])
                        
                        with st.container():
                            col_a, col_b = st.columns([1, 3])
                            with col_a:
                                if friend.get('profile_pic'):
                                    st.image(friend['profile_pic'], width=40)
                                else:
                                    emoji = "👑" if friend['role'] == 'admin' else "👨‍🏫" if friend['role'] == 'teacher' else "👨‍🎓" if friend['role'] == 'student' else "👪"
                                    st.markdown(f"<span style='font-size: 1.5rem;'>{emoji}</span>", unsafe_allow_html=True)
                            with col_b:
                                st.markdown(f"**{friend['fullname']}**")
                                if last_msg:
                                    st.markdown(f"<small>{last_msg}</small>", unsafe_allow_html=True)
                                if unread > 0:
                                    st.markdown(f"<span class='request-badge'>{unread}</span>", unsafe_allow_html=True)
                            
                            if st.button("Open", key=f"open_chat_{friend_email}", use_container_width=True):
                                st.session_state.chat_with = friend_email
                                st.rerun()
            else:
                st.info("Add friends to start chatting!")
        
        with col2:
            if st.session_state.chat_with:
                other_email = st.session_state.chat_with
                other_user = next((u for u in users if u['email'] == other_email), None)
                
                if other_user:
                    st.markdown(f"### Chat with {other_user['fullname']}")
                    
                    conv_id = f"{min(user['email'], other_email)}_{max(user['email'], other_email)}"
                    messages = load_school_data(school_code, "messages.json", [])
                    conv_msgs = [m for m in messages if m['conversation_id'] == conv_id and not m.get('deleted', False)]
                    conv_msgs.sort(key=lambda x: x['timestamp'])
                    
                    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
                    
                    for msg in conv_msgs:
                        if msg['recipient'] == user['email'] and not msg.get('read', False):
                            mark_as_read(msg['id'], school_code)
                        
                        is_sent = msg['sender'] == user['email']
                        sender_user = user if is_sent else other_user
                        
                        st.markdown(f"""
                        <div class="chat-message-wrapper {'chat-message-sent' if is_sent else 'chat-message-received'}">
                            <div class="chat-bubble {'chat-bubble-sent' if is_sent else 'chat-bubble-received'}">
                                <div class="chat-sender-info">
                                    <span class="chat-sender-name">{sender_user['fullname']}</span>
                                </div>
                                <div>{msg['message']}</div>
                                <div class="chat-time">{msg['timestamp'][:16]}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if msg.get('attachment'):
                            with st.expander("📎 Attachment"):
                                display_attachment(msg['attachment'])
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    with st.form("send_message", clear_on_submit=True):
                        col_a, col_b = st.columns([5, 1])
                        with col_a:
                            message = st.text_area("Message", height=60, placeholder="Type a message...")
                        with col_b:
                            attachment = st.file_uploader("📎", type=['jpg', 'png', 'pdf', 'docx', 'txt'], label_visibility="collapsed")
                        
                        if st.form_submit_button("📤 Send", use_container_width=True):
                            if message or attachment:
                                attachment_data = save_attachment(attachment) if attachment else None
                                send_message(school_code, user['email'], other_email, message, attachment_data)
                                st.rerun()
            else:
                st.info("Select a chat to start messaging")
    
    elif menu == "Group Chats 👥":
        st.markdown("<h2 style='text-align: center;'>👥 Group Chats</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### My Groups")
            user_groups = get_user_groups(school_code, user['email'])
            
            if user_groups:
                for group in user_groups:
                    if st.button(f"👥 {group['name']}", key=f"group_{group['id']}", use_container_width=True):
                        st.session_state.group_chat_with = group['id']
                        st.rerun()
            else:
                st.info("You're not in any groups yet")
            
            if user['role'] in ['admin', 'teacher']:
                st.markdown("### Create Group Chat")
                with st.form("create_group_chat"):
                    group_name = st.text_input("Group Name")
                    members = st.multiselect("Select Members", 
                                           [f"{u['fullname']} ({u['email']})" for u in users if u['email'] != user['email']])
                    
                    if st.form_submit_button("➕ Create"):
                        if group_name and members:
                            member_emails = [m.split('(')[1].rstrip(')') for m in members] + [user['email']]
                            group_id = create_group_chat(school_code, group_name, user['email'], member_emails)
                            st.success(f"Group chat '{group_name}' created!")
                            st.session_state.group_chat_with = group_id
                            st.rerun()
        
        with col2:
            if st.session_state.group_chat_with:
                all_chats = load_school_data(school_code, "group_chats.json", [])
                current_group = next((g for g in all_chats if g['id'] == st.session_state.group_chat_with), None)
                
                if current_group:
                    st.markdown(f"### {current_group['name']}")
                    
                    with st.expander("Group Members"):
                        for member_email in current_group.get('members', []):
                            member = next((u for u in users if u['email'] == member_email), None)
                            if member:
                                role_badge = " (Admin)" if member_email in current_group.get('admins', []) else ""
                                st.write(f"{member['fullname']}{role_badge}")
                    
                    st.markdown('<div class="chat-container" style="height: 400px;">', unsafe_allow_html=True)
                    
                    messages = current_group.get('messages', [])
                    for msg in messages:
                        sender = next((u for u in users if u['email'] == msg['sender']), None)
                        sender_name = sender['fullname'] if sender else msg['sender']
                        
                        is_sent = msg['sender'] == user['email']
                        
                        st.markdown(f"""
                        <div class="chat-message-wrapper {'chat-message-sent' if is_sent else 'chat-message-received'}">
                            <div class="chat-bubble {'chat-bubble-sent' if is_sent else 'chat-bubble-received'}">
                                <div class="chat-sender-info">
                                    <span class="chat-sender-name">{sender_name}</span>
                                </div>
                                <div>{msg['message']}</div>
                                <div class="chat-time">{msg['timestamp'][:16]}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if msg.get('attachment'):
                            with st.expander("📎 Attachment"):
                                display_attachment(msg['attachment'])
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    with st.form("send_group_message", clear_on_submit=True):
                        col_a, col_b = st.columns([5, 1])
                        with col_a:
                            message = st.text_area("Message", height=60, placeholder="Type a message...")
                        with col_b:
                            attachment = st.file_uploader("📎", type=['jpg', 'png', 'pdf', 'docx', 'txt'], 
                                                        label_visibility="collapsed", key="group_attach")
                        
                        if st.form_submit_button("📤 Send", use_container_width=True):
                            if message or attachment:
                                attachment_data = save_attachment(attachment) if attachment else None
                                send_group_message(school_code, st.session_state.group_chat_with, user['email'], message, attachment_data)
                                st.rerun()
            else:
                st.info("Select a group to start chatting")
    
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

else:
    st.error("Something went wrong")
    if st.button("Restart"):
        st.session_state.page = 'welcome'
        st.rerun()
