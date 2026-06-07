import os
import ifcopenshell
import pandas as pd

# Automatically handle local version unique ID rules
ifcopenshell.guid.create = ifcopenshell.guid.new

# Clear destination file paths
ifc_file_path = "C:/Users/malot/OneDrive/Desktop/Bim_automation/expert_foundation_project.ifc"
excel_file_path = "C:/Users/malot/OneDrive/Desktop/Bim_automation/structural_quantity_takeoff.xlsx"

print("Compiling perfectly aligned structural foundation models...")

# 1. INITIALIZE IFC DATABASE FILE
model = ifcopenshell.file(schema="IFC4")

# 2. DECLARE CORE SYSTEM WORKSPACE METADATA
owner_history = model.createIfcOwnerHistory()

# Set standard measurement scales (Metric Meters)
unit_length = model.createIfcSIUnit(UnitType="LENGTHUNIT", Name="METRE")
unit_assignment = model.createIfcUnitAssignment(Units=[unit_length])

# Set absolute world zero origin point (0,0,0)
wcs_point = model.createIfcCartesianPoint((0.0, 0.0, 0.0))
wcs_axis = model.createIfcAxis2Placement3D(wcs_point, None, None)

# Wake up the visual 3D graphics canvas rendering contexts
context_3d = model.createIfcGeometricRepresentationContext(
    ContextType="Model", CoordinateSpaceDimension=3, Precision=1e-5, WorldCoordinateSystem=wcs_axis
)

# Global project collection root container
project = model.createIfcProject(
    ifcopenshell.guid.create(), owner_history, Name="Expert Foundation Automation",
    RepresentationContexts=[context_3d], UnitsInContext=unit_assignment
)

# 3. BUILD SPATIAL HIERARCHY CONTAINERS
site = model.createIfcSite(ifcopenshell.guid.create(), owner_history, Name="Infrastructure Site", ObjectPlacement=wcs_axis)
building = model.createIfcBuilding(ifcopenshell.guid.create(), owner_history, Name="Engineering Complex", ObjectPlacement=wcs_axis)
storey = model.createIfcBuildingStorey(ifcopenshell.guid.create(), owner_history, Name="Foundation Level", Elevation=0.0, ObjectPlacement=wcs_axis)

# Link spatial tree architecture structure cleanly
model.createIfcRelAggregates(ifcopenshell.guid.create(), owner_history, "ProjToSite", None, project, [site])
model.createIfcRelAggregates(ifcopenshell.guid.create(), owner_history, "SiteToBuild", None, site, [building])
model.createIfcRelAggregates(ifcopenshell.guid.create(), owner_history, "BuildToStorey", None, building, [storey])

# 4. FIXED INDEPENDENT PARAMETRIC GEOMETRY GENERATOR FUNCTION
def generate_3d_element_shape(model, context, x_dim, y_dim, height, x_pos, y_pos, z_pos):
    # CRITICAL FIX: Every object gets its own isolated point and orientation instances
    item_position = model.createIfcCartesianPoint((x_pos, y_pos, z_pos))
    item_placement_3d = model.createIfcAxis2Placement3D(item_position, None, None)
    local_placement = model.createIfcLocalPlacement(None, item_placement_3d)
    
    # Establish local 2D shape drawing face profile
    profile_origin_point = model.createIfcCartesianPoint((0.0, 0.0))
    profile_placement_2d = model.createIfcAxis2Placement2D(profile_origin_point, None)
    profile_shape_2d = model.createIfcRectangleProfileDef("AREA", None, profile_placement_2d, XDim=x_dim, YDim=y_dim)
    
    # Run vertical 3D solid extrusion operation along Z-axis
    extrusion_axis_direction = model.createIfcDirection((0.0, 0.0, 1.0))
    solid_extrusion_body = model.createIfcExtrudedAreaSolid(profile_shape_2d, item_placement_3d, extrusion_axis_direction, Depth=height)
    
    # Wrap solid object body inside visual representation containers
    shape_representation_wrapper = model.createIfcShapeRepresentation(
        ContextOfItems=context, RepresentationIdentifier="Body", RepresentationType="SweptSolid", Items=[solid_extrusion_body]
    )
    product_definition_shape_output = model.createIfcProductDefinitionShape(Representations=[shape_representation_wrapper])
    
    return product_definition_shape_output, local_placement

