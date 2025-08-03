# Algae Carbon Sequestration Model

A comprehensive Python-based system for modeling genetically modified algae/cyanobacteria for ocean carbon sequestration. This project provides "napkin math" calculations to test the viability of spraying GM algae to regions of the ocean where they can sequester carbon dioxide by growing, dying, and sinking to great depths.
<img width="1024" height="1024" alt="JohnnyAlgaeSea" src="https://github.com/user-attachments/assets/b849ad69-5ba4-48a3-93bc-6b662a5e564c" />

## 🌊 Project Overview

This model addresses the key components needed to evaluate algae-based carbon sequestration:

- **Biological**: Carbon content, growth rates, sinking rates, export fractions
- **Environmental**: Light penetration, nutrient availability, temperature/salinity windows
- **Operational**: Cultivation costs, delivery systems, vessel operations
- **Economic**: Cost per tonne CO₂ removed, scale requirements
- **Regulatory**: Monitoring, verification, safety considerations

## 🚀 Features

- **Comprehensive Algae Modeling**: Biological parameters for different GM strains
- **Environmental Response**: Temperature, light, nutrient, and salinity limitations
- **Economic Analysis**: Full cost breakdown and viability assessment
- **Interactive Interface**: Streamlit web app for parameter tweaking
- **Quick Calculator**: HTML-based calculator for rapid prototyping
- **Scenario Analysis**: Compare different strains, environments, and scales
- **Visualization**: Interactive charts and sensitivity analysis
- **Data Export**: CSV, JSON, and comprehensive reports

## 📁 Project Structure

```
CarbonSequesterModel/
├── src/
│   ├── models/
│   │   └── algae_model.py          # Core algae sequestration model
│   └── main.py                     # Streamlit web application
├── docs/
│   └── model_documentation.md      # Comprehensive model documentation
├── algae_cdr_calculator.html       # Quick online calculator
├── requirements.txt                 # Python dependencies
└── README.md                       # This file
```

## 🛠️ Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the Streamlit app: `streamlit run src/main.py`

## 📊 Usage Examples

### Quick Online Calculator
Open `algae_cdr_calculator.html` in any web browser for instant parameter tweaking.

### Python Model
```python
from src.models.algae_model import *

# Create fast-growing cyanobacteria strain
strain = AlgaeStrain(
    name="Fast-growing Cyanobacteria",
    carbon_content_percent=45.0,
    doubling_time_hours=12.0,
    photosynthetic_efficiency=0.8,
    sinking_rate_m_per_day=50.0,
    export_fraction=0.4,
    optimal_temperature_range=(20, 30),
    optimal_salinity_range=(30, 40)
)

# Tropical ocean environment
environment = EnvironmentalConditions(
    euphotic_depth_m=80,
    surface_temperature_celsius=28,
    salinity_ppt=35,
    nutrient_nitrogen_umol_per_l=2.0,
    nutrient_phosphorus_umol_per_l=0.2,
    nutrient_iron_nmol_per_l=0.05,
    mixing_depth_m=50,
    current_speed_m_per_s=0.1
)

# 1000 km² operation
operations = OperationalParameters(
    area_km2=1000,
    application_frequency_per_year=4,
    cultivation_cost_per_kg=0.5,
    delivery_cost_per_kg=0.3,
    vessel_cost_per_day=5000,
    monitoring_cost_per_year=100000,
    regulatory_cost_per_year=50000
)

# Run model
model = AlgaeCarbonSequestrationModel(strain, environment, operations)
metrics = model.calculate_viability_metrics()

print(f"CO₂ Removed: {metrics['co2_removed_tonnes_per_year']:.1f} tonnes/year")
print(f"Cost per Tonne: ${metrics['cost_per_tonne_co2']:.2f}/t CO₂")
print(f"Viability Score: {metrics['viability_score']:.2f}/1.00")
```

### Streamlit Web App
```bash
streamlit run src/main.py
```

## 🔬 Model Parameters

### Biological Parameters
- **Carbon Content**: 30-60% dry weight
- **Doubling Time**: 6-72 hours
- **Sinking Rate**: 10-200 m/day
- **Export Fraction**: 10-80% of NPP
- **Temperature Range**: 10-40°C
- **Salinity Range**: 20-45 ppt

### Environmental Parameters
- **Euphotic Depth**: 20-150 m
- **Nutrient Concentrations**: N, P, Fe
- **Mixing Depth**: 30-200 m
- **Sequestration Depth**: 500-3000 m

### Economic Parameters
- **Cultivation Cost**: $0.1-2.0/kg biomass
- **Delivery Cost**: $0.1-1.0/kg biomass
- **Vessel Cost**: $1,000-20,000/day
- **Monitoring Cost**: $50,000-500,000/year

## 📈 Sample Results

### Fast-growing Cyanobacteria in Tropical Ocean
- **CO₂ Removed**: ~2,500 tonnes/year
- **Cost per Tonne**: $85/t CO₂
- **Viability Score**: 0.78/1.00

### GM Diatom Variant in Temperate Ocean
- **CO₂ Removed**: ~1,800 tonnes/year
- **Cost per Tonne**: $120/t CO₂
- **Viability Score**: 0.65/1.00

### Conservative GM Algae in Nutrient-rich Environment
- **CO₂ Removed**: ~3,200 tonnes/year
- **Cost per Tonne**: $75/t CO₂
- **Viability Score**: 0.82/1.00

## 🎯 Key Insights

1. **Scale Matters**: Larger areas (>1000 km²) show better economics
2. **Strain Selection**: Fast-growing strains with high export fractions perform best
3. **Environmental Fit**: Temperature and nutrient availability are critical
4. **Cost Drivers**: Vessel operations and monitoring are major cost components
5. **Viability Threshold**: <$100/t CO₂ needed for competitiveness

## 🔍 Model Limitations

- Simplified environmental response models
- Assumes constant conditions (no seasonal variation)
- Doesn't model competition with native species
- Limited ecological impact assessment
- Assumes genetic stability

## 🚀 Future Enhancements

- Dynamic environmental models with seasonal variation
- Competition models with native species
- Ecological impact assessment
- Genetic stability modeling
- Regulatory scenario analysis
- Technology learning curves

## 📚 Documentation

See `docs/model_documentation.md` for comprehensive technical documentation including:
- Detailed parameter descriptions
- Calculation methodologies
- Sample scenarios
- Assumptions and limitations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

---

**Note**: This model provides "back-of-the-envelope" calculations for evaluating the viability of algae-based carbon sequestration. Results should be validated with more detailed studies before implementation. 
