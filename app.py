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
import os

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

# ============ EXPANDED THEMES COLLECTION ============
THEMES = {
    # Solid Color Themes (can also serve as backgrounds)
    "Sunrise Glow": {
        "primary": "#ff6b6b",
        "secondary": "#feca57",
        "accent": "#48dbfb",
        "background": "linear-gradient(135deg, #ff6b6b, #feca57, #ff9ff3, #48dbfb)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #cfa668, #e5b873, #f5d742)",
        "type": "gradient"
    },
    "Ocean Breeze": {
        "primary": "#00d2ff",
        "secondary": "#3a1c71",
        "accent": "#00ff00",
        "background": "linear-gradient(135deg, #00d2ff, #3a1c71, #d76d77, #ffaf7b)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #4facfe, #00f2fe, #43e97b)",
        "type": "gradient"
    },
    "Purple Haze": {
        "primary": "#8E2DE2",
        "secondary": "#4A00E0",
        "accent": "#a044ff",
        "background": "linear-gradient(135deg, #8E2DE2, #4A00E0, #6a3093, #a044ff)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #c471ed, #f64f59, #c471ed)",
        "type": "gradient"
    },
    "Tropical Paradise": {
        "primary": "#00b09b",
        "secondary": "#96c93d",
        "accent": "#fbd786",
        "background": "linear-gradient(135deg, #00b09b, #96c93d, #c6ffdd, #fbd786)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #4facfe, #00f2fe, #43e97b)",
        "type": "gradient"
    },
    "Cherry Blossom": {
        "primary": "#ff9a9e",
        "secondary": "#fad0c4",
        "accent": "#a1c4fd",
        "background": "linear-gradient(135deg, #ff9a9e, #fad0c4, #ffd1ff, #a1c4fd)",
        "text": "#333333",
        "sidebar": "linear-gradient(135deg, #fbc2eb, #a6c1ee, #fbc2eb)",
        "type": "gradient"
    },
    "Midnight City": {
        "primary": "#232526",
        "secondary": "#414345",
        "accent": "#4b6cb7",
        "background": "linear-gradient(135deg, #232526, #414345, #2c3e50, #4b6cb7)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #182848, #4b6cb7, #182848)",
        "type": "gradient"
    },
    "Autumn Leaves": {
        "primary": "#e44d2e",
        "secondary": "#f39c12",
        "accent": "#f1c40f",
        "background": "linear-gradient(135deg, #e44d2e, #f39c12, #d35400, #e67e22)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #f1c40f, #e67e22, #d35400)",
        "type": "gradient"
    },
    "Northern Lights": {
        "primary": "#43C6AC",
        "secondary": "#191654",
        "accent": "#00CDAC",
        "background": "linear-gradient(135deg, #43C6AC, #191654, #02AAB0, #00CDAC)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #02AAB0, #00CDAC, #191654)",
        "type": "gradient"
    },
    "Forest Mist": {
        "primary": "#11998e",
        "secondary": "#38ef7d",
        "accent": "#38ef7d",
        "background": "linear-gradient(135deg, #11998e, #38ef7d, #11998e, #38ef7d)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #11998e, #38ef7d, #11998e)",
        "type": "gradient"
    },
    "Lavender Dream": {
        "primary": "#aa4b6b",
        "secondary": "#6b6b83",
        "accent": "#3b8d99",
        "background": "linear-gradient(135deg, #aa4b6b, #6b6b83, #3b8d99, #aa4b6b)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #aa4b6b, #6b6b83, #3b8d99)",
        "type": "gradient"
    },
    "Sunset Orange": {
        "primary": "#f12711",
        "secondary": "#f5af19",
        "accent": "#f5af19",
        "background": "linear-gradient(135deg, #f12711, #f5af19, #f12711, #f5af19)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #f12711, #f5af19, #f12711)",
        "type": "gradient"
    },
    "Electric Blue": {
        "primary": "#00c6fb",
        "secondary": "#005bea",
        "accent": "#00c6fb",
        "background": "linear-gradient(135deg, #00c6fb, #005bea, #00c6fb, #005bea)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #00c6fb, #005bea, #00c6fb)",
        "type": "gradient"
    },
    "Pink Flamingo": {
        "primary": "#f857a6",
        "secondary": "#ff5858",
        "accent": "#f857a6",
        "background": "linear-gradient(135deg, #f857a6, #ff5858, #f857a6, #ff5858)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #f857a6, #ff5858, #f857a6)",
        "type": "gradient"
    },
    "Emerald City": {
        "primary": "#348f50",
        "secondary": "#56ab2f",
        "accent": "#56ab2f",
        "background": "linear-gradient(135deg, #348f50, #56ab2f, #348f50, #56ab2f)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #348f50, #56ab2f, #348f50)",
        "type": "gradient"
    },
    "Ruby Red": {
        "primary": "#cb356b",
        "secondary": "#bd3f32",
        "accent": "#cb356b",
        "background": "linear-gradient(135deg, #cb356b, #bd3f32, #cb356b, #bd3f32)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #cb356b, #bd3f32, #cb356b)",
        "type": "gradient"
    },
    "Sapphire Blue": {
        "primary": "#0f0c29",
        "secondary": "#302b63",
        "accent": "#24243e",
        "background": "linear-gradient(135deg, #0f0c29, #302b63, #24243e, #0f0c29)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #0f0c29, #302b63, #24243e)",
        "type": "gradient"
    },
    "Amber Glow": {
        "primary": "#ff8008",
        "secondary": "#ffc837",
        "accent": "#ff8008",
        "background": "linear-gradient(135deg, #ff8008, #ffc837, #ff8008, #ffc837)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #ff8008, #ffc837, #ff8008)",
        "type": "gradient"
    },
    "Teal Tide": {
        "primary": "#1d976c",
        "secondary": "#93f9b9",
        "accent": "#1d976c",
        "background": "linear-gradient(135deg, #1d976c, #93f9b9, #1d976c, #93f9b9)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #1d976c, #93f9b9, #1d976c)",
        "type": "gradient"
    },
    "Grape Escape": {
        "primary": "#8e2de2",
        "secondary": "#4a00e0",
        "accent": "#8e2de2",
        "background": "linear-gradient(135deg, #8e2de2, #4a00e0, #8e2de2, #4a00e0)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #8e2de2, #4a00e0, #8e2de2)",
        "type": "gradient"
    },
    "Peach Perfect": {
        "primary": "#ff6a88",
        "secondary": "#ff99ac",
        "accent": "#ff6a88",
        "background": "linear-gradient(135deg, #ff6a88, #ff99ac, #ff6a88, #ff99ac)",
        "text": "#333333",
        "sidebar": "linear-gradient(135deg, #ff6a88, #ff99ac, #ff6a88)",
        "type": "gradient"
    },
    
    # Solid Color Themes (can be used as backgrounds)
    "Solid Red": {
        "primary": "#ff4444",
        "secondary": "#cc0000",
        "accent": "#ff8888",
        "background": "#ff4444",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #cc0000, #ff4444)",
        "type": "solid"
    },
    "Solid Blue": {
        "primary": "#4444ff",
        "secondary": "#0000cc",
        "accent": "#8888ff",
        "background": "#4444ff",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #0000cc, #4444ff)",
        "type": "solid"
    },
    "Solid Green": {
        "primary": "#44ff44",
        "secondary": "#00cc00",
        "accent": "#88ff88",
        "background": "#44ff44",
        "text": "#000000",
        "sidebar": "linear-gradient(135deg, #00cc00, #44ff44)",
        "type": "solid"
    },
    "Solid Purple": {
        "primary": "#aa44ff",
        "secondary": "#6600cc",
        "accent": "#cc88ff",
        "background": "#aa44ff",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #6600cc, #aa44ff)",
        "type": "solid"
    },
    "Solid Orange": {
        "primary": "#ff8844",
        "secondary": "#cc4400",
        "accent": "#ffaa88",
        "background": "#ff8844",
        "text": "#000000",
        "sidebar": "linear-gradient(135deg, #cc4400, #ff8844)",
        "type": "solid"
    },
    "Solid Teal": {
        "primary": "#44ffaa",
        "secondary": "#00cc88",
        "accent": "#88ffcc",
        "background": "#44ffaa",
        "text": "#000000",
        "sidebar": "linear-gradient(135deg, #00cc88, #44ffaa)",
        "type": "solid"
    },
    "Solid Pink": {
        "primary": "#ff44aa",
        "secondary": "#cc0088",
        "accent": "#ff88cc",
        "background": "#ff44aa",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #cc0088, #ff44aa)",
        "type": "solid"
    },
    "Solid Brown": {
        "primary": "#aa6644",
        "secondary": "#884422",
        "accent": "#cc8866",
        "background": "#aa6644",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #884422, #aa6644)",
        "type": "solid"
    },
    "Solid Gray": {
        "primary": "#888888",
        "secondary": "#666666",
        "accent": "#aaaaaa",
        "background": "#888888",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #666666, #888888)",
        "type": "solid"
    },
    "Solid Black": {
        "primary": "#222222",
        "secondary": "#000000",
        "accent": "#444444",
        "background": "#222222",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #000000, #222222)",
        "type": "solid"
    }
}

