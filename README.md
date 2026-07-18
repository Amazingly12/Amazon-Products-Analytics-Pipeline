# Amazon Products Analytics Pipeline

> An end-to-end data pipeline that scrapes, cleans, stores, and visualizes Amazon product data across 9 categories from raw HTML to interactive Tableau dashboards.

---

## Navigate through the README file.

<p align="center">
  <a href="#data-architecture"><b>Data Architecture</b></a> |  
  <a href="#installation-and-setup"><b>Installation and Setup</b></a> | 
  <a href="#project-structure"><b>Project Structure</b></a> | 
  <a href="#key-insights"><b>Key Insights</b></a> | 
  <a href="#dashboards"><b>Dashboards</b></a>
</p>

---

## Data Architecture

![Pipeline Architecture](Pipeline_Architecture.png)

The pipeline moves data through four stages:

**1. Extraction:**  Amazon product listings are scraped using Python Requests and BeautifulSoup inside Jupyter notebooks, and saved as raw CSV files.

**2. Automate & Clean:** n8n watches for new raw CSV files (file trigger), passes them to a cleaning node, and ingests the cleaned output automatically, no manual steps. Cleaning logic itself (deduplication, type casting, null handling) is done in Pandas and NumPy.

**3. Store & Analyze:** Cleaned data is loaded into MySQL. From there, SQL views and summary tables are built to generate descriptive statistics and KPIs (Top Brand, Top Niches, Competition Density Scores, and other metrics.).

**4. Visualize:** Tableau connects to MySQL and renders the KPIs and summary views into two interactive dashboards: an Entry Strategy Dashboard and a TagIntel (pricing/discount) Dashboard.

[Back to navigation](#navigate-through-the-readme-file)

---

## Installation and Setup

**Ensure you have these softwares pre-installed:**
- Python 3.9+
- MySQL Server & MySQL Workbench (or any preferred SQL edition)
- n8n (self-hosted or cloud)
- Tableau Desktop / Tableau Public (or any preferred BI Tool)

#### Steps to follow!

**1. Clone the repo**
```bash
git clone https://github.com/AmAzInG@12/Amazon-Products-Analytics-Pipeline.git
cd Amazon-Products-Analytics-Pipeline

# Install Python dependencies
pip install -r requirements.txt
```
> **Note on NLP Resources:** The scraping pipeline utilizes NLTK for keyword extraction. The script will automatically check for and download the required `punkt` and `stopwords` data packages on its first execution.

**2. Setup MySQL**
- Create a new Database (products_data)
- Execute the SQL Files in the '/SQL' Directory in this order:
```MySQL
SOURCE SQL/Schema.sql;
SOURCE SQL/Views.sql;
```

**3. Import n8n Workflow Automation**
- Launch n8n Application
- Import the file 'Pipeline/n8n_workflow.json' from this directory.
> **Optional:** Adjust the nodes inside the canvas and point to your local directories. 

**4. Start the Automation Process**
- Make sure the n8n workflow is in `Published Mode`.
- Run the `Scraping_Script` (If you prefer, you can change to scrape your desired Amazon Categories!)
- After 15 - 20 mins the Scraping will be done for around 200 products. File will hear trigger and start cleaning node and ingestion process and within seconds your views, kpis, competition density score will be ready to be used in your dashboards!

[Back to navigation](#navigate-through-the-readme-file)

---

## Project Structure

```
Project_Amazon_Products_Analytics_Pipeline/
├── README.md
├── requirements.txt
├── .gitignore
├── Scrapers/
│   ├── Scraping_Script.ipynb
│   └── scraper_config
├── Raw_Data/
│   └── Scraped Data will get saved here.
├── Clean_Data/
│   └── Cleaned Data will get saved here.
├── Pipeline/
│   └── n8n_workflow.json
├── n8n_scripters/
│   ├── n8n_cleaner.py
│   └── n8n_merger.py
├── SQL/
│   ├── Procedures_Maintenance.sql
│   ├── Schema.sql
│   └── Views.sql
├── Docs/
│   ├── dashboard_screenshots/
│   └── pipeline_architecture.png
└── Sample_Data/
│   ├── Sample_Cleaned_Data.csv
    └── Sample_Raw_Data.csv
```

[Back to navigation](#navigate-through-the-readme-file)

---

## Key Insights

- **Footwear and Men's Shirts** show the lowest competition density scores (22.84 and 25.21) despite healthy review velocity, flagged as high-opportunity entry categories.
- **Appliances and Headphones** are the most saturated categories, with competition density scores above 55.
- Average discount across all categories sits at **46.38%**, with an average review rating of **4.05/5**.
- Samsung was identified as the top competitor by brand presence across the dataset.

[Back to navigation](#navigate-through-the-readme-file)

---

# Dashboards

The analytics layer consists of two interactive Tableau dashboards designed to help identify profitable product opportunities and understand pricing behavior across Amazon categories.

---

## Entry Strategy Dashboard

Designed for sellers and market researchers to quickly identify low-competition, high-potential product categories.

### Highlights

- Competition Density Score
- Top Performing Brands
- Average Rating & Reviews
- Entry Radar (Butterfly Chart)
- Category Comparison
- Interactive Filters

<p align="center">
<img src="/Dashboards/EntryStrategy_Dashboard.png" width="900">
</p>

---

## TagIntel Dashboard

Provides detailed pricing intelligence by analyzing discounts, pricing distributions, customer ratings, and category trends.

### Highlights

- Discount Distribution
- Price vs MRP Analysis
- Category-wise Pricing
- KPIs
- Interactive Filters

<p align="center">
<img src="/Dashboards/TagIntel_Dashboard.png" width="900">
</p>

---

# Dashboard Gallery

A closer look at individual visualizations powering the dashboards.

<p align="center">
  <img src="/Dashboards/KPIS_Pic.png" width="350" height = "400"/>
  <img src="/Dashboards/Discount_Histogram.png" width="350" height = "400"/>
  <img src="/Dashboards/Pricing_Distribution.png" width="350" height = "400"/>
</p>

---

# Dashboard Walkthrough

Watch the interactive Tableau dashboard in action, including filtering, category selection, and KPI updates.

<p align="center">
<img src="/Dashboards/TagIntel.gif" width="900">
</p>

> Demonstrates interactive filters, dynamic KPI updates, pricing analysis, and competition insights.


[Back to navigation](#navigate-through-the-readme-file)

---

## Contact

Built by  | [LinkedIn](#) | [Github](#)
