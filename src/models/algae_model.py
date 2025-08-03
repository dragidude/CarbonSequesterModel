"""
Algae Carbon Sequestration Model

This module models genetically modified algae/cyanobacteria for ocean carbon sequestration.
Based on biological, environmental, and economic parameters to calculate viability.
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import matplotlib.pyplot as plt
import seaborn as sns


@dataclass
class AlgaeStrain:
    """Represents a specific algae/cyanobacteria strain with its properties."""
    name: str
    carbon_content_percent: float  # % dry weight
    doubling_time_hours: float
    photosynthetic_efficiency: float  # g C fixed per mol photons
    sinking_rate_m_per_day: float
    export_fraction: float  # % of POC exported below thermocline
    optimal_temperature_range: Tuple[float, float]  # (min, max) in Celsius
    optimal_salinity_range: Tuple[float, float]  # (min, max) in ppt
    genetic_kill_switch: bool = True
    r_and_d_cost_millions: float = 10.0


@dataclass
class EnvironmentalConditions:
    """Environmental parameters affecting algae growth and sequestration."""
    euphotic_depth_m: float  # Light penetration depth
    surface_temperature_celsius: float
    salinity_ppt: float
    nutrient_nitrogen_umol_per_l: float
    nutrient_phosphorus_umol_per_l: float
    nutrient_iron_nmol_per_l: float
    mixing_depth_m: float
    current_speed_m_per_s: float
    sequestration_depth_m: float = 1000  # Depth for permanent sequestration


@dataclass
class OperationalParameters:
    """Operational and economic parameters."""
    area_km2: float
    application_frequency_per_year: float
    cultivation_cost_per_kg: float  # $/kg biomass
    delivery_cost_per_kg: float  # $/kg biomass
    vessel_cost_per_day: float  # $/day
    monitoring_cost_per_year: float  # $/year
    regulatory_cost_per_year: float  # $/year


class AlgaeCarbonSequestrationModel:
    """
    Comprehensive model for algae-based carbon sequestration.
    
    Calculates carbon sequestration potential, costs, and viability metrics.
    """
    
    def __init__(self, strain: AlgaeStrain, environment: EnvironmentalConditions, 
                 operations: OperationalParameters):
        self.strain = strain
        self.environment = environment
        self.operations = operations
        
        # Constants
        self.CARBON_TO_CO2_RATIO = 3.67  # g CO2 per g C
        self.DAYS_PER_YEAR = 365.25
        
    def calculate_growth_rate(self) -> float:
        """Calculate effective growth rate considering environmental conditions."""
        # Base growth rate from doubling time
        base_growth_rate = np.log(2) / (self.strain.doubling_time_hours / 24)
        
        # Temperature limitation
        temp_opt = (self.strain.optimal_temperature_range[0] + 
                   self.strain.optimal_temperature_range[1]) / 2
        temp_factor = self._temperature_response_factor()
        
        # Light limitation (based on euphotic depth)
        light_factor = self._light_limitation_factor()
        
        # Nutrient limitation
        nutrient_factor = self._nutrient_limitation_factor()
        
        # Salinity limitation
        salinity_factor = self._salinity_response_factor()
        
        effective_growth_rate = base_growth_rate * temp_factor * light_factor * nutrient_factor * salinity_factor
        
        return max(0, effective_growth_rate)
    
    def _temperature_response_factor(self) -> float:
        """Calculate temperature response factor (0-1)."""
        temp = self.environment.surface_temperature_celsius
        opt_min, opt_max = self.strain.optimal_temperature_range
        opt_temp = (opt_min + opt_max) / 2
        
        if temp < opt_min or temp > opt_max:
            return 0.0
        elif temp == opt_temp:
            return 1.0
        else:
            # Simple bell curve response
            return 1.0 - ((temp - opt_temp) / (opt_max - opt_min)) ** 2
    
    def _light_limitation_factor(self) -> float:
        """Calculate light limitation factor based on euphotic depth."""
        # Simplified light limitation model
        euphotic_depth = self.environment.euphotic_depth_m
        if euphotic_depth < 10:
            return 0.1
        elif euphotic_depth > 100:
            return 1.0
        else:
            return 0.1 + 0.9 * (euphotic_depth - 10) / 90
    
    def _nutrient_limitation_factor(self) -> float:
        """Calculate nutrient limitation factor (Liebig's law of minimum)."""
        # Nitrogen limitation
        n_factor = min(1.0, self.environment.nutrient_nitrogen_umol_per_l / 5.0)
        
        # Phosphorus limitation
        p_factor = min(1.0, self.environment.nutrient_phosphorus_umol_per_l / 0.3)
        
        # Iron limitation
        fe_factor = min(1.0, self.environment.nutrient_iron_nmol_per_l / 0.06)
        
        return min(n_factor, p_factor, fe_factor)
    
    def _salinity_response_factor(self) -> float:
        """Calculate salinity response factor (0-1)."""
        salinity = self.environment.salinity_ppt
        opt_min, opt_max = self.strain.optimal_salinity_range
        
        if salinity < opt_min or salinity > opt_max:
            return 0.0
        elif salinity == (opt_min + opt_max) / 2:
            return 1.0
        else:
            return 1.0 - ((salinity - (opt_min + opt_max) / 2) / (opt_max - opt_min)) ** 2
    
    def calculate_net_primary_productivity(self) -> float:
        """Calculate Net Primary Productivity in g C/m²/year."""
        growth_rate = self.calculate_growth_rate()
        
        # Convert to annual NPP
        # Assuming average biomass of 1 g C/m² in mixed layer
        mixed_layer_depth = self.environment.mixing_depth_m
        biomass_density = 1.0  # g C/m³
        
        npp = growth_rate * biomass_density * mixed_layer_depth * self.DAYS_PER_YEAR
        
        return max(0, npp)
    
    def calculate_carbon_export(self) -> float:
        """Calculate carbon export below sequestration depth in g C/m²/year."""
        npp = self.calculate_net_primary_productivity()
        
        # Apply export fraction
        export_carbon = npp * self.strain.export_fraction
        
        # Apply remineralization during sinking
        sinking_time_days = self.environment.sequestration_depth_m / self.strain.sinking_rate_m_per_day
        remineralization_rate_per_day = 0.1  # 10% per day
        survival_fraction = np.exp(-remineralization_rate_per_day * sinking_time_days)
        
        return export_carbon * survival_fraction
    
    def calculate_total_carbon_sequestered(self) -> float:
        """Calculate total carbon sequestered in the area in kg C/year."""
        carbon_export_per_m2 = self.calculate_carbon_export()
        area_m2 = self.operations.area_km2 * 1e6
        
        return carbon_export_per_m2 * area_m2 / 1000  # Convert to kg
    
    def calculate_co2_removed(self) -> float:
        """Calculate CO2 removed in tonnes/year."""
        carbon_kg = self.calculate_total_carbon_sequestered()
        return carbon_kg * self.CARBON_TO_CO2_RATIO / 1000  # Convert to tonnes
    
    def calculate_biomass_required(self) -> float:
        """Calculate biomass required for seeding in kg/year."""
        # Estimate based on target NPP and growth rate
        target_npp = 125  # g C/m²/year (typical ocean NPP)
        current_npp = self.calculate_net_primary_productivity()
        
        if current_npp >= target_npp:
            return 0  # No additional biomass needed
        
        # Calculate biomass needed to achieve target NPP
        biomass_needed_per_m2 = (target_npp - current_npp) / self.strain.carbon_content_percent * 100
        area_m2 = self.operations.area_km2 * 1e6
        
        return biomass_needed_per_m2 * area_m2 / 1000  # Convert to kg
    
    def calculate_operational_costs(self) -> Dict[str, float]:
        """Calculate all operational costs in $/year."""
        biomass_required = self.calculate_biomass_required()
        
        # Cultivation costs
        cultivation_cost = biomass_required * self.operations.cultivation_cost_per_kg
        
        # Delivery costs
        delivery_cost = biomass_required * self.operations.delivery_cost_per_kg
        
        # Vessel costs
        vessel_cost = self.operations.vessel_cost_per_day * self.DAYS_PER_YEAR
        
        # Monitoring and regulatory costs
        monitoring_cost = self.operations.monitoring_cost_per_year
        regulatory_cost = self.operations.regulatory_cost_per_year
        
        # R&D costs (amortized over 10 years)
        r_and_d_cost = self.strain.r_and_d_cost_millions * 1e6 / 10
        
        total_cost = (cultivation_cost + delivery_cost + vessel_cost + 
                     monitoring_cost + regulatory_cost + r_and_d_cost)
        
        return {
            'cultivation': cultivation_cost,
            'delivery': delivery_cost,
            'vessel': vessel_cost,
            'monitoring': monitoring_cost,
            'regulatory': regulatory_cost,
            'r_and_d': r_and_d_cost,
            'total': total_cost
        }
    
    def calculate_cost_per_tonne_co2(self) -> float:
        """Calculate cost per tonne CO2 removed in $/t CO2."""
        costs = self.calculate_operational_costs()
        co2_removed = self.calculate_co2_removed()
        
        if co2_removed <= 0:
            return float('inf')
        
        return costs['total'] / co2_removed
    
    def calculate_viability_metrics(self) -> Dict[str, float]:
        """Calculate comprehensive viability metrics."""
        co2_removed = self.calculate_co2_removed()
        cost_per_tonne = self.calculate_cost_per_tonne_co2()
        costs = self.calculate_operational_costs()
        
        # Target metrics for viability
        target_cost_per_tonne = 100  # $/t CO2 (competitive with other CDR methods)
        target_co2_removed = 1000  # tonnes/year (meaningful scale)
        
        return {
            'co2_removed_tonnes_per_year': co2_removed,
            'cost_per_tonne_co2': cost_per_tonne,
            'total_cost_per_year': costs['total'],
            'biomass_required_kg_per_year': self.calculate_biomass_required(),
            'carbon_sequestered_kg_per_year': self.calculate_total_carbon_sequestered(),
            'npp_g_c_per_m2_per_year': self.calculate_net_primary_productivity(),
            'growth_rate_per_day': self.calculate_growth_rate(),
            'viability_score': self._calculate_viability_score(cost_per_tonne, co2_removed),
            'cost_competitiveness': target_cost_per_tonne / cost_per_tonne if cost_per_tonne > 0 else 0,
            'scale_adequacy': co2_removed / target_co2_removed
        }
    
    def _calculate_viability_score(self, cost_per_tonne: float, co2_removed: float) -> float:
        """Calculate a viability score (0-1) based on cost and scale."""
        if cost_per_tonne <= 0 or co2_removed <= 0:
            return 0.0
        
        # Cost component (lower is better)
        cost_score = max(0, 1 - (cost_per_tonne - 50) / 200)  # 50-250 $/t range
        
        # Scale component (higher is better)
        scale_score = min(1, co2_removed / 10000)  # 10,000 t/year as full score
        
        # Environmental safety component
        safety_score = 1.0 if self.strain.genetic_kill_switch else 0.5
        
        return (cost_score * 0.4 + scale_score * 0.4 + safety_score * 0.2)
    
    def generate_report(self) -> str:
        """Generate a comprehensive text report."""
        metrics = self.calculate_viability_metrics()
        costs = self.calculate_operational_costs()
        
        report = f"""
ALGAE CARBON SEQUESTRATION MODEL REPORT
=======================================

STRAIN PARAMETERS:
- Name: {self.strain.name}
- Carbon Content: {self.strain.carbon_content_percent:.1f}% dry weight
- Doubling Time: {self.strain.doubling_time_hours:.1f} hours
- Export Fraction: {self.strain.export_fraction:.1%}
- Sinking Rate: {self.strain.sinking_rate_m_per_day:.1f} m/day

ENVIRONMENTAL CONDITIONS:
- Euphotic Depth: {self.environment.euphotic_depth_m:.0f} m
- Surface Temperature: {self.environment.surface_temperature_celsius:.1f}°C
- Salinity: {self.environment.salinity_ppt:.1f} ppt
- Sequestration Depth: {self.environment.sequestration_depth_m:.0f} m

OPERATIONAL PARAMETERS:
- Area: {self.operations.area_km2:.1f} km²
- Application Frequency: {self.operations.application_frequency_per_year:.1f} per year

RESULTS:
- CO2 Removed: {metrics['co2_removed_tonnes_per_year']:.1f} tonnes/year
- Cost per Tonne CO2: ${metrics['cost_per_tonne_co2']:.2f}/t CO2
- Total Annual Cost: ${metrics['total_cost_per_year']:,.0f}
- Biomass Required: {metrics['biomass_required_kg_per_year']:,.0f} kg/year
- NPP: {metrics['npp_g_c_per_m2_per_year']:.1f} g C/m²/year
- Growth Rate: {metrics['growth_rate_per_day']:.3f} per day

VIABILITY ASSESSMENT:
- Viability Score: {metrics['viability_score']:.2f}/1.00
- Cost Competitiveness: {metrics['cost_competitiveness']:.2f}x target
- Scale Adequacy: {metrics['scale_adequacy']:.2f}x target

COST BREAKDOWN:
- Cultivation: ${costs['cultivation']:,.0f}
- Delivery: ${costs['delivery']:,.0f}
- Vessel Operations: ${costs['vessel']:,.0f}
- Monitoring: ${costs['monitoring']:,.0f}
- Regulatory: ${costs['regulatory']:,.0f}
- R&D (amortized): ${costs['r_and_d']:,.0f}
"""
        return report


def create_sample_strains() -> Dict[str, AlgaeStrain]:
    """Create sample algae strains for testing."""
    strains = {
        'fast_growing_cyanobacteria': AlgaeStrain(
            name="Fast-growing Cyanobacteria",
            carbon_content_percent=45.0,
            doubling_time_hours=12.0,
            photosynthetic_efficiency=0.8,
            sinking_rate_m_per_day=50.0,
            export_fraction=0.4,
            optimal_temperature_range=(20, 30),
            optimal_salinity_range=(30, 40),
            genetic_kill_switch=True,
            r_and_d_cost_millions=15.0
        ),
        'diatom_variant': AlgaeStrain(
            name="GM Diatom Variant",
            carbon_content_percent=52.0,
            doubling_time_hours=24.0,
            photosynthetic_efficiency=0.9,
            sinking_rate_m_per_day=100.0,
            export_fraction=0.6,
            optimal_temperature_range=(15, 25),
            optimal_salinity_range=(25, 35),
            genetic_kill_switch=True,
            r_and_d_cost_millions=20.0
        ),
        'conservative_strain': AlgaeStrain(
            name="Conservative GM Algae",
            carbon_content_percent=40.0,
            doubling_time_hours=48.0,
            photosynthetic_efficiency=0.7,
            sinking_rate_m_per_day=25.0,
            export_fraction=0.3,
            optimal_temperature_range=(18, 28),
            optimal_salinity_range=(28, 38),
            genetic_kill_switch=True,
            r_and_d_cost_millions=10.0
        )
    }
    return strains


def create_sample_environments() -> Dict[str, EnvironmentalConditions]:
    """Create sample environmental conditions for testing."""
    environments = {
        'tropical_ocean': EnvironmentalConditions(
            euphotic_depth_m=80,
            surface_temperature_celsius=28,
            salinity_ppt=35,
            nutrient_nitrogen_umol_per_l=2.0,
            nutrient_phosphorus_umol_per_l=0.2,
            nutrient_iron_nmol_per_l=0.05,
            mixing_depth_m=50,
            current_speed_m_per_s=0.1,
            sequestration_depth_m=1000
        ),
        'temperate_ocean': EnvironmentalConditions(
            euphotic_depth_m=60,
            surface_temperature_celsius=15,
            salinity_ppt=33,
            nutrient_nitrogen_umol_per_l=5.0,
            nutrient_phosphorus_umol_per_l=0.4,
            nutrient_iron_nmol_per_l=0.08,
            mixing_depth_m=100,
            current_speed_m_per_s=0.2,
            sequestration_depth_m=1500
        ),
        'nutrient_rich': EnvironmentalConditions(
            euphotic_depth_m=40,
            surface_temperature_celsius=20,
            salinity_ppt=34,
            nutrient_nitrogen_umol_per_l=10.0,
            nutrient_phosphorus_umol_per_l=0.8,
            nutrient_iron_nmol_per_l=0.12,
            mixing_depth_m=75,
            current_speed_m_per_s=0.15,
            sequestration_depth_m=1200
        )
    }
    return environments


if __name__ == "__main__":
    # Example usage
    strains = create_sample_strains()
    environments = create_sample_environments()
    
    # Test with fast-growing cyanobacteria in tropical ocean
    strain = strains['fast_growing_cyanobacteria']
    environment = environments['tropical_ocean']
    operations = OperationalParameters(
        area_km2=1000,
        application_frequency_per_year=4,
        cultivation_cost_per_kg=0.5,
        delivery_cost_per_kg=0.3,
        vessel_cost_per_day=5000,
        monitoring_cost_per_year=100000,
        regulatory_cost_per_year=50000
    )
    
    model = AlgaeCarbonSequestrationModel(strain, environment, operations)
    
    print(model.generate_report()) 