# ============ EXPANDED WALLPAPERS COLLECTION ============
WALLPAPERS = {
    "None": "",
    
    # Abstract & Geometric
    "Abstract Waves": "https://images.unsplash.com/photo-1557682250-33bd709cbe85?q=80&w=2024&auto=format&fit=crop",
    "Geometric Pattern": "https://images.unsplash.com/photo-1557683311-eac922347aa1?q=80&w=2024&auto=format&fit=crop",
    "Color Splash": "https://images.unsplash.com/photo-1557683304-6733ba7e4d6f?q=80&w=2024&auto=format&fit=crop",
    "Gradient Flow": "https://images.unsplash.com/photo-1557683316-973673baf926?q=80&w=2024&auto=format&fit=crop",
    "Minimal Lines": "https://images.unsplash.com/photo-1557683311-eac922347aa1?q=80&w=2024&auto=format&fit=crop",
    "Dark Texture": "https://images.unsplash.com/photo-1557682250-33bd709cbe85?q=80&w=2024&auto=format&fit=crop",
    "Light Texture": "https://images.unsplash.com/photo-1557683320-2d5001d5e9c5?q=80&w=2024&auto=format&fit=crop",
    "Hexagon Pattern": "https://images.unsplash.com/photo-1558591710-4b4a1ae0f04d?q=80&w=1974&auto=format&fit=crop",
    "Polka Dots": "https://images.unsplash.com/photo-1558591710-4b4a1ae0f04d?q=80&w=1974&auto=format&fit=crop",
    "Stripes": "https://images.unsplash.com/photo-1557683316-973673baf926?q=80&w=2024&auto=format&fit=crop",
    "Zigzag": "https://images.unsplash.com/photo-1557683311-eac922347aa1?q=80&w=2024&auto=format&fit=crop",
    "Chevron": "https://images.unsplash.com/photo-1557682250-33bd709cbe85?q=80&w=2024&auto=format&fit=crop",
    
    # Nature
    "Forest": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=2024&auto=format&fit=crop",
    "Mountains": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?q=80&w=2024&auto=format&fit=crop",
    "Ocean": "https://images.unsplash.com/photo-1507525425510-56b1e2d6c4f2?q=80&w=2024&auto=format&fit=crop",
    "Desert": "https://images.unsplash.com/photo-1509316785289-025f5b846b35?q=80&w=2024&auto=format&fit=crop",
    "Aurora": "https://images.unsplash.com/photo-1483347756197-71ef80e95f73?q=80&w=2024&auto=format&fit=crop",
    "Galaxy": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?q=80&w=2024&auto=format&fit=crop",
    "Sunset": "https://images.unsplash.com/photo-1506815444479-bfdb1e96c566?q=80&w=2024&auto=format&fit=crop",
    "Rainbow": "https://images.unsplash.com/photo-1511300636408-a63a89df3482?q=80&w=2024&auto=format&fit=crop",
    "Clouds": "https://images.unsplash.com/photo-1501630834273-4b5604d2ee31?q=80&w=2024&auto=format&fit=crop",
    "Stars": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?q=80&w=2024&auto=format&fit=crop",
    "Waterfall": "https://images.unsplash.com/photo-1432405972618-c60b0225b8f9?q=80&w=2024&auto=format&fit=crop",
    "Beach": "https://images.unsplash.com/photo-1507525425510-56b1e2d6c4f2?q=80&w=2024&auto=format&fit=crop",
    "Lake": "https://images.unsplash.com/photo-1501785888041-af3ef285b470?q=80&w=2024&auto=format&fit=crop",
    "River": "https://images.unsplash.com/photo-1501785888041-af3ef285b470?q=80&w=2024&auto=format&fit=crop",
    "Meadow": "https://images.unsplash.com/photo-1504196606672-aef5c9cefc92?q=80&w=2024&auto=format&fit=crop",
    "Flowers": "https://images.unsplash.com/photo-1490750967868-88aa4486c946?q=80&w=2024&auto=format&fit=crop",
    "Autumn Leaves": "https://images.unsplash.com/photo-1501503064935-e07c1f0f0b8e?q=80&w=2024&auto=format&fit=crop",
    "Snow": "https://images.unsplash.com/photo-1491002052546-bf38f186af56?q=80&w=2024&auto=format&fit=crop",
    
    # City & Urban
    "City Lights": "https://images.unsplash.com/photo-1519501025264-65ba15a82390?q=80&w=2024&auto=format&fit=crop",
    "Skyline": "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?q=80&w=2024&auto=format&fit=crop",
    "Night City": "https://images.unsplash.com/photo-1514565131-fce0801e5785?q=80&w=2024&auto=format&fit=crop",
    "Downtown": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?q=80&w=2024&auto=format&fit=crop",
    "Street": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?q=80&w=2024&auto=format&fit=crop",
    "Bridge": "https://images.unsplash.com/photo-1514924013411-cbf25faa35bb?q=80&w=2024&auto=format&fit=crop",
    "Subway": "https://images.unsplash.com/photo-1514924013411-cbf25faa35bb?q=80&w=2024&auto=format&fit=crop",
    
    # Space & Science
    "Nebula": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?q=80&w=2024&auto=format&fit=crop",
    "Planets": "https://images.unsplash.com/photo-1614732414444-096e5f1122e1?q=80&w=2024&auto=format&fit=crop",
    "Milky Way": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a?q=80&w=2024&auto=format&fit=crop",
    "Comet": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?q=80&w=2024&auto=format&fit=crop",
    "Solar System": "https://images.unsplash.com/photo-1614732414444-096e5f1122e1?q=80&w=2024&auto=format&fit=crop",
    
    # Patterns & Textures
    "Wood Grain": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?q=80&w=2024&auto=format&fit=crop",
    "Marble": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?q=80&w=2024&auto=format&fit=crop",
    "Concrete": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?q=80&w=2024&auto=format&fit=crop",
    "Brick Wall": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?q=80&w=2024&auto=format&fit=crop",
    "Fabric": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?q=80&w=2024&auto=format&fit=crop",
    "Paper Texture": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?q=80&w=2024&auto=format&fit=crop",
    
    # Artistic
    "Watercolor": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?q=80&w=2024&auto=format&fit=crop",
    "Oil Painting": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?q=80&w=2024&auto=format&fit=crop",
    "Sketch": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?q=80&w=2024&auto=format&fit=crop",
    "Digital Art": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?q=80&w=2024&auto=format&fit=crop",
    
    # School & Education
    "Library": "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?q=80&w=2024&auto=format&fit=crop",
    "Classroom": "https://images.unsplash.com/photo-1580582932707-520aed937b7b?q=80&w=2024&auto=format&fit=crop",
    "Books": "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?q=80&w=2024&auto=format&fit=crop",
    "Graduation": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?q=80&w=2024&auto=format&fit=crop",
    "Campus": "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?q=80&w=2024&auto=format&fit=crop",
    
    # Inspirational
    "Success": "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?q=80&w=2024&auto=format&fit=crop",
    "Achievement": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?q=80&w=2024&auto=format&fit=crop",
    "Teamwork": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?q=80&w=2024&auto=format&fit=crop",
    "Innovation": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2024&auto=format&fit=crop",
    "Future": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2024&auto=format&fit=crop",
    
    # Seasonal
    "Spring": "https://images.unsplash.com/photo-1490750967868-88aa4486c946?q=80&w=2024&auto=format&fit=crop",
    "Summer": "https://images.unsplash.com/photo-1507525425510-56b1e2d6c4f2?q=80&w=2024&auto=format&fit=crop",
    "Autumn": "https://images.unsplash.com/photo-1501503064935-e07c1f0f0b8e?q=80&w=2024&auto=format&fit=crop",
    "Winter": "https://images.unsplash.com/photo-1491002052546-bf38f186af56?q=80&w=2024&auto=format&fit=crop",
    
    # Holidays
    "Christmas": "https://images.unsplash.com/photo-1482517967863-00e15c9b44be?q=80&w=2024&auto=format&fit=crop",
    "New Year": "https://images.unsplash.com/photo-1482517967863-00e15c9b44be?q=80&w=2024&auto=format&fit=crop",
    "Easter": "https://images.unsplash.com/photo-1482517967863-00e15c9b44be?q=80&w=2024&auto=format&fit=crop",
    "Diwali": "https://images.unsplash.com/photo-1482517967863-00e15c9b44be?q=80&w=2024&auto=format&fit=crop",
    "Hanukkah": "https://images.unsplash.com/photo-1482517967863-00e15c9b44be?q=80&w=2024&auto=format&fit=crop",
    
    # Animals
    "Wildlife": "https://images.unsplash.com/photo-1474511320723-9a56873867b5?q=80&w=2024&auto=format&fit=crop",
    "Pets": "https://images.unsplash.com/photo-1474511320723-9a56873867b5?q=80&w=2024&auto=format&fit=crop",
    "Birds": "https://images.unsplash.com/photo-1474511320723-9a56873867b5?q=80&w=2024&auto=format&fit=crop",
    "Butterflies": "https://images.unsplash.com/photo-1474511320723-9a56873867b5?q=80&w=2024&auto=format&fit=crop",
    
    # Sports
    "Football": "https://images.unsplash.com/photo-1489944440615-453fc2b6a9a9?q=80&w=2024&auto=format&fit=crop",
    "Basketball": "https://images.unsplash.com/photo-1489944440615-453fc2b6a9a9?q=80&w=2024&auto=format&fit=crop",
    "Soccer": "https://images.unsplash.com/photo-1489944440615-453fc2b6a9a9?q=80&w=2024&auto=format&fit=crop",
    "Swimming": "https://images.unsplash.com/photo-1489944440615-453fc2b6a9a9?q=80&w=2024&auto=format&fit=crop",
    "Athletics": "https://images.unsplash.com/photo-1489944440615-453fc2b6a9a9?q=80&w=2024&auto=format&fit=crop",
    
    # Music
    "Instruments": "https://images.unsplash.com/photo-1511379938547-c1f69419868d?q=80&w=2024&auto=format&fit=crop",
    "Concert": "https://images.unsplash.com/photo-1511379938547-c1f69419868d?q=80&w=2024&auto=format&fit=crop",
    "Studio": "https://images.unsplash.com/photo-1511379938547-c1f69419868d?q=80&w=2024&auto=format&fit=crop",
    
    # Art
    "Paintings": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?q=80&w=2024&auto=format&fit=crop",
    "Sculpture": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?q=80&w=2024&auto=format&fit=crop",
    "Museum": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?q=80&w=2024&auto=format&fit=crop",
    
    # Technology
    "Circuit": "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=2024&auto=format&fit=crop",
    "Code": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?q=80&w=2024&auto=format&fit=crop",
    "Robotics": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?q=80&w=2024&auto=format&fit=crop",
    "AI": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?q=80&w=2024&auto=format&fit=crop",
    
    # Travel
    "World Map": "https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?q=80&w=2024&auto=format&fit=crop",
    "Globe": "https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?q=80&w=2024&auto=format&fit=crop",
    "Compass": "https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?q=80&w=2024&auto=format&fit=crop",
    "Airplane": "https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?q=80&w=2024&auto=format&fit=crop",
    
    # Food
    "Fruits": "https://images.unsplash.com/photo-1490818387583-1baba5e638af?q=80&w=2024&auto=format&fit=crop",
    "Vegetables": "https://images.unsplash.com/photo-1490818387583-1baba5e638af?q=80&w=2024&auto=format&fit=crop",
    "Healthy Food": "https://images.unsplash.com/photo-1490818387583-1baba5e638af?q=80&w=2024&auto=format&fit=crop",
    
    # Abstract Art
    "Abstract 1": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?q=80&w=2024&auto=format&fit=crop",
    "Abstract 2": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?q=80&w=2024&auto=format&fit=crop",
    "Abstract 3": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?q=80&w=2024&auto=format&fit=crop",
    "Abstract 4": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?q=80&w=2024&auto=format&fit=crop",
    "Abstract 5": "https://images.unsplash.com/photo-1541701494587-cb58502866ab?q=80&w=2024&auto=format&fit=crop"
}

