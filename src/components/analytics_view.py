import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def render_analytics_view(df):
    """
    Renders dynamic multi-axis time series charts for water quality trends,
    precipitation events, and pathogen/vector spikes.
    """
    st.markdown("<div class='section-header'>📈 Temporal Trend & Correlation Analytics</div>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🌊 Water Quality & Temp", "🦠 Pathogen & Vector Risk"])
    
    with tab1:
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=df["Date"], y=df["Dissolved_Oxygen_mgL"],
            name="Dissolved Oxygen (mg/L)", line=dict(color="#00F2FE", width=3)
        ))
        fig1.add_trace(go.Scatter(
            x=df["Date"], y=df["Water_Temp_C"],
            name="Water Temp (°C)", line=dict(color="#FF7B00", width=2, dash="dash")
        ))
        fig1.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=df["Date"], y=df["Precipitation_mm"],
            name="Precipitation (mm)", marker_color="rgba(0, 242, 254, 0.3)", yaxis="y2"
        ))
        fig2.add_trace(go.Scatter(
            x=df["Date"], y=df["E_Coli_CFU"],
            name="E. coli (CFU/100mL)", line=dict(color="#F85149", width=3)
        ))
        fig2.add_trace(go.Scatter(
            x=df["Date"], y=df["Mosquito_Vector_Index"],
            name="Mosquito Vector Index", line=dict(color="#D29922", width=2)
        ))
        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(title="Pathogen / Vector Index"),
            yaxis2=dict(title="Precipitation (mm)", overlaying="y", side="right"),
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig2, use_container_width=True)
