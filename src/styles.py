import streamlit as st

def apply_custom_styles():
    """
    Applies an ultra-modern dark-tech design system adhering to the UX/UI agent skill
    standards: WCAG 2.2 AA contrast, distinct typographic scale (Plus Jakarta Sans &
    JetBrains Mono for telemetry), layered glassmorphism cards, glowing status beacons,
    and responsive interactive controls.
    """
    custom_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

        /* Root CSS Variables */
        :root {
            --bg-base: #0B0E14;
            --bg-surface: #121721;
            --bg-elevated: #1A2232;
            --border-subtle: rgba(255, 255, 255, 0.08);
            --border-accent: rgba(0, 242, 254, 0.3);
            --text-primary: #F0F6FC;
            --text-secondary: #94A3B8;
            --text-muted: #64748B;
            --cyan-neon: #00F2FE;
            --cyan-glow: rgba(0, 242, 254, 0.2);
            --emerald-good: #10B981;
            --amber-warn: #F59E0B;
            --rose-danger: #F43F5E;
        }

        /* Base App Styling */
        .stApp {
            background-color: var(--bg-base);
            color: var(--text-primary);
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        /* Telemetry Numbers & Data Readouts */
        .data-mono {
            font-family: 'JetBrains Mono', monospace;
        }

        /* Top Brand Header */
        .brand-header {
            background: linear-gradient(135deg, rgba(18, 23, 33, 0.95) 0%, rgba(11, 14, 20, 0.9) 100%);
            border: 1px solid var(--border-accent);
            border-radius: 18px;
            padding: 22px 28px;
            margin-bottom: 22px;
            box-shadow: 0 10px 30px -10px rgba(0, 242, 254, 0.15);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }

        .brand-title-group h1 {
            font-size: 2.1rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            margin: 0;
            background: linear-gradient(90deg, #FFFFFF 0%, #00F2FE 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .brand-title-group p {
            color: var(--text-secondary);
            margin: 6px 0 0 0;
            font-size: 0.98rem;
            font-weight: 400;
        }

        /* Live Status Beacon */
        .live-beacon {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(16, 185, 129, 0.12);
            border: 1px solid rgba(16, 185, 129, 0.35);
            padding: 6px 14px;
            border-radius: 9999px;
            font-size: 0.82rem;
            font-weight: 600;
            color: #34D399;
            letter-spacing: 0.4px;
            text-transform: uppercase;
        }

        .pulse-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: #10B981;
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
            animation: pulse-ring 1.8s infinite cubic-bezier(0.66, 0, 0, 1);
        }

        @keyframes pulse-ring {
            0% {
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
            }
            70% {
                transform: scale(1);
                box-shadow: 0 0 0 8px rgba(16, 185, 129, 0);
            }
            100% {
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
            }
        }

        /* Hero Lead Metric Card */
        .hero-lead-card {
            background: linear-gradient(180deg, rgba(26, 34, 50, 0.8) 0%, rgba(18, 23, 33, 0.95) 100%);
            border: 1px solid rgba(0, 242, 254, 0.35);
            border-radius: 18px;
            padding: 24px;
            box-shadow: 0 12px 36px rgba(0, 0, 0, 0.4);
            margin-bottom: 22px;
            position: relative;
            overflow: hidden;
        }

        .hero-lead-card::after {
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 140px;
            height: 140px;
            background: radial-gradient(circle, rgba(0, 242, 254, 0.15) 0%, transparent 70%);
            pointer-events: none;
        }

        .hero-score-badge {
            font-size: 3.5rem;
            font-weight: 800;
            font-family: 'JetBrains Mono', monospace;
            line-height: 1;
            color: #FFFFFF;
        }

        /* Metric Pillar Cards */
        .pillar-card {
            background: rgba(18, 23, 33, 0.85);
            border: 1px solid var(--border-subtle);
            border-radius: 16px;
            padding: 20px;
            height: 100%;
            transition: all 0.25s ease;
            position: relative;
        }

        .pillar-card:hover {
            border-color: var(--cyan-neon);
            transform: translateY(-3px);
            box-shadow: 0 8px 24px var(--cyan-glow);
        }

        .pillar-header {
            font-size: 0.85rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            color: var(--text-secondary);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .pillar-value {
            font-size: 2.3rem;
            font-weight: 800;
            font-family: 'JetBrains Mono', monospace;
            color: #FFFFFF;
            margin-bottom: 6px;
        }

        /* Mini Progress Bars */
        .meter-track {
            background: rgba(255, 255, 255, 0.08);
            border-radius: 6px;
            height: 6px;
            width: 100%;
            margin: 10px 0;
            overflow: hidden;
        }

        .meter-fill-good {
            height: 100%;
            background: linear-gradient(90deg, #10B981, #34D399);
            border-radius: 6px;
        }

        .meter-fill-warn {
            height: 100%;
            background: linear-gradient(90deg, #F59E0B, #FBBF24);
            border-radius: 6px;
        }

        .meter-fill-danger {
            height: 100%;
            background: linear-gradient(90deg, #F43F5E, #FB7185);
            border-radius: 6px;
        }

        /* Status Chips */
        .chip-good {
            background: rgba(16, 185, 129, 0.15);
            color: #34D399;
            border: 1px solid rgba(16, 185, 129, 0.3);
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.78rem;
            font-weight: 600;
        }

        .chip-warn {
            background: rgba(245, 158, 11, 0.15);
            color: #FBBF24;
            border: 1px solid rgba(245, 158, 11, 0.3);
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.78rem;
            font-weight: 600;
        }

        .chip-danger {
            background: rgba(244, 63, 94, 0.15);
            color: #FB7185;
            border: 1px solid rgba(244, 63, 94, 0.3);
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.78rem;
            font-weight: 600;
        }

        /* Quick Scenario Pill Buttons */
        .scenario-box {
            background: rgba(18, 23, 33, 0.7);
            border: 1px solid var(--border-subtle);
            border-radius: 14px;
            padding: 16px 20px;
            margin: 18px 0;
        }

        /* Custom Streamlit Widgets */
        div[data-testid="stMetric"] {
            background: linear-gradient(180deg, rgba(18, 23, 33, 0.85) 0%, rgba(14, 18, 26, 0.95) 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 14px 16px;
            transition: all 0.2s ease;
        }

        div[data-testid="stMetric"]:hover {
            border-color: rgba(0, 242, 254, 0.3);
            box-shadow: 0 4px 16px rgba(0, 242, 254, 0.08);
        }

        div[data-testid="stMetricLabel"] {
            font-size: 0.8rem !important;
            font-weight: 600 !important;
            color: var(--text-secondary) !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        div[data-testid="stMetricValue"] {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 1.45rem !important;
            font-weight: 700 !important;
            color: #FFFFFF !important;
            white-space: nowrap !important;
        }

        div[data-testid="stMetricDelta"] {
            font-size: 0.78rem !important;
            font-weight: 600 !important;
        }

        /* Tab Navigation Bar */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background: rgba(18, 23, 33, 0.5);
            padding: 6px;
            border-radius: 12px;
            border: 1px solid var(--border-subtle);
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 8px;
            color: var(--text-secondary);
            font-weight: 600;
            padding: 8px 18px;
            border: 1px solid transparent;
            transition: all 0.2s ease;
        }

        .stTabs [data-baseweb="tab"]:hover {
            color: var(--text-primary);
            background: rgba(255, 255, 255, 0.04);
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, rgba(0, 242, 254, 0.18), rgba(16, 185, 129, 0.12)) !important;
            color: var(--cyan-neon) !important;
            border: 1px solid var(--border-accent) !important;
        }

        /* Section Headings */
        .ui-section-title {
            color: var(--text-primary);
            font-size: 1.3rem;
            font-weight: 700;
            margin: 24px 0 12px 0;
            display: flex;
            align-items: center;
            gap: 8px;
            letter-spacing: -0.3px;
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
