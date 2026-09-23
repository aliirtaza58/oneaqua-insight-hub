import folium
from streamlit_folium import st_folium
import streamlit as st

def render_map_view(city_data, segments, sensors_df, reports_df):
    """
    Renders an interactive Folium geospatial map with stream polylines,
    sensor nodes, citizen reports, and custom HTML overlays.
    """
    coords = city_data["coords"]
    zoom = city_data["zoom"]
    
    # Retrieve map API key from Streamlit secrets if present
    api_key = st.secrets.get("MAP_API_KEY", "")
    
    # Initialize Folium Map
    m = folium.Map(
        location=coords,
        zoom_start=zoom,
        tiles=None  # We add custom TileLayer explicitly
    )

    if api_key:
        # CartoDB dark tile layer with valid API Key
        folium.TileLayer(
            tiles=f"https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png?api_key={api_key}",
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            name="Dark Canvas",
            subdomains="abcd",
            max_zoom=19,
            control=True
        ).add_to(m)
    else:
        # High quality fallback (CartoDB Positron / OpenStreetMap)
        folium.TileLayer(
            tiles="CartoDB dark_matter",
            name="Dark Canvas",
            control=True
        ).add_to(m)
    
    # Feature Groups for Layer Control
    fg_streams = folium.FeatureGroup(name="Stream Health Segments", show=True)
    fg_sensors = folium.FeatureGroup(name="IoT Telemetry Stations", show=True)
    fg_citizens = folium.FeatureGroup(name="Citizen Science Reports", show=True)

    # Add Stream Segments (Polylines)
    for seg in segments:
        status_color = "#10B981" if seg['status'] == "Good" else ("#F59E0B" if seg['status'] == "Moderate" else "#F43F5E")
        popup_html = f"""
        <div style="font-family: 'Plus Jakarta Sans', Arial, sans-serif; width: 230px; padding: 6px; color: #1E293B;">
            <div style="font-weight: 700; font-size: 14px; margin-bottom: 4px; color: {status_color};">
                {seg['name']}
            </div>
            <div style="font-size: 11px; margin-bottom: 8px; color: #64748B;">Segment ID: {seg['segment_id']}</div>
            <div style="background: #F8FAFC; border-radius: 8px; padding: 8px; font-size: 12px; line-height: 1.6;">
                <b>Status:</b> <span style="color: {status_color}; font-weight: 600;">{seg['status']}</span><br/>
                <b>Dissolved O₂:</b> {seg['do_mg_l']} mg/L<br/>
                <b>Bio-Index:</b> {seg['macro_index']}/10<br/>
                <b>E. coli:</b> {seg['e_coli']} CFU/100mL<br/>
                <b>Vector Density:</b> {seg['vector_density']}/100
            </div>
        </div>
        """
        folium.PolyLine(
            locations=seg["coords"],
            color=status_color,
            weight=7,
            opacity=0.9,
            tooltip=f"{seg['name']} — {seg['status']}",
            popup=folium.Popup(popup_html, max_width=280)
        ).add_to(fg_streams)

    # Add IoT Sensor Nodes
    for _, row in sensors_df.iterrows():
        sensor_popup = f"""
        <div style="font-family: Arial, sans-serif; width: 190px; padding: 4px; color: #0F172A;">
            <b style="color: #0284C7;">{row['name']}</b><br/>
            <span style="font-size: 11px; color: #64748B;">Node ID: {row['node_id']}</span>
            <hr style="margin: 6px 0; border: none; border-top: 1px solid #E2E8F0;"/>
            <b>Status:</b> <span style="color: #10B981;">Online</span><br/>
            <b>Battery:</b> {row['battery']}%<br/>
            <b>Telemetry:</b> Active Data Stream
        </div>
        """
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=8,
            color="#00F2FE",
            weight=2,
            fill=True,
            fill_color="#00F2FE",
            fill_opacity=0.9,
            tooltip=f"Sensor Node: {row['name']} ({row['node_id']})",
            popup=folium.Popup(sensor_popup, max_width=220)
        ).add_to(fg_sensors)

    # Add Citizen Observation Reports
    for _, row in reports_df.iterrows():
        icon_color = "red" if row["severity"] == "High" else ("orange" if row["severity"] == "Medium" else "green")
        rep_popup = f"""
        <div style="font-family: Arial, sans-serif; width: 220px; padding: 4px; color: #0F172A;">
            <b style="color: #DC2626 if '{row['severity']}'=='High' else #D97706;">{row['category']}</b><br/>
            <span style="font-size: 11px; color: #64748B;">Reported: {row['timestamp']}</span>
            <p style="font-size: 12px; margin: 6px 0; color: #334155;"><i>"{row['notes']}"</i></p>
            <b>Severity:</b> {row['severity']} | <b>Confidence:</b> {int(row['confidence']*100)}%
        </div>
        """
        folium.Marker(
            location=[row["lat"], row["lon"]],
            icon=folium.Icon(color=icon_color, icon="info-sign", prefix="glyphicon"),
            tooltip=f"Citizen Report: {row['category']} ({row['severity']})",
            popup=folium.Popup(rep_popup, max_width=260)
        ).add_to(fg_citizens)

    # Add all groups to map
    fg_streams.add_to(m)
    fg_sensors.add_to(m)
    fg_citizens.add_to(m)

    # Add Layer Control
    folium.LayerControl(position="topright", collapsed=False).add_to(m)

    # Render Map
    st_folium(m, width="100%", height=520, returned_objects=[])

    # Visual Map Legend
    st.markdown("""
    <div style="display: flex; gap: 20px; flex-wrap: wrap; background: rgba(18, 23, 33, 0.7); padding: 12px 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.06); font-size: 0.82rem; margin-top: 8px;">
        <div style="display: flex; align-items: center; gap: 6px;">
            <span style="width: 14px; height: 4px; background: #10B981; border-radius: 2px;"></span> Good Ecological Quality
        </div>
        <div style="display: flex; align-items: center; gap: 6px;">
            <span style="width: 14px; height: 4px; background: #F59E0B; border-radius: 2px;"></span> Moderate Stream Stress
        </div>
        <div style="display: flex; align-items: center; gap: 6px;">
            <span style="width: 14px; height: 4px; background: #F43F5E; border-radius: 2px;"></span> Critical / Impaired Reach
        </div>
        <div style="display: flex; align-items: center; gap: 6px;">
            <span style="width: 8px; height: 8px; border-radius: 50%; background: #00F2FE;"></span> IoT Sensor Station
        </div>
        <div style="display: flex; align-items: center; gap: 6px;">
            <span style="width: 8px; height: 8px; border-radius: 50%; background: #EF4444;"></span> Citizen Observation Marker
        </div>
    </div>
    """, unsafe_allow_html=True)
