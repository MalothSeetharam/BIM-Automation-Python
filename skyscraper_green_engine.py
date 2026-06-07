import ifcopenshell
import pandas as pd

def run_green_compliance_engine(excel_path):
    print("🌿 Initializing Sustainable Skyscraper Compliance Engine...")
    
    # 1. Initialize an IFC model container using a stable base schema
    model = ifcopenshell.file(schema="IFC2X3")
    model.create_entity("IfcProject", GlobalId="123_GREEN_PROJ", Name="Dubai Green Tower")
    
    # Corporate Regulatory Standard: Maximum allowable Embodied Carbon per square meter
    # Based on modern international sustainable building thresholds (Al Sa'fat / LEED benchmarks)
    MAX_CARBON_ALLOWABLE_PER_M2 = 200.0  # kg CO2e / m2
    FLOOR_AREA = 1500.0  # 1,500 sq meters floor plate
    
    # Material Environmental Coefficients (Global Averages for Production Materials)
    # Embodied Carbon: kg CO2e per m3 | Embodied Energy: MegaJoules (MJ) per m3
    ENVIRONMENTAL_FACTORS = {
        "Concrete": {"carbon_factor": 320.0, "energy_factor": 2500.0},
        "Structural Steel": {"carbon_factor": 1850.0, "energy_factor": 12000.0},
        "Glass": {"carbon_factor": 890.0, "energy_factor": 6000.0}
    }
    
    compliance_records = []
    print("📊 Evaluating material volumes against global green building regulations...")
    
    # 2. Process load, material layout, and compliance variations for a 10-story tower
    for level in range(1, 12):
        floor_name = f"Level {level:02d}"
        
        # Design Logic: Material quantities vary by height to minimize upper structural dead load
        if level <= 3:
            concrete_vol = 450.0   # Heavy foundation columns and core walls
            steel_vol = 30.0
            glass_vol = 10.0
        elif level <= 8:
            concrete_vol = 300.0   # Standard typical floors
            steel_vol = 25.0
            glass_vol = 25.0       # Higher percentage of glass facade
        else:
            concrete_vol = 100.0   # Reduced concrete to save weight
            steel_vol = 45.0       # High steel reinforcement for the structural crown
            glass_vol = 50.0       # Premium floor-to-ceiling glass paneling      # High glass observation zones
            
        # Write structural component database references locally into the IFC schema
        model.create_entity("IfcBuildingStorey", GlobalId=f"STOREY_L{level}", Name=floor_name)
        
        # Calculate Total Embodied Carbon on this specific level (Material Volume x Coefficient)
        total_carbon = (
            (concrete_vol * ENVIRONMENTAL_FACTORS["Concrete"]["carbon_factor"]) +
            (steel_vol * ENVIRONMENTAL_FACTORS["Structural Steel"]["carbon_factor"]) +
            (glass_vol * ENVIRONMENTAL_FACTORS["Glass"]["carbon_factor"])
        )
        
        # Calculate Total Embodied Energy on this specific level
        total_energy = (
            (concrete_vol * ENVIRONMENTAL_FACTORS["Concrete"]["energy_factor"]) +
            (steel_vol * ENVIRONMENTAL_FACTORS["Structural Steel"]["energy_factor"]) +
            (glass_vol * ENVIRONMENTAL_FACTORS["Glass"]["energy_factor"])
        )
        
        # Calculate Regulatory Intensity Metrics
        carbon_intensity = total_carbon / FLOOR_AREA
        
        # 3. Regulatory Guardrails & Automated Mitigation Logic
        if carbon_intensity > MAX_CARBON_ALLOWABLE_PER_M2:
            status = "❌ NON-COMPLIANT"
            excess_carbon = total_carbon - (MAX_CARBON_ALLOWABLE_PER_M2 * FLOOR_AREA)
            # Mitigation directive: Recommend substituting standard Portland mix with Fly-Ash/GGBS green concrete
            # Standard green concrete substitution saves roughly 200 kg CO2e per m3 altered
            suggested_substitution_m3 = excess_carbon / 200.0
            mitigation = f"Excess carbon: {excess_carbon:,.0f} kg. Substitute {suggested_substitution_m3:.1f} m3 with Fly-Ash/GGBS Green Mix."
        else:
            status = "✅ COMPLIANT"
            mitigation = "Meets regulatory standard. Structural design carbon-optimized."
            
        compliance_records.append({
            "Floor_Level": floor_name,
            "Concrete_Vol_(m3)": concrete_vol,
            "Steel_Vol_(m3)": steel_vol,
            "Glass_Vol_(m3)": glass_vol,
            "Total_Carbon_(kg_CO2e)": total_carbon,
            "Carbon_Intensity_(kg/m2)": round(carbon_intensity, 2),
            "Embodied_Energy_(MJ)": total_energy,
            "Sustainability_Status": status,
            "Engineering_Mitigation_Directives": mitigation
        })
        
    # Compile metrics into a master dashboard data frame
    df = pd.DataFrame(compliance_records)
    
    # 4. Export to a clean corporate spreadsheet report
    df.to_excel(excel_path, index=False)
    
    print("\n🚀 SUSTAINABILITY COMPLIANCE RUN COMPLETE!")
    print("=" * 125)
    print(df.to_string(index=False, columns=["Floor_Level", "Carbon_Intensity_(kg/m2)", "Sustainability_Status", "Engineering_Mitigation_Directives"]))
    print("=" * 125)
    print(f"📂 Executive audit dashboard compiled successfully and exported to: {excel_path}")

if __name__ == "__main__":
    run_green_compliance_engine("Skyscraper_Green_Compliance_Report.xlsx")