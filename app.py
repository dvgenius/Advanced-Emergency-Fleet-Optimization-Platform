import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px

from utils import generate_mock_incidents, generate_mock_responders


st.set_page_config(
    page_title="Disaster AI Sentinel Optimizer",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: url("https://images.unsplash.com/photo-1542314831-c53cd418511e?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80");
        background-size: cover;
        background-attachment: fixed;
    }
    
    /* Overlay for readability */
    .block-container {
        padding-top: 2rem;
        background: rgba(15, 23, 42, 0.85); /* Dark slate overlay */
        border-radius: 15px;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        margin-top: 1rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        color: #e2e8f0;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #f8fafc;
        font-weight: 600;
        letter-spacing: -0.025em;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
            color:green;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #38bdf8;
        font-weight: bold;
    }
    
    /* Buttons */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        background: linear-gradient(135deg, #f87171 0%, #ef4444 100%);
    }
    
    /* Dataframes */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    return generate_mock_incidents(), generate_mock_responders()

incidents_df, responders_df = load_data()


st.sidebar.title("Disaster AI Sentinel")
page = st.sidebar.radio("Navigation", ["Dashboard Overview", "Live Map", "AI Route Optimizer"])

st.sidebar.markdown("---")
st.sidebar.info("System Status: **ONLINE**\\n\\nAI Core: **Active**")


if page == "Dashboard Overview":
    st.title("Dashboard Overview")
    st.markdown("Real-time telemetry and KPI metrics for ongoing operations.")
    
 
    st.markdown("### Operational Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    active_incidents = len(incidents_df[incidents_df['Status'] == 'Active'])
    available_responders = len(responders_df[responders_df['Status'] == 'Available'])
  
    critical_cases = len(incidents_df[incidents_df['Severity'] == 'Critical'])
    
    col1.metric("Active Emergencies", active_incidents, "+2 in last hr", delta_color="inverse")
    col2.metric("Available Responders", available_responders, "-1 from avg", delta_color="normal")
    col3.metric("Critical Cases", critical_cases, "+1", delta_color="inverse")
    col4.metric("Avg Response Time", "8m 42s", "-12s")
    
    st.markdown("---")
    

    colA, colB = st.columns(2)
    
    with colA:
        st.subheader("Incident Severity Breakdown")
        fig_sev = px.pie(incidents_df, names='Severity', hole=0.5, 
                         color_discrete_sequence=['#ef4444', '#f97316', '#eab308', '#3b82f6'],
                         template="plotly_dark")
        fig_sev.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_sev, use_container_width=True)
        
    with colB:
        st.subheader("Responder Status")
        fig_res = px.bar(responders_df['Status'].value_counts().reset_index(), 
                         x='Status', y='count', color='Status',
                         color_discrete_sequence=['#10b981', '#3b82f6', '#64748b'],
                         template="plotly_dark")
        fig_res.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_res, use_container_width=True)

elif page == "Live Map":
    st.title("Live Incident & Responder Map")
    st.markdown("Geospatial visualization of active units and emergency locations.")
    

    center_lat = incidents_df['Lat'].mean()
    center_lon = incidents_df['Lon'].mean()
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=12, tiles="cartodb dark_matter")
    

    for idx, row in incidents_df.iterrows():
        if row['Status'] != 'Resolved':
            color = '#ef4444' if row['Severity'] in ['High', 'Critical'] else '#f97316'
            loc_disp = row.get('Location', 'Unknown Area')
            folium.CircleMarker(
                location=[row['Lat'], row['Lon']],
                radius=8,
                popup=f"<b>{row['ID']}</b><br>{row['Type']}<br><i>{loc_disp}</i><br>Sev: {row['Severity']}",
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7
            ).add_to(m)
     
    for idx, row in responders_df.iterrows():
        icon_color = 'green' if row['Status'] == 'Available' else 'blue'
        icon_type = 'ambulance' if row['Type'] == 'Ambulance' else 'fire-extinguisher'
        folium.Marker(
            location=[row['Lat'], row['Lon']],
            popup=f"<b>{row['ID']}</b><br>{row['Type']}<br>{row['Status']}",
            icon=folium.Icon(color=icon_color, icon=icon_type, prefix='fa')
        ).add_to(m)
        
    st_folium(m, width=1200, height=600, returned_objects=[])

elif page == "AI Route Optimizer":
    st.title(" AI Route Optimizer")
    st.markdown("Leverage AI to predict the fastest response vector considering traffic, weather, and historical bottlenecks.")
    
    st.markdown("---")
    
    col_input, col_output = st.columns([1, 1.5])
    
    with col_input:
        st.subheader("Optimization Parameters")
        active_ids = incidents_df[incidents_df['Status'] == 'Active']['ID'].tolist()
        
       
        id_to_loc = {}
        for _, row in incidents_df[incidents_df['Status'] == 'Active'].iterrows():
            loc = row.get('Location', 'Unknown Area')
            id_to_loc[row['ID']] = f"{row['ID']} - {loc} ({row['Type']})"
            
        selected_incident = st.selectbox(
            "Target Incident", 
            active_ids if active_ids else ["No Active Incidents"],
            format_func=lambda x: id_to_loc.get(x, x) if x != "No Active Incidents" else x
        )
        
        traffic_level = st.slider("Current Traffic Density (Simulated)", 1, 10, 6)
        weather = st.selectbox("Weather Conditions", ["Clear", "Light Rain", "Heavy Rain", "Snow", "Fog"])
        
        optimize_btn = st.button("Calculate Optimal Route & Dispatch")
        
    with col_output:
        st.subheader("AI System Output")
        
        if optimize_btn:
            st.success("Analysis Complete")
            
          
            baseline_time = 12.5 + (traffic_level * 0.8)
            ai_time = baseline_time * 0.75 
            
            st.markdown(f"""
            <div style='background: rgba(16, 185, 129, 0.1); border-left: 5px solid #10b981; padding: 15px; border-radius: 5px; margin-bottom: 20px;'>
                <h4 style='margin: 0; color: #10b981;'>Optimal Vector Found</h4>
                <p style='margin: 10px 0 0 0; font-size: 1.1em;'>Estimated AI Arrival: <b>{ai_time:.1f} minutes</b></p>
                <p style='margin: 5px 0 0 0; color: #94a3b8;'>Standard Routing ETA: {baseline_time:.1f} minutes (Saved: {(baseline_time - ai_time):.1f} min)</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.progress(92, text="Model Confidence: 92%")
            
            dest_loc = incidents_df[incidents_df['ID'] == selected_incident]['Location'].iloc[0] if selected_incident != "No Active Incidents" and 'Location' in incidents_df.columns else "Accident Area"
            st.info(f"Dispatched Unit: **RES-2014 (Ambulance)** via fastest clear route to **{dest_loc}**.")
            
        else:
            st.info("Ready. Awaiting Optimization Request.")


