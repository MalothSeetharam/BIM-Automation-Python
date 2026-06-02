import ifcopenshell
import pandas as pd
import os

def generate_large_skyscraper_dataset(file_path):
    print("🏗️ Synthesizing 10-Story Skyscraper Structural Database...")
    
    # Initialize a completely empty, standard compliant IFC file
    model = ifcopenshell.file(schema="IFC2X3")
    
    # 1. Establish the baseline project framework using standard entity methods
    owner_history = model.create_entity("IfcOwnerHistory") # Required structural metadata link
    project = model.create_entity("IfcProject", GlobalId="123_Project_ID", Name="Dubai Tech Tower")
    building = model.create_entity("IfcBuilding", GlobalId="456_Building_ID", Name="Tower A")
    
    # 2. Build out the 10-story skyscraper sequence
    for level in range(1, 11):
        floor_id = f"Floor_UUID_{level:02d}"
        floor_name = f"Level {level:02d}"
        elevation = float((level - 1) * 4.0)  # 4-meter ceiling height increments
        
        # Create structural floor level container entity
        storey = model.create_entity("IfcBuildingStorey", GlobalId=floor_id, Name=floor_name, Elevation=elevation)
        
        # Simulating skyscraper column/wall optimization curves:
        # Heavier structural components on lower foundations, scaling down gracefully
        columns_on_this_floor = 24 - (level * 1)  
        walls_on_this_floor = 16 + (level % 2 * 4)
        slabs_on_this_floor = 2 if level < 10 else 1  # Multi-slabs down low vs a single roof cap
        
        elements_group = []
        
        # Populate columns for this level
        for i in range(columns_on_this_floor):
            col = model.create_entity("IfcColumn", GlobalId=f"COL_L{level}_{i}", Name=f"Column-C{i}")
            elements_group.append(col)
            
        # Populate load-bearing wall configurations
        for j in range(walls_on_this_floor):
            wall = model.create_entity("IfcWall", GlobalId=f"WAL_L{level}_{j}", Name=f"StructuralWall-W{j}")
            elements_group.append(wall)
            
        # Populate concrete slab arrays
        for k in range(slabs_on_this_floor):
            slab = model.create_entity("IfcSlab", GlobalId=f"SLB_L{level}_{k}", Name=f"ConcreteSlab-S{k}")
            elements_group.append(slab)
            
        # 3. Create the spatial containment mapping to bind elements directly to this level
        model.create_entity(
            "IfcRelContainedInSpatialStructure",
            GlobalId=f"REL_SPATIAL_L{level}",
            Name=f"Spatial-Containment-L{level}",
            RelatingStructure=storey,
            RelatedElements=elements_group
        )
        
    model.write(file_path)
    print(f"📦 Local asset generation complete! Generated structural layout: '{file_path}'")


def run_skyscraper_analytics(ifc_path, excel_path):
    print("\n🔍 Booting Structural Analytics Engine...")
    model = ifcopenshell.open(ifc_path)
    
    # Scan building storeys from the fresh dataset
    floors = model.by_type("IfcBuildingStorey")
    dashboard_summary = []
    
    for floor in floors:
        floor_name = floor.Name
        elevation = floor.Elevation
        
        column_count = 0
        wall_count = 0
        slab_count = 0
        
        # Traverse the spatial containment lists to build counts
        if hasattr(floor, "ContainsElements"):
            for containment in floor.ContainsElements:
                for element in containment.RelatedElements:
                    if element.is_a("IfcColumn"):
                        column_count += 1
                    elif element.is_a("IfcWall"):
                        wall_count += 1
                    elif element.is_a("IfcSlab"):
                        slab_count += 1
                        
        dashboard_summary.append({
            "Floor_Level": floor_name,
            "Elevation_Height": f"{elevation:.1f}m",
            "Total_Columns": column_count,
            "Total_Walls": wall_count,
            "Total_Floor_Slabs": slab_count,
            "Total_Level_Assets": column_count + wall_count + slab_count
        })
        
    # Compile the final spreadsheet dashboard asset
    df = pd.DataFrame(dashboard_summary)
    df.to_excel(excel_path, index=False)
    
    print("\n🚀 SUCCESS! Production Dashboard Live.")
    print("=" * 80)
    print(df.to_string(index=False))
    print("=" * 80)
    print(f"📂 Compiled data sheet successfully written to: {excel_path}")


if __name__ == "__main__":
    ifc_file = "skyscraper_structure.ifc"
    excel_file = "Skyscraper_Level_Dashboard.xlsx"
    
    generate_large_skyscraper_dataset(ifc_file)
    run_skyscraper_analytics(ifc_file, excel_file)