# ================================
# SARMAAN II AMR YOBE STATE - QC DASHBOARD
# Advanced Quality Control Dashboard for Antimicrobial Resistance Study
# ================================

from datetime import date
import pandas as pd
import streamlit as st
import requests
from io import BytesIO
import plotly.express as px

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="SARMAAN II AMR Dashboard - Yobe State",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🏥"
)

# ---------------- ADMIN CREDENTIALS ----------------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "SARMAAN2024@AMR"

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
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-left: 4px solid var(--primary-blue);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-blue);
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.95rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
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
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .dashboard-title { font-size: 2rem; }
        .metric-value { font-size: 2rem; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- DATA SOURCE ----------------
# Replace with your actual KoboToolbox export URL
DATA_URL = "https://kf.kobotoolbox.org/api/v2/assets/aCddKcS2rVF7zJP9fHRWPz/export-settings/esgZhUs8BZoiVwYSPbLHSHA/data.xlsx"
MAIN_SHEET = "SARMAAN II AMR YOBE STATE"
MOTHER_SHEET = "mother_information"
CHILD_SHEET = "child_info"

# ---------------- SESSION STATE INITIALIZATION ----------------
# Auto-login as Admin (set to False to enable login page)
AUTO_LOGIN_ADMIN = True

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
Yobe,Bade,Dagona,Zango Loko,C1-110111,14
Yobe,Bade,Dagona,Zango Company,C1-110112,44
Yobe,Bade,Katuzu,Kaikabo,C1-110121,25
Yobe,Bade,Katuzu,Kara,C1-110122,41
Yobe,Bade,Lawan Fannami,Babuje,C1-110131,21
Yobe,Bade,Lawan Fannami,Bagar Dankoli,C1-110132,11
Yobe,Bade,Sabon Gari,Asibitin Agana,C1-110141,26
Yobe,Bade,Sabon Gari,Kabalan Kara Arfo,C1-110142,21
Yobe,Bade,Sarkin Hausawa,Sarkin Ruwa B,C1-110151,9
Yobe,Bade,Sarkin Hausawa,Tsangayan Alhaji Usman Idris,C1-110152,43
Yobe,Bursari,Danani/Lawanti,Ganawajiri Alhaji,C1-110211,9
Yobe,Bursari,Danani/Lawanti,Matti Umarari,C1-110212,13
Yobe,Bursari,Dapchi,Bulama Adamu Kellumi Gundumari,C1-110221,29
Yobe,Bursari,Dapchi,Bulama Burah,C1-110222,42
Yobe,Bursari,Guji/Metalari,Ajiri Goniri,C1-110231,22
Yobe,Bursari,Guji/Metalari,Karasuwa,C1-110232,15
Yobe,Bursari,Jawa Garun Dole,Garin Alkali Bamusu,C1-110241,53
Yobe,Bursari,Jawa Garun Dole,Garun Dole Lawanti,C1-110242,35
Yobe,Bursari,Juluri/Damnawa,G Mai Njiru,C1-110251,20
Yobe,Bursari,Juluri/Damnawa,Gamsa Goniri,C1-110252,18
Yobe,Damaturu,Bindigari/Pawari,Alimarami Ext North,C1-110311,34
Yobe,Damaturu,Bindigari/Pawari,Bra Bra West,C1-110312,17
Yobe,Damaturu,Damakasu,Kimeri Modubulama Bindi,C1-110321,15
Yobe,Damaturu,Damakasu,Maji Kauri,C1-110322,21
Yobe,Damaturu,Kalallawa/Gabai,Kalallawa B Ahmad,C1-110331,17
Yobe,Damaturu,Kalallawa/Gabai,Kangol,C1-110332,21
Yobe,Damaturu,Kukareta/Warsala,Bulama Mustapha Tanko,C1-110341,13
Yobe,Damaturu,Kukareta/Warsala,Bulama Ya Kana,C1-110342,22
Yobe,Damaturu,Nayinawa,Abbari Byepass,C1-110351,57
Yobe,Damaturu,Nayinawa,Abbari Pri Sch Area,C1-110352,39
Yobe,Fika,Gadaka/Shembire,Anguwan Ibrahim Allahure,C1-110411,14
Yobe,Fika,Gadaka/Shembire,Dala Koe,C1-110412,30
Yobe,Fika,Garu,Garu,C1-110421,18
Yobe,Fika,Garu,Seminti Anguwan Malam Buba,C1-110422,27
Yobe,Fika,Gudi Dozi,Lawe Shula,C1-110431,33
Yobe,Fika,Gudi Dozi,Umaru Dari,C1-110432,9
Yobe,Fika,Janga,Damshi,C1-110441,20
Yobe,Fika,Janga,Gashaka Ung Sa Adu,C1-110442,24
Yobe,Fika,Ngalda Dumbulwa,Unguwan Madu,C1-110451,59
Yobe,Fika,Ngalda Dumbulwa,Dambuna Mtn,C1-110452,20
Yobe,Fune,Ngelzarma B,Abakire Katsuwa,C1-110511,55
Yobe,Fune,Ngelzarma B,Bulawaini,C1-110512,23
Yobe,Fune,Daura A,Bijawa Yamma,C1-110521,24
Yobe,Fune,Daura A,Bulanguwa,C1-110522,36
Yobe,Fune,Daura B,Anguwan Gamji,C1-110531,17
Yobe,Fune,Daura B,Dankara,C1-110532,12
Yobe,Fune,Mashio,Shanga B Saidu,C1-110541,16
Yobe,Fune,Mashio,Dumbulwa Jauro Adamu,C1-110542,37
Yobe,Fune,Kolere/Kafaje,Balangu,C1-110551,15
Yobe,Fune,Kolere/Kafaje,Balarabe Ali,C1-110552,22
Yobe,Geidam,Asheikiri,Alhaji Goggo,C1-110611,20
Yobe,Geidam,Asheikiri,Bulama Isiyaku,C1-110612,21
Yobe,Geidam,Balle,Fulatari B Marawa,C1-110621,52
Yobe,Geidam,Balle,Kelluri B Bukar,C1-110622,27
Yobe,Geidam,Jororo,Kalgeri Hausari,C1-110631,36
Yobe,Geidam,Jororo,Kalari,C1-110632,21
Yobe,Geidam,Ma'Anna,Bukar Ganari,C1-110641,11
Yobe,Geidam,Ma'Anna,Karamma,C1-110642,11
Yobe,Geidam,Kolori,Bulama Miko,C1-110651,35
Yobe,Geidam,Kolori,Fulatari Engine,C1-110652,23
Yobe,Gujba,Wagir,Jauro Guru,C1-110711,15
Yobe,Gujba,Wagir,Ngaurawa,C1-110712,44
Yobe,Gujba,Buni Yadi,Alhaji Haruna Sarkin Aska,C1-110721,20
Yobe,Gujba,Buni Yadi,Audu Gazari,C1-110722,18
Yobe,Gujba,Mutai,Bandila,C1-110731,18
Yobe,Gujba,Mutai,Dingare,C1-110732,14
Yobe,Gujba,Buni Gari,Buni West,C1-110741,28
Yobe,Gujba,Buni Gari,Bulama Yaga,C1-110742,17
Yobe,Gujba,Gujba,Bulama Shettima,C1-110751,36
Yobe,Gujba,Gujba,Bungai,C1-110752,46
Yobe,Gulani,Bara,Gala Chiroma B,C1-110811,50
Yobe,Gulani,Bara,Jauro Jao,C1-110812,10
Yobe,Gulani,Bularafa,Shishiwaji,C1-110821,33
Yobe,Gulani,Bularafa,Umar Mai Kwariya,C1-110822,28
Yobe,Gulani,Bumsa,Garagari,C1-110831,16
Yobe,Gulani,Bumsa,Gargari Sabo,C1-110832,34
Yobe,Gulani,Dokshi,Doarga,C1-110841,15
Yobe,Gulani,Dokshi,Dokshi Anguwan Balari,C1-110842,8
Yobe,Gulani,Gulani,Gala Bahamma,C1-110851,27
Yobe,Gulani,Gulani,Gala Chiroma,C1-110852,35
Yobe,Jakusko,Dumbari,Dumbari Tsangaya,C1-110911,39
Yobe,Jakusko,Dumbari,Ardo Manu,C1-110912,25
Yobe,Jakusko,Girgir/Bayam,Bayam Ang Lawan,C1-110921,21
Yobe,Jakusko,Girgir/Bayam,Garin Buri,C1-110922,51
Yobe,Jakusko,Zabudum/Dachia,Amshi An Galadima,C1-110931,7
Yobe,Jakusko,Zabudum/Dachia,Amshi An Hausawa,C1-110932,20
Yobe,Jakusko,Jawur Katama,Alhaji Jauro,C1-110941,20
Yobe,Jakusko,Jawur Katama,Jama Are,C1-110942,15
Yobe,Jakusko,Lafia Loi Loi,Babawuro,C1-110951,27
Yobe,Jakusko,Lafia Loi Loi,Gada,C1-110952,30
Yobe,Karasuwa,Fajiganari,Alhaji Maina,C1-111011,11
Yobe,Karasuwa,Fajiganari,Garin Mallam,C1-111012,14
Yobe,Karasuwa,Garin Gawo,Buddum,C1-111021,15
Yobe,Karasuwa,Garin Gawo,Garin Gawo,C1-111022,32
Yobe,Karasuwa,Gasma,Gadan Dinya,C1-111031,36
Yobe,Karasuwa,Gasma,Garin Ahmadu Lawanti,C1-111032,25
Yobe,Karasuwa,Karasuwa Galu,Garin Goni,C1-111041,45
Yobe,Karasuwa,Karasuwa Galu,Karasuwa Galu B,C1-111042,11
Yobe,Karasuwa,Karasuwa Garin Guna,Baja,C1-111051,13
Yobe,Karasuwa,Karasuwa Garin Guna,Hausari,C1-111052,54
Yobe,Machina,Dole Machina,Hardo M Azu,C1-111111,13
Yobe,Machina,Dole Machina,Inkibulwa Tari,C1-111112,16
Yobe,Machina,Falimaram,Abbari Adambe,C1-111121,20
Yobe,Machina,Falimaram,Ariyamari,C1-111122,18
Yobe,Machina,Konkomma,Alhaji Hari,C1-111131,24
Yobe,Machina,Konkomma,Ariyamari,C1-111132,36
Yobe,Machina,Kukayasku,Garin Isa Tsangayan Bukari,C1-111141,24
Yobe,Machina,Kukayasku,Kambar Anguwan Maigari Usaini,C1-111142,12
Yobe,Machina,Machina,Mafidu M Mamman,C1-111151,28
Yobe,Machina,Machina,Maina Islamia,C1-111152,63
Yobe,Nangere,Dawasa/Garin Baba,Bagaldi,C1-111211,11
Yobe,Nangere,Dawasa/Garin Baba,Katsalle,C1-111212,24
Yobe,Nangere,Degubi,Degubi Sarki,C1-111221,9
Yobe,Nangere,Degubi,Gabur Sarki,C1-111222,8
Yobe,Nangere,Duddaye/Pakarau,Duddaye,C1-111231,37
Yobe,Nangere,Duddaye/Pakarau,Garin Shuwa,C1-111232,39
Yobe,Nangere,Kukuri/Chiromari,Hassan Girema,C1-111241,28
Yobe,Nangere,Kukuri/Chiromari,Minchika,C1-111242,15
Yobe,Nangere,Nangere,Makwayo,C1-111251,36
Yobe,Nangere,Nangere,Mallam Sarkin Fawa,C1-111252,48
Yobe,Nguru,Afunori,Afunori,C1-111311,93
Yobe,Nguru,Afunori,Kaigamari,C1-111312,26
Yobe,Nguru,Bulabulin,Goruba Haruna Pharmacy,C1-111321,18
Yobe,Nguru,Bulabulin,Layin Mai Malamala,C1-111322,16
Yobe,Nguru,Bulanguwa,Balanguwa Lawanti,C1-111331,8
Yobe,Nguru,Bulanguwa,Gwalgwale Aug Arewa,C1-111332,20
Yobe,Nguru,Dabule,Jajiruwa,C1-111341,17
Yobe,Nguru,Dabule,Kallari,C1-111342,30
Yobe,Nguru,Dumsai,Garin Mallam,C1-111351,11
Yobe,Nguru,Dumsai,Dumsai,C1-111352,16
Yobe,Potiskum,Bare Bari,Atiyaye,C1-111411,22
Yobe,Potiskum,Bare Bari,Jigawa City Petroleum,C1-111412,25
Yobe,Potiskum,Bolewa A,Baban Sani,C1-111421,17
Yobe,Potiskum,Bolewa A,Bm Maina Yusuf,C1-111422,15
Yobe,Potiskum,Bolewa B,Audu 77,C1-111431,16
Yobe,Potiskum,Bolewa B,M Dalibi,C1-111432,11
Yobe,Potiskum,Dogo Nini,Adamu Doctor,C1-111441,22
Yobe,Potiskum,Dogo Nini,Adamu Wanzam,C1-111442,36
Yobe,Potiskum,Dogo Tebo,Aliyu Daya,C1-111451,8
Yobe,Potiskum,Dogo Tebo,Bayan Cabs,C1-111452,83
Yobe,Tarmuwa,Babangida,B Hammadu Pawari,C1-111511,30
Yobe,Tarmuwa,Babangida,Bulama Bulau Arewa,C1-111512,28
Yobe,Tarmuwa,Biriri,Galadimawa,C1-111521,22
Yobe,Tarmuwa,Biriri,Tashan Biri,C1-111522,29
Yobe,Tarmuwa,Mandadawa,Kojolowa,C1-111531,18
Yobe,Tarmuwa,Mandadawa,Koromari,C1-111532,40
Yobe,Tarmuwa,Koriyel,Barbuma,C1-111541,7
Yobe,Tarmuwa,Koriyel,Fulatari,C1-111542,25
Yobe,Tarmuwa,Lantewa,Bulama Fugu,C1-111551,18
Yobe,Tarmuwa,Lantewa,Bulama Audu,C1-111552,40
Yobe,Yunusari,Yunusari,Ali Butari,C1-111611,16
Yobe,Yunusari,Yunusari,Izala Mosque,C1-111612,23
Yobe,Yunusari,Zajibiriri/Dumbol,Dumbol Lawanti,C1-111621,35
Yobe,Yunusari,Zajibiriri/Dumbol,Fulatari Musaye,C1-111622,13
Yobe,Yunusari,Dilala/Kalgi,Mustafari,C1-111631,18
Yobe,Yunusari,Dilala/Kalgi,Yawule,C1-111632,28
Yobe,Yunusari,Kafiya,Bukar Matoye,C1-111641,40
Yobe,Yunusari,Kafiya,Kattisulum,C1-111642,35
Yobe,Yunusari,Toshia,Fulatari Near Toshia,C1-111651,26
Yobe,Yunusari,Toshia,Goni Mele Street,C1-111652,21
Yobe,Yusufari,Bulatura,Jekifada,C1-111711,13
Yobe,Yusufari,Bulatura,Sunomari Bulin,C1-111712,50
Yobe,Yusufari,Yusufari,Limanti,C1-111721,23
Yobe,Yusufari,Yusufari,Zangoma Manga,C1-111722,17
Yobe,Yusufari,Guya,Kasharam Fusemi,C1-111731,20
Yobe,Yusufari,Guya,Maibugori,C1-111732,36
Yobe,Yusufari,Jebuwa,Lamido Ali,C1-111741,31
Yobe,Yusufari,Jebuwa,Shutti,C1-111742,71
Yobe,Yusufari,Mayori,Kerewa A Maigari Maina,C1-111751,17
Yobe,Yusufari,Mayori,Kerewa Buk ar,C1-111752,32"""

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
# Format: {lga_username: (password, lga_name, [wards_list])}
LGA_CREDENTIALS = {
    "bade": ("Bade@2024", "Bade"),
    "bursari": ("Bursari@2024", "Bursari"),
    "damaturu": ("Damaturu@2024", "Damaturu"),
    "fika": ("Fika@2024", "Fika"),
    "fune": ("Fune@2024", "Fune"),
    "geidam": ("Geidam@2024", "Geidam"),
    "gujba": ("Gujba@2024", "Gujba"),
    "gulani": ("Gulani@2024", "Gulani"),
    "jakusko": ("Jakusko@2024", "Jakusko"),
    "karasuwa": ("Karasuwa@2024", "Karasuwa"),
    "machina": ("Machina@2024", "Machina"),
    "nangere": ("Nangere@2024", "Nangere"),
    "nguru": ("Nguru@2024", "Nguru"),
    "potiskum": ("Potiskum@2024", "Potiskum"),
    "tarmuwa": ("Tarmuwa@2024", "Tarmuwa"),
    "yunusari": ("Yunusari@2024", "Yunusari"),
    "yusufari": ("Yusufari@2024", "Yusufari"),
}

# ---------------- DATA LOADING FUNCTION ----------------
@st.cache_data(show_spinner="📊 Loading SARMAAN II AMR data...", ttl=600)
def load_data(force_refresh=False):
    """Load data from KoboToolbox API"""
    try:
        # Load data from KoboToolbox API
        response = requests.get(DATA_URL, timeout=60)
        response.raise_for_status()
        excel_file = BytesIO(response.content)
        
        # Load all sheets
        data_dict = pd.read_excel(excel_file, sheet_name=None)
        
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
        st.markdown('<h2 class="login-title">🔐 Secure Login</h2>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                login_button = st.form_submit_button("🔓 Login", use_container_width=True)
            with col_b:
                help_button = st.form_submit_button("❓ Help", use_container_width=True)
            
            if login_button:
                # Check admin login
                if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                    st.session_state.logged_in = True
                    st.session_state.current_user = username
                    st.session_state.user_role = 'admin'
                    st.success("✅ Admin login successful!")
                    st.rerun()
                
                # Check LGA login
                elif username.lower() in LGA_CREDENTIALS:
                    pwd, lga_name = LGA_CREDENTIALS[username.lower()]
                    if password == pwd:
                        st.session_state.logged_in = True
                        st.session_state.current_user = username
                        st.session_state.user_role = 'lga'
                        st.session_state.selected_lga = lga_name
                        st.success(f"✅ Login successful! Welcome {lga_name} LGA supervisor")
                        st.rerun()
                    else:
                        st.error("❌ Invalid password")
                else:
                    st.error("❌ Invalid username or password")
            
            if help_button:
                st.info("""
                **Login Instructions:**
                - **LGA Supervisors**: Use your LGA username (e.g., 'potiskum', 'bade') and password
                - **Admin**: Use admin credentials to view all data
                
                **Example LGA Logins:**
                - Username: potiskum, Password: Potiskum@2024
                - Username: bade, Password: Bade@2024
                
                Contact your M&E coordinator for login issues
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
            <p class="dashboard-subtitle">Yobe State - Quality Control & Monitoring System</p>
            <div class="user-badge">👤 {user_role_display}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Filter data based on user role
    if st.session_state.user_role == 'lga':
        lga_col = find_column_with_keyword(df_main, 'Local Government')
        
        if lga_col and lga_col in df_main.columns:
            df_main = df_main[df_main[lga_col] == st.session_state.selected_lga]
            
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
                    df_main = df_main[df_main[lga_col] == selected_lga]
            
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
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">🏠 Total Households</div>
                <div class="metric-value">{qc_metrics['total_households']:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">👩 Total Mothers</div>
                <div class="metric-value">{qc_metrics['total_mothers']:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">👶 Total Children</div>
                <div class="metric-value">{qc_metrics['total_children']:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">💊 AZM Received</div>
                <div class="metric-value">{qc_metrics['azm_received']:,}</div>
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
    
    # Adverse Events Section
    if qc_metrics['adverse_events'] > 0:
        st.markdown('<div class="section-header"><h2 class="section-title">⚠️ Adverse Events Monitoring</h2></div>', unsafe_allow_html=True)
        
        st.markdown(
            f"""
            <div class="alert-box alert-warning">
                <strong>⚠️ Adverse Events Reported:</strong> {qc_metrics['adverse_events']:,} cases
                <br>
                <small>Requires immediate attention from medical team</small>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Show adverse events details if available
        if not df_mother.empty:
            ae_col = 'Q59. Did the child experience any adverse events?'
            if ae_col in df_mother.columns:
                ae_mothers = df_mother[df_mother[ae_col] == 'Yes']
                
                if not ae_mothers.empty:
                    with st.expander("📋 View Adverse Events Details"):
                        display_cols = ['Household ID', 'Mother ID', "Q51. Mother ${mother_id_001} name"]
                        display_cols = [col for col in display_cols if col in ae_mothers.columns]
                        st.dataframe(ae_mothers[display_cols], use_container_width=True)
    
    # Detailed Quality Issues
    st.markdown('<div class="section-header"><h2 class="section-title">🔍 Detailed Quality Issues</h2></div>', unsafe_allow_html=True)
    
    issues_df = identify_data_quality_issues(df_main, df_mother, df_child)
    
    if not issues_df.empty:
        for _, issue in issues_df.iterrows():
            severity_class = {
                'High': 'danger',
                'Medium': 'warning',
                'Low': 'info'
            }.get(issue['severity'], 'info')
            
            st.markdown(
                f"""
                <div class="alert-box alert-{severity_class}">
                    <strong>{issue['category']}:</strong> {issue['description']}
                    <br>
                    <span class="qc-badge qc-{severity_class}">Severity: {issue['severity']}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.success("✅ No major data quality issues detected!")
    
    # Enumerator Performance
    st.markdown('<div class="section-header"><h2 class="section-title">👥 Enumerator Performance</h2></div>', unsafe_allow_html=True)
    
    username_col = find_column_with_keyword(df_main, 'username')
    if username_col and username_col in df_main.columns:
        enumerator_stats = df_main.groupby(username_col).agg({
            '_uuid': 'count',
            '_validation_status': lambda x: (x == 'Approved').sum()
        }).reset_index()
        enumerator_stats.columns = ['Enumerator', 'Total Submissions', 'Approved Submissions']
        enumerator_stats['Approval Rate %'] = (
            enumerator_stats['Approved Submissions'] / enumerator_stats['Total Submissions'] * 100
        ).round(1)
        enumerator_stats = enumerator_stats.sort_values('Total Submissions', ascending=False)
        
        # Create bar chart
        fig = px.bar(
            enumerator_stats.head(10),
            x='Enumerator',
            y='Total Submissions',
            color='Approval Rate %',
            title='Top 10 Enumerators by Submission Count',
            color_continuous_scale='RdYlGn',
            text='Total Submissions'
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(
            height=400,
            xaxis_title="Enumerator",
            yaxis_title="Total Submissions",
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Show table
        with st.expander("📊 View Full Enumerator Statistics"):
            st.dataframe(enumerator_stats, use_container_width=True, hide_index=True)
    
    # Geographic Coverage
    st.markdown('<div class="section-header"><h2 class="section-title">🗺️ Geographic Coverage</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        ward_col = find_column_with_keyword(df_main, 'Ward')
        if ward_col and ward_col in df_main.columns:
            ward_counts = df_main[ward_col].value_counts().reset_index()
            ward_counts.columns = ['Ward', 'Submissions']
            
            fig = px.pie(
                ward_counts,
                values='Submissions',
                names='Ward',
                title='Submissions by Ward',
                hole=0.4
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        community_col = find_column_with_keyword(df_main, 'Community')
        if community_col and community_col in df_main.columns:
            community_counts = df_main[community_col].value_counts().head(10).reset_index()
            community_counts.columns = ['Community', 'Submissions']
            
            fig = px.bar(
                community_counts,
                x='Submissions',
                y='Community',
                orientation='h',
                title='Top 10 Communities by Submissions',
                color='Submissions',
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Community Coverage Table with Planned vs Actual
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
        
        # Display summary stats
        col1, col2, col3, col4 = st.columns(4)
        total_communities = len(coverage_table)
        completed = (coverage_table['Actual_Submissions'] >= coverage_table['Planned_Community']).sum()
        partial = ((coverage_table['Actual_Submissions'] > 0) & (coverage_table['Actual_Submissions'] < coverage_table['Planned_Community'])).sum()
        not_started = (coverage_table['Actual_Submissions'] == 0).sum()
        
        with col1:
            st.metric("Total Communities", f"{total_communities:,}")
        with col2:
            st.metric("✅ Completed", f"{completed:,}", delta=f"{(completed/total_communities*100):.1f}%")
        with col3:
            st.metric("⚠️ Partial", f"{partial:,}", delta=f"{(partial/total_communities*100):.1f}%")
        with col4:
            st.metric("❌ Not Started", f"{not_started:,}", delta=f"{(not_started/total_communities*100):.1f}%")
        
        # Display table
        st.markdown("#### Detailed Community Coverage")
        
        # Filter by LGA if not admin
        if st.session_state.user_role == 'lga':
            coverage_table = coverage_table[coverage_table['lga'] == st.session_state.selected_lga]
        
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
        
        # Download button
        csv = display_coverage.to_csv(index=False)
        st.download_button(
            label="📥 Download Community Coverage Report",
            data=csv,
            file_name=f"community_coverage_{date.today()}.csv",
            mime="text/csv"
        )
    
    # Data Collection Timeline
    st.markdown('<div class="section-header"><h2 class="section-title">📅 Data Collection Timeline</h2></div>', unsafe_allow_html=True)
    
    if 'start' in df_main.columns and not df_main.empty:
        daily_counts = df_main.groupby(df_main['start'].dt.date).size().reset_index()
        daily_counts.columns = ['Date', 'Submissions']
        
        fig = px.line(
            daily_counts,
            x='Date',
            y='Submissions',
            title='Daily Submission Trends',
            markers=True
        )
        fig.update_layout(
            height=400,
            xaxis_title="Date",
            yaxis_title="Number of Submissions",
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Rejected Submissions Detail
    if qc_metrics['validation_rejected'] > 0:
        st.markdown('<div class="section-header"><h2 class="section-title">❌ Rejected Submissions - Action Required</h2></div>', unsafe_allow_html=True)
        
        validation_col = '_validation_status'
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
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #64748b; padding: 2rem;">
            <p><strong>SARMAAN II - Safety and Antimicrobial Resistance of Mass Administration of Azithromycin</strong></p>
            <p>Near real-time data quality monitoring system for AMR</p>
            <p style="font-size: 0.85rem; margin-top: 1rem;">
                Dashboard Version 2.0 | Last Updated: December 2025
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
