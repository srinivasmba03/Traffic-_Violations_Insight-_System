# Traffic Violations Analytics Project

## Overview

This project provides an end-to-end Traffic Violations Analytics solution consisting of:

1. **Data Cleaning & ETL (Extract Transform Load) Notebook** (`Traffic_Violations.ipynb`)
2. **Interactive Streamlit Dashboard** (`appnew.py`)
3. **MySQL Database Backend**
4. **Geospatial and Statistical Analytics**

The solution is designed to clean, standardize, analyze, store, and visualize traffic violation records for law enforcement, transportation departments, and data analysts.

---

# Project Architecture

```text
Traffic_Violations.csv
        |
        v
Traffic_Violations.ipynb
(Data Cleaning & Transformation)
        |
        v
MySQL Database
traffic_violations
        |
        v
Streamlit Dashboard (appnew.py)
        |
        +--> KPI Metrics
        +--> Trend Analysis
        +--> Demographic Analysis
        +--> Vehicle Analysis
        +--> Geographic Heatmaps
        +--> High-Risk Zone Detection
```

---

# Files Included

## 1. Traffic_Violations.ipynb

Jupyter Notebook responsible for:

- Data ingestion
- Data cleaning
- Data standardization
- Feature engineering
- Exploratory Data Analysis (EDA)
- Statistical reporting
- Database preparation

### Main Operations

#### Data Loading

Reads traffic violation records from:

```python
Traffic_Violations.csv
```

and loads them into a Pandas DataFrame.

---

#### Database Connection

Connects to MySQL using SQLAlchemy.

Example:

```python
mysql+mysqldb://root:<password>@localhost:3306/traffic_violations
```

---

#### Data Cleaning

##### SeqID Validation

- Converts SeqID to string.
- Detects duplicates.
- Removes duplicate records.
- Preserves unique identifiers.

##### Date Of Stop Cleaning

- Converts dates to proper datetime format.
- Handles mixed date formats.
- Removes invalid/future dates.
- Standardizes date values.

##### Time Of Stop Cleaning

Converts inconsistent time values such as:

```text
23.11.00
16.41.00
```

to:

```text
23:11:00
16:41:00
```

##### Agency Standardization

- Converts values to uppercase.
- Removes extra spaces.
- Replaces null-like values with UNKNOWN.

##### SubAgency Cleaning

- Standardizes formatting.
- Removes spacing issues.
- Extracts district numbers.
- Creates:

```python
District_Number
```
column.

##### Description Cleaning

Standardizes text and categorizes violations into groups such as:

- Speeding
- Registration
- License
- Insurance
- Seat Belt
- Other

---

### Feature Engineering

The notebook creates analytical features including:

| Feature | Description |
|----------|------------|
| Year | Year of stop |
| Month | Month name |
| Weekday | Day of week |
| Hour | Hour of stop |
| District_Number | Extracted district |

---

### Exploratory Data Analysis

#### Most Common Violations

Identifies:

- Top violation categories
- Violation frequencies
- Distribution statistics

#### High Incident Locations

Analyzes:

- Most frequent violation locations
- Geographic hotspots
- Coordinate clustering

#### Demographic Analysis

Studies relationships between:

- Race vs Violation Type
- Gender vs Violation Type

using heatmaps and cross-tabulations.

#### Time-Based Analysis

Investigates:

- Violations by hour
- Violations by weekday
- Violations by month

to identify temporal patterns.

---

# 2. Streamlit Dashboard (appnew.py)

Interactive analytics dashboard built using Streamlit.

### Technologies Used

- Streamlit
- Pandas
- NumPy
- SQLAlchemy
- Plotly
- Matplotlib
- Seaborn
- Folium
- Streamlit-Folium

---

## Dashboard Features

### Database Integration

Data is loaded directly from MySQL:

```sql
traffic_violations
```

table.

Selected fields:

- Date Of Stop
- Location
- VehicleType
- Gender
- Race
- Violation Type
- Accident
- Make
- Model
- Latitude
- Longitude

---

### Sidebar Filters

Users can dynamically filter records by:

- Date Range
- Location
- Vehicle Type
- Gender
- Race
- Violation Category

All dashboard visualizations update automatically.

---

### KPI Metrics

Displays key indicators:

#### Total Violations

Total filtered violation records.

#### Accident Violations

Number of violations involving accidents.

#### High Risk Zone

Location with highest number of violations.

#### Top Vehicle Make

Most common vehicle manufacturer.

#### Top Vehicle Model

Most common vehicle model.

---

### Violation Trend Analysis

Monthly trend visualization showing:

- Growth patterns
- Seasonal fluctuations
- Long-term behavior

Implemented using Plotly line charts.

---

### Violation Category Analysis

Displays:

- Top violation categories
- Relative frequencies
- Violation concentration

using interactive bar charts.

---

### Vehicle Analytics

#### Top Vehicle Types

Shows:

- Most cited vehicle types
- Vehicle distribution

using Seaborn count plots.

#### Top Vehicle Makes

Displays leading vehicle manufacturers involved in violations.

#### Top Vehicle Models

Shows most frequent vehicle models.

---

### Demographic Analytics

#### Race Distribution

Interactive pie chart displaying racial distribution of violations.

#### Gender Distribution

Bar chart showing gender-based violation counts.

---

### Geographic Analytics

#### Incident Heatmap

Uses Folium HeatMap to visualize:

- Traffic violation density
- Geographic hotspots
- Concentrated risk areas

Coordinates used:

```text
Latitude
Longitude
```

---

### High Risk Zones

Ranks locations by:

- Number of violations
- Relative risk level

and visualizes them through horizontal bar charts.

---

### Raw Data Viewer

Provides:

- Paginated records
- Interactive table
- Filtered dataset inspection

for analysts and auditors.

---

# Database Schema

Expected database:

```sql
traffic_violations
```

Example fields:

```text
Date Of Stop
Time Of Stop
Location
VehicleType
Gender
Race
Violation Type
Accident
Personal Injury
Property Damage
Make
Model
Latitude
Longitude
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
cd traffic-violations-project
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```


## Install Dependencies

```bash
pip install -r requirements.txt
```

Suggested packages:

```text
streamlit
pandas
numpy
sqlalchemy
pymysql
mysqlclient
matplotlib
seaborn
plotly
folium
streamlit-folium
jupyter
```

---

# Running the Notebook

```bash
jupyter notebook
```

Open:

```text
Traffic_Violations.ipynb
```

Run all cells sequentially.

---

# Running the Dashboard

```bash
streamlit run appnew.py
```

Default URL:

```text
http://localhost:8501
```

---

# Key Business Insights Supported

The project enables organizations to:

- Identify high-risk traffic zones.
- Detect violation hotspots.
- Monitor monthly violation trends.
- Understand demographic patterns.
- Analyze vehicle-related trends.
- Support public safety initiatives.
- Improve traffic enforcement strategies.
- Generate data-driven operational decisions.

---

# Author

Traffic Violations Analytics Dashboard & Data Engineering Project
