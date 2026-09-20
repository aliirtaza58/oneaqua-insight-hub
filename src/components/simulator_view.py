import streamlit as st

def render_simulator_view():
    """
    Renders interactive "What-If" climate & urban intervention sliders.
    Returns slider offset values.
    """
    st.markdown("<div class='section-header'>⚡ Interactive Climate & Resilience Scenario Sandbox</div>", unsafe_allow_html=True)
    st.markdown("Simulate how sudden climate stressors or green infrastructure interventions impact stream health metrics in real time.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        temp_delta = st.slider("☀️ Heatwave Temperature Spike (°C)", 0.0, 5.0, 0.0, 0.5, help="Simulate increase in urban water temperature")
    with col2:
        rain_delta = st.slider("🌧️ Heavy Rainfall Event (mm/hr)", 0.0, 50.0, 0.0, 5.0, help="Simulate urban stormwater runoff surge")
    with col3:
        riparian_delta = st.slider("🌿 Riparian Vegetation Restoration (%)", 0.0, 30.0, 0.0, 5.0, help="Simulate planting stream buffer zones")
        
    return temp_delta, rain_delta, riparian_delta
