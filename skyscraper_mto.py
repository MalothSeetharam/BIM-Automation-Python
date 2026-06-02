import ifcopenshell
import ifcopenshell.api
import pandas as pd

def generate_material_takeoff(excel_path):
    print("🏗️ Initializing Skyscraper Material Takeoff (MTO) Engine...")
    
    # Initialize a compliant structural model database
    model = ifcopenshell.file(schema="IFC2X3")
    
    # Establish project metadata frameworks
    project = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcProject", name="Dubai Tech Tower")
    building = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcBuilding", name="Tower A")
    
    mto_records = []
    
    print("📐 Calculating concrete volume and material allocation metrics...")
    
    # Loop through all 10 floors to run material math
    for level in range(1, 11):
        floor_name = f"Level {level:02d}"
        elevation = float((level - 1) * 4.0)
        
        # Define slab structural dimensional specifications
        # Let's say lower floors have thicker slabs (0.3m / 300mm) for heavy loads, 
        # and upper floors use standard slabs (0.2m / 200mm) to reduce dead weight.
        slab_thickness = 0.30 if level <= 3 else 0.20
        floor_area = 1200.0 # 1,200 square meters per floor plate
        
        # Material Takeoff Calculations
        concrete_volume_per_slab = floor_area * slab_thickness
        total_slabs_on_floor = 2 if level < 10 else 1 # Roof has a single slab cap
        total_floor_concrete_volume = concrete_volume_per_slab * total_slabs_on_floor
        
        # Standard concrete weight density is roughly 2.4 Tons per cubic meter
        concrete_weight_tons = total_floor_concrete_volume * 2.4
        
        # Create the slab entity in our 3D database model
        ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcSlab", name=f"Slab-L{level}")
        
        # Append calculated engineering metrics to our schedule log array
        mto_records.append({
            "Floor_Level": floor_name,
            "Elevation": f"{elevation:.1f}m",
            "Floor_Area_(m2)": floor_area,
            "Slab_Thickness_(m)": slab_thickness,
            "Slab_Count": total_slabs_on_floor,
            "Concrete_Volume_(m3)": total_floor_concrete_volume,
            "Est_Concrete_Weight_(Tons)": concrete_weight_tons
        })
        
    # Compile everything into a structured master schedule dataframe
    df = pd.DataFrame(mto_records)
    
    # Add a Summary Row at the bottom for total project procurement order
    total_row = pd.DataFrame([{
        "Floor_Level": "TOTAL REQUIREMENT",
        "Elevation": "-",
        "Floor_Area_(m2)": df["Floor_Area_(m2)"].sum(),
        "Slab_Thickness_(m)": "-",
        "Slab_Count": df["Slab_Count"].sum(),
        "Concrete_Volume_(m3)": df["Concrete_Volume_(m3)"].sum(),
        "Est_Concrete_Weight_(Tons)": df["Est_Concrete_Weight_(Tons)"].sum()
    }])
    
    final_df = pd.concat([df, total_row], ignore_index=True)
    
    # Export cleanly to an Excel material schedule
    final_df.to_excel(excel_path, index=False)
    
    print("\n🚀 MATERIAL TAKEOFF SCHEDULE GENERATED SUCCESSFULLY!")
    print("=" * 95)
    print(final_df.to_string(index=False))
    print("=" * 95)
    print(f"📂 Master procurement sheet compiled and written to: {excel_path}")

if __name__ == "__main__":
    generate_material_takeoff("Skyscraper_Material_Takeoff_Schedule.xlsx")