import ifcopenshell
import ifcopenshell.template

# Force the library to use your local version's unique ID settings
ifcopenshell.guid.create = ifcopenshell.guid.new

# 1. Initialize a clean IFC4 project template
model = ifcopenshell.template.create(
    "IFC4", 
    "C:/Users/malot/OneDrive/Desktop/Bim_automation/my_fresh_wall_model.ifc"
)

# Extract the root project container and owner records
project = model.by_type("IfcProject")[0]
owner_history = model.by_type("IfcOwnerHistory")[0]

# 2. Build the structural levels (Site -> Building -> Floor Storey)
site = model.createIfcSite(ifcopenshell.guid.create(), owner_history, Name="Project Site")
building = model.createIfcBuilding(ifcopenshell.guid.create(), owner_history, Name="Residential Tower")
storey = model.createIfcBuildingStorey(ifcopenshell.guid.create(), owner_history, Name="First Floor", Elevation=0.0)

# Connect the structural layers together 
model.createIfcRelAggregates(ifcopenshell.guid.create(), owner_history, "ProjectToSite", None, project, [site])
model.createIfcRelAggregates(ifcopenshell.guid.create(), owner_history, "SiteToBuilding", None, site, [building])
model.createIfcRelAggregates(ifcopenshell.guid.create(), owner_history, "BuildingToStorey", None, building, [storey])

# 3. DEFINE THE 3D POSITION AND GEOMETRY
# Here we define 'origin' FIRST so Python knows what it is!
origin = model.createIfcAxis2Placement3D(
    model.createIfcCartesianPoint((0.0, 0.0, 0.0)), None, None
)

# Set the 2D profile thickness (0.2m) and length (5.0m)
profile_origin = model.createIfcAxis2Placement2D(
    model.createIfcCartesianPoint((0.0, 0.0)), None
)
rectangle_profile = model.createIfcRectangleProfileDef(
    "AREA", None, profile_origin, XDim=5.0, YDim=0.2
)

# Extrude the 2D rectangle profile upward by 3.0 meters along the Z-axis
direction = model.createIfcDirection((0.0, 0.0, 1.0))
extruded_solid = model.createIfcExtrudedAreaSolid(
    rectangle_profile, origin, direction, Depth=3.0
)

# Package the geometry representation layers properly for rendering
shape_representation = model.createIfcShapeRepresentation(
    ContextOfItems=model.by_type("IfcGeometricRepresentationContext")[0],
    RepresentationIdentifier="Body",
    RepresentationType="SweptSolid",
    Items=[extruded_solid]
)
product_definition = model.createIfcProductDefinitionShape(
    Representations=[shape_representation]
)

# 4. Create the physical Wall entity and connect its 3D shape structure
wall = model.createIfcWall(
    ifcopenshell.guid.create(), 
    owner_history, 
    Name="Main_Structural_Wall", 
    ObjectPlacement=origin, 
    Representation=product_definition
)

# Map the wall to the First Floor spatial location
model.createIfcRelContainedInSpatialStructure(
    ifcopenshell.guid.create(), owner_history, "FloorToWall", None, [wall], storey
)

# 5. Save the file cleanly to your local desktop folder paths
model.write("C:/Users/malot/OneDrive/Desktop/Bim_automation/my_fresh_wall_model.ifc")
print("Success! Your brand new 3D Wall file has been created completely.")