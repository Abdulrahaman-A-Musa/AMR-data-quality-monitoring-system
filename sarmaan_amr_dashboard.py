# ================================
# SARMAAN II AMR SOKOTO STATE - QC DASHBOARD
# Advanced Quality Control Dashboard for Antimicrobial Resistance Study
# ================================

from datetime import date
import pandas as pd
import streamlit as st
import requests
from io import BytesIO
import plotly.express as px
import plotly.graph_objects as go

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="SARMAAN II AMR Dashboard - Sokoto State",
    layout="wide",
    initial_sidebar_state="auto",  # Auto-collapse on mobile
    page_icon="🏥"
)

# ---------------- ADMIN CREDENTIALS ----------------
ADMIN_USERNAME = "admin"

# ---------------- CUSTOM CSS STYLING ----------------
st.markdown(
    """
    <style>
    /* Main Theme Colors */
    :root {
        --primary-blue: #1e3a8a;
        --secondary-teal: #0d9488;
        --accent-orange: #f97316;
        --success-green: #10b981;
        --danger-red: #ef4444;
        --warning-yellow: #fbbf24;
        --bg-light: #f8fafc;
        --text-dark: #1e293b;
    }
    
    /* Global Styles */
    .main { background-color: var(--bg-light); }
    
    /* Ensure content fits mobile screens */
    * {
        box-sizing: border-box;
        max-width: 100%;
    }
    
    /* Header Styles */
    .dashboard-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #0d9488 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    .dashboard-title {
        font-size: 2.8em;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .dashboard-subtitle {
        font-size: 1.2em;
        opacity: 0.95;
        margin-top: 0.5rem;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.2rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-left: 5px solid var(--primary-blue);
        transition: all 0.3s ease;
        text-align: center;
        min-height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
    }
    
    .metric-value {
        font-size: 2.8rem;
        font-weight: 800;
        color: var(--primary-blue);
        margin: 0;
        line-height: 1;
        letter-spacing: -1px;
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.5rem;
    }
    
    .metric-delta {
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    /* QC Status Badge */
    .qc-badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    .qc-success { background: #d1fae5; color: #065f46; }
    .qc-warning { background: #fef3c7; color: #92400e; }
    .qc-danger { background: #fee2e2; color: #991b1b; }
    .qc-info { background: #dbeafe; color: #1e40af; }
    
    /* Section Headers */
    .section-header {
        background: linear-gradient(90deg, #f8fafc 0%, white 100%);
        padding: 1rem 1.5rem;
        border-left: 5px solid var(--secondary-teal);
        border-radius: 8px;
        margin: 2rem 0 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-dark);
        margin: 0;
    }
    
    /* Sidebar Styling */
    .stSidebar {
        background: linear-gradient(180deg, #1e3a8a 0%, #0d9488 100%);
    }
    
    .stSidebar [data-testid="stSidebarNav"] {
        background-color: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stSidebar .stSelectbox label,
    .stSidebar .stMultiSelect label {
        color: white !important;
        font-weight: 600;
    }
    
    /* Login Page */
    .login-container {
        max-width: 450px;
        margin: 5rem auto;
        padding: 3rem;
        background: white;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .login-title {
        text-align: center;
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-blue);
        margin-bottom: 2rem;
    }
    
    /* Data Tables */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    /* Alert Boxes */
    .alert-box {
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid;
    }
    
    .alert-danger {
        background: #fee2e2;
        border-color: #ef4444;
        color: #991b1b;
    }
    
    .alert-warning {
        background: #fef3c7;
        border-color: #fbbf24;
        color: #92400e;
    }
    
    .alert-success {
        background: #d1fae5;
        border-color: #10b981;
        color: #065f46;
    }
    
    .alert-info {
        background: #dbeafe;
        border-color: #3b82f6;
        color: #1e40af;
    }
    
    /* User Badge */
    .user-badge {
        background: rgba(255,255,255,0.2);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 600;
        display: inline-block;
        margin: 0.5rem 0;
    }
    
    /* Progress Bar */
    .progress-bar {
        height: 8px;
        background: #e5e7eb;
        border-radius: 10px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--secondary-teal), var(--primary-blue));
        transition: width 0.3s ease;
    }
    
    /* Button Styles */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Responsive Design for Mobile */
    @media (max-width: 768px) {
        /* Reduce padding and margins */
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 1rem !important;
        }
        
        .dashboard-title { 
            font-size: 1.5rem; 
        }
        
        .dashboard-subtitle {
            font-size: 0.9rem;
        }
        
        .metric-card {
            padding: 0.8rem 0.5rem;
            min-height: 80px;
            margin-bottom: 0.5rem;
        }
        
        .metric-value { 
            font-size: 1.8rem; 
        }
        
        .metric-label {
            font-size: 0.65rem;
        }
        
        .section-header {
            padding: 0.8rem 1rem;
            margin: 1rem 0 0.5rem 0;
        }
        
        .section-title {
            font-size: 1.1rem;
        }
        
        .dashboard-header {
            padding: 1.2rem;
            margin-bottom: 1rem;
        }
        
        /* Make tables scroll horizontally on mobile */
        .dataframe {
            overflow-x: auto;
            font-size: 0.85rem;
        }
        
        /* Streamlit columns stack on mobile */
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }
        
        /* Better spacing for metrics */
        [data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
        }
        
        [data-testid="stMetricLabel"] {
            font-size: 0.8rem !important;
        }
        
        /* Login container on mobile */
        .login-container {
            margin: 2rem auto;
            padding: 1.5rem;
        }
        
        .login-title {
            font-size: 1.5rem;
        }
        
        /* Sidebar on mobile */
        .stSidebar {
            width: 100% !important;
        }
        
        /* Charts on mobile */
        .js-plotly-plot {
            width: 100% !important;
        }
        
        /* Button full width on mobile */
        .stButton > button {
            width: 100%;
            margin-bottom: 0.5rem;
        }
    }
    
    @media (max-width: 480px) {
        /* Extra small phones */
        .main .block-container {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
        
        .dashboard-title { 
            font-size: 1.2rem; 
        }
        
        .dashboard-subtitle {
            font-size: 0.75rem;
        }
        
        .metric-value { 
            font-size: 1.5rem; 
        }
        
        .metric-label {
            font-size: 0.6rem;
        }
        
        .metric-card {
            padding: 0.6rem 0.4rem;
            min-height: 70px;
        }
        
        .section-title {
            font-size: 1rem;
        }
        
        .dashboard-header {
            padding: 1rem;
            border-radius: 10px;
        }
        
        /* Tables with smaller text */
        .dataframe {
            font-size: 0.75rem;
        }
        
        /* Form inputs full width */
        .stTextInput > div > div > input {
            font-size: 1rem;
        }
        
        /* Selectbox full width */
        .stSelectbox, .stMultiSelect {
            width: 100%;
        }
        
        /* Expander on mobile */
        .streamlit-expanderHeader {
            font-size: 0.9rem;
        }
    }
    
    /* Landscape phones */
    @media (max-width: 900px) and (orientation: landscape) {
        .dashboard-header {
            padding: 1rem;
        }
        
        .metric-card {
            min-height: 70px;
            padding: 0.6rem;
        }
        
        .metric-value {
            font-size: 1.6rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- DATA SOURCE ----------------
DATA_URL = st.secrets.get("DATA_URL", "")
MAIN_SHEET = "SARMAAN II C3 SOKOTO AMR TRA..."
MOTHER_SHEET = "mother_information"
CHILD_SHEET = "child_info"

# ---------------- SESSION STATE INITIALIZATION ----------------
# Auto-login as Admin (set to False to enable login page)
AUTO_LOGIN_ADMIN = False

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = AUTO_LOGIN_ADMIN
if 'current_user' not in st.session_state:
    st.session_state.current_user = ADMIN_USERNAME if AUTO_LOGIN_ADMIN else None
if 'user_role' not in st.session_state:
    st.session_state.user_role = 'admin' if AUTO_LOGIN_ADMIN else None
if 'refresh_count' not in st.session_state:
    st.session_state.refresh_count = 0
if 'selected_lga' not in st.session_state:
    st.session_state.selected_lga = "All"

# ---------------- COMMUNITY MAPPING DATA ----------------
COMMUNITY_MAP_DATA = """state,lga,ward,Community,communitycode,Planned_Community
# Sokoto,Binji,Binji,Gidan Ayya,C3-70111,7
# Sokoto,Binji,Binji,Gidan Garba Daji,C3-70112,6
# Sokoto,Binji,Bunkari,Danmali Yamma,C3-70121,10
# Sokoto,Binji,Bunkari,Gidan Buji,C3-70122,8
# Sokoto,Binji,Gawazai,Bani Zumbu,C3-70131,68
# Sokoto,Binji,Gawazai,Gidan Baba Tulu,C3-70132,6
# Sokoto,Binji,Inname,Faruwa,C3-70141,14
# Sokoto,Binji,Inname,Ginjo,C3-70142,6
# Sokoto,Binji,Jamali,Daddale,C3-70151,14
# Sokoto,Binji,Jamali,Jamali Tsohuwa,C3-70152,22
# Sokoto,Bodinga,Bagarawa,Akayi Ii,C3-70211,16
# Sokoto,Bodinga,Bagarawa,Amanawa,C3-70212,13
# Sokoto,Bodinga,Bangidabaga,Batsauje Shiyar Barade,C3-70221,15
# Sokoto,Bodinga,Bangidabaga,Illela Shiyar Marafa,C3-70222,22
# Sokoto,Bodinga,Bodingatauma,Shiyar Danjekaandi,C3-70231,20
# Sokoto,Bodinga,Bodingatauma,Shiyar Sarki Marafa,C3-70232,12
# Sokoto,Bodinga,Danchadi,Gidandan Bubes Magaji,C3-70241,16
# Sokoto,Bodinga,Danchadi,Kanwuri B,C3-70242,16
# Sokoto,Bodinga,Darhelabadau,Dabagi,C3-70251,15
# Sokoto,Bodinga,Darhelabadau,Tuntsure,C3-70252,15
# Sokoto,Dangeshuni,Bodai,Babban Gida,C3-70311,26
# Sokoto,Dangeshuni,Bodai,Kaura Magaji Gabas,C3-70312,18
# Sokoto,Dangeshuni,Dange,Nasarawa Gabas,C3-70321,18
# Sokoto,Dangeshuni,Dange,Rini,C3-70322,10
# Sokoto,Dangeshuni,Fajaldu,Adarawa Yamma,C3-70331,12
# Sokoto,Dangeshuni,Fajaldu,Bislem Yamma,C3-70332,14
# Sokoto,Dangeshuni,Geeregajara,Bagai Sama,C3-70341,11
# Sokoto,Dangeshuni,Geeregajara,Danwardi,C3-70342,15
# Sokoto,Dangeshuni,Rikina,Bubari Babba,C3-70351,12
# Sokoto,Dangeshuni,Rikina,Bubari Karama,C3-70352,26
# Sokoto,Gada,Dukamaje,Gidan Karo Shiyar Masallaci,C3-70411,14
# Sokoto,Gada,Dukamaje,Tsuga Hayi,C3-70412,13
# Sokoto,Gada,Gilbadi,Batan Warka,C3-70421,13
# Sokoto,Gada,Gilbadi,Batan Warka Shiyar Gabas,C3-70422,16
# Sokoto,Gada,Kadadi,Busaragi,C3-70431,13
# Sokoto,Gada,Kadadi,Kadadi Shiyar Hakimi,C3-70432,14
# Sokoto,Gada,Kaddi,Arawa Shiyar Dan Sarki,C3-70441,23
# Sokoto,Gada,Kaddi,Arawa Shiyar Masallaci,C3-70442,30
# Sokoto,Gada,Kaffe,Alibawa Shiyar Gidan Fako,C3-70451,12
# Sokoto,Gada,Kaffe,Dantudu Shiyar Madawaki,C3-70452,13
# Sokoto,Goronyo,Birjingo,Akuzo,C3-70511,16
# Sokoto,Goronyo,Birjingo,Danya,C3-70512,5
# Sokoto,Goronyo,Boyekai,Gidan Bawa Malaba,C3-70521,25
# Sokoto,Goronyo,Boyekai,Gidan Marafa Shiyar Yamma,C3-70522,5
# Sokoto,Goronyo,Giyawa,Akuzo,C3-70531,9
# Sokoto,Goronyo,Giyawa,Galbace C,C3-70532,15
# Sokoto,Goronyo,Goronyo,Dan Rairai,C3-70541,11
# Sokoto,Goronyo,Goronyo,Gadon Mata Shiyar Gabas B,C3-70542,26
# Sokoto,Goronyo,Kagara,Balla Sabon Gari A,C3-70551,24
# Sokoto,Goronyo,Kagara,Dan Jiro,C3-70552,25
# Sokoto,Gudu,Awilkiti,Awulkitikware,C3-70611,11
# Sokoto,Gudu,Awilkiti,Barebari,C3-70612,11
# Sokoto,Gudu,Bachaka,Unguwar Huri,C3-70621,7
# Sokoto,Gudu,Bachaka,Kukar Geza,C3-70622,5
# Sokoto,Gudu,Balle,Balle Shiyar Dosawa,C3-70631,6
# Sokoto,Gudu,Balle,Gidan Rabo,C3-70632,6
# Sokoto,Gudu,Chilas,Chilas Gabas,C3-70641,89
# Sokoto,Gudu,Chilas,Dangadabro Gabas,C3-70642,11
# Sokoto,Gudu,Gwazange,Boto Shiyar Gube,C3-70651,6
# Sokoto,Gudu,Gwazange,Boto Shiyar Kasuwa,C3-70652,10
# Sokoto,Gwadabawa,Asara,Birnidil,C3-70711,11
# Sokoto,Gwadabawa,Asara,Zangon Namali,C3-70712,12
# Sokoto,Gwadabawa,Atakwanyo,Gidan Magaji Waziri,C3-70721,18
# Sokoto,Gwadabawa,Atakwanyo,Gidan Maisa,C3-70722,20
# Sokoto,Gwadabawa,Chimola,Dan Barunje,C3-70731,35
# Sokoto,Gwadabawa,Chimola,Kanwuri Gabas,C3-70732,12
# Sokoto,Gwadabawa,Gidankaya,Gidan Dutse,C3-70741,13
# Sokoto,Gwadabawa,Gidankaya,Gwara Shiyar Liman,C3-70742,11
# Sokoto,Gwadabawa,Gigane,Gamaru,C3-70751,14
# Sokoto,Gwadabawa,Gigane,Shiyar Galadima,C3-70752,14
# Sokoto,Illela,Araba,B Dusti,C3-70811,5
# Sokoto,Illela,Araba,Danboka,C3-70812,10
# Sokoto,Illela,Damba,Cudan,C3-70821,50
# Sokoto,Illela,Damba,Cudanala,C3-70822,16
# Sokoto,Illela,Darnasabongari,Dullu,C3-70831,12
# Sokoto,Illela,Darnasabongari,Gidan Tudu,C3-70832,13
# Sokoto,Illela,Darnatsolawo,Birnin Isah,C3-70841,6
# Sokoto,Illela,Darnatsolawo,Birnin Isah Dusti,C3-70842,7
# Sokoto,Illela,Garu,Buwadawa Tsururu,C3-70851,22
# Sokoto,Illela,Garu,Diboni Nasarawa,C3-70852,21
# Sokoto,Isa,Bargaja,Gidan Dawa,C3-70911,23
# Sokoto,Isa,Bargaja,Dan Zanke Fage,C3-70912,21
# Sokoto,Isa,Gebe A,Kagara Ganuwa,C3-70921,15
# Sokoto,Isa,Gebe A,Manawa Kanwuri,C3-70922,16
# Sokoto,Isa,Gebe B,Dan Gurmu,C3-70931,18
# Sokoto,Isa,Gebe B,Dan Koloto Gabas,C3-70932,17
# Sokoto,Isa,Isa North,Angawa1,C3-70941,17
# Sokoto,Isa,Isa North,Kantamawa Shiyar Mainasara Magaji,C3-70942,12
# Sokoto,Isa,Isa South,Gidan Rukuma Kabo,C3-70951,9
# Sokoto,Isa,Isa South,Korawa,C3-70952,14
# Sokoto,Kebbe,Fakku,Bashi Shiyar Hakimi,C3-71011,7
# Sokoto,Kebbe,Fakku,Bashi Shiyar Yamma,C3-71012,7
# Sokoto,Kebbe,Girkau,Dankujeri,C3-71021,13
# Sokoto,Kebbe,Girkau,Gidan Dangwani,C3-71022,12
# Sokoto,Kebbe,Kebbeeast,Kebbe Town,C3-71031,11
# Sokoto,Kebbe,Kebbeeast,Shiyar Sabongari,C3-71032,32
# Sokoto,Kebbe,Kebbewest,Shiyar Bazaik,C3-71041,9
# Sokoto,Kebbe,Kebbewest,Shiyar Ajiya,C3-71042,13
# Sokoto,Kebbe,Kuchi,Arausaya,C3-71051,46
# Sokoto,Kebbe,Kuchi,Matatar Iska,C3-71052,12
# Sokoto,Kware,Bankanu,Agalawa,C3-71111,9
# Sokoto,Kware,Bankanu,Gidan Alfari,C3-71112,6
# Sokoto,Kware,Basansan,Adarawa,C3-71121,12
# Sokoto,Kware,Basansan,Gidan Fadama,C3-71122,15
# Sokoto,Kware,Durbawa,Asaula,C3-71131,40
# Sokoto,Kware,Durbawa,Durbawa Bakin Titi,C3-71132,20
# Sokoto,Kware,Gandu,Gidan Alkali,C3-71141,9
# Sokoto,Kware,Gandu,Gidan Dala,C3-71142,10
# Sokoto,Kware,Gidan Ruggamore,Badageni,C3-71151,22
# Sokoto,Kware,Gidanruggamore,G Kwano,C3-71152,18
# Sokoto,Rabah,Gandi1,Adarkawa,C3-71211,17
# Sokoto,Rabah,Gandi1,Dankadu,C3-71212,12
# Sokoto,Rabah,Gandi2,Alikiru,C3-71221,15
# Sokoto,Rabah,Gandi2,Cikaltun Fulani,C3-71222,13
# Sokoto,Rabah,Gandiii,Dangazuri,C3-71231,15
# Sokoto,Rabah,Gandiii,Dangazuri Jumuah Mosque,C3-71232,14
# Sokoto,Rabah,Goddodi,Shiyar Bagudu,C3-71241,16
# Sokoto,Rabah,Goddodi,Shiyar Dangaladima,C3-71242,14
# Sokoto,Rabah,Kurya,Chakaltu,C3-71251,28
# Sokoto,Rabah,Kurya,Mashekari,C3-71252,16
# Sokoto,Sabonbirni,Gatawa,Burkusuma/Kuti,C3-71311,12
# Sokoto,Sabonbirni,Gatawa,Dankaka,C3-71312,14
# Sokoto,Sabonbirni,Kalgo,Dankarmaum,C3-71321,30
# Sokoto,Sabonbirni,Kalgo,Garin Dadi,C3-71322,11
# Sokoto,Sabonbirni,Kurawa,Dabugi/Adarawa,C3-71331,16
# Sokoto,Sabonbirni,Kurawa,Dakwaro Gidanjibo,C3-71332,17
# Sokoto,Sabonbirni,Lajinge,Dungurum Adarawa,C3-71341,16
# Sokoto,Sabonbirni,Lajinge,Jira Shiyar Ila,C3-71342,14
# Sokoto,Sabonbirni,Makuwana,Balbebu Zsala,C3-71351,15
# Sokoto,Sabonbirni,Makuwana,Faru Shiyar Adamu,C3-71352,16
# Sokoto,Shagari,Dandinmahe,Dandin Mahe Shiyar Gandu,C3-71411,12
# Sokoto,Shagari,Dandinmahe,Dandin Mahe Shiyar Kanwuri,C3-71412,15
# Sokoto,Shagari,Gangan,Gangan Shiyar Sarkin Fada,C3-71421,32
# Sokoto,Shagari,Gangan,Gidan Daji,C3-71422,13
# Sokoto,Shagari,Horo,Horo Shiyar Dikko,C3-71431,28
# Sokoto,Shagari,Horo,Horo Shiyar Kwadarko,C3-71432,10
# Sokoto,Shagari,Jaredi,Jaredi Shiyar Asibiti,C3-71441,13
# Sokoto,Shagari,Jaredi,Labani,C3-71442,12
# Sokoto,Shagari,Kajiji,Lafiyar Bature,C3-71451,8
# Sokoto,Shagari,Kajiji,Asarara B,C3-71452,18
# Sokoto,Silame,Gandeward,Falanje,C3-71511,29
# Sokoto,Silame,Gandeward,Gaukonawa,C3-71512,14
# Sokoto,Silame,Gaukaiward,Chofal,C3-71521,11
# Sokoto,Silame,Gaukaiward,Gidan Yaya A,C3-71522,13
# Sokoto,Silame,Jekanaduward,Burmawa,C3-71531,10
# Sokoto,Silame,Jekanaduward,Gabbuwa Gari A,C3-71532,9
# Sokoto,Silame,Kataminorth,Gidan Dari,C3-71541,14
# Sokoto,Silame,Kataminorth,Ingwaba,C3-71542,21
# Sokoto,Silame,Katamisouth,Baichin Koli,C3-71551,29
# Sokoto,Silame,Katamisouth,Gadambe Pegi,C3-71552,11
# Sokoto,Sokoto North,Magajingaria,Binanchi Late Maccido,C3-71611,9
# Sokoto,Sokoto North,Magajingaria,Helele Alh Bello Fari,C3-71612,23
# Sokoto,Sokoto North,Magajingarib,Gidan Sauro Sarkin Baki,C3-71621,13
# Sokoto,Sokoto North,Magajingarib,Sagin Lemu,C3-71622,30
# Sokoto,Sokoto North,Magajinrafia,Alkammawa Saurawa,C3-71631,16
# Sokoto,Sokoto North,Magajinrafia,Alkammawa Shiyar Bunu,C3-71632,13
# Sokoto,Sokoto North,Magajinrafib,Danfili Ashafa,C3-71641,16
# Sokoto,Sokoto North,Magajinrafib,Police Barack Yamma,C3-71642,21
# Sokoto,Sokoto North,Sarkinadargandu,Hajiya Halima C,C3-71651,8
# Sokoto,Sokoto North,Sarkinadargandu,Kaura/Kawa A&Stc,C3-71652,12
# Sokoto,Sokoto South,Gagia,Gagi Rugga Bayan Makaranta,C3-71711,22
# Sokoto,Sokoto South,Gagia,Gidan Masau Shiyar Makaranta,C3-71712,8
Sokoto,Sokoto South,Gagib,Oppa Road,C3-71721,97
# Sokoto,Sokoto South,Gagib,Sagagin Malan Kwaire,C3-71722,17
# Sokoto,Sokoto South,Gagic,Gidan Dahala Shiyar Asani Baya,C3-71731,47
# Sokoto,Sokoto South,Gagic,Iddi Yar Ksuwa Baya,C3-71732,13
# Sokoto,Sokoto South,Rijiaa,Back Of Specialist,C3-71741,11
# Sokoto,Sokoto South,Rijiaa,Hilin Boka Shiyar Mansur,C3-71742,10
# Sokoto,Sokoto South,Rijiab,Diploma Firstbank,C3-71751,14
# Sokoto,Sokoto South,Rijiab,Garkar Sarkin Gara,C3-71752,10
# Sokoto,Tambuwal,Bagida,Dogon Gona,C3-71811,3
# Sokoto,Tambuwal,Bagida,Ganuwa Sabon Gari,C3-71812,3
# Sokoto,Tambuwal,Barkejinabaguda,Gidan Mai Zuma,C3-71821,3
# Sokoto,Tambuwal,Barkejinabaguda,Kyanko A,C3-71822,9
# Sokoto,Tambuwal,Bashiremaikada,Labe Gabas,C3-71831,12
# Sokoto,Tambuwal,Bashiremaikada,Maikada Gabas,C3-71832,13
# Sokoto,Tambuwal,Dogondaji,Barguwa,C3-71841,8
# Sokoto,Tambuwal,Dogondaji,Mashekarin Mata,C3-71842,103
# Sokoto,Tambuwal,Fagaalasan,Inwala,C3-71851,4
# Sokoto,Tambuwal,Fagaalasan,Kaurar Inwala,C3-71852,4
# Sokoto,Tangaza,Gidanmadi,Dakala,C3-71911,15
# Sokoto,Tangaza,Gidanmadi,Gidan Daji,C3-71912,9
# Sokoto,Tangaza,Kalanjeni,Adarawa Tudu,C3-71921,14
# Sokoto,Tangaza,Kalanjeni,Gida Marafi,C3-71922,18
# Sokoto,Tangaza,Kwaccehuru,Araba,C3-71931,19
# Sokoto,Tangaza,Kwaccehuru,Araba Daji,C3-71932,8
# Sokoto,Tangaza,Magonho,Ailya Hausawa,C3-71941,17
# Sokoto,Tangaza,Magonho,Gidan Garba,C3-71942,16
# Sokoto,Tangaza,Raka,Gidan Abdul,C3-71951,29
# Sokoto,Tangaza,Raka,Hawa Ukku,C3-71952,14
# Sokoto,Tureta,Dangulbi,Barkatube Garin Magaji Usman,C3-72011,12
# Sokoto,Tureta,Dangulbi,Dangulbi Shiyar Alh Zarumi,C3-72012,8
# Sokoto,Tureta,Duma,Makera,C3-72021,7
# Sokoto,Tureta,Duma,Takalmawa,C3-72022,14
# Sokoto,Tureta,Furagirke,Fura Girke Shiyar Masallachi,C3-72031,12
# Sokoto,Tureta,Furagirke,Fura Girke Shiyar Runji,C3-72032,8
# Sokoto,Tureta,Gidankare,Bimasa Tasha Shiyar Liman,C3-72041,29
# Sokoto,Tureta,Gidankare,Daddabi,C3-72042,8
# Sokoto,Tureta,Kuruwa,Galadimmai Shiyar Dantudu,C3-72051,18
# Sokoto,Tureta,Kuruwa,Gidan Arzika,C3-72052,44
# Sokoto,Wamakko,Arkilla,Bafarawa Qtrs(Wamakko),C3-72111,16
# Sokoto,Wamakko,Arkilla,Gidan Amba,C3-72112,6
# Sokoto,Wamakko,Bado,Alu Quarters,C3-72121,37
# Sokoto,Wamakko,Bado,Badon Rafi Abc,C3-72122,20
# Sokoto,Wamakko,Dundaye,Dundaye Gabas,C3-72131,29
# Sokoto,Wamakko,Dundaye,Kaura Bella,C3-72132,29
# Sokoto,Wamakko,Gidanbubu,Adarawa,C3-72141,5
# Sokoto,Wamakko,Gidanbubu,Firgeja Marmaro,C3-72142,7
# Sokoto,Wamakko,Gidanhamidu,Anguwar Ruwa,C3-72151,6
# Sokoto,Wamakko,Gidanhamidu,Garu,C3-72152,5
# Sokoto,Wurno,Achida,Sabongari B,C3-72211,23
# Sokoto,Wurno,Achida,Shiyar Ajiya,C3-72212,18
# Sokoto,Wurno,Alkammu,Dan Durumi,C3-72221,11
# Sokoto,Wurno,Alkammu,G Fadama,C3-72222,10
# Sokoto,Wurno,Chachomarnona,Doron Sule,C3-72231,29
# Sokoto,Wurno,Chachomarnona,Gidan Tudu,C3-72232,7
# Sokoto,Wurno,Dimbiso,Dutsi,C3-72241,12
# Sokoto,Wurno,Dimbiso,Shiyar Naibi A,C3-72242,10
# Sokoto,Wurno,Dinawa,Gwargawa,C3-72251,12
# Sokoto,Wurno,Dinawa,Sarkin Yaki A,C3-72252,29
# Sokoto,Yabo,Bakale,Bakale Shiyar Makaranta,C3-72311,16
# Sokoto,Yabo,Bakale,Bakale Shiyar Masanlachi,C3-72312,10
# Sokoto,Yabo,Bengaje,Adiga Marina,C3-72321,17
# Sokoto,Yabo,Bengaje,Bengaje Shiyar Magaji Ii,C3-72322,13
# Sokoto,Yabo,Binjinmuza,Kautaki,C3-72331,11
# Sokoto,Yabo,Binjinmuza,Kibiyare Shiyar Magaji,C3-72332,16
# Sokoto,Yabo,Birniruwa,Birninruwa D Dutsi,C3-72341,24
# Sokoto,Yabo,Birniruwa,Birninruwa G Galoji,C3-72342,28
# Sokoto,Yabo,Dagawa,Danbalo Sabon Gari,C3-72351,14
# Sokoto,Yabo,Dagawa,Magacci Sarki Shiyar/Malammai,C3-72352,12
"""

# Load community mapping
try:
    from io import StringIO
    COMMUNITY_DF = pd.read_csv(StringIO(COMMUNITY_MAP_DATA))
    # Create mapping dictionaries
    COMMUNITY_CODE_TO_NAME = dict(zip(COMMUNITY_DF['communitycode'], COMMUNITY_DF['Community']))
    COMMUNITY_NAME_TO_CODE = dict(zip(COMMUNITY_DF['Community'], COMMUNITY_DF['communitycode']))
    COMMUNITY_PLANNED = dict(zip(COMMUNITY_DF['Community'], COMMUNITY_DF['Planned_Community']))
except Exception as e:
    st.error(f"Error loading community mapping: {e}")
    COMMUNITY_DF = pd.DataFrame()
    COMMUNITY_CODE_TO_NAME = {}
    COMMUNITY_NAME_TO_CODE = {}
    COMMUNITY_PLANNED = {}

# ---------------- LGA-BASED LOGIN CREDENTIALS ----------------
# Format: {lga_username: lga_name}
# Usernames are case-insensitive (will be converted to lowercase)
LGA_CREDENTIALS = {
    "binji": "Binji",
    "bodinga": "Bodinga",
    "dangeshuni": "Dange Shuni",
    "gada": "Gada",
    "goronyo": "Goronyo",
    "gudu": "Gudu",
    "gwadabawa": "Gwadabawa",
    "illela": "Illela",
    "isa": "Isa",
    "kebbe": "Kebbe",
    "kware": "Kware",
    "rabah": "Rabah",
    "sabonbirni": "Sabon Birni",
    "shagari": "Shagari",
    "silame": "Silame",
    "sokoto north": "Sokoto North",
    "sokoto south": "Sokoto South",
    "tambuwal": "Tambuwal",
    "tangaza": "Tangaza",
    "tureta": "Tureta",
    "wamakko": "Wamakko",
    "wurno": "Wurno",
    "yabo": "Yabo",
}

# ---------------- DATA LOADING FUNCTION ----------------
@st.cache_data(show_spinner="📊 Loading SARMAAN II AMR data...", ttl=600)
def load_data(force_refresh=False):
    """Load data from KoboToolbox export URL"""
    try:
        # Load data directly from the export URL (no authentication needed)
        response = requests.get(DATA_URL, timeout=60)
        response.raise_for_status()
        excel_file = BytesIO(response.content)
        
        # Load all sheets
        data_dict = pd.read_excel(excel_file, sheet_name=None)
        
        df_main = data_dict.get(MAIN_SHEET, pd.DataFrame())
        df_mother = data_dict.get(MOTHER_SHEET, pd.DataFrame())
        df_child = data_dict.get(CHILD_SHEET, pd.DataFrame())
        
        # Check if main dataframe is empty
        if df_main.empty:
            st.warning(f"⚠️ Sheet '{MAIN_SHEET}' not found or is empty. Available sheets: {list(data_dict.keys())}")
        
        # Data cleaning and preprocessing
        if not df_main.empty:
            # Convert date columns
            date_cols = ['start', 'end', 'Date of Consent', '_submission_time']
            for col in date_cols:
                if col in df_main.columns:
                    df_main[col] = pd.to_datetime(df_main[col], errors='coerce')
            
            # Clean text columns
            text_cols = ['Q2. State', 'Q3. Local Government Area', 'Q4. Ward', 
                        'Q5. Community Name', 'username']
            for col in text_cols:
                if col in df_main.columns:
                    df_main[col] = df_main[col].astype(str).str.strip()
        
        return df_main, df_mother, df_child
    
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Network error loading data: {str(e)}")
        st.info("💡 **Troubleshooting Tips:**\n"
                "1. Check your internet connection\n"
                "2. Verify the DATA_URL is correct in secrets.toml\n"
                "3. Ensure the export URL is publicly accessible")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.info("💡 **Possible Issues:**\n"
                "1. Invalid Excel file format\n"
                "2. Sheet names don't match (expected: 'SARMAAN II C3 SOKOTO AMR TRA...', 'mother_information', 'child_info')\n"
                "3. Check that the export URL is correct")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
        
        df_main = data_dict.get(MAIN_SHEET, pd.DataFrame())
        df_mother = data_dict.get(MOTHER_SHEET, pd.DataFrame())
        df_child = data_dict.get(CHILD_SHEET, pd.DataFrame())
        
        # Data cleaning and preprocessing
        if not df_main.empty:
            # Convert date columns
            date_cols = ['start', 'end', 'Date of Consent', '_submission_time']
            for col in date_cols:
                if col in df_main.columns:
                    df_main[col] = pd.to_datetime(df_main[col], errors='coerce')
            
            # Clean text columns
            text_cols = ['Q2. State', 'Q3. Local Government Area', 'Q4. Ward', 
                        'Q5. Community Name', 'username']
            for col in text_cols:
                if col in df_main.columns:
                    df_main[col] = df_main[col].astype(str).str.strip()
        
        return df_main, df_mother, df_child
    
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# ---------------- HELPER FUNCTIONS ----------------
def find_column_with_keyword(df, keyword):
    """Find column containing keyword (case-insensitive)"""
    if df.empty:
        return None
    for col in df.columns:
        if keyword.lower() in col.lower():
            return col
    return None

def calculate_qc_metrics(df_main, df_mother, df_child):
    """Calculate comprehensive QC metrics"""
    qc_results = {
        'total_households': 0,
        'total_mothers': 0,
        'total_children': 0,
        'duplicate_households': 0,
        'duplicate_mothers': 0,
        'duplicate_children': 0,
        'missing_data': 0,
        'azm_received': 0,
        'adverse_events': 0,
        'validation_approved': 0,
        'validation_pending': 0,
        'validation_rejected': 0,
    }
    
    if not df_main.empty:
        qc_results['total_households'] = df_main['_uuid'].nunique()
        
        # Check for duplicates using unique_code column
        household_id_col = 'unique_code' if 'unique_code' in df_main.columns else find_column_with_keyword(df_main, 'unique_code')
        if household_id_col and household_id_col in df_main.columns:
            qc_results['duplicate_households'] = df_main[household_id_col].duplicated().sum()
        
        # Validation status
        validation_col = '_validation_status'
        if validation_col in df_main.columns:
            status_counts = df_main[validation_col].value_counts()
            qc_results['validation_approved'] = status_counts.get('Approved', 0)
            qc_results['validation_pending'] = status_counts.get('Validation Ongoing', 0)
            qc_results['validation_rejected'] = status_counts.get('Not Approved', 0)
    
    if not df_mother.empty:
        qc_results['total_mothers'] = df_mother['mother_id'].nunique()
        qc_results['duplicate_mothers'] = df_mother['mother_id'].duplicated().sum()
        
        # AZM administration
        azm_col = 'Q57. Did any of your children receive azithromycin?'
        if azm_col in df_mother.columns:
            qc_results['azm_received'] = (df_mother[azm_col] == 'Yes').sum()
        
        # Adverse events
        ae_col = 'Q59. Did the child experience any adverse events?'
        if ae_col in df_mother.columns:
            qc_results['adverse_events'] = (df_mother[ae_col] == 'Yes').sum()
    
    if not df_child.empty:
        qc_results['total_children'] = df_child['child_id'].nunique()
        qc_results['duplicate_children'] = df_child['child_id'].duplicated().sum()
    
    return qc_results

def identify_data_quality_issues(df_main, df_mother, df_child):
    """Identify specific data quality issues"""
    issues = []
    
    # Check main household data
    if not df_main.empty:
        # Missing GPS coordinates
        gps_lat_col = '_Q9. GPS coordinates_latitude'
        gps_lon_col = '_Q9. GPS coordinates_longitude'
        if gps_lat_col in df_main.columns and gps_lon_col in df_main.columns:
            missing_gps = df_main[[gps_lat_col, gps_lon_col]].isnull().any(axis=1).sum()
            if missing_gps > 0:
                issues.append({
                    'category': 'Missing Data',
                    'description': f'{missing_gps} households missing GPS coordinates',
                    'severity': 'Medium',
                    'count': missing_gps
                })
        
        # Incorrect phone date/time flags
        phone_flag_col = '🛑 Incorrect phone date/time'
        if phone_flag_col in df_main.columns:
            incorrect_phone = df_main[phone_flag_col].notna().sum()
            if incorrect_phone > 0:
                issues.append({
                    'category': 'Data Entry Error',
                    'description': f'{incorrect_phone} records with incorrect phone date/time',
                    'severity': 'High',
                    'count': incorrect_phone
                })
    
    # Check mother data consistency
    if not df_mother.empty:
        # Mismatch in children counts
        total_children_col = 'Q56. Total Number of Children 1 - 59 months'
        azm_children_col = 'Q58.If yes, how many children received AZM?'
        
        if total_children_col in df_mother.columns and azm_children_col in df_mother.columns:
            mismatch = (df_mother[azm_children_col] > df_mother[total_children_col]).sum()
            if mismatch > 0:
                issues.append({
                    'category': 'Logical Error',
                    'description': f'{mismatch} mothers reported more AZM recipients than total children',
                    'severity': 'High',
                    'count': mismatch
                })
    
    # Check child data
    if not df_child.empty:
        # Missing immunization data
        immunization_col = 'Q68. Was ${child_name} ever immunized?'
        if immunization_col in df_child.columns:
            missing_immunization = df_child[immunization_col].isnull().sum()
            if missing_immunization > 0:
                issues.append({
                    'category': 'Missing Data',
                    'description': f'{missing_immunization} children missing immunization status',
                    'severity': 'Low',
                    'count': missing_immunization
                })
    
    return pd.DataFrame(issues)

def perform_comprehensive_qc_checks(df_main, df_mother, df_child):
    """
    Perform comprehensive QC checks across all three sheets
    Returns a DataFrame with all QC issues found
    """
    qc_issues = []
    
    if df_main.empty:
        return pd.DataFrame(qc_issues)
    
    # Merge dataframes to perform cross-sheet validations
    # Merge main with mother using _uuid
    if not df_mother.empty:
        df_merged = df_main.merge(
            df_mother,
            left_on='_uuid',
            right_on='_submission__uuid',
            how='left',
            suffixes=('', '_mother')
        )
    else:
        df_merged = df_main.copy()
    
    # Merge with child data
    if not df_child.empty:
        df_with_child = df_main.merge(
            df_child,
            left_on='_uuid',
            right_on='_submission__uuid',
            how='left',
            suffixes=('', '_child')
        )
    else:
        df_with_child = df_main.copy()
    
    # QC CHECK 1: Education-Occupation Mismatch
    # If Q13 (highest education level) = "No Formal Education" AND Q15 (occupation) = "Professional/technical/managerial"
    # Find columns using pattern matching to avoid exact name issues
    education_col = None
    occupation_col = None
    
    for col in df_main.columns:
        if 'Q13' in col and 'highest level of school' in col.lower():
            education_col = col
        if 'Q15' in col and 'occupation' in col.lower():
            occupation_col = col
    
    # DEBUG: Print to console what we're checking
    print(f"\n=== QC CHECK 1 DEBUG ===")
    print(f"Education column found: {education_col is not None}")
    print(f"Occupation column found: {occupation_col is not None}")
    
    if education_col and occupation_col:
        # DEBUG: Show unique values
        print(f"\nUnique Education values: {df_main[education_col].unique()}")
        print(f"Unique Occupation values: {df_main[occupation_col].unique()}")
        
        # DEBUG: Check for records with "No Formal Education"
        no_formal_count = (df_main[education_col] == 'No Formal Education').sum()
        print(f"\nRecords with 'No Formal Education': {no_formal_count}")
        
        # DEBUG: Check for records with "Professional/technical/managerial"
        professional_count = (df_main[occupation_col] == 'Professional/technical/managerial').sum()
        print(f"Records with 'Professional/technical/managerial': {professional_count}")
        
        # Check for the mismatch - using correct values from the form
        edu_occ_mismatch = df_main[
            (df_main[education_col] == 'No Formal Education') &
            (df_main[occupation_col] == 'Professional/technical/managerial')
        ]
        
        print(f"\nRecords matching BOTH conditions: {len(edu_occ_mismatch)}")
        if len(edu_occ_mismatch) > 0:
            print("Sample record:")
            print(f"  Education: '{edu_occ_mismatch.iloc[0][education_col]}'")
            print(f"  Occupation: '{edu_occ_mismatch.iloc[0][occupation_col]}'")
        print("=" * 50)
        
        for idx, row in edu_occ_mismatch.iterrows():
            qc_issues.append({
                'LGA': row.get('Q3. Local Government Area', ''),
                'Ward': row.get('Q4. Ward', ''),
                'Community': row.get('Q5. Community Name', ''),
                'Unique HH ID': row.get('unique_code', ''),
                'Enumerator': row.get('username', ''),
                'Validation Status': row.get('_validation_status', ''),
                'Issue Type': 'Education-Occupation Mismatch',
                'Description': f'No formal education but has Professional/technical/managerial occupation (Education: {row[education_col]}, Occupation: {row[occupation_col]})'
            })
    else:
        print("One or both columns not found!")
        print("=" * 50)
    
    # QC CHECK 2: Urban Settlement with No Basic Amenities
    # All amenity questions must = "No" and settlement type = "Urban"
    settlement_col = 'Choose the settlement type'
    amenity_cols = [
        'Q18. Does your household have a television?',
        'Q19. Does your household have an electric iron?',
        'Q20. Does your household have a fan?',
        'Q21. Does your household have a refrigerator?',
        'Q22. Does your household have electricity?',
        'Q23. Does your household have a generator?',
        'Q24. Does any member of the household have a bank account?',
        'Q25. Does any member of the household have a watch?',
        'Q26.Does your household have any of the following (Donkey,Camel,Cattle,Horse)?',
        'Q27. Does your household have truck?',
        'Q28. Does your household have bicycle?',
        'Q29. Does your household have tricycle?',
        'Q30. Does your household have computer?',
        'Q31. Does your household have table?',
        'Q32. Does your household have air condition?'
    ]
    
    if settlement_col in df_main.columns:
        # Check which amenity columns exist
        existing_amenity_cols = [col for col in amenity_cols if col in df_main.columns]
        
        if existing_amenity_cols:
            # Create a mask for all amenities being "No"
            all_no_mask = pd.Series([True] * len(df_main), index=df_main.index)
            for col in existing_amenity_cols:
                all_no_mask = all_no_mask & (df_main[col] == 'No')
            
            # Find urban settlements with no basic amenities
            urban_no_amenities = df_main[
                (df_main[settlement_col] == 'Urban') & all_no_mask
            ]
            
            for idx, row in urban_no_amenities.iterrows():
                qc_issues.append({
                    'LGA': row.get('Q3. Local Government Area', ''),
                    'Ward': row.get('Q4. Ward', ''),
                    'Community': row.get('Q5. Community Name', ''),
                    'Unique HH ID': row.get('unique_code', ''),
                    'Enumerator': row.get('username', ''),
                    'Validation Status': row.get('_validation_status', ''),
                    'Issue Type': 'Urban-No Basic Amenities',
                    'Description': 'Urban settlement but household has no basic amenities'
                })
    
    # QC CHECK 3: Children count mismatch (Q48 vs Q56 in mother sheet)
    # Q48 in main sheet should equal Q56 in mother sheet
    main_children_col = 'Q48. How many children in the household are 1-59 months of age?'
    mother_children_col = 'Q56. Total Number of Children 1 - 59 months'
    
    if main_children_col in df_merged.columns and mother_children_col in df_merged.columns:
        children_mismatch = df_merged[
            (df_merged[main_children_col].notna()) &
            (df_merged[mother_children_col].notna()) &
            (df_merged[main_children_col] != df_merged[mother_children_col])
        ]
        
        for idx, row in children_mismatch.iterrows():
            qc_issues.append({
                'LGA': row.get('Q3. Local Government Area', ''),
                'Ward': row.get('Q4. Ward', ''),
                'Community': row.get('Q5. Community Name', ''),
                'Unique HH ID': row.get('unique_code', ''),
                'Enumerator': row.get('username', ''),
                'Validation Status': row.get('_validation_status', ''),
                'Issue Type': 'Children Count Mismatch (1-59 months)',
                'Description': f'Main sheet: {row[main_children_col]}, Mother sheet: {row[mother_children_col]}'
            })
    
    # QC CHECK 4: Infants count mismatch (Q49 vs Q55 in mother sheet)
    main_infants_col = 'Q49. How many children in the household are 0 - 28 days of age?'
    mother_infants_col = 'Q55. Total Number of Children less than 1 month'
    
    if main_infants_col in df_merged.columns and mother_infants_col in df_merged.columns:
        infants_mismatch = df_merged[
            (df_merged[main_infants_col].notna()) &
            (df_merged[mother_infants_col].notna()) &
            (df_merged[main_infants_col] != df_merged[mother_infants_col])
        ]
        
        for idx, row in infants_mismatch.iterrows():
            qc_issues.append({
                'LGA': row.get('Q3. Local Government Area', ''),
                'Ward': row.get('Q4. Ward', ''),
                'Community': row.get('Q5. Community Name', ''),
                'Unique HH ID': row.get('unique_code', ''),
                'Enumerator': row.get('username', ''),
                'Validation Status': row.get('_validation_status', ''),
                'Issue Type': 'Infants Count Mismatch (0-28 days)',
                'Description': f'Main sheet: {row[main_infants_col]}, Mother sheet: {row[mother_infants_col]}'
            })
    
    # QC CHECK 5: AZM recipients exceeds total children
    # Q58 (AZM recipients) should not be greater than Q47 (total children 0-59 months)
    main_total_children_col = 'Q47. How many children in the household are 0-59 months of age?'
    azm_recipients_col = 'Q58.If yes, how many children received AZM?'
    
    if main_total_children_col in df_merged.columns and azm_recipients_col in df_merged.columns:
        azm_exceeds = df_merged[
            (df_merged[azm_recipients_col].notna()) &
            (df_merged[main_total_children_col].notna()) &
            (pd.to_numeric(df_merged[azm_recipients_col], errors='coerce') > 
             pd.to_numeric(df_merged[main_total_children_col], errors='coerce'))
        ]
        
        for idx, row in azm_exceeds.iterrows():
            qc_issues.append({
                'LGA': row.get('Q3. Local Government Area', ''),
                'Ward': row.get('Q4. Ward', ''),
                'Community': row.get('Q5. Community Name', ''),
                'Unique HH ID': row.get('unique_code', ''),
                'Enumerator': row.get('username', ''),
                'Validation Status': row.get('_validation_status', ''),
                'Issue Type': 'AZM Recipients Exceeds Total Children',
                'Description': f'AZM recipients: {row[azm_recipients_col]}, Total children: {row[main_total_children_col]}'
            })
    
    # QC CHECK 6: Child age greater than 59 months
    child_age_col = 'c_age'
    
    if not df_child.empty and child_age_col in df_child.columns:
        age_exceeds = df_child[
            pd.to_numeric(df_child[child_age_col], errors='coerce') > 59
        ]
        
        # Merge with main to get household details
        if not age_exceeds.empty:
            age_exceeds_merged = age_exceeds.merge(
                df_main[['_uuid', 'Q3. Local Government Area', 'Q4. Ward', 'Q5. Community Name', 'unique_code', 'username', '_validation_status']],
                left_on='_submission__uuid',
                right_on='_uuid',
                how='left'
            )
            
            for idx, row in age_exceeds_merged.iterrows():
                qc_issues.append({
                    'LGA': row.get('Q3. Local Government Area', ''),
                    'Ward': row.get('Q4. Ward', ''),
                    'Community': row.get('Q5. Community Name', ''),
                    'Unique HH ID': row.get('unique_code', ''),
                    'Enumerator': row.get('username', ''),
                    'Validation Status': row.get('_validation_status', ''),
                    'Issue Type': 'Age Inconsistency',
                    'Description': f'Child age ({row[child_age_col]} months) exceeds 59 months'
                })
    
    # Convert to DataFrame
    if qc_issues:
        qc_df = pd.DataFrame(qc_issues)
        return qc_df
    else:
        return pd.DataFrame(columns=['LGA', 'Ward', 'Community', 'Unique HH ID', 'Enumerator', 'Validation Status', 'Issue Type', 'Description'])

# ---------------- LOGIN PAGE ----------------
def login_page():
    """Display login interface"""
    st.markdown(
        """
        <div class="dashboard-header" style="text-align: center;">
            <h1 class="dashboard-title">🏥 SARMAAN II</h1>
            <p class="dashboard-subtitle">Antimicrobial Resistance Study</p>
            <p class="dashboard-subtitle">Quality Control Dashboard</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="login-title">🔐 Dashboard Login</h2>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            
            col_a, col_b = st.columns(2)
            with col_a:
                login_button = st.form_submit_button("🔓 Login", use_container_width=True)
            with col_b:
                help_button = st.form_submit_button("❓ Help", use_container_width=True)
            
            if login_button:
                if not username:
                    st.error("❌ Please enter a username")
                # Check admin login (case-insensitive)
                elif username.strip().lower() == "admin":
                    st.session_state.logged_in = True
                    st.session_state.current_user = "admin"
                    st.session_state.user_role = 'admin'
                    st.success("✅ Admin login successful!")
                    st.rerun()
                
                # Check LGA login (case-insensitive)
                elif username.strip().lower() in LGA_CREDENTIALS:
                    lga_name = LGA_CREDENTIALS[username.strip().lower()]
                    st.session_state.logged_in = True
                    st.session_state.current_user = username.strip().lower()
                    st.session_state.user_role = 'lga'
                    st.session_state.selected_lga = lga_name
                    st.success(f"✅ Login successful! Welcome {lga_name} LGA supervisor")
                    st.rerun()
                else:
                    st.error("❌ Invalid username. Please check and try again.")
            
            if help_button:
                st.info("""
                **Login Instructions:**
                
                **For Admin Access:**
                - Username: `admin`
                
                **For LGA Supervisors:**
                - Username: Your LGA name (lowercase)
                - Examples: `Binji`, `Gada`, `Gudu`, `Yabo`, etc.
                
                **Available LGAs:**
                Binji, Bodinga, Dange Shuni, Gada, Goronyo, Gudu, Gwadabawa, Illela, 
                Isa, Kebbe, Kware, Rabah, Sabon Birni, Shagari, Silame, Sokoto North, 
                Sokoto South, Tambuwal, Tangaza, Tureta, Wamakko, Wurno, Yabo
                
                📞 Contact your M&E coordinator for login issues
                """)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Additional info
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📊 **Real-time Data**\nAutomatic sync with KoboToolbox")
    with col2:
        st.info("🔒 **Secure Access**\nRole-based permissions")
    with col3:
        st.info("📈 **Quality Metrics**\nComprehensive QC tracking")

# ---------------- MAIN DASHBOARD ----------------
def run_dashboard(df_main, df_mother, df_child):
    """Main dashboard interface"""
    
    # Store original community codes before mapping
    community_col = find_column_with_keyword(df_main, 'Community')
    if community_col and community_col in df_main.columns:
        # Create a new column to store the original code
        df_main['_community_code_original'] = df_main[community_col].copy()
        
        # Map community codes to names for display
        if COMMUNITY_CODE_TO_NAME:
            df_main[community_col] = df_main[community_col].map(
                lambda x: COMMUNITY_CODE_TO_NAME.get(str(x), x) if pd.notna(x) else x
            )
    
    # Header
    if st.session_state.user_role == 'admin':
        user_role_display = "Administrator - All LGAs"
    elif st.session_state.user_role == 'lga':
        user_role_display = f"{st.session_state.selected_lga} LGA Supervisor"
    else:
        user_role_display = "Dashboard User"
    
    st.markdown(
        f"""
        <div class="dashboard-header">
            <h1 class="dashboard-title">🏥 SARMAAN II AMR Dashboard</h1>
            <p class="dashboard-subtitle">Sokoto State - Quality Control & Monitoring System</p>
            <div class="user-badge">👤 {user_role_display}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Store original unfiltered data for QC checks
    df_main_original = df_main.copy()
    df_mother_original = df_mother.copy()
    df_child_original = df_child.copy()
    
    # Filter data based on user role
    if st.session_state.user_role == 'lga':
        lga_col = find_column_with_keyword(df_main, 'Local Government')
        
        if lga_col and lga_col in df_main.columns:
            # Case-insensitive matching for LGA
            df_main = df_main[df_main[lga_col].str.upper() == st.session_state.selected_lga.upper()]
            
            # Filter related tables
            household_uuids = df_main['_uuid'].unique()
            df_mother = df_mother[df_mother['_submission__uuid'].isin(household_uuids)]
            df_child = df_child[df_child['_submission__uuid'].isin(household_uuids)]
    
    # Sidebar filters
    with st.sidebar:
        st.markdown("### 🎛️ Dashboard Controls")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.user_role = None
            st.rerun()
        
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.session_state.refresh_count += 1
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📅 Date Filter")
        
        if 'start' in df_main.columns:
            min_date = df_main['start'].min().date() if not df_main.empty else date.today()
            max_date = df_main['start'].max().date() if not df_main.empty else date.today()
            
            date_range = st.date_input(
                "Select Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
            
            if len(date_range) == 2:
                df_main = df_main[
                    (df_main['start'].dt.date >= date_range[0]) &
                    (df_main['start'].dt.date <= date_range[1])
                ]
        
        st.markdown("---")
        
        # Additional filters for admin
        if st.session_state.user_role == 'admin':
            st.markdown("### 🗺️ Location Filters")
            
            lga_col = find_column_with_keyword(df_main, 'Local Government')
            if lga_col and lga_col in df_main.columns:
                lgas = ["All"] + sorted(df_main[lga_col].dropna().unique().tolist())
                selected_lga = st.selectbox("Select LGA", lgas)
                
                if selected_lga != "All":
                    # Case-insensitive matching for LGA
                    df_main = df_main[df_main[lga_col].str.upper() == selected_lga.upper()]
            
            ward_col = find_column_with_keyword(df_main, 'Ward')
            if ward_col and ward_col in df_main.columns:
                wards = ["All"] + sorted(df_main[ward_col].dropna().unique().tolist())
                selected_ward = st.selectbox("Select Ward", wards)
                
                if selected_ward != "All":
                    df_main = df_main[df_main[ward_col] == selected_ward]
        
        st.markdown("---")
        st.markdown(f"**Refresh Count:** {st.session_state.refresh_count}")
        st.markdown(f"**Data Points:** {len(df_main):,}")
    
    # Calculate metrics
    qc_metrics = calculate_qc_metrics(df_main, df_mother, df_child)
    
    # KPI Section
    st.markdown('<div class="section-header"><h2 class="section-title">📊 Key Performance Indicators</h2></div>', unsafe_allow_html=True)
    
    # Calculate the metrics from filtered data
    total_submissions = len(df_main)
    lgas_covered = df_main['Q3. Local Government Area'].nunique() if 'Q3. Local Government Area' in df_main.columns else 0
    wards_covered = df_main['Q4. Ward'].nunique() if 'Q4. Ward' in df_main.columns else 0
    communities_covered = df_main['Q5. Community Name'].nunique() if 'Q5. Community Name' in df_main.columns else 0
    research_assistants = df_main['username'].nunique() if 'username' in df_main.columns else 0
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left-color: #3b82f6;">
                <div class="metric-value" style="color: #3b82f6;">{total_submissions}</div>
                <div class="metric-label">Total Submissions</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left-color: #10b981;">
                <div class="metric-value" style="color: #10b981;">{lgas_covered}</div>
                <div class="metric-label">LGAs Covered</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left-color: #14b8a6;">
                <div class="metric-value" style="color: #14b8a6;">{wards_covered}</div>
                <div class="metric-label">Wards Covered</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left-color: #f97316;">
                <div class="metric-value" style="color: #f97316;">{communities_covered}</div>
                <div class="metric-label">Communities</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col5:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left-color: #8b5cf6;">
                <div class="metric-value" style="color: #8b5cf6;">{research_assistants}</div>
                <div class="metric-label">Enumerators</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Validation Status
    st.markdown('<div class="section-header"><h2 class="section-title">✅ Validation Status</h2></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left-color: var(--success-green);">
                <div class="metric-label">✅ Approved</div>
                <div class="metric-value" style="color: var(--success-green);">{qc_metrics['validation_approved']:,}</div>
                <div class="qc-badge qc-success">Ready for Analysis</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left-color: var(--warning-yellow);">
                <div class="metric-label">⏳ Pending Review</div>
                <div class="metric-value" style="color: var(--warning-yellow);">{qc_metrics['validation_pending']:,}</div>
                <div class="qc-badge qc-warning">Awaiting Review</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div class="metric-card" style="border-left-color: var(--danger-red);">
                <div class="metric-label">❌ Rejected</div>
                <div class="metric-value" style="color: var(--danger-red);">{qc_metrics['validation_rejected']:,}</div>
                <div class="qc-badge qc-danger">Requires Action</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Community Coverage Analysis - Moved here after Validation Status
    st.markdown('<div class="section-header"><h2 class="section-title">📋 Community Coverage Analysis</h2></div>', unsafe_allow_html=True)
    
    community_col = find_column_with_keyword(df_main, 'Community')
    lga_col = find_column_with_keyword(df_main, 'Local Government')
    ward_col = find_column_with_keyword(df_main, 'Ward')
    
    if community_col and community_col in df_main.columns and not COMMUNITY_DF.empty:
        # Use the original community code column we saved earlier
        df_main_copy = df_main.copy()
        
        # Check if we have the original community code column
        if '_community_code_original' in df_main_copy.columns:
            # Use original community codes for matching (most reliable)
            actual_coverage = df_main_copy.groupby('_community_code_original').size().reset_index(name='Actual_Submissions')
            
            # Merge with planned data using community code
            coverage_table = COMMUNITY_DF.merge(
                actual_coverage,
                left_on='communitycode',
                right_on='_community_code_original',
                how='left'
            )
        else:
            # Fallback: use LGA + Ward + Community name for matching
            actual_coverage = df_main_copy.groupby([lga_col, ward_col, community_col]).size().reset_index(name='Actual_Submissions')
            
            # Merge with planned data
            coverage_table = COMMUNITY_DF.merge(
                actual_coverage,
                left_on=['lga', 'ward', 'Community'],
                right_on=[lga_col, ward_col, community_col],
                how='left'
            )
        
        # Fill missing values
        coverage_table['Actual_Submissions'] = coverage_table['Actual_Submissions'].fillna(0).astype(int)
        coverage_table['Coverage_%'] = ((coverage_table['Actual_Submissions'] / coverage_table['Planned_Community']) * 100).round(1)
        coverage_table['Status'] = coverage_table.apply(
            lambda row: '✅ Complete' if row['Actual_Submissions'] >= row['Planned_Community'] 
            else '⚠️ Partial' if row['Actual_Submissions'] > 0 
            else '❌ Not Started', axis=1
        )
        
        # Calculate summary metrics
        total_planned_hh = coverage_table['Planned_Community'].sum()
        total_reached_hh = coverage_table['Actual_Submissions'].sum()
        overall_coverage = (total_reached_hh / total_planned_hh * 100) if total_planned_hh > 0 else 0
        
        # Calculate communities at target (100% or more coverage)
        communities_at_target = (coverage_table['Actual_Submissions'] >= coverage_table['Planned_Community']).sum()
        total_communities = len(coverage_table)
        
        # Display large metrics in a row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div style='text-align: left; padding: 20px; background-color: white; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <p style='color: #64748b; font-size: 16px; margin: 0;'>Total Planned HH</p>
                <h1 style='color: #1e293b; font-size: 48px; margin: 10px 0; font-weight: bold;'>{total_planned_hh:,}</h1>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style='text-align: left; padding: 20px; background-color: white; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <p style='color: #64748b; font-size: 16px; margin: 0;'>Total Reached HH</p>
                <h1 style='color: #1e293b; font-size: 48px; margin: 10px 0; font-weight: bold;'>{total_reached_hh:,}</h1>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style='text-align: left; padding: 20px; background-color: white; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <p style='color: #64748b; font-size: 16px; margin: 0;'>Overall Coverage</p>
                <h1 style='color: #1e293b; font-size: 48px; margin: 10px 0; font-weight: bold;'>{overall_coverage:.0f}%</h1>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div style='text-align: left; padding: 20px; background-color: white; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <p style='color: #64748b; font-size: 16px; margin: 0;'>Communities @ Target</p>
                <h1 style='color: #1e293b; font-size: 48px; margin: 10px 0; font-weight: bold;'>{communities_at_target}/{total_communities}</h1>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Debug information (show in expander)
        with st.expander("🔍 Debug Info - Click to see data matching details"):
            st.write(f"**Total submissions in dataset:** {len(df_main_copy):,}")
            st.write(f"**Community column used:** `{community_col}`")
            if '_community_code_original' in df_main_copy.columns:
                st.write("**Using original community codes for matching:** ✅")
                st.write(f"**Unique community codes in data:** {df_main_copy['_community_code_original'].nunique()}")
            st.write(f"**Unique communities in data:** {df_main_copy[community_col].nunique()}")
            st.write(f"**Total communities in master list:** {len(COMMUNITY_DF)}")
            st.write(f"**Communities matched:** {coverage_table[coverage_table['Actual_Submissions'] > 0].shape[0]}")
            
            # Show sample of actual community values
            st.write("**Sample community names from data:**")
            st.dataframe(df_main_copy[community_col].value_counts().head(10), use_container_width=True)
            
            if '_community_code_original' in df_main_copy.columns:
                st.write("**Sample community codes from data:**")
                st.dataframe(df_main_copy['_community_code_original'].value_counts().head(10), use_container_width=True)
        
        # Display table
        st.markdown("#### Detailed Community Coverage")
        
        # Filter by LGA if not admin (case-insensitive)
        if st.session_state.user_role == 'lga':
            coverage_table = coverage_table[coverage_table['lga'].str.upper() == st.session_state.selected_lga.upper()]
        
        # Display columns
        display_coverage = coverage_table[[
            'lga', 'ward', 'Community', 'communitycode', 
            'Planned_Community', 'Actual_Submissions', 'Coverage_%', 'Status'
        ]].rename(columns={
            'lga': 'LGA',
            'ward': 'Ward',
            'Community': 'Community Name',
            'communitycode': 'Community Code',
            'Planned_Community': 'Planned HH',
            'Actual_Submissions': 'Actual HH',
            'Coverage_%': 'Coverage %'
        })
        
        # Color code the dataframe
        def highlight_status(row):
            if row['Status'] == '✅ Complete':
                return ['background-color: #d1fae5'] * len(row)
            elif row['Status'] == '⚠️ Partial':
                return ['background-color: #fef3c7'] * len(row)
            else:
                return ['background-color: #fee2e2'] * len(row)
        
        st.dataframe(
            display_coverage.style.apply(highlight_status, axis=1),
            use_container_width=True,
            hide_index=True,
            height=400
        )
    
    # Data Quality Issues
    st.markdown('<div class="section-header"><h2 class="section-title">🚨 Data Quality Alerts</h2></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        severity = "danger" if qc_metrics['duplicate_households'] > 0 else "success"
        st.markdown(
            f"""
            <div class="alert-box alert-{severity}">
                <strong>🏠 Duplicate Households:</strong> {qc_metrics['duplicate_households']:,}
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        severity = "danger" if qc_metrics['duplicate_mothers'] > 0 else "success"
        st.markdown(
            f"""
            <div class="alert-box alert-{severity}">
                <strong>👩 Duplicate Mothers:</strong> {qc_metrics['duplicate_mothers']:,}
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        severity = "danger" if qc_metrics['duplicate_children'] > 0 else "success"
        st.markdown(
            f"""
            <div class="alert-box alert-{severity}">
                <strong>👶 Duplicate Children:</strong> {qc_metrics['duplicate_children']:,}
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Quality Control Checks Section
    st.markdown('<div class="section-header"><h2 class="section-title">🔍 Quality Control Checks</h2></div>', unsafe_allow_html=True)
    
    # Perform comprehensive QC checks on ORIGINAL unfiltered data
    qc_issues_df = perform_comprehensive_qc_checks(df_main_original, df_mother_original, df_child_original)
    
    # If user is LGA, filter QC issues to show only their LGA (case-insensitive)
    if st.session_state.user_role == 'lga':
        lga_col_name = 'Q3. Local Government Area'
        if 'LGA' in qc_issues_df.columns:
            qc_issues_df = qc_issues_df[qc_issues_df['LGA'].str.upper() == st.session_state.selected_lga.upper()]
        elif lga_col_name in qc_issues_df.columns:
            qc_issues_df = qc_issues_df[qc_issues_df[lga_col_name].str.upper() == st.session_state.selected_lga.upper()]
    
    # Calculate QC metrics safely
    total_issues = len(qc_issues_df)
    
    # Check if qc_issues_df has data and the required column before accessing it
    if not qc_issues_df.empty and 'Issue Type' in qc_issues_df.columns:
        age_inconsistencies = len(qc_issues_df[qc_issues_df['Issue Type'] == 'Age Inconsistency'])
        other_issues = total_issues - age_inconsistencies
    else:
        age_inconsistencies = 0
        other_issues = 0
    
    duplicates = qc_metrics['duplicate_households'] + qc_metrics['duplicate_mothers'] + qc_metrics['duplicate_children']
    
    # Display QC summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Issues Found", f"{total_issues:,}")
    with col2:
        st.metric("Age Inconsistencies", f"{age_inconsistencies:,}")
    with col3:
        st.metric("Duplicates", f"{duplicates:,}")
    with col4:
        st.metric("Other Issues", f"{other_issues:,}")
    
    # Distribution of QC Issues Chart
    if not qc_issues_df.empty:
        st.markdown("#### Distribution of QC Issues")
        
        issue_counts = qc_issues_df['Issue Type'].value_counts().reset_index()
        issue_counts.columns = ['Issue Type', 'Count']
        
        fig = px.bar(
            issue_counts,
            x='Issue Type',
            y='Count',
            title='',
            color='Count',
            color_continuous_scale='Reds',
            text='Count'
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(
            height=400,
            xaxis_title="Issue Type",
            yaxis_title="Count",
            xaxis_tickangle=-45,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("✅ No QC issues detected! All data passes quality checks.")
    
    # Rejected Submissions Detail
    if qc_metrics['validation_rejected'] > 0:
        st.markdown('<div class="section-header"><h2 class="section-title">❌ Rejected Submissions - Action Required</h2></div>', unsafe_allow_html=True)
        
        validation_col = '_validation_status'
        username_col = find_column_with_keyword(df_main, 'username')
        if validation_col in df_main.columns:
            rejected_df = df_main[df_main[validation_col] == 'Not Approved'].copy()
            
            if not rejected_df.empty:
                display_cols = ['unique_code', username_col, 'Q3. Local Government Area', 
                               'Q4. Ward', 'Q5. Community Name', 'start']
                display_cols = [col for col in display_cols if col in rejected_df.columns]
                
                st.dataframe(
                    rejected_df[display_cols].sort_values('start', ascending=False),
                    use_container_width=True,
                    hide_index=True
                )
                
                st.markdown(
                    """
                    <div class="alert-box alert-danger">
                        <strong>⚠️ Action Required:</strong> These submissions must be reviewed and recollected.
                        Contact the respective enumerators immediately.
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    # Detailed QC Issues Table - Moved to the end
    if not qc_issues_df.empty:
        st.markdown('<div class="section-header"><h2 class="section-title">📋 Detailed QC Issues Table</h2></div>', unsafe_allow_html=True)
        st.markdown(f"**{total_issues:,}** issues flagged across LGA, Ward, and Community")
        
        # Add filter expander
        with st.expander("🔍 Filter QC Issues (Optional)"):
            filter_col1, filter_col2, filter_col3 = st.columns(3)
            
            with filter_col1:
                selected_lga_filter = st.multiselect(
                    "Filter by LGA",
                    options=sorted(qc_issues_df['LGA'].unique().tolist()),
                    default=None
                )
            
            with filter_col2:
                selected_issue_type = st.multiselect(
                    "Filter by Issue Type",
                    options=sorted(qc_issues_df['Issue Type'].unique().tolist()),
                    default=None
                )
            
            with filter_col3:
                selected_validation = st.multiselect(
                    "Filter by Validation Status",
                    options=sorted(qc_issues_df['Validation Status'].dropna().unique().tolist()),
                    default=None
                )
        
        # Apply filters
        filtered_qc_df = qc_issues_df.copy()
        if selected_lga_filter:
            filtered_qc_df = filtered_qc_df[filtered_qc_df['LGA'].isin(selected_lga_filter)]
        if selected_issue_type:
            filtered_qc_df = filtered_qc_df[filtered_qc_df['Issue Type'].isin(selected_issue_type)]
        if selected_validation:
            filtered_qc_df = filtered_qc_df[filtered_qc_df['Validation Status'].isin(selected_validation)]
        
        # Display filtered table
        st.dataframe(
            filtered_qc_df,
            use_container_width=True,
            hide_index=True,
            height=400
        )
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #64748b; padding: 2rem;">
            <p><strong>SARMAAN II - Safety and Antimicrobial Resistance of Mass Administration of Azithromycin</strong></p>
            <p>Near real-time data quality monitoring system for AMR</p>
            <p style="font-size: 0.85rem; margin-top: 1rem;">
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- MAIN APPLICATION FLOW ----------------
def main():
    """Main application entry point"""
    
    if not st.session_state.logged_in:
        login_page()
    else:
        # Load data
        df_main, df_mother, df_child = load_data()
        
        if df_main.empty:
            st.error("❌ No data available. Please check your data source.")
            if st.button("🚪 Logout"):
                st.session_state.logged_in = False
                st.rerun()
        else:
            run_dashboard(df_main, df_mother, df_child)

if __name__ == "__main__":
    main()

