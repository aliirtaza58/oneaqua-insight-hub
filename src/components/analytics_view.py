import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def render_analytics_view(df):
    """
    Renders dynamic multi-axis time series charts, threshold danger zones,
    and an environmental correlation matrix.
    """
    st.markdown("<div class='ui-section-title'>📈 Telemetry Trends & Environmental Correlations</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs([
        "🌊 Oxygenation & Temperature",
        "🦠 Pathogen & Runoff Spikes",
        "🔍 Parameter Correlation Matrix"
    ])
    
    with tab1:
        fig1 = go.Figure()
        
        # Danger zone for hypoxia (DO < 5.0 mg/L)
        fig1.add_hrect(
            y0=0, y1=5.0,
            fillcolor="rgba(244, 63, 94, 0.12)", line_width=0,
            annotation_text="Hypoxia Danger Zone (< 5 mg/L)", annotation_position="top left",
            annotation_font=dict(color="#F43F5E", size=10)
        )
        
        fig1.add_trace(go.Scatter(
            x=df["Date"], y=df["Dissolved_Oxygen_mgL"],
            name="Dissolved O₂ (mg/L)",
            line=dict(color="#00F2FE", width=3),
            fill='tozeroy',
            fillcolor='rgba(0, 242, 254, 0.05)'
        ))
        
        fig1.add_trace(go.Scatter(
            x=df["Date"], y=df["Water_Temp_C"],
            name="Water Temp (°C)",
            line=dict(color="#F59E0B", width=2, dash="dash"),
            yaxis="y2"
        ))
        
        fig1.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(18, 23, 33, 0.5)",
            font=dict(family="Plus Jakarta Sans", color="#F0F6FC"),
            yaxis=dict(title="Dissolved Oxygen (mg/L)", gridcolor="rgba(255,255,255,0.06)"),
            yaxis2=dict(title="Water Temp (°C)", overlaying="y", side="right", gridcolor="transparent"),
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        fig2 = go.Figure()
        
        # Rainfall bar
        fig2.add_trace(go.Bar(
            x=df["Date"], y=df["Precipitation_mm"],
            name="Rainfall (mm)",
            marker_color="rgba(79, 172, 254, 0.35)",
            yaxis="y2"
        ))
        
        # Unsafe pathogen threshold
        fig2.add_hline(
            y=400, line_dash="dot", line_color="#F43F5E", line_width=1.5,
            annotation_text="Public Contact Warning (400 CFU)",
            annotation_font=dict(color="#F43F5E", size=10)
        )
        
        # E. coli line
        fig2.add_trace(go.Scatter(
            x=df["Date"], y=df["E_Coli_CFU"],
            name="E. coli (CFU/100mL)",
            line=dict(color="#F43F5E", width=3)
        ))
        
        # Vector line
        fig2.add_trace(go.Scatter(
            x=df["Date"], y=df["Mosquito_Vector_Index"],
            name="Mosquito Vector Index",
            line=dict(color="#F59E0B", width=2)
        ))
        
        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(18, 23, 33, 0.5)",
            font=dict(family="Plus Jakarta Sans", color="#F0F6FC"),
            yaxis=dict(title="Microbial / Vector Count", gridcolor="rgba(255,255,255,0.06)"),
            yaxis2=dict(title="Precipitation (mm)", overlaying="y", side="right", gridcolor="transparent"),
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        corr_cols = ["Dissolved_Oxygen_mgL", "Water_Temp_C", "Precipitation_mm", "E_Coli_CFU", "Mosquito_Vector_Index"]
        corr_matrix = df[corr_cols].corr().round(2)
        
        fig3 = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            color_continuous_scale="Blues",
            title="Pearson Correlation Across Environmental Stressors"
        )
        fig3.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(18, 23, 33, 0.5)",
            font=dict(family="Plus Jakarta Sans", color="#F0F6FC"),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.caption("💡 Key Observation: Inverse correlation between water temperature and dissolved oxygen, and strong positive correlation between heavy rainfall events and microbial E. coli spikes.")