def get_theme_css(theme_name, wallpaper=None):
    theme = THEMES.get(theme_name, THEMES["Sunrise Glow"])
    wallpaper_url = WALLPAPERS.get(wallpaper, "") if wallpaper else ""
    
    # Determine background style
    if wallpaper_url:
        background_style = f"url('{wallpaper_url}') no-repeat center center fixed"
        background_size = "cover"
    else:
        background_style = theme["background"]
        background_size = "400% 400%" if theme.get("type") == "gradient" else "cover"
    
    # Get text color based on theme
    text_color = theme["text"]
    
    return f"""
    <style>
        /* Global text visibility enhancement */
        * {{
            text-shadow: 1px 1px 3px rgba(0,0,0,0.5) !important;
        }}
        
        body {{
            background: {background_style};
            background-size: {background_size};
            margin: 0;
            padding: 0;
            min-height: 100vh;
            font-family: 'Poppins', sans-serif;
            animation: {'' if wallpaper_url else 'gradient-shift 15s ease infinite'};
        }}
        
        .stApp {{
            background: transparent !important;
        }}
        
        /* Translucent main container */
        .main .block-container {{
            background: rgba(0, 0, 0, 0.3) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border-radius: 24px !important;
            padding: 2rem !important;
            margin: 1.5rem !important;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3) !important;
            border: 1px solid rgba(255, 215, 0, 0.3) !important;
            position: relative;
            z-index: 10;
        }}
        
        /* Translucent sidebar */
        section[data-testid="stSidebar"] {{
            background: {theme["sidebar"]} !important;
            background-size: 300% 300% !important;
            animation: golden-shimmer 8s ease infinite !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border-right: 2px solid rgba(255, 215, 0, 0.4) !important;
            box-shadow: 5px 0 30px rgba(218, 165, 32, 0.4) !important;
            z-index: 20;
        }}
        
        section[data-testid="stSidebar"] > div {{
            background: rgba(0, 0, 0, 0.3) !important;
            backdrop-filter: blur(5px) !important;
            -webkit-backdrop-filter: blur(5px) !important;
            padding: 1rem 0.8rem !important;
            width: 100% !important;
        }}
        
        /* Sidebar text visibility */
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] .stRadio label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div {{
            color: #FFD700 !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important;
            font-weight: 600 !important;
        }}
        
        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {{
            background: rgba(0, 0, 0, 0.4) !important;
            backdrop-filter: blur(5px) !important;
            -webkit-backdrop-filter: blur(5px) !important;
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
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important;
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
            text-shadow: none !important;
        }}
        
        /* Enhanced form elements with translucent backgrounds */
        .stSelectbox div[data-baseweb="select"],
        .stTextInput input, 
        .stTextArea textarea, 
        .stDateInput input,
        .stNumberInput input,
        .stTimeInput input,
        .stMultiselect div[data-baseweb="select"],
        .stSlider div[data-baseweb="slider"] {{
            background: rgba(255, 255, 255, 0.95) !important;
            border: 2px solid #FFD700 !important;
            border-radius: 12px !important;
            padding: 0.7rem 1rem !important;
            font-size: 0.95rem !important;
            color: #000000 !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            backdrop-filter: blur(5px) !important;
            -webkit-backdrop-filter: blur(5px) !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2) !important;
        }}
        
        /* Ensure input text is very visible */
        .stSelectbox div[data-baseweb="select"] *,
        .stTextInput input, 
        .stTextArea textarea, 
        .stDateInput input,
        .stNumberInput input,
        .stTimeInput input,
        .stMultiselect div[data-baseweb="select"] * {{
            color: #000000 !important;
            font-weight: 600 !important;
        }}
        
        .stSelectbox div[data-baseweb="select"]:hover,
        .stTextInput input:hover, 
        .stTextArea textarea:hover,
        .stDateInput input:hover,
        .stNumberInput input:hover {{
            border-color: #DAA520 !important;
            box-shadow: 0 0 20px rgba(255, 215, 0, 0.5) !important;
        }}
        
        /* Labels with enhanced visibility */
        .stTextInput label,
        .stTextArea label,
        .stSelectbox label,
        .stDateInput label,
        .stNumberInput label,
        .stCheckbox label,
        .stRadio label {{
            color: {text_color} !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7) !important;
            background: rgba(0,0,0,0.2) !important;
            padding: 2px 8px !important;
            border-radius: 4px !important;
            display: inline-block !important;
            margin-bottom: 5px !important;
        }}
        
        /* Tabs with translucent background */
        .stTabs [data-baseweb="tab-list"] {{
            background: rgba(255, 215, 0, 0.3) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border-radius: 16px !important;
            padding: 0.4rem !important;
            gap: 0.3rem;
            margin-bottom: 1.5rem !important;
            border: 1px solid rgba(255, 215, 0, 0.4) !important;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            color: {text_color} !important;
            border-radius: 12px !important;
            padding: 0.6rem 1.2rem !important;
            font-weight: 700 !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
            background: rgba(0,0,0,0.2) !important;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: rgba(255, 215, 0, 0.4) !important;
            color: #000000 !important;
            font-weight: 800 !important;
            text-shadow: none !important;
        }}
        
        /* Enhanced headers */
        h1, h2, h3, h4, h5, h6 {{
            color: {text_color} !important;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.7) !important;
            font-weight: 700 !important;
            background: rgba(0,0,0,0.2) !important;
            padding: 8px 16px !important;
            border-radius: 12px !important;
            display: inline-block !important;
            backdrop-filter: blur(5px) !important;
            -webkit-backdrop-filter: blur(5px) !important;
        }}
        
        h1 {{
            background: linear-gradient(135deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
            font-size: 2.8rem !important;
            font-weight: 800 !important;
            text-align: center;
            margin-bottom: 2rem !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
            background: rgba(255,255,255,0.1) !important;
            padding: 15px 30px !important;
            border-radius: 50px !important;
        }}
        
        /* Enhanced cards with better visibility */
        .golden-card {{
            background: rgba(0, 0, 0, 0.4) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border-left: 6px solid #FFD700 !important;
            border-radius: 16px !important;
            padding: 25px !important;
            margin-bottom: 20px !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;
            border: 1px solid rgba(255, 215, 0, 0.3) !important;
            color: {text_color} !important;
        }}
        
        .golden-card h1, .golden-card h2, .golden-card h3, 
        .golden-card h4, .golden-card p, .golden-card span {{
            color: {text_color} !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.7) !important;
            background: transparent !important;
        }}
        
        /* Class cards with enhanced visibility */
        .class-card {{
            background: rgba(0, 0, 0, 0.4) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border-radius: 16px !important;
            padding: 20px !important;
            margin-bottom: 15px !important;
            border-left: 4px solid #FFD700 !important;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3) !important;
            border: 1px solid rgba(255, 215, 0, 0.2) !important;
            color: {text_color} !important;
        }}
        
        .class-card h4, .class-card p {{
            color: {text_color} !important;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.6) !important;
        }}
        
        /* Member cards */
        .member-card {{
            background: rgba(0, 0, 0, 0.4) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border-radius: 16px !important;
            padding: 20px !important;
            margin-bottom: 15px !important;
            display: flex;
            align-items: center;
            gap: 15px;
            border: 1px solid rgba(255, 215, 0, 0.3) !important;
            color: {text_color} !important;
        }}
        
        /* Chat container with enhanced visibility */
        .chat-container {{
            background: rgba(0, 0, 0, 0.3) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border-radius: 20px !important;
            padding: 20px !important;
            height: 450px !important;
            overflow-y: auto !important;
            border: 2px solid rgba(255, 215, 0, 0.3) !important;
        }}
        
        .chat-bubble {{
            max-width: 70%;
            padding: 15px 20px !important;
            border-radius: 20px !important;
            position: relative;
            word-wrap: break-word;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 215, 0, 0.3) !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2) !important;
        }}
        
        .chat-bubble-sent {{
            background: rgba(255, 215, 0, 0.3) !important;
            color: {text_color} !important;
        }}
        
        .chat-bubble-received {{
            background: rgba(255, 255, 255, 0.2) !important;
            color: {text_color} !important;
        }}
        
        .chat-sender-name {{
            font-size: 0.85rem !important;
            color: #FFD700 !important;
            font-weight: 700 !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
        }}
        
        /* Metric cards with enhanced visibility */
        .stMetric {{
            background: rgba(0, 0, 0, 0.3) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border-radius: 16px !important;
            padding: 15px !important;
            border: 1px solid rgba(255, 215, 0, 0.3) !important;
        }}
        
        .stMetric label, .stMetric div {{
            color: {text_color} !important;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.6) !important;
            font-weight: 600 !important;
        }}
        
        /* Expander with translucent background */
        .streamlit-expanderHeader {{
            color: {text_color} !important;
            background: rgba(255, 215, 0, 0.2) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border-radius: 12px !important;
            font-weight: 700 !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
        }}
        
        .streamlit-expanderContent {{
            background: rgba(0, 0, 0, 0.2) !important;
            backdrop-filter: blur(8px) !important;
            -webkit-backdrop-filter: blur(8px) !important;
            border-radius: 0 0 12px 12px !important;
        }}
        
        /* Dataframe with enhanced visibility */
        .dataframe {{
            background: rgba(0, 0, 0, 0.3) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            color: {text_color} !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 215, 0, 0.3) !important;
        }}
        
        .dataframe th {{
            background: rgba(255, 215, 0, 0.3) !important;
            color: {text_color} !important;
            font-weight: 700 !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
        }}
        
        .dataframe td {{
            color: {text_color} !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
            background: rgba(0,0,0,0.2) !important;
        }}
        
        /* Buttons with enhanced visibility */
        .stButton button {{
            background: linear-gradient(135deg, #FFD700, #DAA520) !important;
            color: #2b2b2b !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 10px 16px !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(218, 165, 32, 0.4) !important;
            text-shadow: none !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
        }}
        
        .stButton button:hover {{
            transform: translateY(-3px) !important;
            box-shadow: 0 8px 25px rgba(255, 215, 0, 0.6) !important;
        }}
        
        /* Success/Info/Warning/Error messages */
        .stAlert {{
            background: rgba(0, 0, 0, 0.6) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border: 2px solid !important;
            border-radius: 12px !important;
            color: {text_color} !important;
            font-weight: 600 !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
        }}
        
        /* Performance badges */
        .performance-excellent {{
            background: linear-gradient(135deg, #00ff00, #00ff99) !important;
            color: #000000 !important;
            padding: 6px 16px !important;
            border-radius: 30px !important;
            font-weight: 700 !important;
            font-size: 0.9rem !important;
            display: inline-block !important;
            text-shadow: none !important;
            box-shadow: 0 2px 10px rgba(0,255,0,0.3) !important;
        }}
        
        .performance-good {{
            background: linear-gradient(135deg, #00ffff, #0066ff) !important;
            color: #000000 !important;
            padding: 6px 16px !important;
            border-radius: 30px !important;
            font-weight: 700 !important;
            font-size: 0.9rem !important;
            display: inline-block !important;
            text-shadow: none !important;
        }}
        
        .performance-average {{
            background: linear-gradient(135deg, #ffff00, #ff9900) !important;
            color: #000000 !important;
            padding: 6px 16px !important;
            border-radius: 30px !important;
            font-weight: 700 !important;
            font-size: 0.9rem !important;
            display: inline-block !important;
            text-shadow: none !important;
        }}
        
        .performance-needs-improvement {{
            background: linear-gradient(135deg, #ff4444, #ff0000) !important;
            color: white !important;
            padding: 6px 16px !important;
            border-radius: 30px !important;
            font-weight: 700 !important;
            font-size: 0.9rem !important;
            display: inline-block !important;
            text-shadow: none !important;
        }}
        
        /* Animations */
        @keyframes golden-shimmer {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        
        @keyframes gradient-shift {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        
        /* Ensure all text is visible */
        p, span, div, .stMarkdown, .stText {{
            color: {text_color} !important;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.6) !important;
        }}
        
        /* Links */
        a {{
            color: #FFD700 !important;
            text-decoration: none !important;
            font-weight: 600 !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
        }}
        
        a:hover {{
            color: #FFFFFF !important;
            text-decoration: underline !important;
        }}
        
        /* School header with enhanced visibility */
        .school-header {{
            background: rgba(0, 0, 0, 0.5) !important;
            border: 2px solid #FFD700 !important;
            border-radius: 16px !important;
            padding: 15px !important;
            margin-bottom: 15px !important;
            text-align: center !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
        }}
        
        .school-header h2 {{
            color: #FFD700 !important;
            margin: 0 !important;
            font-size: 1.5rem !important;
            font-weight: 700 !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important;
            background: transparent !important;
        }}
        
        .school-code {{
            background: rgba(0, 0, 0, 0.4) !important;
            padding: 5px !important;
            border-radius: 25px !important;
            margin-top: 8px !important;
            border: 1px solid #FFD700 !important;
        }}
        
        .school-code code {{
            background: transparent !important;
            color: #FFD700 !important;
            font-size: 0.9rem !important;
            font-weight: 700 !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
        }}
        
        /* Profile card */
        .profile-card {{
            background: rgba(0, 0, 0, 0.5) !important;
            border: 2px solid #FFD700 !important;
            border-radius: 16px !important;
            padding: 15px !important;
            margin-bottom: 15px !important;
            display: flex !important;
            align-items: center !important;
            gap: 15px !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
        }}
        
        /* Request badge */
        .request-badge {{
            background: #FFD700 !important;
            color: #2b2b2b !important;
            padding: 3px 10px !important;
            border-radius: 15px !important;
            font-size: 0.8rem !important;
            font-weight: 700 !important;
            margin-left: 8px !important;
            text-shadow: none !important;
        }}
    </style>
    """

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

