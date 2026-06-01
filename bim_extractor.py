import ifcopenshell
import pandas as pd
import os

def extract_bim_data(ifc_file_path, output_excel_path):
    if not os.path.exists(ifc_file_path):
        print(f"❌ Error: Could not find '{ifc_file_path}' in this folder.")
        return

    print("🔄 Step 1: Loading your 3D BIM text model into memory...")
    model = ifcopenshell.open(ifc_file_path)
    
    print("🔄 Step 2: Filtering the database for 'IfcColumn' components...")
    elements = model.by_type("IfcColumn")
    print(f"🎯 Found {len(elements)} columns in this model.")
    
    extracted_data = []
    
    print("🔄 Step 3: Extracting unique details from each column...")
    for element in elements:
        element_info = {
            "GlobalID": element.GlobalId,
            "Name": element.Name,
            "Type": element.is_a(),
        }
        extracted_data.append(element_info)
        
    print("🔄 Step 4: Translating the data array into an Excel grid layout...")
    df = pd.DataFrame(extracted_data)
    
    print("🔄 Step 5: Generating the final Excel spreadsheet file...")
    df.to_excel(output_excel_path, index=False)
    print(f"✅ Finished successfully! Your file is ready at: {output_excel_path}")

if __name__ == "__main__":
    INPUT_IFC = "sample_model.ifc"
    OUTPUT_EXCEL = "BIM_Column_Schedule.xlsx"
    
    extract_bim_data(INPUT_IFC, OUTPUT_EXCEL)