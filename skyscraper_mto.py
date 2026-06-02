import ifcopenshell
import pandas as pd

def generate_material_takeoff(excel_path):
    print("🏗️ Initializing Skyscraper Material Takeoff (MTO) Engine...")
    
    # Initialize an empty IFC file with a stable standard schema
    model = ifcopenshell.file(schema="IFC2X3")
    
    # Create baseline project infrastructure directly to avoid user profile errors
    project = model.create_entity("IfcProject", GlobalId="123_Proj_MTO", Name="Dubai Tech Tower")
    building = model.create_entity("IfcBuilding", GlobalId="456_Bldg_MTO", Name="Tower A")
    
    mto_records = []
    
    print("📐 Calculating concrete volumes and material density distributions...")
    
    # Process load variations for all 10 stories
    for level in range(1, 11):
        floor_name = f"Level {level:02d}"
        elevation = float((level - 1) * 4.0)
        
        # Design Logic: Thicker slabs at foundation levels to support cumulative load
        slab_thickness = 0.30 if level <= 3 else 0.20
        floor_area = 1200.0  # 1200 sq meters floor plate
        
        # Quantitative Calculations
        concrete_volume_per_slab = floor_area * slab_thickness
        total_slabs_on_floor = 2 if level < 10 else 1  # Roof has a single cap slab
        total_floor_concrete_volume = concrete_volume_per_slab * total_slabs_on_floor
        
        # Reinforced concrete density constant (~2.4 Tons per cubic meter)
        concrete_weight_tons = total_floor_concrete_volume * 2.4
        
        # Write the component data straight into our local IFC database schema
        model.create_entity("IfcSlab", GlobalId=f"SLB_MTO_L{level}", Name=f"ConcreteSlab-Floor-{level}")
        
        # Append calculated row to our spreadsheet data matrix
        mto_records.append({
            "Floor_Level": floor_name,
            "Elevation": f"{elevation:.1f}m",
            "Floor_Area_(m2)": floor_area,
            "Slab_Thickness_(m)": slab_thickness,
            "Slab_Count": total_slabs_on_floor,
            "Concrete_Volume_(m3)": total_floor_concrete_volume,
            "Est_Concrete_Weight_(Tons)": concrete_weight_tons
        })
        
    # Compile base data metrics
    df = pd.DataFrame(mto_records)
    
    # Calculate global project totals for the summary row
    total_row = pd.DataFrame([{
        "Floor_Level": "TOTAL REQUIREMENT",
        "Elevation": "-",
        "Floor_Area_(m2)": df["Floor_Area_(m2)"].sum(),
        "Slab_Thickness_(m)": "-",
        "Slab_Count": df["Slab_Count"].sum(),
        "Concrete_Volume_(m3)": df["Concrete_Volume_(m3)"].sum(),
        "Est_Concrete_Weight_(Tons)": df["Est_Concrete_Weight_(Tons)"].sum()
    }])
    
    # Merge summary row seamlessly to the bottom
    final_df = pd.concat([df, total_row], ignore_index=True)
    
    # Generate the professional Excel schedule
    final_df.to_excel(excel_path, index=False)
    
    print("\n🚀 MATERIAL TAKEOFF SCHEDULE GENERATED SUCCESSFULLY!")
    print("=" * 95)
    print(final_df.to_string(index=False))
    print("=" * 95)
    print(f"📂 Procurement spreadsheet compiled live at: {excel_path}")

if __name__ == "__main__":
    generate_material_takeoff("Skyscraper_Material_Takeoff_Schedule.xlsx")