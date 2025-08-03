#!/usr/bin/env python3
"""
LEGACY FILE - No longer needed for Johnny Algae Sea

This was a test script for the old Python-based Algae Carbon Sequestration Model.
The project has been simplified to a standalone HTML calculator.

To use the current version:
1. Open johnny_algae_sea_standalone.html in any web browser
2. No Python installation or dependencies required!

This file is kept for reference only.

--- Original Description ---
Test script for the Algae Carbon Sequestration Model
Demonstrates different scenarios and parameter combinations.
"""

# The rest of this file is legacy code and not needed for the current HTML version
print("⚠️  LEGACY FILE - This Python script is no longer needed!")
print("📄 Please use johnny_algae_sea_standalone.html instead")
print("🌐 Simply open the HTML file in any web browser")
exit()

# Legacy code below (not executed)
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models.algae_model import (
    AlgaeCarbonSequestrationModel,
    AlgaeStrain,
    EnvironmentalConditions,
    OperationalParameters,
    create_sample_strains,
    create_sample_environments
)


def test_basic_scenario():
    """Test the basic scenario with fast-growing cyanobacteria."""
    print("=" * 60)
    print("BASIC SCENARIO: Fast-growing Cyanobacteria in Tropical Ocean")
    print("=" * 60)
    
    # Create strain
    strain = AlgaeStrain(
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
        current_speed_m_per_s=0.1,
        sequestration_depth_m=1000
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
    costs = model.calculate_operational_costs()
    
    print(f"CO₂ Removed: {metrics['co2_removed_tonnes_per_year']:,.1f} tonnes/year")
    print(f"Cost per Tonne: ${metrics['cost_per_tonne_co2']:.2f}/t CO₂")
    print(f"Viability Score: {metrics['viability_score']:.2f}/1.00")
    print(f"Total Cost: ${metrics['total_cost_per_year']:,.0f}/year")
    print(f"Biomass Required: {metrics['biomass_required_kg_per_year']:,.0f} kg/year")
    print(f"NPP: {metrics['npp_g_c_per_m2_per_year']:.1f} g C/m²/year")
    print(f"Growth Rate: {metrics['growth_rate_per_day']:.3f} per day")
    print()


def test_all_sample_scenarios():
    """Test all sample strains and environments."""
    print("=" * 60)
    print("COMPARISON OF ALL SAMPLE SCENARIOS")
    print("=" * 60)
    
    strains = create_sample_strains()
    environments = create_sample_environments()
    
    # Fixed operations for comparison
    operations = OperationalParameters(
        area_km2=1000,
        application_frequency_per_year=4,
        cultivation_cost_per_kg=0.5,
        delivery_cost_per_kg=0.3,
        vessel_cost_per_day=5000,
        monitoring_cost_per_year=100000,
        regulatory_cost_per_year=50000
    )
    
    results = []
    
    for strain_name, strain in strains.items():
        for env_name, environment in environments.items():
            model = AlgaeCarbonSequestrationModel(strain, environment, operations)
            metrics = model.calculate_viability_metrics()
            
            results.append({
                'Strain': strain.name,
                'Environment': env_name,
                'CO₂ Removed (t/year)': metrics['co2_removed_tonnes_per_year'],
                'Cost per Tonne ($/t)': metrics['cost_per_tonne_co2'],
                'Viability Score': metrics['viability_score'],
                'NPP (g C/m²/year)': metrics['npp_g_c_per_m2_per_year'],
                'Growth Rate (/day)': metrics['growth_rate_per_day']
            })
    
    # Print results in a table format
    print(f"{'Strain':<25} {'Environment':<20} {'CO₂ (t/year)':<12} {'Cost ($/t)':<10} {'Viability':<10}")
    print("-" * 80)
    
    for result in results:
        print(f"{result['Strain']:<25} {result['Environment']:<20} "
              f"{result['CO₂ Removed (t/year)']:<12.0f} "
              f"{result['Cost per Tonne ($/t)']:<10.1f} "
              f"{result['Viability Score']:<10.2f}")
    print()


def test_parameter_sensitivity():
    """Test sensitivity to key parameters."""
    print("=" * 60)
    print("PARAMETER SENSITIVITY ANALYSIS")
    print("=" * 60)
    
    # Base scenario
    strain = AlgaeStrain(
        name="Test Strain",
        carbon_content_percent=45.0,
        doubling_time_hours=24.0,
        photosynthetic_efficiency=0.8,
        sinking_rate_m_per_day=50.0,
        export_fraction=0.4,
        optimal_temperature_range=(20, 30),
        optimal_salinity_range=(30, 40)
    )
    
    environment = EnvironmentalConditions(
        euphotic_depth_m=80,
        surface_temperature_celsius=25,
        salinity_ppt=35,
        nutrient_nitrogen_umol_per_l=5.0,
        nutrient_phosphorus_umol_per_l=0.4,
        nutrient_iron_nmol_per_l=0.08,
        mixing_depth_m=75,
        current_speed_m_per_s=0.15
    )
    
    operations = OperationalParameters(
        area_km2=1000,
        application_frequency_per_year=4,
        cultivation_cost_per_kg=0.5,
        delivery_cost_per_kg=0.3,
        vessel_cost_per_day=5000,
        monitoring_cost_per_year=100000,
        regulatory_cost_per_year=50000
    )
    
    # Test different doubling times
    print("Effect of Doubling Time:")
    doubling_times = [12, 24, 48, 72]
    for dt in doubling_times:
        strain.doubling_time_hours = dt
        model = AlgaeCarbonSequestrationModel(strain, environment, operations)
        metrics = model.calculate_viability_metrics()
        print(f"  {dt:2d} hours: {metrics['co2_removed_tonnes_per_year']:>8.0f} t/year, "
              f"${metrics['cost_per_tonne_co2']:>6.1f}/t, "
              f"viability {metrics['viability_score']:.2f}")
    
    print()
    
    # Test different areas
    print("Effect of Area:")
    areas = [100, 500, 1000, 5000, 10000]
    strain.doubling_time_hours = 24  # Reset to base
    for area in areas:
        operations.area_km2 = area
        model = AlgaeCarbonSequestrationModel(strain, environment, operations)
        metrics = model.calculate_viability_metrics()
        print(f"  {area:>5d} km²: {metrics['co2_removed_tonnes_per_year']:>8.0f} t/year, "
              f"${metrics['cost_per_tonne_co2']:>6.1f}/t, "
              f"viability {metrics['viability_score']:.2f}")
    
    print()
    
    # Test different export fractions
    print("Effect of Export Fraction:")
    export_fractions = [0.2, 0.4, 0.6, 0.8]
    operations.area_km2 = 1000  # Reset to base
    for ef in export_fractions:
        strain.export_fraction = ef
        model = AlgaeCarbonSequestrationModel(strain, environment, operations)
        metrics = model.calculate_viability_metrics()
        print(f"  {ef:>3.1f}: {metrics['co2_removed_tonnes_per_year']:>8.0f} t/year, "
              f"${metrics['cost_per_tonne_co2']:>6.1f}/t, "
              f"viability {metrics['viability_score']:.2f}")


def main():
    """Run all tests."""
    print("🌊 ALGAE CARBON SEQUESTRATION MODEL - TEST SUITE")
    print("=" * 60)
    
    test_basic_scenario()
    test_all_sample_scenarios()
    test_parameter_sensitivity()
    
    print("=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    print("\nKey Insights:")
    print("1. Faster doubling times generally improve viability")
    print("2. Larger areas show better economics of scale")
    print("3. Higher export fractions increase sequestration")
    print("4. Environmental conditions significantly affect performance")
    print("5. Cost per tonne CO₂ is the key viability metric")


if __name__ == "__main__":
    main() 