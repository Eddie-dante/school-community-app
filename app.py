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
import sqlite3
import bcrypt
import logging
import os
import shutil
from contextlib import contextmanager
from functools import wraps
from typing import Optional, Dict, List, Any
import mimetypes

# ============ CONFIGURATION ============
class Config:
    """Application configuration"""
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    ALLOWED_IMAGE_TYPES = ['jpg', 'jpeg', 'png', 'gif']
    ALLOWED_DOCUMENT_TYPES = ['pdf', 'docx', 'txt', 'xlsx', 'pptx']
    ALLOWED_EXTENSIONS = ALLOWED_IMAGE_TYPES + ALLOWED_DOCUMENT_TYPES
    MAX_BACKUPS = 10
    CACHE_TTL = 300  # 5 minutes
    CHAT_REFRESH_RATE = 5  # seconds
    
    @classmethod
    def get_allowed_extensions(cls, file_type: str = 'all') -> List[str]:
        if file_type == 'image':
            return cls.ALLOWED_IMAGE_TYPES
        elif file_type == 'document':
            return cls.ALLOWED_DOCUMENT_TYPES
        return cls.ALLOWED_EXTENSIONS

# ============ LOGGING SETUP ============
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('school_hub.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============ ERROR HANDLING DECORATOR ============
def handle_errors(func):
    """Decorator for error handling"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            st.error(f"An error occurred: {str(e)}")
            return None
    return wrapper

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="✨ School Community Hub ✨",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ DATABASE MANAGER ============
class DatabaseManager:
    """Manages database operations for the application"""
    
    def __init__(self, school_code: str = None):
        self.school_code = school_code
        self.db_path = Path("school_data")
        self.db_path.mkdir(exist_ok=True)
        
    @contextmanager
    def get_connection(self, school_code: str = None):
        """Get database connection with context management"""
        code = school_code or self.school_code
        if not code:
            raise ValueError("School code is required")
            
        db_file = self.db_path / f"{code}.db"
        conn = sqlite3.connect(str(db_file))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()
    
    @handle_errors
    def init_database(self, school_code: str):
        """Initialize database tables for a school"""
        with self.get_connection(school_code) as conn:
            cursor = conn.cursor()
            
            # Create tables
            cursor.executescript('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    email TEXT UNIQUE,
                    fullname TEXT NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL,
                    joined TEXT NOT NULL,
                    profile_pic TEXT,
                    bio TEXT,
                    phone TEXT,
                    admission_number TEXT UNIQUE,
                    school_code TEXT NOT NULL
                );
                
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    sender TEXT NOT NULL,
                    recipient TEXT NOT NULL,
                    message TEXT,
                    attachment TEXT,
                    timestamp TEXT NOT NULL,
                    read INTEGER DEFAULT 0,
                    deleted INTEGER DEFAULT 0,
                    conversation_id TEXT NOT NULL,
                    FOREIGN KEY (sender) REFERENCES users(email),
                    FOREIGN KEY (recipient) REFERENCES users(email)
                );
                
                CREATE TABLE IF NOT EXISTS friendships (
                    user1 TEXT NOT NULL,
                    user2 TEXT NOT NULL,
                    since TEXT NOT NULL,
                    status TEXT DEFAULT 'active',
                    PRIMARY KEY (user1, user2),
                    FOREIGN KEY (user1) REFERENCES users(email),
                    FOREIGN KEY (user2) REFERENCES users(email)
                );
                
                CREATE TABLE IF NOT EXISTS friend_requests (
                    id TEXT PRIMARY KEY,
                    from_email TEXT NOT NULL,
                    to_email TEXT NOT NULL,
                    status TEXT NOT NULL,
                    date TEXT NOT NULL,
                    FOREIGN KEY (from_email) REFERENCES users(email),
                    FOREIGN KEY (to_email) REFERENCES users(email)
                );
                
                CREATE TABLE IF NOT EXISTS classes (
                    id TEXT PRIMARY KEY,
                    code TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    subject TEXT,
                    grade TEXT,
                    teacher TEXT,
                    teacher_name TEXT,
                    room TEXT,
                    schedule TEXT,
                    max_students INTEGER DEFAULT 40,
                    created TEXT NOT NULL,
                    status TEXT DEFAULT 'active',
                    FOREIGN KEY (teacher) REFERENCES users(email)
                );
                
                CREATE TABLE IF NOT EXISTS class_enrollments (
                    class_code TEXT,
                    student_email TEXT,
                    enrolled_date TEXT NOT NULL,
                    status TEXT DEFAULT 'active',
                    PRIMARY KEY (class_code, student_email),
                    FOREIGN KEY (class_code) REFERENCES classes(code),
                    FOREIGN KEY (student_email) REFERENCES users(email)
                );
                
                CREATE TABLE IF NOT EXISTS groups (
                    id TEXT PRIMARY KEY,
                    code TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT,
                    type TEXT,
                    leader TEXT NOT NULL,
                    leader_name TEXT NOT NULL,
                    created TEXT NOT NULL,
                    max_members INTEGER DEFAULT 20,
                    status TEXT DEFAULT 'active',
                    FOREIGN KEY (leader) REFERENCES users(email)
                );
                
                CREATE TABLE IF NOT EXISTS group_members (
                    group_code TEXT,
                    member_email TEXT,
                    role TEXT DEFAULT 'member',
                    joined_date TEXT NOT NULL,
                    PRIMARY KEY (group_code, member_email),
                    FOREIGN KEY (group_code) REFERENCES groups(code),
                    FOREIGN KEY (member_email) REFERENCES users(email)
                );
                
                CREATE TABLE IF NOT EXISTS announcements (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    author TEXT NOT NULL,
                    author_email TEXT NOT NULL,
                    author_role TEXT NOT NULL,
                    date TEXT NOT NULL,
                    target TEXT NOT NULL,
                    important INTEGER DEFAULT 0,
                    attachment TEXT,
                    FOREIGN KEY (author_email) REFERENCES users(email)
                );
                
                CREATE TABLE IF NOT EXISTS assignments (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    subject TEXT,
                    target_class TEXT,
                    due_date TEXT NOT NULL,
                    total_points INTEGER DEFAULT 100,
                    created_by TEXT NOT NULL,
                    created_date TEXT NOT NULL,
                    attachment TEXT,
                    FOREIGN KEY (created_by) REFERENCES users(email)
                );
                
                CREATE TABLE IF NOT EXISTS assignment_submissions (
                    assignment_id TEXT,
                    student_email TEXT,
                    submission_date TEXT NOT NULL,
                    attachment TEXT,
                    grade INTEGER,
                    feedback TEXT,
                    PRIMARY KEY (assignment_id, student_email),
                    FOREIGN KEY (assignment_id) REFERENCES assignments(id),
                    FOREIGN KEY (student_email) REFERENCES users(email)
                );
                
                CREATE TABLE IF NOT EXISTS teacher_codes (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    code TEXT UNIQUE NOT NULL,
                    department TEXT,
                    created TEXT NOT NULL,
                    status TEXT DEFAULT 'active',
                    last_used TEXT,
                    last_used_by TEXT
                );
                
                CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id);
                CREATE INDEX IF NOT EXISTS idx_messages_recipient ON messages(recipient, read);
                CREATE INDEX IF NOT EXISTS idx_friendships_user ON friendships(user1, user2);
                CREATE INDEX IF NOT EXISTS idx_enrollments_student ON class_enrollments(student_email);
                CREATE INDEX IF NOT EXISTS idx_group_members_member ON group_members(member_email);
            ''')
            
            logger.info(f"Database initialized for school: {school_code}")
    
    @handle_errors
    def backup_database(self, school_code: str) -> str:
        """Create backup of school database"""
        backup_dir = Path("backups") / school_code / datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Backup database file
        db_file = self.db_path / f"{school_code}.db"
        if db_file.exists():
            shutil.copy2(db_file, backup_dir / f"{school_code}.db")
        
        # Keep only last MAX_BACKUPS
        backups = sorted(Path("backups").glob(f"{school_code}/*"))
        if len(backups) > Config.MAX_BACKUPS:
            for old_backup in backups[:-Config.MAX_BACKUPS]:
                shutil.rmtree(old_backup)
        
        logger.info(f"Database backed up for school: {school_code}")
        return str(backup_dir)

# Initialize database manager
db_manager = DatabaseManager()

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
    "Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5", "Grade 6",
    "Grade 7", "Grade 8", "Grade 9", "Form 1", "Form 2", "Form 3", "Form 4"
]

def get_subjects_for_grade(grade: str) -> List[str]:
    """Get subjects based on grade level"""
    if "Grade" in grade:
        grade_num = int(grade.replace("Grade ", ""))
        if grade_num <= 6:
            return PRIMARY_SUBJECTS
        else:
            return JUNIOR_SECONDARY_SUBJECTS
    elif "Form" in grade:
        subjects = []
        for category, subj_list in SENIOR_SECONDARY_SUBJECTS.items():
            subjects.extend(subj_list)
        return subjects
    return PRIMARY_SUBJECTS

# ============ SECURITY FUNCTIONS ============
@handle_errors
def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

@handle_errors
def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# ============ FILE VALIDATION ============
@handle_errors
def validate_file_upload(uploaded_file) -> bool:
    """Validate uploaded file size and type"""
    if uploaded_file is None:
        return False
    
    # Check file size
    if uploaded_file.size > Config.MAX_FILE_SIZE:
        st.error(f"File too large. Maximum size is {Config.MAX_FILE_SIZE // (1024*1024)}MB")
        return False
    
    # Check file type
    file_ext = uploaded_file.name.split('.')[-1].lower()
    if file_ext not in Config.ALLOWED_EXTENSIONS:
        st.error(f"File type not allowed. Allowed types: {', '.join(Config.ALLOWED_EXTENSIONS)}")
        return False
    
    return True

# ============ ATTACHMENT FUNCTIONS ============
@handle_errors
def save_attachment(uploaded_file) -> Optional[Dict]:
    """Save uploaded file as base64 attachment"""
    if not uploaded_file or not validate_file_upload(uploaded_file):
        return None
    
    bytes_data = uploaded_file.getvalue()
    b64 = base64.b64encode(bytes_data).decode('utf-8')
    
    return {
        "name": uploaded_file.name,
        "type": uploaded_file.type or mimetypes.guess_type(uploaded_file.name)[0],
        "data": b64,
        "size": len(bytes_data),
        "extension": uploaded_file.name.split('.')[-1].lower()
    }

@handle_errors
def display_attachment(attachment: Dict):
    """Display attachment in the UI"""
    if not attachment:
        return
    
    file_ext = attachment.get('extension', '')
    
    if file_ext in Config.ALLOWED_IMAGE_TYPES:
        # Display image
        st.image(f"data:{attachment['type']};base64,{attachment['data']}", 
                 caption=attachment['name'], use_column_width=True)
    else:
        # Display download link for documents
        st.markdown(
            f"📎 [{attachment['name']}](data:{attachment['type']};base64,{attachment['data']} "
            f"download=\"{attachment['name']}\")"
        )

# ============ CODE GENERATORS ============
def generate_id(prefix: str, length: int = 8) -> str:
    """Generate unique ID with prefix"""
    chars = string.ascii_uppercase + string.digits
    random_part = ''.join(random.choices(chars, k=length))
    timestamp = datetime.now().strftime("%y%m")
    return f"{prefix}{timestamp}{random_part}"

def generate_school_code() -> str:
    """Generate unique school code"""
    chars = string.ascii_uppercase + string.digits
    return 'SCH' + ''.join(random.choices(chars, k=6))

def generate_class_code() -> str:
    """Generate unique class code"""
    return 'CLS' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def generate_group_code() -> str:
    """Generate unique group code"""
    return 'GRP' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def generate_admission_number() -> str:
    """Generate student admission number"""
    year = datetime.now().strftime("%y")
    random_num = ''.join(random.choices(string.digits, k=4))
    return f"ADM/{year}/{random_num}"

# ============ SCHOOL MANAGEMENT ============
class SchoolManager:
    """Manages school operations"""
    
    def __init__(self):
        self.schools_file = Path("school_data") / "schools.json"
        self.schools_file.parent.mkdir(exist_ok=True)
    
    @handle_errors
    def load_all_schools(self) -> Dict:
        """Load all schools from JSON"""
        if self.schools_file.exists():
            with open(self.schools_file, 'r') as f:
                return json.load(f)
        return {}
    
    @handle_errors
    def save_all_schools(self, schools: Dict):
        """Save all schools to JSON"""
        with open(self.schools_file, 'w') as f:
            json.dump(schools, f, indent=2)
    
    @handle_errors
    def create_school(self, school_data: Dict) -> Dict:
        """Create new school"""
        schools = self.load_all_schools()
        
        # Generate unique code
        code = generate_school_code()
        while code in schools:
            code = generate_school_code()
        
        school = {
            "code": code,
            "name": school_data['name'],
            "city": school_data.get('city', ''),
            "state": school_data.get('state', ''),
            "motto": school_data.get('motto', ''),
            "created": datetime.now().strftime("%Y-%m-%d"),
            "admin_email": school_data['admin_email'],
            "admin_name": school_data['admin_name'],
            "stats": {
                "students": 0,
                "teachers": 0,
                "guardians": 0,
                "classes": 0,
                "groups": 0,
                "announcements": 0
            }
        }
        
        schools[code] = school
        self.save_all_schools(schools)
        
        # Initialize database for the school
        db_manager.init_database(code)
        
        logger.info(f"School created: {code} - {school_data['name']}")
        return school

# Initialize school manager
school_manager = SchoolManager()

# ============ USER MANAGEMENT ============
class UserManager:
    """Manages user operations"""
    
    def __init__(self, school_code: str):
        self.school_code = school_code
    
    @handle_errors
    def create_user(self, user_data: Dict) -> Dict:
        """Create new user"""
        with db_manager.get_connection(self.school_code) as conn:
            cursor = conn.cursor()
            
            # Check if email exists
            cursor.execute("SELECT email FROM users WHERE email = ?", (user_data['email'],))
            if cursor.fetchone():
                raise ValueError("Email already registered")
            
            # Generate user ID
            user_id = generate_id("USR")
            
            # Insert user
            cursor.execute('''
                INSERT INTO users (
                    user_id, email, fullname, password, role, joined, 
                    profile_pic, bio, phone, admission_number, school_code
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                user_data['email'],
                user_data['fullname'],
                hash_password(user_data['password']),
                user_data['role'],
                datetime.now().strftime("%Y-%m-%d"),
                user_data.get('profile_pic'),
                user_data.get('bio', ''),
                user_data.get('phone', ''),
                user_data.get('admission_number'),
                self.school_code
            ))
            
            logger.info(f"User created: {user_data['email']} - {user_data['role']}")
            
            return {
                'user_id': user_id,
                'email': user_data['email'],
                'fullname': user_data['fullname'],
                'role': user_data['role']
            }
    
    @handle_errors
    def authenticate_user(self, email: str, password: str, role: str = None) -> Optional[Dict]:
        """Authenticate user"""
        with db_manager.get_connection(self.school_code) as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM users WHERE email = ?"
            params = [email]
            
            if role:
                query += " AND role = ?"
                params.append(role)
            
            cursor.execute(query, params)
            user = cursor.fetchone()
            
            if user and verify_password(password, user['password']):
                return dict(user)
            
            return None
    
    @handle_errors
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        with db_manager.get_connection(self.school_code) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            return dict(user) if user else None
    
    @handle_errors
    def get_all_users(self, role: str = None) -> List[Dict]:
        """Get all users, optionally filtered by role"""
        with db_manager.get_connection(self.school_code) as conn:
            cursor = conn.cursor()
            
            if role:
                cursor.execute("SELECT * FROM users WHERE role = ? ORDER BY fullname", (role,))
            else:
                cursor.execute("SELECT * FROM users ORDER BY fullname")
            
            return [dict(row) for row in cursor.fetchall()]
    
    @handle_errors
    def update_user_profile(self, email: str, updates: Dict) -> bool:
        """Update user profile"""
        with db_manager.get_connection(self.school_code) as conn:
            cursor = conn.cursor()
            
            allowed_fields = ['fullname', 'phone', 'bio', 'profile_pic']
            update_fields = []
            values = []
            
            for field in allowed_fields:
                if field in updates:
                    update_fields.append(f"{field} = ?")
                    values.append(updates[field])
            
            if not update_fields:
                return False
            
            values.append(email)
            query = f"UPDATE users SET {', '.join(update_fields)} WHERE email = ?"
            
            cursor.execute(query, values)
            return cursor.rowcount > 0

# ============ FRIENDSHIP MANAGEMENT ============
class FriendshipManager:
    """Manages friendships and friend requests"""
    
    def __init__(self, school_code: str):
        self.school_code = school_code
    
    @handle_errors
    def send_request(self, from_email: str, to_email: str) -> bool:
        """Send friend request"""
        if from_email == to_email:
            return False
        
        with db_manager.get_connection(self.school_code) as conn:
            cursor = conn.cursor()
            
            # Check if already friends
            cursor.execute('''
                SELECT * FROM friendships 
                WHERE (user1 = ? AND user2 = ?) OR (user1 = ? AND user2 = ?)
            ''', (from_email, to_email, to_email, from_email))
            
            if cursor.fetchone():
                return False
            
            # Check if request already exists
            cursor.execute('''
                SELECT * FROM friend_requests 
                WHERE from_email = ? AND to_email = ? AND status = 'pending'
            ''', (from_email, to_email))
            
            if cursor.fetchone():
                return False
            
            # Create request
            request_id = generate_id("FRQ")
            cursor.execute('''
                INSERT INTO friend_requests (id, from_email, to_email, status, date)
                VALUES (?, ?, ?, 'pending', ?)
            ''', (request_id, from_email, to_email, datetime.now().strftime("%Y-%m-%d %H:%M")))
            
            return True
    
    @handle_errors
    def accept_request(self, request_id: str) -> bool:
        """Accept friend request"""
        with db_manager.get_connection(self.school_code) as conn:
            cursor = conn.cursor()
            
            # Get request details
            cursor.execute("SELECT * FROM friend_requests WHERE id = ?", (request_id,))
            request = cursor.fetchone()
            
            if not request:
                return False
            
            # Update request status
            cursor.execute('''
                UPDATE friend_requests SET status = 'accepted' WHERE id = ?
            ''', (request_id,))
            
            # Create friendship
            cursor.execute('''
                INSERT INTO friendships (user1, user2, since, status)
                VALUES (?, ?, ?, 'active')
            ''', (request['from_email'], request['to_email'], 
                  datetime.now().strftime("%Y-%m-%d %H:%M")))
            
            return True
    
    @handle_errors
    def decline_request(self, request_id: str) -> bool:
        """Decline friend request"""
        with db_manager.get_connection(self.school_code) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE friend_requests SET status = 'declined' WHERE id = ?
            ''', (request_id,))
            return cursor.rowcount > 0
    
    @handle_errors
    def get_friends(self, email: str) -> List[str]:
        """Get list of friend emails for a user"""
        with db_manager.get_connection(self.school_code) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT user1, user2 FROM friendships 
                WHERE (user1 = ? OR user2 = ?) AND status = 'active'
            ''', (email, email))
            
            friends = []
            for row in cursor.fetchall():
                if row['user1'] == email:
                    friends.append(row['user2'])
                else:
                    friends.append(row['user1'])
            
            return friends
    
    @handle_errors
    def get_pending_requests(self, email: str) -> List[Dict]:
        """Get pending friend requests for a user"""
        with db_manager.get_connection(self.school_code) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM friend_requests 
                WHERE to_email = ? AND status = 'pending'
                ORDER BY date DESC
            ''', (email,))
            return [dict(row) for row in cursor.fetchall()]
    
    @handle_errors
    def get_sent_requests(self, email: str) -> List[Dict]:
        """Get sent friend requests from a user"""
        with db_manager.get_connection(self.school_code) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM friend_requests 
                WHERE from_email = ? AND status = 'pending'
                ORDER BY date DESC
            ''', (email,))
            return [dict(row) for row in cursor.fetchall()]

# ============ MESSAGE MANAGEMENT ============
class MessageManager:
    """Manages messages and conversations"""
    
    def __init__(self, school_code: str):
        self.school_code = school_code
    
    @handle_errors
    def send_message(self, sender: str, recipient: str, message: str, 
                    attachment: Dict = None) -> bool:
        """Send a message"""
        if not message and not attachment:
            return False
        
        with db_manager.get_connection(self.school_code) as conn:
            cursor = conn.cursor()
            
            message_id = generate_id("MSG")
            conversation_id = f"{min(sender, recipient)}_{max(sender, recipient)}"
            
            cursor.execute('''
                INSERT INTO messages (
                    id, sender, recipient, message, attachment, 
                    timestamp, read, deleted, conversation_id
                ) VALUES (?, ?, ?, ?, ?, ?, 0, 0, ?)
            ''', (
                message_id,
                sender,
                recipient,
                message,
                json.dumps(attachment) if attachment else None,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                conversation_id
            ))
            
            return True
    
    @handle_errors
    def get_conversations(self, email: str) -> Dict[str, List[Dict]]:
        """Get all conversations for a user"""
        with db_manager.get_connection(self.school_code) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM messages 
                WHERE (sender = ? OR recipient = ?) AND deleted = 0
                ORDER BY timestamp
            ''', (email, email))
            
            messages = [dict(row) for row in cursor.fetchall()]
            
            # Parse attachment JSON
            for msg in messages:
                if msg['attachment']:
                    msg['attachment'] = json.loads(msg['attachment'])
            
            # Group by conversation
            conversations = {}
            for msg in messages:
                other = msg['recipient'] if msg['sender'] == email else msg['sender']
                if other not in conversations:
                    conversations[other] = []
                conversations[other].append(msg)
            
            return conversations
    
    @handle_errors
    def get_unread_count(self, email: str) -> int:
        """Get number of unread messages for a user"""
        with db_manager.get_connection(self.school_code) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COUNT(*) as count FROM messages 
                WHERE recipient = ? AND read = 0 AND deleted = 0
            ''', (email,))
            result = cursor.fetchone()
            return result['count'] if result else 0
    
    @handle_errors
    def mark_as_read(self, message_id: str) -> bool:
        """Mark a message as read"""
        with db_manager.get_connection(self.school_code) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE messages SET read = 1 WHERE id = ?
            ''', (message_id,))
            return cursor.rowcount > 0
    
    @handle_errors
    def delete_message(self, message_id: str) -> bool:
        """Soft delete a message"""
        with db_manager.get_connection(self.school_code) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE messages SET deleted = 1 WHERE id = ?
            ''', (message_id,))
            return cursor.rowcount > 0

# ============ CACHING ============
class CacheManager:
    """Simple cache manager"""
    
    def __init__(self, ttl: int = Config.CACHE_TTL):
        self.cache = {}
        self.ttl = ttl
    
    def get(self, key: str):
        """Get value from cache"""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, value):
        """Set value in cache"""
        self.cache[key] = (value, time.time())
    
    def clear(self):
        """Clear cache"""
        self.cache.clear()

# Initialize cache
cache = CacheManager()

# ============ RESPONSIVE DESIGN META TAG ============
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
<style>
    @media (max-width: 768px) {
        .main .block-container { padding: 0.8rem !important; }
        h1 { font-size: 1.8rem !important; }
        h2 { font-size: 1.3rem !important; }
        .stButton button { 
            font-size: 0.9rem !important; 
            padding: 0.4rem 0.8rem !important;
            min-height: 44px !important;
        }
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
    
    /* Chat styles */
    .chat-container {
        background: rgba(0, 0, 0, 0.4);
        border-radius: 16px;
        padding: 20px;
        height: 500px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 15px;
    }
    
    @media (max-width: 768px) {
        .chat-container {
            height: 70vh;
            padding: 10px;
        }
    }
    
    .chat-message-wrapper {
        display: flex;
        margin-bottom: 10px;
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .chat-message-sent {
        justify-content: flex-end;
    }
    
    .chat-message-received {
        justify-content: flex-start;
    }
    
    .chat-bubble {
        max-width: 70%;
        padding: 12px 16px;
        border-radius: 20px;
        position: relative;
        word-wrap: break-word;
    }
    
    @media (max-width: 768px) {
        .chat-bubble {
            max-width: 85%;
            padding: 10px 12px;
            font-size: 0.9rem;
        }
    }
    
    .chat-bubble-sent {
        background: linear-gradient(135deg, #0095f6, #1877f2);
        color: white;
        border-bottom-right-radius: 4px;
    }
    
    .chat-bubble-received {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border-bottom-left-radius: 4px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .chat-time {
        font-size: 0.65rem;
        color: rgba(255,255,255,0.5);
        margin-top: 4px;
        text-align: right;
    }
    
    /* Profile card */
    .profile-card {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    /* Member card */
    .member-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 15px;
        transition: all 0.2s ease;
        border: 1px solid transparent;
    }
    
    .member-card:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: rgba(255, 215, 0, 0.3);
    }
    
    .member-pic {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid gold;
    }
    
    .member-role {
        color: gold;
        font-size: 0.8rem;
        display: inline-block;
        padding: 2px 8px;
        border-radius: 12px;
        background: rgba(255, 215, 0, 0.1);
        margin-top: 4px;
    }
    
    /* Announcement card */
    .announcement-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 4px solid gold;
    }
    
    .announcement-title {
        color: gold;
        font-weight: 600;
        font-size: 1.2rem;
    }
    
    /* Request badge */
    .request-badge {
        background: gold;
        color: black;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        margin-left: 8px;
    }
    
    /* Loading spinner */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,215,0,0.3);
        border-radius: 50%;
        border-top-color: gold;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# ============ SESSION STATE INITIALIZATION ============
def init_session_state():
    """Initialize session state variables"""
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
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = time.time()
    if 'loading' not in st.session_state:
        st.session_state.loading = False

init_session_state()

# ============ AUTO-REFRESH FUNCTION ============
def should_refresh() -> bool:
    """Check if page should auto-refresh"""
    current_time = time.time()
    if current_time - st.session_state.last_refresh > Config.CHAT_REFRESH_RATE:
        st.session_state.last_refresh = current_time
        return True
    return False

# ============ MAIN APP ============

# ----- WELCOME PAGE -----
if st.session_state.page == 'welcome':
    st.markdown('<h1>✨ School Community Hub ✨</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: white;">Connect • Collaborate • Shine Together</p>', unsafe_allow_html=True)
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
                        schools = school_manager.load_all_schools()
                        if school_code in schools:
                            school = schools[school_code]
                            if school['admin_email'] == admin_email:
                                user_manager = UserManager(school_code)
                                user = user_manager.authenticate_user(admin_email, admin_password, 'admin')
                                
                                if user:
                                    st.session_state.current_school = school
                                    st.session_state.user = user
                                    st.session_state.page = 'dashboard'
                                    st.rerun()
                                else:
                                    st.error("Invalid password")
                            else:
                                st.error("Invalid admin email")
                        else:
                            st.error("School not found")
        
        with col2:
            st.markdown("""
            <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,215,0,0.3); 
                        border-radius: 20px; padding: 2rem; text-align: center;">
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
                        # Create school
                        school = school_manager.create_school({
                            "name": school_name,
                            "city": city,
                            "state": state,
                            "motto": motto,
                            "admin_email": admin_email,
                            "admin_name": admin_name
                        })
                        
                        # Create admin user
                        user_manager = UserManager(school['code'])
                        user = user_manager.create_user({
                            "email": admin_email,
                            "fullname": admin_name,
                            "password": password,
                            "role": "admin"
                        })
                        
                        # Get full user data
                        user = user_manager.get_user_by_email(admin_email)
                        
                        st.session_state.current_school = school
                        st.session_state.user = user
                        st.session_state.page = 'dashboard'
                        
                        st.success(f"✨ School Created! Your Code: **{school['code']}**")
                        st.rerun()
        
        with col2:
            st.markdown("""
            <div style="background: rgba(255,255,255,0.05); border: 1px solid rgba(255,215,0,0.3); 
                        border-radius: 20px; padding: 2rem; text-align: center;">
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
                            schools = school_manager.load_all_schools()
                            if school_code in schools:
                                user_manager = UserManager(school_code)
                                user = user_manager.authenticate_user(email, password, 'teacher')
                                
                                if user:
                                    st.session_state.current_school = schools[school_code]
                                    st.session_state.user = user
                                    st.session_state.page = 'dashboard'
                                    st.rerun()
                                else:
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
                            schools = school_manager.load_all_schools()
                            if school_code not in schools:
                                st.error("School not found")
                                st.stop()
                            
                            # Verify teacher code
                            with db_manager.get_connection(school_code) as conn:
                                cursor = conn.cursor()
                                cursor.execute('''
                                    SELECT * FROM teacher_codes 
                                    WHERE code = ? AND status = 'active'
                                ''', (teacher_code.upper(),))
                                teacher_record = cursor.fetchone()
                                
                                if not teacher_record:
                                    st.error("Invalid teacher code")
                                    st.stop()
                                
                                # Update teacher code usage
                                cursor.execute('''
                                    UPDATE teacher_codes 
                                    SET last_used = ?, last_used_by = ? 
                                    WHERE code = ?
                                ''', (datetime.now().strftime("%Y-%m-%d %H:%M"), email, teacher_code.upper()))
                            
                            # Create teacher user
                            user_manager = UserManager(school_code)
                            try:
                                user = user_manager.create_user({
                                    "email": email,
                                    "fullname": fullname,
                                    "password": password,
                                    "role": "teacher",
                                    "phone": ""
                                })
                                
                                # Update school stats
                                schools[school_code]['stats']['teachers'] += 1
                                school_manager.save_all_schools(schools)
                                
                                st.session_state.current_school = schools[school_code]
                                st.session_state.user = user_manager.get_user_by_email(email)
                                st.session_state.page = 'dashboard'
                                
                                st.success("✅ Registration Successful!")
                                st.rerun()
                                
                            except ValueError as e:
                                st.error(str(e))
    
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
                            schools = school_manager.load_all_schools()
                            if school_code in schools:
                                with db_manager.get_connection(school_code) as conn:
                                    cursor = conn.cursor()
                                    cursor.execute('''
                                        SELECT * FROM users 
                                        WHERE admission_number = ? AND role = 'student'
                                    ''', (admission_number,))
                                    user = cursor.fetchone()
                                    
                                    if user and verify_password(password, user['password']):
                                        st.session_state.current_school = schools[school_code]
                                        st.session_state.user = dict(user)
                                        st.session_state.page = 'dashboard'
                                        st.rerun()
                                    else:
                                        st.error("Invalid credentials")
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
                            schools = school_manager.load_all_schools()
                            if school_code not in schools:
                                st.error("School not found")
                                st.stop()
                            
                            # Generate admission number
                            admission_number = generate_admission_number()
                            
                            # Create student user
                            user_manager = UserManager(school_code)
                            try:
                                user = user_manager.create_user({
                                    "email": email if email else f"{admission_number}@student.local",
                                    "fullname": fullname,
                                    "password": password,
                                    "role": "student",
                                    "admission_number": admission_number,
                                    "phone": ""
                                })
                                
                                # Update school stats
                                schools[school_code]['stats']['students'] += 1
                                school_manager.save_all_schools(schools)
                                
                                st.success(f"✅ Registered! Your Admission Number: **{admission_number}**")
                                st.info("📝 Save this number - you'll need it to login!")
                                
                            except ValueError as e:
                                st.error(str(e))
    
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
                            schools = school_manager.load_all_schools()
                            if school_code in schools:
                                user_manager = UserManager(school_code)
                                user = user_manager.authenticate_user(email, password, 'guardian')
                                
                                if user:
                                    # Check if linked to student
                                    with db_manager.get_connection(school_code) as conn:
                                        cursor = conn.cursor()
                                        cursor.execute('''
                                            SELECT * FROM users 
                                            WHERE admission_number = ? AND role = 'student'
                                        ''', (student_admission,))
                                        student = cursor.fetchone()
                                        
                                        if student:
                                            st.session_state.current_school = schools[school_code]
                                            st.session_state.user = user
                                            st.session_state.page = 'dashboard'
                                            st.rerun()
                                        else:
                                            st.error("Student not found")
                                else:
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
                            schools = school_manager.load_all_schools()
                            if school_code not in schools:
                                st.error("School not found")
                                st.stop()
                            
                            # Verify student exists
                            with db_manager.get_connection(school_code) as conn:
                                cursor = conn.cursor()
                                cursor.execute('''
                                    SELECT * FROM users 
                                    WHERE admission_number = ? AND role = 'student'
                                ''', (student_admission,))
                                student = cursor.fetchone()
                                
                                if not student:
                                    st.error("❌ Student not found with this admission number!")
                                    st.stop()
                            
                            # Create guardian user
                            user_manager = UserManager(school_code)
                            try:
                                user = user_manager.create_user({
                                    "email": email,
                                    "fullname": fullname,
                                    "password": password,
                                    "role": "guardian",
                                    "phone": phone,
                                    "bio": f"Guardian of student: {student_admission}"
                                })
                                
                                # Update school stats
                                schools[school_code]['stats']['guardians'] = schools[school_code]['stats'].get('guardians', 0) + 1
                                school_manager.save_all_schools(schools)
                                
                                st.success("✅ Guardian Registration Successful!")
                                
                            except ValueError as e:
                                st.error(str(e))

# ----- DASHBOARD -----
elif st.session_state.page == 'dashboard' and st.session_state.current_school and st.session_state.user:
    school = st.session_state.current_school
    user = st.session_state.user
    school_code = school['code']
    
    # Initialize managers
    user_manager = UserManager(school_code)
    friendship_manager = FriendshipManager(school_code)
    message_manager = MessageManager(school_code)
    
    # Get data
    users = user_manager.get_all_users()
    friends = friendship_manager.get_friends(user['email'])
    unread_count = message_manager.get_unread_count(user['email'])
    pending_requests = friendship_manager.get_pending_requests(user['email'])
    
    # ============ SIDEBAR ============
    with st.sidebar:
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.3); border: 1px solid rgba(255,215,0,0.3); 
                    border-radius: 12px; padding: 12px; margin-bottom: 12px; text-align: center;">
            <h2 style="color: white; margin: 0;">{school['name']}</h2>
            <div style="background: rgba(0,0,0,0.3); padding: 4px; border-radius: 20px; 
                        margin-top: 5px; border: 1px solid rgba(255,215,0,0.3);">
                <code style="background: transparent; color: gold; font-size: 0.8rem;">{school['code']}</code>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Profile card
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        
        if user.get('profile_pic'):
            st.image(user['profile_pic'], width=50)
        else:
            emoji = "👑" if user['role'] == 'admin' else "👨‍🏫" if user['role'] == 'teacher' else "👨‍🎓" if user['role'] == 'student' else "👪"
            st.markdown(f"<h1 style='font-size: 2rem; margin: 0;'>{emoji}</h1>", unsafe_allow_html=True)
        
        role_display = user['role'].upper()
        
        st.markdown(f"""
        <div style="color: white; flex: 1;">
            <strong>{user['fullname']}</strong><br>
            <span style="background: rgba(255,215,0,0.1); color: gold; padding: 2px 8px; 
                        border-radius: 12px; font-size: 0.7rem;">{role_display}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        
        # Navigation based on role
        if user['role'] == 'admin':
            options = [
                "Dashboard", "Announcements", "Classes", "Groups", 
                "Teachers", "Students", "Guardians", "Assignments", 
                "Community", f"Chat 💬{f' ({unread_count})' if unread_count>0 else ''}", 
                f"Friends 🤝{f' ({len(pending_requests)})' if pending_requests else ''}", 
                "Profile"
            ]
        elif user['role'] == 'teacher':
            options = [
                "Dashboard", "Announcements", "My Classes", "Groups", 
                "Assignments", "Community", 
                f"Chat 💬{f' ({unread_count})' if unread_count>0 else ''}", 
                f"Friends 🤝{f' ({len(pending_requests)})' if pending_requests else ''}", 
                "Profile"
            ]
        elif user['role'] == 'student':
            options = [
                "Dashboard", "Announcements", "Browse Classes", 
                "My Classes", "Groups", "Assignments", "Community", 
                f"Chat 💬{f' ({unread_count})' if unread_count>0 else ''}", 
                f"Friends 🤝{f' ({len(pending_requests)})' if pending_requests else ''}", 
                "Profile"
            ]
        else:  # guardian
            options = [
                "Dashboard", "Announcements", "My Student", 
                "Assignments", "Community", 
                f"Chat 💬{f' ({unread_count})' if unread_count>0 else ''}", 
                f"Friends 🤝{f' ({len(pending_requests)})' if pending_requests else ''}", 
                "Profile"
            ]
        
        # Fix menu index
        if st.session_state.menu_index >= len(options):
            st.session_state.menu_index = 0
            
        menu = st.radio("", options, index=st.session_state.menu_index, label_visibility="collapsed")
        st.session_state.menu_index = options.index(menu)
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            # Create backup on logout
            db_manager.backup_database(school_code)
            
            st.session_state.user = None
            st.session_state.current_school = None
            st.session_state.page = 'welcome'
            st.rerun()
    
    # ============ MAIN CONTENT ============
    
    # Check for auto-refresh on chat pages
    if menu.startswith("Chat") and should_refresh():
        st.rerun()
    
    # ----- DASHBOARD HOME -----
    if menu == "Dashboard":
        st.markdown(f"<h2 style='text-align: center;'>Welcome, {user['fullname']}!</h2>", unsafe_allow_html=True)
        
        if user['role'] == 'admin':
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Students", school['stats'].get('students', 0))
            col2.metric("Teachers", school['stats'].get('teachers', 0))
            col3.metric("Guardians", school['stats'].get('guardians', 0))
            col4.metric("Classes", school['stats'].get('classes', 0))
            col5.metric("Groups", school['stats'].get('groups', 0))
            
            # Recent activity
            st.subheader("📊 Recent Activity")
            
            with db_manager.get_connection(school_code) as conn:
                cursor = conn.cursor()
                
                # Recent users
                cursor.execute('''
                    SELECT * FROM users ORDER BY joined DESC LIMIT 5
                ''')
                recent_users = cursor.fetchall()
                
                if recent_users:
                    st.write("**New Users:**")
                    for u in recent_users:
                        st.write(f"- {u['fullname']} ({u['role']}) - Joined: {u['joined']}")
        
        elif user['role'] == 'teacher':
            with db_manager.get_connection(school_code) as conn:
                cursor = conn.cursor()
                
                # My classes
                cursor.execute('''
                    SELECT COUNT(*) as count FROM classes WHERE teacher = ?
                ''', (user['email'],))
                class_count = cursor.fetchone()['count']
                
                # My groups
                cursor.execute('''
                    SELECT COUNT(*) as count FROM group_members gm
                    JOIN groups g ON gm.group_code = g.code
                    WHERE gm.member_email = ? AND gm.role IN ('leader', 'co-leader')
                ''', (user['email'],))
                group_count = cursor.fetchone()['count']
                
                col1, col2, col3 = st.columns(3)
                col1.metric("My Classes", class_count)
                col2.metric("My Groups", group_count)
                col3.metric("Friends", len(friends))
        
        elif user['role'] == 'student':
            with db_manager.get_connection(school_code) as conn:
                cursor = conn.cursor()
                
                # My classes
                cursor.execute('''
                    SELECT COUNT(*) as count FROM class_enrollments 
                    WHERE student_email = ? AND status = 'active'
                ''', (user['email'],))
                class_count = cursor.fetchone()['count']
                
                # My groups
                cursor.execute('''
                    SELECT COUNT(*) as count FROM group_members 
                    WHERE member_email = ? AND role != 'pending'
                ''', (user['email'],))
                group_count = cursor.fetchone()['count']
                
                col1, col2, col3 = st.columns(3)
                col1.metric("My Classes", class_count)
                col2.metric("My Groups", group_count)
                col3.metric("Admission", user.get('admission_number', 'N/A')[:10] + "...")
        
        else:  # guardian
            st.info(f"Monitoring student progress")
            
            # Show linked students
            with db_manager.get_connection(school_code) as conn:
                cursor = conn.cursor()
                
                # This is simplified - in a real app, you'd have a proper linking table
                cursor.execute('''
                    SELECT * FROM users WHERE role = 'student' LIMIT 1
                ''')
                student = cursor.fetchone()
                
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
                            st.write(f"Admission: {student['admission_number']}")
    
    # ----- ANNOUNCEMENTS -----
    elif menu == "Announcements":
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
                        attachment = st.file_uploader("📎 Attachment", type=Config.ALLOWED_EXTENSIONS)
                    
                    if st.form_submit_button("📢 Post Announcement", use_container_width=True):
                        if title and content:
                            attachment_data = save_attachment(attachment) if attachment else None
                            
                            with db_manager.get_connection(school_code) as conn:
                                cursor = conn.cursor()
                                cursor.execute('''
                                    INSERT INTO announcements (
                                        id, title, content, author, author_email, 
                                        author_role, date, target, important, attachment
                                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                ''', (
                                    generate_id("ANN"),
                                    title,
                                    content,
                                    user['fullname'],
                                    user['email'],
                                    user['role'],
                                    datetime.now().strftime("%Y-%m-%d %H:%M"),
                                    target,
                                    1 if important else 0,
                                    json.dumps(attachment_data) if attachment_data else None
                                ))
                                
                                # Update school stats
                                schools = school_manager.load_all_schools()
                                schools[school_code]['stats']['announcements'] = schools[school_code]['stats'].get('announcements', 0) + 1
                                school_manager.save_all_schools(schools)
                                
                                st.success("Announcement posted!")
                                st.rerun()
        
        # Display announcements
        with db_manager.get_connection(school_code) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM announcements ORDER BY date DESC LIMIT 20
            ''')
            announcements = cursor.fetchall()
        
        if announcements:
            for ann in announcements:
                ann = dict(ann)
                if ann['attachment']:
                    ann['attachment'] = json.loads(ann['attachment'])
                
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
                            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                                <div>
                                    <div class="announcement-title">{ann['title']}{' ⭐' if ann['important'] else ''}</div>
                                    <div style="color: rgba(255,255,255,0.5); font-size: 0.8rem;">
                                        By {ann['author']} • {ann['date'][:16]}
                                    </div>
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
    
    # ----- COMMUNITY -----
    elif menu == "Community":
        st.markdown("<h2 style='text-align: center;'>🌍 School Community</h2>", unsafe_allow_html=True)
        
        # Get all members
        all_members = [u for u in users if u['email'] != user['email']]
        friends = friendship_manager.get_friends(user['email'])
        pending = friendship_manager.get_pending_requests(user['email'])
        sent = friendship_manager.get_sent_requests(user['email'])
        
        # Filter options
        col1, col2 = st.columns([2, 1])
        with col1:
            filter_role = st.selectbox("Filter by Role", ["All", "Admin", "Teacher", "Student", "Guardian"])
        with col2:
            search_term = st.text_input("🔍 Search", placeholder="Type name...")
        
        filtered_members = all_members
        if filter_role != "All":
            filtered_members = [m for m in all_members if m['role'].lower() == filter_role.lower()]
        if search_term:
            filtered_members = [m for m in filtered_members if search_term.lower() in m['fullname'].lower()]
        
        st.subheader(f"👥 Members ({len(filtered_members)})")
        
        for member in filtered_members:
            is_friend = member['email'] in friends
            request_sent = any(r['to_email'] == member['email'] for r in sent)
            request_received = any(r['from_email'] == member['email'] for r in pending)
            
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
                    st.markdown(f"<span style='color: gold; font-size: 0.8rem;'>{member['role'].title()}</span>", unsafe_allow_html=True)
                
                with col3:
                    if is_friend:
                        st.markdown("<span style='color: #00ff88;'>✅ Friend</span>", unsafe_allow_html=True)
                    elif request_sent:
                        st.markdown("<span style='color: gold;'>⏳ Request Sent</span>", unsafe_allow_html=True)
                    elif request_received:
                        st.markdown("<span style='color: #ffa500;'>📥 Request Received</span>", unsafe_allow_html=True)
                    else:
                        st.markdown("<span style='color: rgba(255,255,255,0.5);'>Not Connected</span>", unsafe_allow_html=True)
                
                with col4:
                    if not is_friend and not request_sent and not request_received:
                        if st.button("➕ Add Friend", key=f"add_{member['email']}"):
                            if friendship_manager.send_request(user['email'], member['email']):
                                st.success("Friend request sent!")
                                st.rerun()
                            else:
                                st.error("Could not send request")
                    elif request_received:
                        if st.button("✅ Accept", key=f"accept_{member['email']}"):
                            req = next(r for r in pending if r['from_email'] == member['email'])
                            if friendship_manager.accept_request(req['id']):
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
    
    # ----- FRIENDS -----
    elif menu.startswith("Friends"):
        st.markdown("<h2 style='text-align: center;'>🤝 Friends</h2>", unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["✅ My Friends", "📥 Received", "📤 Sent"])
        
        with tab1:
            friends_list = friendship_manager.get_friends(user['email'])
            if friends_list:
                for friend_email in friends_list:
                    friend = user_manager.get_user_by_email(friend_email)
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
                                st.markdown(f"<span style='color: gold; font-size: 0.8rem;'>{friend['role'].title()}</span>", unsafe_allow_html=True)
                            with col3:
                                if st.button("💬 Chat", key=f"chat_friend_{friend_email}"):
                                    st.session_state.chat_with = friend_email
                                    chat_options = [opt for opt in options if "Chat" in opt]
                                    if chat_options:
                                        st.session_state.menu_index = options.index(chat_options[0])
                                        st.rerun()
                            st.divider()
            else:
                st.info("No friends yet. Go to Community to add friends!")
        
        with tab2:
            pending = friendship_manager.get_pending_requests(user['email'])
            if pending:
                for req in pending:
                    sender = user_manager.get_user_by_email(req['from_email'])
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
                                st.markdown(f"<span style='color: gold; font-size: 0.8rem;'>{sender['role'].title()}</span>", unsafe_allow_html=True)
                                st.markdown(f"<span style='color: rgba(255,255,255,0.5); font-size: 0.7rem;'>{req['date']}</span>", unsafe_allow_html=True)
                            with col3:
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    if st.button("✅ Accept", key=f"accept_{req['id']}"):
                                        if friendship_manager.accept_request(req['id']):
                                            st.rerun()
                                with col_b:
                                    if st.button("❌ Decline", key=f"decline_{req['id']}"):
                                        if friendship_manager.decline_request(req['id']):
                                            st.rerun()
                            st.divider()
            else:
                st.info("No pending friend requests")
        
        with tab3:
            sent = friendship_manager.get_sent_requests(user['email'])
            if sent:
                for req in sent:
                    recipient = user_manager.get_user_by_email(req['to_email'])
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
                                st.markdown(f"<span style='color: gold; font-size: 0.8rem;'>{recipient['role'].title()}</span>", unsafe_allow_html=True)
                                st.markdown(f"<span style='color: rgba(255,255,255,0.5); font-size: 0.7rem;'>Sent: {req['date']}</span>", unsafe_allow_html=True)
                            with col3:
                                st.markdown("<span style='color: gold;'>⏳ Pending</span>", unsafe_allow_html=True)
                            st.divider()
            else:
                st.info("No sent requests")
    
    # ----- CHAT -----
    elif menu.startswith("Chat"):
        st.markdown("<h2 style='text-align: center;'>💬 Messages</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### Chats")
            friends_list = friendship_manager.get_friends(user['email'])
            
            if friends_list:
                conversations = message_manager.get_conversations(user['email'])
                
                for friend_email in friends_list:
                    friend = user_manager.get_user_by_email(friend_email)
                    if friend:
                        # Get last message
                        conv_msgs = conversations.get(friend_email, [])
                        last_msg = conv_msgs[-1]['message'][:30] + "..." if conv_msgs and conv_msgs[-1]['message'] else "No messages"
                        unread = len([m for m in conv_msgs if m['recipient'] == user['email'] and not m['read']])
                        
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
                                    st.markdown(f"<span style='color: rgba(255,255,255,0.5); font-size: 0.8rem;'>{last_msg}</span>", unsafe_allow_html=True)
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
                other_user = user_manager.get_user_by_email(other_email)
                
                if other_user:
                    st.markdown(f"### Chat with {other_user['fullname']}")
                    
                    # Get conversation
                    conversations = message_manager.get_conversations(user['email'])
                    conv_msgs = conversations.get(other_email, [])
                    
                    # Chat container
                    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
                    
                    for msg in conv_msgs:
                        if msg['recipient'] == user['email'] and not msg['read']:
                            message_manager.mark_as_read(msg['id'])
                        
                        is_sent = msg['sender'] == user['email']
                        sender_user = user if is_sent else other_user
                        
                        st.markdown(f"""
                        <div class="chat-message-wrapper {'chat-message-sent' if is_sent else 'chat-message-received'}">
                            <div class="chat-bubble {'chat-bubble-sent' if is_sent else 'chat-bubble-received'}">
                                <div>{msg['message']}</div>
                                <div class="chat-time">{msg['timestamp'][:16]}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if msg.get('attachment'):
                            with st.expander("📎 Attachment"):
                                display_attachment(msg['attachment'])
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Message input
                    with st.form("send_message", clear_on_submit=True):
                        col_a, col_b = st.columns([5, 1])
                        with col_a:
                            message = st.text_area("Message", height=60, placeholder="Type a message...", label_visibility="collapsed")
                        with col_b:
                            attachment = st.file_uploader("📎", type=Config.ALLOWED_EXTENSIONS, label_visibility="collapsed")
                        
                        if st.form_submit_button("📤 Send", use_container_width=True):
                            if message or attachment:
                                attachment_data = save_attachment(attachment) if attachment else None
                                if message_manager.send_message(user['email'], other_email, message, attachment_data):
                                    st.rerun()
            else:
                st.info("Select a chat to start messaging")
    
    # ----- PROFILE -----
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
            if pic and validate_file_upload(pic):
                img = Image.open(pic)
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                b64 = base64.b64encode(buffered.getvalue()).decode()
                profile_pic = f"data:image/png;base64,{b64}"
                
                if user_manager.update_user_profile(user['email'], {'profile_pic': profile_pic}):
                    user['profile_pic'] = profile_pic
                    st.rerun()
        
        with col2:
            with st.form("edit_profile"):
                name = st.text_input("Full Name", user['fullname'])
                phone = st.text_input("Phone", user.get('phone', ''))
                bio = st.text_area("Bio", user.get('bio', ''), height=100)
                
                if st.form_submit_button("💾 Update Profile", use_container_width=True):
                    if user_manager.update_user_profile(user['email'], {
                        'fullname': name,
                        'phone': phone,
                        'bio': bio
                    }):
                        user.update({'fullname': name, 'phone': phone, 'bio': bio})
                        st.success("Profile updated!")
                        st.rerun()
            
            if user.get('admission_number'):
                st.info(f"🎫 Admission Number: **{user['admission_number']}**")
            
            # Stats
            st.subheader("📊 Stats")
            st.write(f"📧 Email: {user['email']}")
            st.write(f"📅 Joined: {user['joined']}")
            st.write(f"👥 Friends: {len(friends)}")
    
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
                        with db_manager.get_connection(school_code) as conn:
                            cursor = conn.cursor()
                            
                            # Check if code exists
                            cursor.execute("SELECT code FROM teacher_codes WHERE code = ?", (code.upper(),))
                            if cursor.fetchone():
                                st.error("Code already exists")
                            else:
                                cursor.execute('''
                                    INSERT INTO teacher_codes (id, name, code, department, created, status)
                                    VALUES (?, ?, ?, ?, ?, 'active')
                                ''', (
                                    generate_id("TCH"),
                                    name,
                                    code.upper(),
                                    dept,
                                    datetime.now().strftime("%Y-%m-%d")
                                ))
                                st.success(f"Code {code.upper()} created")
                                st.rerun()
        
        st.subheader("👥 Active Teachers")
        teachers = [u for u in users if u['role'] == 'teacher']
        
        if teachers:
            for teacher in teachers:
                with st.container():
                    col1, col2, col3 = st.columns([1, 3, 2])
                    with col1:
                        if teacher.get('profile_pic'):
                            st.image(teacher['profile_pic'], width=40)
                        else:
                            st.write("👨‍🏫")
                    with col2:
                        st.write(f"**{teacher['fullname']}**")
                        st.write(f"📧 {teacher['email']}")
                    with col3:
                        st.write(f"Joined: {teacher['joined']}")
                    st.divider()
        else:
            st.info("No teachers registered yet")
    
    # ----- STUDENTS SECTION (Admin only) -----
    elif menu == "Students" and user['role'] == 'admin':
        st.markdown("<h2 style='text-align: center;'>👨‍🎓 Student Management</h2>", unsafe_allow_html=True)
        
        students = [u for u in users if u['role'] == 'student']
        
        if students:
            for student in students:
                with st.container():
                    col1, col2, col3, col4 = st.columns([1, 3, 2, 1])
                    with col1:
                        if student.get('profile_pic'):
                            st.image(student['profile_pic'], width=40)
                        else:
                            st.write("👨‍🎓")
                    with col2:
                        st.write(f"**{student['fullname']}**")
                    with col3:
                        st.write(f"Adm: {student.get('admission_number', 'N/A')}")
                    with col4:
                        if st.button("🗑️", key=f"del_{student['user_id']}"):
                            # Soft delete - in production, you'd want to handle this carefully
                            st.warning("Delete functionality would need careful implementation")
                    st.divider()
        else:
            st.info("No students enrolled")
    
    # ----- GUARDIANS SECTION (Admin only) -----
    elif menu == "Guardians" and user['role'] == 'admin':
        st.markdown("<h2 style='text-align: center;'>👪 Guardian Management</h2>", unsafe_allow_html=True)
        
        guardians = [u for u in users if u['role'] == 'guardian']
        
        if guardians:
            for guardian in guardians:
                with st.container():
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if guardian.get('profile_pic'):
                            st.image(guardian['profile_pic'], width=40)
                        else:
                            st.write("👪")
                    with col2:
                        st.write(f"**{guardian['fullname']}**")
                        st.write(f"📧 {guardian['email']}")
                    st.divider()
        else:
            st.info("No guardians registered")
    
    # ----- ASSIGNMENTS -----
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
                        
                        # Get classes
                        with db_manager.get_connection(school_code) as conn:
                            cursor = conn.cursor()
                            cursor.execute("SELECT name FROM classes WHERE status = 'active'")
                            class_list = [row['name'] for row in cursor.fetchall()]
                        
                        target_class = st.selectbox("Target Class", ["All Classes"] + class_list)
                    
                    with col2:
                        due_date = st.date_input("Due Date")
                        total_points = st.number_input("Total Points", min_value=1, value=100)
                        attachment = st.file_uploader("📎 Attachment", type=Config.ALLOWED_EXTENSIONS)
                    
                    description = st.text_area("Description", height=100)
                    
                    if st.form_submit_button("📝 Create Assignment", use_container_width=True):
                        if title and description:
                            attachment_data = save_attachment(attachment) if attachment else None
                            
                            with db_manager.get_connection(school_code) as conn:
                                cursor = conn.cursor()
                                cursor.execute('''
                                    INSERT INTO assignments (
                                        id, title, description, subject, target_class,
                                        due_date, total_points, created_by, created_date, attachment
                                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                ''', (
                                    generate_id("ASN"),
                                    title,
                                    description,
                                    subject,
                                    target_class,
                                    due_date.strftime("%Y-%m-%d"),
                                    total_points,
                                    user['email'],
                                    datetime.now().strftime("%Y-%m-%d %H:%M"),
                                    json.dumps(attachment_data) if attachment_data else None
                                ))
                                
                                st.success("Assignment created!")
                                st.rerun()
        
        # Display assignments
        st.subheader("📋 Current Assignments")
        
        with db_manager.get_connection(school_code) as conn:
            cursor = conn.cursor()
            
            if user['role'] == 'student':
                # Get student's classes
                cursor.execute('''
                    SELECT c.name FROM classes c
                    JOIN class_enrollments ce ON c.code = ce.class_code
                    WHERE ce.student_email = ? AND ce.status = 'active'
                ''', (user['email'],))
                my_classes = [row['name'] for row in cursor.fetchall()]
                
                # Get assignments
                placeholders = ','.join(['?'] * len(my_classes)) if my_classes else "''"
                query = f'''
                    SELECT * FROM assignments 
                    WHERE target_class IN ('All Classes', {placeholders})
                    ORDER BY due_date
                '''
                cursor.execute(query, my_classes if my_classes else [])
                
            elif user['role'] == 'teacher':
                cursor.execute('''
                    SELECT * FROM assignments 
                    WHERE created_by = ?
                    ORDER BY due_date
                ''', (user['email'],))
                
            else:  # admin or guardian
                cursor.execute('''
                    SELECT * FROM assignments 
                    ORDER BY due_date
                ''')
            
            assignments = cursor.fetchall()
        
        if assignments:
            for a in assignments:
                a = dict(a)
                if a['attachment']:
                    a['attachment'] = json.loads(a['attachment'])
                
                due = datetime.strptime(a['due_date'], '%Y-%m-%d')
                status_color = '#ff4444' if due < datetime.now() else '#00ff88'
                
                with st.container():
                    st.markdown(f"""
                    <div class="assignment-card">
                        <div style="display: flex; justify-content: space-between;">
                            <div>
                                <strong style="color: gold;">{a['title']}</strong>
                                <span style="color: rgba(255,255,255,0.5); margin-left: 10px;">{a['subject']}</span>
                            </div>
                            <div style="color: {status_color};">
                                Due: {a['due_date']}
                            </div>
                        </div>
                        <div style="margin: 10px 0; color: white;">{a['description']}</div>
                        <div style="display: flex; gap: 20px; font-size: 0.9rem; color: rgba(255,255,255,0.6);">
                            <span>Points: {a['total_points']}</span>
                            <span>Target: {a['target_class']}</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if a.get('attachment'):
                        st.markdown("**📎 Attachment:**")
                        display_attachment(a['attachment'])
                    
                    # Submission for students
                    if user['role'] == 'student':
                        # Check if already submitted
                        with db_manager.get_connection(school_code) as conn:
                            cursor = conn.cursor()
                            cursor.execute('''
                                SELECT * FROM assignment_submissions 
                                WHERE assignment_id = ? AND student_email = ?
                            ''', (a['id'], user['email']))
                            submitted = cursor.fetchone()
                        
                        if not submitted:
                            with st.form(key=f"submit_{a['id']}"):
                                submission_file = st.file_uploader(
                                    "Submit your work", 
                                    type=Config.ALLOWED_EXTENSIONS, 
                                    key=f"sub_{a['id']}"
                                )
                                if st.form_submit_button("📤 Submit"):
                                    if submission_file:
                                        sub_data = save_attachment(submission_file)
                                        cursor.execute('''
                                            INSERT INTO assignment_submissions (
                                                assignment_id, student_email, submission_date, attachment
                                            ) VALUES (?, ?, ?, ?)
                                        ''', (
                                            a['id'],
                                            user['email'],
                                            datetime.now().strftime("%Y-%m-%d %H:%M"),
                                            json.dumps(sub_data)
                                        ))
                                        st.success("Assignment submitted!")
                                        st.rerun()
                    
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("No assignments available")
    
    # ----- CLASSES SECTION (simplified for brevity) -----
    elif menu in ["Classes", "My Classes", "Browse Classes"]:
        st.markdown("<h2 style='text-align: center;'>📚 Classes</h2>", unsafe_allow_html=True)
        
        # Simplified class display
        with db_manager.get_connection(school_code) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.*, COUNT(ce.student_email) as student_count
                FROM classes c
                LEFT JOIN class_enrollments ce ON c.code = ce.class_code AND ce.status = 'active'
                GROUP BY c.code
            ''')
            classes = cursor.fetchall()
        
        if menu == "My Classes" and user['role'] == 'student':
            # Show student's enrolled classes
            with db_manager.get_connection(school_code) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT c.* FROM classes c
                    JOIN class_enrollments ce ON c.code = ce.class_code
                    WHERE ce.student_email = ? AND ce.status = 'active'
                ''', (user['email'],))
                display_classes = cursor.fetchall()
            st.subheader(f"📋 My Classes ({len(display_classes)})")
        else:
            display_classes = classes
            st.subheader(f"📋 All Classes ({len(display_classes)})")
        
        for c in display_classes:
            c = dict(c)
            with st.expander(f"📖 {c['name']} - {c.get('grade', 'N/A')} ({c['code']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Subject:** {c.get('subject', 'N/A')}")
                    st.write(f"**Teacher:** {c.get('teacher_name', 'Unknown')}")
                    st.write(f"**Room:** {c.get('room', 'TBD')}")
                with col2:
                    st.write(f"**Schedule:** {c.get('schedule', 'TBD')}")
                    st.write(f"**Students:** {c.get('student_count', 0)}/{c.get('max_students', 40)}")
                
                # Join button for students
                if user['role'] == 'student' and menu == "Browse Classes":
                    # Check if already enrolled
                    with db_manager.get_connection(school_code) as conn:
                        cursor = conn.cursor()
                        cursor.execute('''
                            SELECT * FROM class_enrollments 
                            WHERE class_code = ? AND student_email = ?
                        ''', (c['code'], user['email']))
                        enrolled = cursor.fetchone()
                    
                    if not enrolled:
                        if st.button("📝 Enroll", key=f"enroll_{c['code']}"):
                            cursor.execute('''
                                INSERT INTO class_enrollments (class_code, student_email, enrolled_date, status)
                                VALUES (?, ?, ?, 'active')
                            ''', (c['code'], user['email'], datetime.now().strftime("%Y-%m-%d")))
                            st.success("Enrolled successfully!")
                            st.rerun()
    
    # ----- GROUPS SECTION (simplified for brevity) -----
    elif menu == "Groups":
        st.markdown("<h2 style='text-align: center;'>👥 Groups</h2>", unsafe_allow_html=True)
        
        with db_manager.get_connection(school_code) as conn:
            cursor = conn.cursor()
            
            # Get all groups
            cursor.execute('''
                SELECT g.*, COUNT(gm.member_email) as member_count
                FROM groups g
                LEFT JOIN group_members gm ON g.code = gm.group_code AND gm.role != 'pending'
                GROUP BY g.code
            ''')
            groups = cursor.fetchall()
        
        st.subheader(f"📋 All Groups ({len(groups)})")
        
        for g in groups:
            g = dict(g)
            with st.expander(f"👥 {g['name']} - {g.get('type', 'Group')} ({g['code']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Description:** {g.get('description', 'No description')}")
                    st.write(f"**Leader:** {g.get('leader_name', 'Unknown')}")
                with col2:
                    st.write(f"**Members:** {g.get('member_count', 0)}/{g.get('max_members', 20)}")
                    st.write(f"**Created:** {g['created']}")
                
                # Check membership
                with db_manager.get_connection(school_code) as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        SELECT role FROM group_members 
                        WHERE group_code = ? AND member_email = ?
                    ''', (g['code'], user['email']))
                    membership = cursor.fetchone()
                
                if not membership:
                    if st.button("📝 Request to Join", key=f"join_group_{g['code']}"):
                        cursor.execute('''
                            INSERT INTO group_members (group_code, member_email, role, joined_date)
                            VALUES (?, ?, 'pending', ?)
                        ''', (g['code'], user['email'], datetime.now().strftime("%Y-%m-%d")))
                        st.success("Request sent!")
                        st.rerun()
                elif membership['role'] == 'pending':
                    st.info("⏳ Request pending approval")
                else:
                    st.success(f"✅ You are a {membership['role']}")
    
    # ----- MY STUDENT (guardian only) -----
    elif menu == "My Student" and user['role'] == 'guardian':
        st.markdown("<h2 style='text-align: center;'>👨‍🎓 My Student</h2>", unsafe_allow_html=True)
        
        # Simplified - in production, you'd have proper linking
        with db_manager.get_connection(school_code) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM users WHERE role = 'student' LIMIT 1
            ''')
            student = cursor.fetchone()
        
        if student:
            student = dict(student)
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    if student.get('profile_pic'):
                        st.image(student['profile_pic'], width=80)
                    else:
                        st.markdown("<h1 style='font-size: 3rem;'>👨‍🎓</h1>", unsafe_allow_html=True)
                with col2:
                    st.subheader(student['fullname'])
                    st.write(f"📧 {student.get('email', 'No email')}")
                    st.write(f"🎫 Admission: {student.get('admission_number', 'N/A')}")
                
                # Get student's classes
                with db_manager.get_connection(school_code) as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        SELECT c.* FROM classes c
                        JOIN class_enrollments ce ON c.code = ce.class_code
                        WHERE ce.student_email = ? AND ce.status = 'active'
                    ''', (student['email'],))
                    student_classes = cursor.fetchall()
                
                if student_classes:
                    st.markdown("### 📚 Enrolled Classes")
                    for c in student_classes:
                        st.write(f"- {c['name']} ({c.get('grade', 'N/A')})")
                
                st.divider()
        else:
            st.info("No student linked to your account")

else:
    st.error("Session expired. Please login again.")
    if st.button("Go to Login"):
        st.session_state.page = 'welcome'
        st.rerun()
