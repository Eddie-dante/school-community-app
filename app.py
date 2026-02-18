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
        """
        background: linear-gradient(-45deg, 
            #ff6b6b, #feca57, #ff9ff3, #48dbfb, #1dd1a1, #f368e0, #ff9f43
        );
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        """,
        """
        background: linear-gradient(-45deg, 
            #ff0844, #ffb199, #ff0844, #00d2ff, #3a1c71, #d76d77, #ffaf7b
        );
        background-size: 400% 400%;
        animation: gradient 18s ease infinite;
        """,
        """
        background: linear-gradient(-45deg, 
            #8E2DE2, #4A00E0, #6a3093, #a044ff, #c471ed, #f64f59, #c471ed
        );
        background-size: 400% 400%;
        animation: gradient 20s ease infinite;
        """,
        """
        background: linear-gradient(-45deg, 
            #00b09b, #96c93d, #c6ffdd, #fbd786, #f7797d, #4facfe, #00f2fe
        );
        background-size: 400% 400%;
        animation: gradient 16s ease infinite;
        """
    ]
    return random.choice(gradients)

# ============ LUMINOUS SECTION BACKGROUNDS ============
def get_luminous_colors():
    """Returns vibrant, glowing background colors for sections"""
    luminous_colors = [
        """
        background: linear-gradient(135deg, #FF6B6B, #FF8E8E);
        box-shadow: 0 0 30px rgba(255, 107, 107, 0.5);
        """,
        """
        background: linear-gradient(135deg, #4ECDC4, #6EE7E7);
        box-shadow: 0 0 30px rgba(78, 205, 196, 0.5);
        """,
        """
        background: linear-gradient(135deg, #45B7D1, #6EC8E0);
        box-shadow: 0 0 30px rgba(69, 183, 209, 0.5);
        """,
        """
        background: linear-gradient(135deg, #96CEB4, #B8E0CC);
        box-shadow: 0 0 30px rgba(150, 206, 180, 0.5);
        """,
        """
        background: linear-gradient(135deg, #FFEEAD, #FFF2C2);
        box-shadow: 0 0 30px rgba(255, 238, 173, 0.5);
        """,
        """
        background: linear-gradient(135deg, #D4A5A5, #E3C0C0);
        box-shadow: 0 0 30px rgba(212, 165, 165, 0.5);
        """
    ]
    return random.choice(luminous_colors)

# ============ GOLDEN SIDEBAR STYLING ============
def get_golden_gradient():
    """Returns a beautiful golden gradient for sidebar"""
    return """
    background: linear-gradient(135deg, 
        #cfa668, #e5b873, #f5d742, #e6be5a, #d4a545, #c1933a, #ad7e2e
    );
    background-size: 300% 300%;
    animation: golden-shimmer 8s ease infinite;
    """

