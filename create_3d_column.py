import ifcopenshell
import ifcopenshell.template

# 1. Initialize a blank IFC file with a standard coordinate system
model = ifcopenshell.template.create(
    schema="IFC4", 
    filename="C:/Users/malot/OneDrive/Desktop/Bim_automation/3d_column_project.ifc"
)

# 2. Set up the absolute basic project structure
project = model.by_type("IfcProject")[0]
owner_history = model.by_type("IfcOwnerHistory")[0]

# Create a physical site and a building structure container
site = model.createIfcSite(ifcopenshell.guid.create(), owner_history, Name="Project Site")
building = model.createIfcBuilding(ifcopenshell.guid.create(), owner_history, Name="Structural Tower")
storey = model.createIfcBuildingStorey(ifcopenshell.guid.create(), owner_history, Name="Ground Floor", Elevation=0.0)

# Link the folder layers together using relationship glue
model.createIfcRelAggregates(ifcopenshell.guid.create(), owner_history, "ProjectToSite", None, project, [site])
model.createIfcRelAggregates(ifcopenshell.guid.create(), owner_history, "SiteToBuilding", None, site, [building])
model.createIfcRelAggregates(ifcopenshell.guid.create(), owner_history, "BuildingToStorey", None, building, [storey])

# 3. DEFINE THE 3D GEOMETRY RECOGNITION (This is the trick to show the 3D model!)
# Create point origins (0,0,0)
origin = model.createIfcAxis2Placement3D(
    model.createIfcCartesianPoint((0.0, 0.0, 0.0)), None, None
)

# Create a 2D profile square (500mm x 500mm concrete column profile)
profile_origin = model.createIfcAxis2Placement2D(
    model.createIfcCartesianPoint((0.0, 0.0)), None
)
rectangle = model.createIfcRectangleProfileDef(
    "AREA", None, profile_origin, XDim=0.5, YDim=0.5
)

# Extrude that 2D square upward on the Z-axis by 3.0 meters to make it a 3D block
direction = model.createIfcDirection((0.0, 0.0, 1.0))
extruded_solid = model.createIfcExtrudedAreaSolid(
    rectangle, origin, direction, Depth=3.0
)

# Wrap that solid shape inside a visual product representation layer
shape_representation = model.createIfcShapeRepresentation(
    ContextOfItems=model.by_type("IfcGeometricRepresentationContext")[0],
    RepresentationIdentifier="Body",
    RepresentationType="SweptSolid",
    Items=[extruded_solid]
)
product_definition = model.createIfcProductDefinitionShape(
    Representations=[shape_representation]
)

# 4. Create the physical Column and attach the 3D shape to it!
column = model.createIfcColumn(
    ifcopenshell.guid.create(), 
    owner_history, 
    Name="C1_Concrete_Column", 
    ObjectPlacement=origin, 
    Representation=product_definition
)

# Group the column into the Ground Floor layout structure
model.createIfcRelContainedInSpatialStructure(
    ifcopenshell.guid.create(), owner_history, "FloorToColumn", None, [column], storey
)

# Save the file cleanly to your folder path context
model.write()
print("Success! Your 3D Column Project has been generated.")