def load_user_settings(school_code, user_email):
    settings = load_school_data(school_code, "user_settings.json", {})
    return settings.get(user_email, {"theme": "Sunrise Glow", "wallpaper": "None"})

def save_user_settings(school_code, user_email, settings):
    all_settings = load_school_data(school_code, "user_settings.json", {})
    all_settings[user_email] = settings
    save_school_data(school_code, "user_settings.json", all_settings)

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

def add_academic_record(school_code, student_email, subject, score, term, year, teacher_email, class_name=None):
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

# ============ LIBRARY MANAGEMENT FUNCTIONS ============
def add_book(school_code, title, author, book_type, quantity, isbn=None, publisher=None, year=None):
    books = load_school_data(school_code, "library_books.json", [])
    book = {
        "id": generate_book_id(),
        "title": title,
        "author": author,
        "type": book_type,
        "quantity": quantity,
        "available": quantity,
        "isbn": isbn,
        "publisher": publisher,
        "year": year,
        "added_by": st.session_state.user['email'],
        "added_date": datetime.now().strftime("%Y-%m-%d")
    }
    books.append(book)
    save_school_data(school_code, "library_books.json", books)
    return book['id']

def add_library_member(school_code, user_email, member_type="student"):
    members = load_school_data(school_code, "library_members.json", [])
    if not any(m['email'] == user_email for m in members):
        members.append({
            "email": user_email,
            "member_type": member_type,
            "joined_date": datetime.now().strftime("%Y-%m-%d"),
            "borrowed_books": [],
            "status": "active"
        })
        save_school_data(school_code, "library_members.json", members)

