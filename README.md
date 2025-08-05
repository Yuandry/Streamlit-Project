# Streamlit-Project

Traffic Accident Data Analysis Dashboard

Streamlit App link:https://yuandry-streamlit-project-stream-txqcpc.streamlit.app/



Project Overview
This is an interactive web application built with Python and Streamlit that allows users to explore traffic accident data through visualizations, filters, and data analysis tools. The goal is to help users understand accident trends and spatial distribution more easily.

Key Features:
Date Range Selection
Users can select a custom date range to filter accident records within a specific period.

Filtered Data Table
After filtering, a table shows detailed accident data including:

Date

GPS coordinates (X and Y)

Number of Deaths

Number of Injuries

Accident Density Map (Pydeck)
Displays a map of accident locations using Kernel Density Estimation (KDE). Density is color-coded:

Green = Low

Red = High

Purple = Extreme Hotspot

Casualty Trends Over Time
Users can view a time series line chart of either:

Deaths over time

Injuries over time

Technologies Used:
streamlit – for building the interactive web interface

pandas – for data processing

numpy – for numerical operations

scikit-learn – for Kernel Density Estimation

pydeck – for rendering interactive maps

 File Structure:
.
├── STREAM.py              # Main Streamlit application script

├── OpenData.csv           # Source dataset (CSV format)

├── requirements.txt       # Python dependencies

└── README.md              # Project documentation

How to Run Locally:
pip install -r requirements.txt
streamlit run STREAM.py
