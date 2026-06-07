import ifcopenshell
import ifcopenshell.template

# Force the library's internal GUID system to align with your local installation version
ifcopenshell.guid.create = ifcopenshell.guid.new

# Initialize a standard, fully configured IFC4 project template with geometric rendering contexts
model = ifcopenshell.template.create(
    "IFC4", 
    "C:/Users/malot/OneDrive/Desktop/Bim_automation/my_3d_wall_project.ifc"
)

# Extract the pre-configured project container and owner records
project = model.by_type("IfcProject")[0]
owner_history = model.by_type("IfcOwnerHistory")[0]
geo_context = model.by_type("IfcGeometricRepresentationContext")[0]

# Build your nested spatial tree nodes safely
site = model.createIfcSite(ifcopenshell.guid.create(), owner_history, Name="Project Site")
building = model.createIfcBuilding(ifcopenshell.guid.create(), owner_history, Name="Residential Tower")
storey = model.createIfcBuildingStorey(ifcopenshell.guid.create(), owner_history, Name="First Floor", Elevation=0.0)

# Glue the project spatial hierarchy containers together
model.createIfcRelAggregates(ifcopenshell.guid.create(), owner_history, "ProjectToSite", None, project, [site])
model.createIfcRelAggregates(ifcopenshell.guid.create(), owner_history, "SiteToBuilding", None, site, [building])
model.createIfcRelAggregates(ifcopenshell.guid.create(), owner_history, "BuildingToStorey", None, building, [storey])

# --- FROM HERE DOWN, YOUR EXISTING GEOMETRY & EXTRUSION LINES CONTINUE EXACTLY THE SAME ---

# Create a 2D rectangle profile for the wall thickness and length
# Wall thickness = 0.2 meters (200mm), Wall length = 5.0 meters
profile_origin = model.createIfcAxis2Placement2D(
    model.createIfcCartesianPoint((0.0, 0.0)), None
)
rectangle_profile = model.createIfcRectangleProfileDef(
    "AREA", None, profile_origin, XDim=5.0, YDim=0.2
)

# Extrude that 2D rectangle upward on the Z-axis by 3.0 meters to make a 3D block wall
direction = model.createIfcDirection((0.0, 0.0, 1.0))
extruded_solid = model.createIfcExtrudedAreaSolid(
    rectangle_profile, origin, direction, Depth=3.0
)

# Package the 3D solid geometry into a format IFC understands
shape_representation = model.createIfcShapeRepresentation(
    ContextOfItems=model.by_type("IfcGeometricRepresentationContext")[0],
    RepresentationIdentifier="Body",
    RepresentationType="SweptSolid",
    Items=[extruded_solid]
)
product_definition = model.createIfcProductDefinitionShape(
    Representations=[shape_representation]
)

# 4. Create the physical IfcWall object and attach the 3D shape to it
wall = model.createIfcWall(
    ifcopenshell.guid.create(), 
    owner_history, 
    Name="Main_Structural_Wall", 
    ObjectPlacement=origin, 
    Representation=product_definition
)

# Group the wall into the First Floor layout structure
model.createIfcRelContainedInSpatialStructure(
    ifcopenshell.guid.create(), owner_history, "FloorToWall", None, [wall], storey
)

# 5. Save the file cleanly
# Change your old model.write() to this version:
model.write("C:/Users/malot/OneDrive/Desktop/Bim_automation/my_3d_wall_project.ifc")
print("Success! Your 3D Wall Project has been generated.")