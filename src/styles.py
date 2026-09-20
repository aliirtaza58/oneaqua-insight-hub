import streamlit as st

def apply_custom_styles():
    """
    Injects custom CSS to give Streamlit a modern dark slate glassmorphism theme
    with neon cyan (#00F2FE) highlights and custom KPI cards.
    """
    custom_css = """
    <style>
        /* Import Outfit Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Outfit', sans-serif;
        }

        /* Main Container Styling */
        .stApp {
            background-color: #0D1117;
            color: #F0F6FC;
        }

        /* Glassmorphism Header Bar */
        .glass-header {
            background: rgba(22, 27, 34, 0.75);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 20px 24px;
            margin-bottom: 24px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }

        .glass-header h1 {
            color: #00F2FE;
            font-weight: 700;
            font-size: 2.2rem;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .glass-header p {
            color: #8B949E;
            margin: 6px 0 0 0;
            font-size: 1.05rem;
        }

        /* KPI Card Styling */
        .kpi-card {
            background: rgba(22, 27, 34, 0.85);
            border: 1px solid rgba(0, 242, 254, 0.2);
            border-radius: 14px;
            padding: 18px;
            text-align: center;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }

        .kpi-card:hover {
            transform: translateY(-3px);
            border-color: #00F2FE;
            box-shadow: 0 6px 20px rgba(0, 242, 254, 0.15);
        }

        .kpi-title {
            color: #8B949E;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            font-weight: 600;
            margin-bottom: 6px;
        }

        .kpi-value {
            font-size: 2rem;
            font-weight: 700;
            color: #FFFFFF;
        }

        .kpi-status-good {
            color: #2EA043;
            font-weight: 600;
            font-size: 0.85rem;
        }

        .kpi-status-warning {
            color: #D29922;
            font-weight: 600;
            font-size: 0.85rem;
        }

        .kpi-status-critical {
            color: #F85149;
            font-weight: 600;
            font-size: 0.85rem;
        }

        /* Pilot City Badge */
        .city-badge {
            background: linear-gradient(135deg, rgba(0, 242, 254, 0.15), rgba(46, 160, 67, 0.15));
            border: 1px solid #00F2FE;
            color: #00F2FE;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            display: inline-block;
        }

        /* Section Title */
        .section-header {
            color: #F0F6FC;
            font-weight: 600;
            font-size: 1.4rem;
            margin-top: 18px;
            margin-bottom: 12px;
            border-bottom: 2px solid rgba(0, 242, 254, 0.3);
            padding-bottom: 6px;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #161B22;
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }

        /* Tab Bar Highlights */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: rgba(22, 27, 34, 0.6);
            border-radius: 8px 8px 0px 0px;
            color: #8B949E;
            padding: 10px 16px;
            font-weight: 500;
        }

        .stTabs [aria-selected="true"] {
            background-color: rgba(0, 242, 254, 0.15) !important;
            color: #00F2FE !important;
            border-bottom: 2px solid #00F2FE !important;
        }

        /* Custom Scrollbars */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0D1117;
        }
        ::-webkit-scrollbar-thumb {
            background: #30363D;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #00F2FE;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
