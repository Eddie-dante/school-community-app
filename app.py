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
            width: 280px !important;
            min-width: 280px !important;
            transform: translateX(0) !important;
        }
        .main .block-container {
            margin-left: 280px !important;
            max-width: calc(100% - 280px) !important;
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

# ============ BEAUTIFUL GRADIENT BACKGROUND ============
def get_gradient_colors():
    """Returns a set of beautiful flowing gradient colors"""
    gradients = [
        # Sunrise gradient
        """
        background: linear-gradient(-45deg, 
            #ff6b6b, #feca57, #ff9ff3, #48dbfb, #1dd1a1, #f368e0, #ff9f43
        );
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        """,
        # Ocean sunset
        """
        background: linear-gradient(-45deg, 
            #ff0844, #ffb199, #ff0844, #00d2ff, #3a1c71, #d76d77, #ffaf7b
        );
        background-size: 400% 400%;
        animation: gradient 18s ease infinite;
        """,
        # Purple haze
        """
        background: linear-gradient(-45deg, 
            #8E2DE2, #4A00E0, #6a3093, #a044ff, #c471ed, #f64f59, #c471ed
        );
        background-size: 400% 400%;
        animation: gradient 20s ease infinite;
        """,
        # Tropical
        """
        background: linear-gradient(-45deg, 
            #00b09b, #96c93d, #c6ffdd, #fbd786, #f7797d, #4facfe, #00f2fe
        );
        background-size: 400% 400%;
        animation: gradient 16s ease infinite;
        """,
        # Cherry blossom
        """
        background: linear-gradient(-45deg, 
            #ff9a9e, #fad0c4, #fad0c4, #ffd1ff, #a1c4fd, #c2e9fb, #fbc2eb
        );
        background-size: 400% 400%;
        animation: gradient 22s ease infinite;
        """,
        # Midnight city
        """
        background: linear-gradient(-45deg, 
            #232526, #414345, #232526, #2c3e50, #4b6cb7, #182848, #4b6cb7
        );
        background-size: 400% 400%;
        animation: gradient 25s ease infinite;
        """,
        # Autumn leaves
        """
        background: linear-gradient(-45deg, 
            #e44d2e, #f39c12, #d35400, #e67e22, #f1c40f, #e67e22, #d35400
        );
        background-size: 400% 400%;
        animation: gradient 19s ease infinite;
        """,
        # Northern lights
        """
        background: linear-gradient(-45deg, 
            #43C6AC, #191654, #43C6AC, #02AAB0, #00CDAC, #02AAB0, #191654
        );
        background-size: 400% 400%;
        animation: gradient 21s ease infinite;
        """
    ]
    return random.choice(gradients)

# ============ CUSTOM CSS WITH BEAUTIFUL GRADIENTS ============
GRADIENT_STYLE = get_gradient_colors()

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    * {{
        font-family: 'Poppins', sans-serif;
        box-sizing: border-box;
    }}
    
    @keyframes gradient {{
        0% {{
            background-position: 0% 50%;
        }}
        50% {{
            background-position: 100% 50%;
        }}
        100% {{
            background-position: 0% 50%;
        }}
    }}
    
    .stApp {{
        {GRADIENT_STYLE}
        position: relative;
    }}
    
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(2px);
        z-index: 0;
    }}
    
    .main > div, section[data-testid="stSidebar"] {{
        position: relative;
        z-index: 2;
    }}
    
    section[data-testid="stSidebar"] {{
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 5px 0 30px rgba(0, 0, 0, 0.2) !important;
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
        color: #333333 !important;
        text-shadow: none !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }}
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {{
        background: rgba(255, 255, 255, 0.5) !important;
        border-radius: 12px !important;
        padding: 0.5rem !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        margin: 0.8rem 0 !important;
    }}
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {{
        background: transparent !important;
        border-radius: 8px !important;
        padding: 8px 10px !important;
        margin: 2px 0 !important;
        transition: all 0.2s ease !important;
        color: #333333 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
    }}
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {{
        background: rgba(255, 255, 255, 0.8) !important;
    }}
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] {{
        background: rgba(255, 255, 255, 0.9) !important;
        border-left: 3px solid #ff6b6b !important;
        font-weight: 700 !important;
    }}
    
    section[data-testid="stSidebar"] .stButton button {{
        background: linear-gradient(135deg, #ff6b6b, #feca57) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        margin: 0.5rem 0 !important;
    }}
    
    section[data-testid="stSidebar"] .stButton button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4) !important;
    }}
    
    .school-header {{
        background: rgba(255, 255, 255, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 12px;
        text-align: center;
    }}
    
    .school-header h2 {{
        color: #333333 !important;
        margin: 0;
        font-size: 1.3rem;
        font-weight: 600;
    }}
    
    .school-code {{
        background: rgba(255,255,255,0.5);
        padding: 4px;
        border-radius: 20px;
        margin-top: 5px;
        border: 1px solid rgba(255, 255, 255, 0.5);
    }}
    
    .school-code code {{
        background: transparent !important;
        color: #ff6b6b !important;
        font-size: 0.8rem;
        font-weight: 600;
    }}
    
    .profile-card {{
        background: rgba(255, 255, 255, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    
    .profile-pic-small {{
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #ff6b6b;
    }}
    
    .main > div {{
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }}
    
    h1 {{
        background: linear-gradient(135deg, #ff6b6b, #feca57, #48dbfb, #1dd1a1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        text-align: center;
        margin-bottom: 1.5rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }}
    
    h2, h3 {{
        color: #333333 !important;
        font-weight: 600 !important;
    }}
    
    /* Instagram-style chat */
    .chat-container {{
        background: rgba(255, 255, 255, 0.5);
        border-radius: 16px;
        padding: 20px;
        height: 500px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 15px;
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
        background: linear-gradient(135deg, #ff6b6b, #feca57);
        color: white;
        border-bottom-right-radius: 4px;
    }}
    
    .chat-bubble-received {{
        background: rgba(255, 255, 255, 0.8);
        color: #333333;
        border-bottom-left-radius: 4px;
        border: 1px solid rgba(255, 255, 255, 0.5);
    }}
    
    .chat-sender-info {{
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 4px;
    }}
    
    .chat-sender-pic {{
        width: 24px;
        height: 24px;
        border-radius: 50%;
        object-fit: cover;
    }}
    
    .chat-sender-name {{
        font-size: 0.8rem;
        color: #ff6b6b;
        font-weight: 600;
    }}
    
    .chat-time {{
        font-size: 0.65rem;
        color: rgba(51, 51, 51, 0.5);
        margin-top: 4px;
        text-align: right;
    }}
    
    .chat-attachment {{
        background: rgba(255,255,255,0.2);
        border-radius: 12px;
        padding: 8px;
        margin-top: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    
    .chat-attachment:hover {{
        background: rgba(255,255,255,0.3);
    }}
    
    .chat-delete-btn {{
        color: rgba(51, 51, 51, 0.5);
        font-size: 0.7rem;
        cursor: pointer;
        margin-left: 8px;
        transition: color 0.2s ease;
    }}
    
    .chat-delete-btn:hover {{
        color: #ff4444;
    }}
    
    /* Community member card */
    .member-card {{
        background: rgba(255, 255, 255, 0.5);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 15px;
        transition: all 0.2s ease;
        border: 1px solid transparent;
    }}
    
    .member-card:hover {{
        background: rgba(255, 255, 255, 0.7);
        border-color: #ff6b6b;
    }}
    
    .member-pic {{
        width: 60px;
        height: 60px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #ff6b6b;
    }}
    
    .member-info {{
        flex: 1;
    }}
    
    .member-name {{
        color: #333333;
        font-weight: 600;
        font-size: 1.1rem;
    }}
    
    .member-role {{
        color: #ff6b6b;
        font-size: 0.8rem;
        display: inline-block;
        padding: 2px 8px;
        border-radius: 12px;
        background: rgba(255, 107, 107, 0.1);
        margin-top: 4px;
    }}
    
    .member-status {{
        color: rgba(51, 51, 51, 0.6);
        font-size: 0.8rem;
    }}
    
    /* Friend request badge */
    .request-badge {{
        background: #ff6b6b;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-left: 8px;
    }}
    
    /* Class/Group cards */
    .class-card, .group-card {{
        background: rgba(255, 255, 255, 0.5);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        border-left: 4px solid #ff6b6b;
    }}
    
    /* Assignment card */
    .assignment-card {{
        background: rgba(255, 255, 255, 0.5);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        border-left: 4px solid #00d2ff;
    }}
    
    /* Announcement card */
    .announcement-card {{
        background: rgba(255, 255, 255, 0.5);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 4px solid #ff6b6b;
    }}
    
    .announcement-header {{
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 10px;
    }}
    
    .announcement-author-pic {{
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
    }}
    
    .announcement-title {{
        color: #333333;
        font-weight: 600;
        font-size: 1.2rem;
    }}
    
    .announcement-meta {{
        color: rgba(51, 51, 51, 0.5);
        font-size: 0.8rem;
    }}
    
    .attachment-icon {{
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: rgba(255,255,255,0.2);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    
    .attachment-icon:hover {{
        background: rgba(255,255,255,0.3);
    }}
    
    /* ALL INPUT FIELDS - DEEP BLACK TEXT */
    .stTextInput input, 
    .stTextArea textarea, 
    .stSelectbox div, 
    .stDateInput input,
    .stNumberInput input,
    .stTextInput input[type="text"],
    .stTextInput input[type="password"],
    .stTextInput input[type="email"],
    .stTextInput input[type="number"],
    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder,
    .stSelectbox div[data-baseweb="select"] span,
    .stSelectbox div[role="listbox"] div,
    .stDateInput input[type="date"],
    input[type="text"],
    input[type="password"],
    input[type="email"],
    input[type="number"],
    textarea,
    select,
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label,
    .stDateInput label,
    .stNumberInput label {{
        color: #000000 !important;
        font-weight: 500 !important;
        background: white !important;
        border: 1px solid rgba(0, 0, 0, 0.1) !important;
    }}
    
    .stTextInput input, 
    .stTextArea textarea, 
    .stSelectbox div, 
    .stDateInput input,
    .stNumberInput input {{
        background: white !important;
        border-radius: 12px !important;
        padding: 0.6rem 1rem !important;
        font-size: 0.95rem !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
    }}
    
    .stTextInput input:focus, 
    .stTextArea textarea:focus,
    .stSelectbox div:focus,
    .stDateInput input:focus {{
        border-color: #ff6b6b !important;
        box-shadow: 0 0 0 2px rgba(255, 107, 107, 0.2) !important;
    }}
    
    /* Dropdown options */
    .stSelectbox div[role="listbox"] div,
    .stSelectbox div[data-baseweb="select"] div {{
        color: #000000 !important;
        background: white !important;
    }}
    
    /* Radio and checkbox labels */
    .stRadio label,
    .stCheckbox label {{
        color: #333333 !important;
    }}
    
    .stButton button {{
        background: linear-gradient(135deg, #ff6b6b, #feca57) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
    }}
    
    .stButton button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4) !important;
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        background: rgba(255, 255, 255, 0.5) !important;
        border-radius: 12px !important;
        padding: 0.3rem !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        gap: 0.3rem;
        margin-bottom: 1.5rem !important;
        flex-wrap: wrap !important;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        color: #333333 !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, #ff6b6b, #feca57) !important;
        color: white !important;
        font-weight: 600 !important;
    }}
    
    .stMetric {{
        background: rgba(255, 255, 255, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }}
    
    .stMetric label {{
        color: #333333 !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
    }}
    
    .stMetric div {{
        color: #ff6b6b !important;
        font-size: 1.8rem !important;
        font-weight: 600 !important;
    }}
    
    footer {{
        display: none !important;
    }}
    
    /* Additional black text for all form elements */
    .stSelectbox div[data-baseweb="select"] span,
    .stSelectbox div[role="listbox"] div,
    .stDateInput input,
    .stNumberInput input {{
        color: #000000 !important;
    }}
    
    /* Ensure dropdown options are black */
    div[role="listbox"] div {{
        color: #000000 !important;
        background: white !important;
    }}
    
    /* File uploader text */
    .stFileUploader div {{
        color: #333333 !important;
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

def delete_message(school_code, message_id):
    messages = load_school_data(school_code, "messages.json", [])
    for msg in messages:
        if msg['id'] == message_id:
            msg['deleted'] = True
            break
    save_school_data(school_code, "messages.json", messages)

def get_conversations(user_email, school_code):
    messages = load_school_data(school_code, "messages.json", [])
    conversations = {}
    for msg in messages:
        if not msg.get('deleted', False) and (msg['sender'] == user_email or msg['recipient'] == user_email):
            other = msg['recipient'] if msg['sender'] == user_email else msg['sender']
            if other not in conversations:
                conversations[other] = []
            conversations[other].append(msg)
    for conv in conversations:
        conversations[conv].sort(key=lambda x: x['timestamp'])
    return conversations

def get_unread_count(user_email, school_code):
    messages = load_school_data(school_code, "messages.json", [])
    return len([m for m in messages if m['recipient'] == user_email and not m.get('read', False) and not m.get('deleted', False)])

def mark_as_read(message_id, school_code):
    messages = load_school_data(school_code, "messages.json", [])
    for msg in messages:
        if msg['id'] == message_id:
            msg['read'] = True
            break
    save_school_data(school_code, "messages.json", messages)

# ============ GROUP FUNCTIONS ============
def get_user_rank_in_group(group, user_email):
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
    users = load_school_data(school_code, "users.json", [])
    return [u for u in users if u['email'] != current_user['email']]

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
if 'attachment' not in st.session_state:
    st.session_state.attachment = None

# ============ MAIN APP ============

# ----- WELCOME PAGE -----
if st.session_state.page == 'welcome':
    st.markdown('<h1>✨ School Community Hub ✨</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #333333;">Connect • Collaborate • Shine Together</p>', unsafe_allow_html=True)
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
            <div style="background: rgba(255,255,255,0.5); border: 1px solid rgba(255,255,255,0.5); border-radius: 20px; padding: 2rem; text-align: center;">
                <h3 style="color: #333333;">👑 Admin Powers</h3>
                <p style="color: #333333;">Full control over your school</p>
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
            <div style="background: rgba(255,255,255,0.5); border: 1px solid rgba(255,255,255,0.5); border-radius: 20px; padding: 2rem; text-align: center;">
                <h3 style="color: #333333;">🎓 Begin Your Legacy</h3>
                <p style="color: #333333;">Create your school community</p>
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
        
        # Profile picture display
        if user.get('profile_pic'):
            st.image(user['profile_pic'], width=50)
        else:
            # Default avatar based on role
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
        <div style="color: #333333; flex: 1;">
            <strong>{user['fullname']}</strong><br>
            <span style="background: rgba(255,107,107,0.1); color: #ff6b6b; padding: 2px 8px; border-radius: 12px; font-size: 0.7rem;">{role_display}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        
        # Navigation based on role
        if user['role'] == 'admin':
            options = ["Dashboard", "Announcements", "Classes", "Groups", "Teachers", "Students", "Guardians", "Assignments", "Community", f"Chat 💬{f' ({unread_count})' if unread_count>0 else ''}", f"Friends 🤝{f' ({pending_friend_count})' if pending_friend_count>0 else ''}", "Profile"]
        elif user['role'] == 'teacher':
            options = ["Dashboard", "Announcements", "My Classes", "Groups", "Assignments", "Community", f"Chat 💬{f' ({unread_count})' if unread_count>0 else ''}", f"Friends 🤝{f' ({pending_friend_count})' if pending_friend_count>0 else ''}", "Profile"]
        elif user['role'] == 'student':
            options = ["Dashboard", "Announcements", "Browse Classes", "My Classes", "Groups", "Assignments", "Community", f"Chat 💬{f' ({unread_count})' if unread_count>0 else ''}", f"Friends 🤝{f' ({pending_friend_count})' if pending_friend_count>0 else ''}", "Profile"]
        else:  # guardian
            options = ["Dashboard", "Announcements", "My Student", "Assignments", "Community", f"Chat 💬{f' ({unread_count})' if unread_count>0 else ''}", f"Friends 🤝{f' ({pending_friend_count})' if pending_friend_count>0 else ''}", "Profile"]
        
        # Fix menu index
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
    
    # ----- ANNOUNCEMENTS (for all roles) -----
    if menu == "Announcements":
        st.markdown("<h2 style='text-align: center;'>📢 School Announcements</h2>", unsafe_allow_html=True)
        
        # Admin and teachers can post announcements
        if user['role'] in ['admin', 'teacher']:
            with st.expander("➕ Create New Announcement"):
                with st.form("new_announcement", clear_on_submit=True):
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
                                "author_role": user['role'],
                                "author_pic": user.get('profile_pic'),
                                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                "target": target,
                                "important": important,
                                "attachment": attachment_data
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
                        st.markdown(f"""
                        <div class="announcement-card">
                            <div class="announcement-header">
                                <img src="{ann.get('author_pic', '')}" class="announcement-author-pic" onerror="this.style.display='none'">
                                <div>
                                    <div class="announcement-title">{ann['title']}{' ⭐' if ann.get('important') else ''}</div>
                                    <div class="announcement-meta">By {ann['author']} • {ann['date'][:16]}</div>
                                </div>
                            </div>
                            <div style="margin: 15px 0;">{ann['content']}</div>
                        """, unsafe_allow_html=True)
                        
                        if ann.get('attachment'):
                            st.markdown("**📎 Attachment:**")
                            display_attachment(ann['attachment'])
                        
                        st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No announcements yet")
    
    # ----- ASSIGNMENTS (for all roles) -----
    elif menu == "Assignments":
        st.markdown("<h2 style='text-align: center;'>📝 Assignments</h2>", unsafe_allow_html=True)
        
        # Teachers can create assignments
        if user['role'] in ['admin', 'teacher']:
            with st.expander("➕ Create New Assignment"):
                with st.form("new_assignment", clear_on_submit=True):
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
        
        # Display assignments based on user role
        st.subheader("📋 Current Assignments")
        
        user_assignments = []
        if user['role'] == 'student':
            # Show assignments for classes the student is in
            my_classes = [c['name'] for c in classes if user['email'] in c.get('students', [])]
            user_assignments = [a for a in assignments if a.get('target_class') in ['All Classes'] + my_classes]
        elif user['role'] == 'teacher':
            # Show assignments created by this teacher
            user_assignments = [a for a in assignments if a.get('created_by') == user['email']]
        elif user['role'] == 'guardian':
            # Show assignments for linked students
            linked_adms = user.get('linked_students', [])
            linked_students = [u for u in users if u.get('admission_number') in linked_adms]
            student_classes = []
            for s in linked_students:
                student_classes.extend([c['name'] for c in classes if s['email'] in c.get('students', [])])
            user_assignments = [a for a in assignments if a.get('target_class') in ['All Classes'] + list(set(student_classes))]
        else:  # admin
            user_assignments = assignments
        
        if user_assignments:
            for a in user_assignments:
                with st.container():
                    st.markdown(f"""
                    <div class="assignment-card">
                        <div style="display: flex; justify-content: space-between;">
                            <div>
                                <strong style="color: #ff6b6b;">{a['title']}</strong>
                                <span style="color: rgba(51,51,51,0.5); margin-left: 10px;">{a['subject']}</span>
                            </div>
                            <div style="color: {'#ff4444' if datetime.strptime(a['due_date'], '%Y-%m-%d') < datetime.now() else '#00d2ff'}">
                                Due: {a['due_date']}
                            </div>
                        </div>
                        <div style="margin: 10px 0; color: #333333;">{a['description']}</div>
                        <div style="display: flex; gap: 20px; font-size: 0.9rem; color: rgba(51,51,51,0.6);">
                            <span>Points: {a['total_points']}</span>
                            <span>Target: {a['target_class']}</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if a.get('attachment'):
                        st.markdown("**📎 Attachment:**")
                        display_attachment(a['attachment'])
                    
                    # Submission option for students
                    if user['role'] == 'student':
                        with st.form(key=f"submit_{a['id']}"):
                            submission_file = st.file_uploader("Submit your work", type=['pdf', 'docx', 'txt', 'jpg', 'png'], key=f"sub_{a['id']}")
                            if st.form_submit_button("📤 Submit"):
                                if submission_file:
                                    sub_data = save_attachment(submission_file)
                                    a['submissions'].append({
                                        "student_email": user['email'],
                                        "student_name": user['fullname'],
                                        "submission_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                        "attachment": sub_data
                                    })
                                    save_school_data(school_code, "assignments.json", assignments)
                                    st.success("Assignment submitted!")
                                    st.rerun()
                    
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No assignments available")
    
    # ----- COMMUNITY (see all members with profile pics) -----
    elif menu == "Community":
        st.markdown("<h2 style='text-align: center;'>🌍 School Community</h2>", unsafe_allow_html=True)
        
        all_members = get_all_community_members(school_code, user)
        friends = get_friends(school_code, user['email'])
        pending_requests = get_pending_requests(school_code, user['email'])
        sent_requests = get_sent_requests(school_code, user['email'])
        
        # Filter options
        col1, col2 = st.columns([2, 1])
        with col1:
            filter_role = st.selectbox("Filter by Role", ["All", "Admin", "Teacher", "Student", "Guardian"])
        with col2:
            search_term = st.text_input("🔍 Search by name", placeholder="Type name...")
        
        filtered_members = all_members
        if filter_role != "All":
            filtered_members = [m for m in all_members if m['role'].lower() == filter_role.lower()]
        if search_term:
            filtered_members = [m for m in filtered_members if search_term.lower() in m['fullname'].lower()]
        
        st.subheader(f"👥 Members ({len(filtered_members)})")
        
        for member in filtered_members:
            # Determine friend status
            is_friend = member['email'] in friends
            request_sent = any(r['to'] == member['email'] for r in sent_requests)
            request_received = any(r['from'] == member['email'] for r in pending_requests)
            
            with st.container():
                col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
                
                with col1:
                    if member.get('profile_pic'):
                        st.image(member['profile_pic'], width=50)
                    else:
                        emoji = "👑" if member['role'] == 'admin' else "👨‍🏫" if member['role'] == 'teacher' else "👨‍🎓" if member['role'] == 'student' else "👪"
                        st.markdown(f"<h1 style='font-size: 2rem; margin: 0;'>{emoji}</h1>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"**{member['fullname']}**")
                    st.markdown(f"<span style='color: #ff6b6b; font-size: 0.8rem;'>{member['role'].title()}</span>", unsafe_allow_html=True)
                
                with col3:
                    if is_friend:
                        st.markdown("<span style='color: #00d2ff;'>✅ Friend</span>", unsafe_allow_html=True)
                    elif request_sent:
                        st.markdown("<span style='color: #ff6b6b;'>⏳ Request Sent</span>", unsafe_allow_html=True)
                    elif request_received:
                        st.markdown("<span style='color: #feca57;'>📥 Request Received</span>", unsafe_allow_html=True)
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
                            # Navigate to chat
                            chat_options = [opt for opt in options if "Chat" in opt]
                            if chat_options:
                                st.session_state.menu_index = options.index(chat_options[0])
                                st.rerun()
                
                st.divider()
    
    # ----- FRIENDS & REQUESTS -----
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
                                st.markdown(f"<span style='color: #ff6b6b; font-size: 0.8rem;'>{friend['role'].title()}</span>", unsafe_allow_html=True)
                            with col3:
                                if st.button("💬 Chat", key=f"chat_friend_{friend_email}"):
                                    st.session_state.chat_with = friend_email
                                    # Navigate to chat
                                    chat_options = [opt for opt in options if "Chat" in opt]
                                    if chat_options:
                                        st.session_state.menu_index = options.index(chat_options[0])
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
                            col1, col2, col3 = st.columns([1, 3, 2])
                            with col1:
                                if sender.get('profile_pic'):
                                    st.image(sender['profile_pic'], width=40)
                                else:
                                    emoji = "👑" if sender['role'] == 'admin' else "👨‍🏫" if sender['role'] == 'teacher' else "👨‍🎓" if sender['role'] == 'student' else "👪"
                                    st.markdown(f"<span style='font-size: 1.5rem;'>{emoji}</span>", unsafe_allow_html=True)
                            with col2:
                                st.markdown(f"**{sender['fullname']}**")
                                st.markdown(f"<span style='color: #ff6b6b; font-size: 0.8rem;'>{sender['role'].title()}</span>", unsafe_allow_html=True)
                                st.markdown(f"<span style='color: rgba(51,51,51,0.5); font-size: 0.7rem;'>{req['date']}</span>", unsafe_allow_html=True)
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
                                st.markdown(f"<span style='color: #ff6b6b; font-size: 0.8rem;'>{recipient['role'].title()}</span>", unsafe_allow_html=True)
                                st.markdown(f"<span style='color: rgba(51,51,51,0.5); font-size: 0.7rem;'>Sent: {req['date']}</span>", unsafe_allow_html=True)
                            with col3:
                                st.markdown("<span style='color: #ff6b6b;'>⏳ Pending</span>", unsafe_allow_html=True)
                            st.divider()
            else:
                st.info("No sent requests")
    
    # ----- INSTAGRAM-STYLE CHAT -----
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
                        # Get last message
                        conv_id = f"{min(user['email'], friend_email)}_{max(user['email'], friend_email)}"
                        messages = load_school_data(school_code, "messages.json", [])
                        conv_msgs = [m for m in messages if m['conversation_id'] == conv_id and not m.get('deleted', False)]
                        conv_msgs.sort(key=lambda x: x['timestamp'])
                        
                        last_msg = conv_msgs[-1]['message'][:30] + "..." if conv_msgs and len(conv_msgs[-1]['message']) > 30 else (conv_msgs[-1]['message'] if conv_msgs else "")
                        unread = len([m for m in conv_msgs if m['recipient'] == user['email'] and not m.get('read', False)])
                        
                        # Create chat preview
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
                                    st.markdown(f"<span style='color: rgba(51,51,51,0.5); font-size: 0.8rem;'>{last_msg}</span>", unsafe_allow_html=True)
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
                    
                    # Get conversation
                    conv_id = f"{min(user['email'], other_email)}_{max(user['email'], other_email)}"
                    messages = load_school_data(school_code, "messages.json", [])
                    conv_msgs = [m for m in messages if m['conversation_id'] == conv_id and not m.get('deleted', False)]
                    conv_msgs.sort(key=lambda x: x['timestamp'])
                    
                    # Chat container
                    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
                    
                    for msg in conv_msgs:
                        if msg['recipient'] == user['email'] and not msg.get('read', False):
                            mark_as_read(msg['id'], school_code)
                        
                        is_sent = msg['sender'] == user['email']
                        
                        # Get sender info
                        sender_user = user if is_sent else other_user
                        
                        # Message bubble
                        with st.container():
                            st.markdown(f"""
                            <div class="chat-message-wrapper {'chat-message-sent' if is_sent else 'chat-message-received'}">
                                <div class="chat-bubble {'chat-bubble-sent' if is_sent else 'chat-bubble-received'}">
                                    <div class="chat-sender-info">
                                        <img src="{sender_user.get('profile_pic', '')}" class="chat-sender-pic" onerror="this.style.display='none'">
                                        <span class="chat-sender-name">{sender_user['fullname']}</span>
                                    </div>
                                    <div>{msg['message']}</div>
                            """, unsafe_allow_html=True)
                            
                            if msg.get('attachment'):
                                with st.expander("📎 Attachment"):
                                    display_attachment(msg['attachment'])
                            
                            st.markdown(f"""
                                    <div class="chat-time">{msg['timestamp']}</div>
                                </div>
                                {f'<span class="chat-delete-btn" onclick="alert(\'Delete feature would go here\')">🗑️</span>' if is_sent else ''}
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Message input with attachment
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
    
    # ----- CLASSES SECTION -----
    elif menu in ["Classes", "My Classes", "Browse Classes"]:
        st.markdown("<h2 style='text-align: center;'>📚 Classes</h2>", unsafe_allow_html=True)
        
        # Admin can create classes (ONLY ADMIN)
        if user['role'] == 'admin' and menu == "Classes":
            with st.expander("➕ Create New Class"):
                with st.form("create_class", clear_on_submit=True):
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
                                "announcements": [],
                                "assignments": [],
                                "resources": [],
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
        
        # Display classes
        if menu == "My Classes" and user['role'] == 'teacher':
            # Show classes taught by this teacher
            display_classes = [c for c in classes if c.get('teacher') == user['email']]
            st.subheader(f"📋 My Classes ({len(display_classes)})")
        elif menu == "My Classes" and user['role'] == 'student':
            # Show classes the student is enrolled in
            display_classes = [c for c in classes if user['email'] in c.get('students', [])]
            st.subheader(f"📋 My Classes ({len(display_classes)})")
        else:
            # Show all classes
            display_classes = classes
            st.subheader(f"📋 All Classes ({len(display_classes)})")
        
        for c in display_classes:
            with st.expander(f"📖 {c['name']} - {c['grade']} ({c['code']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Subject:** {c.get('subject', 'N/A')}")
                    st.write(f"**Teacher:** {c.get('teacher_name', 'Unknown')}")
                    st.write(f"**Room:** {c.get('room', 'TBD')}")
                with col2:
                    st.write(f"**Schedule:** {c.get('schedule', 'TBD')}")
                    st.write(f"**Students:** {len(c.get('students', []))}/{c.get('max_students', 40)}")
                
                # Show enrolled students
                if c.get('students'):
                    st.write("**👥 Enrolled Students:**")
                    for student_email in c['students']:
                        student = next((u for u in users if u['email'] == student_email), None)
                        if student:
                            col_a, col_b = st.columns([1, 10])
                            with col_a:
                                if student.get('profile_pic'):
                                    st.image(student['profile_pic'], width=30)
                                else:
                                    st.write("👨‍🎓")
                            with col_b:
                                st.write(f"{student['fullname']}")
                
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
                
                # Admin can approve requests (ONLY ADMIN)
                if user['role'] == 'admin':
                    pending = [r for r in class_requests if r['class_name'] == c['name'] and r['status'] == 'pending']
                    if pending:
                        st.write("**⏳ Pending Requests:**")
                        for req in pending:
                            col_a, col_b = st.columns([3, 1])
                            with col_a:
                                st.write(f"{req['student_name']} ({req['student_email']})")
                            with col_b:
                                if st.button("✅ Approve", key=f"approve_class_{req['id']}"):
                                    c['students'].append(req['student_email'])
                                    req['status'] = 'approved'
                                    save_school_data(school_code, "classes.json", classes)
                                    save_school_data(school_code, "class_requests.json", class_requests)
                                    st.rerun()
    
    # ----- GROUPS SECTION -----
    elif menu == "Groups":
        st.markdown("<h2 style='text-align: center;'>👥 Groups</h2>", unsafe_allow_html=True)
        
        # Admin can create groups (ONLY ADMIN)
        if user['role'] == 'admin':
            with st.expander("➕ Create New Group"):
                with st.form("create_group", clear_on_submit=True):
                    group_name = st.text_input("Group Name", placeholder="e.g., Math Study Group")
                    group_description = st.text_area("Description", placeholder="What is this group about?")
                    group_type = st.selectbox("Group Type", ["Study Group", "Club", "Sports Team", "Project Team", "Other"])
                    max_members = st.number_input("Max Members", min_value=2, max_value=100, value=20)
                    
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
                                "co_leaders": [],
                                "created": datetime.now().strftime("%Y-%m-%d"),
                                "max_members": max_members,
                                "members": [user['email']],
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
        st.subheader(f"📋 All Groups ({len(groups)})")
        
        for g in groups:
            with st.expander(f"👥 {g['name']} - {g.get('type', 'Group')} ({g['code']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Description:** {g.get('description', 'No description')}")
                    st.write(f"**Leader:** {g.get('leader_name', 'Unknown')}")
                with col2:
                    st.write(f"**Members:** {len(g.get('members', []))}/{g.get('max_members', 20)}")
                    st.write(f"**Created:** {g['created']}")
                
                # Show members with profile pics
                if g.get('members'):
                    st.write("**👥 Members:**")
                    for member_email in g['members']:
                        member = next((u for u in users if u['email'] == member_email), None)
                        if member:
                            col_a, col_b = st.columns([1, 10])
                            with col_a:
                                if member.get('profile_pic'):
                                    st.image(member['profile_pic'], width=30)
                                else:
                                    emoji = "👑" if member['role'] == 'admin' else "👨‍🏫" if member['role'] == 'teacher' else "👨‍🎓" if member['role'] == 'student' else "👪"
                                    st.write(emoji)
                            with col_b:
                                rank = "Leader" if member_email == g['leader'] else "Co-Leader" if member_email in g.get('co_leaders', []) else "Member"
                                st.write(f"{member['fullname']} - <span style='color: #ff6b6b;'>{rank}</span>", unsafe_allow_html=True)
                
                # Request to join button
                if user['email'] not in g.get('members', []):
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
                
                # Admin can approve requests (ONLY ADMIN)
                if user['role'] == 'admin':
                    pending = [r for r in group_requests if r['group_name'] == g['name'] and r['status'] == 'pending']
                    if pending:
                        st.write("**⏳ Pending Requests:**")
                        for req in pending:
                            col_a, col_b = st.columns([3, 1])
                            with col_a:
                                st.write(f"{req['student_name']} ({req['student_email']})")
                            with col_b:
                                if st.button("✅ Approve", key=f"approve_group_{req['id']}"):
                                    g['members'].append(req['student_email'])
                                    req['status'] = 'approved'
                                    save_school_data(school_code, "groups.json", groups)
                                    save_school_data(school_code, "group_requests.json", group_requests)
                                    st.rerun()
    
    # ----- TEACHERS SECTION (Admin only) -----
    elif menu == "Teachers" and user['role'] == 'admin':
        st.markdown("<h2 style='text-align: center;'>👨‍🏫 Teacher Management</h2>", unsafe_allow_html=True)
        
        with st.expander("✨ Create Teacher Code"):
            with st.form("create_teacher_code", clear_on_submit=True):
                name = st.text_input("Code Name", placeholder="e.g., Mathematics Department")
                code = st.text_input("Custom Code", placeholder="e.g., MATH-DEPT")
                dept = st.selectbox("Department", ["Mathematics", "Science", "English", "Kiswahili", "History", "Other"])
                if st.form_submit_button("✨ Generate Code"):
                    if name and code:
                        if any(t['code'] == code.upper() for t in teachers_data):
                            st.error("Code already exists")
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
                            st.success(f"Code {code.upper()} created")
                            st.rerun()
        
        st.subheader("👥 Active Teachers")
        teacher_users = [u for u in users if u['role'] == 'teacher']
        if teacher_users:
            for t in teacher_users:
                with st.container():
                    col1, col2, col3 = st.columns([1, 3, 2])
                    with col1:
                        if t.get('profile_pic'):
                            st.image(t['profile_pic'], width=40)
                        else:
                            st.write("👨‍🏫")
                    with col2:
                        st.write(f"**{t['fullname']}**")
                        st.write(f"📧 {t['email']}")
                    with col3:
                        st.write(f"Joined: {t['joined']}")
                    st.divider()
        else:
            st.info("No teachers registered yet")
    
    # ----- STUDENTS SECTION (Admin only) -----
    elif menu == "Students" and user['role'] == 'admin':
        st.markdown("<h2 style='text-align: center;'>👨‍🎓 Student Management</h2>", unsafe_allow_html=True)
        
        student_users = [u for u in users if u['role'] == 'student']
        if student_users:
            for s in student_users:
                with st.container():
                    col1, col2, col3, col4 = st.columns([1, 3, 2, 1])
                    with col1:
                        if s.get('profile_pic'):
                            st.image(s['profile_pic'], width=40)
                        else:
                            st.write("👨‍🎓")
                    with col2:
                        st.write(f"**{s['fullname']}**")
                    with col3:
                        st.write(f"Adm: {s['admission_number']}")
                    with col4:
                        if st.button("🗑️", key=f"del_{s['user_id']}"):
                            users.remove(s)
                            save_school_data(school_code, "users.json", users)
                            school['stats']['students'] -= 1
                            all_schools = load_all_schools()
                            all_schools[school_code] = school
                            save_all_schools(all_schools)
                            st.rerun()
                    st.divider()
        else:
            st.info("No students enrolled")
    
    # ----- GUARDIANS SECTION (Admin only) -----
    elif menu == "Guardians" and user['role'] == 'admin':
        st.markdown("<h2 style='text-align: center;'>👪 Guardian Management</h2>", unsafe_allow_html=True)
        
        guardian_users = [u for u in users if u['role'] == 'guardian']
        if guardian_users:
            for g in guardian_users:
                with st.container():
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if g.get('profile_pic'):
                            st.image(g['profile_pic'], width=40)
                        else:
                            st.write("👪")
                    with col2:
                        st.write(f"**{g['fullname']}**")
                        st.write(f"📧 {g['email']}")
                        st.write(f"Linked Students: {', '.join(g.get('linked_students', []))}")
                    st.divider()
        else:
            st.info("No guardians registered")
    
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
    
    # ----- DASHBOARD (for each role) -----
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
            col3.metric("Assignments", len([a for a in assignments if a.get('created_by') == user['email']]))
        
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
                    with st.container():
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            if student.get('profile_pic'):
                                st.image(student['profile_pic'], width=40)
                            else:
                                st.write("👨‍🎓")
                        with col2:
                            st.write(f"**{student['fullname']}** - {adm}")
                        st.divider()
    
    # ----- MY STUDENT (guardian only) -----
    elif menu == "My Student" and user['role'] == 'guardian':
        st.markdown("<h2 style='text-align: center;'>👨‍🎓 My Student</h2>", unsafe_allow_html=True)
        
        for adm in user.get('linked_students', []):
            student = next((u for u in users if u.get('admission_number') == adm), None)
            if student:
                with st.container():
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if student.get('profile_pic'):
                            st.image(student['profile_pic'], width=80)
                        else:
                            st.markdown("<h1 style='font-size: 3rem;'>👨‍🎓</h1>", unsafe_allow_html=True)
                    with col2:
                        st.subheader(student['fullname'])
                        st.write(f"📧 {student['email'] if student['email'] else 'No email'}")
                        st.write(f"🎫 Admission: {adm}")
                    
                    # Classes
                    student_classes = [c for c in classes if student['email'] in c.get('students', [])]
                    if student_classes:
                        st.markdown("### 📚 Enrolled Classes")
                        for c in student_classes:
                            st.write(f"- {c['name']} ({c['grade']})")
                    
                    # Assignments
                    student_assignments = [a for a in assignments if a.get('target_class') in ['All Classes'] + [c['name'] for c in student_classes]]
                    if student_assignments:
                        st.markdown("### 📝 Pending Assignments")
                        for a in student_assignments:
                            due_date = datetime.strptime(a['due_date'], '%Y-%m-%d')
                            status = "🔴 Overdue" if due_date < datetime.now() else "🟡 Due Soon" if due_date < datetime.now() + timedelta(days=3) else "🟢 Active"
                            st.write(f"- **{a['title']}** - Due: {a['due_date']} ({status})")
                    
                    st.divider()

else:
    st.error("Something went wrong")
    if st.button("Restart"):
        st.session_state.page = 'welcome'
        st.rerun()