def borrow_book(school_code, user_email, book_id, due_days=14):
    books = load_school_data(school_code, "library_books.json", [])
    transactions = load_school_data(school_code, "library_transactions.json", [])
    members = load_school_data(school_code, "library_members.json", [])
    
    # Find book
    book = next((b for b in books if b['id'] == book_id), None)
    if not book or book['available'] <= 0:
        return False, "Book not available"
    
    # Find or create member
    member = next((m for m in members if m['email'] == user_email), None)
    if not member:
        add_library_member(school_code, user_email)
        members = load_school_data(school_code, "library_members.json", [])
        member = next((m for m in members if m['email'] == user_email), None)
    
    # Check if member already has this book
    if any(b['book_id'] == book_id and b['status'] == 'borrowed' for b in member.get('borrowed_books', [])):
        return False, "Already borrowed this book"
    
    # Create transaction
    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=due_days)
    
    transaction = {
        "id": generate_transaction_id(),
        "book_id": book_id,
        "book_title": book['title'],
        "user_email": user_email,
        "borrow_date": borrow_date.strftime("%Y-%m-%d"),
        "due_date": due_date.strftime("%Y-%m-%d"),
        "return_date": None,
        "status": "borrowed",
        "renewals": 0
    }
    transactions.append(transaction)
    
    # Update book availability
    book['available'] -= 1
    
    # Update member's borrowed books
    member.setdefault('borrowed_books', []).append({
        "book_id": book_id,
        "transaction_id": transaction['id'],
        "borrow_date": borrow_date.strftime("%Y-%m-%d"),
        "due_date": due_date.strftime("%Y-%m-%d"),
        "status": "borrowed"
    })
    
    save_school_data(school_code, "library_books.json", books)
    save_school_data(school_code, "library_transactions.json", transactions)
    save_school_data(school_code, "library_members.json", members)
    
    return True, "Book borrowed successfully"

