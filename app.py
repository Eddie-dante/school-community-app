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

# ============ UPDATED WALLPAPERS ============
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

# ============ THEMES ============
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
            background: rgba(0, 0, 0, 0.45);
            backdrop-filter: blur(12px);
            border-radius: 24px;
            padding: 2rem;
            margin: 1.5rem;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 215, 0, 0.25);
            position: relative;
            z-index: 10;
        }}
        
        section[data-testid="stSidebar"] {{
            background: {theme["sidebar"]};
            background-size: 300% 300%;
            animation: golden-shimmer 8s ease infinite;
            backdrop-filter: blur(8px) !important;
            border-right: 2px solid rgba(255, 215, 0, 0.4) !important;
            box-shadow: 5px 0 30px rgba(218, 165, 32, 0.4) !important;
            z-index: 20;
        }}
        
        section[data-testid="stSidebar"] > div {{
            background: rgba(0, 0, 0, 0.3) !important;
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
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important;
            font-weight: 600 !important;
        }}
        
        section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {{
            background: rgba(0, 0, 0, 0.4) !important;
            border-radius: 12px !important;
            padding: 0.5rem !important;
            border: 1px solid rgba(255, 215, 0, 0.3) !important;
            margin: 0.8rem 0 !important;
        }}
        
        .stSelectbox div[data-baseweb="select"] {{
            background: rgba(0, 0, 0, 0.6) !important;
            border: 2px solid #FFD700 !important;
            border-radius: 10px !important;
            color: white !important;
            font-weight: 500 !important;
            backdrop-filter: blur(8px);
        }}
        
        .stTextInput input, 
        .stTextArea textarea, 
        .stDateInput input,
        .stNumberInput input {{
            background: rgba(0, 0, 0, 0.6) !important;
            border: 2px solid #FFD700 !important;
            border-radius: 10px !important;
            padding: 0.6rem 1rem !important;
            font-size: 0.95rem !important;
            color: white !important;
            font-weight: 500 !important;
            backdrop-filter: blur(8px);
        }}
        
        .stTextInput label,
        .stTextArea label,
        .stSelectbox label,
        .stDateInput label,
        .stNumberInput label {{
            color: white !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        }}
        
        .stTabs [data-baseweb="tab-list"] {{
            background: rgba(0, 0, 0, 0.5) !important;
            backdrop-filter: blur(8px) !important;
            border-radius: 12px !important;
            padding: 0.3rem !important;
            gap: 0.3rem;
            margin-bottom: 1.5rem !important;
            border: 1px solid rgba(255, 215, 0, 0.3);
        }}
        
        .stTabs [data-baseweb="tab"] {{
            color: white !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            font-weight: 600 !important;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: rgba(255, 215, 0, 0.3) !important;
            color: #FFD700 !important;
        }}
        
        h1, h2, h3, h4, h5, h6, p, span, div {{
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important;
        }}
        
        .golden-card {{
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(12px);
            border-left: 6px solid #FFD700;
            border-radius: 16px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
            color: white;
            border: 1px solid rgba(255, 215, 0, 0.2);
        }}
        
        .golden-card h1, .golden-card h2, .golden-card h3, .golden-card h4, .golden-card p {{
            color: white !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8) !important;
        }}
        
        .class-card {{
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(12px);
            border-radius: 16px;
            padding: 15px;
            margin-bottom: 10px;
            border-left: 4px solid #FFD700;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            color: white;
            border: 1px solid rgba(255, 215, 0, 0.2);
        }}
        
        .member-card {{
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(12px);
            border-radius: 16px;
            padding: 15px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 15px;
            border: 1px solid rgba(255, 215, 0, 0.3);
            color: white;
        }}
        
        .chat-container {{
            background: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(12px);
            border-radius: 20px;
            padding: 20px;
            height: 450px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
            border: 2px solid #FFD700;
        }}
        
        .chat-message-wrapper {{
            display: flex;
            margin-bottom: 10px;
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
            backdrop-filter: blur(12px);
        }}
        
        .chat-bubble-sent {{
            background: rgba(255, 215, 0, 0.25);
            color: white;
            border-bottom-right-radius: 4px;
            border: 1px solid #FFD700;
        }}
        
        .chat-bubble-received {{
            background: rgba(255, 255, 255, 0.15);
            color: white;
            border-bottom-left-radius: 4px;
            border: 1px solid #FFD700;
        }}
        
        .chat-sender-name {{
            font-size: 0.8rem;
            color: #FFD700;
            font-weight: 600;
        }}
        
        .chat-time {{
            font-size: 0.65rem;
            color: rgba(255, 255, 255, 0.7);
            margin-top: 4px;
            text-align: right;
        }}
        
        .notification-badge {{
            background: #ff4444;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.7rem;
            margin-left: 5px;
        }}
        
        .call-container {{
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(16px);
            border-radius: 24px;
            padding: 30px;
            border: 2px solid #FFD700;
            text-align: center;
        }}
        
        .call-participant {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 10px;
            margin: 5px 0;
            border: 1px solid rgba(255, 215, 0, 0.3);
        }}
        
        .ringing {{
            animation: ring 1s ease infinite;
        }}
        
        @keyframes ring {{
            0% {{ transform: rotate(0deg); }}
            10% {{ transform: rotate(5deg); }}
            20% {{ transform: rotate(-5deg); }}
            30% {{ transform: rotate(3deg); }}
            40% {{ transform: rotate(-3deg); }}
            50% {{ transform: rotate(1deg); }}
            60% {{ transform: rotate(-1deg); }}
            70% {{ transform: rotate(0deg); }}
        }}
        
        @keyframes golden-shimmer {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        
        .stButton button {{
            background: linear-gradient(135deg, #FFD700, #DAA520) !important;
            color: #000000 !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 8px 16px !important;
            font-weight: 700 !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        }}
        
        .stButton button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 16px #FFD700 !important;
        }}
        
        div[data-testid="stMetricValue"] {{
            color: #FFD700 !important;
            font-weight: 700 !important;
        }}
        
        .dataframe {{
            background: rgba(0, 0, 0, 0.5) !important;
            backdrop-filter: blur(8px) !important;
            color: white !important;
            border-radius: 12px !important;
        }}
        
        .dataframe th {{
            background: rgba(255, 215, 0, 0.3) !important;
            color: #FFD700 !important;
        }}
        
        .dataframe td {{
            color: white !important;
        }}
    </style>
    """

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

def generate_call_id():
    return 'CAL' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def generate_notification_id():
    return 'NOT' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def generate_request_id():
    return 'REQ' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

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

# ============ NOTIFICATION SYSTEM ============
def create_notification(school_code, user_email, notification_type, title, message, data=None):
    notifications = load_school_data(school_code, "notifications.json", [])
    notification = {
        "id": generate_notification_id(),
        "user_email": user_email,
        "type": notification_type,
        "title": title,
        "message": message,
        "data": data or {},
        "read": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    notifications.append(notification)
    save_school_data(school_code, "notifications.json", notifications)
    return notification

def mark_notification_read(school_code, notification_id):
    notifications = load_school_data(school_code, "notifications.json", [])
    for n in notifications:
        if n['id'] == notification_id:
            n['read'] = True
            break
    save_school_data(school_code, "notifications.json", notifications)

def get_unread_notifications_count(school_code, user_email):
    notifications = load_school_data(school_code, "notifications.json", [])
    return len([n for n in notifications if n['user_email'] == user_email and not n['read']])

# ============ CALL SYSTEM ============
CALL_TYPES = {
    "audio": {"icon": "🎧", "name": "Audio Call"},
    "video": {"icon": "📹", "name": "Video Call"}
}

def create_call(school_code, caller_email, recipients, call_type, room_name=None):
    calls = load_school_data(school_code, "calls.json", [])
    call_id = generate_call_id()
    
    if not room_name:
        room_name = f"Call_{call_id[:6]}"
    
    call = {
        "id": call_id,
        "caller": caller_email,
        "recipients": recipients,
        "call_type": call_type,
        "room_name": room_name,
        "status": "ringing",
        "started_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "answered_by": [],
        "call_log": []
    }
    calls.append(call)
    save_school_data(school_code, "calls.json", calls)
    
    users = load_school_data(school_code, "users.json", [])
    caller = next((u for u in users if u['email'] == caller_email), None)
    caller_name = caller['fullname'] if caller else caller_email
    
    for recipient in recipients:
        create_notification(
            school_code,
            recipient,
            "incoming_call",
            f"{CALL_TYPES[call_type]['icon']} Incoming {call_type.title()} Call",
            f"{caller_name} is calling you",
            {"call_id": call_id, "caller": caller_email, "call_type": call_type, "room_name": room_name}
        )
    
    return call

def answer_call(school_code, call_id, user_email):
    calls = load_school_data(school_code, "calls.json", [])
    for call in calls:
        if call['id'] == call_id and call['status'] == 'ringing':
            call['status'] = 'active'
            if user_email not in call['answered_by']:
                call['answered_by'].append(user_email)
            save_school_data(school_code, "calls.json", calls)
            return True
    return False

def end_call(school_code, call_id, user_email):
    calls = load_school_data(school_code, "calls.json", [])
    for call in calls:
        if call['id'] == call_id:
            call['status'] = 'ended'
            call['ended_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_school_data(school_code, "calls.json", calls)
            return True
    return False

def get_user_calls(school_code, user_email):
    calls = load_school_data(school_code, "calls.json", [])
    user_calls = []
    for call in calls:
        if user_email == call['caller'] or user_email in call['recipients']:
            user_calls.append(call)
    return user_calls

# ============ CHAT & FRIENDSHIP FUNCTIONS ============
def send_friend_request(school_code, from_email, to_email):
    requests = load_school_data(school_code, "friend_requests.json", [])
    if not any(r['from'] == from_email and r['to'] == to_email and r['status'] == 'pending' for r in requests):
        request_id = generate_request_id()
        requests.append({
            "id": request_id,
            "from": from_email,
            "to": to_email,
            "status": "pending",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        save_school_data(school_code, "friend_requests.json", requests)
        
        users = load_school_data(school_code, "users.json", [])
        from_user = next((u for u in users if u['email'] == from_email), None)
        from_name = from_user['fullname'] if from_user else from_email
        
        create_notification(
            school_code,
            to_email,
            "friend_request",
            "🤝 New Friend Request",
            f"{from_name} sent you a friend request",
            {"request_id": request_id}
        )
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
            create_notification(
                school_code,
                req['from'],
                "friend_accepted",
                "✅ Friend Request Accepted",
                f"{req['to']} accepted your friend request",
                {}
            )
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
    message_id = generate_id("MSG")
    messages.append({
        "id": message_id,
        "sender": sender_email,
        "recipient": recipient_email,
        "message": message,
        "attachment": attachment,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "read": False,
        "deleted": False,
        "deleted_by": [],
        "conversation_id": f"{min(sender_email, recipient_email)}_{max(sender_email, recipient_email)}"
    })
    save_school_data(school_code, "messages.json", messages)
    
    users = load_school_data(school_code, "users.json", [])
    sender = next((u for u in users if u['email'] == sender_email), None)
    sender_name = sender['fullname'] if sender else sender_email
    
    create_notification(
        school_code,
        recipient_email,
        "new_message",
        "💬 New Message",
        f"{sender_name}: {message[:50]}..." if len(message) > 50 else message,
        {"message_id": message_id, "conversation_id": f"{min(sender_email, recipient_email)}_{max(sender_email, recipient_email)}"}
    )
    
    return message_id

def delete_message(school_code, message_id, user_email):
    messages = load_school_data(school_code, "messages.json", [])
    for msg in messages:
        if msg['id'] == message_id:
            if 'deleted_by' not in msg:
                msg['deleted_by'] = []
            if user_email not in msg['deleted_by']:
                msg['deleted_by'].append(user_email)
            if len(msg['deleted_by']) >= 2 or user_email == msg['sender']:
                msg['deleted'] = True
            break
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

def get_conversation_messages(school_code, user_email, other_email):
    messages = load_school_data(school_code, "messages.json", [])
    conv_id = f"{min(user_email, other_email)}_{max(user_email, other_email)}"
    conv_msgs = [m for m in messages if m['conversation_id'] == conv_id and not m.get('deleted', False)]
    
    filtered_msgs = []
    for msg in conv_msgs:
        if user_email not in msg.get('deleted_by', []):
            filtered_msgs.append(msg)
    
    return sorted(filtered_msgs, key=lambda x: x['timestamp'])

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
    
    users = load_school_data(school_code, "users.json", [])
    creator = next((u for u in users if u['email'] == created_by), None)
    creator_name = creator['fullname'] if creator else created_by
    
    for member in members:
        if member != created_by:
            create_notification(
                school_code,
                member,
                "group_added",
                "👥 Added to Group",
                f"{creator_name} added you to '{group_name}'",
                {"group_id": group_chat['id']}
            )
    
    return group_chat['id']

def send_group_message(school_code, group_id, sender_email, message, attachment=None):
    group_chats = load_school_data(school_code, "group_chats.json", [])
    message_id = generate_id("GPM")
    
    for group in group_chats:
        if group['id'] == group_id:
            group['messages'].append({
                "id": message_id,
                "sender": sender_email,
                "message": message,
                "attachment": attachment,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "read_by": [sender_email],
                "deleted": False,
                "deleted_by": []
            })
            
            users = load_school_data(school_code, "users.json", [])
            sender = next((u for u in users if u['email'] == sender_email), None)
            sender_name = sender['fullname'] if sender else sender_email
            
            for member in group['members']:
                if member != sender_email:
                    create_notification(
                        school_code,
                        member,
                        "group_message",
                        f"👥 {group['name']}",
                        f"{sender_name}: {message[:50]}..." if len(message) > 50 else message,
                        {"group_id": group_id, "message_id": message_id}
                    )
            break
    
    save_school_data(school_code, "group_chats.json", group_chats)

def delete_group_message(school_code, group_id, message_id, user_email):
    group_chats = load_school_data(school_code, "group_chats.json", [])
    for group in group_chats:
        if group['id'] == group_id:
            for msg in group['messages']:
                if msg['id'] == message_id:
                    if 'deleted_by' not in msg:
                        msg['deleted_by'] = []
                    if user_email not in msg['deleted_by']:
                        msg['deleted_by'].append(user_email)
                    if user_email == msg['sender'] or user_email in group.get('admins', []):
                        msg['deleted'] = True
                    break
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

def delete_user(school_code, user_email, admin_email):
    if st.session_state.user['role'] != 'admin':
        return False, "Only admins can delete users"
    
    users = load_school_data(school_code, "users.json", [])
    users = [u for u in users if u['email'] != user_email]
    save_school_data(school_code, "users.json", users)
    
    friendships = load_school_data(school_code, "friendships.json", [])
    friendships = [f for f in friendships if f['user1'] != user_email and f['user2'] != user_email]
    save_school_data(school_code, "friendships.json", friendships)
    
    friend_requests = load_school_data(school_code, "friend_requests.json", [])
    friend_requests = [r for r in friend_requests if r['from'] != user_email and r['to'] != user_email]
    save_school_data(school_code, "friend_requests.json", friend_requests)
    
    groups = load_school_data(school_code, "groups.json", [])
    for group in groups:
        if user_email in group.get('members', []):
            group['members'].remove(user_email)
    save_school_data(school_code, "groups.json", groups)
    
    classes = load_school_data(school_code, "classes.json", [])
    for cls in classes:
        if user_email in cls.get('students', []):
            cls['students'].remove(user_email)
    save_school_data(school_code, "classes.json", classes)
    
    return True, f"User {user_email} deleted successfully"

def delete_announcement(school_code, announcement_id, user_email):
    announcements = load_school_data(school_code, "announcements.json", [])
    for i, ann in enumerate(announcements):
        if ann['id'] == announcement_id:
            if user_email == ann['author_email'] or st.session_state.user['role'] == 'admin':
                announcements.pop(i)
                save_school_data(school_code, "announcements.json", announcements)
                return True
    return False

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
    
    book = next((b for b in books if b['id'] == book_id), None)
    if not book or book['available'] <= 0:
        return False, "Book not available"
    
    member = next((m for m in members if m['email'] == user_email), None)
    if not member:
        add_library_member(school_code, user_email)
        members = load_school_data(school_code, "library_members.json", [])
        member = next((m for m in members if m['email'] == user_email), None)
    
    if any(b['book_id'] == book_id and b['status'] == 'borrowed' for b in member.get('borrowed_books', [])):
        return False, "Already borrowed this book"
    
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
    
    book['available'] -= 1
    
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
    
    transaction['return_date'] = datetime.now().strftime("%Y-%m-%d")
    transaction['status'] = 'returned'
    
    book = next((b for b in books if b['id'] == transaction['book_id']), None)
    if book:
        book['available'] += 1
    
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
            if any(u['email'] == row['Email'] for u in users):
                continue
            
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

# ============ PORTFOLIO FUNCTIONS ============
def add_portfolio_project(user_email, school_code, title, description, skills, files=None):
    projects = load_school_data(school_code, "portfolio_projects.json", [])
    
    file_data = []
    if files:
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

def add_portfolio_skill(user_email, school_code, skill, level):
    skills = load_school_data(school_code, "portfolio_skills.json", [])
    skill_entry = {
        "id": generate_id("PFS"),
        "user_email": user_email,
        "skill": skill,
        "level": level,
        "endorsements": [],
        "added_at": datetime.now().strftime("%Y-%m-%d")
    }
    skills.append(skill_entry)
    save_school_data(school_code, "portfolio_skills.json", skills)
    return skill_entry

def get_user_skills(user_email, school_code):
    skills = load_school_data(school_code, "portfolio_skills.json", [])
    return [s for s in skills if s['user_email'] == user_email]

def get_user_projects(user_email, school_code):
    projects = load_school_data(school_code, "portfolio_projects.json", [])
    return [p for p in projects if p['user_email'] == user_email]

# ============ WELLNESS CENTER FUNCTIONS ============
def add_wellness_checkin(user_email, school_code, mood, stress, sleep, anxiety, energy, social, notes=""):
    checkins = load_school_data(school_code, "wellness_checkins.json", [])
    checkin = {
        "id": generate_id("WEL"),
        "user_email": user_email,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "mood": mood,
        "stress": stress,
        "sleep": sleep,
        "anxiety": anxiety,
        "energy": energy,
        "social": social,
        "notes": notes
    }
    checkins.append(checkin)
    save_school_data(school_code, "wellness_checkins.json", checkins)
    
    recent_checkins = [c for c in checkins if c['user_email'] == user_email][-5:]
    if len(recent_checkins) >= 3:
        avg_stress = sum(c['stress'] for c in recent_checkins) / len(recent_checkins)
        avg_anxiety = sum(c['anxiety'] for c in recent_checkins) / len(recent_checkins)
        
        if avg_stress > 7 or avg_anxiety > 7:
            counselors = [u for u in load_school_data(school_code, "users.json", []) if u['role'] == 'counselor']
            for counselor in counselors:
                create_notification(
                    school_code,
                    counselor['email'],
                    "wellness_alert",
                    "⚠️ Student Wellness Alert",
                    f"Student {user_email} showing high stress/anxiety levels",
                    {"student": user_email, "avg_stress": avg_stress, "avg_anxiety": avg_anxiety}
                )
    
    return checkin

# ============ STUDY GROUPS FUNCTIONS ============
def create_study_group(school_code, name, subject, created_by, schedule, max_participants=10):
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
    
    users = load_school_data(school_code, "users.json", [])
    students = [u for u in users if u['role'] == 'student']
    
    for student in students[:10]:
        create_notification(
            school_code,
            student['email'],
            "study_group_created",
            "📚 New Study Group",
            f"A new {subject} study group '{name}' has been created",
            {"group_id": group['id']}
        )
    
    return group['id']

def join_study_group(school_code, group_id, user_email):
    groups = load_school_data(school_code, "study_groups.json", [])
    for group in groups:
        if group['id'] == group_id:
            if len(group['members']) >= group['max_participants']:
                return False
            if user_email not in group['members']:
                group['members'].append(user_email)
                save_school_data(school_code, "study_groups.json", groups)
                
                create_notification(
                    school_code,
                    group['created_by'],
                    "group_join",
                    "👥 New Group Member",
                    f"{user_email} joined your study group '{group['name']}'",
                    {"group_id": group_id}
                )
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

def career_quiz(answers):
    interests = []
    
    if answers.get('q1') in ['math', 'science']:
        interests.extend(['science', 'technology'])
    elif answers.get('q1') in ['english', 'history']:
        interests.extend(['humanities', 'arts'])
    elif answers.get('q1') == 'business':
        interests.extend(['business', 'trades'])
    
    if answers.get('q2') == 'alone':
        interests.extend(['technology', 'research'])
    elif answers.get('q2') == 'team':
        interests.extend(['business', 'healthcare'])
    elif answers.get('q2') == 'creative':
        interests.extend(['arts', 'design'])
    
    if answers.get('q3') == 'analytical':
        interests.extend(['science', 'engineering'])
    elif answers.get('q3') == 'creative':
        interests.extend(['arts', 'marketing'])
    elif answers.get('q3') == 'practical':
        interests.extend(['trades', 'business'])
    
    if answers.get('q4') == 'money':
        interests.extend(['business', 'technology'])
    elif answers.get('q4') == 'helping':
        interests.extend(['healthcare', 'education'])
    elif answers.get('q4') == 'creativity':
        interests.extend(['arts', 'design'])
    elif answers.get('q4') == 'stability':
        interests.extend(['government', 'trades'])
    
    unique_interests = list(set(interests))
    recommendations = []
    for interest in unique_interests[:3]:
        recommendations.extend(CAREER_INTERESTS.get(interest, []))
    
    return recommendations[:5]

# ============ EMERGENCY ALERT SYSTEM ============
EMERGENCY_TYPES = {
    "medical": {"icon": "🚑", "priority": 1, "message": "Medical Emergency"},
    "security": {"icon": "🚨", "priority": 2, "message": "Security Threat"},
    "fire": {"icon": "🔥", "priority": 1, "message": "Fire Emergency"},
    "accident": {"icon": "⚠️", "priority": 2, "message": "Accident Reported"},
    "other": {"icon": "🆘", "priority": 3, "message": "Other Emergency"}
}

def send_emergency_alert(user_email, school_code, alert_type, location="", description=""):
    alerts = load_school_data(school_code, "emergency_alerts.json", [])
    
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
    
    users = load_school_data(school_code, "users.json", [])
    emergency_contacts = [u for u in users if u['role'] in ['admin', 'security']]
    
    alert_info = EMERGENCY_TYPES.get(alert_type, EMERGENCY_TYPES['other'])
    
    for contact in emergency_contacts:
        create_notification(
            school_code,
            contact['email'],
            "emergency_alert",
            f"{alert_info['icon']} EMERGENCY ALERT",
            f"{alert_info['message']} at {location}\nReported by: {user_email}\nDetails: {description}",
            {"alert_id": alert['id'], "priority": alert_info['priority']}
        )
    
    return True, "Emergency alert sent successfully"

def respond_to_emergency(alert_id, responder_email, school_code):
    alerts = load_school_data(school_code, "emergency_alerts.json", [])
    for alert in alerts:
        if alert['id'] == alert_id:
            alert['status'] = 'responded'
            alert['responded_by'] = responder_email
            alert['response_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break
    save_school_data(school_code, "emergency_alerts.json", alerts)
    
    create_notification(
        school_code,
        alert['user_email'],
        "emergency_responded",
        "✅ Emergency Responded",
        f"Your emergency has been responded to by {responder_email}",
        {"alert_id": alert_id}
    )

# ============ RENDER FUNCTIONS ============

def render_notifications_panel():
    if st.session_state.user and st.session_state.current_school:
        unread_count = get_unread_notifications_count(
            st.session_state.current_school['code'],
            st.session_state.user['email']
        )
        
        with st.sidebar.expander(f"🔔 Notifications {f'({unread_count})' if unread_count > 0 else ''}", expanded=False):
            notifications = load_school_data(
                st.session_state.current_school['code'],
                "notifications.json", []
            )
            user_notifications = [n for n in notifications if n['user_email'] == st.session_state.user['email'] and not n['read']]
            
            if user_notifications:
                for notification in sorted(user_notifications, key=lambda x: x['created_at'], reverse=True)[:10]:
                    with st.container():
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.markdown(f"**{notification['title']}**")
                            st.markdown(f"<small>{notification['message']}</small>", unsafe_allow_html=True)
                            st.markdown(f"<small>{notification['created_at'][:16]}</small>", unsafe_allow_html=True)
                        with col2:
                            if st.button("✓", key=f"read_{notification['id']}"):
                                mark_notification_read(
                                    st.session_state.current_school['code'],
                                    notification['id']
                                )
                                st.rerun()
                        st.divider()
            else:
                st.info("No new notifications")

def render_requests_section():
    if st.session_state.user['role'] != 'admin':
        return
    
    with st.sidebar.expander("📋 Pending Requests", expanded=False):
        school_code = st.session_state.current_school['code']
        
        class_requests = load_school_data(school_code, "class_requests.json", [])
        pending_class = [r for r in class_requests if r['status'] == 'pending']
        
        if pending_class:
            st.markdown("#### Class Enrollment")
            for req in pending_class[:5]:
                with st.container():
                    st.markdown(f"**{req['student_name']}** wants to join")
                    st.markdown(f"Class: {req['class_code']}")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅", key=f"accept_class_{req['id']}"):
                            req['status'] = 'accepted'
                            classes = load_school_data(school_code, "classes.json", [])
                            for cls in classes:
                                if cls['code'] == req['class_code']:
                                    cls.setdefault('students', []).append(req['student_email'])
                            save_school_data(school_code, "classes.json", classes)
                            save_school_data(school_code, "class_requests.json", class_requests)
                            st.rerun()
                    with col2:
                        if st.button("❌", key=f"decline_class_{req['id']}"):
                            req['status'] = 'declined'
                            save_school_data(school_code, "class_requests.json", class_requests)
                            st.rerun()
                    st.divider()
        
        group_requests = load_school_data(school_code, "group_requests.json", [])
        pending_group = [r for r in group_requests if r['status'] == 'pending']
        
        if pending_group:
            st.markdown("#### Group Join")
            for req in pending_group[:5]:
                with st.container():
                    st.markdown(f"**{req.get('user_name', 'Someone')}** wants to join")
                    st.markdown(f"Group: {req.get('group_name', req['group_code'])}")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅", key=f"accept_group_{req['id']}"):
                            req['status'] = 'accepted'
                            groups = load_school_data(school_code, "groups.json", [])
                            for group in groups:
                                if group['code'] == req['group_code']:
                                    group.setdefault('members', []).append(req['user_email'])
                            save_school_data(school_code, "groups.json", groups)
                            save_school_data(school_code, "group_requests.json", group_requests)
                            st.rerun()
                    with col2:
                        if st.button("❌", key=f"decline_group_{req['id']}"):
                            req['status'] = 'declined'
                            save_school_data(school_code, "group_requests.json", group_requests)
                            st.rerun()
                    st.divider()

def render_wellness_center():
    st.markdown("### 🧠 Wellness Center")
    
    tab1, tab2, tab3 = st.tabs(["📝 Daily Check-in", "📊 My Wellness", "🆘 Resources"])
    
    with tab1:
        st.markdown("#### How are you feeling today?")
        
        with st.form("wellness_checkin"):
            col1, col2 = st.columns(2)
            
            with col1:
                mood = st.slider("Mood (1-10)", 1, 10, 7)
                stress = st.slider("Stress Level (1-10)", 1, 10, 5)
                sleep = st.number_input("Hours of Sleep", 0.0, 24.0, 7.0, 0.5)
            
            with col2:
                anxiety = st.slider("Anxiety Level (1-10)", 1, 10, 5)
                energy = st.slider("Energy Level (1-10)", 1, 10, 6)
                social = st.slider("Social Connection (1-10)", 1, 10, 6)
            
            notes = st.text_area("Notes (optional)")
            
            if st.form_submit_button("Submit Check-in"):
                if st.session_state.user and st.session_state.current_school:
                    add_wellness_checkin(
                        st.session_state.user['email'],
                        st.session_state.current_school['code'],
                        mood, stress, sleep, anxiety, energy, social, notes
                    )
                    st.success("Check-in recorded! Thank you for sharing.")
                    
                    if stress > 7 or anxiety > 7:
                        st.warning("⚠️ Your stress/anxiety levels seem high. Remember you can talk to our school counselor.")
    
    with tab2:
        if st.session_state.user and st.session_state.current_school:
            checkins = load_school_data(st.session_state.current_school['code'], "wellness_checkins.json", [])
            user_checkins = [c for c in checkins if c['user_email'] == st.session_state.user['email']]
            
            if user_checkins:
                df = pd.DataFrame(user_checkins)
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date')
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Avg Mood", f"{df['mood'].mean():.1f}/10")
                with col2:
                    st.metric("Avg Stress", f"{df['stress'].mean():.1f}/10")
                with col3:
                    st.metric("Avg Sleep", f"{df['sleep'].mean():.1f} hrs")
                
                fig = px.line(df, x='date', y=['mood', 'stress', 'anxiety', 'energy'],
                              title="Wellness Trends",
                              color_discrete_sequence=['#28a745', '#dc3545', '#ffc107', '#17a2b8'])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No check-in data yet. Start tracking your wellness today!")
    
    with tab3:
        st.markdown("""
        #### 📞 Emergency Contacts
        - **School Counselor**: Room 101
        - **Health Center**: Ext 456
        - **Emergency**: 999 / 112
        
        #### 📚 Resources
        - Stress Management Guide
        - Mindfulness Exercises
        - Peer Support Group Schedule
        """)

def render_study_groups():
    st.markdown("### 📚 Study Groups")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Create Study Group")
        with st.form("create_study_group"):
            group_name = st.text_input("Group Name")
            subject = st.selectbox("Subject", PRIMARY_SUBJECTS)
            schedule = st.text_input("Schedule", placeholder="e.g., Mon/Wed 3-4pm")
            max_participants = st.number_input("Max Participants", 2, 20, 10)
            
            if st.form_submit_button("Create Group"):
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
                                    if st.button("Join", key=f"join_{group['id']}"):
                                        if join_study_group(
                                            st.session_state.current_school['code'],
                                            group['id'],
                                            st.session_state.user['email']
                                        ):
                                            st.success(f"Joined {group['name']}!")
                                            st.rerun()
                        st.divider()
            else:
                st.info("No active study groups")

def render_career_guidance():
    st.markdown("### 🎯 Career Guidance")
    
    tab1, tab2 = st.tabs(["🎯 Career Quiz", "💼 Recommendations"])
    
    with tab1:
        st.markdown("#### Discover Your Career Path")
        
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
                ["Analytically", "Creatively", "Practically", "Collaboratively"]
            )
            
            q4 = st.radio(
                "4. What's most important in your career?",
                ["High income", "Helping others", "Creative expression", "Job stability"]
            )
            
            if st.form_submit_button("Get Recommendations"):
                answers = {
                    'q1': q1.lower().split('/')[0],
                    'q2': q2.lower(),
                    'q3': q3.lower(),
                    'q4': q4.lower().split()[0]
                }
                
                recommendations = career_quiz(answers)
                st.session_state.career_recommendations = recommendations
                st.rerun()
    
    with tab2:
        if 'career_recommendations' in st.session_state:
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
    st.markdown("### 🚨 Emergency Alert System")
    st.warning("Only use this for genuine emergencies!")
    
    with st.form("emergency_alert"):
        alert_type = st.selectbox(
            "Alert Type",
            options=list(EMERGENCY_TYPES.keys()),
            format_func=lambda x: EMERGENCY_TYPES[x]['message']
        )
        
        location = st.text_input("Your Location")
        description = st.text_area("Description")
        confirm = st.checkbox("I confirm this is a genuine emergency")
        
        if st.form_submit_button("🚨 SEND EMERGENCY ALERT", type="primary"):
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
                
                if st.form_submit_button("Save Project"):
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
        
        projects = get_user_projects(st.session_state.user['email'], st.session_state.current_school['code'])
        
        if projects:
            for project in projects:
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
                                display_attachment(file)
                    st.divider()
        else:
            st.info("No projects yet. Add your first project!")
    
    with tab2:
        st.markdown("#### Skills")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            with st.form("add_skill"):
                skill = st.text_input("Skill Name")
                level = st.slider("Proficiency Level", 1, 5, 3)
                
                if st.form_submit_button("Add Skill"):
                    add_portfolio_skill(
                        st.session_state.user['email'],
                        st.session_state.current_school['code'],
                        skill,
                        level
                    )
                    st.success("Skill added!")
                    st.rerun()
        
        with col2:
            skills = get_user_skills(
                st.session_state.user['email'],
                st.session_state.current_school['code']
            )
            
            if skills:
                for skill in skills:
                    st.markdown(f"""
                    <div style="margin: 10px 0;">
                        <strong>{skill['skill']}</strong>
                        <div style="background: rgba(255,255,255,0.2); height: 20px; border-radius: 10px;">
                            <div style="background: #FFD700; width: {skill['level']*20}%; 
                                      height: 20px; border-radius: 10px; text-align: center; 
                                      color: black; line-height: 20px;">
                                {skill['level']}/5
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No skills added yet")

