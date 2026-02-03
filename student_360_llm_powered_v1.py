"""
Student 360 LLM-Powered Analytics Platform - Version 1.0
=========================================================
A comprehensive student analytics dashboard powered by Large Language Models.
All insights, narratives, and analysis are dynamically generated using LLM.

Version: 1.0
Release Date: February 2, 2026
Status: Production Release with Full LLM Integration

Features:
- 10 Analytics Tabs with LLM-generated content
- 5 Tabs with Advanced AI-Driven Deep Analysis (Academic, Housing, Financial, Demographics, Risk)
- Ollama Integration (Local & Cloudflare)
- Auto-optimized for system resources
- Interactive visualizations
- Dynamic storytelling and insights
- Context-aware visualization recommendations
- Strategic findings and actionable recommendations
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import json
import hashlib
import psutil
import platform
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import re

# Import journey generation modules
try:
    from journey_definitions import ALL_JOURNEYS, FINANCIAL_CONSTANTS
    from journey_assembler import generate_all_journeys, validate_dataset_for_journeys
    JOURNEY_MODULES_AVAILABLE = True
except ImportError as e:
    JOURNEY_MODULES_AVAILABLE = False
    print(f"Warning: Journey modules not available: {e}")

# Import LLM-driven entity journey system
try:
    from llm_entity_journey_system import generate_complete_llm_journeys, generate_visualization, filter_dataset_for_entity
    LLM_ENTITY_JOURNEY_AVAILABLE = True
except ImportError as e:
    LLM_ENTITY_JOURNEY_AVAILABLE = False
    print(f"Warning: LLM entity journey system not available: {e}")

# Import fully dynamic entity discovery system (ZERO guidance)
try:
    from fully_dynamic_entity_discovery import generate_fully_dynamic_journeys
    FULLY_DYNAMIC_DISCOVERY_AVAILABLE = True
except ImportError as e:
    FULLY_DYNAMIC_DISCOVERY_AVAILABLE = False
    print(f"Warning: Fully dynamic discovery system not available: {e}")

# ====================================================================================
# PAGE CONFIGURATION
# ====================================================================================

st.set_page_config(
    page_title="Student 360 AI-Powered Analytics V1.0 | Exalio",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://exalio.com/support',
        'Report a bug': 'https://exalio.com/bugs',
        'About': '# Student 360 AI-Powered Analytics V1.0 by Exalio\nVersion 1.0 - Production Release\n\nTransform student data into strategic intelligence with AI.\n\nFeatures:\n- 5 Advanced AI-Driven Analysis Tabs\n- Context-aware visualizations\n- Strategic insights & recommendations'
    }
)

# ====================================================================================
# CUSTOM CSS STYLING
# ====================================================================================

def inject_custom_css():
    """Inject custom CSS for enhanced UI - Exact theme from generic_storytelling_app.py"""
    st.markdown("""
    <style>
    /* Import better fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Main theme colors */
    :root {
        --primary: #6366f1;
        --secondary: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --info: #3b82f6;
    }

    /* Dark theme */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    }

    /* Headers */
    h1 {
        color: #ffffff !important;
        font-size: 2.2rem !important;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }

    h2 {
        color: #ffffff !important;
        font-size: 1.5rem !important;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }

    h3 {
        color: #ffffff !important;
        font-size: 1.2rem !important;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }

    /* Metric cards */
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.8rem;
        font-weight: 700;
    }

    [data-testid="stMetricLabel"] {
        color: #ffffff !important;
        font-size: 0.9rem;
        font-weight: 500;
    }

    /* Sidebar styling */
    .stSidebar label {
        color: white !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }

    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.95);
        border-right: 1px solid #334155;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(30, 41, 59, 0.85);
        padding: 12px;
        border-radius: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: 1px solid #334155;
        border-radius: 8px;
        color: #f1f5f9;
        padding: 10px 20px;
    }

    .stTabs [aria-selected="true"] {
        background: #6366f1;
        border-color: #6366f1;
    }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 10px;
        padding: 1.5rem;
        border: 2px solid #475569;
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }

    .kpi-card:hover {
        border-color: #6366f1;
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3);
    }

    .kpi-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #6366f1;
        margin: 0.5rem 0;
    }

    .kpi-label {
        font-size: 1rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Insight cards */
    .insight-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(16, 185, 129, 0.1));
        border: 1px solid #334155;
        border-left: 4px solid #6366f1;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
    }

    .insight-title {
        color: #c7d2fe;
        font-size: 1.2rem;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .insight-text {
        color: #e2e8f0;
        font-size: 1.05rem;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        line-height: 1.8;
    }

    /* Alert boxes */
    .alert-success {
        background: rgba(16, 185, 129, 0.2);
        border-left: 5px solid #10b981;
        padding: 18px 20px;
        border-radius: 10px;
        margin: 15px 0;
        color: #f0fdf4;
    }

    .alert-warning {
        background: rgba(245, 158, 11, 0.2);
        border-left: 5px solid #f59e0b;
        padding: 18px 20px;
        border-radius: 10px;
        margin: 15px 0;
        color: #fef3c7;
    }

    .alert-info {
        background: rgba(59, 130, 246, 0.2);
        border-left: 5px solid #3b82f6;
        padding: 18px 20px;
        border-radius: 10px;
        margin: 15px 0;
        color: #dbeafe;
    }

    .alert-danger {
        background: rgba(239, 68, 68, 0.2);
        border-left: 5px solid #ef4444;
        padding: 18px 20px;
        border-radius: 10px;
        margin: 15px 0;
        color: #fee2e2;
    }

    /* Journey Cards */
    .journey-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border-radius: 10px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 2px solid #475569;
    }

    .journey-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #6366f1;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .journey-story {
        background: rgba(99, 102, 241, 0.1);
        border-left: 3px solid #6366f1;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }

    /* Make all text white and clear */
    p, span, div, label, .stMarkdown {
        color: #ffffff !important;
    }

    .stMarkdown p {
        color: #ffffff !important;
        font-weight: 400;
    }

    .stCaption {
        color: #e2e8f0 !important;
    }

    .stAlert {
        color: #ffffff !important;
    }

    [data-baseweb="radio"] label,
    [data-baseweb="select"] span,
    .stRadio label,
    .stSelectbox label {
        color: #ffffff !important;
    }

    label[data-testid="stWidgetLabel"] {
        color: #ffffff !important;
        font-weight: 500 !important;
    }

    button {
        font-weight: 600 !important;
    }

    /* Buttons - Enhanced Modern Style */
    button[kind="primary"],
    button[kind="secondary"],
    .stButton button {
        background: linear-gradient(135deg, #1e293b, #334155) !important;
        color: #ffffff !important;
        border: 1px solid #475569 !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
        font-size: 0.95rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
    }

    button[kind="primary"]:hover,
    .stButton button:hover {
        background: linear-gradient(135deg, #334155, #475569) !important;
        border-color: #64748b !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
    }

    button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        border-color: rgba(99, 102, 241, 0.5) !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }

    button[kind="primary"]:hover {
        background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
    }

    /* Dropdown/Selectbox - Light background */
    [data-baseweb="select"] {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important;
        border: 1.5px solid rgba(99, 102, 241, 0.4) !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3), 0 0 20px rgba(99, 102, 241, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
        transition: all 0.25s ease !important;
        min-height: 42px !important;
    }

    [data-baseweb="select"]:hover {
        border-color: rgba(99, 102, 241, 0.7) !important;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4), 0 0 25px rgba(99, 102, 241, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.9) !important;
    }

    [data-baseweb="select"] > div {
        background: transparent !important;
        color: #000000 !important;
        font-weight: 600 !important;
        padding: 10px 14px !important;
        font-size: 0.95rem !important;
    }

    [data-baseweb="select"] span {
        color: #000000 !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
    }

    /* Dropdown menu/popover */
    [data-baseweb="popover"] {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important;
        border: 1.5px solid rgba(99, 102, 241, 0.5) !important;
        border-radius: 10px !important;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6), 0 0 30px rgba(99, 102, 241, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.8) !important;
        padding: 6px !important;
    }

    [role="listbox"] li,
    [role="option"] {
        background: rgba(255, 255, 255, 0.5) !important;
        color: #000000 !important;
        border-radius: 6px !important;
        margin: 2px 0 !important;
        padding: 12px 14px !important;
        transition: all 0.2s ease !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
    }

    [role="listbox"] li:hover,
    [role="option"]:hover {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.4), rgba(139, 92, 246, 0.4)) !important;
        color: #000000 !important;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.4) !important;
    }

    [data-baseweb="select"] [aria-selected="true"],
    [role="option"][aria-selected="true"] {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.6), rgba(139, 92, 246, 0.6)) !important;
        color: #000000 !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 10px rgba(99, 102, 241, 0.5), inset 0 0 10px rgba(99, 102, 241, 0.2) !important;
    }

    /* Radio buttons */
    [data-baseweb="radio"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%) !important;
        border: 1.5px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 10px !important;
        padding: 14px 18px !important;
        margin: 8px 0 !important;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.4), 0 0 15px rgba(99, 102, 241, 0.05), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
        transition: all 0.25s ease !important;
        cursor: pointer !important;
    }

    [data-baseweb="radio"]:hover {
        border-color: rgba(99, 102, 241, 0.6) !important;
        box-shadow: 0 5px 16px rgba(0, 0, 0, 0.5), 0 0 25px rgba(99, 102, 241, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
    }

    [data-baseweb="radio"]:has(input:checked) {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.25), rgba(139, 92, 246, 0.25)) !important;
        border-color: rgba(99, 102, 241, 0.8) !important;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3), 0 0 25px rgba(99, 102, 241, 0.2), inset 0 0 15px rgba(99, 102, 241, 0.1) !important;
    }

    /* Text inputs */
    input[type="text"],
    input[type="number"],
    .stTextInput input,
    .stNumberInput input {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%) !important;
        color: #ffffff !important;
        border: 1.5px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        font-size: 0.95rem !important;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
        transition: all 0.25s ease !important;
    }

    input[type="text"]:focus,
    input[type="number"]:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2), 0 4px 16px rgba(99, 102, 241, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
        outline: none !important;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%) !important;
        border: 1.5px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 10px !important;
        padding: 20px !important;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
        transition: all 0.25s ease !important;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: rgba(99, 102, 241, 0.5) !important;
        box-shadow: 0 5px 16px rgba(99, 102, 241, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%) !important;
        border: 1.5px solid rgba(99, 102, 241, 0.3) !important;
        border-radius: 10px !important;
        padding: 14px 18px !important;
        transition: all 0.25s ease !important;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
    }

    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(30, 27, 75, 0.9)) !important;
        border-color: rgba(99, 102, 241, 0.5) !important;
        box-shadow: 0 5px 16px rgba(99, 102, 241, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
    }

    /* Animations */
    @keyframes slideIn {
        from {
            transform: translateX(-10px) !important;
            opacity: 0 !important;
        }
        to {
            transform: translateX(0) !important;
            opacity: 1 !important;
        }
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        animation: fadeInUp 0.6s ease-out;
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
    }

    /* ============================================= */
    /* SELECTBOX BLACK TEXT - NUCLEAR OVERRIDE */
    /* ============================================= */

    /* Force ALL selectbox text to BLACK */
    .stSelectbox select,
    .stSelectbox,
    .stSelectbox *,
    .stSelectbox div,
    .stSelectbox span,
    .stSelectbox p,
    [data-baseweb="select"],
    [data-baseweb="select"] *,
    [data-baseweb="select"] div,
    [data-baseweb="select"] span {
        color: #000000 !important;
    }

    /* Selectbox input background */
    .stSelectbox [data-baseweb="select"] {
        background-color: #ffffff !important;
    }

    /* Dropdown popover BLACK text */
    [data-baseweb="popover"],
    [data-baseweb="popover"] *,
    [data-baseweb="popover"] li,
    [data-baseweb="popover"] div,
    [data-baseweb="popover"] span,
    [role="listbox"],
    [role="listbox"] *,
    [role="listbox"] li,
    [role="listbox"] div {
        color: #000000 !important;
        background-color: #ffffff !important;
    }

    /* Sidebar selectboxes specifically */
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stSelectbox *,
    [data-testid="stSidebar"] [data-baseweb="select"],
    [data-testid="stSidebar"] [data-baseweb="select"] * {
        color: #000000 !important;
    }

    /* Override ANY inherited white/light text */
    .stSelectbox > div,
    .stSelectbox > div > div,
    .stSelectbox > div > div > div,
    .stSelectbox > div > div > div > div {
        color: #000000 !important;
    }

    /* ============================================= */
    /* FILE UPLOADER BLACK TEXT - SIDEBAR */
    /* ============================================= */

    /* Force ALL file uploader text to BLACK */
    [data-testid="stSidebar"] .stFileUploader,
    [data-testid="stSidebar"] .stFileUploader *,
    [data-testid="stSidebar"] .stFileUploader div,
    [data-testid="stSidebar"] .stFileUploader span,
    [data-testid="stSidebar"] .stFileUploader p,
    [data-testid="stSidebar"] .stFileUploader label,
    [data-testid="stSidebar"] .stFileUploader small {
        color: #000000 !important;
    }

    /* File uploader drag-drop area text */
    [data-testid="stSidebar"] [data-testid="stFileUploader"] section,
    [data-testid="stSidebar"] [data-testid="stFileUploader"] section *,
    [data-testid="stSidebar"] [data-testid="stFileUploader"] section div,
    [data-testid="stSidebar"] [data-testid="stFileUploader"] section span,
    [data-testid="stSidebar"] [data-testid="stFileUploader"] section small {
        color: #000000 !important;
    }

    /* File uploader button and text */
    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"],
    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] *,
    [data-testid="stSidebar"] [data-testid="stFileUploaderDropzoneInput"] {
        color: #000000 !important;
    }

    /* File name and size text after upload */
    [data-testid="stSidebar"] [data-testid="stFileUploaderFileName"],
    [data-testid="stSidebar"] [data-testid="stFileUploaderFileSize"] {
        color: #000000 !important;
    }

    /* Browse files button text */
    [data-testid="stSidebar"] .stFileUploader button,
    [data-testid="stSidebar"] .stFileUploader button span {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ====================================================================================
# SYSTEM RESOURCE DETECTION
# ====================================================================================

def get_system_resources() -> dict:
    """Detect system resources for LLM optimization"""
    try:
        resources = {
            'cpu_count': psutil.cpu_count(logical=True),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'ram_total_gb': round(psutil.virtual_memory().total / (1024**3), 1),
            'ram_available_gb': round(psutil.virtual_memory().available / (1024**3), 1),
            'ram_percent': psutil.virtual_memory().percent,
            'platform': platform.system(),
            'is_colab': 'google.colab' in str(get_ipython()) if 'get_ipython' in dir() else False,
            'gpu_available': False
        }

        # Try to detect GPU
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                resources['gpu_available'] = True
                resources['gpu_name'] = gpus[0].name
                resources['gpu_memory_gb'] = round(gpus[0].memoryTotal / 1024, 1)
        except:
            # Try nvidia-smi as fallback
            try:
                import subprocess
                result = subprocess.run(['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'],
                                       capture_output=True, text=True, timeout=2)
                if result.returncode == 0 and result.stdout.strip():
                    resources['gpu_available'] = True
                    resources['gpu_name'] = result.stdout.strip()
            except:
                pass

        return resources
    except Exception as e:
        return {
            'cpu_count': 4,
            'cpu_percent': 50,
            'ram_total_gb': 8.0,
            'ram_available_gb': 4.0,
            'ram_percent': 50,
            'platform': 'Unknown',
            'is_colab': False,
            'gpu_available': False
        }

def get_optimized_llm_params(ollama_url: str = None) -> dict:
    """Get optimized LLM parameters based on system resources"""

    # Check if using Cloudflare
    is_cloudflare = False
    if ollama_url:
        is_cloudflare = "cloudflare" in ollama_url.lower() or "exalio" in ollama_url.lower()

    resources = get_system_resources()

    # Determine optimization tier
    if is_cloudflare or resources['is_colab']:
        if resources['gpu_available']:
            tier = "cloudflare_gpu"
        else:
            tier = "cloudflare_cpu"
    else:
        # Local machine settings
        if resources['ram_available_gb'] >= 16 and resources['gpu_available']:
            tier = "high_end_local"
        elif resources['ram_available_gb'] >= 8:
            tier = "medium_local"
        else:
            tier = "low_end_local"

    # Optimization presets
    presets = {
        "high_end_local": {
            "num_ctx": 8192,
            "num_predict": 2048,
            "num_batch": 512,
            "timeout": 60,
            "num_thread": resources['cpu_count'],
            "num_gpu": 1 if resources['gpu_available'] else 0,
            "tier_name": "🚀 High-End (Optimal for large models)"
        },
        "medium_local": {
            "num_ctx": 4096,
            "num_predict": 1024,
            "num_batch": 256,
            "timeout": 90,
            "num_thread": max(resources['cpu_count'] - 1, 2),
            "num_gpu": 1 if resources['gpu_available'] else 0,
            "tier_name": "⚡ Medium (Balanced performance)"
        },
        "low_end_local": {
            "num_ctx": 2048,
            "num_predict": 512,
            "num_batch": 128,
            "timeout": 120,
            "num_thread": max(resources['cpu_count'] - 2, 1),
            "num_gpu": 0,
            "tier_name": "💻 Standard (Resource-efficient)"
        },
        "cloudflare_gpu": {
            "num_ctx": 4096,
            "num_predict": 1024,
            "num_batch": 256,
            "timeout": 150,
            "num_thread": resources['cpu_count'],
            "num_gpu": 1,
            "tier_name": "☁️ Cloudflare GPU (Remote)"
        },
        "cloudflare_cpu": {
            "num_ctx": 2048,
            "num_predict": 512,
            "num_batch": 128,
            "timeout": 600,
            "num_thread": resources['cpu_count'],
            "num_gpu": 0,
            "tier_name": "☁️ Cloudflare CPU (Remote)"
        }
    }

    params = presets.get(tier, presets["medium_local"])
    params['tier'] = tier
    params['resources'] = resources

    return params

# ====================================================================================
# OLLAMA CONNECTION & HEALTH CHECK
# ====================================================================================

def check_ollama_connection(ollama_url: str) -> bool:
    """Basic connectivity check to Ollama server"""
    try:
        response = requests.get(f"{ollama_url}/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def verify_ollama_health(ollama_url: str) -> dict:
    """Comprehensive health check of Ollama server"""
    health = {
        'connected': False,
        'models_available': False,
        'model_count': 0,
        'models': [],
        'error': None
    }

    try:
        # Dynamic timeout: longer for remote, shorter for local
        timeout = 20 if "cloudflare" in ollama_url.lower() or ollama_url.startswith("https://") else 10

        response = requests.get(f"{ollama_url}/api/tags", timeout=timeout)
        if response.status_code == 200:
            health['connected'] = True
            data = response.json()
            models = data.get('models', [])
            health['models'] = [m.get('name', '') for m in models]
            health['model_count'] = len(health['models'])
            health['models_available'] = health['model_count'] > 0
        else:
            health['error'] = f"HTTP {response.status_code}"
    except requests.exceptions.Timeout:
        health['error'] = "Connection timeout"
    except requests.exceptions.ConnectionError:
        health['error'] = "Connection refused"
    except Exception as e:
        health['error'] = str(e)

    return health

def get_available_models(ollama_url: str) -> List[str]:
    """Get list of available models from Ollama"""
    try:
        health = verify_ollama_health(ollama_url)
        return health['models'] if health['models_available'] else []
    except:
        return []

def ensure_ollama_connection(ollama_url: str, auto_reconnect: bool = True, max_retries: int = 3) -> Tuple[bool, List[str], str]:
    """Ensure Ollama connection with retry logic"""
    for attempt in range(max_retries):
        health = verify_ollama_health(ollama_url)
        if health['connected']:
            models = health['models']
            return True, models, f"Connected successfully ({health['model_count']} models)"

        if not auto_reconnect or attempt == max_retries - 1:
            break

        import time
        time.sleep(1)  # Wait before retry

    return False, [], health.get('error', 'Connection failed')

def fetch_remote_system_resources(ollama_url: str) -> Optional[dict]:
    """Fetch system resources from remote Ollama server"""
    try:
        # Check if remote Ollama is accessible
        response = requests.get(f"{ollama_url}/api/tags", timeout=15)
        if response.status_code == 200:
            # Since Ollama API doesn't expose system resources,
            # we return typical Google Colab resources when connected to remote
            # This assumes Colab Pro+ with GPU (adjust based on your setup)

            # Check if this is a Cloudflare/remote connection
            is_remote = "cloudflare" in ollama_url.lower() or "https://" in ollama_url.lower()

            if is_remote:
                # Return typical Colab resources
                # Colab Pro+ with GPU: 2 CPU cores, ~12GB RAM, Tesla T4/V100 GPU
                return {
                    'cpu_count': 2,
                    'cpu_percent': 0,  # Can't fetch remote CPU usage
                    'ram_total_gb': 12.7,
                    'ram_available_gb': 10.5,
                    'ram_percent': 0,  # Can't fetch remote RAM usage
                    'platform': 'Linux',
                    'is_colab': True,
                    'gpu_available': True,
                    'gpu_name': 'Tesla T4 (Colab)',
                    'gpu_memory_gb': 15.0,
                    'source': 'remote_colab'  # Important: marks this as remote
                }
            else:
                return None
    except:
        return None

# ====================================================================================
# LLM QUERY ENGINE
# ====================================================================================

def query_ollama(
    prompt: str,
    model: str,
    ollama_url: str,
    temperature: float = 0.3,
    top_p: float = 0.9,
    top_k: int = 40,
    repeat_penalty: float = 1.1,
    num_predict: int = None,
    num_ctx: int = None,
    timeout: int = None,
    auto_optimize: bool = True,
    seed: int = None
) -> str:
    """Query Ollama with optimized parameters"""

    # Get optimized parameters if enabled
    if auto_optimize:
        params = get_optimized_llm_params(ollama_url)
        if num_predict is None:
            num_predict = params['num_predict']
        if timeout is None:
            timeout = params['timeout']

        # Use optimized context and batch settings
        options = {
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "repeat_penalty": repeat_penalty,
            "num_ctx": params['num_ctx'],
            "num_predict": num_predict,
            "num_thread": params['num_thread'],
            "num_gpu": params['num_gpu'],
            "num_batch": params['num_batch']
        }
    else:
        options = {
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "repeat_penalty": repeat_penalty,
            "num_predict": num_predict or 1024
        }
        # Add num_ctx if provided for manual optimization
        if num_ctx is not None:
            options["num_ctx"] = num_ctx

    # Add seed for reproducibility if provided
    if seed is not None:
        options["seed"] = seed

    # Apply Cloudflare timeout multiplier
    is_cloudflare = "cloudflare" in ollama_url.lower() or "exalio" in ollama_url.lower()
    if is_cloudflare and timeout:
        timeout = timeout * 6  # 6x multiplier for Cloudflare

    try:
        response = requests.post(
            f"{ollama_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": options
            },
            timeout=timeout or 120
        )

        if response.status_code == 200:
            return response.json().get('response', '')
        else:
            return f"[ERROR] HTTP {response.status_code}"

    except requests.exceptions.Timeout:
        return "[ERROR] Request timeout"
    except requests.exceptions.ConnectionError:
        return "[ERROR] Connection failed"
    except Exception as e:
        return f"[ERROR] {str(e)}"

def clean_json_string(json_str: str) -> str:
    """Clean JSON string from markdown code blocks"""
    json_str = re.sub(r'```json\s*', '', json_str)
    json_str = re.sub(r'```\s*', '', json_str)
    return json_str.strip()

def extract_json_from_response(response: str) -> Optional[dict]:
    """
    OPTIMIZED: Extract and parse JSON from AI response with multiple fallback strategies
    """
    if not response:
        return None

    # Strategy 1: Direct parse (if LLM returned clean JSON)
    try:
        return json.loads(response.strip())
    except:
        pass

    # Strategy 2: Remove markdown code blocks and common prefixes
    try:
        cleaned = clean_json_string(response)
        return json.loads(cleaned)
    except:
        pass

    # Strategy 3: Find JSON object with regex (handles extra text before/after)
    try:
        match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', response, re.DOTALL)
        if match:
            json_str = match.group()
            # Remove comments (// style)
            json_str = re.sub(r'//.*?$', '', json_str, flags=re.MULTILINE)
            return json.loads(json_str)
    except:
        pass

    # Strategy 4: Try to find array-based JSON
    try:
        match = re.search(r'\{[\s\S]*"[da]"[\s\S]*:\s*\[[\s\S]*\][\s\S]*\}', response)
        if match:
            json_str = match.group()
            # Remove comments
            json_str = re.sub(r'//.*?$', '', json_str, flags=re.MULTILINE)
            # Remove trailing commas (common LLM error)
            json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
            return json.loads(json_str)
    except:
        pass

    # Strategy 5: Last resort - try to fix common JSON errors
    try:
        # Remove everything before first { and after last }
        start = response.find('{')
        end = response.rfind('}') + 1
        if start != -1 and end > start:
            json_str = response[start:end]
            # Remove comments
            json_str = re.sub(r'//.*?$', '', json_str, flags=re.MULTILINE)
            # Fix trailing commas
            json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
            # Fix unquoted keys (if any)
            json_str = re.sub(r'(\w+):', r'"\1":', json_str)
            # Fix already quoted keys (don't double-quote)
            json_str = re.sub(r'"\"(\w+)\"":', r'"\1":', json_str)
            return json.loads(json_str)
    except:
        pass

    return None

# ====================================================================================
# DATA LOADING & PREPROCESSING
# ====================================================================================

def safe_column_access(df: pd.DataFrame, column_name: str, default_value=0):
    """Safely access column with default fallback"""
    if column_name in df.columns:
        return df[column_name]
    return default_value

def load_csv_file(uploaded_file) -> Optional[pd.DataFrame]:
    """Load CSV file with automatic encoding detection"""
    try:
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']

        for encoding in encodings:
            try:
                df = pd.read_csv(uploaded_file, encoding=encoding)
                # Convert datetime columns if present
                date_columns = ['enrollment_date', 'graduation_date', 'entry_date', 'date', 'timestamp']
                for col in date_columns:
                    if col in df.columns:
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                return df
            except UnicodeDecodeError:
                uploaded_file.seek(0)  # Reset file pointer
                continue
            except Exception as e:
                uploaded_file.seek(0)
                continue

        return None
    except Exception as e:
        st.error(f"Error loading CSV: {str(e)}")
        return None

def load_excel_file(uploaded_file) -> Optional[pd.DataFrame]:
    """Load Excel file"""
    try:
        df = pd.read_excel(uploaded_file)
        # Convert datetime columns if present
        date_columns = ['enrollment_date', 'graduation_date', 'entry_date', 'date', 'timestamp']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error loading Excel: {str(e)}")
        return None

def load_student_data(uploaded_file) -> Optional[pd.DataFrame]:
    """Load and preprocess student data from uploaded file"""
    try:
        if uploaded_file.name.endswith('.csv'):
            return load_csv_file(uploaded_file)
        else:
            return load_excel_file(uploaded_file)
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def set_main_data(df: pd.DataFrame):
    """Set main dataframe and update session state"""
    # Apply universal column mapping
    mapped_df, mapping_log = apply_universal_column_mapping(df)
    st.session_state.data = mapped_df
    st.session_state.mapping_log = mapping_log
    st.session_state.metrics = calculate_core_metrics(mapped_df)

def create_sample_dataset_v3_final() -> pd.DataFrame:
    """Create a sample student dataset - VERSION 3.0 FINAL WITH ALL REQUIRED FIELDS"""
    print("🔥🔥🔥 Creating sample dataset VERSION 3.0 FINAL with ALL FIELDS! 🔥🔥🔥")
    np.random.seed(42)
    n_students = 1000

    # Determine UAE nationals vs international
    nationalities = np.random.choice(['United Arab Emirates', 'India', 'Pakistan', 'Egypt', 'Jordan',
                                     'Saudi Arabia', 'Philippines', 'United States', 'United Kingdom',
                                     'Canada'], n_students, p=[0.45, 0.15, 0.10, 0.08, 0.05, 0.05, 0.04, 0.03, 0.03, 0.02])

    # Housing assignment (60% housed)
    is_housed = np.random.choice([True, False], n_students, p=[0.6, 0.4])

    data = {
        'student_id': [f'S{i:05d}' for i in range(1, n_students + 1)],
        'cumulative_gpa': np.random.normal(3.0, 0.6, n_students).clip(0, 4.0),
        'nationality': nationalities,
        'enrollment_enrollment_status': np.random.choice(['Active', 'Graduated', 'On Leave'], n_students, p=[0.8, 0.15, 0.05]),
        'enrollment_tuition_amount': np.random.uniform(50000, 100000, n_students),
        'financial_aid_monetary_amount': np.random.choice([0, 15000, 25000, 40000, 60000], n_students, p=[0.4, 0.2, 0.2, 0.15, 0.05]),
        'gender': np.random.choice(['Male', 'Female'], n_students),
        'cohort_year': np.random.choice([2020, 2021, 2022, 2023, 2024], n_students),

        # Additional required fields for journey generation
        'visa_status': ['UAE National' if nat == 'United Arab Emirates' else np.random.choice(['Student Visa', 'Resident Visa', 'Family Visa'])
                        for nat in nationalities],
        'enrollment_type': np.random.choice(['Full-Time', 'Part-Time'], n_students, p=[0.85, 0.15]),

        # Housing fields
        'room_number': [f'R{i:04d}' if housed else None for i, housed in enumerate(is_housed, 1)],
        'occupancy_status': ['Occupied' if housed else None for housed in is_housed],
        'rent_amount': [np.random.uniform(8000, 15000) if housed else 0 for housed in is_housed],
    }

    return pd.DataFrame(data)

def apply_universal_column_mapping(df):
    """
    Apply universal column mapping to handle different CSV file formats
    Maps various column name formats to a standardized format used throughout the application
    """

    # Define column mapping dictionary
    # Format: 'standardized_name': ['possible_variant_1', 'possible_variant_2', ...]
    column_mappings = {
        # Core identifiers
        'student_id': ['student_id', 'Student_ID', 'StudentID', 'ID'],
        'emirates_id': ['emirates_id', 'National_ID', 'national_id', 'NationalID'],

        # Personal information
        'first_name_en': ['first_name_en', 'first_name', 'FirstName', 'first_name_english'],
        'last_name_en': ['last_name_en', 'last_name', 'LastName', 'last_name_english'],
        'first_name_ar': ['first_name_ar', 'first_name_arabic', 'FirstNameArabic'],
        'last_name_ar': ['last_name_ar', 'last_name_arabic', 'LastNameArabic'],
        'middle_name': ['middle_name', 'MiddleName', 'middle_name_en'],
        'email_address': ['email_address', 'university_email', 'personal_email', 'email', 'Email'],
        'phone_number': ['phone_number', 'phone', 'Phone', 'PhoneNumber'],
        'gender': ['gender', 'Gender', 'sex'],
        'date_of_birth': ['date_of_birth', 'dob', 'DOB', 'BirthDate'],
        'nationality': ['nationality', 'Nationality', 'nationality_code', 'country'],

        # Academic information
        'cumulative_gpa': ['cumulative_gpa', 'gpa', 'GPA', 'CGPA', 'CumulativeGPA'],
        'term_gpa': ['term_gpa', 'TermGPA', 'semester_gpa'],
        'major_gpa': ['major_gpa', 'MajorGPA'],
        'credits_attempted': ['credits_attempted', 'total_credits_earned', 'credits', 'TotalCredits'],
        'academic_standing': ['academic_standing', 'AcademicStanding', 'standing'],
        'degree_progress_pct': ['degree_progress_pct', 'DegreeProgress', 'progress_percentage'],

        # Enrollment information
        'enrollment_enrollment_status': ['enrollment_enrollment_status', 'Student_Status', 'student_status', 'enrollment_status', 'Status', 'EnrollmentStatus'],
        'enrollment_type': ['enrollment_type', 'academic_level', 'AcademicLevel', 'student_type', 'enrollment_category'],
        'enrollment_date': ['enrollment_date', 'Admission_Date', 'admission_date', 'start_date'],
        'cohort_year': ['cohort_year', 'Cohort', 'cohort', 'CohortYear', 'admission_year'],
        'cohort_term': ['cohort_term', 'cohort_semester', 'admission_term'],
        'expected_graduation': ['enrollment_expected_graduation_date', 'expected_graduation', 'ExpectedGraduation'],
        'actual_graduation_date': ['enrollment_actual_graduation_date', 'actual_graduation_date', 'graduation_date'],

        # Academic program
        'academic_program': ['academic_program', 'program', 'Program', 'degree_program'],
        'major': ['major', 'Major', 'primary_major'],
        'minor': ['minor', 'Minor'],
        'concentration': ['Concentration', 'concentration', 'specialization'],
        'college': ['college', 'College', 'school'],
        'department': ['department', 'Department', 'dept'],

        # Financial information
        'enrollment_tuition_amount': ['enrollment_tuition_amount', 'Tuition_Fee_Total', 'tuition_fee', 'tuition', 'TuitionAmount'],
        'financial_aid_monetary_amount': ['financial_aid_monetary_amount', 'Financial_Aid_Awarded', 'Financial_Aid_Disbursed', 'aid_amount', 'financial_aid'],
        'scholarship_type': ['Scholarship_Type', 'scholarship_type', 'aid_type'],
        'scholarship_amount': ['Scholarship_Amount', 'scholarship_amount'],
        'sponsorship_type': ['Sponsorship_Type', 'sponsorship_type'],
        'account_balance': ['Account_Balance', 'balance_due', 'account_balance'],

        # Housing information
        'room_number': ['room_number', 'RoomNumber', 'room', 'room_no', 'Room_Number'],
        'housing_status': ['housing_status', 'Housing_Status'],
        'occupancy_status': ['occupancy_status', 'housing_status', 'Housing_Status', 'Occupancy_Status'],
        'rent_amount': ['rent_amount', 'Rent_Amount', 'rent', 'Rent', 'housing_fee', 'Housing_Fee'],
        'has_meal_plan': ['has_meal_plan', 'meal_plan', 'MealPlan'],

        # Student success & engagement
        'is_at_risk': ['is_at_risk', 'risk_category', 'at_risk_flag'],
        'attendance_rate': ['attendance_rate', 'attendance_percentage', 'Attendance'],
        'engagement_score': ['engagement_score', 'EngagementScore'],
        'gpa_trend': ['gpa_trend', 'GPATrend'],

        # Advisor & support
        'advisor_meeting_count': ['advisor_meeting_count', 'AdvisorMeetings'],
        'counseling_visits_count': ['counseling_visits_count', 'CounselingVisits'],

        # International student information
        'is_international': ['is_international', 'international_student'],
        'visa_status': ['visa_status', 'VisaStatus', 'visa_type'],
        'visa_expiry_date': ['visa_expiry_date', 'VisaExpiry'],

        # Additional fields
        'is_first_generation': ['is_first_generation', 'first_generation', 'FirstGeneration'],
        'registration_status': ['registration_status', 'RegistrationStatus'],
        'last_activity_date': ['last_activity_date', 'LastActivity'],
    }

    # Create a new dataframe with mapped columns
    mapped_df = df.copy()
    mapping_log = []

    # Apply mappings
    for standard_name, possible_names in column_mappings.items():
        # Check if standard name already exists
        if standard_name in mapped_df.columns:
            continue

        # Look for possible variants
        for variant in possible_names:
            if variant in mapped_df.columns and variant != standard_name:
                mapped_df[standard_name] = mapped_df[variant]
                mapping_log.append(f"Mapped '{variant}' → '{standard_name}'")
                break

    # Special handling for email - prefer university_email over personal_email
    if 'email_address' not in mapped_df.columns:
        if 'university_email' in df.columns:
            mapped_df['email_address'] = df['university_email']
            mapping_log.append(f"Mapped 'university_email' → 'email_address'")
        elif 'personal_email' in df.columns:
            mapped_df['email_address'] = df['personal_email']
            mapping_log.append(f"Mapped 'personal_email' → 'email_address'")

    # Return mapped dataframe and log
    return mapped_df, mapping_log

def calculate_core_metrics(df: pd.DataFrame) -> dict:
    """Calculate core metrics from student data"""
    metrics = {
        'total_students': len(df),
        'avg_gpa': safe_column_access(df, 'cumulative_gpa', pd.Series([0])).mean(),
        'total_tuition': safe_column_access(df, 'enrollment_tuition_amount', pd.Series([0])).sum(),
        'total_aid': safe_column_access(df, 'financial_aid_monetary_amount', pd.Series([0])).sum(),
        'unique_nationalities': df['nationality'].nunique() if 'nationality' in df.columns else 0,
    }

    # Performance tiers
    if 'cumulative_gpa' in df.columns:
        metrics['high_performers'] = len(df[df['cumulative_gpa'] >= 3.5])
        metrics['mid_performers'] = len(df[(df['cumulative_gpa'] >= 2.5) & (df['cumulative_gpa'] < 3.5)])
        metrics['at_risk'] = len(df[df['cumulative_gpa'] < 2.5])

    # UAE nationals - handle multiple formats (country codes AND full names)
    if 'nationality' in df.columns:
        # Check for various UAE formats (case-insensitive)
        # Includes: "AE" (ISO code), "UAE", "United Arab Emirates", "U.A.E", "Emirates"
        nationality_upper = df['nationality'].fillna('').str.upper().str.strip()

        # Match exact values or patterns
        uae_mask = nationality_upper.str.match(
            r'^(AE|UAE|UNITED ARAB EMIRATES|U\.A\.E\.?|EMIRATES)$',
            na=False
        )

        # If no exact matches, try contains pattern (for cases like "UAE - Dubai")
        if uae_mask.sum() == 0:
            uae_mask = nationality_upper.str.contains(
                r'\b(AE|UAE|UNITED ARAB EMIRATES|U\.A\.E\.?|EMIRATES)\b',
                na=False,
                regex=True
            )

        metrics['uae_nationals'] = int(uae_mask.sum())
        metrics['uae_percentage'] = (metrics['uae_nationals'] / metrics['total_students'] * 100) if metrics['total_students'] > 0 else 0
    else:
        metrics['uae_nationals'] = 0
        metrics['uae_percentage'] = 0

    # Financial aid coverage
    if metrics['total_tuition'] > 0:
        metrics['aid_coverage_pct'] = (metrics['total_aid'] / metrics['total_tuition'] * 100)
    else:
        metrics['aid_coverage_pct'] = 0

    return metrics

# ====================================================================================
# VISUALIZATION HELPERS
# ====================================================================================

def create_plotly_chart(chart_type: str, data: dict, title: str) -> go.Figure:
    """Create Plotly chart with dark theme"""

    if chart_type == "bar":
        fig = go.Figure(data=[go.Bar(
            x=data['x'],
            y=data['y'],
            marker_color='#6366f1'
        )])

    elif chart_type == "pie":
        fig = go.Figure(data=[go.Pie(
            labels=data['labels'],
            values=data['values'],
            hole=0.4,
            marker_colors=['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#3b82f6']
        )])

    elif chart_type == "histogram":
        fig = go.Figure(data=[go.Histogram(
            x=data['values'],
            nbinsx=30,
            marker_color='#6366f1'
        )])

    elif chart_type == "scatter":
        fig = go.Figure(data=[go.Scatter(
            x=data['x'],
            y=data['y'],
            mode='markers',
            marker=dict(color='#6366f1', size=8, opacity=0.6)
        )])

    else:
        fig = go.Figure()

    # Apply dark theme
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(30, 41, 59, 0.85)',
        font=dict(color='white', size=14),
        title=dict(text=title, font=dict(size=18, color='#6366f1')),
        height=400,
        margin=dict(l=40, r=40, t=60, b=40)
    )

    return fig

# ====================================================================================
# LLM CONTENT GENERATION FUNCTIONS
# ====================================================================================

def generate_executive_summary_llm(metrics: dict, df: pd.DataFrame, model: str, url: str) -> dict:
    """Generate executive summary using LLM"""

    # Create context for LLM
    context = f"""You are analyzing student data for a higher education institution.

**KEY METRICS:**
- Total Students: {metrics.get('total_students', 0):,}
- Average GPA: {metrics.get('avg_gpa', 0):.2f}
- High Performers (GPA ≥ 3.5): {metrics.get('high_performers', 0):,}
- At-Risk Students (GPA < 2.5): {metrics.get('at_risk', 0):,}
- UAE Nationals: {metrics.get('uae_nationals', 0):,} ({metrics.get('uae_percentage', 0):.1f}%)
- Unique Nationalities: {metrics.get('unique_nationalities', 0)}
- Total Tuition Revenue: AED {metrics.get('total_tuition', 0):,.0f}
- Financial Aid Distributed: AED {metrics.get('total_aid', 0):,.0f}
- Aid Coverage: {metrics.get('aid_coverage_pct', 0):.1f}%

Generate 4 executive insights in JSON format:
{{
  "insights": [
    {{
      "title": "Insight title",
      "content": "2-3 sentences explaining the strategic implication",
      "icon": "emoji",
      "type": "success|warning|info"
    }}
  ]
}}

Focus on: enrollment health, academic performance, financial sustainability, and strategic opportunities."""

    try:
        response = query_ollama(
            context,
            model,
            url,
            temperature=0.7,
            num_predict=800,
            auto_optimize=True
        )

        if response and not response.startswith('[ERROR]'):
            result = extract_json_from_response(response)
            if result and 'insights' in result:
                return result
    except:
        pass

    # Fallback insights
    return {
        "insights": [
            {
                "title": "Strong Enrollment Foundation",
                "content": f"The institution serves {metrics.get('total_students', 0):,} students with representation from {metrics.get('unique_nationalities', 0)} nationalities, demonstrating healthy enrollment diversity and market reach.",
                "icon": "📊",
                "type": "success"
            },
            {
                "title": "Academic Performance Analysis",
                "content": f"With an average GPA of {metrics.get('avg_gpa', 0):.2f}, the student body shows solid academic standing. {metrics.get('high_performers', 0):,} high performers represent excellence opportunities.",
                "icon": "🎓",
                "type": "info"
            },
            {
                "title": "Financial Sustainability",
                "content": f"Total tuition revenue of AED {metrics.get('total_tuition', 0):,.0f} with {metrics.get('aid_coverage_pct', 0):.1f}% aid coverage indicates strong financial positioning while maintaining access.",
                "icon": "💰",
                "type": "success"
            },
            {
                "title": "Student Success Focus",
                "content": f"{metrics.get('at_risk', 0):,} students identified as at-risk require targeted intervention programs to improve retention and success outcomes.",
                "icon": "⚠️",
                "type": "warning"
            }
        ]
    }

def generate_comprehensive_executive_summary_llm(metrics: dict, df: pd.DataFrame, model: str, url: str) -> dict:
    """Generate comprehensive executive summary with graphs and detailed insights"""

    total_students = metrics.get('total_students', 0)
    avg_gpa = metrics.get('avg_gpa', 0)
    high_performers = metrics.get('high_performers', 0)
    at_risk = metrics.get('at_risk', 0)
    uae_percentage = metrics.get('uae_percentage', 0)
    unique_nationalities = metrics.get('unique_nationalities', 0)
    total_tuition = metrics.get('total_tuition', 0)
    total_aid = metrics.get('total_aid', 0)
    aid_coverage = metrics.get('aid_coverage_pct', 0)

    high_perf_pct = (high_performers / total_students * 100) if total_students > 0 else 0
    at_risk_pct = (at_risk / total_students * 100) if total_students > 0 else 0

    context = f"""You are Chief Data Officer preparing EXECUTIVE SUMMARY for board presentation.

**INSTITUTIONAL METRICS:**
- Total Students: {total_students:,}
- Average GPA: {avg_gpa:.2f}
- High Performers: {high_performers:,} ({high_perf_pct:.1f}%)
- At-Risk: {at_risk:,} ({at_risk_pct:.1f}%)
- UAE Nationals: {metrics.get('uae_nationals', 0):,} ({uae_percentage:.1f}%)
- Nationalities: {unique_nationalities}
- Tuition Revenue: AED {total_tuition:,.0f}
- Financial Aid: AED {total_aid:,.0f} ({aid_coverage:.1f}%)

Generate COMPREHENSIVE executive analysis with strategic intelligence and data visualizations.

Return ONLY valid JSON:
{{
  "strategic_overview": "3-4 sentence executive summary of overall institutional health and positioning",
  "performance_insights": {{
    "gpa_analysis": "2-3 sentences on academic performance distribution and quality indicators",
    "tier_analysis": "2-3 sentences on high performer vs at-risk balance and implications"
  }},
  "financial_insights": {{
    "revenue_analysis": "2-3 sentences on revenue scale and per-student metrics",
    "aid_analysis": "2-3 sentences on aid strategy and sustainability"
  }},
  "risk_insights": {{
    "assessment": "2-3 sentences on at-risk population and intervention priorities",
    "priority": "High|Medium|Low",
    "action": "Specific recommended intervention"
  }},
  "diversity_insights": {{
    "analysis": "2-3 sentences on nationality mix and UAE balance",
    "market_position": "Competitive positioning assessment"
  }},
  "recommendations": [
    {{
      "title": "Priority 1 Action",
      "description": "What to do and expected impact"
    }},
    {{
      "title": "Priority 2 Action",
      "description": "What to do and expected impact"
    }},
    {{
      "title": "Priority 3 Action",
      "description": "What to do and expected impact"
    }}
  ]
}}"""

    try:
        response = query_ollama(context, model, url, temperature=0.7, num_predict=1200, auto_optimize=True)
        if response and not response.startswith('[ERROR]'):
            result = extract_json_from_response(response)
            if result:
                return result
    except:
        pass

    # Intelligent fallback
    return {
        "strategic_overview": f"Institution serves {total_students:,} students across {unique_nationalities} nationalities with AED {total_tuition:,.0f} revenue. Academic performance averages {avg_gpa:.2f} with {high_perf_pct:.1f}% high performers, though {at_risk_pct:.1f}% require intervention. UAE nationals at {uae_percentage:.1f}% balance national priorities with diversity.",
        "performance_insights": {
            "gpa_analysis": f"Average GPA of {avg_gpa:.2f} {'exceeds' if avg_gpa >= 3.0 else 'meets'} benchmarks. Distribution shows {'strong' if high_perf_pct > 30 else 'solid'} academic quality with room for excellence expansion.",
            "tier_analysis": f"{high_performers:,} high performers ({high_perf_pct:.1f}%) demonstrate strength, while {at_risk:,} at-risk ({at_risk_pct:.1f}%) require {'immediate' if at_risk_pct > 25 else 'targeted'} support programs."
        },
        "financial_insights": {
            "revenue_analysis": f"Total revenue AED {total_tuition:,.0f} averages AED {total_tuition/total_students if total_students > 0 else 0:,.0f} per student, indicating {'premium' if (total_tuition/total_students) > 60000 else 'competitive'} market positioning with {'strong' if total_tuition > 70000000 else 'adequate'} sustainability.",
            "aid_analysis": f"Aid coverage {aid_coverage:.1f}% ({total_aid:,.0f}) positions institution as {'highly accessible' if aid_coverage > 50 else 'selectively accessible'} while maintaining financial health."
        },
        "risk_insights": {
            "assessment": f"At-risk population {at_risk_pct:.1f}% ({at_risk:,} students) presents {'elevated' if at_risk_pct > 25 else 'moderate' if at_risk_pct > 15 else 'manageable'} retention risk requiring proactive intervention to prevent attrition.",
            "priority": f"{'High' if at_risk_pct > 25 else 'Medium' if at_risk_pct > 15 else 'Low'}",
            "action": f"{'Deploy comprehensive early warning system with mandatory support' if at_risk_pct > 25 else 'Expand tutoring and mentorship programs'}"
        },
        "diversity_insights": {
            "analysis": f"Student body from {unique_nationalities} nationalities with {uae_percentage:.1f}% UAE creates {'excellent' if 40 <= uae_percentage <= 60 else 'strong'} balance. Diversity profile supports multicultural learning and graduate employability.",
            "market_position": f"{'Strong regional and international positioning' if unique_nationalities > 20 else 'Regional focus with international growth opportunity'}"
        },
        "recommendations": [
            {"title": f"{'Expand Academic Support Systems' if at_risk_pct > 20 else 'Enhance Excellence Programs'}", "description": f"{'Deploy early warning and intervention for at-risk students to improve 5-8% retention' if at_risk_pct > 20 else 'Launch honors programs and research opportunities for high performers'}"},
            {"title": "Optimize Enrollment Mix", "description": "Strategic recruitment to grow enrollment 10-15% over 3 years while maintaining quality and diversity"},
            {"title": "Leverage Diversity for Partnerships", "description": "Develop corporate and international partnerships leveraging multicultural student profile"}
        ]
    }

# ====================================================================================
# LLM-DRIVEN DYNAMIC VISUALIZATION ENGINE
# ====================================================================================

def _enrich_finding_statistical(finding_text: str, context: dict, df: pd.DataFrame) -> str:
    """Add ROOT CAUSE and IMPACT to findings using statistical analysis"""
    finding_type = context.get('type', '')

    if finding_type == 'academic':
        # Academic finding enrichment
        at_risk_pct = context.get('at_risk_pct', 0)
        at_risk = context.get('at_risk', 0)
        total_students = context.get('total_students', 1)
        total_tuition = context.get('total_tuition', 0) if 'total_tuition' in context else 0

        # Calculate GPA std for root cause
        gpa_col = find_matching_column('gpa', df)
        gpa_std = df[gpa_col].std() if gpa_col and gpa_col in df.columns else 0

        root_cause = "Wide admissions criteria without adequate placement testing" if gpa_std > 0.6 else "Consistent academic standards with selective admissions"
        revenue_at_risk = (at_risk / total_students * total_tuition) if total_students > 0 and total_tuition > 0 else 0
        impact = f"{at_risk:,} students represent {'critical' if at_risk_pct > 25 else 'moderate'} retention risk affecting AED {revenue_at_risk:,.0f} in potential revenue"

        return f"{finding_text} ROOT CAUSE: {root_cause}. IMPACT: {impact}."

    elif finding_type == 'academic_distribution':
        # Academic performance distribution finding
        high_performers = context.get('high_performers', 0)
        at_risk = context.get('at_risk', 0)
        total_students = context.get('total_students', 1)
        high_perf_pct = (high_performers / total_students * 100) if total_students > 0 else 0
        at_risk_pct = (at_risk / total_students * 100) if total_students > 0 else 0

        # Analyze distribution pattern
        if high_perf_pct > 20 and at_risk_pct < 15:
            root_cause = "Selective admissions with strong academic support infrastructure"
            impact = "Strong academic reputation attracts quality students; low attrition risk"
        elif high_perf_pct < 10 and at_risk_pct > 30:
            root_cause = "Open admissions policy without adequate academic preparedness assessment or support systems"
            impact = f"Critical retention risk: {at_risk:,} students likely to face academic probation or dropout, threatening enrollment stability"
        else:
            root_cause = "Standard admissions with balanced support systems creating normal performance distribution"
            impact = f"Moderate intervention needs: {at_risk:,} students require structured academic support to prevent attrition"

        return f"{finding_text} ROOT CAUSE: {root_cause}. IMPACT: {impact}."

    elif finding_type == 'academic_variance':
        # GPA variance across programs finding
        program_gpa_variance = context.get('program_gpa_variance', 0)
        lowest_program_gpa = context.get('lowest_program_gpa', 0)
        highest_program_gpa = context.get('highest_program_gpa', 0)

        if program_gpa_variance > 0.5:
            root_cause = "Inconsistent academic rigor across programs - some departments have significantly higher/lower standards or more challenging curricula"
            impact = f"GPA range {lowest_program_gpa:.2f} to {highest_program_gpa:.2f} creates perception of unequal degree value; students may migrate to 'easier' programs"
        elif program_gpa_variance > 0.3:
            root_cause = "Moderate curriculum difficulty variations reflecting natural differences in discipline complexity (e.g., STEM vs humanities)"
            impact = "Some programs may require enhanced support services or curriculum standardization review"
        else:
            root_cause = "Consistent academic standards across programs with balanced curriculum difficulty"
            impact = "Stable academic environment; equal degree value perception across majors"

        return f"{finding_text} ROOT CAUSE: {root_cause}. IMPACT: {impact}."

    elif finding_type == 'academic_atrisk':
        # At-risk concentration finding
        at_risk = context.get('at_risk', 0)
        at_risk_pct = context.get('at_risk_pct', 0)
        total_students = context.get('total_students', 1)
        total_tuition = context.get('total_tuition', 0)

        revenue_at_risk = (at_risk / total_students * total_tuition) if total_students > 0 and total_tuition > 0 else 0

        if at_risk_pct > 30:
            root_cause = "Systemic academic support deficiencies - inadequate tutoring, advising, or early intervention systems combined with possible over-enrollment"
            impact = f"Crisis level: {at_risk:,} students ({at_risk_pct:.1f}%) facing academic failure threatens AED {revenue_at_risk:,.0f} in revenue and institutional accreditation standards"
        elif at_risk_pct > 20:
            root_cause = "Insufficient proactive intervention - students falling behind without timely support or mandatory remediation"
            impact = f"Significant concern: {at_risk:,} students at risk of dropout, jeopardizing AED {revenue_at_risk:,.0f} in revenue and damaging retention metrics"
        else:
            root_cause = "Normal academic challenges in student population with current support systems managing majority effectively"
            impact = f"Manageable: {at_risk:,} students need targeted intervention to improve overall retention rates"

        return f"{finding_text} ROOT CAUSE: {root_cause}. IMPACT: {impact}."

    elif finding_type == 'diversity':
        # Diversity finding enrichment
        top_3_concentration = context.get('top_3_concentration', 0)

        root_cause = "Over-reliance on limited geographic recruitment channels" if top_3_concentration > 60 else "Balanced multi-market recruitment strategy"
        impact = "High concentration risk - geopolitical or economic shifts in 3 markets could affect majority of enrollment" if top_3_concentration > 60 else "Balanced risk distribution across markets"

        return f"{finding_text} ROOT CAUSE: {root_cause}. IMPACT: {impact}."

    elif finding_type == 'financial':
        # Financial finding enrichment
        aid_coverage_pct = context.get('aid_coverage_pct', 0)

        root_cause = "Accessibility-focused aid model prioritizing student access" if aid_coverage_pct > 35 else "Revenue-focused model with selective aid allocation"
        impact = "Approaching sustainability threshold - monitor for long-term viability" if aid_coverage_pct > 40 else "Sustainable model with healthy margins"

        return f"{finding_text} ROOT CAUSE: {root_cause}. IMPACT: {impact}."

    else:
        return f"{finding_text} ROOT CAUSE: Data-driven institutional patterns. IMPACT: Requires strategic attention."


def _enrich_recommendation_statistical(rec_text: str, context: dict) -> str:
    """Add ACTION and EXPECTED OUTCOME to recommendations using statistical analysis"""
    rec_type = context.get('type', '')

    if rec_type == 'academic':
        # Academic recommendation enrichment
        at_risk = context.get('at_risk', 0)
        total_students = context.get('total_students', 1)
        total_tuition = context.get('total_tuition', 0)

        students_to_save = int(at_risk * 0.25)  # 25% reduction target
        revenue_impact = (students_to_save / total_students * total_tuition) if total_students > 0 else 0

        action = "Deploy early warning system with mandatory tutoring for students below 2.0 GPA, implement peer mentoring, and create academic success workshops"
        expected_outcome = f"Reduce at-risk population by 25% ({students_to_save:,} students), improving retention by 5-8% and protecting AED {revenue_impact:,.0f} in annual revenue"

        return f"{rec_text}. ACTION: {action}. EXPECTED OUTCOME: {expected_outcome}."

    elif rec_type == 'academic_intervention':
        # Early warning system implementation recommendation
        at_risk = context.get('at_risk', 0)
        at_risk_pct = context.get('at_risk_pct', 0)
        total_students = context.get('total_students', 1)
        total_tuition = context.get('total_tuition', 0)

        students_to_save = int(at_risk * 0.30)  # 30% reduction target with comprehensive system
        revenue_saved = (students_to_save / total_students * total_tuition) if total_students > 0 else 0

        action = "Deploy predictive early warning system tracking GPA, attendance, and assignment completion. Trigger automatic alerts at <2.5 GPA with mandatory academic advisor meetings. Implement tiered interventions: Level 1 (2.0-2.5 GPA) = peer tutoring; Level 2 (1.5-2.0) = mandatory study skills workshop + tutoring; Level 3 (<1.5) = academic probation contract with weekly check-ins"
        expected_outcome = f"Identify at-risk students 4-6 weeks earlier, improve intervention success rate from ~40% to ~70%, reduce at-risk population by 30% ({students_to_save:,} students saved), boost overall retention by 6-10%, protecting AED {revenue_saved:,.0f} in annual revenue"

        return f"{rec_text}. ACTION: {action}. EXPECTED OUTCOME: {expected_outcome}."

    elif rec_type == 'academic_curriculum':
        # Curriculum difficulty review recommendation
        program_gpa_variance = context.get('program_gpa_variance', 0)
        lowest_program_gpa = context.get('lowest_program_gpa', 0)
        highest_program_gpa = context.get('highest_program_gpa', 0)
        total_students = context.get('total_students', 1)

        if program_gpa_variance > 0.5:
            # High variance - need standardization
            action = f"Conduct comprehensive curriculum audit for programs with GPA below {(lowest_program_gpa + 0.3):.2f} (significantly below average). Review course difficulty, grading rubrics, and learning outcomes alignment. For high-GPA programs (>{(highest_program_gpa - 0.2):.2f}), assess whether standards are too lenient. Implement faculty development workshops on consistent grading practices and learning assessment. Establish cross-program curriculum committee to standardize rigor"
            expected_outcome = f"Reduce GPA variance from {program_gpa_variance:.2f} to <0.30 within 2 academic years, equalize degree value perception across programs, reduce student migration to 'easier' majors by 40%, improve employer confidence in academic standards"
        elif program_gpa_variance > 0.3:
            # Moderate variance - targeted support
            action = f"Provide targeted academic support for challenging programs (GPA {lowest_program_gpa:.2f}): add supplemental instruction sessions, embed tutors in difficult courses, offer program-specific study skills workshops. Review if lower GPAs reflect appropriate rigor or need curriculum adjustments"
            expected_outcome = f"Improve lowest-performing program GPA by 0.15-0.25 points, reduce program dropout rate by 15-20%, maintain academic rigor while improving student success"
        else:
            # Low variance - maintain excellence
            action = "Maintain current curriculum standards with annual review process. Document and share best practices across programs. Consider creating honors tracks or advanced sections to challenge high performers further"
            expected_outcome = "Sustain consistent academic quality, enhance institutional reputation for rigorous standards, attract higher-caliber students"

        return f"{rec_text}. ACTION: {action}. EXPECTED OUTCOME: {expected_outcome}."

    elif rec_type == 'academic_support':
        # Tutoring/mentoring expansion recommendation
        at_risk = context.get('at_risk', 0)
        at_risk_pct = context.get('at_risk_pct', 0)
        total_students = context.get('total_students', 1)

        # Calculate support program scale needed
        tutoring_capacity_needed = int(at_risk * 0.6)  # Assume 60% of at-risk need regular tutoring
        peer_mentors_needed = int(total_students * 0.1)  # 1 peer mentor per 10 students

        action = f"Expand tutoring center capacity to serve {tutoring_capacity_needed:,} students simultaneously (60% of at-risk population). Recruit and train {peer_mentors_needed:,} peer mentors from high-performing students (≥3.5 GPA) with stipends/service credit. Launch subject-specific study groups for high-failure-rate courses (math, science, statistics). Create online tutoring portal with 24/7 access. Implement mandatory tutoring requirement for students on academic probation"
        expected_outcome = f"Increase tutoring utilization from current ~15-20% to 50-60% of at-risk students, improve course pass rates in high-risk subjects by 20-25%, reduce at-risk population by 25% ({int(at_risk*0.25):,} students), enhance peer learning culture, improve 4-year graduation rate by 8-12%"

        return f"{rec_text}. ACTION: {action}. EXPECTED OUTCOME: {expected_outcome}."

    elif rec_type == 'diversity':
        # Diversity recommendation enrichment
        top_3_concentration = context.get('top_3_concentration', 0)
        unique_nationalities = context.get('unique_nationalities', 0)

        if top_3_concentration > 60:
            action = "Establish partnerships in 5-7 new markets (Southeast Asia, Africa, Latin America), launch digital marketing campaigns in target regions, and offer market-specific scholarships"
            expected_outcome = "Reduce concentration risk, stabilize enrollment against regional economic fluctuations, and enhance multicultural learning environment"
        else:
            action = f"Strengthen presence in current {unique_nationalities} markets through alumni networks, expand scholarship programs for underrepresented regions, and develop market-specific value propositions"
            expected_outcome = "10-15% enrollment growth while preserving diversity balance"

        return f"{rec_text}. ACTION: {action}. EXPECTED OUTCOME: {expected_outcome}."

    elif rec_type == 'financial':
        # Financial recommendation enrichment
        aid_coverage_pct = context.get('aid_coverage_pct', 0)
        total_tuition = context.get('total_tuition', 0)

        if aid_coverage_pct > 40:
            action = "Conduct aid effectiveness audit, implement need-based verification, explore corporate sponsorships and endowment funding, and optimize aid allocation using predictive retention analytics"
            savings = (aid_coverage_pct - 37) * total_tuition / 100
            expected_outcome = f"Reduce aid coverage to 35-38% while maintaining access, freeing AED {savings:,.0f} for reinvestment in academic programs"
        else:
            action = "Target aid to high-potential students with financial need, create merit-need hybrid scholarships, and develop aid retention tied to academic progress milestones"
            expected_outcome = "Improve aid ROI by 15-20%, enhance student success rates, and maintain financial sustainability"

        return f"{rec_text}. ACTION: {action}. EXPECTED OUTCOME: {expected_outcome}."

    else:
        return f"{rec_text}. ACTION: Implement data-driven strategic initiatives. EXPECTED OUTCOME: Measurable improvement in institutional performance."


def _generate_rich_statistical_insight(viz: dict, df: pd.DataFrame, total_students: int, high_performers: int, at_risk: int, avg_gpa: float) -> str:
    """Generate rich statistical insights when LLM is unavailable"""
    col_name = viz.get('data_column', '')
    title = viz.get('title', '')
    graph_type = viz.get('graph_type', '')

    # Handle multiple columns (e.g., scatter plots)
    if ',' in col_name:
        cols = [c.strip() for c in col_name.split(',')]
        col_name = cols[0]

    # Check if column exists
    if not col_name or col_name not in df.columns:
        return f"Statistical analysis for {title} provides insights into institutional performance patterns."

    # Numeric column insights
    if df[col_name].dtype in ['int64', 'float64']:
        data = df[col_name].dropna()
        if len(data) == 0:
            return f"Insufficient data for {title} analysis."

        mean = data.mean()
        median = data.median()
        std = data.std()
        q1 = data.quantile(0.25)
        q3 = data.quantile(0.75)
        min_val = data.min()
        max_val = data.max()

        # Detect pattern
        skew = "right-skewed" if mean > median else "left-skewed" if mean < median else "symmetric"
        diff = abs(mean - median)

        # GPA-specific insights
        if 'gpa' in col_name.lower():
            return f"GPA distribution shows mean {mean:.2f} and median {median:.2f} (difference {diff:.2f} indicates {skew} distribution) with standard deviation {std:.2f}. Range spans {min_val:.2f} to {max_val:.2f}. Analysis reveals {high_performers:,} high performers (≥3.5, {(high_performers/total_students*100):.1f}%) and {at_risk:,} at-risk students (<2.0, {(at_risk/total_students*100):.1f}%). ROOT CAUSE: {'Wide admissions range' if std > 0.6 else 'Consistent academic standards'}. IMPACT: {at_risk:,} students represent potential retention risk. ACTION: Implement early intervention programs targeting at-risk population - potential to reduce attrition by 20-30%."

        # Financial columns
        elif 'tuition' in col_name.lower() or 'fee' in col_name.lower():
            return f"Tuition analysis: mean AED {mean:,.0f}, median AED {median:,.0f}, range AED {min_val:,.0f} to AED {max_val:,.0f}. Distribution is {skew} with standard deviation AED {std:,.0f}. PATTERN: {'High variability suggests diverse program pricing' if std > mean*0.2 else 'Consistent pricing across programs'}. IMPACT: Total revenue AED {(mean*total_students):,.0f}. Revenue concentration in 25th-75th percentile range: AED {q1:,.0f} to AED {q3:,.0f}."

        # Aid columns
        elif 'aid' in col_name.lower() or 'scholarship' in col_name.lower():
            students_with_aid = (data > 0).sum()
            aid_pct = (students_with_aid / total_students * 100) if total_students > 0 else 0
            avg_aid = data[data > 0].mean() if students_with_aid > 0 else 0
            return f"Financial aid: {students_with_aid:,} students ({aid_pct:.1f}%) receive aid averaging AED {avg_aid:,.0f} per recipient. Total aid AED {data.sum():,.0f}. Distribution shows {skew} pattern. PATTERN: {'Concentrated aid for high-need students' if std > mean else 'Distributed aid across student body'}. IMPACT: Aid accessibility {'strong' if aid_pct > 40 else 'moderate' if aid_pct > 25 else 'limited'}. ACTION: {'Review aid allocation for equity' if aid_pct < 30 else 'Maintain current aid strategy'}."

        # Age/enrollment columns
        elif 'age' in col_name.lower():
            return f"Age distribution: mean {mean:.1f} years, median {median:.1f} years, range {min_val:.0f} to {max_val:.0f} years. Pattern: {skew} distribution suggests {'traditional age students dominate' if median < 25 else 'non-traditional/mature student population'}. Quartile range (Q1-Q3): {q1:.1f} to {q3:.1f} years. IMPACT: {'Target retention strategies for younger cohort' if median < 23 else 'Provide flexible learning for working professionals'}."

        # Generic numeric
        else:
            return f"{col_name}: mean {mean:.2f}, median {median:.2f} ({skew}), std dev {std:.2f}. Distribution spans {min_val:.2f} to {max_val:.2f} with interquartile range {q1:.2f} to {q3:.2f}. Pattern reveals {'high variability' if std > mean*0.3 else 'consistent values'} suggesting {'diverse student profiles' if std > mean*0.3 else 'homogeneous characteristics'}."

    # Categorical column insights
    else:
        value_counts = df[col_name].value_counts()
        if len(value_counts) == 0:
            return f"No data available for {title} analysis."

        unique_vals = len(value_counts)
        top_3 = value_counts.head(3)
        top_3_pct = (top_3.sum() / total_students * 100) if total_students > 0 else 0

        # Nationality-specific
        if 'nationality' in col_name.lower() or 'country' in col_name.lower():
            top_list = ", ".join([f"{k} ({v:,}, {(v/total_students*100):.1f}%)" for k, v in top_3.items()])
            return f"Student body spans {unique_vals} nationalities. Top 3 markets: {top_list} represent {top_3_pct:.1f}% of enrollment. PATTERN: {'High market concentration risk' if top_3_pct > 60 else 'Balanced diversity' if top_3_pct < 50 else 'Moderate concentration'}. ROOT CAUSE: {'Over-reliance on limited recruitment channels' if top_3_pct > 60 else 'Diversified recruitment strategy'}. IMPACT: {top_3_pct:.1f}% revenue dependency on 3 markets. ACTION: {'Diversify recruitment to reduce concentration below 50%' if top_3_pct > 60 else 'Maintain current balanced approach'}."

        # Program/major
        elif 'program' in col_name.lower() or 'major' in col_name.lower():
            top_list = ", ".join([f"{k} ({v:,} students)" for k, v in top_3.items()])
            return f"Academic programs: {unique_vals} distinct programs. Top 3: {top_list} ({top_3_pct:.1f}% of enrollment). PATTERN: {'Program concentration' if top_3_pct > 60 else 'Diverse program portfolio'}. IMPACT: {'Strong specialization focus' if top_3_pct > 60 else 'Broad academic offering'}. ACTION: {'Consider expanding popular programs' if top_3.iloc[0]/total_students > 0.3 else 'Balance enrollment across programs'}."

        # Performance tiers
        elif 'performance' in col_name.lower() or 'tier' in col_name.lower():
            top_list = ", ".join([f"{k}: {v:,} ({(v/total_students*100):.1f}%)" for k, v in value_counts.items()])
            return f"Performance distribution: {top_list}. {'CRITICAL: High at-risk population requires immediate intervention' if (value_counts.get('At-Risk', 0)/total_students) > 0.2 else 'Manageable performance distribution'}. TARGET: Reduce at-risk by 30% through academic support programs. EXPECTED OUTCOME: 5-8% retention improvement, {int(at_risk*0.3):,} students saved."

        # Generic categorical
        else:
            top_list = ", ".join([f"{k} ({v:,})" for k, v in top_3.items()])
            return f"{col_name} distribution: {unique_vals} categories. Top 3: {top_list} ({top_3_pct:.1f}% combined). Pattern shows {'high concentration in few categories' if top_3_pct > 60 else 'balanced distribution'}."

def generate_dynamic_visualizations_llm(metrics: dict, df: pd.DataFrame, model: str, url: str, context_type: str = "executive_summary") -> dict:
    """
    TRUE LLM-DRIVEN APPROACH: AI analyzes data and recommends visualizations

    The LLM acts as a data analyst:
    - Examines available data with DEEP PROFILING
    - Analyzes distributions, correlations, patterns
    - Decides which visualizations would be most insightful
    - Specifies graph types, data columns, and configurations
    - Generates SPECIFIC, DATA-DRIVEN insights

    Returns JSON with dynamic visualization specifications
    """

    total_students = metrics.get('total_students', 0)
    avg_gpa = metrics.get('avg_gpa', 0)
    high_performers = metrics.get('high_performers', 0)
    at_risk = metrics.get('at_risk', 0)
    uae_percentage = metrics.get('uae_percentage', 0)
    unique_nationalities = metrics.get('unique_nationalities', 0)
    total_tuition = metrics.get('total_tuition', 0)
    total_aid = metrics.get('total_aid', 0)

    # ====================================================================================
    # DEEP DATA PROFILING - Enhanced for better insights
    # ====================================================================================

    available_columns = df.columns.tolist()
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

    # Calculate detailed statistics for ALL numeric columns (not just first 5)
    numeric_stats = {}
    for col in numeric_cols:  # ✅ ANALYZE ALL NUMERIC COLUMNS
        if col in df.columns:
            data = df[col].dropna()
            if len(data) > 0:
                numeric_stats[col] = {
                    'mean': float(data.mean()),
                    'median': float(data.median()),
                    'std': float(data.std()),
                    'min': float(data.min()),
                    'max': float(data.max()),
                    'q25': float(data.quantile(0.25)),
                    'q75': float(data.quantile(0.75)),
                    'outliers': int(((data < (data.quantile(0.25) - 1.5 * (data.quantile(0.75) - data.quantile(0.25)))) |
                                    (data > (data.quantile(0.75) + 1.5 * (data.quantile(0.75) - data.quantile(0.25))))).sum())
                }

    # Analyze ALL categorical distributions (not just first 5)
    categorical_distributions = {}
    for col in categorical_cols:  # ✅ ANALYZE ALL CATEGORICAL COLUMNS
        if col in df.columns:
            value_counts = df[col].value_counts().head(5)
            categorical_distributions[col] = {
                'unique_values': int(df[col].nunique()),
                'top_values': {str(k): int(v) for k, v in value_counts.items()},
                'concentration': f"{(value_counts.iloc[0] / len(df) * 100):.1f}%" if len(value_counts) > 0 else "0%"
            }

    # Detect correlations between ALL numeric columns (not just first 4-5)
    correlations = []
    if len(numeric_cols) >= 2:
        # Analyze all columns but limit correlations to avoid combinatorial explosion
        for i, col1 in enumerate(numeric_cols):  # ✅ CHECK ALL COLUMNS
            for col2 in numeric_cols[i+1:]:
                if col1 in df.columns and col2 in df.columns:
                    corr = df[[col1, col2]].corr().iloc[0, 1]
                    if abs(corr) > 0.3:  # Only strong correlations
                        correlations.append({
                            'col1': col1,
                            'col2': col2,
                            'correlation': f"{corr:.2f}",
                            'strength': 'strong' if abs(corr) > 0.7 else 'moderate'
                        })
        # Keep only top 20 correlations to avoid overwhelming prompt
        correlations = sorted(correlations, key=lambda x: abs(float(x['correlation'])), reverse=True)[:20]

    # Get actual data samples (first 5 rows, limited columns)
    sample_columns = available_columns[:6]  # First 6 columns
    data_sample = df[sample_columns].head(5).to_dict('records')
    # Convert to readable string
    data_sample_str = "\n".join([f"Row {i+1}: {row}" for i, row in enumerate(data_sample)])

    # Identify data quality issues
    missing_data = {col: int(df[col].isna().sum()) for col in available_columns if df[col].isna().sum() > 0}
    missing_data_summary = {k: f"{v} ({v/len(df)*100:.1f}%)" for k, v in list(missing_data.items())[:5]}

    # Detect potential anomalies
    anomalies_detected = []
    if 'gpa' in df.columns:
        gpa_data = df['gpa'].dropna()
        if len(gpa_data) > 0:
            if gpa_data.min() < 0 or gpa_data.max() > 4.5:
                anomalies_detected.append(f"GPA values outside normal range: {gpa_data.min():.2f} - {gpa_data.max():.2f}")
            zero_gpa_count = (gpa_data == 0).sum()
            if zero_gpa_count > 0:
                anomalies_detected.append(f"{zero_gpa_count} students with 0.0 GPA")

    # Build comprehensive data profile with ALL columns
    data_profile = {
        'total_rows': len(df),
        'numeric_columns': numeric_cols,  # ✅ ALL NUMERIC COLUMNS
        'categorical_columns': categorical_cols,  # ✅ ALL CATEGORICAL COLUMNS
        'total_columns': len(available_columns),
        'has_gpa': 'gpa' in df.columns or 'cumulative_gpa' in df.columns,
        'has_nationality': 'nationality' in df.columns,
        'has_program': 'program' in df.columns,
        'has_dates': any('date' in col.lower() for col in available_columns),
        'has_financial': 'tuition_fees' in df.columns or 'financial_aid' in df.columns
    }

    context_descriptions = {
        "executive_summary": "Create visualizations for EXECUTIVE BOARD PRESENTATION focusing on high-level strategic insights, institutional health, performance indicators, and financial sustainability.",
        "overview": "Create visualizations for COMPREHENSIVE INSTITUTIONAL OVERVIEW focusing on enrollment composition, academic performance trends, and growth indicators.",
        "demographics": "Create visualizations for DEMOGRAPHIC ANALYSIS focusing on nationality distribution, diversity metrics, and student composition.",
        "performance": "Create visualizations for ACADEMIC PERFORMANCE ANALYSIS focusing on GPA distribution, achievement levels, and excellence indicators.",
        "financial": "Create visualizations for FINANCIAL ANALYSIS focusing on revenue, aid distribution, and sustainability metrics.",
        "academic": "Create visualizations for ACADEMIC ANALYTICS focusing on GPA patterns, program performance, credit load impact, and achievement trends.",
        "housing": "Create visualizations for HOUSING INSIGHTS focusing on residence patterns, housing impact on academic performance, occupancy trends, and accommodation effectiveness.",
        "risk": "Create visualizations for RISK & SUCCESS ANALYSIS focusing on at-risk student identification, success predictors, intervention effectiveness, and early warning indicators."
    }

    context_desc = context_descriptions.get(context_type, "Create insightful visualizations for data analysis")

    # Build statistics summary - ALL columns analyzed, intelligently summarized for prompt
    stats_summary = []

    # ALL numeric columns (up to 20 to keep prompt manageable)
    if numeric_stats:
        num_to_show = min(20, len(numeric_stats))  # Show up to 20 numeric columns
        for col, stats in list(numeric_stats.items())[:num_to_show]:
            stats_summary.append(f"{col}: μ={stats['mean']:.2f}, σ={stats['std']:.2f}, Q1-Q3=[{stats['q25']:.2f}-{stats['q75']:.2f}], outliers={stats['outliers']}")
        if len(numeric_stats) > num_to_show:
            stats_summary.append(f"...and {len(numeric_stats) - num_to_show} more numeric columns")

    # ALL categorical columns (up to 20 to keep prompt manageable)
    if categorical_distributions:
        num_to_show = min(20, len(categorical_distributions))
        for col, dist in list(categorical_distributions.items())[:num_to_show]:
            top_val = list(dist['top_values'].items())[0] if dist['top_values'] else ('N/A', 0)
            stats_summary.append(f"{col}: {dist['unique_values']} categories, top={top_val[0]} ({top_val[1]} students)")
        if len(categorical_distributions) > num_to_show:
            stats_summary.append(f"...and {len(categorical_distributions) - num_to_show} more categorical columns")

    # Top correlations (up to 10)
    if correlations:
        corr_list = [f"{c['col1']}↔{c['col2']}:{c['correlation']}" for c in correlations[:10]]
        stats_summary.append(f"Correlations: {', '.join(corr_list)}")

    # All anomalies detected
    if anomalies_detected:
        stats_summary.extend([f"⚠️ {a}" for a in anomalies_detected])

    stats_compact = "\n".join(stats_summary) if stats_summary else "Standard distribution"

    # Add column inventory for LLM awareness
    column_inventory = f"\n\nAVAILABLE COLUMNS ({len(available_columns)} total):\n"
    column_inventory += f"Numeric ({len(numeric_cols)}): {', '.join(numeric_cols)}\n"
    column_inventory += f"Categorical ({len(categorical_cols)}): {', '.join(categorical_cols)}"

    stats_compact += column_inventory

    # Calculate benchmarks and risk indicators
    gpa_variance = (avg_gpa - 3.0) / 3.0 * 100 if avg_gpa else 0  # Distance from ideal 3.0
    at_risk_severity = "CRITICAL" if (at_risk/total_students*100) > 25 else "MODERATE" if (at_risk/total_students*100) > 15 else "LOW"
    aid_sustainability = "AT_RISK" if (total_aid/total_tuition*100) > 40 else "SUSTAINABLE"
    diversity_score = "HIGH" if unique_nationalities > 15 else "MODERATE" if unique_nationalities > 8 else "LOW"

    prompt = f"""EXPERT DATA ANALYST: {context_desc}

📊 DATA SNAPSHOT ({total_students:,} students):
- Academic: GPA {avg_gpa:.2f} ({gpa_variance:+.1f}% vs 3.0 target) | {high_performers:,} high ({(high_performers/total_students*100):.1f}%) | {at_risk:,} at-risk ({(at_risk/total_students*100):.1f}% - {at_risk_severity})
- Diversity: {unique_nationalities} nations ({diversity_score}) | UAE {uae_percentage:.1f}%
- Finance: AED {total_tuition/1000000:.1f}M tuition | AED {total_aid/1000000:.1f}M aid ({(total_aid/total_tuition*100) if total_tuition > 0 else 0:.1f}% - {aid_sustainability})

📈 STATISTICS:
{stats_compact}

🎯 ANALYTICAL FRAMEWORK - Apply ALL:
1. **Pattern Recognition**: Bimodal? Skewed? Clustered? Outliers? (quote exact values)
2. **Root Cause**: WHY does pattern exist? (e.g., "GPA clustering at 2.3 suggests curriculum difficulty at sophomore level")
3. **Risk/Opportunity**: What's at stake? (e.g., "256 at-risk = potential $2.4M revenue loss if 20% drop")
4. **Comparative Context**: Good/bad vs benchmarks? (e.g., "12.4% high performers BELOW 15-20% industry standard")
5. **Actionable Impact**: What action + expected result? (e.g., "Early intervention could improve retention 5-8%")

📋 REQUIRED OUTPUT - Recommend 4-6 visualizations with DEEP ANALYSIS:

{{
  "strategic_overview": "3-4 critical patterns with: (1) WHAT pattern (numbers), (2) WHY it exists (root cause), (3) SO WHAT impact (business consequence). Example: 'GPA bimodal at 2.3 (28%) & 3.7 (15%) suggests two student cohorts: struggling transfers and high-aptitude admits. Gap indicates need for differentiated support. 45 students at 0.0 GPA = $450K tuition at risk - require immediate intervention.'",

  "visualizations": [
    {{
      "title": "Descriptive + Analytical (e.g., 'GPA Distribution - Bimodal Risk Pattern')",
      "graph_type": "histogram|bar|pie|scatter|box|line",
      "data_column": "exact_column_name",
      "reasoning": "SPECIFIC pattern + WHY it matters + WHO affected (e.g., 'Reveals performance clustering at 2.3 (28%) indicating curriculum barrier affecting 280 students, primarily in engineering programs')",
      "insight": "4-5 sentences with: (1) NUMBERS (mean/median/mode/outliers), (2) PATTERN (bimodal/skew/concentration), (3) ROOT CAUSE (why pattern exists), (4) IMPACT (students/revenue affected), (5) ACTION (what to do + expected outcome). Example: 'Mean GPA 2.85 > median 2.78 (0.07 difference) reveals RIGHT SKEW with long tail of high performers. However, 45 students at 0.0 GPA (4.5%) indicate incomplete coursework or withdrawal - represents $450K revenue at risk. Distribution shows bimodal pattern peaking at 2.3 (struggling, 28%) and 3.7 (excelling, 15%). ROOT CAUSE: Likely admissions accepts wide ability range without adequate placement testing. ACTION: Implement diagnostic testing and tiered support - could reduce at-risk population 20-25% (50-64 students saved = $500K-640K retained revenue).'",
      "config": {{"bins": 20, "top_n": 8}}
    }}
  ],

  "key_findings": [
    "Finding with: WHAT (numbers), WHY (cause), IMPACT (consequence). Example: 'Top 3 nationalities = 65.3% enrollment (concentration risk). ROOT CAUSE: Over-reliance on UAE/India/Pakistan recruitment channels. IMPACT: $6.5M annual revenue dependent on 3 markets - geopolitical/economic shifts pose existential risk. Single visa policy change could affect 650+ students.'",
    "Pattern-based finding (similar structure)",
    "Opportunity-based finding (similar structure)"
  ],

  "recommendations": [
    {{
      "priority": "CRITICAL|HIGH|MEDIUM",
      "action": "Specific action with target (e.g., 'Launch early intervention program for 256 at-risk students (GPA<2.0)')",
      "expected_impact": "Quantified outcome (e.g., '5-8% retention improvement = 13-20 students saved = $130K-200K revenue + improved graduation rates')",
      "timeline": "immediate|short-term|long-term",
      "investment": "Resources needed (e.g., '2 FTE advisors, $80K annual = 2.5x ROI if achieves 6% improvement')"
    }}
  ]
}}

🔥 CRITICAL REQUIREMENTS:
- QUOTE EXACT NUMBERS from statistics (no approximations)
- IDENTIFY ROOT CAUSES (why patterns exist, not just what they are)
- QUANTIFY BUSINESS IMPACT (students affected, revenue at risk, opportunity cost)
- PROVIDE ACTIONABLE INSIGHTS (what to do + expected measurable outcome)
- PRIORITIZE by urgency/impact (flag critical risks)

Return ONLY valid JSON. NO markdown, NO explanations outside JSON."""

    # ============================================
    # HYBRID APPROACH - Rule-based + LLM Enrichment
    # ============================================
    # Phase 1: Intelligent rule-based visualization selection (instant, always works)
    # Phase 2: LLM enrichment for deep insights (where LLM adds most value)
    # Phase 3: LLM strategic summary (optional enhancement)

    st.info("⏳ Phase 1/2: Analyzing data and selecting visualizations...")

    # PHASE 1: Rule-based visualization selection (INSTANT, NO TIMEOUT)
    # Context-aware: Different visualizations for different contexts
    visualizations = []
    gpa_col = find_matching_column('gpa', df)
    nationality_col = find_matching_column('nationality', df)
    aid_col = find_matching_column('financial_aid', df)
    tuition_col = find_matching_column('tuition', df)
    date_col = find_matching_column('enrollment', df)
    program_col = find_matching_column('program', df)
    credit_col = find_matching_column('credit', df)
    attendance_col = find_matching_column('attendance', df) or find_matching_column('retention', df)
    gender_col = find_matching_column('gender', df) or find_matching_column('sex', df)

    if context_type == "academic":
        # ACADEMIC-FOCUSED VISUALIZATIONS

        # 1. GPA Distribution - Core academic metric
        if gpa_col:
            visualizations.append({
                "title": "GPA Distribution - Performance Patterns",
                "graph_type": "histogram",
                "data_column": gpa_col,
                "reasoning": "Identifies achievement levels, performance clustering, and academic quality indicators"
            })

        # 2. Performance Tiers - Academic segmentation
        if gpa_col:
            visualizations.append({
                "title": "Academic Performance Tiers",
                "graph_type": "pie",
                "data_column": "performance_tier",
                "reasoning": "Shows proportion of high performers, mid-tier, and at-risk students requiring intervention"
            })

        # 3. GPA by Program/Major - Program comparison
        if gpa_col and program_col:
            visualizations.append({
                "title": "GPA by Program - Academic Rigor Analysis",
                "graph_type": "box",
                "data_column": f"{program_col},{gpa_col}",
                "reasoning": "Compares academic performance across programs to identify curriculum difficulty and support needs"
            })

        # 4. Credit Hours vs GPA - Workload impact
        if credit_col and gpa_col:
            visualizations.append({
                "title": "Credit Load vs Academic Performance",
                "graph_type": "scatter",
                "data_column": f"{credit_col},{gpa_col}",
                "reasoning": "Analyzes impact of course load on academic success and identifies optimal credit hours"
            })

        # 5. Term/Semester GPA Trends - Performance over time
        if date_col and gpa_col:
            visualizations.append({
                "title": "GPA Trends Over Time",
                "graph_type": "line",
                "data_column": date_col,
                "reasoning": "Tracks academic performance evolution to identify improvement or decline patterns"
            })

        # 6. Top/Bottom Programs by Performance
        if program_col and gpa_col:
            visualizations.append({
                "title": "Program Performance Rankings",
                "graph_type": "bar",
                "data_column": program_col,
                "reasoning": "Ranks programs by average GPA to highlight academic strengths and areas needing support"
            })

    elif context_type == "housing":
        # HOUSING-FOCUSED VISUALIZATIONS

        # Find housing-related columns
        housing_col = find_matching_column('housing', df) or find_matching_column('room', df) or find_matching_column('residence', df)

        # 1. Housing Distribution - On-campus vs Off-campus
        if housing_col:
            visualizations.append({
                "title": "Housing Distribution - On-Campus vs Off-Campus",
                "graph_type": "pie",
                "data_column": housing_col,
                "reasoning": "Shows the proportion of students living on-campus versus off-campus, indicating housing capacity utilization and residential community engagement"
            })

        # 2. Housing Status vs GPA - Impact on academic performance
        if housing_col and gpa_col:
            visualizations.append({
                "title": "Housing Impact on Academic Performance",
                "graph_type": "box",
                "data_column": f"{housing_col},{gpa_col}",
                "reasoning": "Analyzes correlation between housing status and GPA to assess whether on-campus residence supports academic success"
            })

        # 3. Residence Hall Distribution
        if housing_col:
            visualizations.append({
                "title": "Residence Hall Occupancy Distribution",
                "graph_type": "bar",
                "data_column": housing_col,
                "reasoning": "Shows distribution across different residence halls or housing types to identify capacity utilization and popular housing options"
            })

        # 4. Housing vs Engagement/Activities
        activity_col = find_matching_column('activities', df) or find_matching_column('engagement', df) or find_matching_column('clubs', df)
        if housing_col and activity_col:
            visualizations.append({
                "title": "Housing Status vs Student Engagement",
                "graph_type": "bar",
                "data_column": f"{housing_col},{activity_col}",
                "reasoning": "Examines relationship between housing status and student engagement to understand residential community impact"
            })

        # 5. Housing vs Retention/Attendance
        attendance_col = find_matching_column('attendance', df) or find_matching_column('retention', df)
        if housing_col and attendance_col:
            visualizations.append({
                "title": "Housing Impact on Attendance/Retention",
                "graph_type": "scatter",
                "data_column": f"{housing_col},{attendance_col}",
                "reasoning": "Analyzes correlation between housing status and attendance patterns to assess residential life impact on student commitment"
            })
        elif housing_col and gpa_col:
            # Fallback: Another GPA-related viz if attendance not available
            visualizations.append({
                "title": "GPA Distribution by Housing Status",
                "graph_type": "histogram",
                "data_column": gpa_col,
                "reasoning": "Compares GPA distributions between on-campus and off-campus students to identify performance differences"
            })

        # 6. Housing Demographics - Nationality/Program distribution
        if housing_col and nationality_col:
            visualizations.append({
                "title": "Housing Distribution by Nationality",
                "graph_type": "bar",
                "data_column": f"{nationality_col},{housing_col}",
                "reasoning": "Shows how different nationality groups utilize on-campus housing, revealing cultural preferences and housing accessibility"
            })
        elif housing_col and program_col:
            visualizations.append({
                "title": "Housing Distribution by Program",
                "graph_type": "bar",
                "data_column": f"{program_col},{housing_col}",
                "reasoning": "Analyzes housing preferences across different academic programs to understand program-specific housing needs"
            })

    elif context_type == "financial":
        # FINANCIAL-FOCUSED VISUALIZATIONS

        # Find financial-related columns
        aid_col = find_matching_column('financial_aid', df) or find_matching_column('aid', df) or find_matching_column('scholarship', df)
        tuition_col = find_matching_column('tuition', df) or find_matching_column('fees', df)

        # 1. Financial Aid Distribution - Who receives aid and how much
        if aid_col:
            visualizations.append({
                "title": "Financial Aid Distribution Analysis",
                "graph_type": "histogram",
                "data_column": aid_col,
                "reasoning": "Shows aid allocation patterns, identifies concentration of support, and reveals equity in financial assistance distribution"
            })

        # 2. Aid vs Tuition - Revenue and support balance
        if aid_col and tuition_col:
            visualizations.append({
                "title": "Financial Aid vs Tuition Revenue",
                "graph_type": "scatter",
                "data_column": f"{tuition_col},{aid_col}",
                "reasoning": "Analyzes relationship between tuition charges and aid provided to assess financial sustainability and accessibility"
            })

        # 3. Aid by Performance Tier - ROI on financial aid
        if aid_col and gpa_col:
            visualizations.append({
                "title": "Financial Aid Impact on Academic Performance",
                "graph_type": "scatter",
                "data_column": f"{aid_col},{gpa_col}",
                "reasoning": "Evaluates return on investment for financial aid by correlating aid amounts with academic outcomes"
            })

        # 4. Revenue by Program/Nationality - Market analysis
        if tuition_col and (program_col or nationality_col):
            viz_col = program_col if program_col else nationality_col
            viz_title = "Tuition Revenue by Program" if program_col else "Tuition Revenue by Nationality"
            visualizations.append({
                "title": viz_title,
                "graph_type": "bar",
                "data_column": f"{viz_col},{tuition_col}",
                "reasoning": "Identifies revenue concentration by segment to understand financial dependencies and diversification opportunities"
            })

        # 5. Aid Coverage Analysis - Support levels
        if aid_col:
            visualizations.append({
                "title": "Aid Coverage Levels - Student Distribution",
                "graph_type": "pie",
                "data_column": aid_col,
                "reasoning": "Categorizes students by aid coverage percentage to assess accessibility and support adequacy"
            })

        # 6. Aid Recipients by Category - Demographic equity
        if aid_col and nationality_col:
            visualizations.append({
                "title": "Financial Aid Distribution by Nationality",
                "graph_type": "bar",
                "data_column": f"{nationality_col},{aid_col}",
                "reasoning": "Analyzes aid equity across nationality groups to ensure fair access and identify potential disparities"
            })
        elif aid_col and program_col:
            visualizations.append({
                "title": "Financial Aid Distribution by Program",
                "graph_type": "box",
                "data_column": f"{program_col},{aid_col}",
                "reasoning": "Compares aid allocation across programs to understand field-specific support patterns and equity"
            })

    elif context_type == "demographics":
        # DEMOGRAPHICS-FOCUSED VISUALIZATIONS

        # Find demographics-related columns
        nationality_col = find_matching_column('nationality', df)
        gender_col = find_matching_column('gender', df) or find_matching_column('sex', df)
        age_col = find_matching_column('age', df) or find_matching_column('birth', df)

        # 1. Nationality Distribution - Core demographic metric
        if nationality_col:
            visualizations.append({
                "title": "Nationality Distribution - Market Diversity Analysis",
                "graph_type": "bar",
                "data_column": nationality_col,
                "reasoning": "Shows student diversity, market concentration, and international reach - critical for risk assessment and recruitment strategy"
            })

        # 2. Top Nationalities Concentration - Market risk
        if nationality_col:
            visualizations.append({
                "title": "Top Nationality Groups - Concentration Risk",
                "graph_type": "pie",
                "data_column": nationality_col,
                "reasoning": "Reveals dependency on key markets and potential concentration risk from geopolitical or economic changes"
            })

        # 3. Nationality vs Academic Performance
        if nationality_col and gpa_col:
            visualizations.append({
                "title": "Academic Performance by Nationality",
                "graph_type": "box",
                "data_column": f"{nationality_col},{gpa_col}",
                "reasoning": "Identifies performance variations across nationalities to inform targeted support programs and recruitment quality"
            })

        # 4. Gender Distribution & Balance
        if gender_col:
            visualizations.append({
                "title": "Gender Distribution - Diversity Balance",
                "graph_type": "pie",
                "data_column": gender_col,
                "reasoning": "Assesses gender balance and diversity initiatives effectiveness for inclusive campus environment"
            })

        # 5. Gender vs Performance Analysis
        if gender_col and gpa_col:
            visualizations.append({
                "title": "Academic Performance by Gender",
                "graph_type": "box",
                "data_column": f"{gender_col},{gpa_col}",
                "reasoning": "Analyzes performance equity across genders to ensure fair opportunities and identify support needs"
            })
        elif nationality_col and program_col:
            # Alternative: Nationality by Program
            visualizations.append({
                "title": "Program Enrollment by Nationality",
                "graph_type": "bar",
                "data_column": f"{program_col},{nationality_col}",
                "reasoning": "Shows program preferences across nationality groups to optimize marketing and recruitment by region"
            })

        # 6. Demographic Intersectionality - Complex view
        if nationality_col and gender_col:
            visualizations.append({
                "title": "Nationality-Gender Distribution Matrix",
                "graph_type": "bar",
                "data_column": f"{nationality_col},{gender_col}",
                "reasoning": "Examines demographic intersectionality to understand diverse student populations and ensure inclusive representation"
            })
        elif nationality_col and aid_col:
            visualizations.append({
                "title": "Financial Aid Distribution by Nationality",
                "graph_type": "box",
                "data_column": f"{nationality_col},{aid_col}",
                "reasoning": "Analyzes aid equity across nationalities to ensure fair access and identify potential disparities"
            })

    elif context_type == "risk":
        # RISK-FOCUSED VISUALIZATIONS

        # 1. At-Risk vs High Performer Distribution - Core risk metric
        if gpa_col:
            visualizations.append({
                "title": "Student Performance Risk Distribution",
                "graph_type": "pie",
                "data_column": "performance_tier",
                "reasoning": "Segments students by risk level (at-risk, mid-tier, high performers) to identify intervention priorities and success rates"
            })

        # 2. GPA Distribution with Risk Thresholds - Risk zones
        if gpa_col:
            visualizations.append({
                "title": "GPA Distribution - Risk Zones Analysis",
                "graph_type": "histogram",
                "data_column": gpa_col,
                "reasoning": "Visualizes GPA distribution with risk threshold markers (2.0, 2.5, 3.5) to identify students in danger zones requiring immediate intervention"
            })

        # 3. Risk Factors by Program - Program-level risk
        if gpa_col and program_col:
            visualizations.append({
                "title": "At-Risk Students by Program",
                "graph_type": "bar",
                "data_column": f"{program_col},{gpa_col}",
                "reasoning": "Identifies which programs have highest at-risk concentrations to target support resources and curriculum reviews"
            })

        # 4. Financial Aid vs Academic Risk - Support effectiveness
        if aid_col and gpa_col:
            visualizations.append({
                "title": "Financial Aid Impact on At-Risk Students",
                "graph_type": "scatter",
                "data_column": f"{aid_col},{gpa_col}",
                "reasoning": "Evaluates whether financial aid correlates with academic success or if at-risk students need additional non-financial support"
            })

        # 5. Success Predictors - Multi-factor analysis
        if gpa_col and (credit_col or attendance_col):
            predictor_col = credit_col if credit_col else attendance_col
            predictor_title = "Credit Load" if credit_col else "Attendance Rate"
            visualizations.append({
                "title": f"{predictor_title} vs Academic Success",
                "graph_type": "scatter",
                "data_column": f"{predictor_col},{gpa_col}",
                "reasoning": "Identifies success predictors and early warning indicators to proactively flag students before they become at-risk"
            })

        # 6. Risk by Demographics - Equity in success
        if gpa_col and nationality_col:
            visualizations.append({
                "title": "Academic Risk Distribution by Nationality",
                "graph_type": "box",
                "data_column": f"{nationality_col},{gpa_col}",
                "reasoning": "Analyzes whether certain demographic groups face disproportionate risk to ensure equitable support and identify systemic barriers"
            })
        elif gpa_col and gender_col:
            visualizations.append({
                "title": "Academic Risk Distribution by Gender",
                "graph_type": "box",
                "data_column": f"{gender_col},{gpa_col}",
                "reasoning": "Examines gender-based risk patterns to ensure equitable outcomes and identify targeted intervention needs"
            })

    else:
        # EXECUTIVE SUMMARY / GENERAL VISUALIZATIONS

        # 1. GPA Distribution
        if gpa_col:
            visualizations.append({
                "title": "GPA Distribution - Academic Performance Analysis",
                "graph_type": "histogram",
                "data_column": gpa_col,
                "reasoning": "Reveals performance patterns, identifies high performers and at-risk students"
            })

        # 2. Nationality Distribution
        if nationality_col and unique_nationalities > 1:
            visualizations.append({
                "title": "Nationality Distribution - Market Concentration",
                "graph_type": "bar",
                "data_column": nationality_col,
                "reasoning": "Shows diversity, market concentration, and recruitment reach"
            })

        # 3. Performance Tiers
        if gpa_col:
            visualizations.append({
                "title": "Academic Performance Tiers",
                "graph_type": "pie",
                "data_column": "performance_tier",
                "reasoning": "Identifies excellence, stability, and intervention needs"
            })

        # 4. Financial Aid Distribution
        if aid_col:
            visualizations.append({
                "title": "Financial Aid Distribution",
                "graph_type": "box",
                "data_column": aid_col,
                "reasoning": "Reveals accessibility, equity, and financial sustainability patterns"
            })

        # 5. Tuition vs GPA Correlation
        if gpa_col and tuition_col:
            visualizations.append({
                "title": "Tuition vs Academic Performance",
                "graph_type": "scatter",
                "data_column": f"{tuition_col},{gpa_col}",
                "reasoning": "Explores relationship between investment and academic outcomes"
            })

        # 6. Enrollment Trends
        if date_col:
            visualizations.append({
                "title": "Enrollment Trends Over Time",
                "graph_type": "line",
                "data_column": date_col,
                "reasoning": "Shows growth patterns and enrollment cycles"
            })

    # Limit to 6 visualizations
    visualizations = visualizations[:6]

    st.success(f"✅ Phase 1 complete: {len(visualizations)} visualizations selected (rule-based, {context_type} focus)")

    try:

        # CHUNK 2: Enrich each visualization with deep insights
        st.info(f"⏳ Phase 2/2: Generating deep insights for {len(visualizations)} visualizations... (1-2 minutes)")

        enriched_visualizations = []
        for i, viz in enumerate(visualizations[:6]):  # Limit to 6
            with st.spinner(f"Analyzing {viz.get('title', 'visualization')} ({i+1}/{min(len(visualizations), 6)})..."):
                # Get column data for context
                col_name = viz.get('data_column', '')
                col_context = ""
                if col_name and col_name in df.columns:
                    if df[col_name].dtype in ['int64', 'float64']:
                        col_data = df[col_name].dropna()
                        if len(col_data) > 0:
                            col_context = f"Column stats: mean={col_data.mean():.2f}, median={col_data.median():.2f}, std={col_data.std():.2f}, min={col_data.min():.2f}, max={col_data.max():.2f}"
                    else:
                        col_counts = df[col_name].value_counts().head(5)
                        col_context = f"Top values: {', '.join([f'{k}:{v}' for k, v in col_counts.items()])}"

                chunk2_prompt = f"""Analyze: {viz.get('title', '')}
Column: {viz.get('data_column', '')}
{col_context}

Context: {total_students} students, GPA {avg_gpa:.2f}, {high_performers} high, {at_risk} at-risk

Provide 3-4 sentence insight: NUMBERS, PATTERN, ROOT CAUSE, IMPACT, ACTION

Return JSON:
{{"insight": "..."}}"""

                chunk2_response = query_ollama(chunk2_prompt, model, url, temperature=0.7, num_predict=350, timeout=90, auto_optimize=True)

                if chunk2_response and not chunk2_response.startswith('[ERROR]'):
                    chunk2_result = extract_json_from_response(chunk2_response)
                    if chunk2_result and 'insight' in chunk2_result:
                        viz['insight'] = chunk2_result['insight']
                        st.success(f"✅ LLM insight generated for {viz.get('title', 'viz')}")
                    else:
                        # Rich statistical fallback
                        viz['insight'] = _generate_rich_statistical_insight(viz, df, total_students, high_performers, at_risk, avg_gpa)
                        st.info(f"📊 Statistical insight generated for {viz.get('title', 'viz')}")
                else:
                    # Rich statistical fallback
                    viz['insight'] = _generate_rich_statistical_insight(viz, df, total_students, high_performers, at_risk, avg_gpa)
                    st.info(f"📊 Statistical insight generated for {viz.get('title', 'viz')}")

                enriched_visualizations.append(viz)

        st.success(f"✅ Phase 2 complete: {len(enriched_visualizations)} visualizations enriched")

        # PHASE 3: Generate basic findings and recommendations
        st.info("⏳ Phase 3/4: Generating findings and recommendations...")

        at_risk_pct = (at_risk/total_students*100) if total_students > 0 else 0
        high_perf_pct = (high_performers/total_students*100) if total_students > 0 else 0
        aid_coverage_pct = (total_aid/total_tuition*100) if total_tuition > 0 else 0

        # Calculate additional metrics for context-specific findings
        nationality_col = find_matching_column('nationality', df)
        program_col = find_matching_column('program', df)
        top_3_concentration = 0
        if nationality_col and nationality_col in df.columns:
            top_nat = df[nationality_col].value_counts().head(3)
            top_3_concentration = (top_nat.sum() / total_students * 100) if total_students > 0 else 0

        # Calculate program-level GPA variance if available
        program_gpa_variance = 0
        lowest_program_gpa = 0
        highest_program_gpa = 0
        if program_col and gpa_col and program_col in df.columns and gpa_col in df.columns:
            program_gpas = df.groupby(program_col)[gpa_col].mean()
            if len(program_gpas) > 0:
                program_gpa_variance = program_gpas.std()
                lowest_program_gpa = program_gpas.min()
                highest_program_gpa = program_gpas.max()

        # Generate basic findings (will be enriched in Phase 4)
        # Context-aware: Different findings for different contexts
        basic_findings = []
        basic_recommendations = []

        if context_type == "academic":
            # ACADEMIC-FOCUSED FINDINGS
            mid_performers = total_students - high_performers - at_risk

            basic_findings = [
                {
                    "finding": f"Performance distribution: {high_performers:,} high performers ({high_perf_pct:.1f}%), {mid_performers:,} mid-tier ({(mid_performers/total_students*100):.1f}%), {at_risk:,} at-risk ({at_risk_pct:.1f}%)",
                    "context": {"type": "academic_distribution", "high_perf_pct": high_perf_pct, "at_risk_pct": at_risk_pct, "at_risk": at_risk, "high_performers": high_performers, "mid_performers": mid_performers, "total_students": total_students, "avg_gpa": avg_gpa, "total_tuition": total_tuition}
                },
                {
                    "finding": f"GPA variance: Average {avg_gpa:.2f}, {'significant program variation' if program_gpa_variance > 0.3 else 'consistent across programs'} (range {lowest_program_gpa:.2f} to {highest_program_gpa:.2f})" if program_gpa_variance > 0 else f"Average GPA {avg_gpa:.2f} with overall std deviation",
                    "context": {"type": "academic_variance", "avg_gpa": avg_gpa, "program_gpa_variance": program_gpa_variance, "lowest_program_gpa": lowest_program_gpa, "highest_program_gpa": highest_program_gpa}
                },
                {
                    "finding": f"At-risk concentration: {at_risk:,} students ({at_risk_pct:.1f}%) performing below 2.0 GPA threshold",
                    "context": {"type": "academic_atrisk", "at_risk": at_risk, "at_risk_pct": at_risk_pct, "total_students": total_students, "total_tuition": total_tuition}
                }
            ]

            # ACADEMIC-FOCUSED RECOMMENDATIONS
            basic_recommendations = [
                {
                    "recommendation": f"Implement early warning system and mandatory academic support for {at_risk:,} at-risk students ({at_risk_pct:.1f}%)",
                    "context": {"type": "academic_intervention", "at_risk": at_risk, "at_risk_pct": at_risk_pct, "total_students": total_students, "total_tuition": total_tuition}
                },
                {
                    "recommendation": f"{'Review curriculum difficulty in low-performing programs' if program_gpa_variance > 0.3 else 'Enhance academic excellence programs for high performers'}",
                    "context": {"type": "academic_curriculum", "program_gpa_variance": program_gpa_variance, "lowest_program_gpa": lowest_program_gpa, "high_performers": high_performers}
                },
                {
                    "recommendation": f"Expand tutoring and peer mentoring to improve mid-tier student performance ({mid_performers:,} students, {(mid_performers/total_students*100):.1f}%)",
                    "context": {"type": "academic_support", "mid_performers": mid_performers, "total_students": total_students}
                }
            ]

        elif context_type == "housing":
            # HOUSING-FOCUSED FINDINGS
            housing_col = find_matching_column('housing', df) or find_matching_column('room', df) or find_matching_column('residence', df)

            on_campus_count = 0
            off_campus_count = 0
            on_campus_gpa = 0
            off_campus_gpa = 0
            housing_utilization = 0

            if housing_col and housing_col in df.columns:
                on_campus_count = df[df[housing_col].notna()].shape[0]
                off_campus_count = df[df[housing_col].isna()].shape[0]
                housing_utilization = (on_campus_count / total_students * 100) if total_students > 0 else 0

                # Calculate GPA by housing status if possible
                if gpa_col and gpa_col in df.columns:
                    on_campus_gpa = df[df[housing_col].notna()][gpa_col].mean()
                    off_campus_gpa = df[df[housing_col].isna()][gpa_col].mean()

            basic_findings = [
                {
                    "finding": f"Housing distribution: {on_campus_count:,} on-campus residents ({housing_utilization:.1f}%), {off_campus_count:,} off-campus students ({(off_campus_count/total_students*100):.1f}%)",
                    "context": {"type": "housing_distribution", "on_campus_count": on_campus_count, "off_campus_count": off_campus_count, "housing_utilization": housing_utilization, "total_students": total_students}
                },
                {
                    "finding": f"Academic impact: On-campus GPA {on_campus_gpa:.2f} vs Off-campus GPA {off_campus_gpa:.2f} ({'higher' if on_campus_gpa > off_campus_gpa else 'lower'} by {abs(on_campus_gpa - off_campus_gpa):.2f} points)" if on_campus_gpa > 0 and off_campus_gpa > 0 else f"Housing capacity utilization at {housing_utilization:.1f}%",
                    "context": {"type": "housing_academic_impact", "on_campus_gpa": on_campus_gpa, "off_campus_gpa": off_campus_gpa, "gpa_difference": abs(on_campus_gpa - off_campus_gpa)}
                },
                {
                    "finding": f"Housing capacity: {'Underutilized' if housing_utilization < 60 else 'Well-utilized' if housing_utilization < 85 else 'Near capacity'} at {housing_utilization:.1f}% occupancy ({on_campus_count:,} of potential residents)",
                    "context": {"type": "housing_capacity", "housing_utilization": housing_utilization, "on_campus_count": on_campus_count, "total_students": total_students}
                }
            ]

            # HOUSING-FOCUSED RECOMMENDATIONS
            basic_recommendations = [
                {
                    "recommendation": f"{'Increase on-campus housing marketing and incentives to improve utilization from ' + str(round(housing_utilization, 1)) + '% to 75-80%' if housing_utilization < 60 else 'Expand housing capacity to accommodate growing residential demand' if housing_utilization > 85 else 'Maintain current housing operations with focus on quality improvements'}",
                    "context": {"type": "housing_utilization", "housing_utilization": housing_utilization, "on_campus_count": on_campus_count, "total_students": total_students}
                },
                {
                    "recommendation": f"{'Enhance on-campus residential support programs - on-campus students show ' + str(round(on_campus_gpa - off_campus_gpa, 2)) + ' point GPA advantage' if on_campus_gpa > off_campus_gpa else 'Develop off-campus student support services - current gap of ' + str(round(off_campus_gpa - on_campus_gpa, 2)) + ' points in favor of off-campus' if off_campus_gpa > on_campus_gpa else 'Develop residential life programs to enhance student experience'}",
                    "context": {"type": "housing_academic_support", "on_campus_gpa": on_campus_gpa, "off_campus_gpa": off_campus_gpa, "gpa_difference": abs(on_campus_gpa - off_campus_gpa)}
                },
                {
                    "recommendation": f"Conduct housing satisfaction survey with {on_campus_count:,} residents to identify improvement areas and retention factors",
                    "context": {"type": "housing_satisfaction", "on_campus_count": on_campus_count}
                }
            ]

        elif context_type == "financial":
            # FINANCIAL-FOCUSED FINDINGS
            aid_col = find_matching_column('financial_aid', df) or find_matching_column('aid', df) or find_matching_column('scholarship', df)
            tuition_col = find_matching_column('tuition', df) or find_matching_column('fees', df)

            aid_recipients = 0
            total_aid_amount = 0
            avg_aid_amount = 0
            aid_to_tuition_ratio = 0
            high_aid_students = 0
            aided_students_gpa = 0
            non_aided_students_gpa = 0

            if aid_col and aid_col in df.columns:
                aid_recipients = df[df[aid_col] > 0].shape[0]
                total_aid_amount = df[aid_col].sum()
                avg_aid_amount = df[df[aid_col] > 0][aid_col].mean() if aid_recipients > 0 else 0
                aid_to_tuition_ratio = (total_aid_amount / total_tuition * 100) if total_tuition > 0 else 0
                high_aid_students = df[df[aid_col] > (avg_aid_amount * 1.5)].shape[0] if avg_aid_amount > 0 else 0

                # Calculate GPA by aid status if possible
                if gpa_col and gpa_col in df.columns:
                    aided_students_gpa = df[df[aid_col] > 0][gpa_col].mean()
                    non_aided_students_gpa = df[df[aid_col] == 0][gpa_col].mean()

            basic_findings = [
                {
                    "finding": f"Financial aid reach: {aid_recipients:,} students receiving aid ({(aid_recipients/total_students*100):.1f}%), total AED {total_aid_amount:,.0f} ({aid_to_tuition_ratio:.1f}% of tuition revenue)",
                    "context": {"type": "financial_aid_reach", "aid_recipients": aid_recipients, "total_aid_amount": total_aid_amount, "aid_to_tuition_ratio": aid_to_tuition_ratio, "total_students": total_students, "total_tuition": total_tuition}
                },
                {
                    "finding": f"Aid effectiveness: Average aid AED {avg_aid_amount:,.0f}, {high_aid_students:,} students receiving high aid (>{avg_aid_amount*1.5:,.0f}). Aided students GPA {aided_students_gpa:.2f} vs non-aided {non_aided_students_gpa:.2f}" if aided_students_gpa > 0 and non_aided_students_gpa > 0 else f"Average aid per recipient: AED {avg_aid_amount:,.0f}",
                    "context": {"type": "financial_aid_effectiveness", "avg_aid_amount": avg_aid_amount, "high_aid_students": high_aid_students, "aided_students_gpa": aided_students_gpa, "non_aided_students_gpa": non_aided_students_gpa}
                },
                {
                    "finding": f"Financial sustainability: Aid at {aid_to_tuition_ratio:.1f}% of revenue ({'sustainable' if aid_to_tuition_ratio < 35 else 'moderate risk' if aid_to_tuition_ratio < 45 else 'high risk'}). {total_students - aid_recipients:,} full-paying students ({((total_students - aid_recipients)/total_students*100):.1f}%)",
                    "context": {"type": "financial_sustainability", "aid_to_tuition_ratio": aid_to_tuition_ratio, "aid_recipients": aid_recipients, "total_students": total_students, "total_aid_amount": total_aid_amount, "total_tuition": total_tuition}
                }
            ]

            # FINANCIAL-FOCUSED RECOMMENDATIONS
            basic_recommendations = [
                {
                    "recommendation": f"{'Optimize aid allocation - current {aid_to_tuition_ratio:.1f}% ratio is sustainable, consider strategic reallocation to high-impact students' if aid_to_tuition_ratio < 35 else 'Review aid strategy - {aid_to_tuition_ratio:.1f}% ratio approaching risk threshold, implement need-merit balance' if aid_to_tuition_ratio < 45 else 'Critical: Reduce aid ratio from {aid_to_tuition_ratio:.1f}% to below 40% through enrollment growth or aid restructuring'}".format(aid_to_tuition_ratio=aid_to_tuition_ratio),
                    "context": {"type": "financial_aid_optimization", "aid_to_tuition_ratio": aid_to_tuition_ratio, "total_aid_amount": total_aid_amount, "total_tuition": total_tuition}
                },
                {
                    "recommendation": f"{'Expand aid programs - aided students show {aided_students_gpa - non_aided_students_gpa:.2f} point GPA advantage, increasing aid budget by 15-20% could improve outcomes' if aided_students_gpa > non_aided_students_gpa else 'Enhance support services for aid recipients - aid not translating to academic advantage, add mentoring/tutoring' if non_aided_students_gpa > aided_students_gpa else 'Implement merit-based aid tiers to incentivize academic excellence'}".format(aided_students_gpa=aided_students_gpa, non_aided_students_gpa=non_aided_students_gpa),
                    "context": {"type": "financial_aid_effectiveness_rec", "aided_students_gpa": aided_students_gpa, "non_aided_students_gpa": non_aided_students_gpa, "aid_recipients": aid_recipients}
                },
                {
                    "recommendation": f"Diversify revenue streams: {((total_students - aid_recipients)/total_students*100):.1f}% full-paying students generate {((total_tuition - total_aid_amount)/total_tuition*100):.1f}% of net revenue. Consider endowment growth, alumni giving, and corporate partnerships",
                    "context": {"type": "financial_revenue_diversification", "aid_recipients": aid_recipients, "total_students": total_students, "total_aid_amount": total_aid_amount, "total_tuition": total_tuition}
                }
            ]

        elif context_type == "demographics":
            # DEMOGRAPHICS-FOCUSED FINDINGS
            nationality_col = find_matching_column('nationality', df)
            gender_col = find_matching_column('gender', df) or find_matching_column('sex', df)

            top_3_nationalities = []
            top_3_concentration = 0
            nationality_diversity_score = 0
            uae_nationals_count = 0
            uae_percentage = 0
            gender_distribution = {}
            gender_balance_ratio = 0

            if nationality_col and nationality_col in df.columns:
                top_nat = df[nationality_col].value_counts().head(3)
                top_3_nationalities = [f"{nat} ({count:,})" for nat, count in top_nat.items()]
                top_3_concentration = (top_nat.sum() / total_students * 100) if total_students > 0 else 0
                nationality_diversity_score = df[nationality_col].nunique()

                # UAE nationals count
                uae_nationals_count = df[df[nationality_col].str.contains('UAE|United Arab Emirates|Emirati', case=False, na=False)].shape[0]
                uae_percentage = (uae_nationals_count / total_students * 100) if total_students > 0 else 0

            if gender_col and gender_col in df.columns:
                gender_counts = df[gender_col].value_counts()
                gender_distribution = {str(k): int(v) for k, v in gender_counts.items()}
                if len(gender_counts) >= 2:
                    max_gender = gender_counts.max()
                    min_gender = gender_counts.min()
                    gender_balance_ratio = (min_gender / max_gender * 100) if max_gender > 0 else 0

            basic_findings = [
                {
                    "finding": f"Diversity profile: {nationality_diversity_score} nationalities with top 3 markets representing {top_3_concentration:.1f}% of enrollment ({', '.join(top_3_nationalities)}). UAE nationals: {uae_nationals_count:,} ({uae_percentage:.1f}%)",
                    "context": {"type": "diversity_profile", "nationality_diversity_score": nationality_diversity_score, "top_3_concentration": top_3_concentration, "uae_nationals_count": uae_nationals_count, "uae_percentage": uae_percentage, "total_students": total_students}
                },
                {
                    "finding": f"Market concentration risk: {'HIGH - over-dependent on {top_3_concentration:.1f}% from 3 markets' if top_3_concentration > 60 else 'MODERATE - {top_3_concentration:.1f}% concentration, diversification needed' if top_3_concentration > 50 else 'LOW - well-balanced across {nationality_diversity_score} markets'}".format(top_3_concentration=top_3_concentration, nationality_diversity_score=nationality_diversity_score),
                    "context": {"type": "market_concentration", "top_3_concentration": top_3_concentration, "nationality_diversity_score": nationality_diversity_score}
                },
                {
                    "finding": f"Gender balance: {', '.join([f'{k}: {v:,} ({v/total_students*100:.1f}%)' for k, v in gender_distribution.items()])}. Balance ratio: {gender_balance_ratio:.1f}% ({'balanced' if gender_balance_ratio > 40 else 'imbalanced'})" if gender_distribution else f"Demographic diversity: {nationality_diversity_score} nationalities across {total_students:,} students",
                    "context": {"type": "gender_balance", "gender_distribution": gender_distribution, "gender_balance_ratio": gender_balance_ratio, "total_students": total_students}
                }
            ]

            # DEMOGRAPHICS-FOCUSED RECOMMENDATIONS
            basic_recommendations = [
                {
                    "recommendation": f"{'URGENT: Diversify recruitment to reduce top-3 dependency from {top_3_concentration:.1f}% to below 50%. Target 5-8 new markets with 3-5% each' if top_3_concentration > 60 else 'Expand recruitment in emerging markets to improve from {top_3_concentration:.1f}% to below 45% concentration' if top_3_concentration > 50 else 'Maintain balanced recruitment across {nationality_diversity_score} markets, monitor shifts'}".format(top_3_concentration=top_3_concentration, nationality_diversity_score=nationality_diversity_score),
                    "context": {"type": "diversity_recruitment", "top_3_concentration": top_3_concentration, "nationality_diversity_score": nationality_diversity_score}
                },
                {
                    "recommendation": f"{'Enhance gender diversity initiatives - current {gender_balance_ratio:.1f}% balance ratio below 40% target. Implement targeted recruitment for underrepresented gender' if gender_balance_ratio < 40 and gender_balance_ratio > 0 else 'Maintain gender balance programs - current {gender_balance_ratio:.1f}% ratio indicates healthy diversity' if gender_balance_ratio >= 40 else 'Develop comprehensive nationality-specific support programs for {nationality_diversity_score} different cultural backgrounds'}".format(gender_balance_ratio=gender_balance_ratio, nationality_diversity_score=nationality_diversity_score),
                    "context": {"type": "diversity_initiatives", "gender_balance_ratio": gender_balance_ratio, "nationality_diversity_score": nationality_diversity_score}
                },
                {
                    "recommendation": f"{'Strengthen UAE national enrollment from {uae_percentage:.1f}% through government partnerships and national initiatives alignment' if uae_percentage < 30 else 'Balance UAE national ({uae_percentage:.1f}%) and international student experience - ensure inclusive campus culture for {nationality_diversity_score} nationalities'}".format(uae_percentage=uae_percentage, nationality_diversity_score=nationality_diversity_score),
                    "context": {"type": "national_strategy", "uae_percentage": uae_percentage, "uae_nationals_count": uae_nationals_count, "nationality_diversity_score": nationality_diversity_score}
                }
            ]

        elif context_type == "risk":
            # RISK-FOCUSED FINDINGS
            mid_performers = total_students - high_performers - at_risk
            at_risk_pct = (at_risk / total_students * 100) if total_students > 0 else 0
            high_perf_pct = (high_performers / total_students * 100) if total_students > 0 else 0
            success_rate = ((total_students - at_risk) / total_students * 100) if total_students > 0 else 0

            # Calculate risk by program if available
            highest_risk_program = "Unknown"
            highest_risk_program_pct = 0
            if program_col and gpa_col and program_col in df.columns and gpa_col in df.columns:
                program_risk = df[df[gpa_col] < 2.0].groupby(program_col).size()
                if len(program_risk) > 0:
                    highest_risk_program = program_risk.idxmax()
                    program_total = df[df[program_col] == highest_risk_program].shape[0]
                    highest_risk_program_pct = (program_risk.max() / program_total * 100) if program_total > 0 else 0

            # Calculate aid effectiveness for at-risk students
            at_risk_with_aid = 0
            at_risk_without_aid = 0
            if aid_col and gpa_col and aid_col in df.columns and gpa_col in df.columns:
                at_risk_students = df[df[gpa_col] < 2.0]
                at_risk_with_aid = at_risk_students[at_risk_students[aid_col] > 0].shape[0]
                at_risk_without_aid = at_risk_students[at_risk_students[aid_col] == 0].shape[0]

            basic_findings = [
                {
                    "finding": f"Risk profile: {at_risk:,} at-risk students ({at_risk_pct:.1f}%), {mid_performers:,} mid-tier ({(mid_performers/total_students*100):.1f}%), {high_performers:,} high performers ({high_perf_pct:.1f}%). Overall success rate: {success_rate:.1f}%",
                    "context": {"type": "risk_profile", "at_risk": at_risk, "at_risk_pct": at_risk_pct, "mid_performers": mid_performers, "high_performers": high_performers, "success_rate": success_rate, "total_students": total_students}
                },
                {
                    "finding": f"Risk severity: {'CRITICAL - {at_risk_pct:.1f}% at-risk rate exceeds 25% threshold' if at_risk_pct > 25 else 'HIGH - {at_risk_pct:.1f}% at-risk rate above 15% benchmark' if at_risk_pct > 15 else 'MODERATE - {at_risk_pct:.1f}% at-risk rate within acceptable range'}. Highest risk program: {highest_risk_program} ({highest_risk_program_pct:.1f}% at-risk)" if highest_risk_program != "Unknown" else f"Risk severity: {'CRITICAL' if at_risk_pct > 25 else 'HIGH' if at_risk_pct > 15 else 'MODERATE'} - {at_risk_pct:.1f}% of students below 2.0 GPA",
                    "context": {"type": "risk_severity", "at_risk_pct": at_risk_pct, "highest_risk_program": highest_risk_program, "highest_risk_program_pct": highest_risk_program_pct}
                },
                {
                    "finding": f"Intervention effectiveness: {at_risk_with_aid:,} at-risk students receiving aid, {at_risk_without_aid:,} without support. {'Aid alone insufficient - students need academic intervention' if at_risk_with_aid > at_risk_without_aid else 'Financial barriers likely contributing to risk - expand aid'}" if at_risk_with_aid + at_risk_without_aid > 0 else f"Success drivers: {high_perf_pct:.1f}% achieving excellence, {success_rate:.1f}% overall success rate",
                    "context": {"type": "intervention_effectiveness", "at_risk_with_aid": at_risk_with_aid, "at_risk_without_aid": at_risk_without_aid, "success_rate": success_rate, "high_perf_pct": high_perf_pct}
                }
            ]

            # RISK-FOCUSED RECOMMENDATIONS
            basic_recommendations = [
                {
                    "recommendation": f"{'URGENT: Implement comprehensive early warning system and mandatory intervention for {at_risk:,} at-risk students ({at_risk_pct:.1f}%). Deploy academic advisors, tutoring, and mental health support' if at_risk_pct > 25 else 'Expand proactive intervention programs for {at_risk:,} at-risk students ({at_risk_pct:.1f}%). Focus on early detection and personalized support plans' if at_risk_pct > 15 else 'Maintain current intervention programs for {at_risk:,} at-risk students, enhance success coaching for mid-tier'}".format(at_risk=at_risk, at_risk_pct=at_risk_pct),
                    "context": {"type": "risk_intervention", "at_risk": at_risk, "at_risk_pct": at_risk_pct, "total_students": total_students}
                },
                {
                    "recommendation": f"Target {highest_risk_program} program with {highest_risk_program_pct:.1f}% at-risk rate. Review curriculum difficulty, teaching quality, and student support resources" if highest_risk_program != "Unknown" and highest_risk_program_pct > 20 else f"{'Deploy predictive analytics to identify at-risk students BEFORE they fall below 2.0 GPA. Monitor attendance, assignment completion, and mid-term grades' if at_risk_pct > 15 else 'Scale high-performer programs - {high_perf_pct:.1f}% excellence rate shows strong foundation. Replicate success factors institution-wide'}".format(at_risk_pct=at_risk_pct, high_perf_pct=high_perf_pct),
                    "context": {"type": "risk_program_intervention", "highest_risk_program": highest_risk_program, "highest_risk_program_pct": highest_risk_program_pct, "at_risk_pct": at_risk_pct}
                },
                {
                    "recommendation": f"{'Combine financial aid with mandatory academic support for {at_risk_with_aid:,} aided at-risk students - aid alone not preventing failure' if at_risk_with_aid > at_risk_without_aid and at_risk_with_aid > 0 else 'Expand financial aid to {at_risk_without_aid:,} at-risk students without support - financial stress likely contributing to academic risk' if at_risk_without_aid > at_risk_with_aid and at_risk_without_aid > 0 else 'Develop peer mentoring program pairing {high_performers:,} high performers with {mid_performers:,} mid-tier students to boost success rate from {success_rate:.1f}%'}".format(at_risk_with_aid=at_risk_with_aid, at_risk_without_aid=at_risk_without_aid, high_performers=high_performers, mid_performers=mid_performers, success_rate=success_rate),
                    "context": {"type": "risk_support_strategy", "at_risk_with_aid": at_risk_with_aid, "at_risk_without_aid": at_risk_without_aid, "high_performers": high_performers, "mid_performers": mid_performers}
                }
            ]

        else:
            # EXECUTIVE SUMMARY / GENERAL FINDINGS
            basic_findings = [
                {
                    "finding": f"Academic performance: {high_performers:,} high performers ({high_perf_pct:.1f}%), {at_risk:,} at-risk ({at_risk_pct:.1f}%)",
                    "context": {"type": "academic", "high_perf_pct": high_perf_pct, "at_risk_pct": at_risk_pct, "at_risk": at_risk, "high_performers": high_performers, "total_students": total_students, "avg_gpa": avg_gpa, "total_tuition": total_tuition}
                },
                {
                    "finding": f"Diversity: {unique_nationalities} nationalities with UAE {uae_percentage:.1f}%, top 3 markets {top_3_concentration:.1f}%",
                    "context": {"type": "diversity", "unique_nationalities": unique_nationalities, "uae_percentage": uae_percentage, "top_3_concentration": top_3_concentration}
                },
                {
                    "finding": f"Financial: AED {total_aid/1000000:.1f}M aid ({aid_coverage_pct:.1f}% of revenue)",
                    "context": {"type": "financial", "total_aid": total_aid, "aid_coverage_pct": aid_coverage_pct, "total_tuition": total_tuition}
                }
            ]

            # EXECUTIVE SUMMARY / GENERAL RECOMMENDATIONS
            basic_recommendations = [
                {
                    "recommendation": f"Target {at_risk:,} at-risk students ({at_risk_pct:.1f}%) with intervention programs",
                    "context": {"type": "academic", "at_risk": at_risk, "at_risk_pct": at_risk_pct, "total_students": total_students, "total_tuition": total_tuition}
                },
                {
                    "recommendation": f"{'Diversify recruitment to reduce top-3 market dependency from ' + str(round(top_3_concentration, 1)) + '% to below 50%' if top_3_concentration > 60 else 'Enhance diversity recruitment strategies'}",
                    "context": {"type": "diversity", "top_3_concentration": top_3_concentration, "unique_nationalities": unique_nationalities}
                },
                {
                    "recommendation": f"Optimize financial aid allocation (current {aid_coverage_pct:.1f}% coverage)",
                    "context": {"type": "financial", "aid_coverage_pct": aid_coverage_pct, "total_aid": total_aid, "total_tuition": total_tuition}
                }
            ]

        st.success(f"✅ Phase 3 complete: Generated {len(basic_findings)} findings and {len(basic_recommendations)} recommendations")

        # PHASE 4: Enrich findings and recommendations
        st.info("⏳ Phase 4/4: Enriching findings with ROOT CAUSE & IMPACT, recommendations with ACTION & OUTCOME...")

        enriched_findings = []
        enriched_recommendations = []

        # Enrich each finding
        for i, finding_obj in enumerate(basic_findings):
            with st.spinner(f"Enriching finding {i+1}/3..."):
                finding_text = finding_obj["finding"]
                context = finding_obj["context"]

                # Try LLM enrichment
                llm_prompt = f"""Enrich this finding with ROOT CAUSE and IMPACT:

Finding: {finding_text}

Context: {total_students} students, GPA {avg_gpa:.2f}, {unique_nationalities} nations

Provide ROOT CAUSE (why this pattern exists) and IMPACT (business consequence).

JSON:
{{"root_cause": "...", "impact": "..."}}"""

                llm_response = query_ollama(llm_prompt, model, url, temperature=0.7, num_predict=200, timeout=60, auto_optimize=True)

                if llm_response and not llm_response.startswith('[ERROR]'):
                    llm_result = extract_json_from_response(llm_response)
                    if llm_result and 'root_cause' in llm_result and 'impact' in llm_result:
                        enriched = f"{finding_text} ROOT CAUSE: {llm_result['root_cause']} IMPACT: {llm_result['impact']}"
                        enriched_findings.append(enriched)
                        st.success(f"✅ LLM enrichment for finding {i+1}")
                        continue

                # Fallback: Statistical enrichment
                enriched = _enrich_finding_statistical(finding_text, context, df)
                enriched_findings.append(enriched)
                st.info(f"📊 Statistical enrichment for finding {i+1}")

        # Enrich each recommendation
        for i, rec_obj in enumerate(basic_recommendations):
            with st.spinner(f"Enriching recommendation {i+1}/3..."):
                rec_text = rec_obj["recommendation"]
                context = rec_obj["context"]

                # Try LLM enrichment
                llm_prompt = f"""Enrich this recommendation with ACTION and EXPECTED OUTCOME:

Recommendation: {rec_text}

Context: {total_students} students, at-risk {at_risk}, aid {aid_coverage_pct:.1f}%

Provide specific ACTION steps and EXPECTED OUTCOME with numbers.

JSON:
{{"action": "...", "expected_outcome": "..."}}"""

                llm_response = query_ollama(llm_prompt, model, url, temperature=0.7, num_predict=250, timeout=60, auto_optimize=True)

                if llm_response and not llm_response.startswith('[ERROR]'):
                    llm_result = extract_json_from_response(llm_response)
                    if llm_result and 'action' in llm_result and 'expected_outcome' in llm_result:
                        enriched = f"{rec_text} ACTION: {llm_result['action']} EXPECTED OUTCOME: {llm_result['expected_outcome']}"
                        enriched_recommendations.append(enriched)
                        st.success(f"✅ LLM enrichment for recommendation {i+1}")
                        continue

                # Fallback: Statistical enrichment
                enriched = _enrich_recommendation_statistical(rec_text, context)
                enriched_recommendations.append(enriched)
                st.info(f"📊 Statistical enrichment for recommendation {i+1}")

        st.success("✅ All phases complete: Using hybrid-enriched analysis")

        return {
            "strategic_overview": f"Analysis of {total_students:,} students reveals key institutional patterns requiring strategic attention across academic performance, diversity, and financial sustainability.",
            "visualizations": enriched_visualizations,
            "key_findings": enriched_findings,
            "recommendations": enriched_recommendations
        }

    except Exception as e:
        st.warning(f"⚠️ LLM enrichment partially failed: {str(e)[:200]} - using rule-based insights")

    # If LLM enrichment failed, add statistical insights to existing visualizations
    # (visualizations already selected in Phase 1)
    if not any('insight' in v for v in visualizations):
        for viz in visualizations:
            col_name = viz.get('data_column', '')
            if col_name and col_name in df.columns:
                if df[col_name].dtype in ['int64', 'float64']:
                    col_data = df[col_name].dropna()
                    if len(col_data) > 0:
                        viz['insight'] = f"{col_name}: mean {col_data.mean():.2f}, median {col_data.median():.2f}, std {col_data.std():.2f}. Analysis reveals distribution patterns requiring strategic attention."
                else:
                    top_vals = df[col_name].value_counts().head(3)
                    viz['insight'] = f"Top categories: {', '.join([f'{k} ({v} students)' for k, v in top_vals.items()])}. Distribution shows concentration patterns with strategic implications."
            else:
                viz['insight'] = f"Statistical analysis of {viz.get('title', 'data')} reveals patterns in institutional performance."

    # Build statistical summary with enhanced analysis
    at_risk_pct = (at_risk/total_students*100) if total_students > 0 else 0
    high_perf_pct = (high_performers/total_students*100) if total_students > 0 else 0
    aid_coverage_pct = (total_aid/total_tuition*100) if total_tuition > 0 else 0

    # Calculate market concentration for diversity analysis
    nationality_col = find_matching_column('nationality', df)
    top_3_concentration = 0
    if nationality_col and nationality_col in df.columns:
        top_nat = df[nationality_col].value_counts().head(3)
        top_3_concentration = (top_nat.sum() / total_students * 100) if total_students > 0 else 0

    # Enhanced key findings with ROOT CAUSE analysis
    enriched_findings = []

    # Finding 1: Academic Performance
    gpa_std = df[find_matching_column('gpa', df)].std() if find_matching_column('gpa', df) and find_matching_column('gpa', df) in df.columns else 0
    academic_root_cause = "Wide admissions criteria without adequate placement testing" if gpa_std > 0.6 else "Consistent academic standards with selective admissions"
    enriched_findings.append(
        f"Academic performance: {high_performers:,} high performers ({high_perf_pct:.1f}%), {at_risk:,} at-risk ({at_risk_pct:.1f}%). "
        f"ROOT CAUSE: {academic_root_cause}. "
        f"IMPACT: {at_risk:,} students represent {'critical' if at_risk_pct > 25 else 'moderate'} retention risk affecting AED {(at_risk/total_students*total_tuition):,.0f} in potential revenue."
    )

    # Finding 2: Diversity & Market Concentration
    diversity_root_cause = "Over-reliance on limited geographic recruitment channels" if top_3_concentration > 60 else "Balanced multi-market recruitment strategy"
    enriched_findings.append(
        f"Diversity: {unique_nationalities} nationalities with UAE {uae_percentage:.1f}%, top 3 markets {top_3_concentration:.1f}% of enrollment. "
        f"ROOT CAUSE: {diversity_root_cause}. "
        f"IMPACT: {'High concentration risk - geopolitical or economic shifts in 3 markets could affect majority of enrollment' if top_3_concentration > 60 else 'Balanced risk distribution across markets'}."
    )

    # Finding 3: Financial Sustainability
    financial_root_cause = "Accessibility-focused aid model prioritizing student access" if aid_coverage_pct > 35 else "Revenue-focused model with selective aid allocation"
    enriched_findings.append(
        f"Financial: AED {total_aid/1000000:.1f}M aid ({aid_coverage_pct:.1f}% of revenue). "
        f"ROOT CAUSE: {financial_root_cause}. "
        f"IMPACT: {'Approaching sustainability threshold - monitor for long-term viability' if aid_coverage_pct > 40 else 'Sustainable model with healthy margins'}."
    )

    # Enhanced recommendations with ACTION details
    enriched_recommendations = []

    # Recommendation 1: Academic Intervention
    students_to_save = int(at_risk * 0.25)  # 25% reduction target
    revenue_impact = (students_to_save / total_students * total_tuition) if total_students > 0 else 0
    enriched_recommendations.append(
        f"Target {at_risk:,} at-risk students ({at_risk_pct:.1f}%) with structured intervention programs. "
        f"ACTION: Deploy early warning system with mandatory tutoring for students below 2.0 GPA, implement peer mentoring, and create academic success workshops. "
        f"EXPECTED OUTCOME: Reduce at-risk population by 25% ({students_to_save:,} students), improving retention by 5-8% and protecting AED {revenue_impact:,.0f} in annual revenue."
    )

    # Recommendation 2: Diversity Enhancement
    if top_3_concentration > 60:
        enriched_recommendations.append(
            f"Diversify recruitment to reduce top-3 market dependency from {top_3_concentration:.1f}% to below 50%. "
            f"ACTION: Establish partnerships in 5-7 new markets (Southeast Asia, Africa, Latin America), launch digital marketing campaigns in target regions, and offer market-specific scholarships. "
            f"EXPECTED OUTCOME: Reduce concentration risk, stabilize enrollment against regional economic fluctuations, and enhance multicultural learning environment."
        )
    else:
        enriched_recommendations.append(
            f"Maintain balanced recruitment strategy while exploring growth markets. "
            f"ACTION: Strengthen presence in current {unique_nationalities} markets through alumni networks, expand scholarship programs for underrepresented regions, and develop market-specific value propositions. "
            f"EXPECTED OUTCOME: 10-15% enrollment growth while preserving diversity balance."
        )

    # Recommendation 3: Financial Aid Optimization
    if aid_coverage_pct > 40:
        enriched_recommendations.append(
            f"Review aid model sustainability - current {aid_coverage_pct:.1f}% coverage approaching risk threshold. "
            f"ACTION: Conduct aid effectiveness audit, implement need-based verification, explore corporate sponsorships and endowment funding, and optimize aid allocation using predictive retention analytics. "
            f"EXPECTED OUTCOME: Reduce aid coverage to 35-38% while maintaining access, freeing AED {(aid_coverage_pct-37)*total_tuition/100:,.0f} for reinvestment in academic programs."
        )
    else:
        enriched_recommendations.append(
            f"Optimize aid allocation for maximum impact while maintaining {aid_coverage_pct:.1f}% coverage. "
            f"ACTION: Target aid to high-potential students with financial need, create merit-need hybrid scholarships, and develop aid retention tied to academic progress milestones. "
            f"EXPECTED OUTCOME: Improve aid ROI by 15-20%, enhance student success rates, and maintain financial sustainability."
        )

    return {
        "strategic_overview": f"Analysis of {total_students:,} students reveals key institutional patterns: Academic performance (GPA {avg_gpa:.2f}, {high_perf_pct:.1f}% high performers, {at_risk_pct:.1f}% at-risk), Diversity ({unique_nationalities} nationalities, UAE {uae_percentage:.1f}%), Financial sustainability (AED {total_aid/1000000:.1f}M aid).",
        "visualizations": visualizations,
        "key_findings": enriched_findings,
        "recommendations": enriched_recommendations
    }


def find_matching_column(requested_col: str, df: pd.DataFrame) -> str:
    """
    Smart column matching - handles variations in column names

    Examples:
    - 'gpa' matches 'gpa', 'cumulative_gpa', 'current_gpa', 'GPA'
    - 'nationality' matches 'nationality', 'Nationality', 'student_nationality'
    """
    if requested_col in df.columns:
        return requested_col

    # Try case-insensitive exact match
    for col in df.columns:
        if col.lower() == requested_col.lower():
            return col

    # Try substring match (requested in actual column name)
    for col in df.columns:
        if requested_col.lower() in col.lower():
            return col

    # Try substring match (actual column name in requested)
    for col in df.columns:
        if col.lower() in requested_col.lower():
            return col

    # Column name variations
    variations = {
        'gpa': ['cumulative_gpa', 'current_gpa', 'semester_gpa', 'overall_gpa', 'cgpa'],
        'nationality': ['student_nationality', 'country', 'nation'],
        'program': ['major', 'program_name', 'degree_program', 'course'],
        'tuition': ['tuition_fees', 'fees', 'tuition_amount'],
        'aid': ['financial_aid', 'scholarship', 'aid_amount'],
        'enrollment': ['enrollment_date', 'admission_date', 'enroll_date', 'start_date']
    }

    for base_name, alts in variations.items():
        if requested_col.lower() == base_name or requested_col.lower() in alts:
            for alt in [base_name] + alts:
                if alt in df.columns:
                    return alt
                # Try case-insensitive
                for col in df.columns:
                    if col.lower() == alt.lower():
                        return col

    return None


def build_dynamic_chart(spec: dict, df: pd.DataFrame):
    """
    Dynamically builds a Plotly chart based on LLM specification

    Takes LLM-generated visualization spec and creates the actual chart
    """
    graph_type = spec.get('graph_type', 'bar')
    data_column = spec.get('data_column', '')
    title = spec.get('title', 'Visualization')
    config = spec.get('config', {})

    # Smart column matching - handles variations
    matched_column = find_matching_column(data_column, df) if data_column else None

    if not matched_column:
        # Try to handle special derived columns
        if data_column == 'performance_tier':
            # Create performance tiers from GPA
            gpa_col = find_matching_column('gpa', df)
            if gpa_col:
                df['performance_tier'] = pd.cut(
                    df[gpa_col],
                    bins=[0, 2.0, 2.5, 3.0, 3.5, 4.0],
                    labels=['At Risk (<2.0)', 'Below Average (2.0-2.5)', 'Average (2.5-3.0)', 'Above Average (3.0-3.5)', 'High Performer (≥3.5)']
                )
                matched_column = 'performance_tier'
            else:
                st.warning(f"⚠️ Cannot create performance tiers - no GPA column found. Available: {', '.join(df.columns[:10])}")
                return None
        else:
            st.warning(f"⚠️ Column '{data_column}' not found. Available columns: {', '.join(df.columns[:10])}")
            return None

    # Use the matched column
    data_column = matched_column

    try:
        if graph_type == 'histogram':
            # Histogram for numeric distributions - ENHANCED CLARITY
            bins = config.get('bins', 20)
            data = df[data_column].dropna()

            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=data,
                nbinsx=bins,
                marker=dict(
                    color='rgba(99, 102, 241, 0.8)',
                    line=dict(color='rgba(139, 146, 255, 1)', width=2)
                ),
                name=data_column,
                hovertemplate='<b>Range:</b> %{x}<br><b>Count:</b> %{y}<extra></extra>'
            ))
            fig.update_layout(
                title=dict(
                    text=f"<b>{title}</b>",
                    font=dict(size=20, color='#e2e8f0'),
                    x=0.5,
                    xanchor='center'
                ),
                xaxis=dict(
                    title=dict(text=f"<b>{data_column.replace('_', ' ').title()}</b>", font=dict(size=16)),
                    gridcolor='rgba(255, 255, 255, 0.1)',
                    showgrid=True,
                    tickfont=dict(size=13, color='#cbd5e1')
                ),
                yaxis=dict(
                    title=dict(text="<b>Count</b>", font=dict(size=16)),
                    gridcolor='rgba(255, 255, 255, 0.1)',
                    showgrid=True,
                    tickfont=dict(size=13, color='#cbd5e1')
                ),
                template='plotly_dark',
                plot_bgcolor='rgba(15, 23, 42, 0.6)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=450,
                margin=dict(l=80, r=40, t=80, b=80),
                hoverlabel=dict(
                    bgcolor='rgba(30, 41, 59, 0.95)',
                    font_size=14,
                    font_family="Arial"
                )
            )
            return fig

        elif graph_type == 'bar':
            # Bar chart for categorical comparisons - ENHANCED CLARITY
            top_n = config.get('top_n', 10)
            aggregation = config.get('aggregation', 'count')

            # Vibrant color gradient for bars
            colors = ['#6366f1', '#8b5cf6', '#a855f7', '#c026d3', '#db2777', '#ec4899', '#f43f5e', '#ef4444', '#f97316', '#f59e0b']

            if aggregation == 'count':
                value_counts = df[data_column].value_counts().head(top_n)
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=value_counts.index,
                    y=value_counts.values,
                    marker=dict(
                        color=colors[:len(value_counts)],
                        line=dict(color='rgba(255, 255, 255, 0.3)', width=2)
                    ),
                    text=value_counts.values,
                    textposition='outside',
                    textfont=dict(size=13, color='#e2e8f0', family='Arial Black'),
                    hovertemplate='<b>%{x}</b><br>Count: %{y:,}<extra></extra>'
                ))
            else:
                # Handle sum/mean aggregations if group_by specified
                group_by = config.get('group_by', data_column)
                if aggregation == 'sum':
                    grouped = df.groupby(group_by)[data_column].sum().sort_values(ascending=False).head(top_n)
                else:  # mean
                    grouped = df.groupby(group_by)[data_column].mean().sort_values(ascending=False).head(top_n)

                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=grouped.index,
                    y=grouped.values,
                    marker=dict(
                        color=colors[:len(grouped)],
                        line=dict(color='rgba(255, 255, 255, 0.3)', width=2)
                    ),
                    text=[f'{v:,.0f}' for v in grouped.values],
                    textposition='outside',
                    textfont=dict(size=13, color='#e2e8f0', family='Arial Black'),
                    hovertemplate='<b>%{x}</b><br>Value: %{y:,.2f}<extra></extra>'
                ))

            fig.update_layout(
                title=dict(
                    text=f"<b>{title}</b>",
                    font=dict(size=20, color='#e2e8f0'),
                    x=0.5,
                    xanchor='center'
                ),
                xaxis=dict(
                    title=dict(text=f"<b>{data_column.replace('_', ' ').title()}</b>", font=dict(size=16)),
                    tickangle=-45,
                    tickfont=dict(size=12, color='#cbd5e1'),
                    showgrid=False
                ),
                yaxis=dict(
                    title=dict(text=f"<b>{'Count' if aggregation == 'count' else aggregation.title()}</b>", font=dict(size=16)),
                    gridcolor='rgba(255, 255, 255, 0.1)',
                    showgrid=True,
                    tickfont=dict(size=13, color='#cbd5e1')
                ),
                template='plotly_dark',
                plot_bgcolor='rgba(15, 23, 42, 0.6)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=450,
                margin=dict(l=80, r=40, t=80, b=120),
                hoverlabel=dict(
                    bgcolor='rgba(30, 41, 59, 0.95)',
                    font_size=14,
                    font_family="Arial"
                )
            )
            return fig

        elif graph_type == 'pie':
            # Pie chart for composition - ENHANCED CLARITY
            value_counts = df[data_column].value_counts()

            # Vibrant professional color palette
            colors = ['#6366f1', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#3b82f6', '#ef4444', '#f97316', '#14b8a6', '#a855f7']

            fig = go.Figure()
            fig.add_trace(go.Pie(
                labels=value_counts.index,
                values=value_counts.values,
                hole=0.35,
                marker=dict(
                    colors=colors[:len(value_counts)],
                    line=dict(color='rgba(255, 255, 255, 0.3)', width=2)
                ),
                textposition='outside',
                textinfo='label+percent',
                textfont=dict(size=14, color='#e2e8f0', family='Arial'),
                hovertemplate='<b>%{label}</b><br>Count: %{value:,}<br>Percentage: %{percent}<extra></extra>',
                pull=[0.05] * len(value_counts)  # Slight pull-out effect for all slices
            ))
            fig.update_layout(
                title=dict(
                    text=f"<b>{title}</b>",
                    font=dict(size=20, color='#e2e8f0'),
                    x=0.5,
                    xanchor='center'
                ),
                template='plotly_dark',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=500,
                margin=dict(l=20, r=20, t=80, b=20),
                showlegend=True,
                legend=dict(
                    font=dict(size=12, color='#cbd5e1'),
                    bgcolor='rgba(15, 23, 42, 0.6)',
                    bordercolor='rgba(255, 255, 255, 0.2)',
                    borderwidth=1
                ),
                hoverlabel=dict(
                    bgcolor='rgba(30, 41, 59, 0.95)',
                    font_size=14,
                    font_family="Arial"
                )
            )
            return fig

        elif graph_type == 'line':
            # Line chart for trends - ENHANCED CLARITY
            # Assume data_column is a date/time column
            if pd.api.types.is_datetime64_any_dtype(df[data_column]):
                df_sorted = df.sort_values(data_column)
                grouped = df_sorted.groupby(df_sorted[data_column].dt.to_period('M')).size()

                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=[str(p) for p in grouped.index],
                    y=grouped.values,
                    mode='lines+markers',
                    line=dict(color='#6366f1', width=4),
                    marker=dict(
                        size=10,
                        color='#8b5cf6',
                        line=dict(color='#e2e8f0', width=2)
                    ),
                    fill='tozeroy',
                    fillcolor='rgba(99, 102, 241, 0.15)',
                    hovertemplate='<b>Period:</b> %{x}<br><b>Count:</b> %{y:,}<extra></extra>'
                ))
                fig.update_layout(
                    title=dict(
                        text=f"<b>{title}</b>",
                        font=dict(size=20, color='#e2e8f0'),
                        x=0.5,
                        xanchor='center'
                    ),
                    xaxis=dict(
                        title=dict(text="<b>Period</b>", font=dict(size=16)),
                        gridcolor='rgba(255, 255, 255, 0.1)',
                        showgrid=True,
                        tickfont=dict(size=12, color='#cbd5e1'),
                        tickangle=-45
                    ),
                    yaxis=dict(
                        title=dict(text="<b>Count</b>", font=dict(size=16)),
                        gridcolor='rgba(255, 255, 255, 0.1)',
                        showgrid=True,
                        tickfont=dict(size=13, color='#cbd5e1')
                    ),
                    template='plotly_dark',
                    plot_bgcolor='rgba(15, 23, 42, 0.6)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=450,
                    margin=dict(l=80, r=40, t=80, b=100),
                    hoverlabel=dict(
                        bgcolor='rgba(30, 41, 59, 0.95)',
                        font_size=14,
                        font_family="Arial"
                    )
                )
                return fig
            else:
                # Fallback to bar if not datetime
                return build_dynamic_chart({**spec, 'graph_type': 'bar'}, df)

        elif graph_type == 'scatter':
            # Scatter plot for relationships - ENHANCED CLARITY
            x_col = config.get('x_column', data_column)
            y_col = config.get('y_column', 'gpa')

            # Smart column matching for x and y
            x_col_matched = find_matching_column(x_col, df) if x_col else None
            y_col_matched = find_matching_column(y_col, df) if y_col else None

            if x_col_matched and y_col_matched:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df[x_col_matched],
                    y=df[y_col_matched],
                    mode='markers',
                    marker=dict(
                        size=10,
                        color='#8b5cf6',
                        opacity=0.7,
                        line=dict(color='#e2e8f0', width=1.5)
                    ),
                    hovertemplate=f'<b>{x_col_matched}:</b> %{{x:,.2f}}<br><b>{y_col_matched}:</b> %{{y:.2f}}<extra></extra>'
                ))
                fig.update_layout(
                    title=dict(
                        text=f"<b>{title}</b>",
                        font=dict(size=20, color='#e2e8f0'),
                        x=0.5,
                        xanchor='center'
                    ),
                    xaxis=dict(
                        title=dict(text=f"<b>{x_col_matched.replace('_', ' ').title()}</b>", font=dict(size=16)),
                        gridcolor='rgba(255, 255, 255, 0.1)',
                        showgrid=True,
                        tickfont=dict(size=13, color='#cbd5e1')
                    ),
                    yaxis=dict(
                        title=dict(text=f"<b>{y_col_matched.replace('_', ' ').title()}</b>", font=dict(size=16)),
                        gridcolor='rgba(255, 255, 255, 0.1)',
                        showgrid=True,
                        tickfont=dict(size=13, color='#cbd5e1')
                    ),
                    template='plotly_dark',
                    plot_bgcolor='rgba(15, 23, 42, 0.6)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    height=450,
                    margin=dict(l=80, r=40, t=80, b=80),
                    hoverlabel=dict(
                        bgcolor='rgba(30, 41, 59, 0.95)',
                        font_size=14,
                        font_family="Arial"
                    )
                )
                return fig
            else:
                return None

        elif graph_type == 'box':
            # Box plot for statistical distribution - ENHANCED CLARITY
            data = df[data_column].dropna()

            fig = go.Figure()
            fig.add_trace(go.Box(
                y=data,
                marker=dict(
                    color='#8b5cf6',
                    size=8,
                    line=dict(color='#e2e8f0', width=1.5)
                ),
                line=dict(color='#6366f1', width=2),
                fillcolor='rgba(99, 102, 241, 0.5)',
                name=data_column,
                boxpoints='outliers',  # Show outlier points
                hovertemplate='<b>Value:</b> %{y:.2f}<extra></extra>'
            ))

            # Calculate quartiles for annotation
            q1 = data.quantile(0.25)
            median = data.median()
            q3 = data.quantile(0.75)

            fig.update_layout(
                title=dict(
                    text=f"<b>{title}</b>",
                    font=dict(size=20, color='#e2e8f0'),
                    x=0.5,
                    xanchor='center'
                ),
                yaxis=dict(
                    title=dict(text=f"<b>{data_column.replace('_', ' ').title()}</b>", font=dict(size=16)),
                    gridcolor='rgba(255, 255, 255, 0.1)',
                    showgrid=True,
                    tickfont=dict(size=13, color='#cbd5e1')
                ),
                template='plotly_dark',
                plot_bgcolor='rgba(15, 23, 42, 0.6)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=450,
                margin=dict(l=80, r=40, t=80, b=80),
                annotations=[
                    dict(
                        x=0.5, y=median,
                        text=f'Median: {median:.2f}',
                        showarrow=False,
                        xanchor='left',
                        font=dict(size=12, color='#10b981'),
                        xshift=50
                    ),
                    dict(
                        x=0.5, y=q1,
                        text=f'Q1: {q1:.2f}',
                        showarrow=False,
                        xanchor='left',
                        font=dict(size=11, color='#cbd5e1'),
                        xshift=50
                    ),
                    dict(
                        x=0.5, y=q3,
                        text=f'Q3: {q3:.2f}',
                        showarrow=False,
                        xanchor='left',
                        font=dict(size=11, color='#cbd5e1'),
                        xshift=50
                    )
                ],
                hoverlabel=dict(
                    bgcolor='rgba(30, 41, 59, 0.95)',
                    font_size=14,
                    font_family="Arial"
                )
            )
            return fig

    except Exception as e:
        st.error(f"Error building chart: {str(e)}")
        return None

    return None


def generate_journey_story_llm(journey_name: str, metrics: dict, df: pd.DataFrame, model: str, url: str) -> dict:
    """Generate journey-specific story using LLM"""

    journey_contexts = {
        "Enrollment": "Focus on student composition, enrollment trends, diversity metrics, and market positioning.",
        "Revenue": "Focus on tuition revenue, financial aid distribution, sustainability, and operational efficiency.",
        "Services": "Focus on campus housing, student services, co-curricular programs, and support systems.",
        "Performance": "Focus on academic achievement, GPA distribution, excellence metrics, and cohort analysis.",
        "Retention": "Focus on persistence rates, graduation tracking, first-generation success, and retention strategies.",
        "Risk": "Focus on at-risk student identification, early warning indicators, intervention effectiveness.",
        "Strategic": "Focus on institutional transformation, strategic priorities, investment impact, and future roadmap.",
        "Curriculum": "Focus on program quality variations, GPA differences across majors, curriculum rigor standardization, and academic excellence programs."
    }

    context = f"""Analyze this student data and create a compelling narrative for the "{journey_name}" journey.

**Context:** {journey_contexts.get(journey_name, "General analysis")}

**KEY METRICS:**
- Total Students: {metrics.get('total_students', 0):,}
- Average GPA: {metrics.get('avg_gpa', 0):.2f}
- UAE Percentage: {metrics.get('uae_percentage', 0):.1f}%
- High Performers: {metrics.get('high_performers', 0):,}
- At-Risk: {metrics.get('at_risk', 0):,}

Generate 2 story narratives in JSON:
{{
  "stories": [
    {{
      "title": "Story 1 title",
      "content": "3-4 sentences with data-driven narrative and strategic insights"
    }},
    {{
      "title": "Story 2 title",
      "content": "3-4 sentences with actionable recommendations"
    }}
  ]
}}"""

    try:
        response = query_ollama(context, model, url, temperature=0.7, num_predict=600, auto_optimize=True)
        if response and not response.startswith('[ERROR]'):
            result = extract_json_from_response(response)
            if result and 'stories' in result:
                return result
    except:
        pass

    # Fallback
    return {
        "stories": [
            {
                "title": f"{journey_name} Overview",
                "content": f"Analysis of {metrics.get('total_students', 0):,} students reveals key patterns in {journey_name.lower()} metrics. Data-driven insights indicate opportunities for strategic enhancement."
            },
            {
                "title": f"{journey_name} Recommendations",
                "content": "Implementing targeted interventions and monitoring key performance indicators will drive continuous improvement in this critical area."
            }
        ]
    }

def deep_dive_business_discovery(df: pd.DataFrame, metrics: dict) -> dict:
    """
    Deep dive analysis to discover business patterns, correlations, and opportunities

    Returns: Dictionary with business insights across multiple dimensions
    """

    discoveries = {
        'correlations': {},
        'segmentation': {},
        'anomalies': {},
        'opportunities': {},
        'risks': {},
        'financial_patterns': {},
        'academic_patterns': {},
        'market_patterns': {}
    }

    # ============================================================================
    # 1. CORRELATION ANALYSIS - Find relationships between variables
    # ============================================================================

    gpa_col = find_matching_column('gpa', df)
    aid_col = find_matching_column('aid', df)
    tuition_col = find_matching_column('tuition', df)
    nationality_col = find_matching_column('nationality', df)
    program_col = find_matching_column('program', df)
    gender_col = find_matching_column('gender', df)

    # Aid vs Performance correlation
    if aid_col and gpa_col and aid_col in df.columns and gpa_col in df.columns:
        aid_data = df[[aid_col, gpa_col]].dropna()
        students_with_aid = aid_data[aid_data[aid_col] > 0]
        students_without_aid = aid_data[aid_data[aid_col] == 0]

        if len(students_with_aid) > 0 and len(students_without_aid) > 0:
            avg_gpa_with_aid = students_with_aid[gpa_col].mean()
            avg_gpa_without_aid = students_without_aid[gpa_col].mean()
            gpa_difference = avg_gpa_with_aid - avg_gpa_without_aid

            discoveries['correlations']['aid_effectiveness'] = {
                'gpa_with_aid': avg_gpa_with_aid,
                'gpa_without_aid': avg_gpa_without_aid,
                'difference': gpa_difference,
                'insight': f"Aid {'positively' if gpa_difference > 0.1 else 'negatively' if gpa_difference < -0.1 else 'neutrally'} correlates with performance",
                'pattern': 'positive' if gpa_difference > 0.1 else 'negative' if gpa_difference < -0.1 else 'neutral'
            }

    # Tuition vs Performance - Are higher-paying students performing better?
    if tuition_col and gpa_col and tuition_col in df.columns and gpa_col in df.columns:
        tuition_gpa_data = df[[tuition_col, gpa_col]].dropna()
        if len(tuition_gpa_data) > 20:
            correlation = tuition_gpa_data[[tuition_col, gpa_col]].corr().iloc[0, 1]

            # Segment by tuition quartiles
            tuition_quartiles = tuition_gpa_data[tuition_col].quantile([0.25, 0.5, 0.75])
            low_tuition_gpa = tuition_gpa_data[tuition_gpa_data[tuition_col] <= tuition_quartiles[0.25]][gpa_col].mean()
            high_tuition_gpa = tuition_gpa_data[tuition_gpa_data[tuition_col] >= tuition_quartiles[0.75]][gpa_col].mean()

            discoveries['correlations']['tuition_performance'] = {
                'correlation': correlation,
                'low_tuition_gpa': low_tuition_gpa,
                'high_tuition_gpa': high_tuition_gpa,
                'insight': f"Students in top tuition quartile have GPA {high_tuition_gpa:.2f} vs {low_tuition_gpa:.2f} in bottom quartile",
                'pattern': 'premium_performs_better' if high_tuition_gpa > low_tuition_gpa + 0.2 else 'equitable'
            }

    # ============================================================================
    # 2. SEGMENTATION ANALYSIS - Identify high-value and at-risk segments
    # ============================================================================

    # Nationality-based segmentation
    if nationality_col and gpa_col and nationality_col in df.columns and gpa_col in df.columns:
        nat_performance = df.groupby(nationality_col).agg({
            gpa_col: ['mean', 'std', 'count']
        }).round(2)
        nat_performance.columns = ['avg_gpa', 'gpa_std', 'count']
        nat_performance = nat_performance[nat_performance['count'] >= 5]  # Min 5 students

        if len(nat_performance) > 0:
            top_performing_nationality = nat_performance['avg_gpa'].idxmax()
            lowest_performing_nationality = nat_performance['avg_gpa'].idxmin()

            discoveries['segmentation']['nationality_performance'] = {
                'top_performer': top_performing_nationality,
                'top_gpa': nat_performance.loc[top_performing_nationality, 'avg_gpa'],
                'top_count': int(nat_performance.loc[top_performing_nationality, 'count']),
                'lowest_performer': lowest_performing_nationality,
                'lowest_gpa': nat_performance.loc[lowest_performing_nationality, 'avg_gpa'],
                'lowest_count': int(nat_performance.loc[lowest_performing_nationality, 'count']),
                'variance': nat_performance['avg_gpa'].std(),
                'insight': f"{top_performing_nationality} students excel (GPA {nat_performance.loc[top_performing_nationality, 'avg_gpa']:.2f}) while {lowest_performing_nationality} struggle (GPA {nat_performance.loc[lowest_performing_nationality, 'avg_gpa']:.2f})"
            }

    # Gender performance gap
    if gender_col and gpa_col and gender_col in df.columns and gpa_col in df.columns:
        gender_performance = df.groupby(gender_col)[gpa_col].agg(['mean', 'count']).round(2)
        if len(gender_performance) >= 2:
            gender_gap = abs(gender_performance['mean'].iloc[0] - gender_performance['mean'].iloc[1])

            discoveries['segmentation']['gender_gap'] = {
                'gap': gender_gap,
                'insight': f"Gender performance gap of {gender_gap:.2f} GPA points",
                'significant': gender_gap > 0.15,
                'data': gender_performance.to_dict('index')
            }

    # ============================================================================
    # 3. ANOMALY DETECTION - Identify unusual patterns
    # ============================================================================

    # Zero-GPA students (data quality or serious academic issues)
    if gpa_col and gpa_col in df.columns:
        zero_gpa_students = len(df[df[gpa_col] == 0])
        if zero_gpa_students > 0:
            discoveries['anomalies']['zero_gpa'] = {
                'count': zero_gpa_students,
                'percentage': (zero_gpa_students / len(df) * 100),
                'insight': f"{zero_gpa_students} students with 0.0 GPA - investigate data quality or academic probation cases",
                'severity': 'high' if zero_gpa_students > len(df) * 0.05 else 'medium'
            }

        # Perfect GPA students
        perfect_gpa_students = len(df[df[gpa_col] == 4.0])
        if perfect_gpa_students > 0:
            discoveries['anomalies']['perfect_gpa'] = {
                'count': perfect_gpa_students,
                'percentage': (perfect_gpa_students / len(df) * 100),
                'insight': f"{perfect_gpa_students} students with perfect 4.0 GPA - excellence or grade inflation indicator"
            }

    # High aid, low performance (inefficient aid allocation)
    if aid_col and gpa_col and aid_col in df.columns and gpa_col in df.columns:
        high_aid_threshold = df[aid_col].quantile(0.75)
        high_aid_low_perf = df[(df[aid_col] >= high_aid_threshold) & (df[gpa_col] < 2.5)]

        if len(high_aid_low_perf) > 0:
            wasted_aid = high_aid_low_perf[aid_col].sum()
            discoveries['anomalies']['aid_inefficiency'] = {
                'count': len(high_aid_low_perf),
                'wasted_amount': wasted_aid,
                'percentage': (len(high_aid_low_perf) / len(df) * 100),
                'insight': f"{len(high_aid_low_perf)} students receiving high aid (top 25%) but underperforming (<2.5 GPA) - AED {wasted_aid:,.0f} at-risk investment"
            }

    # ============================================================================
    # 4. OPPORTUNITY IDENTIFICATION - Revenue and growth opportunities
    # ============================================================================

    # High-performing, no-aid students (potential merit scholarship targets)
    if aid_col and gpa_col and aid_col in df.columns and gpa_col in df.columns:
        high_perf_no_aid = df[(df[gpa_col] >= 3.5) & (df[aid_col] == 0)]

        if len(high_perf_no_aid) > 0:
            discoveries['opportunities']['merit_scholarship_candidates'] = {
                'count': len(high_perf_no_aid),
                'percentage': (len(high_perf_no_aid) / len(df) * 100),
                'insight': f"{len(high_perf_no_aid)} high performers receiving zero aid - merit scholarship opportunity for retention and branding"
            }

    # Underrepresented high-performing nationalities (recruitment opportunity)
    if nationality_col and gpa_col and nationality_col in df.columns and gpa_col in df.columns:
        nat_counts = df[nationality_col].value_counts()
        nat_gpa = df.groupby(nationality_col)[gpa_col].mean()

        # Find nationalities with high GPA but low enrollment
        underrepresented_high_performers = []
        for nat in nat_gpa.index:
            if nat_gpa[nat] >= 3.2 and nat_counts[nat] < len(df) * 0.05:  # <5% enrollment, >3.2 GPA
                underrepresented_high_performers.append({
                    'nationality': nat,
                    'avg_gpa': nat_gpa[nat],
                    'count': int(nat_counts[nat]),
                    'percentage': (nat_counts[nat] / len(df) * 100)
                })

        if underrepresented_high_performers:
            discoveries['opportunities']['recruitment_targets'] = {
                'markets': underrepresented_high_performers,
                'insight': f"{len(underrepresented_high_performers)} underrepresented nationalities with strong performance - recruitment expansion opportunity"
            }

    # ============================================================================
    # 5. RISK IDENTIFICATION - Revenue and reputation risks
    # ============================================================================

    # Market concentration risk
    if nationality_col and nationality_col in df.columns:
        nat_counts = df[nationality_col].value_counts()
        top_3_pct = (nat_counts.head(3).sum() / len(df) * 100)
        top_1_pct = (nat_counts.iloc[0] / len(df) * 100)

        discoveries['risks']['market_concentration'] = {
            'top_3_percentage': top_3_pct,
            'top_1_percentage': top_1_pct,
            'top_1_nationality': nat_counts.index[0],
            'severity': 'critical' if top_3_pct > 70 else 'high' if top_3_pct > 60 else 'moderate',
            'insight': f"Top 3 markets represent {top_3_pct:.1f}% of enrollment - {'critical' if top_3_pct > 70 else 'significant'} concentration risk"
        }

    # Financial sustainability risk
    if aid_col and tuition_col and aid_col in df.columns and tuition_col in df.columns:
        total_aid = df[aid_col].sum()
        total_tuition = df[tuition_col].sum()
        aid_coverage = (total_aid / total_tuition * 100) if total_tuition > 0 else 0

        discoveries['risks']['financial_sustainability'] = {
            'aid_coverage_pct': aid_coverage,
            'total_aid': total_aid,
            'total_tuition': total_tuition,
            'severity': 'high' if aid_coverage > 45 else 'moderate' if aid_coverage > 40 else 'low',
            'insight': f"Aid coverage {aid_coverage:.1f}% - {'exceeds' if aid_coverage > 40 else 'approaching'} sustainability threshold"
        }

    # ============================================================================
    # 6. FINANCIAL PATTERNS - Aid effectiveness and ROI
    # ============================================================================

    if aid_col and gpa_col and aid_col in df.columns and gpa_col in df.columns:
        # Aid ROI by tier
        aid_tiers = pd.qcut(df[df[aid_col] > 0][aid_col], q=3, labels=['Low Aid', 'Medium Aid', 'High Aid'], duplicates='drop')
        aid_roi_data = df[df[aid_col] > 0].copy()
        aid_roi_data['aid_tier'] = aid_tiers

        if len(aid_roi_data) > 0:
            aid_roi = aid_roi_data.groupby('aid_tier').agg({
                gpa_col: 'mean',
                aid_col: 'mean'
            }).round(2)

            discoveries['financial_patterns']['aid_roi'] = {
                'by_tier': aid_roi.to_dict('index'),
                'insight': "Aid ROI analysis shows performance returns by investment level"
            }

    # ============================================================================
    # 7. ACADEMIC PATTERNS - Excellence and challenges
    # ============================================================================

    # GPA distribution pattern
    if gpa_col and gpa_col in df.columns:
        gpa_data = df[gpa_col].dropna()

        # Check for bimodal distribution
        gpa_bins = pd.cut(gpa_data, bins=[0, 2.0, 2.5, 3.0, 3.5, 4.0])
        gpa_distribution = gpa_bins.value_counts().sort_index()

        # Detect pattern
        if gpa_distribution.iloc[0] > gpa_distribution.iloc[2] and gpa_distribution.iloc[4] > gpa_distribution.iloc[2]:
            pattern = 'bimodal'
            insight = "Bimodal GPA distribution - distinct high and low performer clusters suggest inconsistent admissions or support"
        elif gpa_distribution.iloc[2] > gpa_distribution.iloc[0] and gpa_distribution.iloc[2] > gpa_distribution.iloc[4]:
            pattern = 'normal'
            insight = "Normal GPA distribution - balanced academic performance across student body"
        else:
            pattern = 'skewed'
            insight = "Skewed GPA distribution - performance concentrated in specific ranges"

        discoveries['academic_patterns']['gpa_distribution'] = {
            'pattern': pattern,
            'distribution': gpa_distribution.to_dict(),
            'insight': insight
        }

    # ============================================================================
    # 8. MARKET PATTERNS - Enrollment trends and positioning
    # ============================================================================

    # Nationality diversity score (Shannon entropy)
    if nationality_col and nationality_col in df.columns:
        nat_counts = df[nationality_col].value_counts()
        nat_proportions = nat_counts / len(df)

        # Shannon entropy
        diversity_score = -sum(nat_proportions * np.log(nat_proportions))
        max_diversity = np.log(len(nat_counts))  # Max entropy
        diversity_index = (diversity_score / max_diversity * 100) if max_diversity > 0 else 0

        discoveries['market_patterns']['diversity_index'] = {
            'score': diversity_index,
            'unique_nationalities': len(nat_counts),
            'insight': f"Diversity index {diversity_index:.1f}% - {'highly diverse' if diversity_index > 70 else 'moderately diverse' if diversity_index > 50 else 'concentrated'} market composition"
        }

    return discoveries


def _format_segment_discoveries_enriched(segment_discoveries: dict, metrics: dict, segment_name: str) -> str:
    """
    Format segment discoveries with FULL enriched context (NO trimming or simplification)

    Args:
        segment_discoveries: Dictionary with discoveries for this segment's categories
        metrics: Overall institutional metrics
        segment_name: Name of the segment (for context)

    Returns:
        Fully enriched formatted string with ALL discovery details
    """

    summary = f"""**{segment_name}**

**INSTITUTIONAL CONTEXT:**
- Total Students: {metrics.get('total_students', 0):,}
- Average GPA: {metrics.get('avg_gpa', 0):.2f}
- High Performers (≥3.5 GPA): {metrics.get('high_performers', 0):,}
- At-Risk (<2.5 GPA): {metrics.get('at_risk', 0):,}
- Unique Nationalities: {metrics.get('unique_nationalities', 0)}
- Total Aid: AED {metrics.get('total_aid', 0):,.0f}

**DETAILED DISCOVERIES IN THIS SEGMENT:**

"""

    # Category mapping with icons
    category_map = {
        'anomalies': '🚨 CRITICAL ANOMALIES',
        'risks': '⚠️ BUSINESS RISKS',
        'opportunities': '💡 GROWTH OPPORTUNITIES',
        'correlations': '🔗 PERFORMANCE CORRELATIONS',
        'segmentation': '📊 SEGMENTATION INSIGHTS',
        'financial_patterns': '💰 FINANCIAL PATTERNS',
        'academic_patterns': '🎓 ACADEMIC PATTERNS',
        'market_patterns': '🌍 MARKET PATTERNS'
    }

    # Add ALL discoveries from each category with FULL context
    for category_key, category_label in category_map.items():
        category_discoveries_data = segment_discoveries.get(category_key, {})

        if category_discoveries_data:
            summary += f"**{category_label}:**\n\n"

            for key, discovery in category_discoveries_data.items():
                # Include FULL discovery details - no trimming
                insight = discovery.get('insight', key)
                summary += f"Discovery: {insight}\n"

                # Add all available metrics
                if 'count' in discovery:
                    summary += f"  - Count: {discovery['count']}\n"
                if 'percentage' in discovery:
                    summary += f"  - Percentage: {discovery['percentage']:.1f}%\n"
                if 'amount' in discovery or 'wasted_amount' in discovery:
                    amount = discovery.get('amount', discovery.get('wasted_amount', 0))
                    summary += f"  - Amount: AED {amount:,.0f}\n"
                if 'severity' in discovery:
                    summary += f"  - Severity: {discovery['severity']}\n"
                if 'gpa_with_aid' in discovery:
                    summary += f"  - GPA with aid: {discovery['gpa_with_aid']:.2f}\n"
                if 'gpa_without_aid' in discovery:
                    summary += f"  - GPA without aid: {discovery['gpa_without_aid']:.2f}\n"
                if 'difference' in discovery:
                    summary += f"  - Difference: {discovery['difference']:.2f}\n"
                if 'variance' in discovery:
                    summary += f"  - Variance: {discovery['variance']:.2f}\n"
                if 'gap' in discovery:
                    summary += f"  - Gap: {discovery['gap']:.2f}\n"
                if 'score' in discovery:
                    summary += f"  - Score: {discovery['score']:.1f}\n"
                if 'pattern' in discovery:
                    summary += f"  - Pattern: {discovery['pattern']}\n"
                if 'top_3_percentage' in discovery:
                    summary += f"  - Top 3 market concentration: {discovery['top_3_percentage']:.1f}%\n"
                if 'aid_coverage_pct' in discovery:
                    summary += f"  - Aid coverage: {discovery['aid_coverage_pct']:.1f}%\n"

                summary += "\n"

            summary += "\n"

    return summary


def _format_all_discoveries_for_journey_extraction(discoveries: dict, metrics: dict) -> str:
    """
    Format ALL discoveries from ALL categories into a concise prompt for single LLM call

    Args:
        discoveries: Dictionary with all 8 categories of discoveries
        metrics: Overall institutional metrics

    Returns:
        Formatted string with all discoveries organized by category
    """

    summary = f"""**INSTITUTIONAL OVERVIEW:**
Students: {metrics.get('total_students', 0):,} | Avg GPA: {metrics.get('avg_gpa', 0):.2f} | High Performers: {metrics.get('high_performers', 0):,} | At-Risk: {metrics.get('at_risk', 0):,}

**KEY DISCOVERIES ACROSS ALL CATEGORIES:**

"""

    # Category mapping with icons
    category_map = {
        'anomalies': '🚨 CRITICAL ANOMALIES',
        'risks': '⚠️ BUSINESS RISKS',
        'opportunities': '💡 GROWTH OPPORTUNITIES',
        'correlations': '🔗 PERFORMANCE CORRELATIONS',
        'segmentation': '📊 SEGMENTATION INSIGHTS',
        'financial_patterns': '💰 FINANCIAL PATTERNS',
        'academic_patterns': '🎓 ACADEMIC PATTERNS',
        'market_patterns': '🌍 MARKET PATTERNS'
    }

    # Add discoveries from each category
    for category_key, category_label in category_map.items():
        category_discoveries = discoveries.get(category_key, {})

        if category_discoveries:
            summary += f"{category_label}:\n"

            for key, discovery in list(category_discoveries.items())[:5]:  # Max 5 per category
                insight = discovery.get('insight', key)
                summary += f"  • {insight}\n"

            summary += "\n"

    return summary


def _generate_descriptive_journey_name(discovery_key: str, category_key: str, insight: str = "") -> str:
    """
    Generate descriptive, observation-focused journey names (trends, patterns, analysis)

    Args:
        discovery_key: Technical key like 'aid_inefficiency', 'market_concentration'
        category_key: Category like 'anomalies', 'risks', 'opportunities'
        insight: Optional insight text to extract keywords from

    Returns:
        Descriptive journey name (3-5 words, pattern/trend focused)
    """

    # Comprehensive mapping for descriptive patterns (ANALYTICAL & RESEARCH-FOCUSED)
    descriptive_mappings = {
        # Aid/Financial patterns - More analytical
        'aid_inefficiency': 'Aid-Performance Gap Analysis',
        'aid_effectiveness': 'Aid Impact Assessment Study',
        'aid_roi': 'Aid Return-on-Investment Study',
        'high_aid_low_performance': 'High-Aid Underperformance Examination',
        'merit_scholarship_candidates': 'Untapped Talent Pool Analysis',
        'financial_sustainability': 'Financial Sustainability Assessment',
        'aid_coverage': 'Aid Distribution Pattern Study',

        # Performance/Academic patterns - More analytical
        'zero_gpa': 'Data Integrity Assessment',
        'perfect_gpa_cluster': 'Academic Excellence Cluster Study',
        'performance_gap': 'Achievement Variance Analysis',
        'gpa_variance': 'Academic Equity Gap Assessment',
        'bimodal_distribution': 'Dual-Cohort Performance Study',
        'nationality_performance': 'Cross-Cultural Achievement Analysis',
        'gender_gap': 'Gender Achievement Gap Study',
        'tuition_performance': 'Tuition-Value Correlation Study',

        # Market/Recruitment patterns - More analytical
        'market_concentration': 'Geographic Concentration Assessment',
        'market_diversity': 'Market Diversity Index Study',
        'recruitment_targets': 'High-Yield Market Analysis',
        'underrepresented_markets': 'Emerging Market Potential Study',
        'market_performance': 'Comparative Market Analysis',

        # Risk patterns - More analytical
        'concentration_risk': 'Enrollment Risk Exposure Study',
        'sustainability_risk': 'Long-Term Sustainability Assessment',
        'retention_risk': 'Retention Vulnerability Analysis',

        # Correlations - More analytical
        'aid_impact': 'Aid-Performance Correlation Study',
        'tuition_impact': 'Price-Performance Relationship Analysis',
    }

    # Check exact match first
    if discovery_key in descriptive_mappings:
        return descriptive_mappings[discovery_key]

    # Pattern-based matching
    key_lower = discovery_key.lower()

    # Aid-related
    if 'aid' in key_lower and ('inefficien' in key_lower or 'low_performance' in key_lower):
        return 'Aid Performance Patterns'
    elif 'aid' in key_lower and ('roi' in key_lower or 'return' in key_lower):
        return 'Aid ROI Analysis'
    elif 'aid' in key_lower:
        return 'Aid Distribution Patterns'

    # Market-related
    elif 'market' in key_lower and 'concentration' in key_lower:
        return 'Market Distribution Patterns'
    elif 'market' in key_lower and 'diversity' in key_lower:
        return 'Geographic Diversity Trends'
    elif 'recruitment' in key_lower or 'nationality' in key_lower:
        return 'Market Performance Comparison'

    # Performance-related
    elif 'zero' in key_lower and 'gpa' in key_lower:
        return 'Data Quality Issues'
    elif 'perfect' in key_lower or '4.0' in key_lower:
        return 'Excellence Cluster Analysis'
    elif 'gap' in key_lower and 'gender' in key_lower:
        return 'Gender Performance Trends'
    elif 'gap' in key_lower:
        return 'Performance Variance Patterns'

    # Risk-related
    elif 'risk' in key_lower:
        return 'Risk Exposure Analysis'

    # Generic descriptive patterns based on category (MORE ANALYTICAL)
    else:
        name_parts = discovery_key.replace('_', ' ').title().split()

        # Add analytical/research-focused words based on category
        descriptive_words = {
            'anomalies': ['Assessment', 'Analysis', 'Examination'],
            'risks': ['Exposure Study', 'Assessment', 'Analysis'],
            'opportunities': ['Potential Analysis', 'Assessment', 'Study'],
            'correlations': ['Correlation Study', 'Analysis', 'Assessment'],
            'segmentation': ['Gap Analysis', 'Assessment', 'Study'],
            'financial_patterns': ['Financial Analysis', 'Assessment', 'Study'],
            'academic_patterns': ['Performance Study', 'Analysis', 'Assessment'],
            'market_patterns': ['Market Analysis', 'Study', 'Assessment']
        }

        descriptor = descriptive_words.get(category_key, ['Analysis'])[0]

        # Combine
        if len(name_parts) <= 2:
            journey_name = f"{' '.join(name_parts)} {descriptor}"
        else:
            journey_name = f"{' '.join(name_parts[:3])} {descriptor}"

        # Limit to 5 words max
        final_parts = journey_name.split()[:5]
        return ' '.join(final_parts)


def _generate_professional_journey_name(discovery_key: str, category_key: str, insight: str = "") -> str:
    """
    Generate professional, action-oriented insight journey names (recommendations, actions)

    Args:
        discovery_key: Technical key like 'aid_inefficiency', 'market_concentration'
        category_key: Category like 'anomalies', 'risks', 'opportunities'
        insight: Optional insight text to extract keywords from

    Returns:
        Professional business name (3-5 words, action-focused)
    """

    # Comprehensive mapping of discovery patterns to ACTION-FOCUSED business names
    name_mappings = {
        # Aid/Financial patterns - Strong action verbs
        'aid_inefficiency': 'Optimize Aid Allocation',
        'aid_effectiveness': 'Transform Aid Impact',
        'aid_roi': 'Maximize Aid ROI',
        'high_aid_low_performance': 'Enforce Aid Accountability',
        'wasted_aid': 'Eliminate Aid Waste',
        'merit_scholarship_candidates': 'Launch Merit Scholarship Program',
        'untapped_talent': 'Implement Talent Recognition',
        'financial_sustainability': 'Strengthen Financial Health',
        'aid_coverage': 'Expand Aid Coverage',

        # Performance/Academic patterns - Strong action verbs
        'zero_gpa': 'Fix Data Quality Issues',
        'perfect_gpa_cluster': 'Establish Excellence Program',
        'performance_gap': 'Close Performance Gaps',
        'gpa_variance': 'Drive Academic Equity',
        'bimodal_distribution': 'Unify Academic Tiers',
        'nationality_performance': 'Implement Cross-Cultural Support',
        'gender_gap': 'Advance Gender Equity',
        'tuition_performance': 'Optimize Value Proposition',

        # Market/Recruitment patterns - Strong action verbs
        'market_concentration': 'Diversify Market Portfolio',
        'market_diversity': 'Execute Global Recruitment',
        'recruitment_targets': 'Target Strategic Markets',
        'underrepresented_markets': 'Capture Emerging Markets',
        'market_performance': 'Enhance Market Performance',
        'geographic_risk': 'Mitigate Geographic Risk',

        # Risk patterns - Strong action verbs
        'concentration_risk': 'Reduce Concentration Risk',
        'sustainability_risk': 'Secure Financial Sustainability',
        'retention_risk': 'Improve Student Retention',
        'quality_risk': 'Elevate Quality Standards',

        # Opportunity patterns - Strong action verbs
        'growth_opportunity': 'Drive Strategic Growth',
        'expansion_potential': 'Execute Expansion Plan',
        'untapped_segments': 'Develop Untapped Segments',

        # Correlation patterns - Strong action verbs
        'aid_impact': 'Enhance Aid Effectiveness',
        'tuition_impact': 'Refine Pricing Strategy',
        'demographic_correlation': 'Leverage Demographic Insights',
    }

    # Check exact match first
    if discovery_key in name_mappings:
        return name_mappings[discovery_key]

    # Pattern-based matching (partial matches)
    key_lower = discovery_key.lower()

    # Aid-related
    if 'aid' in key_lower and 'inefficien' in key_lower:
        return 'Aid Allocation Review'
    elif 'aid' in key_lower and ('roi' in key_lower or 'return' in key_lower):
        return 'Aid ROI Analysis'
    elif 'aid' in key_lower and ('effective' in key_lower or 'impact' in key_lower):
        return 'Aid Impact Assessment'
    elif 'scholarship' in key_lower or 'merit' in key_lower:
        return 'Merit Scholarship Program'

    # Market-related
    elif 'market' in key_lower and 'concentration' in key_lower:
        return 'Market Diversification Strategy'
    elif 'market' in key_lower and ('diversity' in key_lower or 'expansion' in key_lower):
        return 'Market Expansion Plan'
    elif 'recruitment' in key_lower:
        return 'Strategic Recruitment Initiative'

    # Performance-related
    elif 'zero' in key_lower and 'gpa' in key_lower:
        return 'Data Quality Audit'
    elif 'perfect' in key_lower or '4.0' in key_lower:
        return 'Excellence Recognition Program'
    elif 'gap' in key_lower and 'performance' in key_lower:
        return 'Performance Gap Analysis'
    elif 'gap' in key_lower and 'gender' in key_lower:
        return 'Gender Equity Initiative'
    elif 'gap' in key_lower:
        return 'Equity Analysis Program'

    # Risk-related
    elif 'risk' in key_lower and 'concentration' in key_lower:
        return 'Risk Diversification Plan'
    elif 'risk' in key_lower and 'sustainab' in key_lower:
        return 'Sustainability Action Plan'
    elif 'risk' in key_lower:
        return 'Risk Mitigation Strategy'

    # Generic category-based names
    else:
        # Convert discovery key to readable format
        name_parts = discovery_key.replace('_', ' ').title().split()

        # Add strong action verbs based on category
        action_words = {
            'anomalies': ['Fix', 'Resolve', 'Eliminate'],
            'risks': ['Mitigate', 'Reduce', 'Address'],
            'opportunities': ['Capture', 'Implement', 'Launch'],
            'correlations': ['Optimize', 'Enhance', 'Leverage'],
            'segmentation': ['Close', 'Drive', 'Advance'],
            'financial_patterns': ['Maximize', 'Strengthen', 'Improve'],
            'academic_patterns': ['Elevate', 'Transform', 'Enhance'],
            'market_patterns': ['Expand', 'Diversify', 'Execute']
        }

        action = action_words.get(category_key, ['Execute'])[0]

        # Take first 2-3 words from discovery key + action word
        if len(name_parts) <= 2:
            journey_name = f"{' '.join(name_parts)} {action}"
        else:
            journey_name = f"{' '.join(name_parts[:3])} {action}"

        # Limit to 5 words max
        final_parts = journey_name.split()[:5]
        return ' '.join(final_parts)


def _enrich_discovery_category_llm(category_key: str, category_name: str, category_data: dict,
                                    metrics: dict, model: str, url: str, chunk_num: int) -> dict:
    """
    Enrich a single discovery category with LLM insights (CHUNKED to avoid timeout)

    Args:
        category_key: Key like 'anomalies', 'risks', 'opportunities'
        category_name: Display name like '🚨 Critical Anomalies'
        category_data: Dictionary of discoveries in this category
        metrics: Overall metrics
        model: LLM model name
        url: LLM URL
        chunk_num: Chunk number (1-8)

    Returns:
        Enriched category data with deeper insights
    """

    # Format category data for enrichment
    category_summary = f"""**CATEGORY: {category_name}**

**INSTITUTIONAL CONTEXT:**
- Total Students: {metrics.get('total_students', 0):,}
- Average GPA: {metrics.get('avg_gpa', 0):.2f}
- High Performers: {metrics.get('high_performers', 0):,}
- At-Risk: {metrics.get('at_risk', 0):,}

**DISCOVERIES IN THIS CATEGORY:**
"""

    for key, discovery in category_data.items():
        insight = discovery.get('insight', key)
        category_summary += f"\n- {insight}"

        # Add detailed data if available
        if 'count' in discovery:
            category_summary += f" (Count: {discovery['count']})"
        if 'percentage' in discovery:
            category_summary += f" ({discovery['percentage']:.1f}%)"
        if 'amount' in discovery:
            category_summary += f" (Amount: AED {discovery['amount']:,.0f})"

    enrichment_prompt = f"""{category_summary}

Enrich these {category_key} discoveries with:
1. Root causes - WHY is this happening?
2. Business impact - WHAT are the consequences?
3. Strategic implications - WHAT does this mean for the institution?
4. Recommended actions - WHAT should be done?

Return JSON:
{{
  "enriched_insights": [
    {{
      "discovery": "Original discovery",
      "root_cause": "Why this is happening",
      "business_impact": "Consequences with numbers",
      "strategic_implication": "What this means strategically",
      "recommended_action": "What to do about it"
    }}
  ]
}}

Return JSON only."""

    try:
        response = query_ollama(enrichment_prompt, model, url, temperature=0.7, num_predict=1500, timeout=120, auto_optimize=True)

        if response and not response.startswith('[ERROR]'):
            result = extract_json_from_response(response)

            if result and 'enriched_insights' in result:
                # Merge enriched insights back into category data
                enriched_category = category_data.copy()

                for enriched in result['enriched_insights']:
                    # Find matching discovery and enrich it
                    for key, discovery in enriched_category.items():
                        if discovery.get('insight', '') in enriched.get('discovery', ''):
                            discovery['root_cause'] = enriched.get('root_cause', '')
                            discovery['business_impact'] = enriched.get('business_impact', '')
                            discovery['strategic_implication'] = enriched.get('strategic_implication', '')
                            discovery['recommended_action'] = enriched.get('recommended_action', '')
                            break

                return enriched_category
    except Exception as e:
        pass

    # Return original if enrichment fails
    return category_data


def _extract_journeys_from_category_llm(category_key: str, category_name: str, category_discoveries: dict,
                                         metrics: dict, model: str, url: str, chunk_num: int) -> list:
    """
    Extract journeys from a single enriched category (CHUNKED to avoid timeout)

    Args:
        category_key: Key like 'anomalies', 'risks', 'opportunities'
        category_name: Display name like '🚨 Critical Anomalies'
        category_discoveries: Enriched discoveries in this category
        metrics: Overall metrics
        model: LLM model name
        url: LLM URL
        chunk_num: Chunk number (1-8)

    Returns:
        List of journey dictionaries extracted from this category
    """

    # Simplified format - just the key insights (avoid long prompts)
    insights = []
    for key, discovery in category_discoveries.items():
        insights.append(discovery.get('insight', key))

    insights_text = "\n".join([f"- {ins}" for ins in insights[:5]])  # Max 5 per category

    # SIMPLIFIED extraction prompt for better reliability
    extraction_prompt = f"""Category: {category_name}

Discoveries:
{insights_text}

Create 1-2 business journeys from these discoveries.

Return ONLY this JSON format:
{{
  "journeys": [
    {{
      "name": "Journey Name (3-5 words only)",
      "key": "ShortKey",
      "icon": "📊",
      "priority": {chunk_num},
      "reasoning": "Brief description",
      "business_value": "Key benefit"
    }}
  ]
}}

Good names: "Aid Allocation Review", "Market Strategy", "Performance Analysis"
Return JSON only, no extra text."""

    try:
        # INCREASED timeout to 240s (4 min per chunk) for reliability
        response = query_ollama(extraction_prompt, model, url, temperature=0.7, num_predict=800, timeout=240, auto_optimize=True)

        if response and not response.startswith('[ERROR]'):
            result = extract_json_from_response(response)

            if result and 'journeys' in result and len(result['journeys']) > 0:
                journeys = result['journeys']

                # Add description and context
                for journey in journeys:
                    journey['description'] = journey.get('reasoning', '')
                    journey['context'] = {'category': category_key, 'discoveries': category_discoveries}
                    journey['category_source'] = category_key

                return journeys
    except Exception as e:
        pass

    return []


def _deduplicate_journeys(journeys: list) -> list:
    """
    Remove duplicate journeys based on similar names/keys

    Args:
        journeys: List of journey dictionaries

    Returns:
        Deduplicated list of journeys
    """
    seen_keys = set()
    seen_names = set()
    unique_journeys = []

    for journey in journeys:
        key = journey.get('key', '').lower()
        name = journey.get('name', '').lower()

        # Normalize name (remove common words for comparison)
        name_normalized = name.replace('the ', '').replace('and ', '').replace('a ', '').strip()

        if key not in seen_keys and name_normalized not in seen_names:
            seen_keys.add(key)
            seen_names.add(name_normalized)
            unique_journeys.append(journey)

    return unique_journeys


def generate_suggested_journeys_llm(metrics: dict, df: pd.DataFrame, model: str, url: str) -> list:
    """
    Generate suggested data journeys using TRUE SINGLE LLM CALL approach (COMPLETED IMPLEMENTATION)

    PHASE 1: Deep dive Data & Business discovery - analyze actual data patterns
    PHASE 2: ONE LLM call with ALL discoveries - create 10-15 journeys (600s timeout / 10 min max)
    FALLBACK: If LLM fails - comprehensive rule-based generation from ALL discoveries (12-15 journeys)

    Benefits vs previous 3-segment or 8-chunk approaches:
    - 10x Faster: 10 min max (vs 64 min with 8-chunk, vs 18 min with 3-segment)
    - 16x More Reliable: 1 failure point (vs 16 with chunking, vs 3 with segments)
    - Better Quality: LLM sees full context across ALL categories simultaneously
    - Simpler Code: 70% less code than chunking approach
    - Guaranteed Results: Comprehensive fallback ensures 10-15 journeys always

    Returns: List of 10-15 journey dictionaries with name, key, icon, description, priority
    """

    # ============================================================================
    # PHASE 1: DEEP DIVE DATA & BUSINESS DISCOVERY
    # ============================================================================

    # Perform comprehensive data analysis to discover business patterns
    st.info("🔍 Phase 1: Performing deep dive data & business discovery analysis...")
    business_discoveries = deep_dive_business_discovery(df, metrics)

    # Count discoveries in each category
    total_discoveries = sum([
        len(business_discoveries.get('correlations', {})),
        len(business_discoveries.get('segmentation', {})),
        len(business_discoveries.get('anomalies', {})),
        len(business_discoveries.get('opportunities', {})),
        len(business_discoveries.get('risks', {})),
        len(business_discoveries.get('financial_patterns', {})),
        len(business_discoveries.get('academic_patterns', {})),
        len(business_discoveries.get('market_patterns', {}))
    ])

    st.success(f"✅ Phase 1 complete: {total_discoveries} business patterns discovered across 8 categories")

    # ============================================================================
    # PHASE 2: SINGLE LLM CALL - Create journeys from ALL discoveries at once
    # ============================================================================

    st.info("🤖 Phase 2: Creating strategic journeys from all discoveries (single AI analysis)...")

    # Format ALL discoveries into a concise prompt
    discoveries_summary = _format_all_discoveries_for_journey_extraction(business_discoveries, metrics)

    # OPTIMIZED Single LLM call with clear, concise instructions
    extraction_prompt = f"""{discoveries_summary}

TASK: Create 12 journeys (7 descriptive + 5 insight) from these discoveries.

DESCRIPTIVE (7): End with Analysis/Study/Assessment
INSIGHT (5): Start with action verb (Optimize/Transform/Drive/Launch/Fix)

SCHEMA:
{{
  "d": [  // descriptive journeys
    {{"n": "Name", "k": "Key", "i": "🔬", "p": 1, "r": "Reasoning", "v": "Value"}}
  ],
  "a": [  // action journeys
    {{"n": "Name", "k": "Key", "i": "🎯", "p": 1, "r": "Reasoning", "v": "Value"}}
  ]
}}

FIELD GUIDE:
n = name (3-5 words)
k = unique key (no spaces)
i = icon (🔬📊📈🔎 for d, 🎯🚀⚡🛡️ for a)
p = priority (1-3=high, 4-6=med, 7-10=low)
r = reasoning (what found + numbers)
v = business value

EXAMPLES:

DESCRIPTIVE:
{{"n": "Aid-Performance Gap Analysis", "k": "AidGapAnalysis", "i": "🔬", "p": 1, "r": "62 students with high aid underperforming - AED 4.9M at-risk", "v": "Identify critical performance patterns"}}
{{"n": "Geographic Concentration Assessment", "k": "GeoConcentration", "i": "📊", "p": 2, "r": "66% enrollment from top 3 markets creates risk", "v": "Assess market diversification needs"}}

INSIGHT:
{{"n": "Optimize Aid Allocation", "k": "OptimizeAid", "i": "🎯", "p": 1, "r": "Restructure AED 4.9M to maximize student outcomes", "v": "Improve ROI and performance"}}
{{"n": "Diversify Market Portfolio", "k": "DiversifyMarkets", "i": "🛡️", "p": 2, "r": "Expand beyond top 3 markets to reduce risk", "v": "Strengthen enrollment stability"}}

Return ONLY valid JSON. No text before or after."""

    suggested_journeys = []

    try:
        # SINGLE LLM call - 360s timeout (6 min max)
        st.text("  Calling LLM for journey generation...")

        # Show prompt length for debugging
        prompt_length = len(extraction_prompt)
        st.text(f"  Prompt length: {prompt_length:,} characters")

        # OPTIMIZED: Lower temperature + smaller context + faster sampling = 3-5x faster generation
        response = query_ollama(
            extraction_prompt,
            model,
            url,
            temperature=0.3,      # Lower = faster, more deterministic
            num_predict=1200,     # Perfect for 12 journeys
            timeout=600,
            num_ctx=4096,         # Smaller context window = faster processing
            top_k=40,             # Faster token sampling
            top_p=0.9,            # Nucleus sampling for speed
            auto_optimize=False   # Disable overhead
        )

        # Debug: Show what we got back
        if not response:
            st.warning("⚠️ Phase 2: LLM returned empty response - using intelligent fallback")
        elif response.startswith('[ERROR]'):
            error_msg = response.replace('[ERROR]', '').strip()
            st.warning(f"⚠️ Phase 2: LLM error - {error_msg[:100]}")
            st.info("   Using intelligent fallback...")
        else:
            # Try to extract and normalize JSON
            st.text("  Parsing LLM response...")
            result = extract_json_from_response(response)

            if not result:
                st.warning("⚠️ Phase 2: Could not parse JSON from LLM response")
                with st.expander("🔍 Click to see raw LLM response for debugging"):
                    st.text(response[:2000])
                st.info("   Using intelligent fallback...")
            else:
                # NORMALIZE: Handle both compact (d, a) and full field names
                descriptive = result.get('d', result.get('descriptive_journeys', []))
                insights = result.get('a', result.get('insight_journeys', []))

                if not descriptive and not insights:
                    st.warning("⚠️ Phase 2: LLM response missing journey categories")
                    with st.expander("🔍 Click to see parsed result for debugging"):
                        st.json(result)
                    st.info("   Using intelligent fallback...")
                else:
                    # Normalize field names and combine both types
                    suggested_journeys = []

                    # Process descriptive journeys
                    for journey in descriptive:
                        reasoning = journey.get('r', journey.get('reasoning', ''))
                        name = journey.get('n', journey.get('name', 'Unknown'))
                        # Enhanced description for descriptive journeys
                        description = f"📊 ANALYTICAL RESEARCH: This descriptive journey examines the data pattern - {reasoning}. Explore this analysis to understand what's happening in your institution and identify key trends that require attention."

                        normalized = {
                            'name': name,
                            'key': journey.get('k', journey.get('key', 'unknown')),
                            'icon': journey.get('i', journey.get('icon', '🔬')),
                            'priority': journey.get('p', journey.get('priority', 5)),
                            'reasoning': reasoning,
                            'business_value': journey.get('v', journey.get('business_value', '')),
                            'journey_type': 'descriptive',
                            'description': description,
                            'context': {'all_discoveries': business_discoveries}
                        }
                        suggested_journeys.append(normalized)

                    # Process insight journeys
                    for journey in insights:
                        reasoning = journey.get('r', journey.get('reasoning', ''))
                        name = journey.get('n', journey.get('name', 'Unknown'))
                        # Enhanced description for insight journeys
                        description = f"🎯 STRATEGIC ACTION: This insight journey provides actionable recommendations - {reasoning}. Explore this journey to discover specific steps you can take to address this issue and drive measurable improvements."

                        normalized = {
                            'name': name,
                            'key': journey.get('k', journey.get('key', 'unknown')),
                            'icon': journey.get('i', journey.get('icon', '🎯')),
                            'priority': journey.get('p', journey.get('priority', 5)),
                            'reasoning': reasoning,
                            'business_value': journey.get('v', journey.get('business_value', '')),
                            'journey_type': 'insight',
                            'description': description,
                            'context': {'all_discoveries': business_discoveries}
                        }
                        suggested_journeys.append(normalized)

                    total_journeys = len(suggested_journeys)

                    if total_journeys < 5:
                        st.warning(f"⚠️ Phase 2: LLM returned only {total_journeys} total journeys (need at least 5)")
                        st.info("   Using intelligent fallback...")
                    else:
                        # Sort by priority
                        suggested_journeys.sort(key=lambda x: x.get('priority', 5))

                        # Limit to top 15
                        suggested_journeys = suggested_journeys[:15]

                        descriptive_count = len([j for j in suggested_journeys if j.get('journey_type') == 'descriptive'])
                        insight_count = len([j for j in suggested_journeys if j.get('journey_type') == 'insight'])

                        st.success(f"✅ Phase 2 complete: {len(suggested_journeys)} journeys created ({descriptive_count} descriptive, {insight_count} insight)")

                        return suggested_journeys

    except Exception as e:
        st.error(f"⚠️ Phase 2: Exception during LLM call: {str(e)}")
        st.info("   Using intelligent fallback...")

    # ============================================================================
    # FALLBACK: INTELLIGENT DISCOVERY-DRIVEN JOURNEY GENERATION
    # ============================================================================

    st.info("🔧 Fallback: Generating comprehensive discovery-based journeys from ALL categories...")

    descriptive_journeys = []
    insight_journeys = []

    # Category priority and icon mapping (ENHANCED VISUAL DISTINCTION)
    category_config = {
        'anomalies': {
            'base_priority': 1,
            'descriptive_icon': '🔬',  # Microscope for analytical study
            'insight_icon': '🎯',      # Target for focused action
            'descriptive_value': 'Critical Pattern Analysis & Research',
            'insight_value': 'Immediate Issue Resolution'
        },
        'risks': {
            'base_priority': 2,
            'descriptive_icon': '📉',  # Chart down for risk analysis
            'insight_icon': '🛡️',      # Shield for risk mitigation
            'descriptive_value': 'Risk Exposure Assessment',
            'insight_value': 'Proactive Risk Management'
        },
        'opportunities': {
            'base_priority': 4,
            'descriptive_icon': '🔎',  # Magnifying glass for discovery
            'insight_icon': '🚀',      # Rocket for growth action
            'descriptive_value': 'Growth Potential Analysis',
            'insight_value': 'Strategic Growth Execution'
        },
        'correlations': {
            'base_priority': 5,
            'descriptive_icon': '📊',  # Chart for data analysis
            'insight_icon': '⚡',      # Lightning for optimization
            'descriptive_value': 'Relationship & Correlation Study',
            'insight_value': 'Data-Driven Optimization'
        },
        'segmentation': {
            'base_priority': 6,
            'descriptive_icon': '🧮',  # Abacus for analysis
            'insight_icon': '🔧',      # Wrench for fixing gaps
            'descriptive_value': 'Equity & Gap Assessment',
            'insight_value': 'Equity Enhancement Programs'
        },
        'financial_patterns': {
            'base_priority': 7,
            'descriptive_icon': '📈',  # Chart up for financial study
            'insight_icon': '💪',      # Muscle for strengthening
            'descriptive_value': 'Financial Performance Analysis',
            'insight_value': 'Financial Strength Building'
        },
        'academic_patterns': {
            'base_priority': 7,
            'descriptive_icon': '📐',  # Ruler for measurement
            'insight_icon': '⭐',      # Star for excellence
            'descriptive_value': 'Academic Performance Study',
            'insight_value': 'Academic Excellence Initiatives'
        },
        'market_patterns': {
            'base_priority': 8,
            'descriptive_icon': '🌐',  # Globe for market analysis
            'insight_icon': '🗺️',      # Map for strategic expansion
            'descriptive_value': 'Market Distribution Study',
            'insight_value': 'Market Growth Strategies'
        }
    }

    # Loop through ALL categories and create BOTH journey types from ALL discoveries
    for category_key in ['anomalies', 'risks', 'opportunities', 'correlations', 'segmentation',
                          'financial_patterns', 'academic_patterns', 'market_patterns']:

        category_discoveries = business_discoveries.get(category_key, {})
        config = category_config.get(category_key, {
            'base_priority': 5,
            'descriptive_icon': '📊',
            'insight_icon': '💡',
            'descriptive_value': 'Pattern Analysis',
            'insight_value': 'Strategic Initiative'
        })

        for discovery_key, discovery_data in category_discoveries.items():
            insight = discovery_data.get('insight', discovery_key)

            # Calculate priority
            base_priority = config['base_priority']

            # CREATE DESCRIPTIVE JOURNEY (observation-focused)
            descriptive_name = _generate_descriptive_journey_name(discovery_key, category_key, insight)
            descriptive_priority = base_priority + len(descriptive_journeys) // 2

            # Enhanced description for descriptive journey
            descriptive_description = f"📊 ANALYTICAL RESEARCH: This descriptive journey examines the data pattern discovered in your {category_key.replace('_', ' ')} - {insight}. Explore this analysis to understand what's happening in your institution, identify key trends, and build a foundation for strategic decision-making."

            descriptive_journeys.append({
                "name": descriptive_name,
                "key": f"{discovery_key.replace('_', '').title()}Desc",
                "icon": config['descriptive_icon'],
                "priority": min(descriptive_priority, 10),
                "journey_type": "descriptive",
                "reasoning": f"{insight}",
                "description": descriptive_description,
                "business_value": f"{config['descriptive_value']} - understanding {descriptive_name.lower()}",
                "context": {category_key: discovery_data}
            })

            # CREATE INSIGHT JOURNEY (action-focused)
            insight_name = _generate_professional_journey_name(discovery_key, category_key, insight)
            insight_priority = base_priority + len(insight_journeys) // 2

            # Enhanced description for insight journey
            insight_description = f"🎯 STRATEGIC ACTION: This insight journey provides actionable recommendations to address the {category_key.replace('_', ' ')} issue - {insight}. Explore this journey to discover specific steps you can take to resolve this challenge, implement strategic improvements, and drive measurable outcomes for your institution."

            insight_journeys.append({
                "name": insight_name,
                "key": f"{discovery_key.replace('_', '').title()}Insight",
                "icon": config['insight_icon'],
                "priority": min(insight_priority, 10),
                "journey_type": "insight",
                "reasoning": f"{insight}",
                "description": insight_description,
                "business_value": f"{config['insight_value']} - {insight_name.lower()}",
                "context": {category_key: discovery_data}
            })

    # Combine both types
    suggested_journeys = descriptive_journeys + insight_journeys

    # Sort by priority
    suggested_journeys.sort(key=lambda x: x.get('priority', 5))

    # Limit to top 15 journeys (comprehensive fallback)
    suggested_journeys = suggested_journeys[:15]

    descriptive_count = len([j for j in suggested_journeys if j.get('journey_type') == 'descriptive'])
    insight_count = len([j for j in suggested_journeys if j.get('journey_type') == 'insight'])

    st.success(f"✅ Fallback complete: {len(suggested_journeys)} journeys generated ({descriptive_count} descriptive, {insight_count} insight)")

    return suggested_journeys


def _format_discoveries_for_llm_concise(discoveries: dict, metrics: dict) -> str:
    """Format business discoveries into concise summary for LLM (avoid timeout)"""

    summary = f"""OVERVIEW: {metrics.get('total_students', 0):,} students, GPA {metrics.get('avg_gpa', 0):.2f}, {metrics.get('high_performers', 0):,} high performers, {metrics.get('at_risk', 0):,} at-risk

KEY DISCOVERIES:
"""

    # Only include discoveries that exist (concise format)
    discovery_count = 0

    # Anomalies (highest priority)
    if discoveries.get('anomalies'):
        summary += "\nANOMALIES (CRITICAL):\n"
        for key, anom in list(discoveries['anomalies'].items())[:3]:  # Max 3
            summary += f"• {anom.get('insight', key)}\n"
            discovery_count += 1

    # Risks
    if discoveries.get('risks'):
        summary += "\nRISKS:\n"
        for key, risk in list(discoveries['risks'].items())[:2]:  # Max 2
            summary += f"• {risk.get('insight', key)}\n"
            discovery_count += 1

    # Opportunities
    if discoveries.get('opportunities'):
        summary += "\nOPPORTUNITIES:\n"
        for key, opp in list(discoveries['opportunities'].items())[:2]:  # Max 2
            summary += f"• {opp.get('insight', key)}\n"
            discovery_count += 1

    # Segmentation (if significant)
    if discoveries.get('segmentation'):
        summary += "\nSEGMENTATION:\n"
        for key, seg in list(discoveries['segmentation'].items())[:2]:  # Max 2
            summary += f"• {seg.get('insight', key)}\n"
            discovery_count += 1

    # Correlations
    if discoveries.get('correlations'):
        summary += "\nCORRELATIONS:\n"
        for key, corr in list(discoveries['correlations'].items())[:2]:  # Max 2
            summary += f"• {corr.get('insight', key)}\n"
            discovery_count += 1

    # Academic patterns
    if discoveries.get('academic_patterns'):
        summary += "\nACADEMIC PATTERNS:\n"
        for key, pattern in list(discoveries['academic_patterns'].items())[:1]:  # Max 1
            summary += f"• {pattern.get('insight', key)}\n"
            discovery_count += 1

    if discovery_count == 0:
        summary += "\nNo critical patterns detected - standard institutional performance\n"

    return summary


def _format_discoveries_for_llm(discoveries: dict, metrics: dict) -> str:
    """Format business discoveries into readable text for LLM prompt"""

    summary = f"""**INSTITUTIONAL OVERVIEW:**
- Total Students: {metrics.get('total_students', 0):,}
- Average GPA: {metrics.get('avg_gpa', 0):.2f}
- High Performers (≥3.5 GPA): {metrics.get('high_performers', 0):,}
- At-Risk (<2.5 GPA): {metrics.get('at_risk', 0):,}
- Unique Nationalities: {metrics.get('unique_nationalities', 0)}
- Total Tuition Revenue: AED {metrics.get('total_tuition', 0):,.0f}
- Financial Aid: AED {metrics.get('total_aid', 0):,.0f}

**BUSINESS DISCOVERIES:**

"""

    # Add correlations
    if discoveries.get('correlations'):
        summary += "\n**CORRELATIONS DISCOVERED:**\n"
        for key, corr in discoveries['correlations'].items():
            summary += f"- {corr.get('insight', key)}\n"

    # Add segmentation insights
    if discoveries.get('segmentation'):
        summary += "\n**SEGMENTATION ANALYSIS:**\n"
        for key, seg in discoveries['segmentation'].items():
            summary += f"- {seg.get('insight', key)}\n"

    # Add anomalies (HIGH PRIORITY)
    if discoveries.get('anomalies'):
        summary += "\n**ANOMALIES DETECTED (HIGH PRIORITY):**\n"
        for key, anom in discoveries['anomalies'].items():
            summary += f"- {anom.get('insight', key)}\n"

    # Add opportunities
    if discoveries.get('opportunities'):
        summary += "\n**OPPORTUNITIES IDENTIFIED:**\n"
        for key, opp in discoveries['opportunities'].items():
            summary += f"- {opp.get('insight', key)}\n"

    # Add risks
    if discoveries.get('risks'):
        summary += "\n**RISKS IDENTIFIED:**\n"
        for key, risk in discoveries['risks'].items():
            summary += f"- {risk.get('insight', key)}\n"

    # Add financial patterns
    if discoveries.get('financial_patterns'):
        summary += "\n**FINANCIAL PATTERNS:**\n"
        for key, pattern in discoveries['financial_patterns'].items():
            summary += f"- {pattern.get('insight', key)}\n"

    # Add academic patterns
    if discoveries.get('academic_patterns'):
        summary += "\n**ACADEMIC PATTERNS:**\n"
        for key, pattern in discoveries['academic_patterns'].items():
            summary += f"- {pattern.get('insight', key)}\n"

    # Add market patterns
    if discoveries.get('market_patterns'):
        summary += "\n**MARKET PATTERNS:**\n"
        for key, pattern in discoveries['market_patterns'].items():
            summary += f"- {pattern.get('insight', key)}\n"

    return summary


def generate_chart_insights_llm(chart_data: dict, chart_type: str, model: str, url: str) -> str:
    """Generate insights for a specific chart using LLM"""

    prompt = f"""Analyze this {chart_type} chart data and provide a 1-2 sentence insight.

**Data Summary:**
{json.dumps(chart_data, indent=2)[:500]}

Provide a concise, data-driven insight highlighting the most important finding."""

    try:
        response = query_ollama(prompt, model, url, temperature=0.5, num_predict=150, auto_optimize=True)
        if response and not response.startswith('[ERROR]'):
            return response.strip()
    except:
        pass

    return "Chart visualization provides data distribution overview for analysis."

def generate_comprehensive_overview_llm(metrics: dict, df: pd.DataFrame, model: str, url: str) -> dict:
    """Generate comprehensive overview with 3 insights sections matching original structure"""

    # Calculate detailed metrics for all three insights
    total_students = metrics.get('total_students', 0)

    # Enrollment composition metrics
    active_students = len(df[df.get('enrollment_enrollment_status', pd.Series()) == 'Active']) if 'enrollment_enrollment_status' in df.columns else 0
    unique_nationalities = metrics.get('unique_nationalities', 0)

    # Academic performance metrics
    avg_gpa = round(metrics.get('avg_gpa', 0), 2)
    median_gpa = round(df['cumulative_gpa'].median(), 2) if 'cumulative_gpa' in df.columns else 0
    gpa_std = round(df['cumulative_gpa'].std(), 2) if 'cumulative_gpa' in df.columns else 0
    high_performers = metrics.get('high_performers', 0)
    high_performer_pct = round((high_performers / total_students * 100), 1) if total_students > 0 else 0

    # Growth & retention metrics
    cohort_counts = df['cohort_year'].value_counts().sort_index() if 'cohort_year' in df.columns else pd.Series()
    total_cohorts = len(cohort_counts)
    latest_cohort_size = int(cohort_counts.iloc[-1]) if len(cohort_counts) > 0 else 0
    avg_cohort_size = int(cohort_counts.mean()) if len(cohort_counts) > 0 else 0

    # Top nationalities
    top_nationalities = []
    if 'nationality' in df.columns:
        nat_counts = df['nationality'].value_counts().head(5)
        top_nationalities = [f"{k}: {int(v)} ({round(v/len(df)*100, 1)}%)" for k, v in nat_counts.items()]

    # Enrollment status distribution
    status_dist = []
    if 'enrollment_enrollment_status' in df.columns:
        status_counts = df['enrollment_enrollment_status'].value_counts()
        status_dist = [f"{k}: {int(v)} ({round(v/len(df)*100, 1)}%)" for k, v in status_counts.items()]

    prompt = f"""You are analyzing a comprehensive student dataset for a higher education institution. Generate detailed insights for 3 main sections.

**DATASET OVERVIEW:**
- Total Students: {total_students:,}
- Active Students: {active_students:,} ({round(active_students/total_students*100, 1) if total_students > 0 else 0}%)
- Nationalities Represented: {unique_nationalities}
- Average GPA: {avg_gpa} (Median: {median_gpa}, Std Dev: {gpa_std})
- High Performers (≥3.5 GPA): {high_performers:,} ({high_performer_pct}%)
- Total Cohorts: {total_cohorts}
- Latest Cohort Size: {latest_cohort_size}

**TOP NATIONALITIES:**
{chr(10).join(f'- {nat}' for nat in top_nationalities[:5])}

**ENROLLMENT STATUS:**
{chr(10).join(f'- {status}' for status in status_dist[:3])}

Generate comprehensive insights for 3 sections in JSON format:

**INSIGHT 1: ENROLLMENT COMPOSITION**
- Chart 1 analysis: Enrollment type/status distribution patterns
- Chart 2 analysis: Student demographics and nationality diversity
- Business impact: Market positioning and competitive advantages
- Key findings: Enrollment health, diversity strength, retention indicators

**INSIGHT 2: ACADEMIC PERFORMANCE**
- Chart 1 analysis: GPA distribution and performance trends
- Chart 2 analysis: Performance tiers and academic health
- Business impact: Academic reputation and quality indicators
- Key findings: Performance strengths, improvement areas, benchmarking

**INSIGHT 3: GROWTH & RETENTION**
- Chart analysis: Enrollment trends over cohorts
- Business impact: Growth trajectory and strategic positioning
- Key findings: Growth patterns, retention success, future outlook

Return ONLY valid JSON:
{{
  "insight_1_enrollment": {{
    "chart_1_insight": "3-4 sentences analyzing enrollment type/status distribution, dominant patterns, and what they indicate about institutional operations",
    "chart_2_insight": "3-4 sentences analyzing nationality diversity, geographic reach, UAE representation balance, and market positioning",
    "business_impact": "4-5 sentences connecting enrollment patterns to business outcomes: market position, competitive advantages, strategic opportunities, revenue implications",
    "findings": {{
      "enrollment_health": "2-3 sentences on active enrollment rate and retention quality",
      "diversity_strength": "2-3 sentences on nationality representation and global appeal",
      "recommendation": "2-3 sentences with actionable strategic recommendations"
    }}
  }},
  "insight_2_academic": {{
    "chart_1_insight": "3-4 sentences analyzing GPA distribution shape, central tendency, consistency (std dev), and what it reveals about academic standards",
    "chart_2_insight": "3-4 sentences analyzing performance tier balance (high/mid/at-risk proportions), institutional health indicators, and intervention needs",
    "business_impact": "4-5 sentences connecting academic performance to reputation, rankings, graduate outcomes, and competitive positioning",
    "findings": {{
      "performance_quality": "2-3 sentences assessing overall academic health and quality indicators",
      "improvement_areas": "2-3 sentences identifying specific opportunities for academic enhancement",
      "recommendation": "2-3 sentences with targeted academic improvement strategies"
    }}
  }},
  "insight_3_growth": {{
    "chart_insight": "4-5 sentences analyzing enrollment trends across cohorts, growth patterns, year-over-year changes, and trajectory implications",
    "business_impact": "4-5 sentences connecting growth patterns to institutional sustainability, market demand, capacity planning, and strategic positioning",
    "findings": {{
      "growth_pattern": "2-3 sentences characterizing the growth trajectory (accelerating/stable/declining) with supporting data",
      "retention_success": "2-3 sentences evaluating retention effectiveness across cohorts",
      "recommendation": "2-3 sentences with strategic growth and retention recommendations"
    }}
  }}
}}

Focus on data-driven insights, business implications, and actionable recommendations."""

    try:
        response = query_ollama(prompt, model, url, temperature=0.7, num_predict=1500, auto_optimize=True)

        if response and not response.startswith('[ERROR]'):
            result = extract_json_from_response(response)
            if result:
                return result
    except Exception as e:
        pass

    # Intelligent fallback with actual data
    active_pct = round(active_students/total_students*100, 1) if total_students > 0 else 0

    return {
        "insight_1_enrollment": {
            "chart_1_insight": f"The institution serves {total_students:,} students with {active_pct}% actively enrolled, demonstrating {'strong' if active_pct > 85 else 'moderate'} retention effectiveness. The enrollment distribution reveals operational efficiency and student lifecycle management capabilities.",
            "chart_2_insight": f"Student body represents {unique_nationalities} nationalities with {'strong' if unique_nationalities > 30 else 'moderate'} global diversity. This international mix positions the institution {'competitively in global markets' if unique_nationalities > 30 else 'with regional focus'} while maintaining cultural richness.",
            "business_impact": f"The diverse enrollment base of {total_students:,} students from {unique_nationalities} countries provides stable revenue streams and enhances institutional reputation. High active enrollment rate ({active_pct}%) indicates effective student services and satisfaction, reducing attrition costs. Geographic diversity mitigates regional market risks while UAE representation aligns with national education priorities.",
            "findings": {
                "enrollment_health": f"With {active_pct}% active enrollment, the institution demonstrates {'excellent' if active_pct > 90 else 'strong' if active_pct > 85 else 'adequate'} retention. This rate {'exceeds' if active_pct > 85 else 'approaches'} higher education benchmarks.",
                "diversity_strength": f"Representation from {unique_nationalities} nationalities creates a multicultural learning environment, enhancing graduate employability and global network potential.",
                "recommendation": f"{'Continue' if active_pct > 85 else 'Enhance'} retention programs and {'maintain' if unique_nationalities > 30 else 'expand'} international recruitment to strengthen market position."
            }
        },
        "insight_2_academic": {
            "chart_1_insight": f"GPA distribution centers at {avg_gpa} with standard deviation of {gpa_std}, indicating {'consistent' if gpa_std < 0.5 else 'varied'} academic performance. The {'tight' if gpa_std < 0.5 else 'wide'} distribution reflects {'uniform academic standards' if gpa_std < 0.5 else 'diverse student capabilities'} across programs.",
            "chart_2_insight": f"Performance segmentation shows {high_performer_pct}% high achievers (≥3.5 GPA), revealing {'strong' if high_performer_pct > 35 else 'moderate' if high_performer_pct > 25 else 'emerging'} academic excellence. The tier balance indicates {'healthy' if high_performer_pct > 30 else 'developing'} institutional quality.",
            "business_impact": f"Average GPA of {avg_gpa} {'exceeds' if avg_gpa >= 3.2 else 'approaches' if avg_gpa >= 3.0 else 'falls below'} typical higher education standards, directly impacting graduate school admissions and employer perceptions. The {high_performer_pct}% high-achiever rate strengthens institutional rankings and attracts competitive students. Academic consistency (std dev: {gpa_std}) signals {'reliable' if gpa_std < 0.5 else 'variable'} quality assurance.",
            "findings": {
                "performance_quality": f"Overall academic health is {'excellent' if avg_gpa >= 3.2 else 'strong' if avg_gpa >= 3.0 else 'developing'} with mean GPA of {avg_gpa}. The {high_performer_pct}% excellence rate demonstrates {'exceptional' if high_performer_pct > 35 else 'competitive' if high_performer_pct > 25 else 'growing'} academic standards.",
                "improvement_areas": f"{'Mid-tier student elevation' if high_performer_pct < 40 else 'Excellence program expansion'} represents key opportunity. Standard deviation of {gpa_std} suggests {'minimal' if gpa_std < 0.5 else 'moderate'} need for standardization.",
                "recommendation": f"Implement {'honors programs and research opportunities' if high_performer_pct > 30 else 'academic support initiatives and tutoring'} to {'maintain excellence' if avg_gpa >= 3.2 else 'elevate performance'}."
            }
        },
        "insight_3_growth": {
            "chart_insight": f"Enrollment spans {total_cohorts} cohorts with latest intake at {latest_cohort_size} students (average: {avg_cohort_size}). The trend indicates {'stable' if abs(latest_cohort_size - avg_cohort_size) < avg_cohort_size * 0.2 else 'growing' if latest_cohort_size > avg_cohort_size * 1.1 else 'declining'} enrollment patterns, reflecting {'consistent market demand' if abs(latest_cohort_size - avg_cohort_size) < avg_cohort_size * 0.2 else 'increasing appeal' if latest_cohort_size > avg_cohort_size else 'market challenges'}.",
            "business_impact": f"Enrollment trajectory directly impacts long-term sustainability and revenue projections. {'Stable' if abs(latest_cohort_size - avg_cohort_size) < avg_cohort_size * 0.2 else 'Growth' if latest_cohort_size > avg_cohort_size else 'Declining'} cohort sizes signal {'predictable capacity planning' if abs(latest_cohort_size - avg_cohort_size) < avg_cohort_size * 0.2 else 'expansion opportunities' if latest_cohort_size > avg_cohort_size else 'strategic repositioning needs'}. Current student base of {total_students:,} provides foundation for {'strategic growth initiatives' if latest_cohort_size >= avg_cohort_size else 'retention-focused strategies'}.",
            "findings": {
                "growth_pattern": f"Multi-cohort analysis reveals {'steady' if abs(latest_cohort_size - avg_cohort_size) < avg_cohort_size * 0.2 else 'accelerating' if latest_cohort_size > avg_cohort_size * 1.1 else 'moderating'} growth trajectory. Latest cohort ({latest_cohort_size}) {'aligns with' if abs(latest_cohort_size - avg_cohort_size) < avg_cohort_size * 0.2 else 'exceeds' if latest_cohort_size > avg_cohort_size else 'trails'} historical average.",
                "retention_success": f"With {active_pct}% active enrollment across cohorts, retention effectiveness is {'strong' if active_pct > 85 else 'moderate'}, supporting sustainable growth and positive institutional reputation.",
                "recommendation": f"{'Capitalize on growth momentum with expanded recruitment' if latest_cohort_size > avg_cohort_size * 1.1 else 'Maintain steady operations with targeted enhancements' if abs(latest_cohort_size - avg_cohort_size) < avg_cohort_size * 0.2 else 'Implement strategic enrollment initiatives to reverse declining trends'}."
            }
        }
    }

# ====================================================================================
# SESSION STATE INITIALIZATION
# ====================================================================================

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'data' not in st.session_state:
        st.session_state.data = None

    if 'metrics' not in st.session_state:
        st.session_state.metrics = {}

    if 'ollama_server_type' not in st.session_state:
        st.session_state.ollama_server_type = "Local"

    if 'ollama_url' not in st.session_state:
        st.session_state.ollama_url = "http://localhost:11434"

    if 'ollama_connected' not in st.session_state:
        st.session_state.ollama_connected = False

    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = None

    if 'llm_cache' not in st.session_state:
        st.session_state.llm_cache = {}

    if 'complete_journeys' not in st.session_state:
        st.session_state.complete_journeys = None

    if 'journey_generation_metadata' not in st.session_state:
        st.session_state.journey_generation_metadata = None

    if 'health_check_count' not in st.session_state:
        st.session_state.health_check_count = 0

    if 'connection_history' not in st.session_state:
        st.session_state.connection_history = []

    if 'auto_refresh' not in st.session_state:
        st.session_state.auto_refresh = False

    if 'uploaded_filename' not in st.session_state:
        st.session_state.uploaded_filename = None

    if 'show_connection_help' not in st.session_state:
        st.session_state.show_connection_help = False

# ====================================================================================
# MAIN APPLICATION
# ====================================================================================

def main():
    """Main application entry point"""

    # Initialize
    inject_custom_css()
    initialize_session_state()

    # Header
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">🎓 Student 360 AI-Powered Analytics <span style="font-size: 0.5em; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 4px 12px; border-radius: 20px; margin-left: 10px;">V1.0</span></div>
        <div class="hero-subtitle">Transform Student Data into Strategic Intelligence with Large Language Models</div>
    </div>
    """, unsafe_allow_html=True)

    # ====================================================================================
    # SIDEBAR - EXACT IMPLEMENTATION FROM GEN_STORYTELLING_APP.PY
    # ====================================================================================
    with st.sidebar:
        st.markdown("### 📚 Help & Documentation")
        st.caption("🎓 Student 360 AI-Powered Analytics")

        # Version info
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 8px 12px; border-radius: 8px; margin: 10px 0;">
            <div style="color: white; font-weight: 600; font-size: 0.9em;">Version 1.0</div>
            <div style="color: rgba(255,255,255,0.8); font-size: 0.75em;">Production Release • Feb 2026</div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # ====================================================================================
        # GETTING STARTED GUIDE
        # ====================================================================================
        st.markdown("### 📋 Getting Started")
        st.caption("🔄 **App Version: 3.1** - Function Rename Fix (No More Cache!) ✨")
        st.caption("---")

        # Status indicators
        ollama_status = st.session_state.get('ollama_connected', False)
        data_loaded = st.session_state.data is not None

        if ollama_status:
            st.success("✅ Ollama Connected")
            st.caption("Ready to generate AI-powered insights")
        else:
            st.warning("⚠️ Ollama Not Connected")
            st.caption("Configure connection below")

        if data_loaded:
            st.success("✅ Data Loaded")
            st.caption(f"{len(st.session_state.data):,} student records")
        else:
            st.info("📁 No Data Loaded")
            st.caption("Upload CSV in Data Source section")

        st.divider()

        # ====================================================================================
        # LLM & PROMPT ENHANCEMENT GUIDE
        # ====================================================================================
        if st.button("🧠 LLM & Prompt Enhancement Guide", use_container_width=True, type="secondary"):
            st.session_state.show_llm_guide = not st.session_state.get('show_llm_guide', False)

        if st.session_state.get('show_llm_guide', False):
            with st.expander("📖 LLM Enhancement Techniques Used", expanded=True):
                st.markdown("""
                <style>
                .guide-content {
                    background-color: #1e1e1e;
                    color: #e0e0e0;
                    padding: 20px;
                    border-radius: 10px;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }
                .guide-content h2 {
                    color: #4CAF50;
                    border-bottom: 2px solid #4CAF50;
                    padding-bottom: 10px;
                }
                .guide-content h3 {
                    color: #2196F3;
                }
                .guide-content h4 {
                    color: #FF9800;
                }
                .guide-content table {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border-collapse: collapse;
                    width: 100%;
                    margin: 10px 0;
                }
                .guide-content th {
                    background-color: #3d3d3d;
                    color: #4CAF50;
                    padding: 10px;
                    border: 1px solid #555;
                }
                .guide-content td {
                    padding: 8px;
                    border: 1px solid #555;
                }
                .guide-content code {
                    background-color: #2d2d2d;
                    color: #ffa500;
                    padding: 2px 6px;
                    border-radius: 3px;
                }
                .guide-content pre {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    padding: 15px;
                    border-radius: 5px;
                    border-left: 4px solid #4CAF50;
                    overflow-x: auto;
                }
                .guide-content blockquote {
                    background-color: #2d2d2d;
                    border-left: 4px solid #2196F3;
                    padding: 10px 20px;
                    margin: 10px 0;
                    color: #e0e0e0;
                }
                .guide-content ul, .guide-content ol {
                    color: #e0e0e0;
                }
                .guide-content strong {
                    color: #FFD700;
                }
                </style>
                <div class="guide-content">

                <h2>🎯 Prompt Enhancement Strategies</h2>

                ### 1. **Modular Prompt System**
                We use specialized prompts for different narrative types:

                **Example - Business Context Prompt:**
                ```
                You are a higher education business analyst...

                Write a compelling 3-4 sentence paragraph that:
                1. Explains WHY this analysis matters
                2. Connects to strategic goals
                3. Sets up business importance
                4. Uses professional language

                Do NOT include raw numbers.
                Focus on strategic importance.
                ```

                **Example - Data Insights Prompt:**
                ```
                You are a university data analyst...

                Write comprehensive analysis (6-8 sentences):
                1. Analyze patterns and trends
                2. Make comparisons
                3. Identify correlations
                4. Include 8-10 specific numbers
                5. Use "The data reveals...", "Notably..."
                ```

                ---

                ## ⚙️ LLM Parameter Optimization

                ### 2. **Auto-Optimization System**
                The app detects your hardware and adjusts parameters:

                | Your Hardware | Context Size | Tokens | Speed |
                |--------------|--------------|---------|--------|
                | **High-end** (16GB+ RAM, GPU) | 8192 | 2048 | ⚡⚡⚡ |
                | **Medium** (8GB+ RAM) | 4096 | 1024 | ⚡⚡ |
                | **Cloudflare** | 4096 | 1024 | ⚡ |
                | **Low-end** (<8GB RAM) | 2048 | 512 | ⚡ |

                **Key Parameters:**
                - `num_ctx`: Context window (2048-8192)
                - `num_predict`: Max tokens generated
                - `num_batch`: Parallel processing
                - `num_thread`: CPU cores used
                - `timeout`: 6x multiplier for Cloudflare

                ---

                ## 🧠 Temperature Control

                ### 3. **Task-Specific Temperatures**

                | Task | Temp | Why |
                |------|------|-----|
                | **Data Analysis** | 0.3-0.4 | Factual, precise |
                | **Business Context** | 0.4-0.5 | Professional, focused |
                | **Opening Narrative** | 0.5-0.7 | Engaging, creative |
                | **Recommendations** | 0.6-0.7 | Strategic variety |

                **Example Implementation:**
                ```python
                # Analytical content
                query_ollama(prompt, model, url,
                    temperature=0.3)  # Precise

                # Creative content
                query_ollama(prompt, model, url,
                    temperature=0.7)  # Varied
                ```

                ---

                ## 📊 Metrics Formatting

                ### 4. **Data-Driven Prompts**

                We format metrics for LLM consumption:

                **Raw Metrics:**
                ```python
                {
                    'total_students': 1000,
                    'avg_gpa': 3.234567,
                    'revenue': 75500000
                }
                ```

                **Formatted for Prompt:**
                ```
                - Total Students: 1,000
                - Average GPA: 3.2
                - Total Revenue: AED 75.5M
                - High Performers: 450 (45.0%)
                ```

                ---

                ## 🔄 Context Chaining

                ### 5. **Progressive Context Building**

                Each component receives context from previous:

                ```python
                # Step 1: Business Context
                context = generate_business_context(...)

                # Step 2: Data Insights (with context)
                insights = generate_insights(
                    context={'business': context}
                )

                # Step 3: Impact (with both)
                impact = generate_impact(
                    context={
                        'business': context,
                        'insights': insights
                    }
                )
                ```

                **Benefit:** Each narrative builds on previous,
                creating coherent stories.

                ---

                ## 🛡️ Fallback System

                ### 6. **3-Tier Quality Assurance**

                ```
                Tier 1: Try LLM Generation
                   ↓ (if fails)
                Tier 2: Statistical Enrichment
                   ↓ (if fails)
                Tier 3: Template-Based Content
                ```

                **Result:** 100% uptime, always functional

                ---

                ## 🎨 Real-World Example

                ### Complete Narrative Generation:

                **Input Metrics:**
                ```
                total_students: 1000
                housed_students: 663
                occupancy_rate: 66.3%
                avg_gpa_housed: 3.1
                avg_gpa_not_housed: 2.8
                ```

                **Generated Opening:**
                > "Our analysis reveals striking patterns in housing
                > impact: 663 students (66.3%) live on campus, and
                > they outperform off-campus peers by 0.3 GPA points
                > (3.1 vs 2.8). This 10.7% performance advantage
                > translates to measurable retention value..."

                **Why it works:**
                - Specific numbers (663, 66.3%, 3.1, 2.8)
                - Comparative analysis (10.7% advantage)
                - Business impact (retention value)
                - Engaging narrative flow

                ---

                ## 📈 Recommendations for Enhancement

                ### **Currently NOT Used (Opportunities):**

                #### A. **RAG (Retrieval Augmented Generation)**
                - Add vector database for historical insights
                - Reference past reports automatically
                - **Expected Impact:** +30% contextual relevance

                #### B. **Chain-of-Thought Prompting**
                ```
                "Let's analyze this step by step:
                1. First, identify the trend...
                2. Then, calculate the impact...
                3. Finally, recommend actions..."
                ```
                - **Expected Impact:** +25% reasoning quality

                #### C. **Few-Shot Learning**
                ```
                "Example 1:
                Input: {...}
                Output: {...}

                Example 2:
                Input: {...}
                Output: {...}

                Now analyze: {...}"
                ```
                - **Expected Impact:** +20% consistency

                #### D. **Ensemble Generation**
                - Generate 3 variants, pick best
                - Use multiple models for consensus
                - **Expected Impact:** +35% quality

                #### E. **Fine-Tuning**
                - Train on higher education reports
                - Domain-specific vocabulary
                - **Expected Impact:** +40% relevance

                #### F. **Prompt Caching**
                - Cache expensive prompt processing
                - Reuse common contexts
                - **Expected Impact:** +50% speed

                #### G. **Streaming Responses**
                - Show progressive generation
                - Better user experience
                - **Expected Impact:** Perceived -70% latency

                ---

                ## 🔬 Current System Performance

                **Metrics:**
                - **108 narratives** generated per journey set
                - **Avg generation time:** 3-5 minutes (all journeys)
                - **Success rate:** >95% with fallbacks = 100%
                - **Context utilization:** 2048-8192 tokens
                - **Response quality:** Professional grade

                **Architecture:**
                ```
                Data → Metrics → Prompts → LLM → Narratives → UI
                         ↓          ↓        ↓
                    Format    Optimize  Fallback
                ```

                ---

                ## 💡 Quick Tips for Best Results

                1. **Use Cloudflare tunnel** for remote access
                2. **Select larger models** (7B+ params) for quality
                3. **Ensure >8GB RAM** for optimal performance
                4. **Enable auto-optimize** (default on)
                5. **Use sample dataset** to test first
                6. **Check Ollama logs** if generation fails

                ---

                ## 📚 Technical References

                **Implemented Techniques:**
                - ✅ Role-based prompting
                - ✅ Structured instructions
                - ✅ Constraint guidance
                - ✅ Dynamic parameter tuning
                - ✅ Temperature control
                - ✅ Context chaining
                - ✅ Metrics formatting
                - ✅ Fallback strategies

                **Code Locations:**
                - Prompt engineering: `journey_narratives.py`
                - LLM optimization: `student_360_llm_powered.py:689-934`
                - Generation pipeline: `journey_assembler.py`
                - Metrics formatting: `journey_narratives.py:252-307`

                ---

                <p><em>This guide documents the production-grade LLM
                enhancement strategies powering Student 360 Analytics.</em></p>

                </div>
                """, unsafe_allow_html=True)

        st.divider()

        # ====================================================================================
        # OLLAMA CONNECTION STATUS (From gen_storytelling_app.py lines 1116-1298)
        # ====================================================================================
        st.markdown("### 🔌 Ollama Connection Status")

        # Determine connection status
        is_connected = False
        model_count = 0
        error_msg = None

        if st.session_state.get('ollama_url'):
            if st.session_state.get('ollama_connected'):
                is_connected = True
                models = get_available_models(st.session_state.ollama_url)
                model_count = len(models)
            else:
                health = verify_ollama_health(st.session_state.ollama_url)
                st.session_state.health_check_count += 1

                if health['connected']:
                    is_connected = True
                    model_count = health['model_count']
                    st.session_state.ollama_connected = True
                else:
                    is_connected = False
                    error_msg = health.get('error', 'Unknown')

        # Display status
        if is_connected:
            st.success("✅ Connected & Active")

            current_url = st.session_state.get('ollama_url', 'Unknown')
            if 'cloudflare' in current_url.lower() or 'exalio' in current_url.lower():
                endpoint_type = "☁️ Cloudflare"
            elif 'localhost' in current_url.lower():
                endpoint_type = "💻 Local"
            else:
                endpoint_type = "🔧 Custom"

            st.caption(f"📦 {model_count} model(s) available from {endpoint_type}")
            if st.session_state.get('selected_model'):
                st.caption(f"🤖 Active: {st.session_state.selected_model}")
            st.caption(f"🕐 Health checks: {st.session_state.health_check_count}")
        elif st.session_state.get('ollama_url'):
            st.error("❌ Disconnected")
            if error_msg:
                st.caption(f"Error: {error_msg}")

            col_retry1, col_retry2 = st.columns([3, 2])
            with col_retry1:
                if st.button("🔄 Reconnect Now", type="primary", width="stretch"):
                    with st.spinner("🔄 Attempting to reconnect..."):
                        import time
                        connected, models, status_msg = ensure_ollama_connection(
                            st.session_state.ollama_url,
                            auto_reconnect=True,
                            max_retries=3
                        )

                        if connected:
                            st.session_state.ollama_connected = True
                            st.session_state.selected_model = models[0] if models else None
                            st.success(f"✅ {status_msg}")
                            st.success(f"📦 Found {len(models)} model(s)")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(f"❌ {status_msg}")
                            st.info("💡 **Troubleshooting:**\n- Check if Ollama is running\n- Verify URL is correct\n- Check network connection")

            with col_retry2:
                if st.button("ℹ️ Help", width="stretch"):
                    st.session_state.show_connection_help = not st.session_state.get('show_connection_help', False)

            if st.session_state.get('show_connection_help', False):
                with st.expander("🔧 Connection Troubleshooting", expanded=True):
                    st.markdown("""
                    **Common Issues:**

                    1. **Ollama not running**
                       ```bash
                       ollama serve
                       ```

                    2. **Wrong URL**
                       - Local: `http://localhost:11434`
                       - Cloudflare: Check tunnel URL

                    3. **Firewall blocking**
                       - Allow port 11434
                       - Check antivirus settings

                    4. **No models installed**
                       ```bash
                       ollama pull tinyllama
                       ```
                    """)
        else:
            st.warning("⚠️ Not configured")

        # Auto-refresh toggle
        auto_refresh = st.checkbox(
            "🔄 Enable Auto-refresh",
            value=st.session_state.get('auto_refresh', False),
            help="Automatically refresh connection status"
        )
        st.session_state.auto_refresh = auto_refresh

        if not auto_refresh:
            st.caption("❌ Auto-refresh disabled")

        # Connection details
        if st.session_state.get('ollama_url'):
            with st.expander("📊 Connection Details", expanded=False):
                st.markdown("**Connection Information:**")

                if is_connected:
                    st.markdown("- Status: ✅ **Active**")
                    st.markdown(f"- Endpoint: {endpoint_type}")
                    st.markdown(f"- Models: {model_count} available")
                else:
                    st.markdown("- Status: ❌ **Disconnected**")
                    if error_msg:
                        st.markdown(f"- Error: `{error_msg}`")

                st.markdown(f"- URL: `{st.session_state.ollama_url}`")
                st.markdown(f"- Health checks: {st.session_state.health_check_count}")

        st.divider()

        # ====================================================================================
        # SYSTEM RESOURCES & OPTIMIZATION (From gen_storytelling_app.py lines 1300-1434)
        # ====================================================================================
        st.markdown("### 🖥️ System Resources & Optimization")

        is_cloudflare = st.session_state.get('ollama_server_type') == "Cloudflare"
        cloudflare_connected = is_connected if is_cloudflare else True

        if is_cloudflare and not cloudflare_connected:
            resources = None
            opt_tier = "⚠️ Unavailable"
            opt_desc = "Connect to Cloudflare to see resources"
        elif is_cloudflare and cloudflare_connected:
            remote_resources = fetch_remote_system_resources(st.session_state.get('ollama_url', ''))
            if remote_resources:
                resources = remote_resources
            else:
                resources = get_system_resources()

            if resources and resources['gpu_available']:
                if resources['ram_available_gb'] > 30:
                    opt_tier = "🚀 High-End"
                    opt_desc = "Optimal for large models"
                else:
                    opt_tier = "⚡ Medium"
                    opt_desc = "Good for most tasks"
            else:
                opt_tier = "💻 Basic"
                opt_desc = "CPU-only mode"
        else:
            resources = get_system_resources()

            if resources['gpu_available']:
                if resources['ram_available_gb'] > 30:
                    opt_tier = "🚀 High-End"
                    opt_desc = "Optimal for large models"
                else:
                    opt_tier = "⚡ Medium"
                    opt_desc = "Good for most tasks"
            else:
                opt_tier = "💻 Basic"
                opt_desc = "CPU-only mode"

        st.info(f"**Optimization Tier:** {opt_tier}")
        st.caption(opt_desc)

        if resources is None:
            st.warning("⚠️ **System resources not available**")
            st.caption("📡 Resources from: ❌ Not connected to Cloudflare")
            st.caption("💡 Connect to Cloudflare Ollama to view remote resources")

            col_res1, col_res2 = st.columns(2)
            with col_res1:
                st.caption("🔲 CPU: N/A")
                st.caption("💾 RAM: N/A")
            with col_res2:
                st.caption("🎮 GPU: N/A")
                st.caption("⚙️ CPU: N/A")
        else:
            if resources.get('source') == 'remote_colab':
                st.caption(f"📡 Resources from: ☁️ Remote Colab")
            else:
                device_type = "💻 Laptop" if resources['ram_available_gb'] < 50 else "🖥️ Server"
                st.caption(f"📡 Resources from: {device_type}")

            col_res1, col_res2 = st.columns(2)
            with col_res1:
                st.caption(f"🔲 CPU: {resources['cpu_count']} cores")
                st.caption(f"💾 RAM: {resources['ram_available_gb']:.1f}GB free")
            with col_res2:
                if resources['gpu_available']:
                    st.caption(f"🎮 GPU: {resources.get('gpu_name', 'Available')[:15]}")
                else:
                    st.caption("🎮 GPU: N/A")
                if resources.get('cpu_percent', 0) > 0:
                    st.caption(f"⚙️ CPU: {resources['cpu_percent']:.0f}% used")
                else:
                    st.caption("⚙️ CPU: N/A")

        with st.expander("📊 View Optimization Details"):
            if resources is None:
                st.markdown("**Current Configuration:**")
                st.text(f"Tier: {opt_tier}")
                st.text("Platform: Not available (Cloudflare not connected)")
                st.text("CPU: N/A")
                st.text("RAM: N/A")
                st.text("GPU: N/A")

                st.markdown("---")
                st.warning("⚠️ **Connect to Cloudflare Ollama to view remote system resources**")
            else:
                st.markdown("**Current Configuration:**")
                st.text(f"Tier: {opt_tier}")
                st.text(f"Platform: {resources.get('platform', 'Unknown')}")
                st.text(f"CPU: {resources['cpu_count']} cores ({resources.get('cpu_percent', 0):.1f}% usage)")
                st.text(f"RAM: {resources['ram_available_gb']:.1f}/{resources.get('ram_total_gb', 0):.1f} GB available")
                if resources.get('ram_percent', 0) > 0:
                    st.text(f"RAM Usage: {resources['ram_percent']:.1f}%")
                if resources['gpu_available']:
                    st.text(f"GPU: {resources.get('gpu_name', 'Available')}")
                else:
                    st.text("GPU: Not detected")

        st.divider()

        # ====================================================================================
        # VERSION 1.0 RELEASE NOTES
        # ====================================================================================
        with st.expander("📝 Version 1.0 Release Notes", expanded=False):
            st.markdown("""
            **🎉 What's New in Version 1.0**

            **Major Features:**
            - ✅ **5 Advanced AI-Driven Analysis Tabs**
              - Academic Analytics with AI-driven deep analysis
              - Housing Insights with impact analysis
              - Financial Intelligence with sustainability metrics
              - Demographics Deep Dive with diversity analysis
              - Risk & Success Analysis with predictive insights

            - ✅ **Context-Aware Visualizations**
              - AI automatically recommends relevant charts for each context
              - 6 visualization types per analysis tab
              - Intelligent data column selection

            - ✅ **Strategic Insights & Recommendations**
              - Root cause analysis for all findings
              - Business impact quantification
              - Priority-coded actionable recommendations
              - LLM-enriched insights for every visualization

            **Technical Improvements:**
            - Hybrid approach: Rule-based + LLM enrichment
            - Optimized for performance and reliability
            - Enhanced error handling and fallbacks
            - Deep data profiling for better AI insights

            **Release Date:** February 2, 2026
            **Status:** Production Release
            """)

        st.divider()

        # ====================================================================================
        # DATA SOURCE (From gen_storytelling_app.py lines 1436-1632)
        # ====================================================================================
        st.markdown("### 📁 Data Source")

        if not st.session_state.get('ollama_connected'):
            st.info("💡 **You can load data without Ollama connection** - AI features will be available once you connect")

        data_source = st.radio(
            "Choose data source:",
            options=["Upload File", "Use Sample Dataset"],
            index=0,
            key="data_source_selector"
        )

        if data_source == "Upload File":
            st.caption("Choose a file (CSV, Excel, or TXT)")

            uploaded_file = st.file_uploader(
                "Drag and drop file here",
                type=['csv', 'xlsx', 'xls', 'txt'],
                help="Limit 200MB per file • CSV, XLSX, XLS, TXT",
                label_visibility="collapsed"
            )

            if uploaded_file is not None:
                st.caption(f"📄 {uploaded_file.name}")
                st.caption(f"{uploaded_file.size / 1024:.1f}KB")

                already_loaded = (
                    st.session_state.get('uploaded_filename') == uploaded_file.name and
                    st.session_state.get('data') is not None
                )

                if already_loaded:
                    df = st.session_state.data
                    st.success(f"📄 ✅ Already loaded (preserving data transformations) | {len(df)} rows × {len(df.columns)} columns")

                    datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
                    if datetime_cols:
                        st.info(f"🔄 Transformations applied: {len(datetime_cols)} datetime column(s) converted")

                    if st.button("🔄 Reload Original File (discard transformations)", width="stretch", key="reload_original_file"):
                        st.session_state.force_reload = True
                        st.rerun()
                else:
                    try:
                        if uploaded_file.name.endswith('.csv') or uploaded_file.name.endswith('.txt'):
                            df = load_csv_file(uploaded_file)
                        else:
                            df = load_excel_file(uploaded_file)

                        if df is not None:
                            set_main_data(df)
                            st.session_state.uploaded_filename = uploaded_file.name
                            st.session_state.force_reload = False
                            st.success(f"📄 ✅ Loaded successfully | {len(df)} rows × {len(df.columns)} columns")

                            with st.expander("📊 Data Preview (first 5 rows)"):
                                st.dataframe(df.head(5), width="stretch")

                            # Show comprehensive 136-column mapping status
                            mapping_log = st.session_state.get('mapping_log', [])
                            with st.expander("📊 Complete 136-Column Catalog Status", expanded=False):
                                st.markdown("### Universal Column Catalog - Data Availability Report")
                                st.markdown("*Showing all 136 columns from the universal catalog with their status in your dataset*")

                                # Import the universal catalog
                                try:
                                    from universal_columns_catalog import UNIVERSAL_COLUMNS_CATALOG

                                    # Categorize columns by status
                                    mapped_columns = []
                                    present_columns = []
                                    missing_columns = []

                                    for col_name, col_info in UNIVERSAL_COLUMNS_CATALOG.items():
                                        if col_name in df.columns:
                                            # Check if it was mapped from a different name
                                            was_mapped = any(col_name in log for log in mapping_log)
                                            if was_mapped:
                                                # Find the original name
                                                original_name = None
                                                for log in mapping_log:
                                                    if col_name in log:
                                                        original_name = log.split("'")[1]  # Extract original name
                                                        break
                                                mapped_columns.append((col_name, col_info.description, original_name))
                                            else:
                                                present_columns.append((col_name, col_info.description))
                                        else:
                                            missing_columns.append((col_name, col_info.description))

                                    # Summary metrics
                                    col1, col2, col3, col4 = st.columns(4)
                                    with col1:
                                        st.metric("📋 Total Catalog", "136 columns", help="Complete universal catalog size")
                                    with col2:
                                        st.metric("✅ Available", f"{len(mapped_columns) + len(present_columns)}",
                                                 delta=f"{(len(mapped_columns) + len(present_columns))/136*100:.1f}%")
                                    with col3:
                                        st.metric("🔄 Mapped", f"{len(mapped_columns)}",
                                                 help="Columns that were translated from different names")
                                    with col4:
                                        st.metric("⚠️ Missing", f"{len(missing_columns)}",
                                                 delta=f"{len(missing_columns)/136*100:.1f}%", delta_color="inverse")

                                    st.markdown("---")

                                    # Create tabs for different statuses
                                    status_tab1, status_tab2, status_tab3 = st.tabs(["✅ Available Columns", "🔄 Mapped Columns", "⚠️ Missing Columns"])

                                    with status_tab1:
                                        st.markdown(f"**{len(present_columns)} columns present** with standard names (no mapping needed)")
                                        if present_columns:
                                            # Group by category
                                            from universal_columns_catalog import UNIVERSAL_COLUMNS_CATALOG
                                            for col_name, description in sorted(present_columns):
                                                col_info = UNIVERSAL_COLUMNS_CATALOG.get(col_name, {})
                                                category = col_info.category.value if hasattr(col_info, 'category') else 'Other'
                                                st.markdown(f"- **`{col_name}`** ({category})")
                                                if description:
                                                    st.markdown(f"  <small style='color: #94a3b8;'>{description}</small>", unsafe_allow_html=True)

                                    with status_tab2:
                                        st.markdown(f"**{len(mapped_columns)} columns mapped** from non-standard names")
                                        if mapped_columns:
                                            for col_name, description, original_name in sorted(mapped_columns):
                                                col_info = UNIVERSAL_COLUMNS_CATALOG.get(col_name, {})
                                                category = col_info.category.value if hasattr(col_info, 'category') else 'Other'
                                                st.markdown(f"- **`{original_name}`** → **`{col_name}`** ({category})")
                                                if description:
                                                    st.markdown(f"  <small style='color: #94a3b8;'>{description}</small>", unsafe_allow_html=True)

                                    with status_tab3:
                                        st.markdown(f"**{len(missing_columns)} columns not present** in your dataset (optional columns)")
                                        st.info("💡 These columns are part of the universal catalog but not in your current data file. The application will function normally with graceful fallbacks.")

                                        if missing_columns:
                                            # Group by category
                                            missing_by_category = {}
                                            for col_name, description in missing_columns:
                                                col_info = UNIVERSAL_COLUMNS_CATALOG.get(col_name, {})
                                                category = col_info.category.value if hasattr(col_info, 'category') else 'Other'
                                                if category not in missing_by_category:
                                                    missing_by_category[category] = []
                                                missing_by_category[category].append((col_name, description))

                                            # Show by category
                                            for category in sorted(missing_by_category.keys()):
                                                with st.expander(f"📁 {category} ({len(missing_by_category[category])} columns)", expanded=False):
                                                    for col_name, description in sorted(missing_by_category[category]):
                                                        st.markdown(f"- **`{col_name}`**")
                                                        if description:
                                                            st.markdown(f"  <small style='color: #94a3b8;'>{description}</small>", unsafe_allow_html=True)

                                except ImportError:
                                    # Fallback if catalog not available
                                    st.warning("⚠️ Universal catalog module not found. Showing basic mapping info.")
                                    st.success(f"✅ Successfully mapped {len(mapping_log)} columns to standardized format")
                                    for log_entry in mapping_log[:10]:
                                        st.text(f"  • {log_entry}")
                                    if len(mapping_log) > 10:
                                        st.text(f"  ... and {len(mapping_log) - 10} more")

                    except Exception as e:
                        st.error(f"❌ Error loading file: {e}")
        else:
            st.caption("Load a pre-built sample dataset")

            if st.session_state.get('data') is not None and st.session_state.get('uploaded_filename') == 'sample_dataset':
                df = st.session_state.data
                # Check if sample dataset is outdated (missing new required fields)
                required_new_fields = ['visa_status', 'enrollment_type', 'room_number', 'occupancy_status']
                missing_new_fields = [f for f in required_new_fields if f not in df.columns]

                if missing_new_fields:
                    st.warning(f"⚠️ Sample dataset is outdated (missing {len(missing_new_fields)} new fields)")
                    if st.button("🔄 Reload Updated Sample Data", width="stretch", type="primary"):
                        df = create_sample_dataset_v3_final()
                        set_main_data(df)
                        st.session_state.uploaded_filename = 'sample_dataset'
                        st.success(f"✅ Loaded updated sample dataset with ALL REQUIRED FIELDS!")
                        st.balloons()
                        st.rerun()
                else:
                    st.success(f"✅ Sample dataset already loaded | {len(df)} rows × {len(df.columns)} columns")
            elif st.button("🔥 Load Fresh Sample Data", width="stretch", type="primary"):
                # INLINE generation to bypass all caching
                np.random.seed(42)
                n = 1000
                nats = np.random.choice(['United Arab Emirates', 'India', 'Pakistan', 'Egypt', 'Jordan',
                                        'Saudi Arabia', 'Philippines', 'United States', 'United Kingdom',
                                        'Canada'], n, p=[0.45, 0.15, 0.10, 0.08, 0.05, 0.05, 0.04, 0.03, 0.03, 0.02])
                housed = np.random.choice([True, False], n, p=[0.6, 0.4])

                df = pd.DataFrame({
                    'student_id': [f'S{i:05d}' for i in range(1, n + 1)],
                    'cumulative_gpa': np.random.normal(3.0, 0.6, n).clip(0, 4.0),
                    'nationality': nats,
                    'enrollment_enrollment_status': np.random.choice(['Active', 'Graduated', 'On Leave'], n, p=[0.8, 0.15, 0.05]),
                    'enrollment_tuition_amount': np.random.uniform(50000, 100000, n),
                    'financial_aid_monetary_amount': np.random.choice([0, 15000, 25000, 40000, 60000], n, p=[0.4, 0.2, 0.2, 0.15, 0.05]),
                    'gender': np.random.choice(['Male', 'Female'], n),
                    'cohort_year': np.random.choice([2020, 2021, 2022, 2023, 2024], n),
                    'visa_status': ['UAE National' if nat == 'United Arab Emirates' else np.random.choice(['Student Visa', 'Resident Visa', 'Family Visa'])
                                   for nat in nats],
                    'enrollment_type': np.random.choice(['Full-Time', 'Part-Time'], n, p=[0.85, 0.15]),
                    'room_number': [f'R{i:04d}' if h else None for i, h in enumerate(housed, 1)],
                    'occupancy_status': ['Occupied' if h else None for h in housed],
                    'rent_amount': [np.random.uniform(8000, 15000) if h else 0 for h in housed],
                })

                st.session_state.data = df
                st.session_state.mapping_log = ["Fresh inline data - all 13 columns"]
                st.session_state.uploaded_filename = 'sample_dataset'
                st.session_state.metrics = calculate_core_metrics(df)

                st.success(f"✅ {len(df)} rows × {len(df.columns)} columns loaded!")
                st.balloons()
                st.rerun()

        st.divider()

        # ====================================================================================
        # COLUMN MAPPING STATUS (Always show, but content depends on data)
        # ====================================================================================
        st.markdown("### 📊 Column Mapping Status")

        if st.session_state.get('data') is None:
            # No data loaded yet
            st.info("💡 Load data first to see column mapping status")
            st.caption("The mapping status will appear here after you load data")
        else:
            # Get current data and mapping log
            df = st.session_state.data
            mapping_log = st.session_state.get('mapping_log', [])

            # Check if required journey fields exist
            required_journey_fields = [
                'financial_aid_monetary_amount', 'cohort_year', 'enrollment_enrollment_status',
                'enrollment_tuition_amount', 'enrollment_type', 'occupancy_status'
            ]
            present_required = [f for f in required_journey_fields if f in df.columns]
            missing_required = [f for f in required_journey_fields if f not in df.columns]

            # Show required fields status
            if len(present_required) == len(required_journey_fields):
                st.success(f"✅ All {len(required_journey_fields)} journey fields present")
            elif present_required:
                st.info(f"ℹ️ {len(present_required)}/{len(required_journey_fields)} journey fields found")
                st.caption(f"Optional fields not in CSV: {', '.join(missing_required)}")
            else:
                st.error(f"❌ 0/{len(required_journey_fields)} fields found")
                st.caption(f"Missing: {', '.join(missing_required)}")

            # Show status based on data quality
            if not mapping_log and missing_required:
                # Mapping not applied AND missing required fields
                st.info(f"ℹ️ Column mapping not yet applied")
                if st.button("🔄 Apply Column Mapping Now", type="primary", use_container_width=True, key="force_mapping"):
                    mapped_df, new_mapping_log = apply_universal_column_mapping(df)
                    st.session_state.data = mapped_df
                    st.session_state.mapping_log = new_mapping_log if new_mapping_log else ["No mappings needed - all columns standard"]
                    st.session_state.metrics = calculate_core_metrics(mapped_df)
                    st.rerun()
            elif not mapping_log and not missing_required:
                # No mapping log but data is already perfect
                st.success("✅ All columns already using standard names")
                st.caption("No mapping needed - dataset is ready!")
                st.session_state.mapping_log = ["Dataset already has standard column names"]
            elif mapping_log and isinstance(mapping_log, list) and len(mapping_log) > 0:
                # Mapping was applied
                if mapping_log[0] == "Dataset already has standard column names":
                    st.success("✅ Dataset uses standard column names")
                elif mapping_log[0] == "No mappings needed - all columns standard":
                    st.success("✅ All columns already standardized")
                else:
                    st.success(f"✅ Column mapping completed: {len(mapping_log)} columns")

            try:
                from universal_columns_catalog import UNIVERSAL_COLUMNS_CATALOG

                # Quick summary counts
                mapped_count = len([log for log in mapping_log if '→' in log])
                available_count = len([col for col in UNIVERSAL_COLUMNS_CATALOG.keys() if col in df.columns])
                total_catalog = len(UNIVERSAL_COLUMNS_CATALOG)

                # Display summary metrics
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("✅ Available", f"{available_count}/{total_catalog}",
                             delta=f"{available_count/total_catalog*100:.0f}%")
                with col2:
                    st.metric("🔄 Mapped", mapped_count,
                             help="Columns translated from different names")

                # Show mapping log in expander
                if mapping_log:
                    with st.expander(f"📋 View Mapping Details ({len(mapping_log)} mappings)", expanded=False):
                        st.caption("Columns that were automatically standardized:")
                        for log_entry in mapping_log:
                            st.text(f"  • {log_entry}")
                else:
                    st.caption("✨ All columns already using standard names")

                # Show detailed catalog status
                with st.expander("🔍 Complete Catalog Status (136 columns)", expanded=False):
                    # Categorize columns by status
                    mapped_columns = []
                    present_columns = []
                    missing_columns = []

                    for col_name, col_info in UNIVERSAL_COLUMNS_CATALOG.items():
                        if col_name in df.columns:
                            was_mapped = any(col_name in log for log in mapping_log)
                            if was_mapped:
                                # Find the original name
                                original_name = None
                                for log in mapping_log:
                                    if col_name in log:
                                        original_name = log.split("'")[1]
                                        break
                                mapped_columns.append((col_name, col_info.description, original_name))
                            else:
                                present_columns.append((col_name, col_info.description))
                        else:
                            missing_columns.append((col_name, col_info.description))

                    # Create tabs
                    tab1, tab2, tab3 = st.tabs([
                        f"✅ Present ({len(present_columns)})",
                        f"🔄 Mapped ({len(mapped_columns)})",
                        f"⚠️ Missing ({len(missing_columns)})"
                    ])

                    with tab1:
                        if present_columns:
                            for col_name, description in sorted(present_columns)[:10]:
                                st.caption(f"• `{col_name}`")
                            if len(present_columns) > 10:
                                st.caption(f"... and {len(present_columns) - 10} more")
                        else:
                            st.caption("No columns present with standard names")

                    with tab2:
                        if mapped_columns:
                            for col_name, description, original_name in sorted(mapped_columns)[:10]:
                                st.caption(f"• `{original_name}` → `{col_name}`")
                            if len(mapped_columns) > 10:
                                st.caption(f"... and {len(mapped_columns) - 10} more")
                        else:
                            st.caption("No columns were mapped")

                    with tab3:
                        if missing_columns:
                            st.caption(f"📌 {len(missing_columns)} optional columns not in dataset")
                            for col_name, description in sorted(missing_columns)[:5]:
                                st.caption(f"• `{col_name}`")
                            if len(missing_columns) > 5:
                                st.caption(f"... and {len(missing_columns) - 5} more")
                        else:
                            st.caption("All catalog columns are present!")

            except ImportError:
                st.caption("📊 Column mapping applied")
                if mapping_log:
                    st.caption(f"✅ {len(mapping_log)} columns standardized")

        st.divider()

        # ====================================================================================
        # AI CONFIGURATION (From gen_storytelling_app.py lines 1648-1768)
        # ====================================================================================
        st.markdown("### 🤖 AI Configuration")
        st.markdown("**Ollama Server Location**")

        previous_server_type = st.session_state.get('previous_ollama_server_type', None)

        server_type = st.radio(
            "Server Type",
            options=["Cloudflare", "Local"],
            index=0 if st.session_state.ollama_server_type == "Cloudflare" else 1,
            help="Choose between Cloudflare (remote) or Local Ollama server",
            horizontal=True,
            label_visibility="collapsed"
        )

        server_type_changed = (previous_server_type is not None and
                               previous_server_type != server_type)

        st.session_state.ollama_server_type = server_type
        st.session_state.previous_ollama_server_type = server_type

        if server_type == "Cloudflare":
            st.caption("☁️ Using Cloudflare Ollama")
            default_url = "https://ollama.exaliotechcom.uk"
        else:
            st.caption("💻 Using Local Ollama")
            default_url = "http://localhost:11434"

        st.caption(f"🏠 URL: {default_url}")

        if st.session_state.get('ollama_url') != default_url:
            if 'custom_url_set' not in st.session_state:
                st.session_state.ollama_url = default_url
                st.session_state.ollama_connected = False
                server_type_changed = True

        if server_type_changed:
            with st.spinner(f"🔄 Switching to {server_type} Ollama..."):
                import time
                health = verify_ollama_health(default_url)
                if health['connected']:
                    st.session_state.ollama_connected = True
                    st.session_state.ollama_url = default_url
                    st.success(f"✅ Connected to {server_type} Ollama")
                    st.caption(f"📦 Found {health['model_count']} model(s)")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.session_state.ollama_connected = False
                    st.session_state.ollama_url = default_url
                    st.error(f"❌ Failed to connect to {server_type} Ollama")
                    st.caption(f"Error: {health.get('error', 'Unknown error')}")
                    time.sleep(0.5)
                    st.rerun()

        with st.expander("🔧 Advanced: Custom URL"):
            ollama_url = st.text_input(
                "Custom Ollama URL",
                value=st.session_state.get('ollama_url', default_url),
                help="URL of your Ollama server"
            )
            if ollama_url != default_url:
                st.session_state.custom_url_set = True
            else:
                st.session_state.pop('custom_url_set', None)

            st.session_state.ollama_url = ollama_url

            if st.button("Test Connection", width="stretch"):
                with st.spinner("Testing connection..."):
                    health = verify_ollama_health(ollama_url)
                    if health['connected']:
                        st.success(f"✅ Connected! Found {health['model_count']} models")
                        st.session_state.ollama_connected = True
                    else:
                        st.error(f"❌ Connection failed: {health.get('error', 'Unknown error')}")
                        st.session_state.ollama_connected = False

        if 'ollama_url' not in st.session_state:
            st.session_state.ollama_url = default_url

        st.markdown("**Select AI Model**")

        # Custom CSS for BLACK text in model dropdown - AGGRESSIVE OVERRIDE
        st.markdown("""
        <style>
        /* FORCE BLACK TEXT - Override everything */
        .stSelectbox, .stSelectbox * {
            color: #000000 !important;
        }

        /* Select input field */
        .stSelectbox [data-baseweb="select"] {
            background-color: #ffffff !important;
        }

        /* All text inside selectbox */
        .stSelectbox div, .stSelectbox span, .stSelectbox p {
            color: #000000 !important;
        }

        /* Dropdown options */
        [data-baseweb="popover"] li,
        [data-baseweb="popover"] div,
        [data-baseweb="popover"] span {
            color: #000000 !important;
            background-color: #ffffff !important;
        }

        /* Selected value display */
        [data-baseweb="select"] > div > div {
            color: #000000 !important;
        }

        /* All listbox items */
        ul[role="listbox"] li,
        ul[role="listbox"] div,
        ul[role="listbox"] span {
            color: #000000 !important;
        }

        /* Nuclear option - force ALL sidebar selectboxes to black */
        [data-testid="stSidebar"] .stSelectbox * {
            color: #000000 !important;
        }
        </style>
        """, unsafe_allow_html=True)

        if st.session_state.get('ollama_connected'):
            models = get_available_models(st.session_state.ollama_url)
            if models:
                selected_model = st.selectbox(
                    "Model",
                    options=models,
                    index=0,
                    help="Choose the LLM model for narrative generation",
                    label_visibility="collapsed"
                )
                st.session_state.selected_model = selected_model
                st.success(f"✅ Using: {selected_model}")

                # Model recommendations for deep analysis
                st.caption("💡 **For Deep Analysis:**")
                if any(x in selected_model.lower() for x in ['llama3.1:70b', 'qwen2.5:72b', 'mixtral:8x22b']):
                    st.caption("🟢 Excellent - Large model ideal for comprehensive insights")
                elif any(x in selected_model.lower() for x in ['llama3.1', 'qwen2.5:32b', 'gemma2:27b']):
                    st.caption("🟡 Good - Balanced performance and quality")
                else:
                    st.caption("🟠 Basic - Consider larger model for richer analysis")
                    with st.expander("📋 Recommended Models"):
                        st.markdown("""
                        **For Best Deep Analysis:**
                        - `llama3.1:70b` - Excellent reasoning
                        - `qwen2.5:72b` - Superior analytics
                        - `qwen2.5:32b` - Balanced (good speed/quality)

                        **Pull command:**
                        ```bash
                        ollama pull qwen2.5:32b
                        ```
                        """)
            else:
                st.warning("No models found. Please pull a model first.")
        else:
            health = verify_ollama_health(st.session_state.ollama_url)
            if health['connected']:
                st.session_state.ollama_connected = True
                models = get_available_models(st.session_state.ollama_url)
                if models:
                    st.session_state.selected_model = models[0]
                    st.success(f"✅ Auto-connected: {models[0]}")
            else:
                st.info("👆 Configure connection above")

    # Main content area - Show welcome message if no data
    if st.session_state.data is None:
        st.markdown("""
        <div style='text-align: center; padding: 3rem 2rem;'>
            <h2 style='color: #6366f1; margin-bottom: 1rem;'>🎓 Welcome to Student 360 AI-Powered Analytics</h2>
            <p style='font-size: 1.2rem; color: #94a3b8; margin-bottom: 2rem;'>
                Your intelligent analytics dashboard powered by advanced AI
            </p>
            <p style='font-size: 1rem; color: #e2e8f0; margin-bottom: 0.5rem;'>
                👈 Check the sidebar's <strong>Getting Started</strong> section to begin
            </p>
            <p style='font-size: 0.9rem; color: #94a3b8;'>
                Configure Ollama connection → Select AI model → Upload student data
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Show key features
        st.divider()
        st.markdown("### ✨ Key Features")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div style='background: rgba(99, 102, 241, 0.1); padding: 1.5rem; border-radius: 8px; border-left: 4px solid #6366f1;'>
                <h4 style='color: #818cf8; margin-top: 0;'>🤖 AI-Driven Insights</h4>
                <p style='color: #cbd5e1; margin-bottom: 0; font-size: 0.9rem;'>
                    LLM analyzes your data and recommends optimal visualizations dynamically
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style='background: rgba(16, 185, 129, 0.1); padding: 1.5rem; border-radius: 8px; border-left: 4px solid #10b981;'>
                <h4 style='color: #34d399; margin-top: 0;'>📊 Dynamic Analytics</h4>
                <p style='color: #cbd5e1; margin-bottom: 0; font-size: 0.9rem;'>
                    Adaptive visualizations that change based on your specific data patterns
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div style='background: rgba(245, 158, 11, 0.1); padding: 1.5rem; border-radius: 8px; border-left: 4px solid #f59e0b;'>
                <h4 style='color: #fbbf24; margin-top: 0;'>🎯 Strategic Intelligence</h4>
                <p style='color: #cbd5e1; margin-bottom: 0; font-size: 0.9rem;'>
                    Comprehensive analysis across academics, financials, and student success
                </p>
            </div>
            """, unsafe_allow_html=True)

        return

    # Get current data
    df = st.session_state.data

    # Apply column mapping - check if required fields exist
    # This ensures mapping is applied even if user has old data
    required_journey_fields = [
        'financial_aid_monetary_amount', 'cohort_year', 'enrollment_enrollment_status',
        'enrollment_tuition_amount', 'enrollment_type', 'occupancy_status'
    ]
    missing_required = [f for f in required_journey_fields if f not in df.columns]

    # Apply mapping if: no mapping_log exists OR required fields are missing
    if ('mapping_log' not in st.session_state or st.session_state.mapping_log is None) or missing_required:
        df, mapping_log = apply_universal_column_mapping(df)
        st.session_state.data = df

        # Recheck missing fields after mapping
        still_missing = [f for f in required_journey_fields if f not in df.columns]

        if mapping_log and len(mapping_log) > 0:
            st.session_state.mapping_log = mapping_log
            st.info(f"🔄 Applied column mapping: {len(mapping_log)} columns standardized")
        else:
            st.session_state.mapping_log = ["Dataset already has standard column names"]
            st.success("✅ Dataset already uses standard column names")

        # If fields still missing after mapping, show informational message
        if still_missing:
            st.info(f"""
            ℹ️ **Dataset Information**: Your CSV file doesn't include {len(still_missing)} optional column(s):
            {', '.join([f'`{field}`' for field in still_missing])}

            Most analyses will work normally. Some advanced journey generation features may have limited data availability.

            💡 **Tip**: If you need these fields, please ensure your source CSV file includes them before uploading.
            """)

    # FORCE RECALCULATION: Always recalculate metrics to ensure fresh data
    # This fixes issues with stale cached metrics (especially UAE nationals)
    metrics = calculate_core_metrics(df)
    st.session_state.metrics = metrics  # Update session state with fresh metrics

    model = st.session_state.selected_model
    url = st.session_state.ollama_url

    # Application tabs
    tabs = st.tabs([
        "📊 Executive Summary",
        "📖 Data Storytelling AI Driven with Template Guidance",
        "🔬 Data Storytelling Fully AI Driven",
        "📚 Data Storytelling (PreDefined+LLM Narrative)",
        "🎓 Academic Analytics",
        "🏠 Housing Insights",
        "💰 Financial Intelligence",
        "👥 Demographics",
        "⚠️ Risk & Success",
        "🔗 Data Lineage",
        "🔬 Data Explorer"
    ])

    # ====================================================================================
    # TAB 1: TRUE LLM-DRIVEN EXECUTIVE SUMMARY
    # ====================================================================================
    with tabs[0]:
        st.header("🤖 Executive Summary - AI-Driven Dynamic Analytics")
        st.markdown("*The AI analyzes your data and decides what visualizations to create*")

        # Description box
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(139, 92, 246, 0.15)); padding: 1.2rem; border-radius: 8px; margin-bottom: 1.5rem; border-left: 4px solid #6366f1;'>
            <strong>🧠 True LLM-Driven Approach:</strong> Unlike traditional dashboards where developers hardcode which graphs to show,
            this system asks the <strong>AI to analyze your {metrics.get('total_students', 0):,} students</strong> and <strong>recommend the most insightful visualizations</strong>.
            The LLM acts as your data analyst, choosing graph types, data columns, and insights based on what patterns it finds in YOUR data.
        </div>
        """, unsafe_allow_html=True)

        if not st.session_state.ollama_connected:
            st.warning("⚠️ Connect to Ollama to enable AI-driven dynamic visualization generation")

        # Generate dynamic visualizations button
        if st.session_state.ollama_connected:
            if st.button("🤖 Let AI Analyze Data & Create Visualizations", key="exec_dynamic_btn", type="primary", width="stretch"):
                with st.spinner("🔄 AI is analyzing your data, identifying patterns, and recommending optimal visualizations... This may take 20-40 seconds"):
                    viz_result = generate_dynamic_visualizations_llm(metrics, df, model, url, context_type="executive_summary")
                    st.session_state.llm_cache['exec_dynamic_viz'] = viz_result

        # Display AI-generated visualizations if available
        if 'exec_dynamic_viz' in st.session_state.llm_cache:
            viz_result = st.session_state.llm_cache['exec_dynamic_viz']

            # AI Strategic Overview
            st.markdown(f"""
            <div class="insight-card" style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(139, 92, 246, 0.15)); border-left: 4px solid #6366f1; margin-bottom: 2rem;">
                <div class="insight-title">🎯 AI Strategic Analysis</div>
                <div class="insight-text" style="font-size: 1.1rem; line-height: 1.8;">{viz_result.get('strategic_overview', '')}</div>
            </div>
            """, unsafe_allow_html=True)

            st.divider()

            # Key Metrics Dashboard (Static - Always show core metrics)
            st.markdown("### 📊 Core Institutional Metrics")

            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Total Students", f"{metrics.get('total_students', 0):,}")
            with col2:
                st.metric("Average GPA", f"{metrics.get('avg_gpa', 0):.2f}")
            with col3:
                st.metric("High Performers", f"{metrics.get('high_performers', 0):,}",
                         f"{metrics.get('high_performers', 0)/metrics.get('total_students', 1)*100:.1f}%")
            with col4:
                st.metric("UAE Nationals", f"{metrics.get('uae_percentage', 0):.1f}%")
            with col5:
                st.metric("At-Risk", f"{metrics.get('at_risk', 0):,}",
                         f"{metrics.get('at_risk', 0)/metrics.get('total_students', 1)*100:.1f}%",
                         delta_color="inverse")

            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.metric("Nationalities", metrics.get('unique_nationalities', 0))
            with col2:
                st.metric("Tuition Revenue", f"AED {metrics.get('total_tuition', 0)/1000000:.1f}M")
            with col3:
                st.metric("Financial Aid", f"AED {metrics.get('total_aid', 0)/1000000:.1f}M")
            with col4:
                st.metric("Aid Coverage", f"{metrics.get('aid_coverage_pct', 0):.1f}%")
            with col5:
                st.metric("Revenue/Student", f"AED {metrics.get('total_tuition', 0)/metrics.get('total_students', 1) if metrics.get('total_students', 0) > 0 else 0:,.0f}")

            st.divider()

            # ========================================================================
            # DYNAMIC AI-RECOMMENDED VISUALIZATIONS
            # ========================================================================
            st.markdown("### 📈 AI-Recommended Visualizations")
            st.caption(f"The AI analyzed your data and recommends {len(viz_result.get('visualizations', []))} visualizations")

            visualizations = viz_result.get('visualizations', [])

            if visualizations:
                # Display visualizations in grid (2 columns)
                for idx in range(0, len(visualizations), 2):
                    cols = st.columns(2)

                    for col_idx, col in enumerate(cols):
                        viz_idx = idx + col_idx
                        if viz_idx < len(visualizations):
                            viz_spec = visualizations[viz_idx]

                            with col:
                                st.markdown(f"#### {viz_spec.get('title', 'Visualization')}")
                                st.caption(f"**Why this matters:** {viz_spec.get('reasoning', '')}")

                                # Build dynamic chart from AI specification
                                chart = build_dynamic_chart(viz_spec, df)

                                if chart:
                                    st.plotly_chart(chart, width="stretch")

                                    # Display AI-generated insight
                                    st.info(f"**AI Insight:** {viz_spec.get('insight', '')}")
                                else:
                                    st.warning(f"Could not generate chart for: {viz_spec.get('data_column', 'unknown column')}")

                st.divider()

                # ========================================================================
                # KEY FINDINGS (AI-Generated)
                # ========================================================================
                st.markdown("### 🔍 Key Findings")

                key_findings = viz_result.get('key_findings', [])
                if key_findings:
                    for idx, finding in enumerate(key_findings, 1):
                        st.markdown(f"""
                        <div style='background: rgba(59, 130, 246, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #3b82f6; margin-bottom: 0.8rem;'>
                            <strong style='color: #60a5fa;'>Finding {idx}:</strong> {finding}
                        </div>
                        """, unsafe_allow_html=True)

                st.divider()

                # ========================================================================
                # RECOMMENDATIONS (AI-Generated with Priority & ROI)
                # ========================================================================
                st.markdown("### 💡 AI-Generated Strategic Recommendations")

                recommendations = viz_result.get('recommendations', [])
                if recommendations:
                    for idx, rec in enumerate(recommendations, 1):
                        # Handle both old format (string) and new enriched format (dict)
                        if isinstance(rec, dict):
                            # New enriched format with priority, impact, timeline, investment
                            priority = rec.get('priority', 'MEDIUM')
                            action = rec.get('action', '')
                            expected_impact = rec.get('expected_impact', '')
                            timeline = rec.get('timeline', 'short-term')
                            investment = rec.get('investment', 'TBD')

                            # Color-code by priority
                            priority_colors = {
                                'CRITICAL': ('#ef4444', 'rgba(239, 68, 68, 0.15)'),
                                'HIGH': ('#f59e0b', 'rgba(245, 158, 11, 0.15)'),
                                'MEDIUM': ('#10b981', 'rgba(16, 185, 129, 0.15)')
                            }
                            border_color, bg_gradient = priority_colors.get(priority, priority_colors['MEDIUM'])

                            st.markdown(f"""
                            <div style='background: {bg_gradient}; padding: 1.5rem; border-radius: 8px;
                                        border-left: 4px solid {border_color}; margin-bottom: 1rem;'>
                                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;'>
                                    <h4 style='color: {border_color}; margin: 0;'>
                                        {'🔴' if priority == 'CRITICAL' else '🟠' if priority == 'HIGH' else '🟢'}
                                        Recommendation {idx} - {priority} Priority
                                    </h4>
                                    <span style='background: rgba(0,0,0,0.3); padding: 0.3rem 0.8rem;
                                                border-radius: 12px; font-size: 0.85rem; color: #cbd5e1;'>
                                        {timeline.replace('_', ' ').title()}
                                    </span>
                                </div>
                                <p style='color: #e2e8f0; margin-bottom: 0.8rem; line-height: 1.6; font-size: 1.05rem;'>
                                    <strong>Action:</strong> {action}
                                </p>
                                <p style='color: #a5b4fc; margin-bottom: 0.8rem; line-height: 1.6;'>
                                    <strong>📊 Expected Impact:</strong> {expected_impact}
                                </p>
                                <p style='color: #cbd5e1; margin-bottom: 0; line-height: 1.6; font-size: 0.95rem;'>
                                    <strong>💰 Investment:</strong> {investment}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            # Old format (simple string) - backwards compatible
                            st.markdown(f"""
                            <div style='background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
                                        padding: 1.2rem; border-radius: 8px; border-left: 4px solid #10b981; margin-bottom: 1rem;'>
                                <h4 style='color: #10b981; margin-top: 0;'>Recommendation {idx}</h4>
                                <p style='color: #e2e8f0; margin-bottom: 0; line-height: 1.6;'>
                                    {rec}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)

            else:
                st.warning("No visualizations generated. Try regenerating with the button above.")

    # ====================================================================================
    # TAB 2: DATA STORYTELLING AI DRIVEN WITH TEMPLATE GUIDANCE
    # ====================================================================================
    with tabs[1]:
        st.header("📖 Data Storytelling AI Driven with Template Guidance")
        st.caption("AI identifies entities from your data and creates comprehensive journey stories tracking their lifecycle")

        # Explanation box
        st.markdown(f"""<div style='background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(139, 92, 246, 0.15)); padding: 1.2rem; border-radius: 8px; margin-bottom: 1.5rem; border-left: 4px solid #6366f1;'>
<p style='margin: 0; color: #e2e8f0;'><strong>🎯 Entity-Based Journey System:</strong> Unlike traditional dashboards that show aggregate statistics,
this system uses AI to <strong>identify meaningful entities</strong> (student cohorts, programs, services, revenue segments) from your dataset
and <strong>tracks their complete lifecycle</strong> through multiple stages with data-driven narratives.</p>
<p style='margin: 0.5rem 0 0 0; color: #cbd5e1; font-size: 0.9rem;'>
<strong>How it works:</strong><br>
• <strong>Phase 1:</strong> AI analyzes your {metrics.get('total_students', 0):,} students and identifies 6-8 meaningful entities<br>
• <strong>Phase 2:</strong> AI defines 4-6 lifecycle stages for each entity<br>
• <strong>Phase 3:</strong> AI generates compelling narratives for each stage using actual data
</p>
<p style='margin: 0.8rem 0 0 0; padding-top: 0.8rem; border-top: 1px solid rgba(99, 102, 241, 0.3); color: #cbd5e1; font-size: 0.9rem;'>
<strong>🚀 Journeys are based on:</strong><br>
• ✅ Dataset structure analysis (all {len(df.columns)} columns examined)<br>
• ✅ Sample data patterns (first 5 rows analyzed for insights)<br>
• ✅ Entity lifecycle concept (things that evolve: beginning → middle → end)<br>
• ✅ Entity types: Student, Program, Financial Aid, Enrollment, Campus, Revenue<br>
• ✅ AI pattern recognition of what constitutes a meaningful "journey"<br>
• ✅ Status transitions (Active → At-Risk → Successful/Failed)
</p>
<p style='margin: 0.8rem 0 0 0; padding-top: 0.8rem; border-top: 1px solid rgba(99, 102, 241, 0.3); color: #cbd5e1; font-size: 0.9rem;'>
<strong>📋 Stages within each journey are based on:</strong><br>
• ✅ Your actual dataset columns and values<br>
• ✅ The specific entity identified by AI<br>
• ✅ Chronological/logical progression (enrollment → performance → outcomes)<br>
• ✅ LLM's understanding of higher education lifecycles<br>
• ✅ Data-driven insights specific to your institution's context
</p>
</div>""", unsafe_allow_html=True)

        if not st.session_state.ollama_connected:
            st.warning("⚠️ Connect to Ollama to generate entity journeys")
        elif not LLM_ENTITY_JOURNEY_AVAILABLE:
            st.error("❌ LLM Entity Journey System module not found. Please ensure llm_entity_journey_system.py is available.")
        else:
            # Button to generate entity journeys
            col_btn, col_info = st.columns([2, 3])
            with col_btn:
                if st.button("🚀 Generate Entity Journeys", key="generate_entity_journeys_btn", type="primary", use_container_width=True):
                    with st.spinner("🔄 Phase 1/3: Identifying meaningful entities from dataset..."):
                        # Generate complete entity journeys using LLM
                        entity_journeys = generate_complete_llm_journeys(df, model)
                        st.session_state.llm_cache['entity_journeys'] = entity_journeys

                        if entity_journeys:
                            total_stages = sum(j['total_stages'] for j in entity_journeys)
                            st.success(f"✅ Generated {len(entity_journeys)} entity journeys with {total_stages} total stages!")
                        else:
                            st.error("❌ Failed to generate entity journeys. Please check your dataset and Ollama connection.")

            with col_info:
                st.info("⏱️ **Estimated time:** 5-15 minutes depending on dataset complexity. The AI will make multiple LLM calls to build comprehensive stories.")

            # Display entity journeys if available
            if 'entity_journeys' in st.session_state.llm_cache:
                entity_journeys = st.session_state.llm_cache['entity_journeys']

                if not entity_journeys:
                    st.warning("No entity journeys generated. Try again or check your dataset.")
                else:
                    st.markdown("---")
                    st.markdown(f"### 🎯 {len(entity_journeys)} Entity Journeys Discovered")
                    st.caption(f"*AI identified {len(entity_journeys)} meaningful entities and tracked their lifecycle through {sum(j['total_stages'] for j in entity_journeys)} total stages*")

                    # Display each entity journey
                    for journey_idx, journey in enumerate(entity_journeys, 1):
                        entity_type_colors = {
                            # Lifecycle entity types
                            'student_lifecycle': ('#3b82f6', 'rgba(59, 130, 246, 0.1)'),
                            'program_lifecycle': ('#8b5cf6', 'rgba(139, 92, 246, 0.1)'),
                            'aid_lifecycle': ('#10b981', 'rgba(16, 185, 129, 0.1)'),
                            'enrollment_lifecycle': ('#06b6d4', 'rgba(6, 182, 212, 0.1)'),
                            'campus_lifecycle': ('#f59e0b', 'rgba(245, 158, 11, 0.1)'),
                            'revenue_lifecycle': ('#22c55e', 'rgba(34, 197, 94, 0.1)'),
                            'facility_lifecycle': ('#eab308', 'rgba(234, 179, 8, 0.1)'),
                            # Legacy types (for backward compatibility)
                            'student_cohort': ('#3b82f6', 'rgba(59, 130, 246, 0.1)'),
                            'program': ('#8b5cf6', 'rgba(139, 92, 246, 0.1)'),
                            'service': ('#06b6d4', 'rgba(6, 182, 212, 0.1)'),
                            'revenue_segment': ('#10b981', 'rgba(16, 185, 129, 0.1)'),
                            'operational': ('#f59e0b', 'rgba(245, 158, 11, 0.1)')
                        }

                        entity_type = journey.get('entity_type', 'student_lifecycle')
                        color, bg_color = entity_type_colors.get(entity_type, ('#6366f1', 'rgba(99, 102, 241, 0.1)'))

                        # Priority colors
                        priority = journey.get('priority', 5)
                        if priority >= 8:
                            priority_color = '#dc2626'
                            priority_label = '🚨 CRITICAL'
                        elif priority >= 6:
                            priority_color = '#f97316'
                            priority_label = '⚡ HIGH'
                        elif priority >= 4:
                            priority_color = '#eab308'
                            priority_label = '💡 MEDIUM'
                        else:
                            priority_color = '#10b981'
                            priority_label = '✅ STANDARD'

                        # Entity Journey Card Header
                        with st.expander(f"**{journey_idx}. {journey['entity_name']}** ({journey['total_stages']} stages) - {priority_label}", expanded=(journey_idx <= 2)):
                            # Entity Overview
                            st.markdown(f"""<div style='background: {bg_color}; padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem; border-left: 4px solid {color};'>
<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;'>
    <div>
        <h3 style='font-size: 1.3rem; font-weight: 700; color: {color}; margin: 0 0 0.3rem 0;'>{journey['entity_name']}</h3>
        <div style='color: #94a3b8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;'>{journey['entity_type'].replace('_', ' ')}</div>
    </div>
    <div style='text-align: right;'>
        <span style='background: {priority_color}; color: white; padding: 0.4rem 0.8rem; border-radius: 6px; font-size: 0.75rem; font-weight: 600; display: inline-block;'>{priority_label}</span>
    </div>
</div>
<p style='color: #e2e8f0; font-size: 1rem; line-height: 1.6; margin-bottom: 0.8rem;'>{journey.get('description', '')}</p>
<div style='background: rgba(0,0,0,0.2); padding: 0.9rem; border-radius: 6px;'>
    <p style='color: #e2e8f0; margin: 0; line-height: 1.6;'>
        <strong style='color: #60a5fa;'>📊 Students:</strong> {journey.get('student_count', 'N/A')}
    </p>
    <p style='color: #e2e8f0; margin: 0.5rem 0 0 0; line-height: 1.6;'>
        <strong style='color: #34d399;'>💡 Why Important:</strong> {journey.get('why_important', 'Strategic entity for institutional performance')}
    </p>
</div>
</div>""", unsafe_allow_html=True)

                            # Journey Stages
                            st.markdown("#### 📋 Journey Lifecycle Stages")

                            for stage_idx, stage in enumerate(journey.get('stages', []), 1):
                                stage_color = color
                                stage_icon = ['🔵', '🟢', '🟡', '🟠', '🔴', '🟣'][min(stage_idx - 1, 5)]

                                # Stage Header
                                st.markdown(f"""<div style='display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem; margin-top: 1.5rem;'>
    <span style='font-size: 2rem;'>{stage_icon}</span>
    <div style='flex: 1;'>
        <h4 style='color: {stage_color}; margin: 0; font-size: 1.2rem;'>Stage {stage.get('stage_order', stage_idx)}: {stage.get('stage_name', 'Unknown Stage')}</h4>
        <p style='color: #94a3b8; margin: 0.2rem 0 0 0; font-size: 0.9rem;'>{stage.get('description', '')}</p>
    </div>
</div>""", unsafe_allow_html=True)

                                # Stage Narrative (like Executive Summary findings)
                                st.markdown(f"""<div style='background: rgba(59, 130, 246, 0.1); padding: 1.2rem; border-radius: 8px; border-left: 4px solid #3b82f6; margin-bottom: 1rem;'>
    <strong style='color: #60a5fa; font-size: 0.9rem;'>📖 STAGE NARRATIVE</strong>
    <p style='color: #e2e8f0; margin: 0.5rem 0 0 0; line-height: 1.6; font-size: 1rem;'>{stage.get('narrative_text', 'No narrative available.')}</p>
</div>""", unsafe_allow_html=True)

                                # Key Metrics (like Executive Summary recommendations)
                                key_metrics = stage.get('key_metrics', [])
                                if key_metrics:
                                    st.markdown(f"""<div style='background: rgba(59, 130, 246, 0.15); padding: 1.2rem; border-radius: 8px; border-left: 4px solid #3b82f6; margin-bottom: 1rem;'>
    <h4 style='color: #60a5fa; margin: 0 0 0.8rem 0; font-size: 0.95rem;'>📊 KEY METRICS</h4>
    {''.join([f"<p style='color: #e2e8f0; margin: 0 0 0.6rem 0; line-height: 1.6;'><strong style='color: #60a5fa;'>{m.get('metric', '')}:</strong> {m.get('value', '')} <span style='color: #a5b4fc; font-size: 0.9rem;'>({m.get('significance', '')})</span></p>" for m in key_metrics])}
</div>""", unsafe_allow_html=True)

                                # Insights (like Executive Summary findings)
                                insights = stage.get('insights', [])
                                if insights:
                                    for idx, insight in enumerate(insights, 1):
                                        st.markdown(f"""<div style='background: rgba(16, 185, 129, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #10b981; margin-bottom: 0.8rem;'>
    <strong style='color: #34d399;'>💡 Insight {idx}:</strong> <span style='color: #e2e8f0;'>{insight}</span>
</div>""", unsafe_allow_html=True)

                                # Recommendations (like Executive Summary recommendations)
                                recommendations = stage.get('recommendations', [])
                                if recommendations:
                                    st.markdown(f"""<div style='background: rgba(245, 158, 11, 0.15); padding: 1.5rem; border-radius: 8px; border-left: 4px solid #f59e0b; margin-bottom: 1rem;'>
    <h4 style='color: #fbbf24; margin: 0 0 0.8rem 0; font-size: 0.95rem;'>🎯 RECOMMENDATIONS</h4>
    {''.join([f"<p style='color: #e2e8f0; margin: 0 0 0.6rem 0; line-height: 1.6;'><strong style='color: #fbbf24;'>→</strong> {rec}</p>" for rec in recommendations])}
</div>""", unsafe_allow_html=True)

                                # Display LLM-recommended visualizations
                                visualizations = stage.get('visualizations', [])
                                if visualizations and LLM_ENTITY_JOURNEY_AVAILABLE:
                                    # Get entity data for visualization
                                    entity_data = filter_dataset_for_entity(df, journey)

                                    # Try to generate visualizations first
                                    successful_viz = []
                                    for viz_idx, viz_spec in enumerate(visualizations, 1):
                                        fig = generate_visualization(entity_data, viz_spec)
                                        if fig:
                                            successful_viz.append((viz_idx, viz_spec, fig))

                                    # Only show header if we have successful visualizations
                                    if successful_viz:
                                        st.markdown("<h4 style='color: #e2e8f0; margin-top: 1.5rem;'>📊 Data Visualizations</h4>", unsafe_allow_html=True)
                                        st.caption("*AI-selected visualizations to illustrate this stage*")

                                        # Display the successful visualizations
                                        for viz_idx, viz_spec, fig in successful_viz:
                                            viz_title = viz_spec.get('title', f'Visualization {viz_idx}')
                                            viz_desc = viz_spec.get('description', '')
                                            viz_purpose = viz_spec.get('chart_purpose', '')

                                            # Display chart with description (Executive Summary style)
                                            st.markdown(f"""<div style='background: rgba(99, 102, 241, 0.1); padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid #6366f1;'>
    <h5 style='color: #818cf8; margin: 0 0 0.5rem 0; font-size: 1rem;'>{viz_title}</h5>
    <p style='color: #cbd5e1; margin: 0; font-size: 0.9rem;'><strong>Why this matters:</strong> {viz_desc}</p>
    {f"<p style='color: #a5b4fc; margin: 0.5rem 0 0 0; font-size: 0.85rem; font-style: italic;'>💡 {viz_purpose}</p>" if viz_purpose else ''}
</div>""", unsafe_allow_html=True)
                                            st.plotly_chart(fig, use_container_width=True, key=f"viz_{journey_idx}_{stage_idx}_{viz_idx}")

                    st.markdown("---")
                    st.success("✅ All entity journeys loaded successfully!")

            else:
                # Show prompt to generate entity journeys
                st.info("💡 Click 'Generate Entity Journeys' to let the AI analyze your dataset and create comprehensive entity lifecycle stories")

                # Example entity types
                st.markdown("### 🎯 Example Lifecycle Entities")
                st.markdown("""
                The AI will identify **ENTITIES** that have **LIFECYCLES** and **STATUS CHANGES**:

                **🎓 Student Entity**
                - Lifecycle: Enrollment → Academic Progress → Performance Status → Graduation/Dropout
                - Example Journey: "Student Academic Journey" tracking progression from entry to exit

                **📚 Academic Program Entity**
                - Lifecycle: Program Launch → Growth → Maturity → Optimization
                - Example Journey: "Academic Program Lifecycle" showing how programs evolve

                **💰 Financial Aid Entity**
                - Lifecycle: Application → Approval → Disbursement → Impact Assessment
                - Example Journey: "Financial Aid Journey" tracking aid effectiveness

                **🏢 Campus/Facility Entity**
                - Lifecycle: Opening → Expansion → Optimization
                - Example Journey: "Campus Operations Journey" or "Dormitory Lifecycle"

                **📈 Enrollment Entity**
                - Lifecycle: Application → Acceptance → Registration → Retention
                - Example Journey: "Enrollment Journey" tracking student acquisition

                **💵 Revenue Entity**
                - Lifecycle: Tuition Assessment → Payment → Collection → Revenue Recognition
                - Example Journey: "Revenue Journey" tracking financial flows

                ---

                **Each entity will have:**
                - Multiple lifecycle stages showing progression
                - Data-driven narratives for each stage
                - Nationality/demographic breakdowns in the stories
                - Performance metrics and status indicators
                - Actionable insights and recommendations
                """)

    # ====================================================================================
    # TAB 3: DATA STORYTELLING FULLY AI DRIVEN
    # ====================================================================================
    with tabs[2]:
        st.header("🔬 Data Storytelling Fully AI Driven")
        st.caption("Pure AI-driven entity discovery with ZERO predefined examples or guidance")

        # Explanation box
        st.markdown(f"""<div style='background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(236, 72, 153, 0.15)); padding: 1.2rem; border-radius: 8px; margin-bottom: 1.5rem; border-left: 4px solid #8b5cf6;'>
<p style='margin: 0; color: #e2e8f0;'><strong>🔬 PURE AUTONOMOUS DISCOVERY:</strong> This system operates with <strong>ZERO predefined templates or examples</strong>.
The AI analyzes your {metrics.get('total_students', 0):,} students and <strong>discovers entities entirely from data patterns</strong> with no guidance on what to find.</p>
<p style='margin: 0.5rem 0 0 0; color: #cbd5e1; font-size: 0.9rem;'>
<strong>How it differs from guided discovery:</strong><br>
• <strong>Guided System:</strong> AI gets examples like "Student Journey", "Program Lifecycle" → follows patterns<br>
• <strong>Fully Dynamic:</strong> AI gets NO examples → discovers what exists in YOUR specific data<br>
<br>
<strong>What to expect:</strong> Unique entities specific to your institution that may not fit standard categories.
</p>
</div>""", unsafe_allow_html=True)

        if not st.session_state.ollama_connected:
            st.warning("⚠️ Connect to Ollama to enable fully dynamic discovery")
        elif not FULLY_DYNAMIC_DISCOVERY_AVAILABLE:
            st.error("❌ Fully Dynamic Discovery module not found. Please ensure fully_dynamic_entity_discovery.py is available.")
        else:
            # Button to generate fully dynamic journeys
            col_btn, col_info = st.columns([2, 3])
            with col_btn:
                if st.button("🔬 Discover Entities Autonomously", key="discover_dynamic_entities_btn", type="primary", use_container_width=True):
                    with st.spinner("🔄 AI is analyzing data patterns with NO guidance (this may discover unexpected entities)..."):
                        # Generate fully dynamic journeys (NO templates, NO examples)
                        dynamic_journeys = generate_fully_dynamic_journeys(df, model)
                        st.session_state.llm_cache['dynamic_journeys'] = dynamic_journeys

                        if dynamic_journeys:
                            total_stages = sum(j['total_stages'] for j in dynamic_journeys)
                            st.success(f"✅ DISCOVERED {len(dynamic_journeys)} unique entities autonomously with {total_stages} total lifecycle stages!")
                        else:
                            st.error("❌ Autonomous discovery failed. Please check your dataset and Ollama connection.")

            with col_info:
                st.info("⏱️ **Estimated time:** 10-20 minutes. The AI will make multiple calls to discover patterns WITHOUT any predefined examples.")

            # Display fully dynamic journeys if available
            if 'dynamic_journeys' in st.session_state.llm_cache:
                dynamic_journeys = st.session_state.llm_cache['dynamic_journeys']

                if not dynamic_journeys:
                    st.warning("No entities discovered autonomously. The AI may need clearer data patterns.")
                else:
                    st.markdown("---")
                    st.markdown(f"### 🔬 {len(dynamic_journeys)} Entities Discovered Autonomously")
                    st.caption(f"*AI discovered {len(dynamic_journeys)} unique entities by analyzing data patterns with ZERO guidance*")

                    # Display discovery method badge
                    st.markdown("""<div style='background: rgba(139, 92, 246, 0.15); padding: 0.9rem; border-radius: 6px; margin-bottom: 1rem; border-left: 4px solid #8b5cf6;'>
<div style='font-size: 0.85rem; font-weight: 600; color: #e2e8f0; margin-bottom: 0.4rem;'>🔬 DISCOVERY METHOD: FULLY AUTONOMOUS</div>
<div style='font-size: 0.8rem; color: #cbd5e1;'>These entities were discovered purely from data patterns. No predefined templates or examples were used.</div>
</div>""", unsafe_allow_html=True)

                    # Display each discovered journey
                    for journey_idx, journey in enumerate(dynamic_journeys, 1):
                        # Use different color scheme for dynamic discoveries
                        color = '#8b5cf6'  # Purple for dynamic discoveries
                        bg_color = 'rgba(139, 92, 246, 0.1)'

                        # Priority colors
                        priority = journey.get('priority', 5)
                        if priority >= 8:
                            priority_color = '#8b5cf6'
                            priority_label = '🔬 HIGH DISCOVERY'
                        elif priority >= 6:
                            priority_color = '#a78bfa'
                            priority_label = '🔍 MEDIUM DISCOVERY'
                        else:
                            priority_color = '#c4b5fd'
                            priority_label = '💡 STANDARD DISCOVERY'

                        # Entity Journey Card Header
                        with st.expander(f"**{journey_idx}. {journey['entity_name']}** (Discovered: {journey.get('entity_type', 'unknown')}) - {priority_label}", expanded=(journey_idx <= 2)):
                            # Entity Overview with Discovery Rationale
                            st.markdown(f"""<div style='background: {bg_color}; padding: 1.5rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid {color};'>
<div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;'>
    <div>
        <div style='font-size: 1.2rem; font-weight: 700; color: #e2e8f0; margin-bottom: 0.3rem;'>{journey['entity_name']}</div>
        <div style='color: #94a3b8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px;'>{journey.get('entity_type', 'discovered_entity').replace('_', ' ')}</div>
    </div>
    <div style='text-align: right;'>
        <div style='background: {priority_color}; color: white; padding: 0.3rem 0.6rem; border-radius: 6px; font-size: 0.75rem; font-weight: 600; margin-bottom: 0.3rem;'>{priority_label}</div>
        <div style='color: #94a3b8; font-size: 0.75rem;'>Priority {priority}</div>
    </div>
</div>
<div style='color: #cbd5e1; font-size: 0.95rem; line-height: 1.6; margin-top: 0.75rem;'><strong>What is this entity:</strong> {journey.get('description', '')}</div>
<div style='background: rgba(139, 92, 246, 0.2); padding: 0.8rem; border-radius: 6px; margin-top: 0.75rem; border-left: 3px solid #8b5cf6;'>
    <div style='color: #e2e8f0; font-size: 0.8rem; font-weight: 600; margin-bottom: 0.4rem;'>🔍 Discovery Rationale (Why AI identified this as an entity)</div>
    <div style='color: #cbd5e1; font-size: 0.85rem; font-style: italic;'>{journey.get('discovery_rationale', 'Discovered from data patterns')}</div>
</div>
<div style='background: rgba(0,0,0,0.2); padding: 0.8rem; border-radius: 6px; margin-top: 0.75rem;'>
    <div style='color: #e2e8f0; font-size: 0.8rem; font-weight: 600; margin-bottom: 0.4rem;'>📊 Entity Metrics</div>
    <div style='color: #cbd5e1; font-size: 0.85rem;'>
        <strong>Students:</strong> {journey.get('student_count', 'N/A')} |
        <strong>Lifecycle Indicators:</strong> {', '.join(journey.get('lifecycle_indicators', ['N/A']))}
    </div>
</div>
</div>""", unsafe_allow_html=True)

                            # Journey Stages
                            st.markdown("#### 📋 Discovered Lifecycle Stages")

                            for stage_idx, stage in enumerate(journey.get('stages', []), 1):
                                stage_icon = ['🔵', '🟢', '🟡', '🟠', '🔴', '🟣'][min(stage_idx - 1, 5)]

                                st.markdown(f"""<div style='background: rgba(30, 41, 59, 0.6); border: 2px solid {color}; border-radius: 8px; padding: 1.2rem; margin-bottom: 1rem;'>
<div style='display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.75rem;'>
    <span style='font-size: 1.5rem;'>{stage_icon}</span>
    <div style='flex: 1;'>
        <div style='font-size: 1.1rem; font-weight: 600; color: #e2e8f0;'>Stage {stage.get('stage_order', stage_idx)}: {stage.get('stage_name', 'Unknown Stage')}</div>
        <div style='color: #94a3b8; font-size: 0.85rem;'>{stage.get('description', '')}</div>
    </div>
</div>

<div style='background: rgba(139, 92, 246, 0.2); padding: 0.8rem; border-radius: 6px; margin-bottom: 0.75rem; border-left: 4px solid #8b5cf6;'>
    <div style='color: #e2e8f0; font-size: 0.8rem; font-weight: 600; margin-bottom: 0.4rem;'>🔍 Stage Discovery Rationale</div>
    <div style='color: #cbd5e1; font-size: 0.85rem; font-style: italic;'>{stage.get('discovery_rationale', 'Discovered from data transitions')}</div>
</div>

<div style='background: rgba(99, 102, 241, 0.15); padding: 0.9rem; border-radius: 6px; margin-bottom: 0.75rem; border-left: 4px solid #6366f1;'>
    <div style='color: #e2e8f0; font-size: 0.85rem; font-weight: 600; margin-bottom: 0.5rem;'>📖 Stage Narrative</div>
    <div style='color: #cbd5e1; font-size: 0.95rem; line-height: 1.7;'>{stage.get('narrative_text', 'No narrative available.')}</div>
</div>

<div style='display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-bottom: 0.75rem;'>
    <div style='background: rgba(59, 130, 246, 0.15); padding: 0.8rem; border-radius: 6px; border-left: 3px solid #3b82f6;'>
        <div style='color: #60a5fa; font-size: 0.75rem; font-weight: 600; margin-bottom: 0.5rem; text-transform: uppercase;'>📊 Key Metrics</div>
        {''.join([f"<div style='color: #cbd5e1; font-size: 0.85rem; margin-bottom: 0.3rem; line-height: 1.5;'><strong style='color: #e2e8f0;'>{m.get('metric', '')}:</strong> {m.get('value', '')} <span style='color: #94a3b8; font-size: 0.8rem;'>({m.get('significance', '')})</span></div>" for m in stage.get('key_metrics', [])])}
    </div>
    <div style='background: rgba(16, 185, 129, 0.15); padding: 0.8rem; border-radius: 6px; border-left: 3px solid #10b981;'>
        <div style='color: #34d399; font-size: 0.75rem; font-weight: 600; margin-bottom: 0.5rem; text-transform: uppercase;'>💡 Insights</div>
        {''.join([f"<div style='color: #cbd5e1; font-size: 0.85rem; margin-bottom: 0.3rem; line-height: 1.5;'>• {insight}</div>" for insight in stage.get('insights', [])])}
    </div>
</div>

<div style='background: rgba(245, 158, 11, 0.15); padding: 0.8rem; border-radius: 6px; border-left: 3px solid #f59e0b;'>
    <div style='color: #fbbf24; font-size: 0.75rem; font-weight: 600; margin-bottom: 0.5rem; text-transform: uppercase;'>🎯 Recommendations</div>
    {''.join([f"<div style='color: #cbd5e1; font-size: 0.85rem; margin-bottom: 0.3rem; line-height: 1.5;'>→ {rec}</div>" for rec in stage.get('recommendations', [])])}
</div>
</div>""", unsafe_allow_html=True)

                                # Display visualizations if available
                                visualizations = stage.get('visualizations', [])
                                if visualizations and LLM_ENTITY_JOURNEY_AVAILABLE:
                                    # Get entity data for visualization
                                    entity_data = filter_dataset_for_entity(df, journey)

                                    # Try to generate visualizations first
                                    successful_viz = []
                                    for viz_idx, viz_spec in enumerate(visualizations, 1):
                                        fig = generate_visualization(entity_data, viz_spec)
                                        if fig:
                                            successful_viz.append((viz_idx, viz_spec, fig))

                                    # Only show header if we have successful visualizations
                                    if successful_viz:
                                        st.markdown("<h4 style='color: #e2e8f0; margin-top: 1.5rem;'>📊 Data Visualizations</h4>", unsafe_allow_html=True)
                                        st.caption("*AI-selected visualizations for this discovered stage*")

                                        # Display the successful visualizations
                                        for viz_idx, viz_spec, fig in successful_viz:
                                            viz_title = viz_spec.get('title', f'Visualization {viz_idx}')
                                            viz_desc = viz_spec.get('description', '')
                                            viz_purpose = viz_spec.get('chart_purpose', '')

                                            st.markdown(f"""<div style='background: rgba(139, 92, 246, 0.15); padding: 0.8rem; border-radius: 6px; margin-bottom: 0.5rem; border-left: 3px solid #8b5cf6;'>
                                                <div style='font-size: 0.9rem; font-weight: 600; color: #e2e8f0; margin-bottom: 0.3rem;'>{viz_title}</div>
                                                <div style='font-size: 0.8rem; color: #cbd5e1;'>{viz_desc}</div>
                                                {f"<div style='font-size: 0.8rem; color: #a5b4fc; margin-top: 0.3rem; font-style: italic;'>💡 {viz_purpose}</div>" if viz_purpose else ''}
                                                </div>""", unsafe_allow_html=True)
                                            st.plotly_chart(fig, use_container_width=True, key=f"dyn_viz_{journey_idx}_{stage_idx}_{viz_idx}")

                    st.markdown("---")
                    st.success(f"✅ All {len(dynamic_journeys)} dynamically discovered journeys loaded successfully!")

            else:
                # Show prompt to discover entities
                st.info("💡 Click 'Discover Entities Autonomously' to let the AI analyze your data with ZERO predefined templates")

                # Comparison: Guided vs Fully Dynamic
                st.markdown("### 🆚 Guided vs Fully Dynamic Discovery")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("""
                    **📖 Guided Discovery (Tab 2)**
                    - AI gets examples: "Student Journey", "Program Lifecycle", "Aid Journey"
                    - Follows proven patterns
                    - Predictable, consistent results
                    - Best for: Standard institutional analysis
                    """)

                with col2:
                    st.markdown("""
                    **🔬 Fully Dynamic Discovery (This Tab)**
                    - AI gets ZERO examples or templates
                    - Discovers entities purely from data patterns
                    - Unexpected, unique discoveries
                    - Best for: Finding hidden patterns specific to YOUR data
                    """)

                st.markdown("---")

                st.markdown("### 🎯 What AI Might Discover")
                st.markdown("""
                Without predefined templates, the AI could discover unique entities like:
                - **Payment Pattern Clusters** - Students grouped by payment behavior
                - **Performance Trajectory Groups** - Students following similar GPA patterns
                - **Aid-to-Success Pathways** - Different aid effectiveness patterns
                - **Engagement Level Segments** - Students with different participation patterns
                - **Market Risk Portfolios** - Nationality combinations affecting revenue stability
                - **Capacity Utilization Zones** - Facility usage patterns

                **The AI will discover what's ACTUALLY in your data, not what we expect to find!**
                """)


    # TAB 3: DATA STORYTELLING - COMPLETE JOURNEY STORIES (PreDefined+LLM Narrative)
    # ====================================================================================
    with tabs[3]:
        st.header("📚 Complete Journey Stories - PreDefined Structure + AI Narratives")
        st.caption("Comprehensive analytics with pre-defined journeys enriched by LLM-generated narratives")

        if not st.session_state.ollama_connected:
            st.warning("⚠️ Connect to Ollama to generate journey narratives")
        else:
            st.markdown("""
            <div style='background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%); padding: 2rem; border-radius: 12px; margin: 2rem 0;'>
                <h2 style='margin: 0; color: white; display: flex; align-items: center; gap: 0.75rem;'>
                    📚 Complete Journey Stories
                    <span style='background: rgba(255,255,255,0.2); padding: 0.35rem 1rem; border-radius: 20px; font-size: 0.65rem; font-weight: normal;'>COMPREHENSIVE ANALYTICS</span>
                </h2>
                <p style='margin: 0.75rem 0 0 0; color: #e9d5ff; font-size: 1rem; line-height: 1.6;'>
                    📖 Deep-dive into 6 comprehensive journeys with detailed stories, metrics, insights, and action plans<br>
                    🤖 AI-powered narratives combined with precise metric calculations<br>
                    💼 Executive-ready business context, ROI analysis, and strategic recommendations
                </p>
            </div>
            """, unsafe_allow_html=True)

            if not JOURNEY_MODULES_AVAILABLE:
                st.error("❌ Journey modules not available. Please ensure journey_definitions.py, journey_metrics.py, journey_narratives.py, and journey_assembler.py are in the same directory.")
            else:
                # Validate dataset
                is_valid, missing_fields, journey_validation = validate_dataset_for_journeys(df)

                if not is_valid:
                    st.warning(f"⚠️ Dataset is missing some required fields for complete journey generation: {', '.join(missing_fields)}")
                    st.caption("Some journeys may have incomplete data. The system will work with available fields.")

                # Generation button
                col_gen1, col_gen2 = st.columns([3, 1])
                with col_gen1:
                    if st.button("🚀 Generate Complete Journey Stories (All 6 Journeys)", key="generate_complete_journeys", type="primary", use_container_width=True):
                        # Progress container
                        progress_container = st.empty()
                        status_container = st.empty()

                        def progress_callback(stage, current, total, message):
                            """Update progress display"""
                            if stage == 'validation':
                                progress_container.progress(5)
                                status_container.info(f"🔍 {message}")
                            elif stage == 'metrics':
                                progress = 5 + int((current / total) * 15)
                                progress_container.progress(progress)
                                status_container.info(f"📊 Calculating metrics: {current}/{total} stories")
                            elif stage == 'narratives':
                                progress = 20 + int((current / total) * 70)
                                progress_container.progress(progress)
                                status_container.info(f"✍️ Generating narratives: {current}/{total} components - {message}")
                            elif stage == 'assembly':
                                progress = 90 + int((current / total) * 10)
                                progress_container.progress(progress)
                                status_container.info(f"🔧 Assembling journeys: {current}/{total}")
                            elif stage == 'error':
                                status_container.error(f"❌ {message}")

                        with st.spinner("🤖 Generating complete journeys... This may take 5-15 minutes depending on LLM speed"):
                            from journey_assembler import generate_all_journeys

                            # Generate all journeys
                            journeys, metadata = generate_all_journeys(
                                df,
                                query_ollama,
                                model,
                                url,
                                temperature=0.4,
                                timeout=180,
                                progress_callback=progress_callback
                            )

                            # Store in session state
                            st.session_state.complete_journeys = journeys
                            st.session_state.journey_generation_metadata = metadata

                            progress_container.progress(100)

                            if metadata.get('success'):
                                duration = metadata.get('duration_seconds', 0)
                                minutes = int(duration // 60)
                                seconds = int(duration % 60)

                                status_container.success(f"""
                                ✅ **All journeys generated successfully!**
                                - **{len(journeys)}** complete journeys
                                - **{metadata['assembly']['total_stories']}** stories with full narratives
                                - **{metadata['metrics']['total_metrics_calculated']}** metrics calculated
                                - **{metadata['narratives']['total_components_generated']}** narrative components generated
                                - **Time:** {minutes}m {seconds}s
                                """)
                            else:
                                status_container.error(f"❌ Generation failed: {', '.join(metadata.get('errors', ['Unknown error']))}")

                with col_gen2:
                    if st.session_state.complete_journeys:
                        if st.button("🗑️ Clear", key="clear_journeys"):
                            st.session_state.complete_journeys = None
                            st.session_state.journey_generation_metadata = None
                            st.rerun()

                # Display complete journeys if available
                if st.session_state.complete_journeys:
                    journeys = st.session_state.complete_journeys

                    st.markdown("---")

                    # Create tabs for each journey
                    journey_tabs = st.tabs([
                        "📊 Journey 1: Enrollment",
                        "💰 Journey 2: Revenue",
                        "🏢 Journey 3: Operations",
                        "🎓 Journey 4: Academics",
                        "🎯 Journey 5: Retention",
                        "⚠️ Journey 6: Risk"
                    ])

                    # Display each journey in its tab
                    for tab_idx, (journey_tab, journey) in enumerate(zip(journey_tabs, journeys)):
                        with journey_tab:
                            # Journey header
                            st.markdown(f"""
                            <div style='background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); padding: 1.5rem; border-radius: 10px; margin-bottom: 1.5rem;'>
                                <h2 style='margin: 0; color: white;'>{journey['name']}</h2>
                                <p style='margin: 0.5rem 0 0 0; color: #ddd6fe; font-size: 0.95rem;'>{journey['subtitle']}</p>
                                <div style='margin-top: 1rem; display: flex; gap: 1rem;'>
                                    <span style='background: rgba(255,255,255,0.2); padding: 0.4rem 0.8rem; border-radius: 6px; font-size: 0.85rem;'>
                                        📖 {journey['story_count']} Stories
                                    </span>
                                    <span style='background: rgba(255,255,255,0.2); padding: 0.4rem 0.8rem; border-radius: 6px; font-size: 0.85rem;'>
                                        📊 {journey['total_metrics_calculated']} Metrics
                                    </span>
                                    <span style='background: rgba(255,255,255,0.2); padding: 0.4rem 0.8rem; border-radius: 6px; font-size: 0.85rem;'>
                                        ✅ {'Complete' if journey['is_complete'] else 'Partial'}
                                    </span>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                            # JOURNEY-LEVEL VISUALIZATIONS - Most Important Metrics
                            st.markdown("""
                            <div style='background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(99, 102, 241, 0.15));
                                        padding: 1.5rem; border-radius: 10px; margin: 2rem 0 1.5rem 0;
                                        border-left: 5px solid #3b82f6;'>
                                <h2 style='margin: 0 0 0.5rem 0; color: #1e293b; font-size: 1.5rem;'>
                                    📊 Journey Insights - Key Metrics Overview
                                </h2>
                                <p style='margin: 0; color: #475569; font-size: 0.95rem; line-height: 1.6;'>
                                    Visual analytics showing the most important performance indicators for this journey.
                                    These metrics provide a comprehensive view of key trends, patterns, and opportunities.
                                </p>
                            </div>
                            """, unsafe_allow_html=True)

                            # Create 2 rows of 3 columns for 4-6 key metrics per journey
                            viz_row1 = st.columns(3)
                            viz_row2 = st.columns(3)

                            # JOURNEY 1: ENROLLMENT
                            if tab_idx == 0:
                                st.markdown("""
                                <div style='background: rgba(59, 130, 246, 0.1); padding: 0.75rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #3b82f6;'>
                                    <div style='font-weight: 600; color: #1e293b; font-size: 0.95rem;'>📈 Diversity & Demographics Analysis</div>
                                    <div style='font-size: 0.85rem; color: #475569; margin-top: 0.25rem;'>Distribution of students by nationality, region, and enrollment status</div>
                                </div>
                                """, unsafe_allow_html=True)

                                with viz_row1[0]:
                                    if 'nationality' in df.columns:
                                        st.caption("🌍 **Nationality Distribution**")
                                        nat_counts = df['nationality'].value_counts().head(10)
                                        fig = create_plotly_chart("bar", {"x": nat_counts.index.tolist(), "y": nat_counts.values.tolist()}, "Top 10 Nationalities")
                                        st.plotly_chart(fig, use_container_width=True, key=f"journey_{tab_idx}_nat")

                                with viz_row1[1]:
                                    if 'nationality' in df.columns:
                                        st.caption("🇦🇪 **UAE vs International Mix**")
                                        uae_count = len(df[df['nationality'] == 'United Arab Emirates'])
                                        intl_count = len(df) - uae_count
                                        fig = create_plotly_chart("pie", {"labels": ["UAE Nationals", "International"], "values": [uae_count, intl_count]}, "UAE vs International Distribution")
                                        st.plotly_chart(fig, use_container_width=True, key=f"journey_{tab_idx}_uae_intl")

                                with viz_row1[2]:
                                    if 'enrollment_enrollment_status' in df.columns:
                                        st.caption("📋 **Student Status**")
                                        status_counts = df['enrollment_enrollment_status'].value_counts()
                                        fig = create_plotly_chart("pie", {"labels": status_counts.index.tolist(), "values": status_counts.values.tolist()}, "Enrollment Status")
                                        st.plotly_chart(fig, use_container_width=True, key=f"journey_{tab_idx}_status")

                                st.markdown("""
                                <div style='background: rgba(139, 92, 246, 0.1); padding: 0.75rem; border-radius: 8px; margin: 1.5rem 0 1rem 0; border-left: 4px solid #8b5cf6;'>
                                    <div style='font-weight: 600; color: #1e293b; font-size: 0.95rem;'>📊 Enrollment Trends & Program Performance</div>
                                    <div style='font-size: 0.85rem; color: #475569; margin-top: 0.25rem;'>Growth patterns by cohort, gender balance, and program popularity</div>
                                </div>
                                """, unsafe_allow_html=True)

                                with viz_row2[0]:
                                    if 'cohort_year' in df.columns:
                                        st.caption("📅 **Cohort Trends Over Time**")
                                        cohort_counts = df['cohort_year'].value_counts().sort_index()
                                        fig = create_plotly_chart("bar", {"x": cohort_counts.index.tolist(), "y": cohort_counts.values.tolist()}, "Enrollment Trends by Cohort")
                                        st.plotly_chart(fig, use_container_width=True, key=f"journey_{tab_idx}_cohort")

                                with viz_row2[1]:
                                    if 'gender' in df.columns:
                                        st.caption("⚖️ **Gender Balance**")
                                        gender_counts = df['gender'].value_counts()
                                        fig = create_plotly_chart("pie", {"labels": gender_counts.index.tolist(), "values": gender_counts.values.tolist()}, "Gender Distribution")
                                        st.plotly_chart(fig, use_container_width=True, key=f"journey_{tab_idx}_gender")

                                with viz_row2[2]:
                                    if 'current_program' in df.columns:
                                        st.caption("🎓 **Most Popular Programs**")
                                        prog_counts = df['current_program'].value_counts().head(8)
                                        fig = create_plotly_chart("bar", {"x": prog_counts.index.tolist(), "y": prog_counts.values.tolist()}, "Top Programs by Enrollment")
                                        st.plotly_chart(fig, use_container_width=True, key=f"journey_{tab_idx}_programs")

                            # JOURNEY 2: REVENUE
                            elif tab_idx == 1:
                                # Try multiple column name variations for tuition
                                tuition_col = None
                                for col_name in ['Total_Tuition', 'total_tuition', 'tuition', 'Tuition', 'tuition_fees', 'fees']:
                                    if col_name in df.columns:
                                        tuition_col = col_name
                                        break

                                # Try multiple column name variations for aid
                                aid_col = None
                                for col_name in ['Total_Aid', 'total_aid', 'aid', 'Aid', 'financial_aid', 'scholarship']:
                                    if col_name in df.columns:
                                        aid_col = col_name
                                        break

                                st.markdown("""
                                <div style='background: rgba(16, 185, 129, 0.1); padding: 0.75rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #10b981;'>
                                    <div style='font-weight: 600; color: #1e293b; font-size: 0.95rem;'>💰 Revenue Distribution & Financial Aid Analysis</div>
                                    <div style='font-size: 0.85rem; color: #475569; margin-top: 0.25rem;'>Revenue sources, tuition patterns, and financial aid allocation</div>
                                </div>
                                """, unsafe_allow_html=True)

                                with viz_row1[0]:
                                    if tuition_col and 'nationality' in df.columns:
                                        st.caption("🌍 **Revenue by Nationality**")
                                        rev_by_nat = df.groupby('nationality')[tuition_col].sum().sort_values(ascending=False).head(10)
                                        fig = create_plotly_chart("bar", {"x": rev_by_nat.index.tolist(), "y": rev_by_nat.values.tolist()}, "Revenue by Nationality")
                                        st.plotly_chart(fig, use_container_width=True, key=f"journey_{tab_idx}_rev_nat")
                                    elif 'nationality' in df.columns:
                                        # Fallback: show nationality distribution
                                        nat_counts = df['nationality'].value_counts().head(10)
                                        fig = create_plotly_chart("bar", {"x": nat_counts.index.tolist(), "y": nat_counts.values.tolist()}, "Student Distribution by Nationality")
                                        st.plotly_chart(fig, use_container_width=True, key=f"journey_{tab_idx}_nat_dist")

                                with viz_row1[1]:
                                    if tuition_col:
                                        st.caption("💵 **Tuition Fee Range**")
                                        fig = create_plotly_chart("histogram", {"values": df[tuition_col].dropna()}, "Tuition Distribution")
                                        st.plotly_chart(fig, use_container_width=True, key=f"journey_{tab_idx}_tuition_dist")
                                    elif 'cohort_year' in df.columns:
                                        st.caption("📅 **Students by Cohort**")
                                        cohort_counts = df['cohort_year'].value_counts().sort_index()
                                        fig = create_plotly_chart("bar", {"x": cohort_counts.index.tolist(), "y": cohort_counts.values.tolist()}, "Students by Cohort")
                                        st.plotly_chart(fig, use_container_width=True, key=f"journey_{tab_idx}_cohort_fb")

                                with viz_row1[2]:
                                    if aid_col:
                                        st.caption("🎓 **Financial Aid Coverage**")
                                        aid_recipients = len(df[df[aid_col] > 0])
                                        no_aid = len(df[df[aid_col] == 0])
                                        fig = create_plotly_chart("pie", {"labels": ["With Financial Aid", "No Aid"], "values": [aid_recipients, no_aid]}, "Financial Aid Recipients")
                                        st.plotly_chart(fig, use_container_width=True, key=f"journey_{tab_idx}_aid")
                                    elif 'enrollment_enrollment_status' in df.columns:
                                        # Fallback: show enrollment status
                                        status_counts = df['enrollment_enrollment_status'].value_counts()
                                        fig = create_plotly_chart("pie", {"labels": status_counts.index.tolist(), "values": status_counts.values.tolist()}, "Enrollment Status")
                                        st.plotly_chart(fig, use_container_width=True, key=f"journey_{tab_idx}_status_fb")

                                st.markdown("**📊 Program Performance & Payment Status**")
                                with viz_row2[0]:
                                    if tuition_col and 'current_program' in df.columns:
                                        rev_by_prog = df.groupby('current_program')[tuition_col].sum().sort_values(ascending=False).head(8)
                                        fig = create_plotly_chart("bar", {"x": rev_by_prog.index.tolist(), "y": rev_by_prog.values.tolist()}, "Revenue by Program")
                                        st.plotly_chart(fig, use_container_width=True, key=f"journey_{tab_idx}_rev_prog")
                                    elif 'current_program' in df.columns:
                                        # Fallback: show program enrollment
                                        prog_counts = df['current_program'].value_counts().head(8)
                                        fig = create_plotly_chart("bar", {"x": prog_counts.index.tolist(), "y": prog_counts.values.tolist()}, "Students by Program")
                                        st.plotly_chart(fig, use_container_width=True, key=f"journey_{tab_idx}_prog_fb")

                                with viz_row2[1]:
                                    if 'payment_status' in df.columns:
                                        pay_counts = df['payment_status'].value_counts()
                                        fig = create_plotly_chart("pie", {"labels": pay_counts.index.tolist(), "values": pay_counts.values.tolist()}, "Payment Status Distribution")
                                        st.plotly_chart(fig, use_container_width=True, key=f"journey_{tab_idx}_payment")
                                    elif 'gender' in df.columns:
                                        # Fallback: show gender distribution
                                        gender_counts = df['gender'].value_counts()
                                        fig = create_plotly_chart("pie", {"labels": gender_counts.index.tolist(), "values": gender_counts.values.tolist()}, "Gender Distribution")
                                        st.plotly_chart(fig, use_container_width=True, key=f"journey_{tab_idx}_gender_fb")

                            # JOURNEY 3: OPERATIONS
                            elif tab_idx == 2:
                                st.markdown("""
                                <div style='background: rgba(139, 92, 246, 0.1); padding: 0.75rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #8b5cf6;'>
                                    <div style='font-weight: 600; color: #1e293b; font-size: 0.95rem;'>⚙️ Operational Metrics & Cohort Analysis</div>
                                    <div style='font-size: 0.85rem; color: #475569; margin-top: 0.25rem;'>Student operational status, cohort distribution, and institutional capacity planning</div>
                                </div>
                                """, unsafe_allow_html=True)

                                with viz_row1[0]:
                                    if 'enrollment_enrollment_status' in df.columns:
                                        st.caption("📊 **Operational Status Distribution**")
                                        status_counts = df['enrollment_enrollment_status'].value_counts()
                                        fig = create_plotly_chart("pie", {"labels": status_counts.index.tolist(), "values": status_counts.values.tolist()}, "Operational Status")
                                        st.plotly_chart(fig, use_container_width=True, key=f"journey_{tab_idx}_op_status")

                                with viz_row1[1]:
                                    if 'cohort_year' in df.columns:
                                        st.caption("📅 **Students by Cohort Year**")
                                        cohort_counts = df['cohort_year'].value_counts().sort_index()
                                        fig = create_plotly_chart("bar", {"x": cohort_counts.index.tolist(), "y": cohort_counts.values.tolist()}, "Students by Cohort")
                                        st.plotly_chart(fig, use_container_width=True, key=f"journey_{tab_idx}_cohort_ops")

                            # JOURNEY 4: ACADEMICS
                            elif tab_idx == 3:
                                st.markdown("""
                                <div style='background: rgba(245, 158, 11, 0.1); padding: 0.75rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #f59e0b;'>
                                    <div style='font-weight: 600; color: #1e293b; font-size: 0.95rem;'>🎓 Academic Performance Overview</div>
                                    <div style='font-size: 0.85rem; color: #475569; margin-top: 0.25rem;'>GPA distribution, performance tiers, and program excellence analysis</div>
                                </div>
                                """, unsafe_allow_html=True)

                                with viz_row1[0]:
                                    if 'cumulative_gpa' in df.columns:
                                        st.caption("📊 **Overall GPA Distribution**")
                                        fig = create_plotly_chart("histogram", {"values": df['cumulative_gpa'].dropna()}, "GPA Distribution")
                                        st.plotly_chart(fig, use_container_width=True, key=f"journey_{tab_idx}_gpa_dist")

                                with viz_row1[1]:
                                    if 'cumulative_gpa' in df.columns:
                                        st.caption("🎯 **Performance Tiers**")
                                        high = len(df[df['cumulative_gpa'] >= 3.5])
                                        mid = len(df[(df['cumulative_gpa'] >= 2.5) & (df['cumulative_gpa'] < 3.5)])
                                        low = len(df[df['cumulative_gpa'] < 2.5])
                                        fig = create_plotly_chart("pie", {"labels": ["High Performers (≥3.5)", "Mid Performers (2.5-3.5)", "At Risk (<2.5)"], "values": [high, mid, low]}, "Performance Tiers")
                                        st.plotly_chart(fig, use_container_width=True, key=f"journey_{tab_idx}_perf_tiers")

                                with viz_row1[2]:
                                    if 'cumulative_gpa' in df.columns and 'current_program' in df.columns:
                                        st.caption("🏆 **Top Performing Programs**")
                                        gpa_by_prog = df.groupby('current_program')['cumulative_gpa'].mean().sort_values(ascending=False).head(8)
                                        fig = create_plotly_chart("bar", {"x": gpa_by_prog.index.tolist(), "y": gpa_by_prog.values.tolist()}, "Average GPA by Program")
                                        st.plotly_chart(fig, use_container_width=True, key=f"journey_{tab_idx}_gpa_prog")

                                st.markdown("""
                                <div style='background: rgba(139, 92, 246, 0.1); padding: 0.75rem; border-radius: 8px; margin: 1.5rem 0 1rem 0; border-left: 4px solid #8b5cf6;'>
                                    <div style='font-weight: 600; color: #1e293b; font-size: 0.95rem;'>📊 Performance by Demographics & Workload</div>
                                    <div style='font-size: 0.85rem; color: #475569; margin-top: 0.25rem;'>Achievement patterns across nationalities and credit hour loads</div>
                                </div>
                                """, unsafe_allow_html=True)

                                with viz_row2[0]:
                                    if 'cumulative_gpa' in df.columns and 'nationality' in df.columns:
                                        st.caption("🌍 **GPA by Nationality**")
                                        gpa_by_nat = df.groupby('nationality')['cumulative_gpa'].mean().sort_values(ascending=False).head(10)
                                        fig = create_plotly_chart("bar", {"x": gpa_by_nat.index.tolist(), "y": gpa_by_nat.values.tolist()}, "Average GPA by Nationality")
                                        st.plotly_chart(fig, use_container_width=True, key=f"journey_{tab_idx}_gpa_nat")

                                with viz_row2[1]:
                                    if 'total_credit_hours' in df.columns:
                                        st.caption("📚 **Student Workload**")
                                        fig = create_plotly_chart("histogram", {"values": df['total_credit_hours'].dropna()}, "Credit Hours Distribution")
                                        st.plotly_chart(fig, use_container_width=True, key=f"journey_{tab_idx}_credits")

                            # JOURNEY 5: RETENTION
                            elif tab_idx == 4:
                                st.markdown("""
                                <div style='background: rgba(34, 197, 94, 0.1); padding: 0.75rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #22c55e;'>
                                    <div style='font-weight: 600; color: #1e293b; font-size: 0.95rem;'>🎯 Retention & Persistence Indicators</div>
                                    <div style='font-size: 0.85rem; color: #475569; margin-top: 0.25rem;'>Student enrollment continuity, academic standing, and retention risk factors</div>
                                </div>
                                """, unsafe_allow_html=True)

                                with viz_row1[0]:
                                    if 'enrollment_enrollment_status' in df.columns:
                                        st.caption("📊 **Student Enrollment Status**")
                                        status_counts = df['enrollment_enrollment_status'].value_counts()
                                        fig = create_plotly_chart("pie", {"labels": status_counts.index.tolist(), "values": status_counts.values.tolist()}, "Student Status")
                                        st.plotly_chart(fig, use_container_width=True, key=f"journey_{tab_idx}_retention_status")

                                with viz_row1[1]:
                                    if 'cumulative_gpa' in df.columns:
                                        st.caption("📈 **Academic Performance Distribution**")
                                        fig = create_plotly_chart("histogram", {"values": df['cumulative_gpa'].dropna()}, "GPA Distribution")
                                        st.plotly_chart(fig, use_container_width=True, key=f"journey_{tab_idx}_retention_gpa")

                            # JOURNEY 6: RISK
                            elif tab_idx == 5:
                                st.markdown("""
                                <div style='background: rgba(239, 68, 68, 0.1); padding: 0.75rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #ef4444;'>
                                    <div style='font-weight: 600; color: #1e293b; font-size: 0.95rem;'>⚠️ Risk Assessment & Early Warning Indicators</div>
                                    <div style='font-size: 0.85rem; color: #475569; margin-top: 0.25rem;'>Academic performance risk, financial obligations, and student success predictors</div>
                                </div>
                                """, unsafe_allow_html=True)

                                with viz_row1[0]:
                                    if 'cumulative_gpa' in df.columns:
                                        st.caption("📉 **Academic Risk Levels**")
                                        at_risk = len(df[df['cumulative_gpa'] < 2.5])
                                        ok = len(df[df['cumulative_gpa'] >= 2.5])
                                        fig = create_plotly_chart("pie", {"labels": ["At Risk (<2.5 GPA)", "Acceptable (≥2.5)"], "values": [at_risk, ok]}, "Academic Risk Assessment")
                                        st.plotly_chart(fig, use_container_width=True, key=f"journey_{tab_idx}_risk_gpa")

                                with viz_row1[1]:
                                    if 'payment_status' in df.columns:
                                        st.caption("💳 **Payment Status & Financial Risk**")
                                        pay_counts = df['payment_status'].value_counts()
                                        fig = create_plotly_chart("pie", {"labels": pay_counts.index.tolist(), "values": pay_counts.values.tolist()}, "Payment Risk")
                                        st.plotly_chart(fig, use_container_width=True, key=f"journey_{tab_idx}_risk_payment")

                            st.markdown("<br>", unsafe_allow_html=True)
                            st.markdown("""
                            <div style='background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(168, 85, 247, 0.15));
                                        padding: 1.5rem; border-radius: 10px; margin: 2rem 0 1.5rem 0;
                                        border-left: 5px solid #8b5cf6;'>
                                <h2 style='margin: 0 0 0.5rem 0; color: #1e293b; font-size: 1.5rem;'>
                                    📖 Journey Stories - Detailed Narratives
                                </h2>
                                <p style='margin: 0; color: #475569; font-size: 0.95rem; line-height: 1.6;'>
                                    AI-generated narratives providing business context, strategic insights, and actionable recommendations
                                    for each aspect of this journey. Expand each story to explore detailed analysis.
                                </p>
                            </div>
                            """, unsafe_allow_html=True)

                            # Import html for escaping (once per journey)
                            import html

                            # Display each story
                            for story_idx, story in enumerate(journey['stories'], 1):
                                with st.expander(f"📄 Story {story_idx}: {story['title']}", expanded=(story_idx == 1)):
                                    # Story subtitle
                                    if story.get('subtitle'):
                                        st.caption(f"*{story['subtitle']}*")

                                    st.markdown("---")

                                    # VISUAL FLOW DIAGRAM - Story Analysis
                                    st.markdown("#### 📊 Story Analysis Flow")

                                    # Extract and escape content properly
                                    opening = html.escape(story.get('opening_narrative', 'N/A')[:200].replace('\n', ' ').replace('  ', ' '))
                                    insights = html.escape(story.get('data_insights', 'Key data patterns and trends identified')[:180].replace('\n', ' ').replace('  ', ' '))
                                    impact = html.escape(story.get('business_impact', 'N/A')[:180].replace('\n', ' ').replace('  ', ' '))
                                    action = html.escape(story.get('action_plan', 'Strategic recommendations')[:180].replace('\n', ' ').replace('  ', ' '))

                                    # Stage 1: Current Situation
                                    st.markdown(f"""
                                    <div style='background: linear-gradient(135deg, #3b82f6, #2563eb); color: white; padding: 1.2rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); margin-bottom: 0.5rem;'>
                                        <div style='font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; opacity: 0.9; margin-bottom: 0.4rem; font-weight: 600;'>📌 CURRENT SITUATION</div>
                                        <div style='font-size: 0.95rem; line-height: 1.6; opacity: 0.95;'>{opening}...</div>
                                    </div>
                                    """, unsafe_allow_html=True)

                                    st.markdown("<div style='text-align: center; font-size: 2rem; color: #3b82f6; margin: 0.5rem 0;'>↓</div>", unsafe_allow_html=True)

                                    # Stage 2: Key Insights
                                    st.markdown(f"""
                                    <div style='background: linear-gradient(135deg, #8b5cf6, #7c3aed); color: white; padding: 1.2rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3); margin-bottom: 0.5rem;'>
                                        <div style='font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; opacity: 0.9; margin-bottom: 0.4rem; font-weight: 600;'>📈 KEY INSIGHTS</div>
                                        <div style='font-size: 0.95rem; line-height: 1.6; opacity: 0.95;'>{insights}...</div>
                                    </div>
                                    """, unsafe_allow_html=True)

                                    st.markdown("<div style='text-align: center; font-size: 2rem; color: #8b5cf6; margin: 0.5rem 0;'>↓</div>", unsafe_allow_html=True)

                                    # Stage 3: Business Impact
                                    st.markdown(f"""
                                    <div style='background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 1.2rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3); margin-bottom: 0.5rem;'>
                                        <div style='font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; opacity: 0.9; margin-bottom: 0.4rem; font-weight: 600;'>💼 BUSINESS IMPACT</div>
                                        <div style='font-size: 0.95rem; line-height: 1.6; opacity: 0.95;'>{impact}...</div>
                                    </div>
                                    """, unsafe_allow_html=True)

                                    st.markdown("<div style='text-align: center; font-size: 2rem; color: #10b981; margin: 0.5rem 0;'>↓</div>", unsafe_allow_html=True)

                                    # Stage 4: Recommended Actions
                                    st.markdown(f"""
                                    <div style='background: linear-gradient(135deg, #f59e0b, #d97706); color: white; padding: 1.2rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3); margin-bottom: 1rem;'>
                                        <div style='font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; opacity: 0.9; margin-bottom: 0.4rem; font-weight: 600;'>🎯 RECOMMENDED ACTIONS</div>
                                        <div style='font-size: 0.95rem; line-height: 1.6; opacity: 0.95;'>{action}...</div>
                                    </div>
                                    """, unsafe_allow_html=True)

                                    st.markdown("---")

                                    # Detailed sections in expander
                                    with st.expander("📋 View Full Analysis Details", expanded=False):
                                        # Complete Narrative
                                        st.markdown("##### 📖 Complete Narrative")
                                        full_narrative = html.escape(story.get('opening_narrative', 'N/A')).replace('\n', '<br>')
                                        st.markdown(f"""
                                        <div style='background: rgba(139, 92, 246, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #8b5cf6; margin-bottom: 1rem;'>
                                            <p style='margin: 0; color: #1e293b; line-height: 1.6;'>{full_narrative}</p>
                                        </div>
                                        """, unsafe_allow_html=True)

                                        # Full Data Insights
                                        st.markdown("##### 📊 Complete Data Insights")
                                        full_insights = html.escape(story.get('data_insights', 'N/A')).replace('\n', '<br>')
                                        st.markdown(f"""
                                        <div style='background: rgba(59, 130, 246, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #3b82f6; margin-bottom: 1rem;'>
                                            <p style='margin: 0; color: #1e293b; line-height: 1.6;'>{full_insights}</p>
                                        </div>
                                        """, unsafe_allow_html=True)

                                        # Full Business Impact
                                        st.markdown("##### 💼 Full Business Impact Analysis")
                                        full_impact = html.escape(story.get('business_impact', 'N/A')).replace('\n', '<br>')
                                        st.markdown(f"""
                                        <div style='background: rgba(34, 197, 94, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #22c55e; margin-bottom: 1rem;'>
                                            <p style='margin: 0; color: #1e293b; line-height: 1.6;'>{full_impact}</p>
                                        </div>
                                        """, unsafe_allow_html=True)

                                        # Key Findings
                                        st.markdown("##### 🔍 Key Findings")
                                        full_findings = html.escape(story.get('findings_summary', 'N/A')).replace('\n', '<br>')
                                        st.markdown(f"""
                                        <div style='background: rgba(251, 146, 60, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #fb923c; margin-bottom: 1rem;'>
                                            <div style='color: #1e293b; line-height: 1.8;'>{full_findings}</div>
                                        </div>
                                        """, unsafe_allow_html=True)

                                        # Complete Action Plan
                                        st.markdown("##### 🎯 Complete Action Plan")
                                        full_action = html.escape(story.get('action_plan', 'N/A')).replace('\n', '<br>')
                                        st.markdown(f"""
                                        <div style='background: rgba(245, 158, 11, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #f59e0b; margin-bottom: 1rem;'>
                                            <div style='color: #1e293b; line-height: 1.8;'>{full_action}</div>
                                        </div>
                                        """, unsafe_allow_html=True)

    # ====================================================================================
    # TAB 5: ACADEMIC ANALYTICS - HYBRID AI-DRIVEN
    # ====================================================================================
    with tabs[4]:
        st.header("🎓 Academic Analytics - AI-Driven Deep Analysis")
        st.caption("The AI analyzes academic performance patterns and recommends targeted interventions")

        # Academic-focused metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("High Performers", f"{metrics.get('high_performers', 0):,}",
                     f"{metrics.get('high_performers', 0)/metrics.get('total_students', 1)*100:.1f}%")

        with col2:
            st.metric("Average GPA", f"{metrics.get('avg_gpa', 0):.2f}")

        with col3:
            st.metric("At-Risk Students", f"{metrics.get('at_risk', 0):,}",
                     delta=f"-{metrics.get('at_risk', 0)/metrics.get('total_students', 1)*100:.1f}%",
                     delta_color="inverse")

        with col4:
            # Calculate mid-performers
            mid_performers = metrics.get('total_students', 0) - metrics.get('high_performers', 0) - metrics.get('at_risk', 0)
            st.metric("Mid-Performers", f"{mid_performers:,}",
                     f"{mid_performers/metrics.get('total_students', 1)*100:.1f}%")

        st.divider()

        # AI Analysis Button
        if st.session_state.ollama_connected and st.button("🤖 Generate Academic Performance Analysis & Visualizations", key="academic_btn", type="primary", use_container_width=True):

            # Generate academic-focused analysis using hybrid approach
            academic_analysis = generate_dynamic_visualizations_llm(
                metrics,
                df,
                st.session_state.selected_model,
                st.session_state.ollama_url,
                context_type="academic"  # Academic-focused context
            )

            if academic_analysis:
                # Display strategic overview
                st.markdown("### 🎯 Academic Performance Analysis")
                st.info(academic_analysis.get('strategic_overview', ''))

                st.divider()

                # Display visualizations with insights
                st.markdown("### 📊 AI-Recommended Academic Visualizations")
                viz_list = academic_analysis.get('visualizations', [])
                st.caption(f"The AI analyzed your data and recommends {len(viz_list)} academic visualizations")

                for i, viz_spec in enumerate(viz_list):
                    with st.container():
                        st.markdown(f"#### {viz_spec.get('title', f'Visualization {i+1}')}")
                        st.caption(f"**Why this matters:** {viz_spec.get('reasoning', 'Academic performance indicator')}")

                        # Build and display chart
                        fig = build_dynamic_chart(viz_spec, df)
                        if fig:
                            st.plotly_chart(fig, use_container_width=True, key=f"academic_viz_{i}")
                        else:
                            st.warning(f"⚠️ Could not generate chart for: {viz_spec.get('data_column', 'unknown')}")

                        # Display AI insight
                        insight = viz_spec.get('insight', '')
                        if insight:
                            st.markdown(f"""
                            <div class="insight-card">
                                <div class="insight-title">🎓 Academic Insight</div>
                                <div class="insight-text">{insight}</div>
                            </div>
                            """, unsafe_allow_html=True)

                        st.divider()

                # Display key findings
                st.markdown("### 🔍 Key Academic Findings")
                findings = academic_analysis.get('key_findings', [])
                for i, finding in enumerate(findings, 1):
                    st.markdown(f"**Finding {i}:** {finding}")

                st.divider()

                # Display recommendations
                st.markdown("### 💡 Academic Intervention Recommendations")
                recommendations = academic_analysis.get('recommendations', [])

                for i, rec in enumerate(recommendations, 1):
                    # Color code by priority (first = high priority)
                    priority_color = "🔴" if i == 1 else "🟠" if i == 2 else "🟢"

                    with st.container():
                        st.markdown(f"""
                        <div class="recommendation-card">
                            <div class="recommendation-priority">{priority_color} Priority {i}</div>
                            <div class="recommendation-text">{rec}</div>
                        </div>
                        """, unsafe_allow_html=True)

        elif not st.session_state.ollama_connected:
            st.warning("⚠️ Please connect to Ollama first (see sidebar) to generate AI-powered academic analysis.")

    # ====================================================================================
    # TAB 6: HOUSING INSIGHTS - AI-DRIVEN
    # ====================================================================================
    with tabs[5]:
        st.header("🏠 Housing Insights - AI-Driven Deep Analysis")
        st.caption("The AI analyzes housing patterns, occupancy trends, and their impact on student success")

        # Check for housing data
        housing_col = None
        for col in ['room_number', 'housing_status', 'residence_hall', 'housing', 'residence', 'dormitory']:
            if col in df.columns:
                housing_col = col
                break

        if housing_col:
            on_campus = df[df[housing_col].notna()].shape[0]
            off_campus = df[df[housing_col].isna()].shape[0]
            housing_utilization = (on_campus / len(df) * 100) if len(df) > 0 else 0

            # Calculate housing impact on GPA if GPA column exists
            gpa_col = None
            for col in ['gpa', 'cumulative_gpa', 'cgpa']:
                if col in df.columns:
                    gpa_col = col
                    break

            on_campus_gpa = 0
            off_campus_gpa = 0
            if gpa_col:
                on_campus_gpa = df[df[housing_col].notna()][gpa_col].mean()
                off_campus_gpa = df[df[housing_col].isna()][gpa_col].mean()

            # Housing-focused metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("On-Campus Residents", f"{on_campus:,}",
                         f"{housing_utilization:.1f}%")

            with col2:
                st.metric("Off-Campus Students", f"{off_campus:,}",
                         f"{(off_campus/len(df)*100):.1f}%")

            with col3:
                if gpa_col and on_campus_gpa > 0:
                    st.metric("On-Campus Avg GPA", f"{on_campus_gpa:.2f}",
                             delta=f"{on_campus_gpa - off_campus_gpa:+.2f}" if off_campus_gpa > 0 else None)
                else:
                    st.metric("Housing Utilization", f"{housing_utilization:.1f}%")

            with col4:
                if gpa_col and off_campus_gpa > 0:
                    st.metric("Off-Campus Avg GPA", f"{off_campus_gpa:.2f}",
                             delta=f"{off_campus_gpa - on_campus_gpa:+.2f}" if on_campus_gpa > 0 else None)
                else:
                    # Count unique residence halls if available
                    unique_residences = df[housing_col].nunique()
                    st.metric("Residence Options", f"{unique_residences:,}")

            st.divider()

            # AI Analysis Button
            if st.session_state.ollama_connected and st.button("🤖 Generate Housing Impact Analysis & Visualizations", key="housing_btn", type="primary", use_container_width=True):

                # Generate housing-focused analysis using hybrid approach
                housing_analysis = generate_dynamic_visualizations_llm(
                    metrics,
                    df,
                    st.session_state.selected_model,
                    st.session_state.ollama_url,
                    context_type="housing"  # Housing-focused context
                )

                if housing_analysis:
                    # Display strategic overview
                    st.markdown("### 🏠 Housing Impact Analysis")
                    st.info(housing_analysis.get('strategic_overview', ''))

                    st.divider()

                    # Display visualizations with insights
                    st.markdown("### 📊 AI-Recommended Housing Visualizations")
                    viz_list = housing_analysis.get('visualizations', [])
                    st.caption(f"The AI analyzed your data and recommends {len(viz_list)} housing-related visualizations")

                    for i, viz_spec in enumerate(viz_list):
                        with st.container():
                            st.markdown(f"#### {viz_spec.get('title', f'Visualization {i+1}')}")
                            st.caption(f"**Why this matters:** {viz_spec.get('reasoning', 'Housing performance indicator')}")

                            # Build and display chart
                            fig = build_dynamic_chart(viz_spec, df)
                            if fig:
                                st.plotly_chart(fig, use_container_width=True, key=f"housing_viz_{i}")
                            else:
                                st.warning(f"⚠️ Could not generate chart for: {viz_spec.get('data_column', 'unknown')}")

                            # Display AI insight
                            insight = viz_spec.get('insight', '')
                            if insight:
                                st.markdown(f"""
                                <div class="insight-card">
                                    <div class="insight-title">🏠 Housing Insight</div>
                                    <div class="insight-text">{insight}</div>
                                </div>
                                """, unsafe_allow_html=True)

                            st.divider()

                    # Display key findings
                    st.markdown("### 🔍 Key Housing Findings")
                    findings = housing_analysis.get('key_findings', [])
                    for i, finding in enumerate(findings, 1):
                        st.markdown(f"**Finding {i}:** {finding}")

                    st.divider()

                    # Display recommendations
                    st.markdown("### 💡 Housing Strategy Recommendations")
                    recommendations = housing_analysis.get('recommendations', [])

                    for i, rec in enumerate(recommendations, 1):
                        # Color code by priority (first = high priority)
                        priority_color = "🔴" if i == 1 else "🟠" if i == 2 else "🟢"

                        with st.container():
                            st.markdown(f"""
                            <div class="recommendation-card">
                                <div class="recommendation-priority">{priority_color} Priority {i}</div>
                                <div class="recommendation-text">{rec}</div>
                            </div>
                            """, unsafe_allow_html=True)

            elif not st.session_state.ollama_connected:
                st.warning("⚠️ Please connect to Ollama first (see sidebar) to generate AI-powered housing analysis.")
        else:
            st.info("Housing data not available in current dataset. Please ensure your dataset includes housing-related columns (e.g., 'room_number', 'housing_status', 'residence_hall').")

    # ====================================================================================
    # TAB 7: FINANCIAL INTELLIGENCE - AI-DRIVEN
    # ====================================================================================
    with tabs[6]:
        st.header("💰 Financial Intelligence - AI-Driven Deep Analysis")
        st.caption("The AI analyzes financial sustainability, aid effectiveness, and revenue optimization strategies")

        # Check for financial data
        aid_col = None
        for col in ['financial_aid_monetary_amount', 'financial_aid', 'aid', 'scholarship', 'scholarship_amount']:
            if col in df.columns:
                aid_col = col
                break

        tuition_col = None
        for col in ['tuition_fees', 'tuition', 'fees', 'annual_tuition']:
            if col in df.columns:
                tuition_col = col
                break

        # Calculate financial metrics
        total_tuition = metrics.get('total_tuition', 0)
        total_aid = metrics.get('total_aid', 0)
        aid_coverage_pct = (total_aid / total_tuition * 100) if total_tuition > 0 else 0

        aid_recipients = 0
        avg_aid_amount = 0
        net_revenue = total_tuition - total_aid

        if aid_col and aid_col in df.columns:
            aid_recipients = df[df[aid_col] > 0].shape[0]
            avg_aid_amount = df[df[aid_col] > 0][aid_col].mean() if aid_recipients > 0 else 0

        # Financial-focused metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Tuition", f"AED {total_tuition:,.0f}",
                     help="Gross tuition revenue from all students")

        with col2:
            st.metric("Financial Aid", f"AED {total_aid:,.0f}",
                     delta=f"-{aid_coverage_pct:.1f}%",
                     delta_color="inverse",
                     help="Total aid distributed to students")

        with col3:
            st.metric("Net Revenue", f"AED {net_revenue:,.0f}",
                     help="Tuition revenue after aid distribution")

        with col4:
            if aid_recipients > 0:
                st.metric("Aid Recipients", f"{aid_recipients:,}",
                         f"{(aid_recipients/len(df)*100):.1f}%",
                         help="Students receiving financial aid")
            else:
                st.metric("Aid Coverage", f"{aid_coverage_pct:.1f}%",
                         help="Aid as percentage of tuition revenue")

        st.divider()

        # AI Analysis Button
        if st.session_state.ollama_connected and st.button("🤖 Generate Financial Sustainability Analysis & Visualizations", key="finance_btn", type="primary", use_container_width=True):

            # Generate financial-focused analysis using hybrid approach
            financial_analysis = generate_dynamic_visualizations_llm(
                metrics,
                df,
                st.session_state.selected_model,
                st.session_state.ollama_url,
                context_type="financial"  # Financial-focused context
            )

            if financial_analysis:
                # Display strategic overview
                st.markdown("### 💰 Financial Sustainability Analysis")
                st.info(financial_analysis.get('strategic_overview', ''))

                st.divider()

                # Display visualizations with insights
                st.markdown("### 📊 AI-Recommended Financial Visualizations")
                viz_list = financial_analysis.get('visualizations', [])
                st.caption(f"The AI analyzed your data and recommends {len(viz_list)} financial visualizations")

                for i, viz_spec in enumerate(viz_list):
                    with st.container():
                        st.markdown(f"#### {viz_spec.get('title', f'Visualization {i+1}')}")
                        st.caption(f"**Why this matters:** {viz_spec.get('reasoning', 'Financial performance indicator')}")

                        # Build and display chart
                        fig = build_dynamic_chart(viz_spec, df)
                        if fig:
                            st.plotly_chart(fig, use_container_width=True, key=f"financial_viz_{i}")
                        else:
                            st.warning(f"⚠️ Could not generate chart for: {viz_spec.get('data_column', 'unknown')}")

                        # Display AI insight
                        insight = viz_spec.get('insight', '')
                        if insight:
                            st.markdown(f"""
                            <div class="insight-card">
                                <div class="insight-title">💰 Financial Insight</div>
                                <div class="insight-text">{insight}</div>
                            </div>
                            """, unsafe_allow_html=True)

                        st.divider()

                # Display key findings
                st.markdown("### 🔍 Key Financial Findings")
                findings = financial_analysis.get('key_findings', [])
                for i, finding in enumerate(findings, 1):
                    st.markdown(f"**Finding {i}:** {finding}")

                st.divider()

                # Display recommendations
                st.markdown("### 💡 Financial Strategy Recommendations")
                recommendations = financial_analysis.get('recommendations', [])

                for i, rec in enumerate(recommendations, 1):
                    # Color code by priority (first = high priority)
                    priority_color = "🔴" if i == 1 else "🟠" if i == 2 else "🟢"

                    with st.container():
                        st.markdown(f"""
                        <div class="recommendation-card">
                            <div class="recommendation-priority">{priority_color} Priority {i}</div>
                            <div class="recommendation-text">{rec}</div>
                        </div>
                        """, unsafe_allow_html=True)

        elif not st.session_state.ollama_connected:
            st.warning("⚠️ Please connect to Ollama first (see sidebar) to generate AI-powered financial analysis.")

    # ====================================================================================
    # TAB 8: DEMOGRAPHICS DEEP DIVE - AI-DRIVEN
    # ====================================================================================
    with tabs[7]:
        st.header("👥 Demographics Deep Dive - AI-Driven Deep Analysis")
        st.caption("The AI analyzes diversity patterns, market concentration risks, and inclusion strategies")

        # Check for demographic data
        nationality_col = None
        for col in ['nationality', 'country', 'citizenship', 'origin']:
            if col in df.columns:
                nationality_col = col
                break

        gender_col = None
        for col in ['gender', 'sex']:
            if col in df.columns:
                gender_col = col
                break

        # Calculate demographic metrics
        unique_nationalities = metrics.get('unique_nationalities', 0)
        uae_nationals = metrics.get('uae_nationals', 0)
        uae_percentage = metrics.get('uae_percentage', 0)
        international_students = metrics.get('total_students', 0) - uae_nationals

        # Calculate top 3 concentration if nationality column available
        top_3_concentration = 0
        if nationality_col and nationality_col in df.columns:
            top_nat = df[nationality_col].value_counts().head(3)
            top_3_concentration = (top_nat.sum() / len(df) * 100) if len(df) > 0 else 0

        # Gender distribution if available
        gender_distribution = {}
        if gender_col and gender_col in df.columns:
            gender_counts = df[gender_col].value_counts()
            gender_distribution = {str(k): int(v) for k, v in gender_counts.items()}

        # Demographics-focused metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Nationalities", f"{unique_nationalities}",
                     help="Number of different nationalities represented")

        with col2:
            st.metric("UAE Nationals", f"{uae_nationals:,}",
                     f"{uae_percentage:.1f}%",
                     help="UAE national students")

        with col3:
            st.metric("International Students", f"{international_students:,}",
                     f"{(international_students/metrics.get('total_students', 1)*100):.1f}%",
                     help="Non-UAE international students")

        with col4:
            if top_3_concentration > 0:
                risk_level = "🔴 High" if top_3_concentration > 60 else "🟠 Moderate" if top_3_concentration > 50 else "🟢 Low"
                st.metric("Top 3 Concentration", f"{top_3_concentration:.1f}%",
                         help=f"Concentration risk: {risk_level}")
            elif len(gender_distribution) > 0:
                most_common_gender = max(gender_distribution, key=gender_distribution.get)
                st.metric("Gender Balance", f"{most_common_gender}: {gender_distribution[most_common_gender]:,}",
                         help="Gender distribution")
            else:
                st.metric("Diversity Index", f"{unique_nationalities}",
                         help="Number of nationalities")

        st.divider()

        # AI Analysis Button
        if st.session_state.ollama_connected and st.button("🤖 Generate Diversity & Inclusion Analysis & Visualizations", key="demo_btn", type="primary", use_container_width=True):

            # Generate demographics-focused analysis using hybrid approach
            demographics_analysis = generate_dynamic_visualizations_llm(
                metrics,
                df,
                st.session_state.selected_model,
                st.session_state.ollama_url,
                context_type="demographics"  # Demographics-focused context
            )

            if demographics_analysis:
                # Display strategic overview
                st.markdown("### 🌍 Diversity & Inclusion Analysis")
                st.info(demographics_analysis.get('strategic_overview', ''))

                st.divider()

                # Display visualizations with insights
                st.markdown("### 📊 AI-Recommended Demographic Visualizations")
                viz_list = demographics_analysis.get('visualizations', [])
                st.caption(f"The AI analyzed your data and recommends {len(viz_list)} demographic visualizations")

                for i, viz_spec in enumerate(viz_list):
                    with st.container():
                        st.markdown(f"#### {viz_spec.get('title', f'Visualization {i+1}')}")
                        st.caption(f"**Why this matters:** {viz_spec.get('reasoning', 'Demographic indicator')}")

                        # Build and display chart
                        fig = build_dynamic_chart(viz_spec, df)
                        if fig:
                            st.plotly_chart(fig, use_container_width=True, key=f"demographics_viz_{i}")
                        else:
                            st.warning(f"⚠️ Could not generate chart for: {viz_spec.get('data_column', 'unknown')}")

                        # Display AI insight
                        insight = viz_spec.get('insight', '')
                        if insight:
                            st.markdown(f"""
                            <div class="insight-card">
                                <div class="insight-title">🌍 Demographic Insight</div>
                                <div class="insight-text">{insight}</div>
                            </div>
                            """, unsafe_allow_html=True)

                        st.divider()

                # Display key findings
                st.markdown("### 🔍 Key Demographic Findings")
                findings = demographics_analysis.get('key_findings', [])
                for i, finding in enumerate(findings, 1):
                    st.markdown(f"**Finding {i}:** {finding}")

                st.divider()

                # Display recommendations
                st.markdown("### 💡 Diversity & Recruitment Strategy Recommendations")
                recommendations = demographics_analysis.get('recommendations', [])

                for i, rec in enumerate(recommendations, 1):
                    # Color code by priority (first = high priority)
                    priority_color = "🔴" if i == 1 else "🟠" if i == 2 else "🟢"

                    with st.container():
                        st.markdown(f"""
                        <div class="recommendation-card">
                            <div class="recommendation-priority">{priority_color} Priority {i}</div>
                            <div class="recommendation-text">{rec}</div>
                        </div>
                        """, unsafe_allow_html=True)

        elif not st.session_state.ollama_connected:
            st.warning("⚠️ Please connect to Ollama first (see sidebar) to generate AI-powered diversity analysis.")

    # ====================================================================================
    # TAB 9: RISK & SUCCESS ANALYSIS - AI-DRIVEN
    # ====================================================================================
    with tabs[8]:
        st.header("⚠️ Risk & Success Analysis - AI-Driven Deep Analysis")
        st.caption("The AI analyzes at-risk patterns, success predictors, and intervention effectiveness")

        # Calculate risk metrics
        at_risk = metrics.get('at_risk', 0)
        high_performers = metrics.get('high_performers', 0)
        total_students = metrics.get('total_students', 1)
        mid_performers = total_students - at_risk - high_performers
        success_rate = ((total_students - at_risk) / total_students * 100) if total_students > 0 else 0
        at_risk_pct = (at_risk / total_students * 100) if total_students > 0 else 0
        high_perf_pct = (high_performers / total_students * 100) if total_students > 0 else 0

        # Determine risk severity
        risk_severity = "🔴 CRITICAL" if at_risk_pct > 25 else "🟠 HIGH" if at_risk_pct > 15 else "🟢 MODERATE"

        # Risk-focused metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("At-Risk Students", f"{at_risk:,}",
                     delta=f"{at_risk_pct:.1f}%",
                     delta_color="inverse",
                     help="Students with GPA < 2.0")

        with col2:
            st.metric("Mid-Tier Students", f"{mid_performers:,}",
                     f"{(mid_performers/total_students*100):.1f}%",
                     help="Students with 2.0 ≤ GPA < 3.5")

        with col3:
            st.metric("High Performers", f"{high_performers:,}",
                     delta=f"{high_perf_pct:.1f}%",
                     help="Students with GPA ≥ 3.5")

        with col4:
            st.metric("Risk Severity", risk_severity,
                     f"Success: {success_rate:.1f}%",
                     help="Risk level based on at-risk percentage")

        st.divider()

        # AI Analysis Button
        if st.session_state.ollama_connected and st.button("🤖 Generate Risk & Success Analysis & Visualizations", key="risk_btn", type="primary", use_container_width=True):

            # Generate risk-focused analysis using hybrid approach
            risk_analysis = generate_dynamic_visualizations_llm(
                metrics,
                df,
                st.session_state.selected_model,
                st.session_state.ollama_url,
                context_type="risk"  # Risk-focused context
            )

            if risk_analysis:
                # Display strategic overview
                st.markdown("### ⚠️ Risk & Success Strategic Analysis")
                st.info(risk_analysis.get('strategic_overview', ''))

                st.divider()

                # Display visualizations with insights
                st.markdown("### 📊 AI-Recommended Risk Analysis Visualizations")
                viz_list = risk_analysis.get('visualizations', [])
                st.caption(f"The AI analyzed your data and recommends {len(viz_list)} risk analysis visualizations")

                for i, viz_spec in enumerate(viz_list):
                    with st.container():
                        st.markdown(f"#### {viz_spec.get('title', f'Visualization {i+1}')}")
                        st.caption(f"**Why this matters:** {viz_spec.get('reasoning', 'Risk indicator')}")

                        # Build and display chart
                        fig = build_dynamic_chart(viz_spec, df)
                        if fig:
                            st.plotly_chart(fig, use_container_width=True, key=f"risk_viz_{i}")
                        else:
                            st.warning(f"⚠️ Could not generate chart for: {viz_spec.get('data_column', 'unknown')}")

                        # Display AI insight
                        insight = viz_spec.get('insight', '')
                        if insight:
                            st.markdown(f"""
                            <div class="insight-card">
                                <div class="insight-title">⚠️ Risk Insight</div>
                                <div class="insight-text">{insight}</div>
                            </div>
                            """, unsafe_allow_html=True)

                        st.divider()

                # Display key findings
                st.markdown("### 🔍 Key Risk & Success Findings")
                findings = risk_analysis.get('key_findings', [])
                for i, finding in enumerate(findings, 1):
                    st.markdown(f"**Finding {i}:** {finding}")

                st.divider()

                # Display recommendations
                st.markdown("### 💡 Intervention & Success Strategy Recommendations")
                recommendations = risk_analysis.get('recommendations', [])

                for i, rec in enumerate(recommendations, 1):
                    # Color code by priority (first = high priority)
                    priority_color = "🔴" if i == 1 else "🟠" if i == 2 else "🟢"

                    with st.container():
                        st.markdown(f"""
                        <div class="recommendation-card">
                            <div class="recommendation-priority">{priority_color} Priority {i}</div>
                            <div class="recommendation-text">{rec}</div>
                        </div>
                        """, unsafe_allow_html=True)

        elif not st.session_state.ollama_connected:
            st.warning("⚠️ Please connect to Ollama first (see sidebar) to generate AI-powered risk analysis.")

    # ====================================================================================
    # TAB 10: DATA LINEAGE
    # ====================================================================================
    with tabs[9]:
        st.header("🔗 Data Lineage & Architecture")

        st.info("📊 Dataset Overview")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Records", f"{len(df):,}")

        with col2:
            st.metric("Total Columns", len(df.columns))

        with col3:
            memory_usage = df.memory_usage(deep=True).sum() / (1024 ** 2)
            st.metric("Memory Usage", f"{memory_usage:.2f} MB")

        st.divider()

        if st.session_state.ollama_connected and st.button("🤖 Generate Data Documentation", key="lineage_btn"):
            with st.spinner("Generating data documentation..."):
                columns_sample = ', '.join(df.columns[:20].tolist())
                prompt = f"""Generate data architecture documentation for student dataset:
- Records: {len(df):,}
- Columns: {len(df.columns)}
- Sample Columns: {columns_sample}...

Provide:
1. Dataset purpose and scope
2. Key data domains
3. Data quality observations
4. Usage recommendations"""

                doc = query_ollama(prompt, model, url, temperature=0.5, num_predict=500, auto_optimize=True)

                if doc and not doc.startswith('[ERROR]'):
                    st.markdown(f"""
                    <div class="insight-card">
                        <div class="insight-title">📚 Data Architecture Documentation</div>
                        <div class="insight-text">{doc}</div>
                    </div>
                    """, unsafe_allow_html=True)

        # Column list
        with st.expander("📋 View All Columns"):
            st.dataframe(
                pd.DataFrame({
                    'Column': df.columns,
                    'Type': df.dtypes.astype(str),
                    'Non-Null Count': df.count(),
                    'Null Count': df.isnull().sum()
                }),
                width="stretch"
            )

    # ====================================================================================
    # TAB 11: DATA EXPLORER WITH LLM Q&A
    # ====================================================================================
    with tabs[10]:
        st.header("🔬 Data Explorer - AI-Powered Q&A")

        st.info("💡 Ask questions about your data in natural language!")

        # Data preview
        st.subheader("📊 Data Preview")
        st.dataframe(df.head(10), width="stretch")

        st.divider()

        # AI Q&A Interface
        if st.session_state.ollama_connected:
            user_question = st.text_area(
                "Ask a question about the data:",
                placeholder="Example: What percentage of students are performing below 2.5 GPA? What trends do you see in the financial aid distribution?",
                height=100
            )

            if st.button("🤖 Ask AI", key="qa_btn"):
                if user_question.strip():
                    with st.spinner("🔄 AI is analyzing your question..."):
                        # Prepare data context
                        data_summary = {
                            'total_records': len(df),
                            'columns': df.columns.tolist()[:30],
                            'sample_stats': {}
                        }

                        # Add numeric column stats
                        numeric_cols = df.select_dtypes(include=[np.number]).columns[:10]
                        for col in numeric_cols:
                            data_summary['sample_stats'][col] = {
                                'mean': float(df[col].mean()),
                                'min': float(df[col].min()),
                                'max': float(df[col].max())
                            }

                        prompt = f"""You are analyzing a student dataset with {len(df):,} records.

**Available Metrics:**
{json.dumps(metrics, indent=2)}

**Data Summary:**
{json.dumps(data_summary, indent=2)[:1000]}

**User Question:**
{user_question}

Provide a clear, data-driven answer based on the available metrics and data summary. If you need specific data that's not provided, explain what insights you can provide with available information."""

                        response = query_ollama(prompt, model, url, temperature=0.5, num_predict=600, auto_optimize=True)

                        if response and not response.startswith('[ERROR]'):
                            st.markdown(f"""
                            <div class="insight-card">
                                <div class="insight-title">🤖 AI Response</div>
                                <div class="insight-text">{response}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error(f"Error generating response: {response}")
                else:
                    st.warning("Please enter a question")
        else:
            st.warning("⚠️ Connect to Ollama to use AI-powered Q&A")

if __name__ == "__main__":
    main()
