# Algae Carbon Sequestration Model Documentation

## Overview

This model calculates the viability of genetically modified algae/cyanobacteria for ocean carbon sequestration. It incorporates biological, environmental, and economic parameters to provide comprehensive viability assessments.

## Model Components

### 1. Biological Parameters (AlgaeStrain)

#### Carbon Content (% dry weight)
- **Range**: 30-60%
- **Typical Values**: 40-52%
- **Impact**: Higher carbon content means more carbon sequestered per unit biomass

#### Doubling Time (hours)
- **Range**: 6-72 hours
- **Typical Values**: 12-48 hours
- **Impact**: Faster doubling time = higher growth rate = more carbon sequestration

#### Photosynthetic Efficiency
- **Range**: 0.5-1.0
- **Typical Values**: 0.7-0.9
- **Impact**: Higher efficiency = more carbon fixed per unit light

#### Sinking Rate (m/day)
- **Range**: 10-200 m/day
- **Typical Values**: 25-100 m/day
- **Impact**: Faster sinking = less remineralization = more permanent sequestration

#### Export Fraction (%)
- **Range**: 10-80%
- **Typical Values**: 30-60%
- **Impact**: Higher export = more carbon reaching sequestration depth

#### Optimal Temperature Range (°C)
- **Range**: 10-40°C
- **Typical Values**: 15-30°C
- **Impact**: Determines environmental suitability

#### Optimal Salinity Range (ppt)
- **Range**: 20-45 ppt
- **Typical Values**: 25-40 ppt
- **Impact**: Determines environmental suitability

### 2. Environmental Parameters (EnvironmentalConditions)

#### Euphotic Depth (m)
- **Range**: 20-150 m
- **Typical Values**: 40-100 m
- **Impact**: Determines light availability for photosynthesis

#### Surface Temperature (°C)
- **Range**: 5-35°C
- **Impact**: Affects growth rate and metabolic activity

#### Salinity (ppt)
- **Range**: 25-40 ppt
- **Impact**: Affects osmotic balance and growth

#### Nutrient Concentrations
- **Nitrogen (μmol/L)**: 0.5-15.0
- **Phosphorus (μmol/L)**: 0.1-1.5
- **Iron (nmol/L)**: 0.01-0.3
- **Impact**: Limiting factors for growth (Liebig's law of minimum)

#### Mixing Depth (m)
- **Range**: 30-200 m
- **Impact**: Determines volume available for growth

#### Sequestration Depth (m)
- **Range**: 500-3000 m
- **Typical Values**: 1000-1500 m
- **Impact**: Depth required for permanent sequestration

### 3. Operational Parameters (OperationalParameters)

#### Area (km²)
- **Range**: 100-10,000 km²
- **Impact**: Scale of operation

#### Application Frequency (per year)
- **Range**: 1-12 applications/year
- **Impact**: Operational complexity and costs

#### Cost Parameters
- **Cultivation Cost ($/kg)**: 0.1-2.0
- **Delivery Cost ($/kg)**: 0.1-1.0
- **Vessel Cost ($/day)**: 1,000-20,000
- **Monitoring Cost ($/year)**: 50,000-500,000
- **Regulatory Cost ($/year)**: 25,000-250,000

## Calculations

### 1. Growth Rate Calculation

```python
# Base growth rate from doubling time
base_growth_rate = ln(2) / (doubling_time_hours / 24)

# Environmental limitations
temp_factor = temperature_response_function()
light_factor = light_limitation_function()
nutrient_factor = nutrient_limitation_function()
salinity_factor = salinity_response_function()

effective_growth_rate = base_growth_rate * temp_factor * light_factor * nutrient_factor * salinity_factor
```

### 2. Net Primary Productivity (NPP)

```python
npp = effective_growth_rate * biomass_density * mixed_layer_depth * days_per_year
```

### 3. Carbon Export

```python
export_carbon = npp * export_fraction
sinking_time = sequestration_depth / sinking_rate
survival_fraction = exp(-remineralization_rate * sinking_time)
carbon_export = export_carbon * survival_fraction
```

### 4. Cost Calculations

```python
biomass_required = calculate_biomass_needed()
cultivation_cost = biomass_required * cultivation_cost_per_kg
delivery_cost = biomass_required * delivery_cost_per_kg
vessel_cost = vessel_cost_per_day * 365
total_cost = cultivation_cost + delivery_cost + vessel_cost + monitoring_cost + regulatory_cost
cost_per_tonne = total_cost / co2_removed
```

### 5. Viability Score

```python
cost_score = max(0, 1 - (cost_per_tonne - 50) / 200)
scale_score = min(1, co2_removed / 10000)
safety_score = 1.0 if genetic_kill_switch else 0.5
viability_score = cost_score * 0.4 + scale_score * 0.4 + safety_score * 0.2
```

## Sample Scenarios

### Fast-growing Cyanobacteria in Tropical Ocean
- **Strain**: 12-hour doubling time, 45% carbon content, 50 m/day sinking
- **Environment**: 80m euphotic depth, 28°C, 35 ppt salinity
- **Results**: ~2,500 tonnes CO₂/year, $85/t CO₂

### GM Diatom Variant in Temperate Ocean
- **Strain**: 24-hour doubling time, 52% carbon content, 100 m/day sinking
- **Environment**: 60m euphotic depth, 15°C, 33 ppt salinity
- **Results**: ~1,800 tonnes CO₂/year, $120/t CO₂

### Conservative GM Algae in Nutrient-rich Environment
- **Strain**: 48-hour doubling time, 40% carbon content, 25 m/day sinking
- **Environment**: 40m euphotic depth, 20°C, 34 ppt salinity, high nutrients
- **Results**: ~3,200 tonnes CO₂/year, $75/t CO₂

## Key Assumptions

1. **Remineralization Rate**: 10% per day during sinking
2. **Biomass Density**: 1 g C/m³ in mixed layer
3. **Target NPP**: 125 g C/m²/year (typical ocean NPP)
4. **Carbon to CO₂ Ratio**: 3.67 g CO₂ per g C
5. **R&D Amortization**: 10 years
6. **Genetic Kill Switch**: Assumed present for safety

## Limitations

1. **Simplified Environmental Models**: Temperature, light, and nutrient responses are simplified
2. **Constant Parameters**: Some parameters (like remineralization rate) are assumed constant
3. **No Competition**: Doesn't model competition with native species
4. **No Ecological Impact**: Doesn't assess broader ecological effects
5. **No Seasonal Variation**: Assumes constant conditions

## Future Improvements

1. **Dynamic Environmental Models**: Include seasonal and spatial variability
2. **Competition Models**: Model interactions with native species
3. **Ecological Impact Assessment**: Include broader ecosystem effects
4. **Genetic Stability**: Model genetic drift and mutation rates
5. **Regulatory Scenarios**: Include different regulatory frameworks
6. **Technology Learning**: Include cost reductions over time

## Usage Examples

### Python Model
```python
from src.models.algae_model import *

# Create strain
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

# Create environment
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

# Create operations
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
```

### Streamlit App
```bash
streamlit run src/main.py
```

### HTML Calculator
Open `algae_cdr_calculator.html` in any web browser for quick parameter tweaking. 