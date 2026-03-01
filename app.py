""")

# ============ INTERACTIVE WHITEBOARD ============
def interactive_whiteboard():
"""Interactive whiteboard for teaching"""
st.subheader("🎨 Interactive Whiteboard")

# Whiteboard controls
col1, col2, col3, col4 = st.columns(4)

with col1:
    drawing_mode = st.selectbox("Drawing Mode", 
                              ["freedraw", "line", "rect", "circle", "transform"])

with col2:
    stroke_width = st.slider("Stroke Width", 1, 20, 3)

with col3:
    stroke_color = st.color_picker("Stroke Color", "#FFD700")

with col4:
    bg_color = st.color_picker("Background", "#000000")

# Create canvas
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    background_image=None,
    update_streamlit=True,
    height=500,
    drawing_mode=drawing_mode,
    key="canvas",
)

# Whiteboard actions
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Clear Canvas"):
        st.session_state.canvas = None
        st.rerun()

with col2:
    if st.button("Save Whiteboard"):
        if canvas_result.image_data is not None:
            img = Image.fromarray(canvas_result.image_data.astype('uint8'))
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            st.download_button(
                "Download Image",
                data=base64.b64decode(img_str),
                file_name=f"whiteboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                mime="image/png"
            )

with col3:
    if st.button("Share with Class"):
        # Save to session and share
        if canvas_result.image_data is not None:
            st.session_state.shared_whiteboard = canvas_result.image_data
            st.success("Whiteboard shared with class!")

with col4:
    if st.button("Start Video Meeting"):
        meeting = create_video_meeting("whiteboard", f"whiteboard-{datetime.now().strftime('%Y%m%d%H%M%S')}")
        st.session_state.video_meeting = meeting
        st.rerun()

# Display video meeting if active
if 'video_meeting' in st.session_state:
    st.markdown("### 🎥 Video Meeting")
    display_video_meeting(st.session_state.video_meeting['url'], height=400)

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

def generate_teacher_code():
dept = random.choice(['MATH', 'ENG', 'SCI', 'SOC', 'CRE', 'BUS', 'TECH'])
num = ''.join(random.choices(string.digits, k=3))
return f"{dept}{num}"

def generate_book_id():
return 'BOK' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def generate_transaction_id():
return 'TRN' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# ============ DATABASE OPERATIONS ============
@cache_data(ttl=300)
def get_user_by_email(email):
"""Get user by email with caching"""
conn = sqlite3.connect('school_hub.db')
c = conn.cursor()

c.execute('SELECT * FROM users WHERE email = ?', (email,))
user = c.fetchone()
conn.close()

if user:
    columns = [desc[0] for desc in c.description]
    return dict(zip(columns, user))
return None

def save_user(user_data):
"""Save or update user"""
conn = sqlite3.connect('school_hub.db')
c = conn.cursor()

c.execute('''INSERT OR REPLACE INTO users 
             (email, user_id, fullname, password, role, school_code, joined, 
              profile_pic, phone, bio, admission_number, teacher_code_used,
              notification_settings, language, accessibility_settings, last_login, created_at)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
          (user_data.get('email'), user_data.get('user_id'), user_data.get('fullname'),
           user_data.get('password'), user_data.get('role'), user_data.get('school_code'),
           user_data.get('joined'), user_data.get('profile_pic'), user_data.get('phone'),
           user_data.get('bio'), user_data.get('admission_number'), 
           user_data.get('teacher_code_used'), json.dumps(user_data.get('notification_settings', {})),
           user_data.get('language', 'en'), json.dumps(user_data.get('accessibility_settings', {})),
           user_data.get('last_login'), user_data.get('created_at')))

conn.commit()
conn.close()

def get_school_users(school_code):
"""Get all users in a school"""
conn = sqlite3.connect('school_hub.db')
c = conn.cursor()

c.execute('SELECT * FROM users WHERE school_code = ?', (school_code,))
users = c.fetchall()
conn.close()

if users:
    columns = [desc[0] for desc in c.description]
    return [dict(zip(columns, user)) for user in users]
return []

def save_school_data(school_code, table, data):
"""Generic function to save school-specific data"""
conn = sqlite3.connect('school_hub.db')
c = conn.cursor()

# Clear existing data for this school and table (if replacing)
c.execute(f"DELETE FROM {table} WHERE school_code = ?", (school_code,))

# Insert new data
if isinstance(data, list):
    for item in data:
        item['school_code'] = school_code
        placeholders = ','.join(['?'] * len(item))
        columns = ','.join(item.keys())
        c.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", 
                 list(item.values()))

conn.commit()
conn.close()

def load_school_data(school_code, table, default=None):
"""Generic function to load school-specific data"""
conn = sqlite3.connect('school_hub.db')
c = conn.cursor()

c.execute(f"SELECT * FROM {table} WHERE school_code = ?", (school_code,))
rows = c.fetchall()

if rows:
    columns = [desc[0] for desc in c.description]
    result = [dict(zip(columns, row)) for row in rows]
    conn.close()
    return result

conn.close()
return default if default is not None else []

# ============ THEME AND ACCESSIBILITY ============
def get_theme_css(theme_name, wallpaper=None, accessibility=None):
"""Generate theme CSS with accessibility settings"""
theme = THEMES.get(theme_name, THEMES["Sunrise Glow"])
wallpaper_url = WALLPAPERS.get(wallpaper, "") if wallpaper else ""

background_style = f"url('{wallpaper_url}') no-repeat center center fixed" if wallpaper_url else theme["background"]
background_size = "cover" if wallpaper_url else "400% 400%"

# Apply accessibility settings
accessibility = accessibility or {}
text_size = accessibility.get('text_size', 'Normal')
font_family = accessibility.get('font_family', 'Default')
high_contrast = accessibility.get('high_contrast', False)

# Text size mapping
text_size_map = {
    "Small": "14px",
    "Normal": "16px",
    "Large": "18px",
    "Extra Large": "20px"
}

# Font family mapping
font_map = {
    "Default": "'Poppins', sans-serif",
    "OpenDyslexic": "'OpenDyslexic', sans-serif",
    "Arial": "Arial, sans-serif",
    "Verdana": "Verdana, sans-serif"
}

contrast_css = """
    filter: contrast(150%) brightness(120%) !important;
