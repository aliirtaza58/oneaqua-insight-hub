import streamlit as st
from src.engine import SCENARIO_PRESETS

def render_simulator_view():
    """
    Renders interactive "What-If" climate scenario sandbox with 1-click presets
    and fine-tuning sliders.
    """
    st.markdown("<div class='ui-section-title'>⚡ Climate Stress & Resilience Scenario Sandbox</div>", unsafe_allow_html=True)
    st.markdown("Test how climate extremes or municipal nature-based solutions impact stream vital signs in real time.")
    
    # Preset Selector
    selected_preset = st.selectbox(
        "⚡ Choose a Realistic Simulation Scenario:",
        options=list(SCENARIO_PRESETS.keys()),
        index=0
    )
    
    preset_data = SCENARIO_PRESETS[selected_preset]
    st.info(f"**Scenario Dynamics:** {preset_data['desc']}")
    
    # Sliders initialized with preset values
    col1, col2, col3 = st.columns(3)
    
    with col1:
        temp_delta = st.slider(
            "☀️ Heatwave Temperature Spike (°C)",
            min_value=-2.0, max_value=6.0,
            value=float(preset_data["temp_delta"]),
            step=0.5,
            help="Simulates water temperature increase reducing oxygen saturation."
        )
    with col2:
        rain_delta = st.slider(
            "🌧️ Storm Runoff Volume (mm/hr)",
            min_value=0.0, max_value=60.0,
            value=float(preset_data["rain_delta"]),
            step=5.0,
            help="Simulates heavy rainfall causing combined sewer overflow and runoff."
        )
    with col3:
        riparian_delta = st.slider(
            "🌿 Buffer Restoration (%)",
            min_value=0.0, max_value=40.0,
            value=float(preset_data["riparian_delta"]),
            step=5.0,
            help="Simulates expanding native riparian vegetation buffers along stream banks."
        )
        
    return temp_delta, rain_delta, riparian_delta