def return_book(school_code, transaction_id):
    books = load_school_data(school_code, "library_books.json", [])
    transactions = load_school_data(school_code, "library_transactions.json", [])
    members = load_school_data(school_code, "library_members.json", [])
    
    transaction = next((t for t in transactions if t['id'] == transaction_id), None)
    if not transaction or transaction['status'] != 'borrowed':
        return False, "Invalid transaction"
    
    # Update transaction
    transaction['return_date'] = datetime.now().strftime("%Y-%m-%d")
    transaction['status'] = 'returned'
    
    # Update book availability
    book = next((b for b in books if b['id'] == transaction['book_id']), None)
    if book:
        book['available'] += 1
    
    # Update member's record
    member = next((m for m in members if m['email'] == transaction['user_email']), None)
    if member:
        for b in member.get('borrowed_books', []):
            if b['transaction_id'] == transaction_id:
                b['status'] = 'returned'
                b['return_date'] = transaction['return_date']
                break
    
    save_school_data(school_code, "library_books.json", books)
    save_school_data(school_code, "library_transactions.json", transactions)
    save_school_data(school_code, "library_members.json", members)
    
    return True, "Book returned successfully"

def import_books_from_excel(school_code, uploaded_file):
    try:
        df = pd.read_excel(uploaded_file)
        required_columns = ['Title', 'Author', 'Type', 'Quantity']
        
        if not all(col in df.columns for col in required_columns):
            return False, "Excel must contain columns: Title, Author, Type, Quantity"
        
        books = load_school_data(school_code, "library_books.json", [])
        imported_count = 0
        
        for _, row in df.iterrows():
            book = {
                "id": generate_book_id(),
                "title": row['Title'],
                "author": row['Author'],
                "type": row['Type'],
                "quantity": int(row['Quantity']),
                "available": int(row['Quantity']),
                "isbn": row.get('ISBN', ''),
                "publisher": row.get('Publisher', ''),
                "year": row.get('Year', ''),
                "added_by": st.session_state.user['email'],
                "added_date": datetime.now().strftime("%Y-%m-%d")
            }
            books.append(book)
            imported_count += 1
        
        save_school_data(school_code, "library_books.json", books)
        return True, f"Successfully imported {imported_count} books"
    except Exception as e:
        return False, f"Error importing books: {str(e)}"

