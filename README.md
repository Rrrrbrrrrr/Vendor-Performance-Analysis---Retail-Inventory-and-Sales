# Vendor Performance Analysis - Retail Inventory & Sales

## 📌 Overview
This project analyzes vendor performance using sales and purchase data to identify high-performing and low-performing vendors. 
The goal is to support better procurement decisions and optimize vendor selection.

---

## 🛠️ Tools & Technologies
- SQL (data extraction and joins)
- Python (Pandas, Matplotlib for EDA)
- Power BI (dashboard and visualization)

---

## 📂 Project Structure
vendor-performance-analysis - Retail Inventory & Sales/
  |-data/ # Cleaned dataset used for analysis
  |-images/ # Dashboard files and screenshots
     |-vendor_analysis_dashboard.pbix
     |-PowerBI_dashboard.png
  |-notebooks/ # Jupyter notebooks for EDA
     |-Exploratory Data Analysis.ipnyb # EDA using SQL
     |-Vendor Performance Analysi.ipnyb # vendor eda using python
  |-scripts/ # Python scripts for data processing
     |-get_vendor_summary.py
     |-ingestion_db.py

 README.md


---

## ⚙️ Workflow
1. Data ingestion from multiple vendor tables using SQL  
2. Data cleaning and transformation using Python  
3. Merging multiple datasets into a single analysis-ready dataset  
4. Exploratory Data Analysis (EDA) to identify trends and patterns  
5. Visualization and dashboard creation using Power BI  

---

## 📊 Key Insights
- A small percentage of vendors contribute to a large share of total purchases  
- Identified underperforming vendors with low contribution  
- Vendor contribution trends help in optimizing procurement strategy  

---

## 📜 Scripts
- `ingestion_db.py` → Loads raw data into database  
- `get_vendor_summary.py` → Generates vendor performance summary  

---

## 📷 Dashboard
Power BI dashboard showing vendor contribution and performance insights:

---

## 👤 Author
Rakesh Bera
