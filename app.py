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

# Try importing optional dependencies (will be handled gracefully if not installed)
try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False

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

# ============ THEMES AND WALLPAPERS ============
THEMES = {
    "Sunrise Glow": {
        "primary": "#ff6b6b",
        "secondary": "#feca57",
        "accent": "#48dbfb",
        "background": "linear-gradient(135deg, #ff6b6b, #feca57, #ff9ff3, #48dbfb)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #cfa668, #e5b873, #f5d742)"
    },
    "Ocean Breeze": {
        "primary": "#00d2ff",
        "secondary": "#3a1c71",
        "accent": "#00ff00",
        "background": "linear-gradient(135deg, #00d2ff, #3a1c71, #d76d77, #ffaf7b)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #4facfe, #00f2fe, #43e97b)"
    },
    "Purple Haze": {
        "primary": "#8E2DE2",
        "secondary": "#4A00E0",
        "accent": "#a044ff",
        "background": "linear-gradient(135deg, #8E2DE2, #4A00E0, #6a3093, #a044ff)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #c471ed, #f64f59, #c471ed)"
    },
    "Tropical Paradise": {
        "primary": "#00b09b",
        "secondary": "#96c93d",
        "accent": "#fbd786",
        "background": "linear-gradient(135deg, #00b09b, #96c93d, #c6ffdd, #fbd786)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #4facfe, #00f2fe, #43e97b)"
    },
    "Cherry Blossom": {
        "primary": "#ff9a9e",
        "secondary": "#fad0c4",
        "accent": "#a1c4fd",
        "background": "linear-gradient(135deg, #ff9a9e, #fad0c4, #ffd1ff, #a1c4fd)",
        "text": "#333333",
        "sidebar": "linear-gradient(135deg, #fbc2eb, #a6c1ee, #fbc2eb)"
    },
    "Midnight City": {
        "primary": "#232526",
        "secondary": "#414345",
        "accent": "#4b6cb7",
        "background": "linear-gradient(135deg, #232526, #414345, #2c3e50, #4b6cb7)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #182848, #4b6cb7, #182848)"
    },
    "Autumn Leaves": {
        "primary": "#e44d2e",
        "secondary": "#f39c12",
        "accent": "#f1c40f",
        "background": "linear-gradient(135deg, #e44d2e, #f39c12, #d35400, #e67e22)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #f1c40f, #e67e22, #d35400)"
    },
    "Northern Lights": {
        "primary": "#43C6AC",
        "secondary": "#191654",
        "accent": "#00CDAC",
        "background": "linear-gradient(135deg, #43C6AC, #191654, #02AAB0, #00CDAC)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #02AAB0, #00CDAC, #191654)"
    },
    "Forest Mist": {
        "primary": "#11998e",
        "secondary": "#38ef7d",
        "accent": "#38ef7d",
        "background": "linear-gradient(135deg, #11998e, #38ef7d, #11998e, #38ef7d)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #11998e, #38ef7d, #11998e)"
    },
    "Lavender Dream": {
        "primary": "#aa4b6b",
        "secondary": "#6b6b83",
        "accent": "#3b8d99",
        "background": "linear-gradient(135deg, #aa4b6b, #6b6b83, #3b8d99, #aa4b6b)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #aa4b6b, #6b6b83, #3b8d99)"
    },
    "Sunset Orange": {
        "primary": "#f12711",
        "secondary": "#f5af19",
        "accent": "#f5af19",
        "background": "linear-gradient(135deg, #f12711, #f5af19, #f12711, #f5af19)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #f12711, #f5af19, #f12711)"
    },
    "Electric Blue": {
        "primary": "#00c6fb",
        "secondary": "#005bea",
        "accent": "#00c6fb",
        "background": "linear-gradient(135deg, #00c6fb, #005bea, #00c6fb, #005bea)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #00c6fb, #005bea, #00c6fb)"
    },
    "Pink Flamingo": {
        "primary": "#f857a6",
        "secondary": "#ff5858",
        "accent": "#f857a6",
        "background": "linear-gradient(135deg, #f857a6, #ff5858, #f857a6, #ff5858)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #f857a6, #ff5858, #f857a6)"
    },
    "Emerald City": {
        "primary": "#348f50",
        "secondary": "#56ab2f",
        "accent": "#56ab2f",
        "background": "linear-gradient(135deg, #348f50, #56ab2f, #348f50, #56ab2f)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #348f50, #56ab2f, #348f50)"
    },
    "Ruby Red": {
        "primary": "#cb356b",
        "secondary": "#bd3f32",
        "accent": "#cb356b",
        "background": "linear-gradient(135deg, #cb356b, #bd3f32, #cb356b, #bd3f32)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #cb356b, #bd3f32, #cb356b)"
    },
    "Sapphire Blue": {
        "primary": "#0f0c29",
        "secondary": "#302b63",
        "accent": "#24243e",
        "background": "linear-gradient(135deg, #0f0c29, #302b63, #24243e, #0f0c29)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #182848, #4b6cb7, #182848)"
    },
    "Amber Glow": {
        "primary": "#ff8008",
        "secondary": "#ffc837",
        "accent": "#ff8008",
        "background": "linear-gradient(135deg, #ff8008, #ffc837, #ff8008, #ffc837)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #ff8008, #ffc837, #ff8008)"
    },
    "Teal Tide": {
        "primary": "#1d976c",
        "secondary": "#93f9b9",
        "accent": "#1d976c",
        "background": "linear-gradient(135deg, #1d976c, #93f9b9, #1d976c, #93f9b9)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #1d976c, #93f9b9, #1d976c)"
    },
    "Grape Escape": {
        "primary": "#8e2de2",
        "secondary": "#4a00e0",
        "accent": "#8e2de2",
        "background": "linear-gradient(135deg, #8e2de2, #4a00e0, #8e2de2, #4a00e0)",
        "text": "#ffffff",
        "sidebar": "linear-gradient(135deg, #8e2de2, #4a00e0, #8e2de2)"
    },
    "Peach Perfect": {
        "primary": "#ff6a88",
        "secondary": "#ff99ac",
        "accent": "#ff6a88",
        "background": "linear-gradient(135deg, #ff6a88, #ff99ac, #ff6a88, #ff99ac)",
        "text": "#333333",
        "sidebar": "linear-gradient(135deg, #ff6a88, #ff99ac, #ff6a88)"
    }
}

