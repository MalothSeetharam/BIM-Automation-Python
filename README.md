# BIM Automation & Virtual Design and Construction (VDC) Portfolio

Welcome to my professional engineering repository. This space showcases production-ready Python engines, openBIM data pipelines, and automated quantity takeoff workflows designed to eliminate manual tracking errors and bridge 3D modeling environments directly with financial procurement.

---

## 🚀 Project 1: Parametric Foundations Generator & Automated Quantity Takeoff Engine (IFC4)

An independent, object-oriented Python automation engine built to programmatically compile standard-compliant 3D structural foundation networks completely from a blank file state. 

### 🔑 Key Features
- **Raw IFC4 Compilation:** Bypasses software translation bugs by generating custom geometric contexts, unit assignments, and structural spatial trees directly from a blank state using `IfcOpenShell`.
- **Parametric Symmetrical Geometry:** Positions columns flawlessly on the center lines of footings without geometric drift.
- **Automated Quantity Takeoff (QTO):** Computes exact concrete volumes ($m^3$) and perimeter formwork surface areas ($m^2$) for structural elements inside programmatic execution loops.
- **Pandas Data Pipeline:** Automatically extracts geometry metadata out of the backend BIM engine to synthesize clean Bill of Quantities (BOQ) Excel spreadsheets with integrated summary total calculation matrices.

### 📦 Generated Project Outputs
1. `expert_foundation_project.ifc`: A complete, standard-compliant 3D architectural model featuring isolated pad footings and symmetrical vertical concrete columns.
2. `structural_quantity_takeoff.xlsx`: A spreadsheet calculation matrix detailing concrete volumes ($m^3$) and formwork surface requirements ($m^2$) broken down by structural elements.

### 📊 Takeoff Data Preview (Sample Material Output)
| Element ID | Structural Element Type | Concrete Volume ($m^3$) | Formwork Area ($m^2$) | Procurement Status |
| :--- | :--- | :--- | :--- | :--- |
| `IfcFooting_F1` | Isolated Pad Footing | 1.125 | 3.00 | Ready for Order |
| `IfcColumn_C1` | Reinforced Concrete Column | 0.400 | 4.00 | Ready for Order |
| **TOTALS** | **Structural Foundation Set** | **1.525 $m^3$** | **7.00 $m^2$** | **Summary Compiled** |

---

## 🌱 Project 2: Automated BIM Quantity Takeoff & Environmental Compliance Engine

An end-to-end data pipeline built to parse multi-story IFC structural databases, track dead-load variations, and flag environmental sustainability thresholds.

### 🔑 Key Features
- **Multi-Story Parsing:** Automates Material Take-Off (MTO) extractions from concrete structural elements across multiple floor levels simultaneously.
- **Structural Load Logic simulation:** Varies concrete slab thicknesses across floor levels and tracks volumetric distributions per `IfcBuildingStorey` to simulate dead-load reductions.
- **Environmental Compliance Baseline:** Built structural logic to support future environmental tracking modules to calculate embodied carbon (kg CO₂e) and energy metrics (MJ) mapped against LEED and Dubai Al Sa'fat green building standards.

---

## 🔧 Deep Technical Engineering Solves
* **Zero Coordinate Drift:** Overcame geometric distortion inside loop arrays by anchoring independent 3D tracking placement systems (`IfcAxis2Placement3D`) and custom Cartesian point vectors (`IfcCartesianPoint`).
* **Clean Database Spatial Trees:** Successfully linked foundational components to the root building model tree through precise assignment structures (`IfcRelAggregates` and `IfcRelContainedInSpatialStructure`).

## 💻 Tech Stack & Dependencies
- **Language:** Python 3.11+
- **Libraries:** IfcOpenShell, Pandas, OpenPyXL, ReportLab
- **Validation CAD Environment:** BIMvision (OpenBIM IFC Viewer)

## ⚙️ Execution Guide
Ensure dependencies are installed before execution:
```bash
pip install ifcopenshell pandas openpyxl reportlab
python expert_bim_project.py
