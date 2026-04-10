# Automated Reporting Pipeline

A Python-based script designed to automate retail sales reporting. This tool streamlines the end-to-end process from raw data ingestion to the generation of business-ready insights.

## Key Features

* Data Preparation: Cleans and preprocesses raw sales data from CSV files.

* KPI Calculation: Computes total revenue, average ticket size, Month-over-Month (MoM) growth, and average discount rates.

* Performance Tracking: Identifies top-performing products, stores, and categories.

* Visual Analytics: Automatically generates 4 charts for the final report.

* Multi-Tab Export: Produces a comprehensive Excel workbook with 6 dedicated tabs, saved to the outputs/ directory.

## Project Structure

```
automated-reporting-pipeline/
├── run.py             # Main entry point: executes the full workflow
├── pipeline.py        # Core data processing and metric logic
├── generate_data.py   # Utility to create synthetic sales data for testing
└── requirements.txt
```

## Installation & Usage

```bash
pip install -r requirements.txt
python run.py
```

Note: If data/sales.csv is not present, the script will automatically generate a sample dataset.

## Core KPIs
The script automates the tracking of several critical business metrics:

* Total Revenue: Aggregate sales and revenue broken down by time period.

* Average Ticket: The mean transaction value per customer.

* MoM Growth: Percentage change in revenue compared to the previous month.

* Average Discount: The mean percentage of discount applied across transactions.

* Rankings: Performance leaderboards for stores, products, and categories.

## Tech Stack

Python · Pandas · NumPy · Matplotlib · OpenPyXL