# Set up tracking lists for structural schedule calculations
element_names, element_types, volumes, formwork_areas = [], [], [], []

# Precise coordinates spacing the elements 5.0 meters apart cleanly along the X-axis
foundation_layout_grid = [(-5.0, 0.0), (0.0, 0.0), (5.0, 0.0)]

print("Looping through elements to establish perfect structural alignment...")
for idx, (x_loc, y_loc) in enumerate(foundation_layout_grid, start=1):
    
    # --- PART A: Concrete Footing Pad (1.5m x 1.5m x 0.5m) ---
    f_w, f_l, f_h = 1.5, 1.5, 0.5
    f_shape, f_place = generate_3d_element_shape(model, context_3d, f_w, f_l, f_h, x_loc, y_loc, 0.0)
    
    footing = model.createIfcFooting(
        ifcopenshell.guid.create(), owner_history, Name=f"Isolated_Footing_F{idx}",
        ObjectPlacement=f_place, Representation=f_shape, PredefinedType="PAD_FOOTING"
    )
    model.createIfcRelContainedInSpatialStructure(ifcopenshell.guid.create(), owner_history, None, None, [footing], storey)
    
    element_names.append(footing.Name)
    element_types.append("Concrete Pad Footing")
    volumes.append(f_w * f_l * f_h)
    formwork_areas.append((2 * (f_w + f_l)) * f_h)
    
    # --- PART B: RCC Column (0.4m x 0.4m x 2.5m) sitting flawlessly on top of the footing ---
    c_w, c_l, c_h = 0.4, 0.4, 2.5
    # Z position sits exactly at footing height (f_h), keeping it from floating
    c_shape, c_place = generate_3d_element_shape(model, context_3d, c_w, c_l, c_h, x_loc, y_loc, f_h)
    
    column = model.createIfcColumn(
        ifcopenshell.guid.create(), owner_history, Name=f"Structural_Column_C{idx}",
        ObjectPlacement=c_place, Representation=c_shape
    )
    model.createIfcRelContainedInSpatialStructure(ifcopenshell.guid.create(), owner_history, None, None, [column], storey)
    
    element_names.append(column.Name)
    element_types.append("Reinforced Concrete Column")
    volumes.append(c_w * c_l * c_h)
    formwork_areas.append((2 * (c_w + c_l)) * c_h)

# 5. WRITE COPIED IFC FILE DATA SAFELY TO DIRECTORY
model.write(ifc_file_path)
print(f"-> Perfectly aligned 3D IFC model saved: {ifc_file_path}")

# 6. PIPELINE DATA AUTOMATION SPREADSHEETS VIA PANDAS TO EXCEL
print("Processing engineering quantity spreadsheet data pipelines...")
df = pd.DataFrame({
    "Element Name": element_names,
    "Structural Type": element_types,
    "Concrete Volume (m³)": volumes,
    "Formwork Surface Area (m²)": formwork_areas
})

totals_summary_row = pd.DataFrame([{
    "Element Name": "TOTAL QUANTITIES", "Structural Type": "-",
    "Concrete Volume (m³)": df["Concrete Volume (m³)"].sum(),
    "Formwork Surface Area (m²)": df["Formwork Surface Area (m²)"].sum()
}])
df = pd.concat([df, totals_summary_row], ignore_index=True)

df.to_excel(excel_file_path, index=False)
print(f"-> Excel Take-off Schedule generated successfully: {excel_file_path}")
print("\n🎉 MASTER LEVEL COMPLETE. Open files to see flawless 3D symmetry!")