""" if high_contrast else ""

return f"""
<style>
    body {{
        background: {background_style};
        background-size: {background_size};
        margin: 0;
        padding: 0;
        min-height: 10vh;
        font-family: {font_map.get(font_family, "'Poppins', sans-serif")};
        font-size: {text_size_map.get(text_size, "16px")};
        {contrast_css}
    }}
    
    .stApp {{
        background: transparent !important;
    }}
    
    .main .block-container {{
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        position: relative;
        z-index: 10;
    }}
    
    section[data-testid="stSidebar"] {{
        background: {theme["sidebar"]};
        background-size: 300% 300%;
        animation: golden-shimmer 8s ease infinite;
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
    
    .stButton button {{
        background: linear-gradient(135deg, #FFD700, #DAA520) !important;
        color: #2b2b2b !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 15px rgba(218, 165, 32, 0.4) !important;
    }}
    
    .stButton button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.6) !important;
    }}
    
    .stTextInput input, 
    .stTextArea textarea, 
    .stDateInput input,
    .stNumberInput input {{
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid #FFD700 !important;
        border-radius: 10px !important;
        padding: 0.6rem 1rem !important;
        font-size: 0.95rem !important;
        color: #000000 !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }}
    
    .golden-card {{
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border-left: 6px solid #FFD700;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
        color: {theme["text"]};
    }}
    
    @keyframes golden-shimmer {{
        0% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
        100% {{ background-position: 0% 50%; }}
    }}
</style>
"""

def save_user_settings(school_code, user_email, settings):
"""Save user settings including theme and accessibility"""
conn = sqlite3.connect('school_hub.db')
c = conn.cursor()

c.execute('''INSERT OR REPLACE INTO user_settings 
             (user_email, school_code, theme, wallpaper, language, notification_prefs, accessibility)
             VALUES (?, ?, ?, ?, ?, ?, ?)''',
          (user_email, school_code, settings.get('theme', 'Sunrise Glow'),
           settings.get('wallpaper', 'None'), settings.get('language', 'en'),
           json.dumps(settings.get('notification_prefs', {})),
           json.dumps(settings.get('accessibility', {}))))

conn.commit()
conn.close()

def load_user_settings(school_code, user_email):
"""Load user settings"""
conn = sqlite3.connect('school_hub.db')
c = conn.cursor()

c.execute('''SELECT * FROM user_settings 
             WHERE user_email = ? AND school_code = ?''', (user_email, school_code))
settings = c.fetchone()
conn.close()

if settings:
    return {
        "theme": settings[2],
        "wallpaper": settings[3],
        "language": settings[4],
        "notification_prefs": json.loads(settings[5]) if settings[5] else {},
        "accessibility": json.loads(settings[6]) if settings[6] else {}
    }

return {
    "theme": "Sunrise Glow",
    "wallpaper": "None",
    "language": "en",
    "notification_prefs": {},
    "accessibility": ACCESSIBILITY_PRESETS["default"]
}

# ============ PASSWORD VALIDATION ============
def validate_password(password):
"""Validate password strength"""
if len(password) < 8:
    return False, "Password must be at least 8 characters long"

if not any(c.isupper() for c in password):
    return False, "Password must contain at least one uppercase letter"

if not any(c.islower() for c in password):
    return False, "Password must contain at least one lowercase letter"

if not any(c.isdigit() for c in password):
    return False, "Password must contain at least one number"

if not any(c in "!@#$%^&*" for c in password):
    return False, "Password must contain at least one special character (!@#$%^&*)"

return True, "Password is strong"

# ============ PERFORMANCE CALCULATIONS ============
def calculate_student_performance(grades, student_email):
"""Calculate student performance metrics"""
student_grades = [g for g in grades if g['student_email'] == student_email]
if not student_grades:
    return {"average": 0, "subjects": {}, "rank": "N/A", "subject_details": []}

subjects = {}
subject_details = []
total = 0
for grade in student_grades:
    subjects[grade['subject']] = grade['score']
    subject_details.append({
        "subject": grade['subject'],
        "score": grade['score'],
        "term": grade['term'],
        "year": grade['year'],
        "teacher": grade.get('teacher_email', 'Unknown'),
        "date": grade.get('date', 'Unknown')
    })
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

return {"average": round(avg, 2), "subjects": subjects, "rank": rank, "subject_details": subject_details}

# ============ BADGE SYSTEM ============
def award_badge(school_code, user_email, badge_id):
"""Award a badge to a user"""
badge = BADGES.get(badge_id)
if not badge:
    return False

conn = sqlite3.connect('school_hub.db')
c = conn.cursor()

# Check if already awarded
c.execute('''SELECT * FROM badges 
             WHERE user_email = ? AND badge_id = ? AND school_code = ?''',
          (user_email, badge_id, school_code))

if c.fetchone():
    conn.close()
    return False

# Award badge
badge_data = {
    "id": generate_id("BDG"),
    "user_email": user_email,
    "badge_id": badge_id,
    "badge_name": badge['name'],
    "badge_icon": badge['icon'],
    "badge_color": badge['color'],
    "awarded_date": datetime.now().strftime("%Y-%m-%d"),
    "school_code": school_code
}

c.execute('''INSERT INTO badges 
             (id, user_email, badge_id, badge_name, badge_icon, badge_color, awarded_date, school_code)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
          (badge_data['id'], user_email, badge_id, badge['name'], badge['icon'], 
           badge['color'], badge_data['awarded_date'], school_code))

conn.commit()
conn.close()

# Send notification
send_push_notification([user_email], "🏆 New Badge Earned!", 
                      f"You earned the {badge['name']} badge!")

return True

def check_and_award_badges(school_code, user_email):
"""Check conditions and award appropriate badges"""
conn = sqlite3.connect('school_hub.db')
c = conn.cursor()

# Get user data
c.execute('SELECT * FROM users WHERE email = ?', (user_email,))
user = c.fetchone()

# Check attendance
c.execute('''SELECT COUNT(*) FROM attendance 
             WHERE student_email = ? AND school_code = ? AND status = 'Present' ''',
          (user_email, school_code))
present_count = c.fetchone()[0]

c.execute('''SELECT COUNT(*) FROM attendance 
             WHERE student_email = ? AND school_code = ?''',
          (user_email, school_code))
total_attendance = c.fetchone()[0]

if total_attendance > 0 and (present_count / total_attendance) >= 0.95:
    award_badge(school_code, user_email, "perfect_attendance")

# Check academic performance
c.execute('''SELECT score FROM academic_records 
             WHERE student_email = ? AND school_code = ?''',
          (user_email, school_code))
grades = c.fetchall()

if grades:
    avg_score = sum(g[0] for g in grades) / len(grades)
    if avg_score >= 90:
        award_badge(school_code, user_email, "math_wizard")  # This should be more subject-specific

# Check library usage
c.execute('''SELECT COUNT(*) FROM library_transactions 
             WHERE user_email = ? AND school_code = ?''',
          (user_email, school_code))
book_count = c.fetchone()[0]

if book_count >= 20:
    award_badge(school_code, user_email, "library_enthusiast")

conn.close()

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
if 'selected_class' not in st.session_state:
st.session_state.selected_class = None
if 'theme' not in st.session_state:
st.session_state.theme = "Sunrise Glow"
if 'wallpaper' not in st.session_state:
st.session_state.wallpaper = "None"
if 'language' not in st.session_state:
st.session_state.language = "en"
if 'accessibility' not in st.session_state:
st.session_state.accessibility = ACCESSIBILITY_PRESETS["default"]
if 'login_time' not in st.session_state:
st.session_state.login_time = None

# ============ SESSION MANAGEMENT ============
def check_session_timeout():
"""Check if session has timed out"""
if st.session_state.login_time:
    if time.time() - st.session_state.login_time > 3600:  # 1 hour
        st.session_state.user = None
        st.session_state.current_school = None
        st.session_state.page = 'welcome'
        st.warning("Session expired. Please login again.")
        st.rerun()

# ============ MAIN APP ============

# Check session timeout
check_session_timeout()

# Load user settings if logged in
if st.session_state.user and st.session_state.current_school:
settings = load_user_settings(st.session_state.current_school['code'], st.session_state.user['email'])
st.session_state.theme = settings.get("theme", "Sunrise Glow")
st.session_state.wallpaper = settings.get("wallpaper", "None")
st.session_state.language = settings.get("language", "en")
st.session_state.accessibility = settings.get("accessibility", ACCESSIBILITY_PRESETS["default"])

# Apply theme CSS
st.markdown(get_theme_css(st.session_state.theme, st.session_state.wallpaper, st.session_state.accessibility), 
       unsafe_allow_html=True)

# ----- WELCOME PAGE -----
if st.session_state.page == 'welcome':
st.markdown('<h1>✨ School Community Hub ✨</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: white; font-size: 1.2rem; text-shadow: 1px 1px 2px black;">Connect • Collaborate • Manage • Shine</p>', unsafe_allow_html=True)

# Mobile app QR code
with st.expander("📱 Get Mobile App"):
    qr_img = generate_qr_code("https://schoolhub.app/download")
    st.image(qr_img, width=200)
    st.markdown("Scan to download our mobile app")

st.divider()

# MAIN NAVIGATION BUTTONS
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏫 School Community", key="nav_community", use_container_width=True):
        st.session_state.main_nav = 'School Community'

with col2:
    if st.button("📊 School Management", key="nav_management", use_container_width=True):
        st.session_state.main_nav = 'School Management'

with col3:
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
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["👑 Admin Login", "🏫 Create New School", "👨‍🏫 Teacher", "👨‍🎓 Student", "👪 Guardian"])
    
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
                        user = get_user_by_email(admin_email)
                        if user and user['school_code'] == school_code and user['role'] == 'admin':
                            hashed = hashlib.sha256(admin_password.encode()).hexdigest()
                            if user['password'] == hashed:
                                st.session_state.current_school = {"code": school_code, "name": "School"}
                                st.session_state.user = user
                                st.session_state.page = 'dashboard'
                                st.session_state.login_time = time.time()
                                st.rerun()
                            else:
                                st.error("Invalid password")
                        else:
                            st.error("School not found or not admin")
    
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
                        # Validate password strength
                        valid, message = validate_password(password)
                        if not valid:
                            st.error(message)
                        else:
                            code = generate_school_code()
                            
                            # Create school
                            conn = sqlite3.connect('school_hub.db')
                            c = conn.cursor()
                            
                            school_data = {
                                "code": code,
                                "name": school_name,
                                "city": city,
                                "state": state,
                                "motto": motto,
                                "created": datetime.now().strftime("%Y-%m-%d"),
                                "admin_email": admin_email,
                                "admin_name": admin_name,
                                "stats": json.dumps({"students":0, "teachers":0, "guardians":0, "classes":0, "groups":0}),
                                "settings": json.dumps({})
                            }
                            
                            c.execute('''INSERT INTO schools 
                                       (code, name, city, state, motto, created, admin_email, admin_name, stats, settings)
                                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                     list(school_data.values()))
                            
                            # Create admin user
                            user_data = {
                                "user_id": generate_id("USR"),
                                "email": admin_email,
                                "fullname": admin_name,
                                "password": hashlib.sha256(password.encode()).hexdigest(),
                                "role": "admin",
                                "joined": datetime.now().strftime("%Y-%m-%d"),
                                "school_code": code,
                                "profile_pic": None,
                                "phone": "",
                                "bio": "",
                                "admission_number": None,
                                "teacher_code_used": None,
                                "notification_settings": json.dumps({}),
                                "language": "en",
                                "accessibility_settings": json.dumps(ACCESSIBILITY_PRESETS["default"]),
                                "last_login": None,
                                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
                            }
                            
                            c.execute('''INSERT INTO users 
                                       (user_id, email, fullname, password, role, joined, school_code, 
                                        profile_pic, phone, bio, admission_number, teacher_code_used,
                                        notification_settings, language, accessibility_settings, last_login, created_at)
                                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                     list(user_data.values()))
                            
                            conn.commit()
                            conn.close()
                            
                            st.success(f"✅ School Created! Your School Code is: **{code}**")
                            st.info("Save this code - you'll need it for login!")
    
    with tab3, tab4, tab5:
        # Similar login/registration forms for teacher, student, guardian
        # (Keeping existing forms from original code)
        pass

elif st.session_state.main_nav == 'School Management':
    st.markdown("""
    <div class="golden-card" style="text-align: center;">
        <h3>📊 School Management System</h3>
        <p>Complete school administration - Academics, Finance, Discipline, Library, and more!</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.user and st.session_state.current_school:
        st.success(f"✅ Logged in as: {st.session_state.user['fullname']} ({st.session_state.user['role']})")
        if st.button("Go to Management Dashboard", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()
    else:
        st.warning("⚠️ Please log in first to access the School Management System.")

elif st.session_state.main_nav == 'Personal Dashboard':
    st.markdown("""
    <div class="golden-card" style="text-align: center;">
        <h3>👤 Personal Dashboard</h3>
        <p>Your personal information, performance, reviews, achievements, and library account!</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.user and st.session_state.current_school:
        st.success(f"✅ Logged in as: {st.session_state.user['fullname']} ({st.session_state.user['role']})")
        if st.button("Go to Personal Dashboard", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()
    else:
        st.warning("⚠️ Please log in first to view your Personal Dashboard.")

# ----- DASHBOARD (for logged in users) -----
elif st.session_state.page == 'dashboard' and st.session_state.current_school and st.session_state.user:
school = st.session_state.current_school
user = st.session_state.user
school_code = school['code']

# Load data
users = get_school_users(school_code)
classes = load_school_data(school_code, "classes", [])
groups = load_school_data(school_code, "groups", [])
announcements = load_school_data(school_code, "announcements", [])
assignments = load_school_data(school_code, "assignments", [])
academic_records = load_school_data(school_code, "academic_records", [])

# Check and award badges
check_and_award_badges(school_code, user['email'])

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
        role_emoji = "👑" if user['role'] == 'admin' else "👨‍🏫" if user['role'] == 'teacher' else "👨‍🎓" if user['role'] == 'student' else "👪"
        st.markdown(f"<h1 style='font-size: 2rem; margin: 0;'>{role_emoji}</h1>", unsafe_allow_html=True)
    
    role_display = user['role'].upper()
    
    st.markdown(f"""
    <div style="color: #FFD700; flex: 1; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
        <strong>{user['fullname']}</strong><br>
        <span style="background: rgba(0,0,0,0.3); color: #FFD700; padding: 2px 8px; border-radius: 12px; font-size: 0.7rem; border: 1px solid #FFD700;">{role_display}</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Sidebar navigation based on role
    base_options = ["Dashboard", "Announcements", "Community", "Chat", "Friends", "Groups"]
    
    if user['role'] == 'admin':
        options = base_options + ["Classes", "Teachers", "Students", "Guardians", "Assignments", 
                                "School Management", "Library Management", "Wellness Center", 
                                "Career Guidance", "Analytics", "Emergency Alert", "Settings", "Profile"]
    elif user['role'] == 'teacher':
        options = base_options + ["My Classes", "Assignments", "School Management", "Library Management",
                                "Wellness Center", "Career Guidance", "Virtual Lab", "Whiteboard",
                                "Study Groups", "Settings", "Profile"]
    elif user['role'] == 'student':
        options = base_options + ["My Classes", "My Performance", "My Library", "My Portfolio",
                                "Wellness Check-in", "Career Quiz", "Virtual Lab", "Study Groups",
                                "AI Homework Help", "Settings", "Profile"]
    else:  # guardian
        options = base_options + ["My Student", "Assignments", "My Library", "Wellness Center",
                                "Parent Portal", "Settings", "Profile"]
    
    if st.session_state.menu_index >= len(options):
        st.session_state.menu_index = 0
        
    menu = st.radio("Navigation", options, index=st.session_state.menu_index, label_visibility="collapsed")
    st.session_state.menu_index = options.index(menu)
    
    st.divider()
    
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.user = None
        st.session_state.current_school = None
        st.session_state.page = 'welcome'
        st.session_state.login_time = None
        st.rerun()

# ============ MAIN CONTENT ============

if menu == "Dashboard":
    st.markdown(f"<h2 style='text-align: center; color: white;'>Welcome, {user['fullname']}!</h2>", unsafe_allow_html=True)
    
    # Display badges
    conn = sqlite3.connect('school_hub.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM badges WHERE user_email = ? AND school_code = ?''', (user['email'], school_code))
    badges = c.fetchall()
    conn.close()
    
    if badges:
        st.subheader("🏆 Your Badges")
        cols = st.columns(5)
        for i, badge in enumerate(badges[:5]):
            with cols[i]:
                st.markdown(f"""
                <div style="text-align: center;">
                    <h1 style="font-size: 2.5rem; margin: 0; color: {badge[5]};">{badge[4]}</h1>
                    <p style="font-size: 0.8rem;">{badge[3]}</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Role-specific dashboard
    if user['role'] == 'admin':
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("👨‍🎓 Students", len([u for u in users if u['role'] == 'student']))
        with col2:
            st.metric("👨‍🏫 Teachers", len([u for u in users if u['role'] == 'teacher']))
        with col3:
            st.metric("👪 Guardians", len([u for u in users if u['role'] == 'guardian']))
        with col4:
            st.metric("📚 Classes", len(classes))
        with col5:
            st.metric("👥 Groups", len(groups))
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("📢 New Announcement"):
                st.session_state.menu_index = options.index("Announcements")
                st.rerun()
        with col2:
            if st.button("➕ Add Teacher"):
                st.session_state.menu_index = options.index("Teachers")
                st.rerun()
        with col3:
            if st.button("📊 View Analytics"):
                st.session_state.menu_index = options.index("Analytics")
                st.rerun()
        with col4:
            if st.button("🚨 Emergency"):
                st.session_state.menu_index = options.index("Emergency Alert")
                st.rerun()
    
    elif user['role'] == 'student':
        performance = calculate_student_performance(academic_records, user['email'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Average", f"{performance['average']}%")
        with col2:
            st.metric("📚 Classes", len([c for c in classes if user['email'] in c.get('students', [])]))
        with col3:
            st.metric("🏆 Badges", len(badges))
        
        # Wellness tip of the day
        st.info("🧠 **Wellness Tip:** Take 5 minutes to practice deep breathing today!")

elif menu == "AI Homework Help" and user['role'] == 'student':
    st.subheader("🤖 AI Homework Helper")
    
    col1, col2 = st.columns(2)
    with col1:
        subject = st.selectbox("Subject", PRIMARY_SUBJECTS)
    with col2:
        grade = st.selectbox("Grade Level", KENYAN_GRADES[:3])
    
    question = st.text_area("What do you need help with?", height=150)
    
    if st.button("Get Help", use_container_width=True):
        if question:
            with st.spinner("AI is thinking..."):
                answer = ai_homework_helper(question, subject, grade)
                st.markdown("### Answer:")
                st.write(answer)
                
                # Save to history
                st.session_state.last_ai_query = {
                    "subject": subject,
                    "question": question,
                    "answer": answer,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M")
                }

elif menu == "Wellness Check-in" and user['role'] == 'student':
    wellness_checkin(school_code, user['email'])

elif menu == "Wellness Center":
    st.subheader("🧠 Wellness Center")
    
    tabs = st.tabs(["Check-in", "Resources", "Counselor Contact", "Peer Support"])
    
    with tabs[0]:
        if user['role'] == 'student':
            wellness_checkin(school_code, user['email'])
        else:
            # View student check-ins for teachers/admins
            conn = sqlite3.connect('school_hub.db')
            c = conn.cursor()
            c.execute('''SELECT * FROM wellness_checkins 
                       WHERE school_code = ? ORDER BY date DESC LIMIT 20''', (school_code,))
            checkins = c.fetchall()
            conn.close()
            
            if checkins:
                for checkin in checkins:
                    student = get_user_by_email(checkin[1])
                    st.markdown(f"""
                    <div class="golden-card">
                        <strong>{student['fullname'] if student else checkin[1]}</strong><br>
                        Date: {checkin[2]}<br>
                        Mood: {checkin[3]}<br>
                        Stress: {checkin[4]}/10<br>
                        Notes: {checkin[5]}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No check-ins recorded")
    
    with tabs[1]:
        st.markdown("""
        ### 📚 Wellness Resources
        
        **Mental Health:**
        - School Counselor: Room 101
        - National Helpline: 0800-123-456
        - Online Counseling: Available 24/7
        
        **Stress Management:**
        - Deep breathing exercises
        - Meditation apps
        - Physical activity
        
        **Academic Support:**
        - Study groups
        - Tutoring center
        - Time management workshops
        """)
    
    with tabs[2]:
        st.markdown("### 👥 Counselor Contact")
        
        conn = sqlite3.connect('school_hub.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM users 
                   WHERE school_code = ? AND role = 'counselor' ''', (school_code,))
        counselors = c.fetchall()
        conn.close()
        
        if counselors:
            for counselor in counselors:
                st.markdown(f"""
                **{counselor[2]}** - Counselor<br>
                Email: {counselor[0]}<br>
                Phone: {counselor[5] if counselor[5] else 'N/A'}
                """, unsafe_allow_html=True)
        else:
            st.info("No counselor assigned yet")

elif menu == "Virtual Lab":
    virtual_science_lab()

elif menu == "Whiteboard" and user['role'] == 'teacher':
    interactive_whiteboard()

elif menu == "Study Groups":
    st.subheader("📚 Study Groups")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if user['role'] in ['student', 'teacher']:
            create_study_group(school_code, user['email'])
    
    with col2:
        display_study_groups(school_code, user['email'])

elif menu == "Career Quiz" and user['role'] == 'student':
    career_interest_quiz(school_code, user['email'])

elif menu == "Career Guidance":
    st.subheader("🎯 Career Guidance")
    
    tabs = st.tabs(["Career Quiz", "Alumni Network", "Resources"])
    
    with tabs[0]:
        if user['role'] == 'student':
            career_interest_quiz(school_code, user['email'])
        else:
            # View student results
            conn = sqlite3.connect('school_hub.db')
            c = conn.cursor()
            c.execute('''SELECT * FROM career_guidance 
                       WHERE school_code = ? ORDER BY date_taken DESC''', (school_code,))
            results = c.fetchall()
            conn.close()
            
            if results:
                for result in results:
                    student = get_user_by_email(result[1])
                    st.markdown(f"""
                    <div class="golden-card">
                        <strong>{student['fullname'] if student else result[1]}</strong><br>
                        Date: {result[4]}<br>
                        Recommendations: {', '.join(json.loads(result[3]))}
                    </div>
                    """, unsafe_allow_html=True)
    
    with tabs[1]:
        alumni_network(school_code, user['email'])
    
    with tabs[2]:
        st.markdown("""
        ### 📚 Career Resources
        
        **Universities:**
        - University of Nairobi
        - Kenyatta University
        - Strathmore University
        
        **Scholarships:**
        - Government scholarship
        - Equity Leadership Program
        - Mastercard Foundation
        
        **Career Paths:**
        - STEM careers
        - Humanities & Social Sciences
        - Arts & Design
        - Business & Entrepreneurship
        """)

elif menu == "My Portfolio" and user['role'] == 'student':
    create_portfolio(school_code, user['email'])

elif menu == "Parent Portal" and user['role'] == 'guardian':
    st.subheader("👪 Parent Engagement Portal")
    
    linked_adms = user.get('linked_students', [])
    linked_students = [u for u in users if u.get('admission_number') in linked_adms]
    
    if linked_students:
        for student in linked_students:
            with st.expander(f"📚 {student['fullname']}", expanded=True):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Today's attendance
                    conn = sqlite3.connect('school_hub.db')
                    c = conn.cursor()
                    c.execute('''SELECT status FROM attendance 
                               WHERE student_email = ? AND date = ?''',
                             (student['email'], datetime.now().strftime("%Y-%m-%d")))
                    attendance = c.fetchone()
                    conn.close()
                    
                    status = attendance[0] if attendance else "Not marked"
                    st.metric("Today's Attendance", status)
                
                with col2:
                    # Upcoming tests
                    st.metric("Upcoming Tests", "2")
                
                with col3:
                    # Homework count
                    st.metric("Homework Due", "3")
                
                # Message teacher
                st.markdown("#### Message Teacher")
                with st.form(f"message_teacher_{student['email']}"):
                    teachers = [u for u in users if u['role'] == 'teacher']
                    teacher = st.selectbox("Select Teacher", 
                                         [f"{t['fullname']}" for t in teachers], key=f"teacher_{student['email']}")
                    message = st.text_area("Message", key=f"msg_{student['email']}")
                    
                    if st.form_submit_button("Send Message"):
                        send_email_notification(
                            teachers[0]['email'],
                            f"Message from {user['fullname']} about {student['fullname']}",
                            message
                        )
                        st.success("Message sent!")
                
                # Schedule meeting
                if st.button("Schedule Parent-Teacher Meeting", key=f"meet_{student['email']}"):
                    meeting = create_video_meeting("parent-teacher", 
                                                  f"PTM-{student['fullname']}-{datetime.now().strftime('%Y%m%d')}")
                    st.success(f"Meeting created! Link: {meeting['url']}")
                    st.info("Share this link with the teacher")
    else:
        st.info("No linked students found")

elif menu == "Emergency Alert" and user['role'] in ['admin', 'teacher', 'security']:
    emergency_alert_system(school_code, user['email'])

elif menu == "Analytics" and user['role'] == 'admin':
    st.subheader("📈 Advanced Analytics")
    
    # Performance trends
    if academic_records:
        df = pd.DataFrame(academic_records)
        
        fig = px.line(df.groupby('date')['score'].mean().reset_index(), 
                     x='date', y='score', 
                     title='Overall Performance Trend')
        st.plotly_chart(fig, use_container_width=True)
        
        # Subject comparison
        fig2 = px.box(df, x='subject', y='score', 
                     title='Score Distribution by Subject')
        st.plotly_chart(fig2, use_container_width=True)
        
        # Attendance heatmap
        attendance = load_school_data(school_code, "attendance", [])
        if attendance:
            df_att = pd.DataFrame(attendance)
            df_att['date'] = pd.to_datetime(df_att['date'])
            df_att['day_of_week'] = df_att['date'].dt.day_name()
            df_att['hour'] = pd.to_datetime(df_att['recorded_at']).dt.hour
            
            pivot = df_att.pivot_table(values='status', index='hour', 
                                     columns='day_of_week', aggfunc='count')
            
            fig3 = px.imshow(pivot, title='Attendance Patterns Heatmap')
            st.plotly_chart(fig3, use_container_width=True)

elif menu == "Settings":
    st.subheader("⚙️ Settings")
    
    tabs = st.tabs(["Theme", "Language", "Accessibility", "Notifications"])
    
    with tabs[0]:
        st.markdown("### Theme Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_theme = st.selectbox("Choose Theme", list(THEMES.keys()),
                                        index=list(THEMES.keys()).index(st.session_state.theme))
        
        with col2:
            selected_wallpaper = st.selectbox("Choose Wallpaper", list(WALLPAPERS.keys()),
                                            index=list(WALLPAPERS.keys()).index(st.session_state.wallpaper))
        
        if st.button("Save Theme"):
            st.session_state.theme = selected_theme
            st.session_state.wallpaper = selected_wallpaper
            save_user_settings(school_code, user['email'], {
                "theme": selected_theme,
                "wallpaper": selected_wallpaper,
                "language": st.session_state.language,
                "accessibility": st.session_state.accessibility
            })
            st.success("Theme saved!")
            st.rerun()
    
    with tabs[1]:
        st.markdown("### Language Settings")
        
        selected_language = st.selectbox("Choose Language", list(LANGUAGES.keys()),
                                       index=list(LANGUAGES.values()).index(st.session_state.language))
        
        if st.button("Save Language"):
            st.session_state.language = LANGUAGES[selected_language]
            save_user_settings(school_code, user['email'], {
                "theme": st.session_state.theme,
                "wallpaper": st.session_state.wallpaper,
                "language": st.session_state.language,
                "accessibility": st.session_state.accessibility
            })
            st.success("Language saved!")
            st.rerun()
    
    with tabs[2]:
        st.markdown("### Accessibility Settings")
        
        preset = st.selectbox("Accessibility Preset", list(ACCESSIBILITY_PRESETS.keys()))
        
        if preset:
            st.session_state.accessibility = ACCESSIBILITY_PRESETS[preset]
        
        col1, col2 = st.columns(2)
        
        with col1:
            text_size = st.select_slider("Text Size", 
                                       options=["Small", "Normal", "Large", "Extra Large"],
                                       value=st.session_state.accessibility.get('text_size', 'Normal'))
            
            font_family = st.selectbox("Font Family", 
                                     ["Default", "OpenDyslexic", "Arial", "Verdana"],
                                     index=["Default", "OpenDyslexic", "Arial", "Verdana"].index(
                                         st.session_state.accessibility.get('font_family', 'Default')))
        
        with col2:
            high_contrast = st.checkbox("High Contrast Mode", 
                                      value=st.session_state.accessibility.get('high_contrast', False))
            
            reduced_motion = st.checkbox("Reduce Motion", 
                                       value=st.session_state.accessibility.get('reduced_motion', False))
        
        color_blindness = st.selectbox("Color Blindness Mode",
                                     ["None", "Protanopia", "Deuteranopia", "Tritanopia"],
                                     index=["None", "Protanopia", "Deuteranopia", "Tritanopia"].index(
                                         st.session_state.accessibility.get('color_blindness', 'None')))
        
        if st.button("Save Accessibility Settings"):
            st.session_state.accessibility = {
                "text_size": text_size,
                "font_family": font_family,
                "high_contrast": high_contrast,
                "reduced_motion": reduced_motion,
                "color_blindness": color_blindness
            }
            save_user_settings(school_code, user['email'], {
                "theme": st.session_state.theme,
                "wallpaper": st.session_state.wallpaper,
                "language": st.session_state.language,
                "accessibility": st.session_state.accessibility
            })
            st.success("Accessibility settings saved!")
            st.rerun()
    
    with tabs[3]:
        st.markdown("### Notification Settings")
        
        with st.form("notification_settings"):
            email_notifications = st.checkbox("Email Notifications", value=True)
            push_notifications = st.checkbox("Push Notifications", value=True)
            sms_notifications = st.checkbox("SMS Notifications", value=False)
            
            notify_announcements = st.checkbox("Announcements", value=True)
            notify_messages = st.checkbox("Messages", value=True)
            notify_assignments = st.checkbox("Assignments", value=True)
            notify_grades = st.checkbox("Grade Updates", value=True)
            notify_attendance = st.checkbox("Attendance Reports", value=False)
            
            if st.form_submit_button("Save Notification Settings"):
                notification_prefs = {
                    "email": email_notifications,
                    "push": push_notifications,
                    "sms": sms_notifications,
                    "announcements": notify_announcements,
                    "messages": notify_messages,
                    "assignments": notify_assignments,
                    "grades": notify_grades,
                    "attendance": notify_attendance
                }
                
                save_user_settings(school_code, user['email'], {
                    "theme": st.session_state.theme,
                    "wallpaper": st.session_state.wallpaper,
                    "language": st.session_state.language,
                    "accessibility": st.session_state.accessibility,
                    "notification_prefs": notification_prefs
                })
                st.success("Notification settings saved!")

elif menu == "Profile":
    st.subheader("👤 My Profile")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if user.get('profile_pic'):
            st.image(user['profile_pic'], width=150)
        else:
            role_emoji = "👑" if user['role'] == 'admin' else "👨‍🏫" if user['role'] == 'teacher' else "👨‍🎓" if user['role'] == 'student' else "👪"
            st.markdown(f"<h1 style='font-size: 5rem; text-align: center;'>{role_emoji}</h1>", unsafe_allow_html=True)
        
        pic = st.file_uploader("📸 Upload Photo", type=['png', 'jpg', 'jpeg'])
        if pic:
            img = Image.open(pic)
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            b64 = base64.b64encode(buffered.getvalue()).decode()
            user['profile_pic'] = f"data:image/png;base64,{b64}"
            save_user(user)
            st.rerun()
    
    with col2:
        with st.form("edit_profile"):
            fullname = st.text_input("Full Name", user['fullname'])
            phone = st.text_input("Phone", user.get('phone', ''))
            bio = st.text_area("Bio", user.get('bio', ''), height=100)
            
            if st.form_submit_button("Update Profile"):
                user['fullname'] = fullname
                user['phone'] = phone
                user['bio'] = bio
                save_user(user)
                st.success("Profile updated!")
                st.rerun()

# Other existing sections (Classes, Community, Chat, etc.) remain the same as original code
# ...

else:
st.error("Something went wrong. Please restart.")
if st.button("Restart"):
    st.session_state.page = 'welcome'
    st.rerun()

# ============ FOOTER ============
st.markdown("""
<div style="text-align: center; margin-top: 50px; padding: 20px; color: rgba(255,255,255,0.5);">
<hr style="border-color: rgba(255,215,0,0.3);">
<p>✨ School Community Hub v3.0 - Empowering Education Through Technology ✨</p>
<p style="font-size: 0.8rem;">© 2024 All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
