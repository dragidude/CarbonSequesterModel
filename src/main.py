"""
Main Streamlit application for the Johnny Algae Sea Carbon Sequestration Model.
Provides an interactive interface for parameter tweaking and scenario analysis.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from typing import Dict, List

# Import our model
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.algae_model import (
    AlgaeCarbonSequestrationModel, 
    AlgaeStrain, 
    EnvironmentalConditions, 
    OperationalParameters,
    create_sample_strains,
    create_sample_environments
)


def main():
    st.set_page_config(
        page_title="Johnny Algae Sea - Carbon Sequestration Model",
        page_icon="🌊",
        layout="wide"
    )
    
    # Custom CSS for ocean theme
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #87CEEB 0%, #4682B4 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }
    .main-header h1 {
        color: white;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    .slogan {
        font-size: 1.5rem;
        font-style: italic;
        margin-bottom: 1rem;
    }
    .stMetric {
        background: linear-gradient(135deg, #E0F6FF 0%, #F0F8FF 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #20B2AA;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #F0F8FF 0%, #E0F6FF 100%);
        border-radius: 8px 8px 0px 0px;
        border: 2px solid #E0F6FF;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #20B2AA 0%, #48D1CC 100%);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header with Johnny Algae Sea branding
    st.markdown("""
    <div class="main-header">
        <h1>🌊 Johnny Algae Sea</h1>
        <div class="slogan">Carbon Sequestration Model</div>
        <div style="font-size: 1.2rem; font-weight: bold;">Spray. Grow. Sink Carbon.</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    This interactive model calculates the viability of genetically modified algae/cyanobacteria 
    for ocean carbon sequestration. Adjust parameters below to explore different scenarios with Johnny Algae Sea.
    """)
    
    # Sidebar for parameter controls
    with st.sidebar:
        st.header("📊 Model Parameters")
        
        # Strain selection
        st.subheader("🌱 Algae Strain")
        strain_name = st.selectbox(
            "Select Strain Type",
            ["Custom", "Fast-growing Cyanobacteria", "GM Diatom Variant", "Conservative GM Algae"]
        )
        
        if strain_name == "Custom":
            col1, col2 = st.columns(2)
            with col1:
                carbon_content = st.slider(
                    "Carbon Content (%)", 
                    30.0, 60.0, 45.0, 0.5,
                    help="The percentage of the algae's dry weight that is pure carbon. Higher carbon content means more carbon is stored per kilogram of algae biomass."
                )
                doubling_time = st.slider(
                    "Doubling Time (hours)", 
                    6.0, 72.0, 24.0, 1.0,
                    help="How long it takes for the algae population to double in size. Faster doubling (fewer hours) means the algae grow and multiply more quickly, capturing more carbon."
                )
                photosynthetic_efficiency = st.slider(
                    "Photosynthetic Efficiency", 
                    0.5, 1.0, 0.8, 0.05,
                    help="How efficiently the algae convert sunlight into carbon biomass. Higher efficiency means more carbon captured per unit of light."
                )
            
            with col2:
                sinking_rate = st.slider(
                    "Sinking Rate (m/day)", 
                    10.0, 200.0, 50.0, 5.0,
                    help="How fast the algae sink to the deep ocean. Faster sinking means less time for decomposition near the surface, leading to more permanent carbon storage."
                )
                export_fraction = st.slider(
                    "Export Fraction", 
                    0.1, 0.8, 0.4, 0.05,
                    help="The percentage of algae that actually sink to the deep ocean instead of being eaten or decomposed near the surface. Only the sinking algae permanently remove carbon from the atmosphere."
                )
                r_and_d_cost = st.slider(
                    "R&D Cost (millions $)", 
                    5.0, 50.0, 15.0, 1.0,
                    help="The research and development costs to develop this specific algae strain, amortized over 10 years."
                )
            
            temp_min, temp_max = st.slider(
                "Temperature Range (°C)", 
                10.0, 40.0, (20.0, 30.0),
                help="The optimal temperature range for this algae strain. Temperatures outside this range will reduce growth."
            )
            salinity_min, salinity_max = st.slider(
                "Salinity Range (ppt)", 
                20.0, 45.0, (30.0, 40.0),
                help="The optimal salinity range for this algae strain. Salinity outside this range will reduce growth."
            )
            
            strain = AlgaeStrain(
                name="Custom Strain",
                carbon_content_percent=carbon_content,
                doubling_time_hours=doubling_time,
                photosynthetic_efficiency=photosynthetic_efficiency,
                sinking_rate_m_per_day=sinking_rate,
                export_fraction=export_fraction,
                optimal_temperature_range=(temp_min, temp_max),
                optimal_salinity_range=(salinity_min, salinity_max),
                genetic_kill_switch=True,
                r_and_d_cost_millions=r_and_d_cost
            )
        else:
            strains = create_sample_strains()
            strain_map = {
                "Fast-growing Cyanobacteria": "fast_growing_cyanobacteria",
                "GM Diatom Variant": "diatom_variant", 
                "Conservative GM Algae": "conservative_strain"
            }
            strain = strains[strain_map[strain_name]]
        
        # Environment selection
        st.subheader("🌊 Environmental Conditions")
        env_name = st.selectbox(
            "Select Environment",
            ["Custom", "Tropical Ocean", "Temperate Ocean", "Nutrient Rich"]
        )
        
        if env_name == "Custom":
            euphotic_depth = st.slider(
                "Euphotic Depth (m)", 
                20.0, 150.0, 80.0, 5.0,
                help="The depth of water where sunlight can penetrate for photosynthesis. Deeper euphotic zones mean more space for algae to grow and more light available."
            )
            surface_temp = st.slider(
                "Surface Temperature (°C)", 
                5.0, 35.0, 25.0, 0.5,
                help="The water temperature at the ocean surface. Algae have optimal temperature ranges - too hot or too cold and they won't grow well."
            )
            salinity = st.slider(
                "Salinity (ppt)", 
                25.0, 40.0, 35.0, 0.5,
                help="The saltiness of the ocean water (parts per thousand). Different algae strains prefer different salinity levels for optimal growth."
            )
            
            col1, col2 = st.columns(2)
            with col1:
                nitrogen = st.slider(
                    "Nitrogen (μmol/L)", 
                    0.5, 15.0, 5.0, 0.1,
                    help="The concentration of nitrogen nutrients in the water. Nitrogen is essential for algae growth - too little limits growth."
                )
                phosphorus = st.slider(
                    "Phosphorus (μmol/L)", 
                    0.1, 1.5, 0.4, 0.05,
                    help="The concentration of phosphorus nutrients in the water. Phosphorus is essential for algae growth - too little limits growth."
                )
            
            with col2:
                iron = st.slider(
                    "Iron (nmol/L)", 
                    0.01, 0.3, 0.08, 0.01,
                    help="The concentration of iron in the water. Iron is a micronutrient that can limit algae growth in some ocean regions."
                )
                mixing_depth = st.slider(
                    "Mixing Depth (m)", 
                    30.0, 200.0, 75.0, 5.0,
                    help="The depth of the surface mixed layer where algae can grow. Deeper mixing provides more space for algae but may dilute nutrients."
                )
            
            sequestration_depth = st.slider(
                "Sequestration Depth (m)", 
                500.0, 3000.0, 1000.0, 100.0,
                help="The depth required for permanent carbon sequestration. Carbon that reaches this depth is considered permanently removed from the atmosphere."
            )
            
            environment = EnvironmentalConditions(
                euphotic_depth_m=euphotic_depth,
                surface_temperature_celsius=surface_temp,
                salinity_ppt=salinity,
                nutrient_nitrogen_umol_per_l=nitrogen,
                nutrient_phosphorus_umol_per_l=phosphorus,
                nutrient_iron_nmol_per_l=iron,
                mixing_depth_m=mixing_depth,
                current_speed_m_per_s=0.15,
                sequestration_depth_m=sequestration_depth
            )
        else:
            environments = create_sample_environments()
            env_map = {
                "Tropical Ocean": "tropical_ocean",
                "Temperate Ocean": "temperate_ocean",
                "Nutrient Rich": "nutrient_rich"
            }
            environment = environments[env_map[env_name]]
        
        # Operational parameters
        st.subheader("💰 Operational Parameters")
        area_km2 = st.slider(
            "Area (km²)", 
            100.0, 10000.0, 1000.0, 100.0,
            help="The total ocean area where the algae will be deployed. Larger areas can sequester more carbon but require more resources to manage."
        )
        application_freq = st.slider(
            "Applications per Year", 
            1.0, 12.0, 4.0, 1.0,
            help="How many times per year the algae need to be deployed. More frequent applications may be needed in some environments."
        )
        
        col1, col2 = st.columns(2)
        with col1:
            cultivation_cost = st.slider(
                "Cultivation Cost ($/kg)", 
                0.1, 2.0, 0.5, 0.1,
                help="How much it costs to grow and prepare one kilogram of algae biomass for deployment. This includes cultivation, processing, and preparation costs."
            )
            delivery_cost = st.slider(
                "Delivery Cost ($/kg)", 
                0.1, 1.0, 0.3, 0.1,
                help="The cost to transport and deploy one kilogram of algae to the target ocean area. Includes fuel, vessel time, and deployment equipment."
            )
        
        with col2:
            vessel_cost = st.slider(
                "Vessel Cost ($/day)", 
                1000.0, 20000.0, 5000.0, 500.0,
                help="The daily operating cost of the ships needed to deploy and monitor the algae. Includes crew, fuel, maintenance, and vessel rental."
            )
            monitoring_cost = st.slider(
                "Monitoring Cost ($/year)", 
                50000.0, 500000.0, 100000.0, 10000.0,
                help="Annual costs for monitoring the algae deployment, including scientific measurements, environmental impact assessment, and compliance reporting."
            )
        
        regulatory_cost = st.slider(
            "Regulatory Cost ($/year)", 
            25000.0, 250000.0, 50000.0, 5000.0,
            help="Annual costs for regulatory compliance, including permits, environmental assessments, and legal requirements."
        )
        
        operations = OperationalParameters(
            area_km2=area_km2,
            application_frequency_per_year=application_freq,
            cultivation_cost_per_kg=cultivation_cost,
            delivery_cost_per_kg=delivery_cost,
            vessel_cost_per_day=vessel_cost,
            monitoring_cost_per_year=monitoring_cost,
            regulatory_cost_per_year=regulatory_cost
        )
    
    # Create model and calculate results
    model = AlgaeCarbonSequestrationModel(strain, environment, operations)
    metrics = model.calculate_viability_metrics()
    costs = model.calculate_operational_costs()
    
    # Main results display
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "🌊 CO₂ Removed",
            f"{metrics['co2_removed_tonnes_per_year']:.1f} tonnes/year",
            f"{metrics['co2_removed_tonnes_per_year']/1000:.1f}k tonnes/year"
        )
    
    with col2:
        st.metric(
            "💵 Cost per Tonne CO₂",
            f"${metrics['cost_per_tonne_co2']:.2f}/t CO₂",
            f"{'Competitive' if metrics['cost_per_tonne_co2'] < 100 else 'Expensive'}"
        )
    
    with col3:
        st.metric(
            "🎯 Viability Score",
            f"{metrics['viability_score']:.2f}/1.00",
            f"{'High' if metrics['viability_score'] > 0.7 else 'Medium' if metrics['viability_score'] > 0.4 else 'Low'}"
        )
    
    # Detailed results tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Results", "💰 Costs", "🔬 Biology", "📊 Analysis"])
    
    with tab1:
        st.subheader("📊 Detailed Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🌱 Carbon Sequestration Metrics:**")
            st.write(f"- Carbon Sequestered: {metrics['carbon_sequestered_kg_per_year']:,.0f} kg C/year")
            st.write(f"- Biomass Required: {metrics['biomass_required_kg_per_year']:,.0f} kg/year")
            st.write(f"- NPP: {metrics['npp_g_c_per_m2_per_year']:.1f} g C/m²/year")
            st.write(f"- Growth Rate: {metrics['growth_rate_per_day']:.3f} per day")
        
        with col2:
            st.write("**🎯 Viability Assessment:**")
            st.write(f"- Cost Competitiveness: {metrics['cost_competitiveness']:.2f}x target")
            st.write(f"- Scale Adequacy: {metrics['scale_adequacy']:.2f}x target")
            st.write(f"- Total Annual Cost: ${metrics['total_cost_per_year']:,.0f}")
    
    with tab2:
        st.subheader("💰 Cost Breakdown")
        
        # Cost breakdown pie chart
        cost_data = {
            'Cultivation': costs['cultivation'],
            'Delivery': costs['delivery'],
            'Vessel Operations': costs['vessel'],
            'Monitoring': costs['monitoring'],
            'Regulatory': costs['regulatory'],
            'R&D (amortized)': costs['r_and_d']
        }
        
        fig = px.pie(
            values=list(cost_data.values()),
            names=list(cost_data.keys()),
            title="Annual Cost Breakdown",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Cost details table
        cost_df = pd.DataFrame([
            {"Category": k, "Cost ($/year)": f"${v:,.0f}", "Percentage": f"{v/costs['total']*100:.1f}%"}
            for k, v in cost_data.items()
        ])
        st.dataframe(cost_df, use_container_width=True)
    
    with tab3:
        st.subheader("🔬 Biological Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🌱 Strain Characteristics:**")
            st.write(f"- Name: {strain.name}")
            st.write(f"- Carbon Content: {strain.carbon_content_percent:.1f}%")
            st.write(f"- Doubling Time: {strain.doubling_time_hours:.1f} hours")
            st.write(f"- Export Fraction: {strain.export_fraction:.1%}")
            st.write(f"- Sinking Rate: {strain.sinking_rate_m_per_day:.1f} m/day")
            st.write(f"- Genetic Kill Switch: {'Yes' if strain.genetic_kill_switch else 'No'}")
        
        with col2:
            st.write("**🌊 Environmental Conditions:**")
            st.write(f"- Euphotic Depth: {environment.euphotic_depth_m:.0f} m")
            st.write(f"- Surface Temperature: {environment.surface_temperature_celsius:.1f}°C")
            st.write(f"- Salinity: {environment.salinity_ppt:.1f} ppt")
            st.write(f"- Nitrogen: {environment.nutrient_nitrogen_umol_per_l:.1f} μmol/L")
            st.write(f"- Phosphorus: {environment.nutrient_phosphorus_umol_per_l:.2f} μmol/L")
            st.write(f"- Iron: {environment.nutrient_iron_nmol_per_l:.2f} nmol/L")
    
    with tab4:
        st.subheader("📊 Sensitivity Analysis")
        
        # Parameter sensitivity analysis
        base_metrics = metrics.copy()
        
        # Test different areas
        areas = [100, 500, 1000, 5000, 10000]
        co2_results = []
        cost_results = []
        
        for area in areas:
            test_ops = OperationalParameters(
                area_km2=area,
                application_frequency_per_year=operations.application_frequency_per_year,
                cultivation_cost_per_kg=operations.cultivation_cost_per_kg,
                delivery_cost_per_kg=operations.delivery_cost_per_kg,
                vessel_cost_per_day=operations.vessel_cost_per_day,
                monitoring_cost_per_year=operations.monitoring_cost_per_year,
                regulatory_cost_per_year=operations.regulatory_cost_per_year
            )
            test_model = AlgaeCarbonSequestrationModel(strain, environment, test_ops)
            test_metrics = test_model.calculate_viability_metrics()
            co2_results.append(test_metrics['co2_removed_tonnes_per_year'])
            cost_results.append(test_metrics['cost_per_tonne_co2'])
        
        # Create sensitivity plot
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("CO₂ Removal vs Area", "Cost per Tonne vs Area")
        )
        
        fig.add_trace(
            go.Scatter(x=areas, y=co2_results, mode='lines+markers', name='CO₂ Removed'),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=areas, y=cost_results, mode='lines+markers', name='Cost per Tonne'),
            row=1, col=2
        )
        
        fig.update_xaxes(title_text="Area (km²)", row=1, col=1)
        fig.update_xaxes(title_text="Area (km²)", row=1, col=2)
        fig.update_yaxes(title_text="CO₂ Removed (tonnes/year)", row=1, col=1)
        fig.update_yaxes(title_text="Cost ($/t CO₂)", row=1, col=2)
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Download results
    st.subheader("📥 Download Results")
    
    # Create results dataframe
    results_data = {
        "Metric": [
            "CO₂ Removed (tonnes/year)",
            "Cost per Tonne CO₂ ($/t)",
            "Total Annual Cost ($)",
            "Biomass Required (kg/year)",
            "Carbon Sequestered (kg/year)",
            "NPP (g C/m²/year)",
            "Growth Rate (per day)",
            "Viability Score",
            "Cost Competitiveness",
            "Scale Adequacy"
        ],
        "Value": [
            metrics['co2_removed_tonnes_per_year'],
            metrics['cost_per_tonne_co2'],
            metrics['total_cost_per_year'],
            metrics['biomass_required_kg_per_year'],
            metrics['carbon_sequestered_kg_per_year'],
            metrics['npp_g_c_per_m2_per_year'],
            metrics['growth_rate_per_day'],
            metrics['viability_score'],
            metrics['cost_competitiveness'],
            metrics['scale_adequacy']
        ]
    }
    
    results_df = pd.DataFrame(results_data)
    
    csv = results_df.to_csv(index=False)
    st.download_button(
        label="Download Results as CSV",
        data=csv,
        file_name="johnny_algae_sea_results.csv",
        mime="text/csv"
    )
    
    # Show full report
    with st.expander("📋 Full Model Report"):
        st.text(model.generate_report())


if __name__ == "__main__":
    main() 