# ============ CUSTOM CSS ============
GRADIENT_STYLE = get_gradient_colors()

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
    
    body {{
        {GRADIENT_STYLE}
        margin: 0;
        padding: 0;
        min-height: 100vh;
    }}
    
    .stApp {{
        background: transparent !important;
    }}
    
    .main .block-container {{
        background: transparent !important;
        padding: 1rem;
        margin: 0;
        border: none;
        box-shadow: none;
    }}
    
    .section-container {{
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        animation: glow 3s ease-in-out infinite;
    }}
    
    @keyframes glow {{
        0% {{ box-shadow: 0 0 20px rgba(255, 255, 255, 0.3); }}
        50% {{ box-shadow: 0 0 40px rgba(255, 255, 255, 0.6); }}
        100% {{ box-shadow: 0 0 20px rgba(255, 255, 255, 0.3); }}
    }}
    
    .section-community {{ {get_luminous_colors()} }}
    .section-management {{ {get_luminous_colors()} }}
    .section-personal {{ {get_luminous_colors()} }}
    
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
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {{
        background: rgba(255, 215, 0, 0.2) !important;
        transform: translateX(5px) !important;
    }}
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] {{
        background: rgba(255, 215, 0, 0.3) !important;
        border-left: 4px solid #FFD700 !important;
        font-weight: 700 !important;
    }}
    
    section[data-testid="stSidebar"] .stButton button {{
        background: linear-gradient(135deg, #FFD700, #DAA520) !important;
        color: #2b2b2b !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        font-weight: 700 !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
        margin: 0.5rem 0 !important;
        box-shadow: 0 4px 15px rgba(218, 165, 32, 0.4) !important;
    }}
    
    section[data-testid="stSidebar"] .stButton button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.6) !important;
    }}
    
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
    
    .stSelectbox div[data-baseweb="select"] {{
        background: white !important;
        border: 2px solid #FFD700 !important;
        border-radius: 10px !important;
        color: #000000 !important;
        font-weight: 500 !important;
    }}
    
    .stSelectbox div[data-baseweb="select"]:hover {{
        border-color: #DAA520 !important;
        box-shadow: 0 0 15px rgba(218, 165, 32, 0.3) !important;
    }}
    
    .stTextInput input, 
    .stTextArea textarea, 
    .stDateInput input,
    .stNumberInput input {{
        background: white !important;
        border: 2px solid #FFD700 !important;
        border-radius: 10px !important;
        padding: 0.6rem 1rem !important;
        color: #000000 !important;
        font-weight: 500 !important;
    }}
    
    .stTextInput input:focus, 
    .stTextArea textarea:focus,
    .stDateInput input:focus,
    .stNumberInput input:focus {{
        border-color: #DAA520 !important;
        box-shadow: 0 0 15px rgba(218, 165, 32, 0.3) !important;
    }}
    
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
    
    h1 {{
        background: linear-gradient(135deg, #FFD700, #FFA500, #FF8C00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        text-align: center;
        margin-bottom: 1.5rem !important;
    }}
    
    .golden-card {{
        background: rgba(255, 255, 255, 0.9);
        border-left: 6px solid #FFD700;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(218, 165, 32, 0.2);
    }}
    
    .performance-excellent {{
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 0 15px rgba(40, 167, 69, 0.5);
    }}
    
    .performance-good {{
        background: linear-gradient(135deg, #17a2b8, #6f42c1);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 0 15px rgba(23, 162, 184, 0.5);
    }}
    
    .performance-average {{
        background: linear-gradient(135deg, #ffc107, #fd7e14);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 0 15px rgba(255, 193, 7, 0.5);
    }}
    
    .performance-needs-improvement {{
        background: linear-gradient(135deg, #dc3545, #c82333);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        box-shadow: 0 0 15px rgba(220, 53, 69, 0.5);
    }}
    
    .chat-container {{
        background: rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        padding: 20px;
        height: 400px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 15px;
        border: 1px solid #FFD700;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
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
    
    .chat-message-sent {{ justify-content: flex-end; }}
    .chat-message-received {{ justify-content: flex-start; }}
    
    .chat-bubble {{
        max-width: 70%;
        padding: 12px 16px;
        border-radius: 20px;
        word-wrap: break-word;
    }}
    
    .chat-bubble-sent {{
        background: linear-gradient(135deg, #FFD700, #DAA520);
        color: #2b2b2b;
        border-bottom-right-radius: 4px;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
    }}
    
    .chat-bubble-received {{
        background: rgba(255, 255, 255, 0.95);
        color: #333333;
        border-bottom-left-radius: 4px;
        border: 1px solid #FFD700;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
    }}
    
    .chat-sender-name {{
        font-size: 0.8rem;
        color: #DAA520;
        font-weight: 600;
    }}
    
    .nav-button {{
        background: linear-gradient(135deg, #FFD700, #DAA520);
        color: #2b2b2b;
        border: none;
        border-radius: 15px;
        padding: 25px;
        font-size: 1.3rem;
        font-weight: 700;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(218, 165, 32, 0.3);
        margin: 10px 0;
    }}
    
    .nav-button:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(255, 215, 0, 0.4);
    }}
    
    .stMetric {{
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.3) !important;
    }}
    
    .stMetric label {{ color: #333333 !important; font-weight: 600 !important; }}
    .stMetric div {{ color: #FFD700 !important; font-weight: 700 !important; }}
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

# ============ SCHOOL MANAGEMENT FUNCTIONS ============
def add_academic_record(school_code, student_email, subject, score, term, year, teacher_email, class_name):
    grades = load_school_data(school_code, "academic_records.json", [])
    grades.append({
        "id": generate_id("GRD"),
        "student_email": student_email,
        "subject": subject,
        "score": score,
        "term": term,
        "year": year,
        "teacher_email": teacher_email,
        "class_name": class_name,
        "date": datetime.now().strftime("%Y-%m-%d")
    })
    save_school_data(school_code, "academic_records.json", grades)

def add_attendance_record(school_code, student_email, date, status, remarks="", class_name=""):
    attendance = load_school_data(school_code, "attendance.json", [])
    attendance.append({
        "id": generate_id("ATT"),
        "student_email": student_email,
        "date": date,
        "status": status,
        "remarks": remarks,
        "class_name": class_name,
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

def add_teacher_review(school_code, teacher_email, student_email, review_text, rating, date, class_name):
    reviews = load_school_data(school_code, "teacher_reviews.json", [])
    reviews.append({
        "id": generate_id("REV"),
        "teacher_email": teacher_email,
        "student_email": student_email,
        "review_text": review_text,
        "rating": rating,
        "date": date,
        "class_name": class_name,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    save_school_data(school_code, "teacher_reviews.json", reviews)

def add_furniture_allocation(school_code, item_name, location, quantity, condition, allocated_by):
    furniture = load_school_data(school_code, "furniture.json", [])
    furniture.append({
        "id": generate_id("FUR"),
        "item_name": item_name,
        "location": location,
        "quantity": quantity,
        "condition": condition,
        "allocated_by": allocated_by,
        "allocated_date": datetime.now().strftime("%Y-%m-%d")
    })
    save_school_data(school_code, "furniture.json", furniture)

def add_teacher_allocation(school_code, teacher_name, subject, assigned_class, allocated_by):
    teachers = load_school_data(school_code, "teacher_allocations.json", [])
    teachers.append({
        "id": generate_id("TCH"),
        "teacher_name": teacher_name,
        "subject": subject,
        "assigned_class": assigned_class,
        "allocated_by": allocated_by,
        "allocated_date": datetime.now().strftime("%Y-%m-%d")
    })
    save_school_data(school_code, "teacher_allocations.json", teachers)

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

def get_class_performance(grades, class_name, term, year):
    class_grades = [g for g in grades if g['class_name'] == class_name and g['term'] == term and g['year'] == year]
    if not class_grades:
        return {}
    
    subject_averages = {}
    for grade in class_grades:
        if grade['subject'] not in subject_averages:
            subject_averages[grade['subject']] = []
        subject_averages[grade['subject']].append(grade['score'])
    
    for subject in subject_averages:
        subject_averages[subject] = round(sum(subject_averages[subject]) / len(subject_averages[subject]), 2)
    
    return subject_averages

# ============ SESSION STATE ============
if 'user' not in st.session_state:
    st.session_state.user = None
if 'current_school' not in st.session_state:
    st.session_state.current_school = None
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'main_section' not in st.session_state:
    st.session_state.main_section = 'community'  # 'community', 'management', 'personal'
if 'management_access' not in st.session_state:
    st.session_state.management_access = False
if 'personal_access' not in st.session_state:
    st.session_state.personal_access = False

# ============ MAIN APP ============

# ----- WELCOME PAGE WITH THREE MAIN BUTTONS -----
if st.session_state.page == 'welcome':
    st.markdown('<h1>✨ School Community Hub ✨</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #333333; font-size: 1.2rem;">Connect • Manage • Personalize</p>', unsafe_allow_html=True)
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏫 School Community", key="nav_community", use_container_width=True):
            st.session_state.main_section = 'community'
            st.rerun()
        st.markdown("""
        <p style="text-align: center; color: #666; padding: 10px;">Connect with teachers, students, and guardians. Join groups, chat, and collaborate!</p>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("📊 School Management", key="nav_management", use_container_width=True):
            st.session_state.main_section = 'management'
            st.rerun()
        st.markdown("""
        <p style="text-align: center; color: #666; padding: 10px;">Complete school administration - Academics, Finance, Discipline, Teacher/Furniture Allocation</p>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("👤 Personal Dashboard", key="nav_personal", use_container_width=True):
            st.session_state.main_section = 'personal'
            st.rerun()
        st.markdown("""
        <p style="text-align: center; color: #666; padding: 10px;">Your personal information, performance, reviews, and class analytics</p>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # ============ SCHOOL COMMUNITY SECTION (PUBLIC) ============
    if st.session_state.main_section == 'community':
        st.markdown('<div class="section-container section-community">', unsafe_allow_html=True)
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FF6B6B, #FF8E8E); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 30px; box-shadow: 0 0 40px rgba(255, 107, 107, 0.5);">
            <h3 style="color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">🏫 School Community</h3>
            <p style="color: white;">Login or register to connect with your school community!</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["👑 Admin Login", "🏫 Create School", "👨‍🏫 Teacher", "👨‍🎓 Student", "👪 Guardian"])
        
        with tab1:
            col1, col2 = st.columns([1,1])
            with col1:
                with st.form("admin_login"):
                    st.subheader("Admin Login")
                    school_code = st.text_input("School Code", placeholder="Enter your school code")
                    admin_email = st.text_input("Email", placeholder="admin@school.edu")
                    admin_password = st.text_input("Password", type="password", placeholder="••••••••")
                    if st.form_submit_button("Login", use_container_width=True):
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
                                            st.session_state.management_access = True
                                            st.session_state.personal_access = True
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
                    st.subheader("Create a New School")
                    school_name = st.text_input("School Name", placeholder="e.g., Golden Heights Academy")
                    admin_name = st.text_input("Your Full Name", placeholder="e.g., John Doe")
                    admin_email = st.text_input("Your Email", placeholder="you@school.edu")
                    password = st.text_input("Password", type="password", placeholder="Create a strong password")
                    confirm = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
                    city = st.text_input("City", placeholder="e.g., Nairobi")
                    state = st.text_input("State/Province", placeholder="e.g., Nairobi")
                    motto = st.text_input("School Motto", placeholder="e.g., Excellence is Our Tradition")
                    
                    if st.form_submit_button("Create School", use_container_width=True):
                        if not school_name or not admin_email or not password:
                            st.error("School name, email and password are required")
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
                                "stats": {"students":0, "teachers":0, "guardians":0, "classes":0}
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
                                "class": "Administration",
                                "stream": "",
                                "admission_number": "",
                                "profile_pic": None,
                                "bio": "",
                                "phone": ""
                            }]
                            save_school_data(code, "users.json", users)
                            save_school_data(code, "classes.json", [])
                            save_school_data(code, "academic_records.json", [])
                            save_school_data(code, "attendance.json", [])
                            save_school_data(code, "fees.json", [])
                            save_school_data(code, "discipline.json", [])
                            save_school_data(code, "teacher_reviews.json", [])
                            save_school_data(code, "furniture.json", [])
                            save_school_data(code, "teacher_allocations.json", [])
                            
                            st.session_state.current_school = new_school
                            st.session_state.user = users[0]
                            st.session_state.management_access = True
                            st.session_state.personal_access = True
                            st.session_state.page = 'dashboard'
                            st.success(f"✅ School Created! Your School Code is: **{code}**")
                            st.info("Save this code - you'll need it for login!")
                            st.rerun()
        
        with tab3:
            subtab1, subtab2 = st.tabs(["Login", "Register"])
            with subtab1:
                with st.form("teacher_login"):
                    st.subheader("Teacher Login")
                    school_code = st.text_input("School Code")
                    email = st.text_input("Email")
                    password = st.text_input("Password", type="password")
                    if st.form_submit_button("Login", use_container_width=True):
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
                                        st.session_state.management_access = True
                                        st.session_state.personal_access = True
                                        st.session_state.page = 'dashboard'
                                        st.rerun()
                                st.error("Invalid credentials")
                            else:
                                st.error("School not found")
            
            with subtab2:
                with st.form("teacher_register"):
                    st.subheader("New Teacher Registration")
                    school_code = st.text_input("School Code")
                    teacher_code = st.text_input("Teacher Code (from admin)")
                    fullname = st.text_input("Full Name")
                    email = st.text_input("Email")
                    password = st.text_input("Password", type="password")
                    confirm = st.text_input("Confirm Password", type="password")
                    
                    if st.form_submit_button("Register", use_container_width=True):
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
                                
                                new_user = {
                                    "user_id": generate_id("USR"),
                                    "email": email,
                                    "fullname": fullname,
                                    "password": hashlib.sha256(password.encode()).hexdigest(),
                                    "role": "teacher",
                                    "joined": datetime.now().strftime("%Y-%m-%d"),
                                    "school_code": school_code,
                                    "teacher_code": teacher_code,
                                    "class": "",
                                    "stream": "",
                                    "admission_number": "",
                                    "profile_pic": None,
                                    "bio": "",
                                    "phone": ""
                                }
                                users.append(new_user)
                                save_school_data(school_code, "users.json", users)
                                school['stats']['teachers'] += 1
                                all_schools[school_code] = school
                                save_all_schools(all_schools)
                                
                                st.session_state.current_school = school
                                st.session_state.user = new_user
                                st.session_state.management_access = True
                                st.session_state.personal_access = True
                                st.session_state.page = 'dashboard'
                                st.success("✅ Registration Successful!")
                                st.rerun()
        
        with tab4:
            subtab1, subtab2 = st.tabs(["Login", "Register"])
            with subtab1:
                with st.form("student_login"):
                    st.subheader("Student Login")
                    school_code = st.text_input("School Code")
                    admission_number = st.text_input("Admission Number")
                    password = st.text_input("Password", type="password")
                    if st.form_submit_button("Login", use_container_width=True):
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
                                        st.session_state.management_access = False
                                        st.session_state.personal_access = True
                                        st.session_state.page = 'dashboard'
                                        st.rerun()
                                st.error("Invalid admission number or password")
                            else:
                                st.error("School not found")
            
            with subtab2:
                with st.form("student_register"):
                    st.subheader("New Student Registration")
                    school_code = st.text_input("School Code")
                    fullname = st.text_input("Full Name")
                    email = st.text_input("Email (Optional)")
                    class_name = st.selectbox("Class", KENYAN_GRADES)
                    stream = st.text_input("Stream (e.g., East, North)")
                    password = st.text_input("Password", type="password")
                    confirm = st.text_input("Confirm Password", type="password")
                    
                    if st.form_submit_button("Register", use_container_width=True):
                        if not all([school_code, fullname, password]):
                            st.error("School code, name and password are required")
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
                                    "class": class_name,
                                    "stream": stream,
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
                                
                                st.success(f"✅ Registered! Your Admission Number is: **{admission_number}**")
                                st.info("📝 Save this number - you'll need it to login!")
        
        with tab5:
            subtab1, subtab2 = st.tabs(["Login", "Register"])
            with subtab1:
                with st.form("guardian_login"):
                    st.subheader("Guardian Login")
                    school_code = st.text_input("School Code")
                    student_admission = st.text_input("Student's Admission Number")
                    email = st.text_input("Your Email")
                    password = st.text_input("Password", type="password")
                    if st.form_submit_button("Login", use_container_width=True):
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
                                            st.session_state.management_access = False
                                            st.session_state.personal_access = True
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
                    st.subheader("New Guardian Registration")
                    school_code = st.text_input("School Code")
                    student_admission = st.text_input("Student's Admission Number")
                    fullname = st.text_input("Your Full Name")
                    email = st.text_input("Your Email")
                    phone = st.text_input("Phone Number")
                    password = st.text_input("Password", type="password")
                    confirm = st.text_input("Confirm Password", type="password")
                    
                    if st.form_submit_button("Register", use_container_width=True):
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
                                    "class": "",
                                    "stream": "",
                                    "admission_number": "",
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
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ============ SCHOOL MANAGEMENT SECTION ============
    elif st.session_state.main_section == 'management':
        st.markdown('<div class="section-container section-management">', unsafe_allow_html=True)
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4ECDC4, #6EE7E7); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 30px; box-shadow: 0 0 40px rgba(78, 205, 196, 0.5);">
            <h3 style="color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">📊 School Management System</h3>
            <p style="color: white;">Complete school administration - Requires login with admin/teacher credentials</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.user and st.session_state.current_school:
            if st.session_state.user['role'] in ['admin', 'teacher']:
                school_code = st.session_state.current_school['code']
                users = load_school_data(school_code, "users.json", [])
                
                mgmt_tab1, mgmt_tab2, mgmt_tab3, mgmt_tab4, mgmt_tab5, mgmt_tab6 = st.tabs([
                    "📚 Academics", "💰 Finance", "📋 Discipline", "👨‍🏫 Teacher Allocation", "🪑 Furniture", "⚙️ Admin"
                ])
                
                with mgmt_tab1:
                    st.subheader("Academic Records")
                    students = [u for u in users if u['role'] == 'student']
                    
                    with st.form("add_academic"):
                        student = st.selectbox("Select Student", [f"{s['fullname']} ({s['admission_number']})" for s in students])
                        subject = st.selectbox("Subject", PRIMARY_SUBJECTS)
                        score = st.number_input("Score (0-100)", 0, 100, 0)
                        term = st.selectbox("Term", ["Term 1", "Term 2", "Term 3"])
                        year = st.number_input("Year", datetime.now().year)
                        
                        if st.form_submit_button("Save Record"):
                            student_email = student.split('(')[1].rstrip(')')
                            student_obj = next(s for s in students if s['email'] == student_email)
                            add_academic_record(
                                school_code, student_email, subject, score, term, str(year),
                                st.session_state.user['email'], student_obj['class']
                            )
                            st.success("Record added!")
                            st.rerun()
                    
                    st.subheader("Recent Records")
                    grades = load_school_data(school_code, "academic_records.json", [])
                    if grades:
                        df = pd.DataFrame(grades[-10:])
                        st.dataframe(df[['student_email', 'subject', 'score', 'term', 'year']])
                
                with mgmt_tab2:
                    st.subheader("Fee Management")
                    students = [u for u in users if u['role'] == 'student']
                    
                    with st.form("add_fee"):
                        student = st.selectbox("Select Student", [f"{s['fullname']} ({s['admission_number']})" for s in students])
                        amount = st.number_input("Amount (KES)", 0.0, step=100.0)
                        fee_type = st.selectbox("Type", ["Tuition", "Transport", "Lunch", "Development"])
                        status = st.selectbox("Status", ["Paid", "Pending", "Overdue"])
                        
                        if st.form_submit_button("Save Fee"):
                            student_email = student.split('(')[1].rstrip(')')
                            add_fee_record(
                                school_code, student_email, amount,
                                datetime.now().strftime("%Y-%m-%d"), fee_type, status
                            )
                            st.success("Fee recorded!")
                            st.rerun()
                    
                    fees = load_school_data(school_code, "fees.json", [])
                    if fees:
                        total = sum(f['amount'] for f in fees if f['status'] == 'Paid')
                        st.metric("Total Collected", f"KES {total:,.0f}")
                
                with mgmt_tab3:
                    st.subheader("Discipline Records")
                    students = [u for u in users if u['role'] == 'student']
                    
                    with st.form("add_discipline"):
                        student = st.selectbox("Select Student", [f"{s['fullname']} ({s['admission_number']})" for s in students])
                        incident = st.text_area("Incident")
                        action = st.text_area("Action Taken")
                        
                        if st.form_submit_button("Save Record"):
                            student_email = student.split('(')[1].rstrip(')')
                            add_disciplinary_record(
                                school_code, student_email, incident, action,
                                datetime.now().strftime("%Y-%m-%d"), st.session_state.user['email']
                            )
                            st.success("Record saved!")
                            st.rerun()
                
                with mgmt_tab4:
                    st.subheader("Teacher Allocation")
                    teachers = [u for u in users if u['role'] == 'teacher']
                    
                    with st.form("allocate_teacher"):
                        teacher = st.selectbox("Select Teacher", [f"{t['fullname']} ({t['email']})" for t in teachers])
                        subject = st.selectbox("Subject", PRIMARY_SUBJECTS)
                        assigned_class = st.selectbox("Assigned Class", KENYAN_GRADES)
                        
                        if st.form_submit_button("Allocate"):
                            teacher_name = teacher.split('(')[0].strip()
                            add_teacher_allocation(
                                school_code, teacher_name, subject, assigned_class,
                                st.session_state.user['email']
                            )
                            st.success("Teacher allocated!")
                            st.rerun()
                    
                    allocations = load_school_data(school_code, "teacher_allocations.json", [])
                    if allocations:
                        st.dataframe(pd.DataFrame(allocations))
                
                with mgmt_tab5:
                    st.subheader("Furniture Allocation")
                    
                    with st.form("add_furniture"):
                        item = st.text_input("Item Name")
                        location = st.text_input("Location/Room")
                        quantity = st.number_input("Quantity", 1, 100, 1)
                        condition = st.selectbox("Condition", ["Good", "Fair", "Broken"])
                        
                        if st.form_submit_button("Add Furniture"):
                            add_furniture_allocation(
                                school_code, item, location, quantity, condition,
                                st.session_state.user['email']
                            )
                            st.success("Furniture added!")
                            st.rerun()
                    
                    furniture = load_school_data(school_code, "furniture.json", [])
                    if furniture:
                        st.dataframe(pd.DataFrame(furniture))
                
                with mgmt_tab6:
                    st.subheader("Administration")
                    if st.session_state.user['role'] == 'admin':
                        st.metric("Total Users", len(users))
                        st.metric("Students", len([u for u in users if u['role'] == 'student']))
                        st.metric("Teachers", len([u for u in users if u['role'] == 'teacher']))
                        
                        with st.form("update_school"):
                            school = st.session_state.current_school
                            name = st.text_input("School Name", school['name'])
                            motto = st.text_input("Motto", school.get('motto', ''))
                            
                            if st.form_submit_button("Update"):
                                all_schools = load_all_schools()
                                all_schools[school_code]['name'] = name
                                all_schools[school_code]['motto'] = motto
                                save_all_schools(all_schools)
                                st.session_state.current_school = all_schools[school_code]
                                st.success("Updated!")
                    else:
                        st.warning("Admin access required for this section.")
            else:
                st.warning("⚠️ You need admin or teacher access for School Management. Please login with appropriate credentials.")
                if st.button("Go to Login"):
                    st.session_state.main_section = 'community'
                    st.rerun()
        else:
            st.warning("⚠️ Please login first to access School Management.")
            if st.button("Go to Login"):
                st.session_state.main_section = 'community'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ============ PERSONAL DASHBOARD SECTION ============
    elif st.session_state.main_section == 'personal':
        st.markdown('<div class="section-container section-personal">', unsafe_allow_html=True)
        st.markdown("""
        <div style="background: linear-gradient(135deg, #45B7D1, #6EC8E0); padding: 30px; border-radius: 20px; text-align: center; margin-bottom: 30px; box-shadow: 0 0 40px rgba(69, 183, 209, 0.5);">
            <h3 style="color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">👤 Personal Dashboard</h3>
            <p style="color: white;">Your personal information, performance, and analytics - Requires login</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.user and st.session_state.current_school:
            user = st.session_state.user
            school_code = st.session_state.current_school['code']
            users = load_school_data(school_code, "users.json", [])
            
            personal_tab1, personal_tab2, personal_tab3, personal_tab4 = st.tabs([
                "👤 Profile", "📊 My Performance", "📈 Class Analytics", "⭐ Reviews"
            ])
            
            with personal_tab1:
                st.markdown("#### Personal Information")
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
                    with st.form("update_profile"):
                        fullname = st.text_input("Full Name", user['fullname'])
                        phone = st.text_input("Phone", user.get('phone', ''))
                        bio = st.text_area("Bio", user.get('bio', ''), height=100)
                        
                        if user['role'] == 'student':
                            st.info(f"🎫 Admission: **{user['admission_number']}**")
                            st.info(f"📚 Class: **{user['class']}**")
                            st.info(f"🌊 Stream: **{user['stream']}**")
                        elif user['role'] == 'guardian':
                            st.info(f"👪 Linked Students: {', '.join(user.get('linked_students', []))}")
                        
                        if st.form_submit_button("Update"):
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
                st.markdown("#### My Performance")
                
                if user['role'] == 'student':
                    grades = load_school_data(school_code, "academic_records.json", [])
                    attendance = load_school_data(school_code, "attendance.json", [])
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        perf = calculate_student_performance(grades, user['email'])
                        st.metric("Overall Average", f"{perf['average']}%")
                        
                        rank_class = "performance-excellent" if perf['average'] >= 80 else \
                                     "performance-good" if perf['average'] >= 70 else \
                                     "performance-average" if perf['average'] >= 50 else \
                                     "performance-needs-improvement"
                        st.markdown(f"<div class='{rank_class}' style='padding:10px; text-align:center;'>{perf['rank']}</div>", unsafe_allow_html=True)
                        
                        if perf['subjects']:
                            df = pd.DataFrame(list(perf['subjects'].items()), columns=['Subject', 'Score'])
                            fig = px.bar(df, x='Subject', y='Score', title="Subject Performance", color='Score', color_continuous_scale='YlOrRd')
                            st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        student_attendance = [a for a in attendance if a['student_email'] == user['email']]
                        if student_attendance:
                            present = len([a for a in student_attendance if a['status'] == 'Present'])
                            absent = len([a for a in student_attendance if a['status'] == 'Absent'])
                            late = len([a for a in student_attendance if a['status'] == 'Late'])
                            
                            att_df = pd.DataFrame({'Status': ['Present', 'Absent', 'Late'], 'Count': [present, absent, late]})
                            fig = px.pie(att_df, values='Count', names='Status', title="Attendance",
                                       color_discrete_sequence=['#28a745', '#dc3545', '#ffc107'])
                            st.plotly_chart(fig, use_container_width=True)
                            
                            rate = (present / len(student_attendance)) * 100 if student_attendance else 0
                            st.metric("Attendance Rate", f"{rate:.1f}%")
                        else:
                            st.info("No attendance records")
                    
                    # Fees Summary
                    st.subheader("Fee Status")
                    fees = load_school_data(school_code, "fees.json", [])
                    student_fees = [f for f in fees if f['student_email'] == user['email']]
                    if student_fees:
                        total_paid = sum(f['amount'] for f in student_fees if f['status'] == 'Paid')
                        total_pending = sum(f['amount'] for f in student_fees if f['status'] in ['Pending', 'Overdue'])
                        col1, col2 = st.columns(2)
                        col1.metric("Total Paid", f"KES {total_paid:,.0f}")
                        col2.metric("Outstanding", f"KES {total_pending:,.0f}")
                
                elif user['role'] == 'teacher':
                    st.subheader("Classes Taught")
                    allocations = load_school_data(school_code, "teacher_allocations.json", [])
                    my_allocations = [a for a in allocations if a['teacher_name'] == user['fullname']]
                    if my_allocations:
                        for a in my_allocations:
                            st.info(f"📚 {a['subject']} - {a['assigned_class']}")
                    
                    st.subheader("Reviews Given")
                    reviews = load_school_data(school_code, "teacher_reviews.json", [])
                    my_reviews = [r for r in reviews if r['teacher_email'] == user['email']]
                    st.metric("Total Reviews", len(my_reviews))
                
                elif user['role'] == 'guardian':
                    for adm in user.get('linked_students', []):
                        student = next((u for u in users if u.get('admission_number') == adm), None)
                        if student:
                            st.subheader(f"{student['fullname']}")
                            grades = load_school_data(school_code, "academic_records.json", [])
                            perf = calculate_student_performance(grades, student['email'])
                            st.metric("Average", f"{perf['average']}%")
            
            with personal_tab3:
                st.markdown("#### Class Analytics")
                
                if user['role'] == 'student':
                    # Show class performance comparison
                    grades = load_school_data(school_code, "academic_records.json", [])
                    my_grades = [g for g in grades if g['student_email'] == user['email']]
                    
                    if my_grades:
                        my_class = user['class']
                        my_subjects = {g['subject'] for g in my_grades}
                        
                        for subject in my_subjects:
                            class_grades = [g['score'] for g in grades if g['class_name'] == my_class and g['subject'] == subject]
                            my_score = next(g['score'] for g in my_grades if g['subject'] == subject)
                            
                            if class_grades:
                                avg_class = sum(class_grades) / len(class_grades)
                                col1, col2, col3 = st.columns(3)
                                col1.metric(f"{subject}", f"{my_score}%")
                                col2.metric("Class Average", f"{avg_class:.1f}%")
                                col3.metric("Difference", f"{my_score - avg_class:.1f}%", delta_color="off")
                
                elif user['role'] == 'teacher':
                    st.subheader("Class Performance Overview")
                    allocations = load_school_data(school_code, "teacher_allocations.json", [])
                    my_allocations = [a for a in allocations if a['teacher_name'] == user['fullname']]
                    
                    for alloc in my_allocations:
                        grades = load_school_data(school_code, "academic_records.json", [])
                        class_perf = get_class_performance(grades, alloc['assigned_class'], "Term 1", str(datetime.now().year))
                        if class_perf:
                            st.write(f"**{alloc['assigned_class']} - {alloc['subject']}**")
                            df = pd.DataFrame(list(class_perf.items()), columns=['Subject', 'Average'])
                            st.dataframe(df)
            
            with personal_tab4:
                st.markdown("#### Reviews & Feedback")
                
                if user['role'] == 'student':
                    reviews = load_school_data(school_code, "teacher_reviews.json", [])
                    my_reviews = [r for r in reviews if r['student_email'] == user['email']]
                    
                    for r in my_reviews:
                        teacher = next((u for u in users if u['email'] == r['teacher_email']), None)
                        teacher_name = teacher['fullname'] if teacher else r['teacher_email']
                        st.markdown(f"""
                        <div class="golden-card">
                            <strong>From: {teacher_name}</strong><br>
                            ⭐ {'⭐' * r['rating']}{'☆' * (5-r['rating'])}<br>
                            📅 {r['date']}<br>
                            💬 {r['review_text']}
                        </div>
                        """, unsafe_allow_html=True)
                
                elif user['role'] == 'teacher':
                    with st.form("give_review"):
                        students = [u for u in users if u['role'] == 'student']
                        student = st.selectbox("Student", [f"{s['fullname']} ({s['admission_number']})" for s in students])
                        rating = st.slider("Rating", 1, 5, 3)
                        review = st.text_area("Review")
                        
                        if st.form_submit_button("Submit"):
                            student_email = student.split('(')[1].rstrip(')')
                            student_obj = next(s for s in students if s['email'] == student_email)
                            add_teacher_review(
                                school_code, user['email'], student_email, review, rating,
                                datetime.now().strftime("%Y-%m-%d"), student_obj['class']
                            )
                            st.success("Review submitted!")
                            st.rerun()
        else:
            st.warning("⚠️ Please login first to access Personal Dashboard.")
            if st.button("Go to Login"):
                st.session_state.main_section = 'community'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ----- DASHBOARD (for logged in users with sidebar) -----
elif st.session_state.page == 'dashboard' and st.session_state.current_school and st.session_state.user:
    school = st.session_state.current_school
    user = st.session_state.user
    school_code = school['code']
    
    users = load_school_data(school_code, "users.json", [])
    classes = load_school_data(school_code, "classes.json", [])
    announcements = load_school_data(school_code, "announcements.json", [])
    assignments = load_school_data(school_code, "assignments.json", [])
    
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
            emoji = "👑" if user['role'] == 'admin' else "👨‍🏫" if user['role'] == 'teacher' else "👨‍🎓" if user['role'] == 'student' else "👪"
            st.markdown(f"<h1 style='font-size: 2rem; margin: 0;'>{emoji}</h1>", unsafe_allow_html=True)
        
        role_display = "ADMIN" if user['role'] == 'admin' else "TEACHER" if user['role'] == 'teacher' else "STUDENT" if user['role'] == 'student' else "GUARDIAN"
        st.markdown(f"""
        <div style="color: #FFD700; flex: 1;">
            <strong>{user['fullname']}</strong><br>
            <span style="background: rgba(0,0,0,0.3); color: #FFD700; padding: 2px 8px; border-radius: 12px; font-size: 0.7rem;">{role_display}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        
        options = ["Dashboard", "Announcements", "Community", "School Management", "Personal Dashboard", "Profile"]
        
        menu = st.radio("Navigation", options, index=0, label_visibility="collapsed")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.page = 'welcome'
                st.rerun()
        with col2:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.user = None
                st.session_state.current_school = None
                st.session_state.page = 'welcome'
                st.rerun()
    
    # ============ MAIN CONTENT ============
    if menu == "Dashboard":
        st.markdown(f"<h2 style='text-align: center;'>Welcome, {user['fullname']}!</h2>", unsafe_allow_html=True)
        
        if user['role'] == 'admin':
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Students", school['stats'].get('students', 0))
            col2.metric("Teachers", school['stats'].get('teachers', 0))
            col3.metric("Guardians", school['stats'].get('guardians', 0))
            col4.metric("Classes", school['stats'].get('classes', 0))
        
        elif user['role'] == 'teacher':
            col1, col2 = st.columns(2)
            col1.metric("Classes", len([c for c in classes if c.get('teacher') == user['email']]))
            col2.metric("Assignments", len([a for a in assignments if a.get('created_by') == user['email']]))
        
        elif user['role'] == 'student':
            col1, col2 = st.columns(2)
            col1.metric("Admission", user['admission_number'])
            col2.metric("Class", user['class'])
        
        st.info("Use the navigation menu to access School Management or Personal Dashboard")
    
    elif menu == "School Management":
        if user['role'] in ['admin', 'teacher']:
            st.markdown("<h2 style='text-align: center;'>📊 School Management</h2>", unsafe_allow_html=True)
            st.info("School Management features are available here. Redirecting...")
            # Simplified - full implementation would be similar to above
        else:
            st.warning("Access denied. Admin/Teacher only.")
    
    elif menu == "Personal Dashboard":
        st.markdown("<h2 style='text-align: center;'>👤 Personal Dashboard</h2>", unsafe_allow_html=True)
        st.info("Personal Dashboard features are available here. Redirecting...")
        # Simplified - full implementation would be similar to above
    
    elif menu == "Announcements":
        st.markdown("<h2 style='text-align: center;'>📢 Announcements</h2>", unsafe_allow_html=True)
        if announcements:
            for a in announcements[-5:]:
                st.markdown(f"<div class='golden-card'><h4>{a['title']}</h4><p>{a['content']}</p><small>{a['date']}</small></div>", unsafe_allow_html=True)
        else:
            st.info("No announcements")
    
    elif menu == "Community":
        st.markdown("<h2 style='text-align: center;'>🌍 Community</h2>", unsafe_allow_html=True)
        st.info("Community features - chat, friends, groups would be here")
    
    elif menu == "Profile":
        st.markdown("<h2 style='text-align: center;'>👤 Profile</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 2])
        with col1:
            if user.get('profile_pic'):
                st.image(user['profile_pic'], width=150)
        with col2:
            st.write(f"**Name:** {user['fullname']}")
            st.write(f"**Email:** {user['email']}")
            st.write(f"**Role:** {user['role'].title()}")
            if user['role'] == 'student':
                st.write(f"**Admission:** {user['admission_number']}")
                st.write(f"**Class:** {user['class']}")
                st.write(f"**Stream:** {user['stream']}")

else:
    st.error("Something went wrong.")
    if st.button("Restart"):
        st.session_state.page = 'welcome'
        st.rerun()
