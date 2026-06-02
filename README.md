# Bengaluru Rental Analytics Dashboard

## Overview
A recruiter-ready analytics notebook built to analyze Bengaluru housing listings and rental trends. The project focuses on premium vs affordable neighborhoods, price-per-sqft segmentation, BHK pricing analysis, and SQL-backed insights for Bengaluru internship screening.

## Dataset
- **Source file**: `Bengaluru_House_Data.csv.xls`
- **Cleaned export**: `bengaluru_cleaned_data.csv`
- **SQLite database**: `bengaluru_housing.db`

## Tech Stack
- Python
- pandas
- NumPy
- matplotlib
- seaborn
- SQLite

## Key Features
- Data cleaning and type conversion for Bengaluru housing listings
- Feature engineering for `BHK` and `price_per_sqft`
- Premium and affordable location analysis
- BHK pricing trends and demand distribution
- SQL analytics using SQLite for internship-level signal
- Recruiter-friendly structure with business insights

## Key Insights
- Premium Bengaluru neighborhoods are driven by high price-per-sqft rather than absolute price
- Affordable pockets exist, which is useful for budget-conscious decision making
- Price per sqft is a stronger investment signal than raw price alone
- Listing counts reveal demand hubs, important for location strategy in startups

## Screenshots
- `bengaluru_screenshots/kpi_summary_table.png`
- `bengaluru_screenshots/premium_locations_chart.png`
- `bengaluru_screenshots/affordable_locations_chart.png`
- `bengaluru_screenshots/bhk_price_chart.png`

## Project Structure
- `bengaluru_rental_analytics_dashboard.ipynb` — main notebook
- `Bengaluru_House_Data.csv.xls` — raw dataset
- `bengaluru_cleaned_data.csv` — cleaned dataset export
- `bengaluru_housing.db` — SQLite database of cleaned data
- `bengaluru_screenshots/` — visual outputs

## Future Improvements
- Add clustering and segmentation for location-level insights
- Bring in external Bengaluru geography features such as metro proximity
- Deploy an interactive dashboard with Streamlit or Dash
- Include map visualizations and more structured SQL analytics