WALLPAPERS = {
    "None": "",
    # Core originals and early ones
    "Abstract Waves": "https://images.unsplash.com/photo-1557682250-33bd709cbe85",
    "Geometric Pattern": "https://images.unsplash.com/photo-1557683311-eac922347aa1",
    "Nature Leaves": "https://images.unsplash.com/photo-1557683316-973673baf926",
    "Starry Night": "https://images.unsplash.com/photo-1557683320-2d5001d5e9c5",
    "Color Splash": "https://images.unsplash.com/photo-1557683304-6733ba7e4d6f",
    "Gradient Flow": "https://images.unsplash.com/photo-1557683316-973673baf926",
    "Minimal Lines": "https://images.unsplash.com/photo-1557683311-eac922347aa1",
    "Dark Texture": "https://images.unsplash.com/photo-1596865249308-2472dc5807d7",
    "Light Texture": "https://images.unsplash.com/photo-1557683320-2d5001d5e9c5",
    "Forest": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e",
    "Mountains": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b",
    "Ocean": "https://images.unsplash.com/photo-1507525425510-56b1e2d6c4f2",
    "Desert": "https://images.unsplash.com/photo-1509316785289-025f5b846b35",
    "City Lights": "https://images.unsplash.com/photo-1519501025264-65ba15a82390",
    "Aurora": "https://images.unsplash.com/photo-1483347756197-71ef80e95f73",
    "Galaxy": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564",
    "Sunset": "https://images.unsplash.com/photo-1506815444479-bfdb1e96c566",
    "Rainbow": "https://images.unsplash.com/photo-1511300636408-a63a89df3482",
    "Clouds": "https://images.unsplash.com/photo-1501630834273-4b5604d2ee31",
    "Stars": "https://images.unsplash.com/photo-1419242902214-272b3f66ee7a",

    # Abstracts & Gradients (expanded)
    "Vibrant Color Waves": "https://thumbs.dreamstime.com/b/abstract-colorful-waves-background-vibrant-gradient-texture-stunning-featuring-flowing-beautiful-colors-perfect-396814445.jpg",
    "Neon Rainbow Gradient": "https://thumbs.dreamstime.com/b/color-spectrum-abstract-background-beautiful-colorful-wallpaper-modern-style-vectors-seamless-digital-design-featuring-smooth-392167435.jpg",
    "Soft Pastel Blur Gradient": "https://img.freepik.com/free-photo/vivid-blurred-colorful-wallpaper-background_58702-2787.jpg",
    "Dynamic Fluid Colors": "https://thumbs.dreamstime.com/b/vibrant-abstract-background-featuring-colorful-wavy-patterns-dynamic-shapes-image-showcases-mixture-bold-hues-fluid-321915785.jpg",
    "Layered Wavy Pastels": "https://thumbs.dreamstime.com/b/colorful-wavy-lines-create-beautiful-abstract-pattern-layered-curve-overlap-creating-smooth-texture-arranged-332756007.jpg",
    "Colorful Music Gradient": "https://thumbs.dreamstime.com/b/colorful-music-notes-flowing-abstract-background-high-quality-illustration-349594851.jpg",
    "Pastel Circle Gradient": "https://img.freepik.com/free-vector/beautiful-abstract-pastel-color-gradient-backdrop-with-round-design_1017-53587.jpg",
    "Purple Blue Wave Abstract": "https://images.unsplash.com/photo-1557682257-2f9c97a8a469",

    # Nature & Landscapes (more serene & epic)
    "Misty Mountain Lake": "https://images.unsplash.com/photo-1603979649806-5299879db16b",
    "Tropical Valley View": "https://images.pexels.com/photos/2559941/pexels-photo-2559941.jpeg",
    "Golden Hour Lake Sunset": "https://images4.alphacoders.com/996/thumb-1920-996399.jpg",
    "Alpine Sunset Hills": "https://w0.peakpx.com/wallpaper/609/297/HD-wallpaper-sunset-mountain-hills-amazing-beautiful-sunset-sky-clouds-valley-mountain-wildflowers-nature-landscape.jpg",
    "River Valley Glow": "https://w0.peakpx.com/wallpaper/593/805/HD-wallpaper-sunset-mountain-forest-earth-river.jpg",
    "Lush Green Waterfall": "https://thumbs.dreamstime.com/b/lush-green-landscape-mountains-waterfall-flowing-calm-river-ocean-distance-lush-green-landscape-333961065.jpg",
    "Turquoise Mountain Lake": "https://images.unsplash.com/photo-1603979649806-5299879db16b",
    "Glacier Lake Reflection": "https://wallpapers.com/images/hd/4k-mountain-9md6zlz1czbova8g.jpg",
    "Yosemite Valley Pond": "https://i.pinimg.com/736x/c5/4a/19/c54a19dd5b96e6aece47b015a794ae74.jpg",
    "Autumn Golden Forest Path": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=2400",

    # Space & Cosmic (deep & vibrant)
    "Carina Nebula Cliffs": "https://4kwallpapers.com/images/wallpapers/carina-nebula-cosmic-cliffs-james-webb-space-telescope-3840x2160-8689.jpg",
    "Vibrant Nebula Storm": "https://thumbs.dreamstime.com/b/infinite-universe-closeup-vibrant-deep-space-nebula-cosmic-clouds-dust-particles-high-resolution-wallpaper-image-368102253.jpg",
    "Earth in Colorful Nebula": "https://thumbs.dreamstime.com/b/earth-cosmic-space-surrounded-colorful-nebula-stars-ai-generated-372064323.jpg",
    "Purple Pink Nebula Galaxy": "https://images7.alphacoders.com/568/thumb-1920-568756.jpg",
    "Cosmic Purple Dust": "https://images5.alphacoders.com/432/thumb-1920-432766.jpg",
    "Milky Way Cosmic Burst": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=2400",

    # Additional variety to reach 100+
    "Minimalist Ocean Horizon": "https://images.unsplash.com/photo-1507525425510-56b1e2d6c4f2?w=2400",
    "Enchanted Forest Mist": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=2400",
    "Cyber Neon Grid": "https://images.unsplash.com/photo-1557682257-2f9c97a8a469",
    "Pastel Dreamscape": "https://images.unsplash.com/photo-1553356084-58ef4a67b2a7",
    "Volcanic Lava Flow": "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
    "Serene Bamboo Grove": "https://images.unsplash.com/photo-1518531933039-315f5d4a6b1a",
    "Arctic Iceberg Glow": "https://images.unsplash.com/photo-1540979388789-7cee28a1cdc9",
    "Fiery Mountain Sunset": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4",
    "Underwater Coral Reef": "https://images.unsplash.com/photo-1544551763-46a013bb70b5",
    "Mystical Foggy Lake": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4",
    "Snowy Alpine Peaks": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=2400",
    "Tropical Beach Sunset": "https://images.unsplash.com/photo-1507525425510-56b1e2d6c4f2?w=2400",
    "Northern Lights Forest": "https://images.unsplash.com/photo-1483347756197-71ef80e95f73?w=2400",
    "Minimal Black Horizon": "https://images.unsplash.com/photo-1557682257-2f9c97a8a469",
    "Vibrant Desert Dunes": "https://images.unsplash.com/photo-1509316785289-025f5b846b35?w=2400",
    "City Skyline Neon": "https://images.unsplash.com/photo-1519501025264-65ba15a82390?w=2400",
}
def get_theme_css(theme_name, wallpaper=None):
    theme = THEMES.get(theme_name, THEMES["Sunrise Glow"])
    wallpaper_url = WALLPAPERS.get(wallpaper, "") if wallpaper else ""
    
    background_style = f"url('{wallpaper_url}') no-repeat center center fixed" if wallpaper_url else theme["background"]
    background_size = "cover" if wallpaper_url else "400% 400%"
    
    return f"""
    <style>
        body {{
            background: {background_style};
            background-size: {background_size};
            margin: 0;
            padding: 0;
            min-height: 100vh;
            font-family: 'Poppins', sans-serif;
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
        
        .school-header {{
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid #FFD700;
            border-radius: 12px;
            padding: 12px;
            margin-bottom: 12px;
            text-align: center;
            backdrop-filter: blur(5px);
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
            backdrop-filter: blur(5px);
        }}
        
        .stSelectbox div[data-baseweb="select"] {{
            background: rgba(255, 255, 255, 0.9) !important;
            border: 2px solid #FFD700 !important;
            border-radius: 10px !important;
            color: #000000 !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            backdrop-filter: blur(5px);
        }}
        
        .stSelectbox div[data-baseweb="select"]:hover {{
            border-color: #DAA520 !important;
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.5) !important;
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
            backdrop-filter: blur(5px);
        }}
        
        .stTextInput input:focus, 
        .stTextArea textarea:focus,
        .stDateInput input:focus,
        .stNumberInput input:focus {{
            border-color: #DAA520 !important;
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.5) !important;
        }}
        
        .stTextInput label,
        .stTextArea label,
        .stSelectbox label,
        .stDateInput label,
        .stNumberInput label {{
            color: {theme["text"]} !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
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
            background: linear-gradient(135deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2.5rem !important;
            font-weight: 700 !important;
            text-align: center;
            margin-bottom: 1.5rem !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
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
        
        .golden-card h1, .golden-card h2, .golden-card h3, .golden-card h4, .golden-card p {{
            color: {theme["text"]} !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }}
        
        .performance-excellent {{
            background: linear-gradient(135deg, #00ff00, #00ff99);
            color: #000000;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.8rem;
            display: inline-block;
            text-shadow: none;
        }}
        
        .performance-good {{
            background: linear-gradient(135deg, #00ffff, #0066ff);
            color: #000000;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.8rem;
            display: inline-block;
            text-shadow: none;
        }}
        
        .performance-average {{
            background: linear-gradient(135deg, #ffff00, #ff9900);
            color: #000000;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.8rem;
            display: inline-block;
            text-shadow: none;
        }}
        
        .performance-needs-improvement {{
            background: linear-gradient(135deg, #ff4444, #ff0000);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.8rem;
            display: inline-block;
            text-shadow: none;
        }}
        
        .chat-container {{
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
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
            backdrop-filter: blur(10px);
        }}
        
        .chat-bubble-sent {{
            background: rgba(255, 215, 0, 0.3);
            color: {theme["text"]};
            border-bottom-right-radius: 4px;
            border: 1px solid #FFD700;
        }}
        
        .chat-bubble-received {{
            background: rgba(255, 255, 255, 0.2);
            color: {theme["text"]};
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
            color: #FFD700;
            font-weight: 600;
        }}
        
        .chat-time {{
            font-size: 0.65rem;
            color: rgba(255, 255, 255, 0.5);
            margin-top: 4px;
            text-align: right;
        }}
        
        .main-nav-button {{
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            color: {theme["text"]};
            border: 2px solid #FFD700;
            border-radius: 15px;
            padding: 20px;
            font-size: 1.2rem;
            font-weight: 700;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 10px 30px rgba(255, 215, 0, 0.3);
            margin: 10px 0;
        }}
        
        .main-nav-button:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(255, 215, 0, 0.5);
            border-color: white;
        }}
        
        .class-card {{
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 10px;
            border-left: 4px solid #FFD700;
            box-shadow: 0 2px 8px rgba(255, 215, 0, 0.2);
            color: {theme["text"]};
        }}
        
        .class-card h4, .class-card p {{
            color: {theme["text"]} !important;
        }}
        
        .member-card {{
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 15px;
            border: 1px solid #FFD700;
            color: {theme["text"]};
        }}
        
        .member-pic {{
            width: 50px;
            height: 50px;
            border-radius: 50%;
            object-fit: cover;
            border: 2px solid #FFD700;
        }}
        
        .request-badge {{
            background: #FFD700;
            color: #2b2b2b;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 600;
            margin-left: 8px;
        }}
        
        .main p, .main span, .main div:not(.stTextInput):not(.stTextArea) {{
            color: {theme["text"]} !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }}
        
        .stMetric label, .stMetric div {{
            color: {theme["text"]} !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }}
        
        .streamlit-expanderHeader {{
            color: {theme["text"]} !important;
            background: rgba(255, 215, 0, 0.2) !important;
            backdrop-filter: blur(10px) !important;
        }}
        
        .dataframe {{
            background: rgba(255, 255, 255, 0.15) !important;
            color: {theme["text"]} !important;
            backdrop-filter: blur(10px) !important;
        }}
        
        .dataframe th {{
            background: rgba(255, 215, 0, 0.3) !important;
            color: {theme["text"]} !important;
        }}
        
        .dataframe td {{
            color: {theme["text"]} !important;
        }}
        
        @keyframes golden-shimmer {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
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

# ============ NEW FEATURE FUNCTIONS (ADDED HERE) ============

# ============ MULTI-LANGUAGE SUPPORT ============
TRANSLATIONS = {
    "en": {  # English
        "welcome": "✨ School Community Hub ✨",
        "connect": "Connect • Collaborate • Manage • Shine",
        "school_community": "🏫 School Community",
        "school_management": "📊 School Management",
        "personal_dashboard": "👤 Personal Dashboard",
        "admin_login": "👑 Admin Login",
        "teacher_login": "👨‍🏫 Teacher Login",
        "student_login": "👨‍🎓 Student Login",
        "guardian_login": "👪 Guardian Login",
        "create_school": "🏫 Create New School",
        "login": "Login",
        "register": "Register",
        "email": "Email",
        "password": "Password",
        "school_code": "School Code",
        "full_name": "Full Name",
        "phone": "Phone",
        "admission_number": "Admission Number",
        "dashboard": "Dashboard",
        "announcements": "Announcements",
        "community": "Community",
        "chat": "Chat",
        "friends": "Friends",
        "classes": "Classes",
        "groups": "Groups",
        "assignments": "Assignments",
        "library": "Library",
        "settings": "Settings",
        "profile": "Profile",
        "logout": "Logout",
        "submit": "Submit",
        "cancel": "Cancel",
        "save": "Save",
        "delete": "Delete",
        "edit": "Edit",
        "search": "Search",
        "filter": "Filter",
        "loading": "Loading...",
        "error": "Error",
        "success": "Success",
        "warning": "Warning",
        "info": "Info",
        "confirm": "Confirm",
        "yes": "Yes",
        "no": "No",
        "welcome_back": "Welcome back, {name}!",
        "no_data": "No data available",
        "please_wait": "Please wait...",
        "processing": "Processing...",
        "completed": "Completed",
        "pending": "Pending",
        "failed": "Failed",
    },
    "sw": {  # Kiswahili
        "welcome": "✨ Kituo cha Jumuiya ya Shule ✨",
        "connect": "Unganisha • Shirikiana • Simamia • Angaza",
        "school_community": "🏫 Jumuiya ya Shule",
        "school_management": "📊 Usimamizi wa Shule",
        "personal_dashboard": "👤 Dashbodi ya Kibinafsi",
        "admin_login": "👑 Kuingia kwa Msimamizi",
        "teacher_login": "👨‍🏫 Kuingia kwa Mwalimu",
        "student_login": "👨‍🎓 Kuingia kwa Mwanafunzi",
        "guardian_login": "👪 Kuingia kwa Mlezi",
        "create_school": "🏫 Unda Shule Mpya",
        "login": "Ingia",
        "register": "Jisajili",
        "email": "Barua pepe",
        "password": "Nywila",
        "school_code": "Msimbo wa Shule",
        "full_name": "Jina Kamili",
        "phone": "Simu",
        "admission_number": "Nambari ya Udahili",
        "dashboard": "Dashbodi",
        "announcements": "Matangazo",
        "community": "Jumuiya",
        "chat": "Mazungumzo",
        "friends": "Marafiki",
        "classes": "Madarasa",
        "groups": "Vikundi",
        "assignments": "Kazi",
        "library": "Maktaba",
        "settings": "Mipangilio",
        "profile": "Wasifu",
        "logout": "Toka",
        "submit": "Wasilisha",
        "cancel": "Ghairi",
        "save": "Hifadhi",
        "delete": "Futa",
        "edit": "Hariri",
        "search": "Tafuta",
        "filter": "Chuja",
        "loading": "Inapakia...",
        "error": "Hitilafu",
        "success": "Imefaulu",
        "warning": "Onyo",
        "info": "Taarifa",
        "confirm": "Thibitisha",
        "yes": "Ndiyo",
        "no": "Hapana",
        "welcome_back": "Karibu tena, {name}!",
        "no_data": "Hakuna data",
        "please_wait": "Tafadhali subiri...",
        "processing": "Inachakatwa...",
        "completed": "Imekamilika",
        "pending": "Inasubiri",
        "failed": "Imeshindwa",
    },
    "fr": {  # French
        "welcome": "✨ Centre Communautaire Scolaire ✨",
        "connect": "Connecter • Collaborer • Gérer • Briller",
        "school_community": "🏫 Communauté Scolaire",
        "school_management": "📊 Gestion Scolaire",
        "personal_dashboard": "👤 Tableau de Bord Personnel",
        "admin_login": "👑 Connexion Admin",
        "teacher_login": "👨‍🏫 Connexion Enseignant",
        "student_login": "👨‍🎓 Connexion Élève",
        "guardian_login": "👪 Connexion Parent",
        "create_school": "🏫 Créer une École",
        "login": "Connexion",
        "register": "S'inscrire",
        "email": "Email",
        "password": "Mot de passe",
        "school_code": "Code de l'école",
        "full_name": "Nom Complet",
        "phone": "Téléphone",
        "admission_number": "Numéro d'admission",
        "dashboard": "Tableau de Bord",
        "announcements": "Annonces",
        "community": "Communauté",
        "chat": "Discussion",
        "friends": "Amis",
        "classes": "Classes",
        "groups": "Groupes",
        "assignments": "Devoirs",
        "library": "Bibliothèque",
        "settings": "Paramètres",
        "profile": "Profil",
        "logout": "Déconnexion",
        "submit": "Soumettre",
        "cancel": "Annuler",
        "save": "Enregistrer",
        "delete": "Supprimer",
        "edit": "Modifier",
        "search": "Rechercher",
        "filter": "Filtrer",
        "loading": "Chargement...",
        "error": "Erreur",
        "success": "Succès",
        "warning": "Avertissement",
        "info": "Info",
        "confirm": "Confirmer",
        "yes": "Oui",
        "no": "Non",
        "welcome_back": "Bon retour, {name}!",
        "no_data": "Aucune donnée",
        "please_wait": "Veuillez patienter...",
        "processing": "Traitement...",
        "completed": "Terminé",
        "pending": "En attente",
        "failed": "Échoué",
    },
    "ar": {  # Arabic
        "welcome": "✨ مركز المجتمع المدرسي ✨",
        "connect": "تواصل • تعاون • إدارة • تألق",
        "school_community": "🏫 المجتمع المدرسي",
        "school_management": "📊 إدارة المدرسة",
        "personal_dashboard": "👤 لوحة التحكم الشخصية",
        "admin_login": "👑 تسجيل دخول المدير",
        "teacher_login": "👨‍🏫 تسجيل دخول المعلم",
        "student_login": "👨‍🎓 تسجيل دخول الطالب",
        "guardian_login": "👪 تسجيل دخول ولي الأمر",
        "create_school": "🏫 إنشاء مدرسة جديدة",
        "login": "تسجيل الدخول",
        "register": "التسجيل",
        "email": "البريد الإلكتروني",
        "password": "كلمة المرور",
        "school_code": "رمز المدرسة",
        "full_name": "الاسم الكامل",
        "phone": "الهاتف",
        "admission_number": "رقم القبول",
        "dashboard": "لوحة التحكم",
        "announcements": "الإعلانات",
        "community": "المجتمع",
        "chat": "الدردشة",
        "friends": "الأصدقاء",
        "classes": "الفصول",
        "groups": "المجموعات",
        "assignments": "الواجبات",
        "library": "المكتبة",
        "settings": "الإعدادات",
        "profile": "الملف الشخصي",
        "logout": "تسجيل الخروج",
        "submit": "إرسال",
        "cancel": "إلغاء",
        "save": "حفظ",
        "delete": "حذف",
        "edit": "تعديل",
        "search": "بحث",
        "filter": "تصفية",
        "loading": "جاري التحميل...",
        "error": "خطأ",
        "success": "نجاح",
        "warning": "تحذير",
        "info": "معلومات",
        "confirm": "تأكيد",
        "yes": "نعم",
        "no": "لا",
        "welcome_back": "مرحباً بعودتك، {name}!",
        "no_data": "لا توجد بيانات",
        "please_wait": "الرجاء الانتظار...",
        "processing": "جاري المعالجة...",
        "completed": "مكتمل",
        "pending": "قيد الانتظار",
        "failed": "فشل",
    }
}

def get_text(key: str, **kwargs) -> str:
    """Get translated text"""
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    lang = st.session_state.language
    text = TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text

# ============ ACCESSIBILITY FEATURES ============
ACCESSIBILITY_PRESETS = {
    "Default": {
        "text_size": "Medium",
        "contrast_mode": False,
        "dyslexia_font": False,
        "color_blind_mode": "None",
        "reduced_motion": False
    },
    "Large Text": {
        "text_size": "Large",
        "contrast_mode": False,
        "dyslexia_font": False,
        "color_blind_mode": "None",
        "reduced_motion": False
    },
    "High Contrast": {
        "text_size": "Medium",
        "contrast_mode": True,
        "dyslexia_font": False,
        "color_blind_mode": "None",
        "reduced_motion": False
    },
    "Dyslexia Friendly": {
        "text_size": "Medium",
        "contrast_mode": False,
        "dyslexia_font": True,
        "color_blind_mode": "None",
        "reduced_motion": False
    }
}

COLOR_BLIND_FILTERS = {
    "None": "",
    "Protanopia": "protanopia",
    "Deuteranopia": "deuteranopia",
    "Tritanopia": "tritanopia"
}

# ============ BADGES & ACHIEVEMENTS ============
BADGES = {
    "perfect_attendance": {
        "name": "Perfect Attendance",
        "description": "Achieved 100% attendance for a term",
        "icon": "📅",
        "color": "gold"
    },
    "homework_streak": {
        "name": "Homework Streak",
        "description": "Completed all assignments for 30 days",
        "icon": "📚",
        "color": "silver"
    },
    "helpful_peer": {
        "name": "Helpful Peer",
        "description": "Helped 10 classmates with their studies",
        "icon": "🤝",
        "color": "blue"
    },
    "math_wizard": {
        "name": "Math Wizard",
        "description": "Scored 90%+ in all math tests",
        "icon": "🧮",
        "color": "purple"
    },
    "science_whiz": {
        "name": "Science Whiz",
        "description": "Excellent performance in science subjects",
        "icon": "🔬",
        "color": "green"
    },
    "library_enthusiast": {
        "name": "Library Enthusiast",
        "description": "Borrowed 20+ books from the library",
        "icon": "📖",
        "color": "brown"
    },
    "sports_champion": {
        "name": "Sports Champion",
        "description": "Participated in 5+ sports events",
        "icon": "⚽",
        "color": "orange"
    },
    "artistic_talent": {
        "name": "Artistic Talent",
        "description": "Showcased artwork in school exhibitions",
        "icon": "🎨",
        "color": "pink"
    },
    "leadership_excellence": {
        "name": "Leadership Excellence",
        "description": "Led a group or club successfully",
        "icon": "👑",
        "color": "gold"
    },
    "community_service": {
        "name": "Community Service",
        "description": "Volunteered for 20+ hours",
        "icon": "❤️",
        "color": "red"
    }
}

# ============ WELLNESS CENTER FUNCTIONS ============
def add_wellness_checkin(user_email: str, school_code: str, mood: int, stress: int, 
                         sleep: float, anxiety: int, energy: int, social: int, notes: str = ""):
    """Add a wellness check-in"""
    checkins = load_school_data(school_code, "wellness_checkins.json", [])
    checkin = {
        "id": generate_id("WEL"),
        "user_email": user_email,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "mood": mood,  # 1-10
        "stress": stress,  # 1-10
        "sleep": sleep,  # hours
        "anxiety": anxiety,  # 1-10
        "energy": energy,  # 1-10
        "social": social,  # 1-10
        "notes": notes
    }
    checkins.append(checkin)
    save_school_data(school_code, "wellness_checkins.json", checkins)
    
    # Check for concerning patterns
    recent_checkins = [c for c in checkins if c['user_email'] == user_email][-5:]
    if len(recent_checkins) >= 3:
        avg_stress = sum(c['stress'] for c in recent_checkins) / len(recent_checkins)
        avg_anxiety = sum(c['anxiety'] for c in recent_checkins) / len(recent_checkins)
        
        if avg_stress > 7 or avg_anxiety > 7:
            # Alert counselor
            counselors = [u for u in load_school_data(school_code, "users.json", []) if u['role'] == 'counselor']
            for counselor in counselors:
                # Use your existing notification system
                if 'send_notification' in globals():
                    send_notification(
                        school_code,
                        counselor['email'],
                        "wellness_alert",
                        "⚠️ Student Wellness Alert",
                        f"Student {user_email} showing high stress/anxiety levels",
                        {"student": user_email, "avg_stress": avg_stress, "avg_anxiety": avg_anxiety}
                    )
    
    return checkin

# ============ STUDY GROUPS FUNCTIONS ============
def create_study_group(school_code: str, name: str, subject: str, created_by: str,
                       schedule: str, max_participants: int = 10) -> str:
    """Create a study group"""
    groups = load_school_data(school_code, "study_groups.json", [])
    group = {
        "id": generate_id("STG"),
        "name": name,
        "subject": subject,
        "created_by": created_by,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "members": [created_by],
        "schedule": schedule,
        "max_participants": max_participants,
        "status": "active"
    }
    groups.append(group)
    save_school_data(school_code, "study_groups.json", groups)
    return group['id']

def join_study_group(school_code: str, group_id: str, user_email: str) -> bool:
    """Join a study group"""
    groups = load_school_data(school_code, "study_groups.json", [])
    for group in groups:
        if group['id'] == group_id:
            if len(group['members']) >= group['max_participants']:
                return False
            if user_email not in group['members']:
                group['members'].append(user_email)
                save_school_data(school_code, "study_groups.json", groups)
                return True
    return False

# ============ CAREER GUIDANCE FUNCTIONS ============
CAREER_INTERESTS = {
    "science": ["Medicine", "Engineering", "Research", "Pharmacy", "Environmental Science"],
    "arts": ["Graphic Design", "Photography", "Fine Arts", "Animation", "Fashion Design"],
    "business": ["Accounting", "Marketing", "Entrepreneurship", "Finance", "Human Resources"],
    "technology": ["Software Development", "Data Science", "Cybersecurity", "AI/ML", "IT Management"],
    "humanities": ["Law", "Journalism", "Psychology", "Education", "Social Work"],
    "trades": ["Electrician", "Plumbing", "Carpentry", "Welding", "Automotive"]
}

def career_quiz(answers: dict) -> list:
    """Process career quiz and return recommendations"""
    interests = []
    
    # Q1: What subjects do you enjoy?
    if answers.get('q1') in ['math', 'science']:
        interests.extend(['science', 'technology'])
    elif answers.get('q1') in ['english', 'history']:
        interests.extend(['humanities', 'arts'])
    elif answers.get('q1') == 'business':
        interests.extend(['business', 'trades'])
    
    # Q2: How do you like to work?
    if answers.get('q2') == 'alone':
        interests.extend(['technology', 'research'])
    elif answers.get('q2') == 'team':
        interests.extend(['business', 'healthcare'])
    elif answers.get('q2') == 'creative':
        interests.extend(['arts', 'design'])
    
    # Q3: What's your problem-solving style?
    if answers.get('q3') == 'analytical':
        interests.extend(['science', 'engineering'])
    elif answers.get('q3') == 'creative':
        interests.extend(['arts', 'marketing'])
    elif answers.get('q3') == 'practical':
        interests.extend(['trades', 'business'])
    
    # Q4: What's important in your career?
    if answers.get('q4') == 'money':
        interests.extend(['business', 'technology'])
    elif answers.get('q4') == 'helping':
        interests.extend(['healthcare', 'education'])
    elif answers.get('q4') == 'creativity':
        interests.extend(['arts', 'design'])
    elif answers.get('q4') == 'stability':
        interests.extend(['government', 'trades'])
    
    # Get unique interests and map to careers
    unique_interests = list(set(interests))
    recommendations = []
    for interest in unique_interests[:3]:
        recommendations.extend(CAREER_INTERESTS.get(interest, []))
    
    return recommendations[:5]  # Return top 5

# ============ EMERGENCY ALERT SYSTEM ============
EMERGENCY_TYPES = {
    "medical": {"icon": "🚑", "priority": 1, "message": "Medical Emergency"},
    "security": {"icon": "🚨", "priority": 2, "message": "Security Threat"},
    "fire": {"icon": "🔥", "priority": 1, "message": "Fire Emergency"},
    "accident": {"icon": "⚠️", "priority": 2, "message": "Accident Reported"},
    "other": {"icon": "🆘", "priority": 3, "message": "Other Emergency"}
}

def send_emergency_alert(user_email: str, school_code: str, alert_type: str, 
                         location: str = "", description: str = ""):
    """Send an emergency alert"""
    alerts = load_school_data(school_code, "emergency_alerts.json", [])
    
    # Check for recent similar alerts to prevent spam
    recent = [a for a in alerts if a['user_email'] == user_email and 
              a['timestamp'].startswith(datetime.now().strftime("%Y-%m-%d"))]
    if len(recent) > 3:
        return False, "Too many alerts from this user today"
    
    alert = {
        "id": generate_id("EMA"),
        "user_email": user_email,
        "alert_type": alert_type,
        "location": location,
        "description": description,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "active",
        "responded_by": None,
        "response_time": None
    }
    alerts.append(alert)
    save_school_data(school_code, "emergency_alerts.json", alerts)
    
    # Get emergency contacts (admins, security)
    users = load_school_data(school_code, "users.json", [])
    emergency_contacts = [u for u in users if u['role'] in ['admin', 'security']]
    
    alert_info = EMERGENCY_TYPES.get(alert_type, EMERGENCY_TYPES['other'])
    
    for contact in emergency_contacts:
        # Use your existing notification system
        if 'send_notification' in globals():
            send_notification(
                school_code,
                contact['email'],
                "emergency_alert",
                f"{alert_info['icon']} EMERGENCY ALERT",
                f"{alert_info['message']} at {location}\nReported by: {user_email}\nDetails: {description}",
                {"alert_id": alert['id'], "priority": alert_info['priority']}
            )
    
    return True, "Emergency alert sent successfully"

# ============ VIDEO CONFERENCING ============
def create_video_meeting(school_code: str, room_name: str, created_by: str,
                         meeting_type: str, scheduled_for: datetime = None) -> dict:
    """Create a Jitsi Meet video conference"""
    meetings = load_school_data(school_code, "video_meetings.json", [])
    
    # Generate unique room name
    room_id = generate_id("VID")
    jitsi_url = f"https://meet.jit.si/{school_code}_{room_id}"
    
    meeting = {
        "id": room_id,
        "room_name": room_name,
        "created_by": created_by,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "scheduled_for": scheduled_for.strftime("%Y-%m-%d %H:%M:%S") if scheduled_for else None,
        "participants": [created_by],
        "meeting_type": meeting_type,  # class, parent_teacher, study_group
        "link": jitsi_url,
        "status": "scheduled" if scheduled_for else "active"
    }
    meetings.append(meeting)
    save_school_data(school_code, "video_meetings.json", meetings)
    
    return meeting

# ============ QR CODE GENERATOR ============
def generate_qr_code(data: str, size: int = 200) -> str:
    """Generate QR code and return as base64 image (if qrcode is available)"""
    if not QRCODE_AVAILABLE:
        return ""
    
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        return ""

# ============ E-PORTFOLIO FUNCTIONS ============
def add_portfolio_project(user_email: str, school_code: str, title: str, 
                          description: str, skills: list, files: list = None):
    """Add a project to user's portfolio"""
    projects = load_school_data(school_code, "portfolio_projects.json", [])
    
    # Process uploaded files using your existing save_attachment function
    file_data = []
    if files and 'save_attachment' in globals():
        for file in files:
            attachment = save_attachment(file)
            if attachment:
                file_data.append(attachment)
    
    project = {
        "id": generate_id("PFP"),
        "user_email": user_email,
        "title": title,
        "description": description,
        "skills": skills,
        "files": file_data,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    projects.append(project)
    save_school_data(school_code, "portfolio_projects.json", projects)
    
    return project

# ============ RENDER FUNCTIONS FOR NEW UI ELEMENTS ============
def render_language_selector():
    """Render language selection dropdown"""
    st.sidebar.markdown("### 🌐 Language")
    col1, col2, col3, col4 = st.sidebar.columns(4)
    with col1:
        if st.sidebar.button("🇬🇧 EN", key="lang_en", use_container_width=True):
            st.session_state.language = 'en'
            st.rerun()
    with col2:
        if st.sidebar.button("🇰🇪 SW", key="lang_sw", use_container_width=True):
            st.session_state.language = 'sw'
            st.rerun()
    with col3:
        if st.sidebar.button("🇫🇷 FR", key="lang_fr", use_container_width=True):
            st.session_state.language = 'fr'
            st.rerun()
    with col4:
        if st.sidebar.button("🇸🇦 AR", key="lang_ar", use_container_width=True):
            st.session_state.language = 'ar'
            st.rerun()

def render_accessibility_panel():
    """Render accessibility settings panel"""
    with st.sidebar.expander("♿ Accessibility", expanded=False):
        if 'accessibility' not in st.session_state:
            st.session_state.accessibility = ACCESSIBILITY_PRESETS["Default"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Text size
            text_size = st.select_slider(
                "Text Size",
                options=["Small", "Medium", "Large", "Extra Large"],
                value=st.session_state.accessibility.get('text_size', 'Medium'),
                key="acc_text_size"
            )
            
            # High contrast
            high_contrast = st.checkbox(
                "High Contrast Mode",
                value=st.session_state.accessibility.get('contrast_mode', False),
                key="acc_contrast"
            )
            
            # Dyslexia font
            dyslexia_font = st.checkbox(
                "Dyslexia-Friendly Font",
                value=st.session_state.accessibility.get('dyslexia_font', False),
                key="acc_dyslexia"
            )
        
        with col2:
            # Color blind mode
            color_blind = st.selectbox(
                "Color Blindness Mode",
                options=list(COLOR_BLIND_FILTERS.keys()),
                index=list(COLOR_BLIND_FILTERS.keys()).index(
                    st.session_state.accessibility.get('color_blind_mode', 'None')
                ),
                key="acc_color_blind"
            )
            
            # Reduced motion
            reduced_motion = st.checkbox(
                "Reduced Motion",
                value=st.session_state.accessibility.get('reduced_motion', False),
                key="acc_motion"
            )
            
            # Accessibility presets
            preset = st.selectbox(
                "Presets",
                options=list(ACCESSIBILITY_PRESETS.keys()),
                key="acc_preset"
            )
            if st.button("Apply Preset", key="acc_apply", use_container_width=True):
                st.session_state.accessibility = ACCESSIBILITY_PRESETS[preset]
                st.rerun()
        
        if st.button("💾 Save Settings", key="acc_save", use_container_width=True):
            st.session_state.accessibility.update({
                'text_size': text_size,
                'contrast_mode': high_contrast,
                'dyslexia_font': dyslexia_font,
                'color_blind_mode': color_blind,
                'reduced_motion': reduced_motion
            })
            st.success("Accessibility settings saved!")
            st.rerun()

def render_wellness_center():
    """Render wellness center interface"""
    st.markdown("### 🧠 Wellness Center")
    
    tab1, tab2, tab3 = st.tabs([
        "📝 Daily Check-in",
        "📊 My Wellness",
        "🆘 Resources"
    ])
    
    with tab1:
        st.markdown("#### How are you feeling today?")
        
        with st.form("wellness_checkin"):
            col1, col2 = st.columns(2)
            
            with col1:
                mood = st.slider("Mood (1-10)", 1, 10, 7, help="1=Very Sad, 10=Very Happy")
                stress = st.slider("Stress Level (1-10)", 1, 10, 5, help="1=No stress, 10=Extremely stressed")
                sleep = st.number_input("Hours of Sleep", min_value=0.0, max_value=24.0, value=7.0, step=0.5)
            
            with col2:
                anxiety = st.slider("Anxiety Level (1-10)", 1, 10, 5, help="1=No anxiety, 10=Extremely anxious")
                energy = st.slider("Energy Level (1-10)", 1, 10, 6, help="1=Very low, 10=Very high")
                social = st.slider("Social Connection (1-10)", 1, 10, 6, help="1=Isolated, 10=Very connected")
            
            notes = st.text_area("Notes (optional)", placeholder="Anything you'd like to share...")
            
            if st.form_submit_button("Submit Check-in", use_container_width=True):
                if st.session_state.user and st.session_state.current_school:
                    add_wellness_checkin(
                        st.session_state.user['email'],
                        st.session_state.current_school['code'],
                        mood, stress, sleep, anxiety, energy, social, notes
                    )
                    st.success("Check-in recorded! Thank you for sharing.")
                    
                    if stress > 7 or anxiety > 7:
                        st.warning("""
                        ⚠️ Your stress/anxiety levels seem high. 
                        Remember you can talk to our school counselor.
                        """)
    
    with tab2:
        if st.session_state.user and st.session_state.current_school:
            checkins = load_school_data(
                st.session_state.current_school['code'], 
                "wellness_checkins.json", 
                []
            )
            user_checkins = [c for c in checkins if c['user_email'] == st.session_state.user['email']]
            
            if user_checkins:
                df = pd.DataFrame(user_checkins)
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date')
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    avg_mood = df['mood'].mean()
                    st.metric("Average Mood", f"{avg_mood:.1f}/10")
                with col2:
                    avg_stress = df['stress'].mean()
                    st.metric("Average Stress", f"{avg_stress:.1f}/10")
                with col3:
                    avg_sleep = df['sleep'].mean()
                    st.metric("Average Sleep", f"{avg_sleep:.1f} hrs")
                
                # Trend graphs
                fig = px.line(df, x='date', y=['mood', 'stress', 'anxiety', 'energy'],
                              title="Wellness Trends Over Time",
                              color_discrete_sequence=['#28a745', '#dc3545', '#ffc107', '#17a2b8'])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No check-in data yet. Start tracking your wellness today!")
    
    with tab3:
        st.markdown("""
        #### 📞 Emergency Contacts
        - **School Counselor**: Room 101, Ext 123
        - **Health Center**: Ext 456
        - **Emergency**: 999 / 112
        
        #### 📚 Self-Help Resources
        - Stress Management Guide
        - Mindfulness Exercises
        - Study-Life Balance Tips
        - Peer Support Group Schedule
        
        #### 🗓️ Support Groups
        - **Anxiety Support**: Mondays 4pm, Room 203
        - **Study Stress**: Wednesdays 3pm, Library
        - **Peer Connection**: Fridays 2pm, Student Lounge
        """)

def render_study_groups():
    """Render study groups interface"""
    st.markdown("### 📚 Study Groups")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Create Study Group")
        with st.form("create_study_group"):
            group_name = st.text_input("Group Name", placeholder="e.g., Math Masters")
            subject = st.selectbox("Subject", PRIMARY_SUBJECTS)
            schedule = st.text_input("Schedule", placeholder="e.g., Mon/Wed 3-4pm")
            max_participants = st.number_input("Max Participants", min_value=2, max_value=20, value=10)
            
            if st.form_submit_button("Create Group", use_container_width=True):
                if st.session_state.user and st.session_state.current_school:
                    group_id = create_study_group(
                        st.session_state.current_school['code'],
                        group_name,
                        subject,
                        st.session_state.user['email'],
                        schedule,
                        max_participants
                    )
                    st.success(f"Study group '{group_name}' created!")
                    st.rerun()
    
    with col2:
        st.markdown("#### Available Study Groups")
        if st.session_state.user and st.session_state.current_school:
            groups = load_school_data(st.session_state.current_school['code'], "study_groups.json", [])
            active_groups = [g for g in groups if g['status'] == 'active']
            
            if active_groups:
                for group in active_groups:
                    with st.container():
                        col_a, col_b = st.columns([3, 1])
                        with col_a:
                            st.markdown(f"**{group['name']}** ({group['subject']})")
                            st.markdown(f"Schedule: {group['schedule']}")
                            st.markdown(f"Members: {len(group['members'])}/{group['max_participants']}")
                        with col_b:
                            if st.session_state.user['email'] not in group['members']:
                                if len(group['members']) < group['max_participants']:
                                    if st.button("Join", key=f"join_{group['id']}", use_container_width=True):
                                        if join_study_group(
                                            st.session_state.current_school['code'],
                                            group['id'],
                                            st.session_state.user['email']
                                        ):
                                            st.success(f"Joined {group['name']}!")
                                            st.rerun()
                        st.divider()
            else:
                st.info("No active study groups available")

def render_career_guidance():
    """Render career guidance interface"""
    st.markdown("### 🎯 Career Guidance")
    
    tab1, tab2 = st.tabs(["🎯 Career Quiz", "💼 Recommendations"])
    
    with tab1:
        st.markdown("#### Discover Your Career Path")
        st.markdown("Answer a few questions to get personalized career recommendations.")
        
        with st.form("career_quiz"):
            q1 = st.radio(
                "1. What subjects do you enjoy most?",
                ["Mathematics/Science", "Languages/Arts", "Business/Commerce", "Practical/Trades"]
            )
            
            q2 = st.radio(
                "2. How do you prefer to work?",
                ["Independently", "In a team", "Creatively", "With my hands"]
            )
            
            q3 = st.radio(
                "3. How do you solve problems?",
                ["Analytically - break them down", "Creatively - think outside box", 
                 "Practically - try solutions", "Collaboratively - ask others"]
            )
            
            q4 = st.radio(
                "4. What's most important in your career?",
                ["High income", "Helping others", "Creative expression", "Job stability"]
            )
            
            if st.form_submit_button("Get Recommendations", use_container_width=True):
                answers = {
                    'q1': q1.lower().split('/')[0],
                    'q2': q2.lower(),
                    'q3': q3.lower().split()[0],
                    'q4': q4.lower().split()[0]
                }
                
                recommendations = career_quiz(answers)
                st.session_state.career_recommendations = recommendations
                st.rerun()
    
    with tab2:
        if 'career_recommendations' in st.session_state and st.session_state.career_recommendations:
            st.markdown("#### Your Career Recommendations")
            
            for i, career in enumerate(st.session_state.career_recommendations, 1):
                with st.container():
                    st.markdown(f"""
                    <div class="golden-card">
                        <h4>{i}. {career}</h4>
                        <p>📚 Recommended subjects: Mathematics, Sciences, Languages</p>
                        <p>🎓 Education path: Bachelor's degree in relevant field</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Take the career quiz to get personalized recommendations!")

def render_emergency_alerts():
    """Render emergency alert system"""
    st.markdown("### 🚨 Emergency Alert System")
    st.warning("Only use this for genuine emergencies!")
    
    with st.form("emergency_alert"):
        alert_type = st.selectbox(
            "Alert Type",
            options=list(EMERGENCY_TYPES.keys()),
            format_func=lambda x: EMERGENCY_TYPES[x]['message']
        )
        
        location = st.text_input("Your Location", placeholder="e.g., Room 101, Library, Field")
        description = st.text_area("Description", placeholder="Briefly describe the situation...")
        
        # Confirmation checkbox to prevent false alarms
        confirm = st.checkbox("I confirm this is a genuine emergency")
        
        if st.form_submit_button("🚨 SEND EMERGENCY ALERT", use_container_width=True, type="primary"):
            if not confirm:
                st.error("Please confirm this is a genuine emergency")
            elif st.session_state.user and st.session_state.current_school:
                success, message = send_emergency_alert(
                    st.session_state.user['email'],
                    st.session_state.current_school['code'],
                    alert_type,
                    location,
                    description
                )
                if success:
                    st.error("🚨 EMERGENCY ALERT SENT - Help is on the way!")
                    st.balloons()
                else:
                    st.error(message)

def render_portfolio():
    """Render e-portfolio interface"""
    st.markdown("### 📁 My Portfolio")
    
    tab1, tab2 = st.tabs(["📁 Projects", "🎯 Skills"])
    
    with tab1:
        st.markdown("#### My Projects")
        
        with st.expander("➕ Add New Project"):
            with st.form("add_project"):
                title = st.text_input("Project Title")
                description = st.text_area("Description", height=100)
                skills = st.multiselect("Skills Used", 
                                       ["Python", "Java", "HTML/CSS", "JavaScript", "Design", 
                                        "Research", "Writing", "Leadership", "Teamwork"])
                files = st.file_uploader("Upload Files", accept_multiple_files=True)
                
                if st.form_submit_button("Save Project", use_container_width=True):
                    if st.session_state.user and st.session_state.current_school:
                        project = add_portfolio_project(
                            st.session_state.user['email'],
                            st.session_state.current_school['code'],
                            title,
                            description,
                            skills,
                            files
                        )
                        st.success("Project added to portfolio!")
                        st.rerun()
        
        # Display projects
        if st.session_state.user and st.session_state.current_school:
            projects = load_school_data(st.session_state.current_school['code'], "portfolio_projects.json", [])
            user_projects = [p for p in projects if p['user_email'] == st.session_state.user['email']]
            
            if user_projects:
                for project in user_projects:
                    with st.container():
                        st.markdown(f"""
                        <div class="golden-card">
                            <h4>{project['title']}</h4>
                            <p>{project['description']}</p>
                            <p><strong>Skills:</strong> {', '.join(project['skills'])}</p>
                            <p><small>Added: {project['created_at'][:10]}</small></p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if project.get('files'):
                            with st.expander("📎 Project Files"):
                                for file in project['files']:
                                    if 'display_attachment' in globals():
                                        display_attachment(file)
                        st.divider()
            else:
                st.info("No projects yet. Add your first project!")
    
    with tab2:
        st.markdown("#### Skills")
        st.info("Skills tracking feature coming soon!")

def render_video_meeting():
    """Render video conferencing interface"""
    st.markdown("### 🎥 Video Meeting")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Create Meeting")
        with st.form("create_meeting"):
            room_name = st.text_input("Meeting Name", placeholder="e.g., Math Class")
            meeting_type = st.selectbox("Meeting Type", 
                                      ["Class Session", "Study Group", "Parent-Teacher"])
            
            schedule = st.checkbox("Schedule for later")
            if schedule:
                scheduled_time = st.datetime_input("Scheduled Time", 
                                                 min_value=datetime.now())
            else:
                scheduled_time = datetime.now()
            
            if st.form_submit_button("Create Meeting", use_container_width=True):
                if st.session_state.user and st.session_state.current_school:
                    meeting = create_video_meeting(
                        st.session_state.current_school['code'],
                        room_name,
                        st.session_state.user['email'],
                        meeting_type.lower().replace(' ', '_'),
                        scheduled_time if schedule else None
                    )
                    
                    st.session_state.current_meeting = meeting
                    st.success(f"Meeting created!")
                    st.rerun()
    
    with col2:
        if 'current_meeting' in st.session_state:
            meeting = st.session_state.current_meeting
            st.markdown(f"#### {meeting['room_name']}")
            st.markdown(f"**Meeting Link:** {meeting['link']}")
            st.markdown("Open this link in a new tab to join the meeting.")
            
            if st.button("Leave Meeting", use_container_width=True):
                del st.session_state.current_meeting
                st.rerun()
        else:
            st.info("Create a meeting to start")

def render_mobile_qr():
    """Render mobile app QR code"""
    st.sidebar.markdown("### 📱 Mobile App")
    
    if QRCODE_AVAILABLE and st.session_state.current_school:
        qr = generate_qr_code(f"https://schoolhub.app/download?school={st.session_state.current_school['code']}")
        if qr:
            st.sidebar.image(qr, width=150)
        else:
            st.sidebar.info("QR code unavailable")
    else:
        st.sidebar.info("Install qrcode package to enable QR features")

# ============ UPDATE SESSION STATE WITH NEW VARIABLES ============
if 'language' not in st.session_state:
    st.session_state.language = 'en'
if 'accessibility' not in st.session_state:
    st.session_state.accessibility = ACCESSIBILITY_PRESETS["Default"]
if 'current_feature' not in st.session_state:
    st.session_state.current_feature = None
if 'career_recommendations' not in st.session_state:
    st.session_state.career_recommendations = None
if 'current_meeting' not in st.session_state:
    st.session_state.current_meeting = None

# ============ NEW SIDEBAR ENHANCEMENTS ============
def render_enhanced_sidebar_additions():
    """Add these elements to your existing sidebar - call this after your sidebar content"""
    if st.session_state.user:
        st.sidebar.divider()
        
        # Language selector
        render_language_selector()
        
        # Accessibility panel
        render_accessibility_panel()
        
        st.sidebar.divider()
        
        # New features section
        st.sidebar.markdown("### 🆕 New Features")
        
        # Wellness Center
        if st.sidebar.button("🧠 Wellness Center", key="nav_wellness", use_container_width=True):
            st.session_state.current_feature = 'wellness'
            st.rerun()
        
        # Study Groups
        if st.sidebar.button("📚 Study Groups", key="nav_study", use_container_width=True):
            st.session_state.current_feature = 'study_groups'
            st.rerun()
        
        # Career Guidance
        if st.sidebar.button("🎯 Career Guidance", key="nav_career", use_container_width=True):
            st.session_state.current_feature = 'career'
            st.rerun()
        
        # Portfolio
        if st.sidebar.button("📁 Portfolio", key="nav_portfolio", use_container_width=True):
            st.session_state.current_feature = 'portfolio'
            st.rerun()
        
        # Video Meeting
        if st.sidebar.button("🎥 Video Meeting", key="nav_video", use_container_width=True):
            st.session_state.current_feature = 'video'
            st.rerun()
        
        st.sidebar.divider()
        
        # Emergency Alert Button
        if st.sidebar.button("🚨 EMERGENCY ALERT", key="nav_emergency", use_container_width=True, type="primary"):
            st.session_state.current_feature = 'emergency'
            st.rerun()
        
        # Mobile QR
        render_mobile_qr()

# ============ NEW FEATURE RENDERER ============
def render_selected_feature():
    """Render the selected feature in the main area"""
    if 'current_feature' in st.session_state and st.session_state.current_feature:
        if st.session_state.current_feature == 'wellness':
            render_wellness_center()
        elif st.session_state.current_feature == 'study_groups':
            render_study_groups()
        elif st.session_state.current_feature == 'career':
            render_career_guidance()
        elif st.session_state.current_feature == 'portfolio':
            render_portfolio()
        elif st.session_state.current_feature == 'video':
            render_video_meeting()
        elif st.session_state.current_feature == 'emergency':
            render_emergency_alerts()
        
        if st.button("← Back to Dashboard", key="back_to_dash", use_container_width=True):
            st.session_state.current_feature = None
            st.rerun()
        return True
    return False

# ============ ACCESSIBILITY CSS INTEGRATION ============
def get_accessibility_css():
    """Generate accessibility CSS based on settings"""
    if 'accessibility' not in st.session_state:
        return ""
    
    settings = st.session_state.accessibility
    css = ""
    
    # Text size
    text_sizes = {
        "Small": "0.85rem",
        "Medium": "1rem",
        "Large": "1.2rem",
        "Extra Large": "1.4rem"
    }
    base_size = text_sizes.get(settings.get('text_size', 'Medium'), '1rem')
    css += f"""
        body, .stApp, .main, .stMarkdown, p, h1, h2, h3, h4, h5, h6, .stTextInput, .stTextArea, .stSelectbox, .stButton {{
            font-size: {base_size} !important;
            line-height: 1.5 !important;
        }}
    """
    
    # High contrast mode
    if settings.get('contrast_mode', False):
        css += """
            body, .stApp, .main, .stMarkdown, p, h1, h2, h3, h4, h5, h6 {
                background: black !important;
                color: yellow !important;
            }
            a { color: cyan !important; }
            button, .stButton button {
                background: yellow !important;
                color: black !important;
                border: 2px solid yellow !important;
            }
            input, textarea, select {
                background: black !important;
                color: yellow !important;
                border: 2px solid yellow !important;
            }
            .golden-card, .class-card, .member-card {
                background: black !important;
                border: 2px solid yellow !important;
            }
        """
    
    # Dyslexia-friendly font
    if settings.get('dyslexia_font', False):
        css += """
            @import url('https://fonts.googleapis.com/css2?family=OpenDyslexic&display=swap');
            body, .stApp, .main, .stMarkdown, p, h1, h2, h3, h4, h5, h6, .stTextInput, .stTextArea, .stSelectbox {
                font-family: 'OpenDyslexic', Arial, sans-serif !important;
                line-height: 1.5 !important;
                letter-spacing: 0.05em !important;
            }
        """
    
    # Color blind filters
    color_blind_mode = settings.get('color_blind_mode', 'None')
    if color_blind_mode != 'None':
        filters = {
            "Protanopia": "url('#protanopia')",
            "Deuteranopia": "url('#deuteranopia')",
            "Tritanopia": "url('#tritanopia')"
        }
        css += f"""
            <svg style="position: absolute; width: 0; height: 0;">
                <filter id="protanopia">
                    <feColorMatrix type="matrix" values="0.567,0.433,0,0,0 0.558,0.442,0,0,0 0,0.242,0.758,0,0 0,0,0,1,0"/>
                </filter>
                <filter id="deuteranopia">
                    <feColorMatrix type="matrix" values="0.625,0.375,0,0,0 0.7,0.3,0,0,0 0,0.3,0.7,0,0 0,0,0,1,0"/>
                </filter>
                <filter id="tritanopia">
                    <feColorMatrix type="matrix" values="0.95,0.05,0,0,0 0,0.433,0.567,0,0 0,0.475,0.525,0,0 0,0,0,1,0"/>
                </filter>
            </svg>
            body, .stApp {{
                filter: {filters[color_blind_mode]};
            }}
        """
    
    # Reduced motion
    if settings.get('reduced_motion', False):
        css += """
            * {
                animation: none !important;
                transition: none !important;
            }
            @keyframes golden-shimmer {
                0% { background-position: 0% 50%; }
                100% { background-position: 0% 50%; }
            }
        """
    
    return css

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

# Apply accessibility CSS
if st.session_state.page == 'dashboard' and st.session_state.user:
    st.markdown(f"<style>{get_accessibility_css()}</style>", unsafe_allow_html=True)

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
        
        # Add the new features to sidebar
        render_enhanced_sidebar_additions()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.current_school = None
            st.session_state.page = 'welcome'
            st.rerun()
    
    # ============ MAIN CONTENT ============
    
    # Check if a new feature is selected
    if render_selected_feature():
        pass  # Feature is being displayed, nothing else to do
    elif menu == "Dashboard":
        st.markdown(f"<h2 style='text-align: center; color: white;'>Welcome, {user['fullname']}!</h2>", unsafe_allow_html=True)
        
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
                st.metric("🎫 Admission", user['admission_number'][:10] + "..." if len(user['admission_number']) > 10 else user['admission_number'])
            
            # Show borrowed books count
            if borrowed_books:
                active_borrows = len([b for b in borrowed_books if b['status'] == 'borrowed'])
                st.metric("📚 Books Borrowed", active_borrows)
        
        else:  # guardian
            st.info(f"👪 Linked to {len(user.get('linked_students', []))} student(s)")
            for adm in user.get('linked_students', []):
                student = next((u for u in users if u.get('admission_number') == adm), None)
                if student:
                    st.write(f"**{student['fullname']}** - {adm}")
    
    elif menu == "Announcements":
        st.markdown("<h2 style='text-align: center; color: white;'>📢 School Announcements</h2>", unsafe_allow_html=True)
        
        if user['role'] in ['admin', 'teacher']:
            with st.expander("➕ Create New Announcement"):
                with st.form("new_announcement"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        title = st.text_input("Title", placeholder="Announcement title")
                        content = st.text_area("Content", height=100, placeholder="Write your announcement here...")
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
        st.markdown("<h2 style='text-align: center; color: white;'>📝 Assignments</h2>", unsafe_allow_html=True)
        
        if user['role'] in ['admin', 'teacher']:
            with st.expander("➕ Create New Assignment"):
                with st.form("new_assignment"):
                    col1, col2 = st.columns(2)
                    with col1:
                        title = st.text_input("Assignment Title", placeholder="e.g., Math Homework 1")
                        subject = st.selectbox("Subject", PRIMARY_SUBJECTS)
                        target_class = st.selectbox("Target Class", ["All Classes"] + [c['name'] for c in classes])
                    with col2:
                        due_date = st.date_input("Due Date")
                        total_points = st.number_input("Total Points", min_value=1, value=100)
                        attachment = st.file_uploader("📎 Attachment", type=['pdf', 'docx', 'txt', 'jpg', 'png'])
                    
                    description = st.text_area("Description", height=100, placeholder="Describe the assignment...")
                    
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
                                <span style="color: rgba(255,255,255,0.7); margin-left: 10px;">{a['subject']}</span>
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
        st.markdown("<h2 style='text-align: center; color: white;'>🌍 School Community</h2>", unsafe_allow_html=True)
        
        all_members = [u for u in users if u['email'] != user['email']]
        friends = get_friends(school_code, user['email'])
        pending_requests = get_pending_requests(school_code, user['email'])
        sent_requests = get_sent_requests(school_code, user['email'])
        
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
                        st.markdown("<span style='color: #00ff00;'>✅ Friend</span>", unsafe_allow_html=True)
                    elif request_sent:
                        st.markdown("<span style='color: #ffff00;'>⏳ Request Sent</span>", unsafe_allow_html=True)
                    elif request_received:
                        st.markdown("<span style='color: #00ffff;'>📥 Request Received</span>", unsafe_allow_html=True)
                    else:
                        st.markdown("<span style='color: rgba(255,255,255,0.5);'>Not Connected</span>", unsafe_allow_html=True)
                
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
        st.markdown("<h2 style='text-align: center; color: white;'>🤝 Friends</h2>", unsafe_allow_html=True)
        
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
                                st.markdown("<span style='color: #ffff00;'>⏳ Pending</span>", unsafe_allow_html=True)
                            st.divider()
            else:
                st.info("No sent requests")
    
    elif menu.startswith("Chat"):
        st.markdown("<h2 style='text-align: center; color: white;'>💬 Messages</h2>", unsafe_allow_html=True)
        
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
        st.markdown("<h2 style='text-align: center; color: white;'>👥 Group Chats</h2>", unsafe_allow_html=True)
        
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
                    group_name = st.text_input("Group Name", placeholder="e.g., Math Study Group")
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
    
    # ============ CLASSES SECTION ============
    elif menu == "Classes" or menu == "My Classes" or menu == "Browse Classes":
        if menu == "Classes":
            st.markdown("<h2 style='text-align: center; color: white;'>📚 All Classes</h2>", unsafe_allow_html=True)
        elif menu == "My Classes":
            st.markdown("<h2 style='text-align: center; color: white;'>📚 My Classes</h2>", unsafe_allow_html=True)
        else:
            st.markdown("<h2 style='text-align: center; color: white;'>📚 Browse Classes</h2>", unsafe_allow_html=True)
        
        # Admin: View and create classes
        if user['role'] == 'admin':
            with st.expander("➕ Create New Class"):
                with st.form("create_class"):
                    class_name = st.text_input("Class Name", placeholder="e.g., Grade 4A")
                    grade = st.selectbox("Grade Level", KENYAN_GRADES)
                    teacher_email = st.selectbox("Class Teacher", 
                                               [f"{u['fullname']} ({u['email']})" for u in users if u['role'] == 'teacher'])
                    max_students = st.number_input("Maximum Students", min_value=1, value=40)
                    
                    if st.form_submit_button("Create Class", use_container_width=True):
                        if class_name:
                            new_class = {
                                "code": generate_class_code(),
                                "name": class_name,
                                "grade": grade,
                                "teacher": teacher_email.split('(')[1].rstrip(')') if '(' in teacher_email else teacher_email,
                                "teacher_name": teacher_email.split('(')[0].strip(),
                                "max_students": max_students,
                                "students": [],
                                "subjects": get_subjects_for_grade(grade),
                                "created_by": user['email'],
                                "created_at": datetime.now().strftime("%Y-%m-%d")
                            }
                            classes.append(new_class)
                            save_school_data(school_code, "classes.json", classes)
                            st.success(f"Class {class_name} created!")
                            st.rerun()
            
            # Display all classes for admin
            if classes:
                for cls in classes:
                    with st.container():
                        st.markdown(f"""
                        <div class="class-card">
                            <h4>{cls['name']} - {cls['grade']}</h4>
                            <p><strong>Teacher:</strong> {cls.get('teacher_name', 'Not assigned')}</p>
                            <p><strong>Students:</strong> {len(cls.get('students', []))}/{cls.get('max_students', 40)}</p>
                            <p><strong>Code:</strong> {cls['code']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("📝 Manage", key=f"manage_{cls['code']}"):
                                st.session_state.selected_class = cls['code']
                                st.rerun()
                        with col2:
                            if st.button("👥 View Students", key=f"students_{cls['code']}"):
                                st.session_state.selected_class = cls['code']
                                st.rerun()
                        with col3:
                            if st.button("📊 Performance", key=f"perf_{cls['code']}"):
                                st.session_state.selected_class = cls['code']
                                st.rerun()
                        st.divider()
            else:
                st.info("No classes created yet")
        
        # Teacher: View their classes
        elif user['role'] == 'teacher':
            my_classes = [c for c in classes if c.get('teacher') == user['email']]
            
            if my_classes:
                for cls in my_classes:
                    with st.container():
                        st.markdown(f"""
                        <div class="class-card">
                            <h4>{cls['name']} - {cls['grade']}</h4>
                            <p><strong>Students:</strong> {len(cls.get('students', []))}/{cls.get('max_students', 40)}</p>
                            <p><strong>Code:</strong> {cls['code']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("📝 Manage", key=f"manage_{cls['code']}"):
                                st.session_state.selected_class = cls['code']
                                st.rerun()
                        with col2:
                            if st.button("👥 Students", key=f"students_{cls['code']}"):
                                st.session_state.selected_class = cls['code']
                                st.rerun()
                        with col3:
                            if st.button("📊 Add Grades", key=f"grades_{cls['code']}"):
                                st.session_state.selected_class = cls['code']
                                st.rerun()
                        st.divider()
            else:
                st.info("You haven't been assigned any classes yet")
        
        # Student: View classes they're enrolled in
        elif user['role'] == 'student':
            my_classes = [c for c in classes if user['email'] in c.get('students', [])]
            
            if my_classes:
                for cls in my_classes:
                    with st.container():
                        st.markdown(f"""
                        <div class="class-card">
                            <h4>{cls['name']} - {cls['grade']}</h4>
                            <p><strong>Teacher:</strong> {cls.get('teacher_name', 'Not assigned')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button("📊 View My Performance", key=f"perf_{cls['code']}"):
                            st.session_state.selected_class = cls['code']
                            st.rerun()
                        st.divider()
            else:
                st.info("You're not enrolled in any classes yet")
                st.markdown("### Available Classes")
                available_classes = [c for c in classes if len(c.get('students', [])) < c.get('max_students', 40)]
                for cls in available_classes:
                    with st.container():
                        st.markdown(f"""
                        <div class="class-card">
                            <h4>{cls['name']} - {cls['grade']}</h4>
                            <p><strong>Teacher:</strong> {cls.get('teacher_name', 'Not assigned')}</p>
                            <p><strong>Available Seats:</strong> {cls.get('max_students', 40) - len(cls.get('students', []))}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button("📝 Request Enrollment", key=f"enroll_{cls['code']}"):
                            # Add enrollment request
                            class_requests.append({
                                "id": generate_id("CLR"),
                                "class_code": cls['code'],
                                "student_email": user['email'],
                                "student_name": user['fullname'],
                                "status": "pending",
                                "date": datetime.now().strftime("%Y-%m-%d")
                            })
                            save_school_data(school_code, "class_requests.json", class_requests)
                            st.success("Enrollment request sent!")
                            st.rerun()
                        st.divider()
        
        # Guardian: View their children's classes
        elif user['role'] == 'guardian':
            linked_adms = user.get('linked_students', [])
            linked_students = [u for u in users if u.get('admission_number') in linked_adms]
            
            for student in linked_students:
                student_classes = [c for c in classes if student['email'] in c.get('students', [])]
                if student_classes:
                    st.markdown(f"### {student['fullname']}'s Classes")
                    for cls in student_classes:
                        st.markdown(f"""
                        <div class="class-card">
                            <h4>{cls['name']} - {cls['grade']}</h4>
                            <p><strong>Teacher:</strong> {cls.get('teacher_name', 'Not assigned')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button("📊 View Performance", key=f"guard_perf_{cls['code']}_{student['email']}"):
                            st.session_state.selected_class = cls['code']
                            st.session_state.viewing_student = student['email']
                            st.rerun()
                        st.divider()
    
    # ============ GROUPS SECTION ============
    elif menu == "Groups":
        st.markdown("<h2 style='text-align: center; color: white;'>👥 Groups</h2>", unsafe_allow_html=True)
        
        if user['role'] in ['admin', 'teacher']:
            with st.expander("➕ Create New Group"):
                with st.form("create_group"):
                    group_name = st.text_input("Group Name", placeholder="e.g., Science Club")
                    group_type = st.selectbox("Group Type", ["Academic", "Sports", "Arts", "Cultural", "Other"])
                    description = st.text_area("Description", placeholder="Group purpose and activities...")
                    leader_email = st.selectbox("Group Leader", 
                                              [f"{u['fullname']} ({u['email']})" for u in users if u['role'] in ['teacher', 'student']])
                    
                    if st.form_submit_button("Create Group", use_container_width=True):
                        if group_name:
                            new_group = {
                                "code": generate_group_code(),
                                "name": group_name,
                                "type": group_type,
                                "description": description,
                                "leader": leader_email.split('(')[1].rstrip(')') if '(' in leader_email else leader_email,
                                "leader_name": leader_email.split('(')[0].strip(),
                                "co_leaders": [],
                                "members": [leader_email.split('(')[1].rstrip(')') if '(' in leader_email else leader_email],
                                "created_by": user['email'],
                                "created_at": datetime.now().strftime("%Y-%m-%d")
                            }
                            groups.append(new_group)
                            save_school_data(school_code, "groups.json", groups)
                            st.success(f"Group {group_name} created!")
                            st.rerun()
        
        # Display all groups
        if groups:
            for grp in groups:
                with st.container():
                    st.markdown(f"""
                    <div class="class-card">
                        <h4>{grp['name']}</h4>
                        <p><strong>Type:</strong> {grp['type']}</p>
                        <p><strong>Leader:</strong> {grp.get('leader_name', 'Not assigned')}</p>
                        <p><strong>Members:</strong> {len(grp.get('members', []))}</p>
                        <p>{grp.get('description', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    is_member = user['email'] in grp.get('members', [])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if is_member:
                            if st.button("🚪 Leave Group", key=f"leave_{grp['code']}"):
                                grp['members'].remove(user['email'])
                                save_school_data(school_code, "groups.json", groups)
                                st.rerun()
                        else:
                            if st.button("➕ Join Group", key=f"join_{grp['code']}"):
                                grp.setdefault('members', []).append(user['email'])
                                save_school_data(school_code, "groups.json", groups)
                                st.rerun()
                    with col2:
                        if st.button("👥 View Members", key=f"members_{grp['code']}"):
                            st.session_state.selected_group = grp['code']
                            st.rerun()
                    st.divider()
        else:
            st.info("No groups created yet")
    
    # ============ TEACHERS SECTION ============
    elif menu == "Teachers":
        st.markdown("<h2 style='text-align: center; color: white;'>👨‍🏫 Teachers</h2>", unsafe_allow_html=True)
        
        if user['role'] == 'admin':
            with st.expander("➕ Add New Teacher Code"):
                with st.form("add_teacher"):
                    teacher_name = st.text_input("Teacher Name", placeholder="Enter teacher's full name")
                    teacher_email = st.text_input("Email", placeholder="teacher@school.edu")
                    department = st.selectbox("Department", ["Mathematics", "English", "Sciences", "Humanities", "Languages", "Technical"])
                    
                    if st.form_submit_button("Generate Teacher Code", use_container_width=True):
                        if teacher_name:
                            new_code = generate_teacher_code()
                            teachers_data.append({
                                "code": new_code,
                                "name": teacher_name,
                                "email": teacher_email,
                                "department": department,
                                "status": "active",
                                "created": datetime.now().strftime("%Y-%m-%d"),
                                "used_by_list": []
                            })
                            save_school_data(school_code, "teachers.json", teachers_data)
                            st.success(f"Teacher code generated: {new_code}")
                            st.info(f"Share this code with {teacher_name} for registration")
        
        # Display all teachers
        st.subheader("📋 Teacher Directory")
        teacher_users = [u for u in users if u['role'] == 'teacher']
        
        if teacher_users:
            for teacher in teacher_users:
                with st.container():
                    col1, col2, col3 = st.columns([1, 3, 2])
                    with col1:
                        if teacher.get('profile_pic'):
                            st.image(teacher['profile_pic'], width=40)
                        else:
                            st.markdown("👨‍🏫")
                    with col2:
                        st.markdown(f"**{teacher['fullname']}**")
                        st.markdown(f"<small>{teacher['email']}</small>", unsafe_allow_html=True)
                    with col3:
                        teacher_classes = [c['name'] for c in classes if c.get('teacher') == teacher['email']]
                        st.markdown(f"Classes: {', '.join(teacher_classes) if teacher_classes else 'None'}")
                    st.divider()
        else:
            st.info("No teachers registered yet")
    
    # ============ STUDENTS SECTION ============
    elif menu == "Students":
        st.markdown("<h2 style='text-align: center; color: white;'>👨‍🎓 Students</h2>", unsafe_allow_html=True)
        
        # Display all students
        student_users = [u for u in users if u['role'] == 'student']
        
        if student_users:
            search = st.text_input("🔍 Search by name or admission number", placeholder="Type to search...")
            
            filtered_students = student_users
            if search:
                filtered_students = [s for s in student_users if search.lower() in s['fullname'].lower() or 
                                   search.lower() in s.get('admission_number', '').lower()]
            
            for student in filtered_students:
                with st.container():
                    col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
                    with col1:
                        if student.get('profile_pic'):
                            st.image(student['profile_pic'], width=40)
                        else:
                            st.markdown("👨‍🎓")
                    with col2:
                        st.markdown(f"**{student['fullname']}**")
                    with col3:
                        st.markdown(f"Admission: {student.get('admission_number', 'N/A')}")
                    with col4:
                        student_classes = [c['name'] for c in classes if student['email'] in c.get('students', [])]
                        st.markdown(f"Classes: {len(student_classes)}")
                    
                    if user['role'] == 'admin' or user['role'] == 'teacher':
                        if st.button("📊 View Performance", key=f"student_perf_{student['email']}"):
                            st.session_state.viewing_student = student['email']
                            st.rerun()
                    st.divider()
        else:
            st.info("No students registered yet")
    
    # ============ GUARDIANS SECTION ============
    elif menu == "Guardians":
        st.markdown("<h2 style='text-align: center; color: white;'>👪 Guardians</h2>", unsafe_allow_html=True)
        
        guardian_users = [u for u in users if u['role'] == 'guardian']
        
        if guardian_users:
            for guardian in guardian_users:
                with st.container():
                    col1, col2, col3 = st.columns([1, 3, 3])
                    with col1:
                        if guardian.get('profile_pic'):
                            st.image(guardian['profile_pic'], width=40)
                        else:
                            st.markdown("👪")
                    with col2:
                        st.markdown(f"**{guardian['fullname']}**")
                        st.markdown(f"<small>{guardian['email']}</small>", unsafe_allow_html=True)
                    with col3:
                        linked = guardian.get('linked_students', [])
                        linked_names = []
                        for adm in linked:
                            student = next((u for u in users if u.get('admission_number') == adm), None)
                            if student:
                                linked_names.append(student['fullname'])
                        st.markdown(f"Linked to: {', '.join(linked_names) if linked_names else 'None'}")
                    st.divider()
        else:
            st.info("No guardians registered yet")
    
    # ============ MY STUDENT (Guardian view) ============
    elif menu == "My Student":
        st.markdown("<h2 style='text-align: center; color: white;'>👪 My Students</h2>", unsafe_allow_html=True)
        
        linked_adms = user.get('linked_students', [])
        linked_students = [u for u in users if u.get('admission_number') in linked_adms]
        
        if linked_students:
            for student in linked_students:
                with st.expander(f"📚 {student['fullname']}", expanded=True):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Personal Information**")
                        st.write(f"Admission: {student.get('admission_number', 'N/A')}")
                        st.write(f"Email: {student.get('email', 'N/A')}")
                        st.write(f"Phone: {student.get('phone', 'N/A')}")
                    
                    with col2:
                        st.markdown("**Academic Summary**")
                        performance = calculate_student_performance(academic_records, student['email'])
                        st.metric("Overall Average", f"{performance['average']}%")
                        
                        rank_class = "performance-excellent" if performance['average'] >= 80 else \
                                     "performance-good" if performance['average'] >= 70 else \
                                     "performance-average" if performance['average'] >= 50 else \
                                     "performance-needs-improvement"
                        st.markdown(f"<div class='{rank_class}' style='padding:5px; text-align:center;'>{performance['rank']}</div>", 
                                   unsafe_allow_html=True)
                    
                    student_classes = [c for c in classes if student['email'] in c.get('students', [])]
                    if student_classes:
                        st.markdown("**Classes**")
                        for cls in student_classes:
                            st.write(f"- {cls['name']} ({cls['grade']})")
                    
                    if st.button("📊 View Full Performance", key=f"view_perf_{student['email']}"):
                        st.session_state.viewing_student = student['email']
                        st.rerun()
        else:
            st.info("No linked students found")
    
    # ============ LIBRARY MANAGEMENT ============
    elif menu == "Library Management" or menu == "My Library":
        if menu == "Library Management":
            st.markdown("<h2 style='text-align: center; color: white;'>📚 Library Management System</h2>", unsafe_allow_html=True)
            
            # External links
            st.markdown("### 🔗 External Management Systems")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                <a href="https://eddie-dante.github.io/Management-System/" target="_blank">
                    <button style="background: linear-gradient(135deg, #FFD700, #DAA520); border: none; color: black; padding: 12px 20px; border-radius: 8px; font-weight: bold; width: 100%; cursor: pointer; margin: 5px 0;">
                        📊 Open Main Management System
                    </button>
                </a>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown("""
                <a href="https://eddie-dante.github.io/Library-Management-System-/" target="_blank">
                    <button style="background: linear-gradient(135deg, #FFD700, #DAA520); border: none; color: black; padding: 12px 20px; border-radius: 8px; font-weight: bold; width: 100%; cursor: pointer; margin: 5px 0;">
                        📚 Open Library Management System
                    </button>
                </a>
                """, unsafe_allow_html=True)
            
            st.divider()
            
            lib_tab1, lib_tab2, lib_tab3, lib_tab4, lib_tab5 = st.tabs([
                "📖 Book Catalog", "📋 Borrow/Return", "👥 Members", "📊 Transactions", "📤 Import Data"
            ])
            
            with lib_tab1:
                st.subheader("Book Catalog")
                
                if user['role'] in ['admin', 'teacher', 'librarian']:
                    with st.expander("➕ Add New Book"):
                        with st.form("add_book"):
                            col1, col2 = st.columns(2)
                            with col1:
                                title = st.text_input("Book Title")
                                author = st.text_input("Author")
                                book_type = st.selectbox("Book Type", ["Textbook", "Novel", "Reference", "Magazine", "Other"])
                            with col2:
                                quantity = st.number_input("Quantity", min_value=1, value=1)
                                isbn = st.text_input("ISBN (Optional)")
                                publisher = st.text_input("Publisher (Optional)")
                                year = st.text_input("Year (Optional)")
                            
                            if st.form_submit_button("Add Book", use_container_width=True):
                                if title and author:
                                    add_book(school_code, title, author, book_type, quantity, isbn, publisher, year)
                                    st.success(f"Book '{title}' added successfully!")
                                    st.rerun()
                
                # Display books
                if library_books:
                    search_book = st.text_input("🔍 Search books by title or author", placeholder="Type to search...")
                    
                    filtered_books = library_books
                    if search_book:
                        filtered_books = [b for b in library_books if 
                                         search_book.lower() in b['title'].lower() or 
                                         search_book.lower() in b['author'].lower()]
                    
                    for book in filtered_books:
                        with st.container():
                            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                            with col1:
                                st.markdown(f"**{book['title']}**")
                                st.markdown(f"<small>by {book['author']} ({book['type']})</small>", unsafe_allow_html=True)
                            with col2:
                                st.markdown(f"Total: {book['quantity']}")
                            with col3:
                                st.markdown(f"Available: {book['available']}")
                            with col4:
                                if book['available'] > 0 and user['role'] in ['student', 'teacher']:
                                    if st.button("📖 Borrow", key=f"borrow_{book['id']}"):
                                        success, message = borrow_book(school_code, user['email'], book['id'])
                                        if success:
                                            st.success(message)
                                            st.rerun()
                                        else:
                                            st.error(message)
                            st.divider()
                else:
                    st.info("No books in catalog yet")
            
            with lib_tab2:
                st.subheader("Borrow/Return Books")
                
                if user['role'] in ['admin', 'teacher', 'librarian']:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("##### Borrow Book")
                        with st.form("borrow_book_form"):
                            members_list = [f"{m['email']} ({m.get('member_type', 'unknown')})" for m in library_members if m['status'] == 'active']
                            books_list = [f"{b['title']} by {b['author']}" for b in library_books if b['available'] > 0]
                            
                            if members_list and books_list:
                                borrower = st.selectbox("Select Borrower", members_list)
                                book_choice = st.selectbox("Select Book", books_list)
                                due_days = st.number_input("Due in (days)", min_value=1, value=14)
                                
                                if st.form_submit_button("Process Borrowing"):
                                    borrower_email = borrower.split('(')[0].strip()
                                    book_index = books_list.index(book_choice)
                                    book_id = library_books[book_index]['id']
                                    
                                    success, message = borrow_book(school_code, borrower_email, book_id, due_days)
                                    if success:
                                        st.success(message)
                                        st.rerun()
                                    else:
                                        st.error(message)
                            else:
                                st.warning("No active members or available books")
                    
                    with col2:
                        st.markdown("##### Return Book")
                        active_transactions = [t for t in library_transactions if t['status'] == 'borrowed']
                        
                        if active_transactions:
                            for trans in active_transactions[:5]:
                                with st.container():
                                    st.markdown(f"**{trans['book_title']}**")
                                    st.markdown(f"Borrowed by: {trans['user_email']}")
                                    st.markdown(f"Due: {trans['due_date']}")
                                    
                                    if st.button("📤 Return", key=f"return_{trans['id']}"):
                                        success, message = return_book(school_code, trans['id'])
                                        if success:
                                            st.success(message)
                                            st.rerun()
                                        else:
                                            st.error(message)
                                    st.divider()
                        else:
                            st.info("No active borrowings")
                
                # Display user's borrowed books
                if borrowed_books:
                    st.markdown("##### My Borrowed Books")
                    active_borrows = [b for b in borrowed_books if b['status'] == 'borrowed']
                    
                    for borrow in active_borrows:
                        book = next((b for b in library_books if b['id'] == borrow['book_id']), None)
                        if book:
                            with st.container():
                                col1, col2, col3 = st.columns([3, 2, 1])
                                with col1:
                                    st.markdown(f"**{book['title']}**")
                                with col2:
                                    due_date = datetime.strptime(borrow['due_date'], "%Y-%m-%d")
                                    days_left = (due_date - datetime.now()).days
                                    status_color = "🟢" if days_left > 3 else "🟡" if days_left > 0 else "🔴"
                                    st.markdown(f"{status_color} Due: {borrow['due_date']} ({days_left} days)")
                                with col3:
                                    if st.button("Return", key=f"user_return_{borrow['transaction_id']}"):
                                        success, message = return_book(school_code, borrow['transaction_id'])
                                        if success:
                                            st.success(message)
                                            st.rerun()
                                        else:
                                            st.error(message)
                                st.divider()
            
            with lib_tab3:
                st.subheader("Library Members")
                
                if user['role'] in ['admin', 'teacher', 'librarian']:
                    with st.expander("➕ Add Member Manually"):
                        with st.form("add_member"):
                            member_email = st.text_input("Member Email")
                            member_type = st.selectbox("Member Type", ["student", "teacher", "guardian", "librarian"])
                            
                            if st.form_submit_button("Add Member"):
                                add_library_member(school_code, member_email, member_type)
                                st.success(f"Member {member_email} added")
                                st.rerun()
                
                # Display members
                if library_members:
                    for member in library_members:
                        with st.container():
                            col1, col2, col3 = st.columns([3, 1, 2])
                            with col1:
                                st.markdown(f"**{member['email']}**")
                                st.markdown(f"<small>Type: {member['member_type']}</small>", unsafe_allow_html=True)
                            with col2:
                                active_borrows = len([b for b in member.get('borrowed_books', []) if b['status'] == 'borrowed'])
                                st.markdown(f"Borrowed: {active_borrows}")
                            with col3:
                                if member['status'] == 'active':
                                    if st.button("Deactivate", key=f"deact_{member['email']}"):
                                        member['status'] = 'inactive'
                                        save_school_data(school_code, "library_members.json", library_members)
                                        st.rerun()
                                else:
                                    if st.button("Activate", key=f"act_{member['email']}"):
                                        member['status'] = 'active'
                                        save_school_data(school_code, "library_members.json", library_members)
                                        st.rerun()
                            st.divider()
                else:
                    st.info("No library members yet")
            
            with lib_tab4:
                st.subheader("Transaction History")
                
                if library_transactions:
                    # Create DataFrame for visualization
                    trans_data = []
                    for t in library_transactions[-20:]:
                        trans_data.append({
                            "Book": t['book_title'][:30] + "...",
                            "Borrower": t['user_email'],
                            "Borrow Date": t['borrow_date'],
                            "Due Date": t['due_date'],
                            "Return Date": t.get('return_date', 'Not returned'),
                            "Status": t['status']
                        })
                    
                    if trans_data:
                        df = pd.DataFrame(trans_data)
                        st.dataframe(df, use_container_width=True)
                    
                    # Statistics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Transactions", len(library_transactions))
                    with col2:
                        active = len([t for t in library_transactions if t['status'] == 'borrowed'])
                        st.metric("Active Borrowings", active)
                    with col3:
                        overdue = len([t for t in library_transactions if t['status'] == 'borrowed' and 
                                     datetime.strptime(t['due_date'], "%Y-%m-%d") < datetime.now()])
                        st.metric("Overdue Books", overdue)
                else:
                    st.info("No transactions yet")
            
            with lib_tab5:
                st.subheader("Import Data from Excel")
                
                if user['role'] in ['admin', 'teacher', 'librarian']:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("##### Import Books")
                        books_file = st.file_uploader("Upload Books Excel", type=['xlsx', 'xls'], key="books_import")
                        
                        if books_file:
                            if st.button("Import Books", use_container_width=True):
                                success, message = import_books_from_excel(school_code, books_file)
                                if success:
                                    st.success(message)
                                    st.rerun()
                                else:
                                    st.error(message)
                            
                            st.info("Excel should have columns: Title, Author, Type, Quantity")
                    
                    with col2:
                        st.markdown("##### Import Members")
                        members_file = st.file_uploader("Upload Members Excel", type=['xlsx', 'xls'], key="members_import")
                        
                        if members_file:
                            if st.button("Import Members", use_container_width=True):
                                success, message = import_members_from_excel(school_code, members_file)
                                if success:
                                    st.success(message)
                                    st.rerun()
                                else:
                                    st.error(message)
                            
                            st.info("Excel should have columns: Name, Email, Type")
        
        else:  # My Library for students/guardians
            st.markdown("<h2 style='text-align: center; color: white;'>📚 My Library</h2>", unsafe_allow_html=True)
            
            lib_tab1, lib_tab2, lib_tab3 = st.tabs(["📖 Browse Books", "📋 My Borrowed Books", "📊 My History"])
            
            with lib_tab1:
                st.subheader("Browse Available Books")
                
                available_books = [b for b in library_books if b['available'] > 0]
                
                if available_books:
                    search_book = st.text_input("🔍 Search books by title or author", placeholder="Type to search...")
                    
                    filtered_books = available_books
                    if search_book:
                        filtered_books = [b for b in available_books if 
                                         search_book.lower() in b['title'].lower() or 
                                         search_book.lower() in b['author'].lower()]
                    
                    for book in filtered_books:
                        with st.container():
                            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                            with col1:
                                st.markdown(f"**{book['title']}**")
                                st.markdown(f"<small>by {book['author']} ({book['type']})</small>", unsafe_allow_html=True)
                            with col2:
                                st.markdown(f"Available: {book['available']}")
                            with col3:
                                if user['role'] in ['student', 'teacher']:
                                    if st.button("📖 Borrow", key=f"user_borrow_{book['id']}"):
                                        success, message = borrow_book(school_code, user['email'], book['id'])
                                        if success:
                                            st.success(message)
                                            st.rerun()
                                        else:
                                            st.error(message)
                            st.divider()
                else:
                    st.info("No books available for borrowing")
            
            with lib_tab2:
                st.subheader("My Borrowed Books")
                
                if borrowed_books:
                    active_borrows = [b for b in borrowed_books if b['status'] == 'borrowed']
                    
                    if active_borrows:
                        for borrow in active_borrows:
                            book = next((b for b in library_books if b['id'] == borrow['book_id']), None)
                            if book:
                                with st.container():
                                    col1, col2, col3 = st.columns([3, 2, 1])
                                    with col1:
                                        st.markdown(f"**{book['title']}**")
                                        st.markdown(f"<small>by {book['author']}</small>", unsafe_allow_html=True)
                                    with col2:
                                        due_date = datetime.strptime(borrow['due_date'], "%Y-%m-%d")
                                        days_left = (due_date - datetime.now()).days
                                        status_color = "🟢" if days_left > 3 else "🟡" if days_left > 0 else "🔴"
                                        st.markdown(f"{status_color} Due: {borrow['due_date']}")
                                        if days_left < 0:
                                            st.markdown(f"<span style='color: #ff4444;'>Overdue by {abs(days_left)} days</span>", 
                                                      unsafe_allow_html=True)
                                    with col3:
                                        if st.button("Return", key=f"user_return_{borrow['transaction_id']}"):
                                            success, message = return_book(school_code, borrow['transaction_id'])
                                            if success:
                                                st.success(message)
                                                st.rerun()
                                            else:
                                                st.error(message)
                                    st.divider()
                    else:
                        st.info("You have no borrowed books")
                else:
                    st.info("You have no borrowed books")
            
            with lib_tab3:
                st.subheader("My Borrowing History")
                
                user_transactions = [t for t in library_transactions if t['user_email'] == user['email']]
                
                if user_transactions:
                    for trans in reversed(user_transactions[-10:]):
                        with st.container():
                            col1, col2, col3 = st.columns([3, 2, 1])
                            with col1:
                                st.markdown(f"**{trans['book_title']}**")
                            with col2:
                                st.markdown(f"Borrowed: {trans['borrow_date']}")
                                if trans['return_date']:
                                    st.markdown(f"Returned: {trans['return_date']}")
                            with col3:
                                status_color = "🟢" if trans['status'] == 'returned' else "🟡"
                                st.markdown(f"{status_color} {trans['status'].title()}")
                            st.divider()
                else:
                    st.info("No borrowing history yet")
    
    # ============ SETTINGS SECTION ============
    elif menu == "Settings ⚙️":
        st.markdown("<h2 style='text-align: center; color: white;'>⚙️ Settings</h2>", unsafe_allow_html=True)
        
        settings_tab1, settings_tab2, settings_tab3 = st.tabs(["🎨 Theme & Wallpaper", "👤 Profile Settings", "🔔 Notifications"])
        
        with settings_tab1:
            st.subheader("Theme Selection")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Theme selector
                selected_theme = st.selectbox("Choose Theme", list(THEMES.keys()), 
                                            index=list(THEMES.keys()).index(st.session_state.theme))
                
                # Preview theme
                st.markdown(f"""
                <div style="background: {THEMES[selected_theme]['primary']}; padding: 10px; border-radius: 8px; margin: 10px 0;">
                    <p style="color: white;">Primary Color Preview</p>
                </div>
                <div style="background: {THEMES[selected_theme]['secondary']}; padding: 10px; border-radius: 8px; margin: 10px 0;">
                    <p style="color: white;">Secondary Color Preview</p>
                </div>
                <div style="background: {THEMES[selected_theme]['accent']}; padding: 10px; border-radius: 8px; margin: 10px 0;">
                    <p style="color: white;">Accent Color Preview</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Wallpaper selector
                st.subheader("Wallpaper")
                selected_wallpaper = st.selectbox("Choose Wallpaper", list(WALLPAPERS.keys()),
                                                index=list(WALLPAPERS.keys()).index(st.session_state.wallpaper))
                
                if selected_wallpaper != "None":
                    st.image(WALLPAPERS[selected_wallpaper], width=200, caption=selected_wallpaper)
            
            if st.button("💾 Save Theme Settings", use_container_width=True):
                st.session_state.theme = selected_theme
                st.session_state.wallpaper = selected_wallpaper
                save_user_settings(school_code, user['email'], {
                    "theme": selected_theme,
                    "wallpaper": selected_wallpaper
                })
                st.success("Settings saved! Refreshing...")
                st.rerun()
        
        with settings_tab2:
            st.subheader("Profile Settings")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                if user.get('profile_pic'):
                    st.image(user['profile_pic'], width=150)
                else:
                    emoji = "👑" if user['role'] == 'admin' else "👨‍🏫" if user['role'] == 'teacher' else "👨‍🎓" if user['role'] == 'student' else "👪"
                    st.markdown(f"<h1 style='font-size: 5rem; text-align: center;'>{emoji}</h1>", unsafe_allow_html=True)
                
                pic = st.file_uploader("📸 Upload Profile Photo", type=['png', 'jpg', 'jpeg'], key="settings_profile_pic")
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
                    st.success("Profile picture updated!")
                    st.rerun()
            
            with col2:
                with st.form("settings_profile_form"):
                    fullname = st.text_input("Full Name", user['fullname'])
                    phone = st.text_input("Phone", user.get('phone', ''))
                    bio = st.text_area("Bio", user.get('bio', ''), height=100)
                    
                    if st.form_submit_button("💾 Update Profile", use_container_width=True):
                        for u in users:
                            if u['email'] == user['email']:
                                u['fullname'] = fullname
                                u['phone'] = phone
                                u['bio'] = bio
                        save_school_data(school_code, "users.json", users)
                        user.update({'fullname': fullname, 'phone': phone, 'bio': bio})
                        st.success("Profile updated successfully!")
                        st.rerun()
        
        with settings_tab3:
            st.subheader("Notification Settings")
            
            with st.form("notification_settings"):
                st.markdown("##### Email Notifications")
                email_announcements = st.checkbox("Receive announcement emails", value=True)
                email_messages = st.checkbox("Receive message notifications", value=True)
                email_assignments = st.checkbox("Receive assignment reminders", value=True)
                
                st.markdown("##### In-App Notifications")
                sound_notifications = st.checkbox("Play sound for new messages", value=True)
                desktop_notifications = st.checkbox("Show desktop notifications", value=False)
                
                st.markdown("##### Digest Settings")
                digest_frequency = st.selectbox("Email digest frequency", 
                                              ["Daily", "Weekly", "Never"])
                
                if st.form_submit_button("💾 Save Notification Settings", use_container_width=True):
                    # Save notification settings to user profile
                    notification_settings = {
                        "email_announcements": email_announcements,
                        "email_messages": email_messages,
                        "email_assignments": email_assignments,
                        "sound_notifications": sound_notifications,
                        "desktop_notifications": desktop_notifications,
                        "digest_frequency": digest_frequency
                    }
                    
                    for u in users:
                        if u['email'] == user['email']:
                            u['notification_settings'] = notification_settings
                    save_school_data(school_code, "users.json", users)
                    st.success("Notification settings saved!")
    
    # ============ SCHOOL MANAGEMENT ============
    elif menu == "School Management":
        st.markdown("<h2 style='text-align: center; color: white;'>📊 School Management System</h2>", unsafe_allow_html=True)
        
        # External links
        st.markdown("### 🔗 External Management Systems")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <a href="https://eddie-dante.github.io/Management-System/" target="_blank">
                <button style="background: linear-gradient(135deg, #FFD700, #DAA520); border: none; color: black; padding: 12px 20px; border-radius: 8px; font-weight: bold; width: 100%; cursor: pointer; margin: 5px 0;">
                    📊 Open Main Management System
                </button>
            </a>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <a href="https://eddie-dante.github.io/Library-Management-System-/" target="_blank">
                <button style="background: linear-gradient(135deg, #FFD700, #DAA520); border: none; color: black; padding: 12px 20px; border-radius: 8px; font-weight: bold; width: 100%; cursor: pointer; margin: 5px 0;">
                    📚 Open Library Management System
                </button>
            </a>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        mgmt_tab1, mgmt_tab2, mgmt_tab3, mgmt_tab4, mgmt_tab5 = st.tabs([
            "📚 Academic Records", "💰 Finance", "📋 Discipline", "📊 Reports", "⚙️ Administration"
        ])
        
        with mgmt_tab1:
            st.subheader("Academic Records Management")
            
            students = [u for u in users if u['role'] == 'student']
            teacher_classes = [c for c in classes if c.get('teacher') == user['email']] if user['role'] == 'teacher' else classes
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Add New Academic Record")
                with st.form("add_academic_record_dash"):
                    if students:
                        if user['role'] == 'teacher' and teacher_classes:
                            # Teacher can only add grades for students in their classes
                            class_students = []
                            for cls in teacher_classes:
                                for student_email in cls.get('students', []):
                                    student = next((s for s in students if s['email'] == student_email), None)
                                    if student:
                                        class_students.append(f"{student['fullname']} ({student.get('admission_number', 'N/A')}) - {cls['name']}")
                            
                            if class_students:
                                student = st.selectbox("Select Student", class_students)
                            else:
                                st.warning("No students in your classes")
                                student = None
                        else:
                            student = st.selectbox("Select Student", 
                                                 [f"{s['fullname']} ({s.get('admission_number', 'N/A')})" for s in students])
                        
                        if student:
                            subject = st.selectbox("Subject", PRIMARY_SUBJECTS)
                            score = st.number_input("Score (0-100)", min_value=0, max_value=100, value=0)
                            term = st.selectbox("Term", ["Term 1", "Term 2", "Term 3"])
                            year = st.number_input("Year", value=datetime.now().year, min_value=2020, max_value=2030)
                            
                            # Get class name if teacher
                            class_name = None
                            if user['role'] == 'teacher' and teacher_classes:
                                selected_parts = student.split(' - ')
                                if len(selected_parts) > 1:
                                    class_name = selected_parts[1]
                            
                            if st.form_submit_button("Save Record", use_container_width=True):
                                student_email = student.split('(')[1].rstrip(')') if '(' in student else student
                                add_academic_record(
                                    school_code, 
                                    student_email, 
                                    subject, 
                                    score, 
                                    term, 
                                    str(year), 
                                    st.session_state.user['email'],
                                    class_name
                                )
                                st.success("Academic record added successfully!")
                                st.rerun()
            
            with col2:
                st.markdown("#### Performance Overview")
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
            
            st.markdown("#### Recent Academic Records")
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
            st.subheader("Finance Management")
            
            fees = load_school_data(school_code, "fees.json", [])
            students = [u for u in users if u['role'] == 'student']
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Add Fee Record")
                with st.form("add_fee_record_dash"):
                    if students:
                        student = st.selectbox("Select Student", 
                                             [f"{s['fullname']} ({s.get('admission_number', 'N/A')})" for s in students])
                        amount = st.number_input("Amount (KES)", min_value=0.0, value=0.0, step=100.0)
                        fee_type = st.selectbox("Fee Type", ["Tuition", "Transport", "Lunch", "Development", "Uniform", "Other"])
                        status = st.selectbox("Payment Status", ["Paid", "Pending", "Overdue", "Partial"])
                        receipt_no = st.text_input("Receipt Number (Optional)")
                        
                        if st.form_submit_button("Save Fee Record", use_container_width=True):
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
                st.markdown("#### Financial Summary")
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
            
            st.markdown("#### Recent Fee Records")
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
            st.subheader("Discipline Management")
            
            discipline = load_school_data(school_code, "discipline.json", [])
            students = [u for u in users if u['role'] == 'student']
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Add Discipline Record")
                with st.form("add_discipline_record_dash"):
                    if students:
                        student = st.selectbox("Select Student", 
                                             [f"{s['fullname']} ({s.get('admission_number', 'N/A')})" for s in students])
                        incident = st.text_area("Incident Description", height=100, placeholder="Describe what happened...")
                        action_taken = st.text_area("Action Taken", height=100, placeholder="What action was taken?")
                        
                        if st.form_submit_button("Save Record", use_container_width=True):
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
                st.markdown("#### Discipline Summary")
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
            
            st.markdown("#### Recent Discipline Records")
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
            st.subheader("Reports & Analytics")
            
            report_type = st.selectbox("Select Report Type", 
                                      ["Academic Performance", "Attendance Summary", "Financial Report", "Discipline Report"])
            
            if report_type == "Academic Performance":
                students = [u for u in users if u['role'] == 'student']
                if students:
                    selected_student = st.selectbox("Select Student for Detailed Report",
                                                   [f"{s['fullname']} ({s.get('admission_number', 'N/A')})" for s in students])
                    
                    if selected_student:
                        student_email = selected_student.split('(')[1].rstrip(')') if '(' in selected_student else selected_student
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
            
            elif report_type == "Discipline Report":
                discipline = load_school_data(school_code, "discipline.json", [])
                if discipline:
                    students = [u for u in users if u['role'] == 'student']
                    st.markdown("#### Discipline Cases by Student")
                    for student in students:
                        student_cases = [d for d in discipline if d['student_email'] == student['email']]
                        if student_cases:
                            st.write(f"**{student['fullname']}** - {len(student_cases)} case(s)")
                            for case in student_cases[-3:]:
                                st.write(f"- {case['date']}: {case['incident'][:50]}...")
                            st.divider()
                else:
                    st.info("No discipline data")
        
        with mgmt_tab5:
            st.subheader("Administration")
            
            admin_tab1, admin_tab2, admin_tab3 = st.tabs(["👥 User Management", "🏫 School Settings", "📅 Academic Calendar"])
            
            with admin_tab1:
                st.markdown("#### User Management")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Users", len(users))
                with col2:
                    st.metric("Students", len([u for u in users if u['role'] == 'student']))
                with col3:
                    st.metric("Teachers", len([u for u in users if u['role'] == 'teacher']))
                with col4:
                    st.metric("Guardians", len([u for u in users if u['role'] == 'guardian']))
                
                st.markdown("##### User Directory")
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
                st.markdown("#### School Settings")
                
                school = st.session_state.current_school
                
                with st.form("school_settings_dash"):
                    school_name = st.text_input("School Name", school['name'])
                    motto = st.text_input("School Motto", school.get('motto', ''))
                    city = st.text_input("City", school.get('city', ''))
                    state = st.text_input("State/Province", school.get('state', ''))
                    
                    if st.form_submit_button("Update Settings", use_container_width=True):
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
                st.markdown("#### Academic Calendar")
                
                events = load_school_data(school_code, "events.json", [])
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    with st.form("add_event_dash"):
                        st.markdown("##### Add Event")
                        event_name = st.text_input("Event Name")
                        event_date = st.date_input("Date")
                        event_type = st.selectbox("Type", ["Holiday", "Exam", "Meeting", "Sports Day", "Other"])
                        description = st.text_area("Description")
                        
                        if st.form_submit_button("Add Event", use_container_width=True):
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
                    st.markdown("##### Upcoming Events")
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
    
    # ============ PERSONAL DASHBOARD ============
    elif menu == "Personal Dashboard":
        st.markdown("<h2 style='text-align: center; color: white;'>👤 Personal Dashboard</h2>", unsafe_allow_html=True)
        
        personal_tab1, personal_tab2, personal_tab3, personal_tab4 = st.tabs([
            "👤 Profile", "📊 My Performance", "⭐ Reviews & Feedback", "🏆 Achievements"
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
                
                pic = st.file_uploader("📸 Upload Profile Photo", type=['png', 'jpg', 'jpeg'], key="personal_profile_pic")
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
                with st.form("update_personal_info_dash"):
                    fullname = st.text_input("Full Name", user['fullname'])
                    email = st.text_input("Email", user['email'], disabled=True)
                    phone = st.text_input("Phone", user.get('phone', ''))
                    bio = st.text_area("Bio", user.get('bio', ''), height=100)
                    
                    if user['role'] == 'student':
                        st.info(f"🎫 Admission Number: **{user.get('admission_number', 'N/A')}**")
                    elif user['role'] == 'guardian':
                        linked_students = user.get('linked_students', [])
                        st.info(f"👪 Linked Students: {', '.join(linked_students)}")
                    elif user['role'] == 'teacher':
                        st.info(f"📚 Teacher Code: {user.get('teacher_code_used', 'N/A')}")
                    
                    if st.form_submit_button("Update Profile", use_container_width=True):
                        for u in users:
                            if u['email'] == user['email']:
                                u['fullname'] = fullname
                                u['phone'] = phone
                                u['bio'] = bio
                        save_school_data(school_code, "users.json", users)
                        user.update({'fullname': fullname, 'phone': phone, 'bio': bio})
                        st.success("Profile updated successfully!")
                        st.rerun()
        
        with personal_tab2:
            st.markdown("#### My Performance")
            
            if user['role'] == 'student':
                attendance = load_school_data(school_code, "attendance.json", [])
                
                # Get performance data from teacher entries
                performance = calculate_student_performance(academic_records, user['email'])
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Overall Average", f"{performance['average']}%")
                    
                    rank_class = "performance-excellent" if performance['average'] >= 80 else \
                                 "performance-good" if performance['average'] >= 70 else \
                                 "performance-average" if performance['average'] >= 50 else \
                                 "performance-needs-improvement"
                    st.markdown(f"<div class='{rank_class}' style='padding:10px; text-align:center;'>{performance['rank']}</div>", 
                               unsafe_allow_html=True)
                    
                    # Subject-wise performance from teacher data
                    if performance['subject_details']:
                        st.markdown("##### Subject Details")
                        for subject_data in performance['subject_details']:
                            st.markdown(f"""
                            <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; margin: 5px 0;">
                                <strong>{subject_data['subject']}</strong>: {subject_data['score']}% 
                                <small>({subject_data['term']} {subject_data['year']})</small>
                            </div>
                            """, unsafe_allow_html=True)
                
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
                
                # Class performance comparison
                my_classes = [c for c in classes if user['email'] in c.get('students', [])]
                if my_classes:
                    st.markdown("##### Class Performance Comparison")
                    for cls in my_classes:
                        class_students = cls.get('students', [])
                        class_scores = []
                        for student_email in class_students:
                            student_perf = calculate_student_performance(academic_records, student_email)
                            if student_perf['average'] > 0:
                                class_scores.append(student_perf['average'])
                        
                        if class_scores:
                            class_avg = sum(class_scores) / len(class_scores)
                            st.markdown(f"""
                            <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; margin: 5px 0;">
                                <strong>{cls['name']}</strong><br>
                                Class Average: {class_avg:.1f}%<br>
                                Your Performance: {performance['average']}% 
                                ({'Above' if performance['average'] > class_avg else 'Below'} average)
                            </div>
                            """, unsafe_allow_html=True)
            
            elif user['role'] == 'teacher':
                my_classes = [c for c in classes if c.get('teacher') == user['email']]
                
                st.metric("Classes Taught", len(my_classes))
                
                if my_classes:
                    st.markdown("##### My Classes Performance")
                    for cls in my_classes:
                        class_students = cls.get('students', [])
                        class_scores = []
                        for student_email in class_students:
                            student_perf = calculate_student_performance(academic_records, student_email)
                            if student_perf['average'] > 0:
                                class_scores.append(student_perf['average'])
                        
                        if class_scores:
                            class_avg = sum(class_scores) / len(class_scores)
                            st.markdown(f"""
                            <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; margin: 5px 0;">
                                <strong>{cls['name']}</strong><br>
                                Class Average: {class_avg:.1f}%<br>
                                Students: {len(class_students)}
                            </div>
                            """, unsafe_allow_html=True)
                
                reviews = load_school_data(school_code, "teacher_reviews.json", [])
                my_reviews = [r for r in reviews if r['teacher_email'] == user['email']]
                
                if my_reviews:
                    avg_rating = sum([r['rating'] for r in my_reviews]) / len(my_reviews)
                    st.metric("Average Rating", f"{avg_rating:.1f}/5.0")
            
            elif user['role'] == 'guardian':
                linked_students = user.get('linked_students', [])
                
                if linked_students:
                    for adm in linked_students:
                        student = next((u for u in users if u.get('admission_number') == adm), None)
                        if student:
                            st.markdown(f"##### {student['fullname']}")
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
                            
                            if performance['subject_details']:
                                with st.expander("View Subject Details"):
                                    for subject_data in performance['subject_details'][:5]:
                                        st.write(f"**{subject_data['subject']}**: {subject_data['score']}% ({subject_data['term']})")
                            st.divider()
                else:
                    st.info("No linked students")
        
        with personal_tab3:
            st.markdown("#### Reviews & Feedback")
            
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
                    st.markdown("##### Give Student Review")
                    
                    # Get students from teacher's classes
                    my_classes = [c for c in classes if c.get('teacher') == user['email']]
                    class_students = []
                    for cls in my_classes:
                        for student_email in cls.get('students', []):
                            student = next((u for u in users if u['email'] == student_email), None)
                            if student:
                                class_students.append(f"{student['fullname']} ({student.get('admission_number', 'N/A')}) - {cls['name']}")
                    
                    with st.form("give_review_dash"):
                        if class_students:
                            student = st.selectbox("Select Student", class_students)
                            rating = st.slider("Rating (1-5)", 1, 5, 3)
                            review_text = st.text_area("Review", height=100, placeholder="Write your review here...")
                            
                            if st.form_submit_button("Submit Review", use_container_width=True):
                                student_email = student.split('(')[1].rstrip(')') if '(' in student else student
                                add_teacher_review(
                                    school_code,
                                    user['email'],
                                    student_email,
                                    review_text,
                                    rating,
                                    datetime.now().strftime("%Y-%m-%d")
                                )
                                st.success("Review submitted successfully!")
                                st.rerun()
                        else:
                            st.warning("No students in your classes")
                
                with tab_b:
                    st.markdown("##### Parent Feedback")
                    
                    feedback = load_school_data(school_code, "parent_feedback.json", [])
                    # Filter feedback for students in teacher's classes
                    my_students = []
                    for cls in my_classes:
                        my_students.extend(cls.get('students', []))
                    
                    filtered_feedback = [fb for fb in feedback if fb['student_email'] in my_students]
                    
                    if filtered_feedback:
                        for fb in reversed(filtered_feedback[-10:]):
                            guardian = next((u for u in users if u['email'] == fb['guardian_email']), None)
                            guardian_name = guardian['fullname'] if guardian else fb['guardian_email']
                            student = next((u for u in users if u['email'] == fb['student_email']), None)
                            student_name = student['fullname'] if student else fb['student_email']
                            
                            st.markdown(f"""
                            <div class="golden-card">
                                <strong>From: {guardian_name}</strong> about <strong>{student_name}</strong><br>
                                📅 {fb['date']}<br>
                                💬 {fb['feedback_text']}
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No feedback yet")
            
            elif user['role'] == 'guardian':
                st.markdown("##### Give Feedback")
                
                linked_students = [u for u in users if u.get('admission_number') in user.get('linked_students', [])]
                
                if linked_students:
                    with st.form("give_feedback_dash"):
                        student = st.selectbox("Select Student", 
                                             [f"{s['fullname']} ({s.get('admission_number', 'N/A')})" for s in linked_students])
                        feedback_text = st.text_area("Your Feedback", height=100, placeholder="Write your feedback here...")
                        
                        if st.form_submit_button("Submit Feedback", use_container_width=True):
                            student_email = student.split('(')[1].rstrip(')') if '(' in student else student
                            add_parent_feedback(
                                school_code,
                                user['email'],
                                student_email,
                                feedback_text,
                                datetime.now().strftime("%Y-%m-%d")
                            )
                            st.success("Feedback submitted successfully!")
                            st.rerun()
                else:
                    st.info("No linked students")
        
        with personal_tab4:
            st.markdown("#### 🏆 Achievements & Recognition")
            
            if user['role'] == 'student':
                # Calculate achievements based on performance
                performance = calculate_student_performance(academic_records, user['email'])
                
                achievements = []
                
                if performance['average'] >= 80:
                    achievements.append(("🏆 Academic Excellence", "Achieved 80%+ overall average", "gold"))
                if performance['average'] >= 70:
                    achievements.append(("📚 Honor Roll", "Achieved 70%+ overall average", "silver"))
                
                attendance = load_school_data(school_code, "attendance.json", [])
                student_attendance = [a for a in attendance if a['student_email'] == user['email']]
                if student_attendance:
                    present_count = len([a for a in student_attendance if a['status'] == 'Present'])
                    if present_count / len(student_attendance) >= 0.95:
                        achievements.append(("⭐ Perfect Attendance", "95%+ attendance rate", "blue"))
                
                # Library achievements
                if library_transactions:
                    user_transactions = [t for t in library_transactions if t['user_email'] == user['email']]
                    if len(user_transactions) >= 10:
                        achievements.append(("📚 Avid Reader", "Borrowed 10+ books", "green"))
                
                if achievements:
                    for achievement in achievements:
                        st.markdown(f"""
                        <div class="golden-card" style="text-align: center;">
                            <h1>{achievement[0][0]}</h1>
                            <h4>{achievement[0]}</h4>
                            <p>{achievement[1]}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No achievements yet. Keep working hard!")
            
            else:
                # Generic achievements for other roles
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
    
    elif menu == "Profile":
        st.markdown("<h2 style='text-align: center; color: white;'>👤 My Profile</h2>", unsafe_allow_html=True)
        
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
            with st.form("edit_profile_dash"):
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
    st.error("Something went wrong. Please restart.")
    if st.button("Restart"):
        st.session_state.page = 'welcome'
        st.rerun()