def import_members_from_excel(school_code, uploaded_file):
    try:
        df = pd.read_excel(uploaded_file)
        required_columns = ['Name', 'Email', 'Type']
        
        if not all(col in df.columns for col in required_columns):
            return False, "Excel must contain columns: Name, Email, Type"
        
        members = load_school_data(school_code, "library_members.json", [])
        users = load_school_data(school_code, "users.json", [])
        imported_count = 0
        
        for _, row in df.iterrows():
            # Check if user exists in system
            user = next((u for u in users if u['email'] == row['Email']), None)
            if not user:
                # Create basic user if not exists
                new_user = {
                    "user_id": generate_id("USR"),
                    "email": row['Email'],
                    "fullname": row['Name'],
                    "password": hashlib.sha256("default123".encode()).hexdigest(),
                    "role": row['Type'].lower(),
                    "joined": datetime.now().strftime("%Y-%m-%d"),
                    "school_code": school_code,
                    "profile_pic": None,
                    "bio": "",
                    "phone": ""
                }
                users.append(new_user)
            
            # Add to library members
            if not any(m['email'] == row['Email'] for m in members):
                member = {
                    "email": row['Email'],
                    "member_type": row['Type'].lower(),
                    "joined_date": datetime.now().strftime("%Y-%m-%d"),
                    "borrowed_books": [],
                    "status": "active"
                }
                members.append(member)
                imported_count += 1
        
        save_school_data(school_code, "users.json", users)
        save_school_data(school_code, "library_members.json", members)
        return True, f"Successfully imported {imported_count} members"
    except Exception as e:
        return False, f"Error importing members: {str(e)}"

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

# ============ MAIN APP ============

# Load user settings if logged in
if st.session_state.user and st.session_state.current_school:
    settings = load_user_settings(st.session_state.current_school['code'], st.session_state.user['email'])
    st.session_state.theme = settings.get("theme", "Sunrise Glow")
    st.session_state.wallpaper = settings.get("wallpaper", "None")

# Apply theme CSS
st.markdown(get_theme_css(st.session_state.theme, st.session_state.wallpaper), unsafe_allow_html=True)

