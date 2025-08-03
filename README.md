# Johnny Algae Sea - Carbon Sequestration Calculator

A simple, standalone HTML calculator for modeling algae-based ocean carbon sequestration. This project provides "napkin math" calculations to test the viability of deploying algae to regions of the ocean where they can sequester carbon dioxide by growing, dying, and sinking to great depths.

<img width="1024" height="1024" alt="JohnnyAlgaeSea" src="https://github.com/user-attachments/assets/b849ad69-5ba4-48a3-93bc-6b662a5e564c" />

## 🌊 Project Overview

**Johnny Algae Sea** evaluates the key components needed for algae-based carbon sequestration:

- **Biological**: Carbon content, growth rates, export fractions, doubling times
- **Environmental**: Light penetration, temperature, salinity conditions
- **Economic**: Cultivation costs, delivery systems, vessel operations, monitoring
- **Viability**: Cost per tonne CO₂ removed, scale requirements, permanence

## 🚀 Features

- **Standalone HTML Calculator**: No installation required - runs in any web browser
- **Real-time Calculations**: Instant results as you adjust parameters
- **Interactive Tooltips**: Detailed explanations for every parameter
- **Comprehensive Modeling**: Biological, environmental, and economic factors
- **Viability Assessment**: Weighted scoring system for project evaluation
- **Visual Feedback**: Color-coded viability indicators
- **Debug Console**: Built-in debugging for troubleshooting calculations

## 📁 Project Structure

```
CarbonSequesterModel/
├── johnny_algae_sea_standalone.html    # Main calculator (open this!)
├── JohnnyAlgaeSea.png                  # Character image
├── README.md                           # This file
├── requirements.txt                    # Legacy file (not needed)
└── test_model.py                       # Legacy file (not needed)
```

## 🛠️ Usage

**It's that simple!**

1. Download `johnny_algae_sea_standalone.html`
2. Open it in any web browser
3. Adjust parameters and see results instantly

No installation, no dependencies, no command line - just open and use!

## 📊 Model Parameters

### 🌱 Biological Parameters
- **NPP (Net Primary Productivity)**: 50-500 g C/m²/yr
- **Export Fraction**: 10-80% of algae that sink to depth
- **Carbon Content**: 30-60% of biomass dry weight
- **Doubling Time**: 6-72 hours for algae population growth

### 🌊 Environmental Parameters
- **Area**: 100-10,000 km² deployment area
- **Euphotic Depth**: 20-200 m where photosynthesis occurs
- **Temperature**: 10-40°C optimal range 20-30°C
- **Salinity**: 20-45 ppt optimal range 30-40 ppt

### 💰 Economic Parameters
- **Cultivation Cost**: $0.1-2.0 per kg biomass
- **Delivery Cost**: $0.1-1.0 per kg to deployment site
- **Vessel Cost**: $1,000-20,000 per day operational costs
- **Monitoring Cost**: $50,000-500,000 per year

### 🎯 Targets & Weights
- **Target Cost**: Competitive threshold (typically $50-200/t CO₂)
- **Target Scale**: Desired annual CO₂ removal (Mt/yr)
- **Permanence**: Required storage time (typically >100 years)
- **Cost/Scale/Environmental Weights**: Customize assessment priorities

## 📈 Sample Results

### Example: Productive Tropical Deployment
**Parameters:**
- Area: 1,000 km²
- NPP: 200 g C/m²/yr
- Export Fraction: 40%
- Temperature: 25°C (optimal)

**Results:**
- **CO₂ Removed**: ~147,000 tonnes/year
- **Cost per Tonne**: ~$450/t CO₂
- **Viability Score**: 0.12/1.00 (Low - too expensive)

### Getting to Viability
To achieve competitive costs (<$100/t CO₂):
- Increase scale (larger areas)
- Improve algae efficiency (higher NPP/export fraction)
- Reduce operational costs (vessel, cultivation)
- Deploy in optimal conditions (temperature, nutrients)

## 🎯 Key Insights

1. **Scale is Critical**: Larger deployments (>1000 km²) improve economics
2. **Export Fraction Matters**: More algae sinking = more carbon sequestered
3. **Environmental Optimization**: Stay within optimal temperature/salinity ranges
4. **Cost Drivers**: Vessel operations and cultivation are major expenses
5. **Viability Threshold**: <$100/t CO₂ needed for competitiveness with other CDR methods

## 🔍 Understanding the Calculator

### Viability Scoring
The calculator uses a weighted scoring system:
- **Cost Score**: Based on cost per tonne vs. target (lower is better)
- **Scale Score**: Based on CO₂ removal vs. target scale (higher is better)  
- **Environmental Score**: Based on permanence and leakage risk

### Cost Categories
- **≤50% of target**: Excellent (Score: 1.0)
- **≤100% of target**: Good (Score: 0.8)
- **≤150% of target**: Fair (Score: 0.4)
- **≤300% of target**: Poor (Score: 0.1)
- **>300% of target**: Unviable (Score: 0.0)

### Debug Features
Open browser console (F12) to see detailed calculation breakdowns including:
- Individual component scores
- Weighted contributions
- Parameter validation
- Step-by-step calculations

## 🔧 Troubleshooting

**No results showing?**
- Check browser console (F12) for errors
- Ensure all parameters are positive numbers
- Try refreshing the page

**Cost weight seems to have no impact?**
- Check if cost score is 0 (project too expensive)
- Adjust parameters to get cost into viable range first
- Use debug console to see weighted component contributions

**Viability score seems wrong?**
- Verify weight percentages add up reasonably
- Check that environmental weight isn't being double-counted
- Use debug output to trace calculation steps

## 🚀 Future Enhancements

- Seasonal variation modeling
- Multiple algae strain comparisons
- Economic scenario analysis
- Sensitivity analysis tools
- Batch parameter testing
- Results export functionality

## 📄 Model Limitations

- Simplified environmental response models
- Assumes constant conditions (no seasonal variation)
- Doesn't model ecological interactions
- Basic economic assumptions
- No regulatory/permitting costs
- Assumes technology feasibility

## 🤝 Contributing

This is a simple HTML file - contributions welcome!
1. Fork the repository
2. Edit `johnny_algae_sea_standalone.html`
3. Test in multiple browsers
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

---

**Note**: This calculator provides "back-of-the-envelope" calculations for evaluating algae-based carbon sequestration concepts. Results should be validated with detailed studies and expert review before any real-world implementation. 
