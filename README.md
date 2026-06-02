# BIM Automation Toolkit (Python & IFC)

A collection of functional Python data engineering utilities designed to parse, audit, and map structural component data from Industry Foundation Classes (IFC) BIM models.

## 🛠️ Tech Stack
- **Language:** Python 3.11
- **Libraries:** IfcOpenShell, Pandas, OpenPyXL
- **Environment:** VS Code, Git & GitHub

## 🚀 Included Utilities

### 1. BIM Data Extractor (`bim_extractor.py`)
- Automatically parses the IFC database for structural components (`IfcColumn`).
- Extracts engineering properties (`GlobalID`, `Name`, `Type`) and cleanly exports them to an organized Excel schedule.

### 2. Automated Model Auditor (`bim_auditor.py`)
- Acts as an automated quality-control script scanning for engineering compliance.
- Automatically flags missing names or elements lacking material classifications ("Concrete"/"Steel") and logs them into a flagged error report.

### 3. Spatial Relationship Mapper (`bim_spatial_mapper.py`)
- Analyzes spatial containment and boundary matrices (`IfcRelSpacesBoundary`).
- Automatically maps architectural boundaries, linking specific room numbers (`IfcSpace`) directly to their corresponding physical door elements (`IfcDoor`) in a master Excel layout.