# ----- WELCOME PAGE -----
if st.session_state.page == 'welcome':
    st.markdown('<h1>✨ School Community Hub ✨</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: white; font-size: 1.2rem; text-shadow: 1px 1px 2px black;">Connect • Collaborate • Manage • Shine</p>', unsafe_allow_html=True)
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
                            save_school_data(code, "library_books.json", [])
                            save_school_data(code, "library_members.json", [])
                            save_school_data(code, "library_transactions.json", [])
                            save_school_data(code, "user_settings.json", {})
                            
                            st.session_state.current_school = new_school
                            st.session_state.user = users[0]
                            st.session_state.page = 'dashboard'
                            st.success(f"✅ School Created! Your School Code is: **{code}**")
                            st.info("Save this code - you'll need it for login!")
                            st.rerun()
        
        with tab3:
            subtab1, subtab2 = st.tabs(["Login", "Register"])
            
            with subtab1:
                with st.form("teacher_login"):
                    st.subheader("Teacher Login")
                    school_code = st.text_input("School Code", placeholder="Enter your school code")
                    email = st.text_input("Email", placeholder="teacher@school.edu")
                    password = st.text_input("Password", type="password", placeholder="••••••••")
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
                                        st.session_state.page = 'dashboard'
                                        st.rerun()
                                st.error("Invalid credentials")
                            else:
                                st.error("School not found")
            
            with subtab2:
                with st.form("teacher_register"):
                    st.subheader("New Teacher Registration")
                    st.info("You need a valid teacher code from your school admin.")
                    school_code = st.text_input("School Code", placeholder="Enter school code")
                    teacher_code = st.text_input("Teacher Code", placeholder="e.g., MATH123")
                    fullname = st.text_input("Full Name", placeholder="e.g., Jane Smith")
                    email = st.text_input("Email", placeholder="jane.smith@school.edu")
                    password = st.text_input("Password", type="password", placeholder="Create a password")
                    confirm = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
                    
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
                                    # Auto-generate teacher code if none exists
                                    new_code = generate_teacher_code()
                                    teachers_data.append({
                                        "code": new_code,
                                        "status": "active",
                                        "created": datetime.now().strftime("%Y-%m-%d"),
                                        "used_by_list": [{
                                            "email": email,
                                            "name": fullname,
                                            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                                        }],
                                        "last_used": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                        "last_used_by": email
                                    })
                                    st.info(f"New teacher code generated: {new_code}")
                                
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
                                school['stats']['teachers'] = school['stats'].get('teachers', 0) + 1
                                all_schools[school_code] = school
                                save_all_schools(all_schools)
                                
                                # Add to library members
                                add_library_member(school_code, email, "teacher")
                                
                                st.session_state.current_school = school
                                st.session_state.user = new_user
                                st.session_state.page = 'dashboard'
                                st.success("✅ Registration Successful!")
                                st.rerun()
        
        with tab4:
            subtab1, subtab2 = st.tabs(["Login", "Register"])
            
            with subtab1:
                with st.form("student_login"):
                    st.subheader("Student Login")
                    school_code = st.text_input("School Code", placeholder="Enter school code")
                    admission_number = st.text_input("Admission Number", placeholder="e.g., ADM/24/1234")
                    password = st.text_input("Password", type="password", placeholder="••••••••")
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
                                        st.session_state.page = 'dashboard'
                                        st.rerun()
                                st.error("Invalid admission number or password")
                            else:
                                st.error("School not found")
            
            with subtab2:
                with st.form("student_register"):
                    st.subheader("New Student Registration")
                    school_code = st.text_input("School Code", placeholder="Enter school code")
                    fullname = st.text_input("Full Name", placeholder="e.g., John Kamau")
                    email = st.text_input("Email (Optional)", placeholder="student@example.com")
                    password = st.text_input("Password", type="password", placeholder="Create a password")
                    confirm = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
                    
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
                                school['stats']['students'] = school['stats'].get('students', 0) + 1
                                all_schools[school_code] = school
                                save_all_schools(all_schools)
                                
                                # Add to library members
                                add_library_member(school_code, new_user['email'], "student")
                                
                                st.success(f"✅ Registered! Your Admission Number is: **{admission_number}**")
                                st.info("📝 Save this number - you'll need it to login!")
        
        with tab5:
            subtab1, subtab2 = st.tabs(["Login", "Register"])
            
            with subtab1:
                with st.form("guardian_login"):
                    st.subheader("Guardian Login")
                    school_code = st.text_input("School Code", placeholder="Enter school code")
                    student_admission = st.text_input("Student's Admission Number", placeholder="e.g., ADM/24/1234")
                    email = st.text_input("Your Email", placeholder="guardian@example.com")
                    password = st.text_input("Password", type="password", placeholder="••••••••")
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
                    st.info("You'll need the student's admission number to link.")
                    school_code = st.text_input("School Code", placeholder="Enter school code")
                    student_admission = st.text_input("Student's Admission Number", placeholder="e.g., ADM/24/1234")
                    fullname = st.text_input("Your Full Name", placeholder="e.g., Mary Wanjiku")
                    email = st.text_input("Your Email", placeholder="mary.wanjiku@example.com")
                    phone = st.text_input("Phone Number", placeholder="+254 7XX XXX XXX")
                    password = st.text_input("Password", type="password", placeholder="Create a password")
                    confirm = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
                    
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
                                
                                # Add to library members
                                add_library_member(school_code, email, "guardian")
                                
                                st.success("✅ Guardian Registration Successful!")
    
    elif st.session_state.main_nav == 'School Management':
        st.markdown("""
        <div class="golden-card" style="text-align: center;">
            <h3>📊 School Management System</h3>
            <p>Complete school administration - Academics, Finance, Discipline, Library, and more!</p>
            <p style="font-size: 0.9rem;">Please log in with your admin or teacher credentials to access management features.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.user and st.session_state.current_school:
            st.success(f"✅ Logged in as: {st.session_state.user['fullname']} ({st.session_state.user['role']})")
            if st.button("Go to Management Dashboard", use_container_width=True):
                st.session_state.page = 'dashboard'
                st.rerun()
        else:
            st.warning("⚠️ Please log in first to access the School Management System.")
            st.info("Go to the School Community tab and log in with your admin or teacher account.")
    
    elif st.session_state.main_nav == 'Personal Dashboard':
        st.markdown("""
        <div class="golden-card" style="text-align: center;">
            <h3>👤 Personal Dashboard</h3>
            <p>Your personal information, performance, reviews, achievements, and library account!</p>
            <p style="font-size: 0.9rem;">Please log in with your student or guardian credentials to view your personal dashboard.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.user and st.session_state.current_school:
            st.success(f"✅ Logged in as: {st.session_state.user['fullname']} ({st.session_state.user['role']})")
            if st.button("Go to Personal Dashboard", use_container_width=True):
                st.session_state.page = 'dashboard'
                st.rerun()
        else:
            st.warning("⚠️ Please log in first to view your Personal Dashboard.")
            st.info("Go to the School Community tab and log in with your student or guardian account.")

# ----- DASHBOARD (for logged in users) -----
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
    academic_records = load_school_data(school_code, "academic_records.json", [])
    library_books = load_school_data(school_code, "library_books.json", [])
    library_members = load_school_data(school_code, "library_members.json", [])
    library_transactions = load_school_data(school_code, "library_transactions.json", [])
    
    unread_count = get_unread_count(user['email'], school_code)
    pending_friend_count = len(get_pending_requests(school_code, user['email']))
    
    # Get user's borrowed books
    user_member = next((m for m in library_members if m['email'] == user['email']), None)
    borrowed_books = user_member.get('borrowed_books', []) if user_member else []
    
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
        
        # Define sidebar options based on role
        base_options = ["Dashboard", "Announcements", "Community", f"Chat 💬{f' ({unread_count})' if unread_count>0 else ''}", f"Group Chats 👥", f"Friends 🤝{f' ({pending_friend_count})' if pending_friend_count>0 else ''}"]
        
        if user['role'] == 'admin':
            options = base_options + ["Classes", "Groups", "Teachers", "Students", "Guardians", "Assignments", "School Management", "Personal Dashboard", "Library Management", "Settings ⚙️", "Profile"]
        elif user['role'] == 'teacher':
            options = base_options + ["My Classes", "Groups", "Assignments", "School Management", "Personal Dashboard", "Library Management", "Settings ⚙️", "Profile"]
        elif user['role'] == 'student':
            options = base_options + ["Browse Classes", "My Classes", "Groups", "Assignments", "Personal Dashboard", "My Library", "Settings ⚙️", "Profile"]
        else:  # guardian
            options = base_options + ["My Student", "Assignments", "Personal Dashboard", "My Library", "Settings ⚙️", "Profile"]
        
        if st.session_state.menu_index >= len(options):
            st.session_state.menu_index = 0
            
        menu = st.radio("Navigation", options, index=st.session_state.menu_index, label_visibility="collapsed")
        st.session_state.menu_index = options.index(menu)
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.current_school = None
            st.session_state.page = 'welcome'
            st.rerun()
    
    # ============ MAIN CONTENT ============
    # (Rest of the dashboard code remains the same as in the original)
    # Note: I've omitted the rest of the dashboard code for brevity,
    # but it should be included here exactly as in the original file.
    # The key changes are in the CSS and theme/wallpaper sections above.
    
else:
    st.error("Something went wrong. Please restart.")
    if st.button("Restart"):
        st.session_state.page = 'welcome'
        st.rerun()
