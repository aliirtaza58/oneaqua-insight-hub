import streamlit as st
from src.engine import SCENARIO_PRESETS

def update_sliders_from_preset():
    """
    Callback triggered when the user picks a new simulation preset.
    Updates the session_state values of the sliders so they immediately sync visually.
    """
    selected = st.session_state.get("scenario_preset", "Baseline Telemetry")
    preset_data = SCENARIO_PRESETS.get(selected, SCENARIO_PRESETS["Baseline Telemetry"])
    st.session_state["temp_delta"] = float(preset_data["temp_delta"])
    st.session_state["rain_delta"] = float(preset_data["rain_delta"])
    st.session_state["riparian_delta"] = float(preset_data["riparian_delta"])

def render_simulator_sidebar():
    """
    Renders the scenario sandbox controls inside the sidebar as a compact control panel.
    Returns (temp_delta, rain_delta, riparian_delta).
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Scenario Sandbox")
    st.sidebar.caption("Stress-test urban freshwater indicators against simulated climate shocks & nature-based solutions.")

    # Initialize slider session state if not already set
    if "temp_delta" not in st.session_state:
        st.session_state["temp_delta"] = 0.0
    if "rain_delta" not in st.session_state:
        st.session_state["rain_delta"] = 0.0
    if "riparian_delta" not in st.session_state:
        st.session_state["riparian_delta"] = 0.0

    selected_preset = st.sidebar.selectbox(
        "Simulation Preset:",
        options=list(SCENARIO_PRESETS.keys()),
        index=0,
        key="scenario_preset",
        on_change=update_sliders_from_preset
    )

    preset_data = SCENARIO_PRESETS[selected_preset]
    st.sidebar.info(f"{preset_data['desc']}")

    temp_delta = st.sidebar.slider(
        "Temperature Anomaly (°C)",
        min_value=-2.0, max_value=6.0,
        step=0.5,
        key="temp_delta"
    )
    rain_delta = st.sidebar.slider(
        "Storm Runoff Intensity (mm/hr)",
        min_value=0.0, max_value=60.0,
        step=5.0,
        key="rain_delta"
    )
    riparian_delta = st.sidebar.slider(
        "Riparian Buffer Enhancement (%)",
        min_value=0.0, max_value=40.0,
        step=5.0,
        key="riparian_delta"
    )

    return temp_delta, rain_delta, riparian_delta
