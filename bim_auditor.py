import ifcopenshell
import pandas as pd
import os

def audit_bim_model(ifc_file_path, report_excel_path):
    if not os.path.exists(ifc_file_path):
        print(f"❌ Error: Could not find '{ifc_file_path}'")
        return

    print("🔄 Loading model for quality check...")
    model = ifcopenshell.open(ifc_file_path)
    elements = model.by_type("IfcColumn")
    
    error_log = []
    
    print("🕵️‍♂️ Scanning columns for engineering compliance...")
    for element in elements:
        name = element.Name if element.Name else ""
        global_id = element.GlobalId
        
        # Rule 1: Check if the element name is completely empty
        if name == "":
            error_log.append({
                "GlobalID": global_id,
                "Element_Type": element.is_a(),
                "Current_Name": "MISSING NAME",
                "Issue_Found": "Critical: Component name is blank in the BIM model."
            })
            
        # Rule 2: Check if structural material label is missing from the name
        elif "Concrete" not in name and "Steel" not in name:
            error_log.append({
                "GlobalID": global_id,
                "Element_Type": element.is_a(),
                "Current_Name": name,
                "Issue_Found": "Warning: Name lacks material classification ('Concrete' or 'Steel')."
            })

    # If errors are found, export them to a clean spreadsheet
    if error_log:
        df = pd.DataFrame(error_log)
        df.to_excel(report_excel_path, index=False)
        print(f"⚠️ Audit complete! Found {len(error_log)} issues.")
        print(f"📋 Error report generated cleanly at: {report_excel_path}")
    else:
        print("✅ Success! Every column passed the structural compliance check.")

if __name__ == "__main__":
    audit_bim_model("sample_model.ifc", "BIM_Audit_Report.xlsx")