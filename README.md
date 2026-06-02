# BIM Data Engineering & Automation Suite (Python & IFC)

A comprehensive repository of functional Python data engineering utilities designed to parse, audit, map, and calculate material requirements directly from Industry Foundation Classes (IFC) structural databases.

## 🛠️ Tech Stack
- **Language:** Python 3.11
- **Libraries:** IfcOpenShell, Pandas, OpenPyXL
- **Environment:** VS Code, Git & GitHub

---

## 🚀 core Engineering Utilities

### 1. Automated Material Takeoff (MTO) Engine (`skyscraper_mto.py`)
- Simulates real-world procurement workflows by calculating concrete volumes and mass distributions across multi-story developments.
- Accounts for load-bearing optimizations (e.g., varying structural slab thicknesses across lower vs. upper levels).
- Generates a polished procurement spreadsheet (`Skyscraper_Material_Takeoff_Schedule.xlsx`) including total aggregated material orders ready for supply chain processing.

### 2. Multi-Level Structural Analytics Framework (`skyscraper_suite.py`)
- Scans spatial containment trees to map the allocation of load-bearing assets (Walls, Columns, Slabs) across individual elevations (`IfcBuildingStorey`).
- Compiles an inventory dashboard for project managers to monitor component density distributions.

### 3. Spatial Relationship Mapper (`bim_spatial_mapper.py`)
- Analyzes structural containment and boundary matrices (`IfcRelSpacesBoundary`).
- Automatically maps architectural boundaries, linking room spaces (`IfcSpace`) directly to their structural door assignments (`IfcDoor`).

### 4. Automated Compliance Auditor (`bim_auditor.py`)
- Acts as an automated quality-control checker parsing structural data grids for compliance missing fields.
- Flags unassigned material classifications or missing naming conventions, logging anomalies into an error spreadsheet.

### 5. Core Data Extractor (`bim_extractor.py`)
- Parses IFC models to isolate specific elements like `IfcColumn` and outputs clean, structured property grids.
