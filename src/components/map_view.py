import folium
from streamlit_folium import st_folium
import streamlit as st

def render_map_view(city_data, segments, sensors_df, reports_df):
    """
    Renders an interactive Folium geospatial map with stream polylines,
    sensor nodes, and citizen reports.
    """
    coords = city_data["coords"]
    zoom = city_data["zoom"]
    
    # Initialize Folium Map with CartoDB Dark Matter tile theme
    m = folium.Map(
        location=coords,
        zoom_start=zoom,
        tiles="CartoDB dark_matter"
    )
    
    # Add Stream Segments (Polylines)
    for seg in segments:
        popup_html = f"""
        <div style="font-family: Arial, sans-serif; width: 220px; color: #333;">
            <h4 style="margin:0 0 6px 0; color: {seg['color']};">{seg['name']}</h4>
            <b>Status:</b> {seg['status']}<br/>
            <b>Dissolved Oxygen:</b> {seg['do_mg_l']} mg/L<br/>
            <b>Macroinvertebrate Index:</b> {seg['macro_index']}/10<br/>
            <b>E. coli:</b> {seg['e_coli']} CFU/100mL<br/>
            <b>Vector Density:</b> {seg['vector_density']}/100
        </div>
        """
        folium.PolyLine(
            locations=seg["coords"],
            color=seg["color"],
            weight=6,
            opacity=0.85,
            tooltip=f"{seg['name']} ({seg['status']})",
            popup=folium.Popup(popup_html, max_width=260)
        ).add_to(m)

    # Add IoT Sensor Nodes
    for _, row in sensors_df.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["lon"]],
            radius=7,
            color="#00F2FE",
            fill=True,
            fill_color="#00F2FE",
            fill_opacity=0.9,
            tooltip=f"Sensor Node: {row['name']} ({row['node_id']})",
            popup=f"<b>{row['name']}</b><br/>Battery: {row['battery']}%"
        ).add_to(m)

    # Add Citizen Observation Reports
    for _, row in reports_df.iterrows():
        icon_color = "red" if row["severity"] == "High" else ("orange" if row["severity"] == "Medium" else "green")
        folium.Marker(
            location=[row["lat"], row["lon"]],
            icon=folium.Icon(color=icon_color, icon="info-sign"),
            tooltip=f"Citizen Report: {row['category']}",
            popup=f"<b>{row['category']}</b><br/>Confidence: {int(row['confidence']*100)}%<br/><i>{row['notes']}</i>"
        ).add_to(m)

    # Render map in Streamlit container
    st_folium(m, width="100%", height=500, returned_objects=[])
