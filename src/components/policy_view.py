import streamlit as st
from src.engine import generate_ai_executive_summary

def render_policy_view(city_name, indices):
    """
    Renders AI-generated executive summaries and provides a download button
    for the One Health Policy Brief.
    """
    st.markdown("<div class='section-header'>One Health Executive Advisory Brief</div>", unsafe_allow_html=True)
    
    summary_md = generate_ai_executive_summary(city_name, indices)
    
    st.markdown(summary_md)
    
    st.write("")
    st.download_button(
        label="Export Policy Brief (.md)",
        data=summary_md,
        file_name=f"OneAqua_Policy_Brief_{city_name}.md",
        mime="text/markdown"
    )
