import ifcopenshell
import pandas as pd
import os

def generate_spatial_door_report(ifc_file_path, output_excel_path):
    if not os.path.exists(ifc_file_path):
        print(f"❌ Error: Cannot find '{ifc_file_path}'")
        return

    print("🔄 Loading 3D model database layout...")
    model = ifcopenshell.open(ifc_file_path)
    
    # Grab all room spaces in the model
    rooms = model.by_type("IfcSpace")
    
    mapping_data = []
    print("🕵️‍♂️ Scanning space boundary matrices for doors...")

    for room in rooms:
        room_name = room.Name if room.Name else "Unnamed Room"
        room_desc = room.Description if room.Description else "No Description"
        
        # Look for relationship boundary connections attached to this room
        found_door = False
        if hasattr(room, "BoundedBy"):
            for boundary in room.BoundedBy:
                # Check if the boundary relation points to a physical element
                related_element = boundary.RelatedBuildingElement
                
                if related_element and related_element.is_a("IfcDoor"):
                    mapping_data.append({
                        "Room_Name": room_name,
                        "Room_Purpose": room_desc,
                        "Connected_Door_ID": related_element.GlobalId,
                        "Door_Label": related_element.Name
                    })
                    found_door = True
        
        # If a room has no door linked, log it as an issue
        if not found_door:
            mapping_data.append({
                "Room_Name": room_name,
                "Room_Purpose": room_desc,
                "Connected_Door_ID": "ALERT",
                "Door_Label": "Missing physical door assignment!"
            })

    # Export structured array to Excel
    df = pd.DataFrame(mapping_data)
    df.to_excel(output_excel_path, index=False)
    print(f"✅ Mapping Success! File generated at: {output_excel_path}")

if __name__ == "__main__":
    generate_spatial_door_report("sample_model.ifc", "BIM_Room_Door_Schedule.xlsx")