def render_calls():
    st.markdown("### 📞 Audio/Video Calls")
    
    tab1, tab2 = st.tabs(["📞 Make a Call", "📋 Active Calls"])
    
    with tab1:
        st.markdown("#### Start a Call")
        
        if st.session_state.user and st.session_state.current_school:
            users = load_school_data(st.session_state.current_school['code'], "users.json", [])
            all_users = [u for u in users if u['email'] != st.session_state.user['email']]
            
            col1, col2 = st.columns(2)
            
            with col1:
                call_type = st.radio("Call Type", ["🎧 Audio Call", "📹 Video Call"])
                actual_call_type = "audio" if "Audio" in call_type else "video"
            
            with col2:
                call_target = st.radio("Call Target", ["Individual", "Group", "Class"])
            
            recipients = []
            
            if call_target == "Individual":
                selected_users = st.multiselect(
                    "Select recipient",
                    [f"{u['fullname']} ({u['role']})" for u in all_users],
                    max_selections=1
                )
                recipients = [u.split('(')[1].rstrip(')').strip() for u in selected_users]
            
            elif call_target == "Group":
                selected_users = st.multiselect(
                    "Select recipients",
                    [f"{u['fullname']} ({u['role']})" for u in all_users]
                )
                recipients = [u.split('(')[1].rstrip(')').strip() for u in selected_users]
            
            elif call_target == "Class":
                classes = load_school_data(st.session_state.current_school['code'], "classes.json", [])
                if st.session_state.user['role'] == 'teacher':
                    my_classes = [c for c in classes if c.get('teacher') == st.session_state.user['email']]
                    if my_classes:
                        selected_class = st.selectbox("Select Class", [c['name'] for c in my_classes])
                        class_obj = next((c for c in my_classes if c['name'] == selected_class), None)
                        if class_obj:
                            recipients = class_obj.get('students', [])
                    else:
                        st.warning("You don't have any classes")
                else:
                    selected_class = st.selectbox("Select Class", [c['name'] for c in classes])
                    class_obj = next((c for c in classes if c['name'] == selected_class), None)
                    if class_obj:
                        recipients = class_obj.get('students', [])
            
            room_name = st.text_input("Room Name (optional)")
            
            if st.button("🚀 Start Call", type="primary"):
                if recipients:
                    call = create_call(
                        st.session_state.current_school['code'],
                        st.session_state.user['email'],
                        recipients,
                        actual_call_type,
                        room_name if room_name else None
                    )
                    st.success(f"Call initiated! Ringing {len(recipients)} participant(s)...")
                    st.session_state.active_call = call
                    st.rerun()
                else:
                    st.error("Please select at least one recipient")
    
    with tab2:
        st.markdown("#### Active Calls")
        
        if st.session_state.user and st.session_state.current_school:
            calls = get_user_calls(
                st.session_state.current_school['code'],
                st.session_state.user['email']
            )
            
            active_calls = [c for c in calls if c['status'] in ['ringing', 'active']]
            
            if active_calls:
                for call in active_calls:
                    with st.container():
                        users_list = load_school_data(st.session_state.current_school['code'], "users.json", [])
                        caller = next((u for u in users_list if u['email'] == call['caller']), None)
                        caller_name = caller['fullname'] if caller else call['caller']
                        
                        call_icon = "🎧" if call['call_type'] == 'audio' else "📹"
                        
                        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
                        
                        with col1:
                            status_emoji = "🔔" if call['status'] == 'ringing' else "🟢"
                            st.markdown(f"{status_emoji} {call_icon} {call['room_name']}")
                        
                        with col2:
                            st.markdown(f"By: {caller_name}")
                            st.markdown(f"Participants: {len(call['answered_by'])}/{len(call['recipients']) + 1}")
                        
                        with col3:
                            if call['status'] == 'ringing' and st.session_state.user['email'] in call['recipients']:
                                if st.button("Answer", key=f"answer_{call['id']}"):
                                    if answer_call(
                                        st.session_state.current_school['code'],
                                        call['id'],
                                        st.session_state.user['email']
                                    ):
                                        st.session_state.active_call = call
                                        st.rerun()
                        
                        with col4:
                            if st.button("End", key=f"end_{call['id']}"):
                                end_call(
                                    st.session_state.current_school['code'],
                                    call['id'],
                                    st.session_state.user['email']
                                )
                                if 'active_call' in st.session_state and st.session_state.active_call['id'] == call['id']:
                                    del st.session_state.active_call
                                st.rerun()
                        
                        st.divider()
            else:
                st.info("No active calls")
    
    if 'active_call' in st.session_state:
        st.markdown("---")
        st.markdown("### 🟢 Active Call")
        call = st.session_state.active_call
        
        with st.container():
            st.markdown(f"""
            <div class="call-container">
                <h3>{'🎧' if call['call_type'] == 'audio' else '📹'} {call['room_name']}</h3>
                <p><strong>Type:</strong> {call['call_type'].title()} Call</p>
                <p><strong>Started:</strong> {call['started_at']}</p>
                <p><strong>Status:</strong> {call['status'].title()}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### Participants")
            all_participants = [call['caller']] + call['recipients']
            
            for participant in all_participants:
                user = next((u for u in users if u['email'] == participant), None)
                name = user['fullname'] if user else participant
                if participant in call['answered_by']:
                    st.markdown(f"🟢 **{name}** (Connected)")
                elif participant == call['caller']:
                    st.markdown(f"🟡 **{name}** (Host)")
                else:
                    st.markdown(f"🔴 **{name}** (Ringing...)")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🔇 Mute"):
                    st.info("Muted (simulated)")
            with col2:
                if st.button("🎤 Unmute"):
                    st.info("Unmuted (simulated)")
            with col3:
                if st.button("📹 Camera"):
                    st.info("Camera toggled (simulated)")
            
            if st.button("🚫 End Call", type="primary"):
                end_call(
                    st.session_state.current_school['code'],
                    call['id'],
                    st.session_state.user['email']
                )
                del st.session_state.active_call
                st.rerun()

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
if 'viewing_student' not in st.session_state:
    st.session_state.viewing_student = None
if 'active_call' not in st.session_state:
    st.session_state.active_call = None
if 'career_recommendations' not in st.session_state:
    st.session_state.career_recommendations = None

# ============ MAIN APP ============

if st.session_state.user and st.session_state.current_school:
    settings = load_user_settings(st.session_state.current_school['code'], st.session_state.user['email'])
    st.session_state.theme = settings.get("theme", "Sunrise Glow")
    st.session_state.wallpaper = settings.get("wallpaper", "None")

st.markdown(get_theme_css(st.session_state.theme, st.session_state.wallpaper), unsafe_allow_html=True)

# ----- WELCOME PAGE -----
if st.session_state.page == 'welcome':
    st.markdown('<h1>✨ School Community Hub ✨</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: white; font-size: 1.2rem;">Connect • Collaborate • Manage • Shine</p>', unsafe_allow_html=True)
    st.divider()
    
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
                    school_code = st.text_input("School Code")
                    admin_email = st.text_input("Email")
                    admin_password = st.text_input("Password", type="password")
                    if st.form_submit_button("Login"):
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
                    school_name = st.text_input("School Name")
                    admin_name = st.text_input("Your Full Name")
                    admin_email = st.text_input("Your Email")
                    password = st.text_input("Password", type="password")
                    confirm = st.text_input("Confirm Password", type="password")
                    city = st.text_input("City")
                    state = st.text_input("State/Province")
                    motto = st.text_input("School Motto")
                    
                    if st.form_submit_button("Create School"):
                        if not school_name or not admin_email or not password:
                            st.error("School name, email and password are required")
                        elif password != confirm:
                            st.error("Passwords do not match")
                        else:
                            all_schools = load_all_schools()
                            
                            email_exists = False
                            for s_code, s_data in all_schools.items():
                                if s_data['admin_email'] == admin_email:
                                    email_exists = True
                                    break
                            
                            if email_exists:
                                st.error("This email is already registered with another school")
                                st.stop()
                            
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
                            save_school_data(code, "notifications.json", [])
                            save_school_data(code, "calls.json", [])
                            save_school_data(code, "portfolio_projects.json", [])
                            save_school_data(code, "portfolio_skills.json", [])
                            save_school_data(code, "wellness_checkins.json", [])
                            save_school_data(code, "study_groups.json", [])
                            save_school_data(code, "career_assessments.json", [])
                            save_school_data(code, "emergency_alerts.json", [])
                            
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
                    school_code = st.text_input("School Code")
                    email = st.text_input("Email")
                    password = st.text_input("Password", type="password")
                    if st.form_submit_button("Login"):
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
                    school_code = st.text_input("School Code")
                    teacher_code = st.text_input("Teacher Code")
                    fullname = st.text_input("Full Name")
                    email = st.text_input("Email")
                    password = st.text_input("Password", type="password")
                    confirm = st.text_input("Confirm Password", type="password")
                    
                    if st.form_submit_button("Register"):
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
                    school_code = st.text_input("School Code")
                    admission_number = st.text_input("Admission Number")
                    password = st.text_input("Password", type="password")
                    if st.form_submit_button("Login"):
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
                    school_code = st.text_input("School Code")
                    fullname = st.text_input("Full Name")
                    email = st.text_input("Email (Optional)")
                    password = st.text_input("Password", type="password")
                    confirm = st.text_input("Confirm Password", type="password")
                    
                    if st.form_submit_button("Register"):
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
                                
                                add_library_member(school_code, new_user['email'], "student")
                                
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
                    if st.form_submit_button("Login"):
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
                    school_code = st.text_input("School Code")
                    student_admission = st.text_input("Student's Admission Number")
                    fullname = st.text_input("Your Full Name")
                    email = st.text_input("Your Email")
                    phone = st.text_input("Phone Number")
                    password = st.text_input("Password", type="password")
                    confirm = st.text_input("Confirm Password", type="password")
                    
                    if st.form_submit_button("Register"):
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
            if st.button("Go to Management Dashboard"):
                st.session_state.page = 'dashboard'
                st.rerun()
        else:
            st.warning("⚠️ Please log in first to access the School Management System.")
            st.info("Go to the School Community tab and log in with your admin or teacher account.")
    
    elif st.session_state.main_nav == 'Personal Dashboard':
        st.markdown("""
        <div class="golden-card" style="text-align: center;">
            <h3>👤 Personal Dashboard</h3>
            <p>Your personal information, performance, reviews, achievements, and portfolio!</p>
            <p style="font-size: 0.9rem;">Please log in with your student or guardian credentials to view your personal dashboard.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.user and st.session_state.current_school:
            st.success(f"✅ Logged in as: {st.session_state.user['fullname']} ({st.session_state.user['role']})")
            if st.button("Go to Personal Dashboard"):
                st.session_state.page = 'dashboard'
                st.rerun()
        else:
            st.warning("⚠️ Please log in first to view your Personal Dashboard.")
            st.info("Go to the School Community tab and log in with your student or guardian account.")

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
    academic_records = load_school_data(school_code, "academic_records.json", [])
    library_books = load_school_data(school_code, "library_books.json", [])
    library_members = load_school_data(school_code, "library_members.json", [])
    library_transactions = load_school_data(school_code, "library_transactions.json", [])
    
    unread_count = get_unread_count(user['email'], school_code)
    pending_friend_count = len(get_pending_requests(school_code, user['email']))
    
    user_member = next((m for m in library_members if m['email'] == user['email']), None)
    borrowed_books = user_member.get('borrowed_books', []) if user_member else []
    
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
        <div style="color: #FFD700; flex: 1;">
            <strong>{user['fullname']}</strong><br>
            <span style="background: rgba(0,0,0,0.3); color: #FFD700; padding: 2px 8px; border-radius: 12px; font-size: 0.7rem; border: 1px solid #FFD700;">{role_display}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        
        # Base navigation options
        base_options = ["Dashboard", "Announcements", "Community", f"Chat 💬{f' ({unread_count})' if unread_count>0 else ''}", f"Group Chats 👥", f"Friends 🤝{f' ({pending_friend_count})' if pending_friend_count>0 else ''}"]
        
        if user['role'] == 'admin':
            options = base_options + ["Classes", "Groups", "Teachers", "Students", "Guardians", "Assignments", "School Management", "Library Management", "Settings ⚙️", "Profile"]
        elif user['role'] == 'teacher':
            options = base_options + ["My Classes", "Groups", "Assignments", "School Management", "Library Management", "Settings ⚙️", "Profile"]
        elif user['role'] == 'student':
            options = base_options + ["Browse Classes", "My Classes", "Groups", "Assignments", "My Library", "Settings ⚙️", "Profile"]
        else:  # guardian
            options = base_options + ["My Student", "Assignments", "My Library", "Settings ⚙️", "Profile"]
        
        if st.session_state.menu_index >= len(options):
            st.session_state.menu_index = 0
            
        menu = st.radio("Navigation", options, index=st.session_state.menu_index, label_visibility="collapsed")
        st.session_state.menu_index = options.index(menu)
        
        st.divider()
        
        # Notifications panel
        render_notifications_panel()
        
        # Requests section for admins
        render_requests_section()
        
        st.divider()
        
        # New Features Section (only on Personal Dashboard)
        if st.session_state.main_nav == 'Personal Dashboard' and user['role'] in ['student', 'guardian']:
            st.sidebar.markdown("### 🆕 New Features")
            
            if st.sidebar.button("🧠 Wellness Center", key="nav_wellness", use_container_width=True):
                st.session_state.current_feature = 'wellness'
                st.rerun()
            
            if st.sidebar.button("📚 Study Groups", key="nav_study", use_container_width=True):
                st.session_state.current_feature = 'study_groups'
                st.rerun()
            
            if st.sidebar.button("🎯 Career Guidance", key="nav_career", use_container_width=True):
                st.session_state.current_feature = 'career'
                st.rerun()
            
            if st.sidebar.button("📁 Portfolio", key="nav_portfolio", use_container_width=True):
                st.session_state.current_feature = 'portfolio'
                st.rerun()
        
        # Calls section (available to all)
        st.sidebar.markdown("### 📞 Communication")
        if st.sidebar.button("📞 Audio/Video Calls", key="nav_calls", use_container_width=True):
            st.session_state.current_feature = 'calls'
            st.rerun()
        
        st.sidebar.divider()
        
        # Emergency Alert (always available)
        if st.sidebar.button("🚨 EMERGENCY ALERT", key="nav_emergency", use_container_width=True, type="primary"):
            st.session_state.current_feature = 'emergency'
            st.rerun()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.session_state.current_school = None
            st.session_state.page = 'welcome'
            st.rerun()
    
    # ============ MAIN CONTENT ============
    
    # Handle feature routing
    if 'current_feature' in st.session_state and st.session_state.current_feature:
        if st.session_state.current_feature == 'wellness':
            render_wellness_center()
        elif st.session_state.current_feature == 'study_groups':
            render_study_groups()
        elif st.session_state.current_feature == 'career':
            render_career_guidance()
        elif st.session_state.current_feature == 'portfolio':
            render_portfolio()
        elif st.session_state.current_feature == 'calls':
            render_calls()
        elif st.session_state.current_feature == 'emergency':
            render_emergency_alerts()
        
        if st.button("← Back to Dashboard", key="back_to_dash", use_container_width=True):
            st.session_state.current_feature = None
            st.rerun()
    
    # Regular menu items
    elif menu == "Dashboard":
        st.markdown(f"<h2 style='text-align: center;'>Welcome, {user['fullname']}!</h2>", unsafe_allow_html=True)
        
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
                    
                    if st.form_submit_button("📢 Post Announcement"):
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
                        col1, col2 = st.columns([5, 1])
                        with col1:
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
                        with col2:
                            if user['role'] == 'admin' or user['email'] == ann['author_email']:
                                if st.button("🗑️", key=f"del_ann_{ann['id']}"):
                                    if delete_announcement(school_code, ann['id'], user['email']):
                                        st.success("Announcement deleted!")
                                        st.rerun()
        else:
            st.info("No announcements yet")
    
    # ... (rest of the existing menu code - Assignments, Community, Friends, Chat, Group Chats, Classes, etc.)
    # I'm truncating here for brevity since you already have that code
    
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
            with st.form("edit_profile_dash"):
                name = st.text_input("Full Name", user['fullname'])
                phone = st.text_input("Phone", user.get('phone', ''))
                bio = st.text_area("Bio", user.get('bio', ''), height=100)
                
                if st.form_submit_button("💾 Update Profile"):
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
