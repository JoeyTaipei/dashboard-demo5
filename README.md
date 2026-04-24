# MarTech_Dashboard

A deployed Streamlit dashboard for chocolate retail analysis, designed to make sales and marketing insights easy to understand for non-technical users.
link: https://dashboard-demo5-49bzop5jio6wyeqdlhhce3.streamlit.app/

## What This App Does

This dashboard turns raw transactional CSV data into an interactive MarTech reporting experience. It helps users quickly understand:

- overall revenue, profit, orders, and average order value
- sales trends over time
- YoY, MoM, and QoQ growth movement
- customer behavior and RFM segmentation
- brand positioning and brand growth comparison
- product, channel, country, and city performance

## Main Dashboard Sections

- `Executive KPIs`
  Includes top-level business metrics and a plain-English summary for non-marketers.

- `Sales Trends`
  Shows monthly and weekly revenue and profit trends.

- `YoY MoM QoQ`
  Tracks growth movement and compares brand-level sales growth on one chart.

- `Customer Analytics`
  Covers loyalty, new vs returning customers, demographics, and RFM segments.

- `Brand Positioning`
  Scores each brand across key positioning attributes and plots a positioning map.

- `Product & Brand Performance`
  Compares category and brand sales performance.

- `Channel & Geo`
  Breaks performance down by store type, country, and city.

## Data Sources

The app reads directly from CSV files stored in the `data/` folder:

- `sales.csv`
- `customers.csv`
- `products.csv`
- `stores.csv`
- `calendar.csv`

## Tech Stack

- `Streamlit`
- `pandas`
- `Plotly`

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project Files

- `app.py` - main dashboard application
- `requirements.txt` - Python dependencies
- `data/` - source CSV files

## Notes

- The dashboard is deployed on Streamlit Community Cloud.
- The app reads directly from source CSV files, so first load may take a bit longer because `sales.csv` is relatively large.
- This repository is intended for demo, analysis, and dashboard presentation purposes.
