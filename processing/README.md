# 🔬 Processing - Analysis & Development Pipeline

**Purpose:** Organized workflow for data processing, analysis, model verification, and development

---

## 📁 Structure (Read in Numbered Order)

### **01_data_analysis/**
Initial data exploration and statistical analysis
- Flight, route, aircraft statistics
- LoadLocations and PieceInformation analysis
- Comprehensive data reports

### **02_infeasibility_analysis/**
Investigation of model infeasibilities
- Analysis of failed runs
- Gurobi log examination
- Feasibility comparison across models

### **03_heuristic_development/**
Development and testing of heuristics
- 3D-BPP extreme points
- Feedback loop improvements

### **04_visualization/**
Visualization generation and analysis
- 3D cargo visualizations
- Weight & balance plots

### **05_documentation/**
General project documentation
- Analysis summaries
- Methodology documentation

### **06_model_verification/** ⭐ NEW - BUG ANALYSIS
Comprehensive benchmark model verification
- **START HERE:** `reports/MASTER_BUG_MATRIX.md`
- 11 bugs found across 4 benchmark models
- Constraint-by-constraint comparison
- Model correctness verification

### **07_communications/** NEW - ADVISOR EMAILS
Communications with Professor Delgado
- Weekly progress reports
- Bug analysis reports
- **For sending:** `reports/EMAIL_RESUMEN_MEJORADO.txt`

### **08_analysis_scripts/** NEW - UTILITY SCRIPTS
Python utility scripts organized by function
- Analysis, checking, debugging, verification scripts
- Exploratory tools developed during project

### **99_archive/**
Old files and superseded documentation
- Old notebooks, docs, temporary files
- Keep for reference only

---

## 🎯 For Professor Delgado

**Recommended navigation:**

1. **06_model_verification/reports/MASTER_BUG_MATRIX.md**
   - See all 11 bugs at a glance

2. **06_model_verification/reports/BUGS_IN_[MODEL].md**
   - Deep dive into specific model bugs

3. **07_communications/reports/EMAIL_FINAL_PROFESOR.txt**
   - Complete pedagogical report

4. **01_data_analysis/reports/**
   - Data understanding and statistics

---

## 📊 Quick Facts

- **Total bugs found:** 11 across 4 benchmark models
- **Models analyzed:** Puttaert, Baseline, Optimized_Actual, BAX_Fixed
- **Reference model:** DelgadoVenezian (0 bugs ✅)
- **Documentation files:** 60+ organized across folders

---

**Last updated:** October 2025

