# NBA Playoff Analysis Project
## Navigation

- [Project Overview](#project-overview)
- [Technologies](#technologies)
- [Architecture Overview](#architecture-overview)
- [Methodology](#methodology)
- [Project Structure](#project-structure)
- [Project Outcome](#project-outcome)
- [Data Dictionary](#data-dictionary)

## Project Overview

This project uses historical NBA data (2022–2024) scraped from web to analyze team, player, and conference performance and identify patterns that inform 2024–2025 playoff expectations, using descriptive and comparative analytics in a three-page Power BI dashboard.


## Technologies

The project uses the below stack:

Data Collection

- Python – Used for web scraping NBA statistics
- Requests / Web Scraping Libraries – Extract structured data from online sources

Data Transformation and Storage

- dbt (Data Build Tool) – SQL-based transformation framework used to structure and test data models
- Snowflake – Cloud data warehouse used to store and process transformed datasets

Data Modeling

- Bronze Layer – Raw staging models that clean and standardize incoming data
- Gold Layer – Final analytical models used for reporting and insights

Data Visualization

- Power BI – Interactive dashboards and analytical reports built from the transformed datasets

## Architecture Overview

The workflow follows these stages:

1. Data Collection:
Python web scraping scripts extract NBA statistics data such as player performance, team ratings, and conference standings from a web source. The scraped data is stored locally as CSV files and pushed into snowflake via a custom python script.

2. Raw Data Storage:
The extracted datasets (players.csv, ratings.csv, and team standings data) serve as the raw input layer for the analytics pipeline.

3. Data Transformation with dbt:
The raw data loaded into Snowflake is transformed using dbt through a layered architecture:

- Bronze Layer (Staging Models) Cleans and standardizes raw datasets into structured staging tables.
- Gold Layer (Analytics Models) Produces curated datasets optimized for analysis, such as team ratings, conference standings, and player statistics.

4. Data Quality & Documentation:
dbt YAML files define tests, documentation, and metadata for each model, ensuring data quality and transparency.

5. Analytics & Visualization:
The final transformed datasets are connected directly to Power BI, where dashboards and reports are created to analyze NBA performance trends.

## Methodology

Raw data is first scraped from the web using a Python library designed for extracting information from online sources. Once collected, these raw datasets are loaded with python into a staging schema in snowflake, where they are stored in their original or minimally processed form. 
From there, DBT (Data Build Tool) connects to the staging schema and applies a series of transformations such as cleaning, standardizing, and modeling the data. The transformed datasets are then loaded into a destination schema within Snowflake that is structured and optimized for analytical use.
Finally, Power BI can connect to this destination schema to perform data analysis and create interactive dashboards and visualizations for reporting and insights.

```
  Source Data                      ingestion         Storage/Transformation           Visualization
  ──────────                       ─────────         ──────────────────────           ─────────────

  players table.html       ─┐                                            
  team_ratings table.html  ─┼──>   Snowflake  ──>    [Raw]     ──>   [Mart]    ──>    Dashboard/Reports
  team_stats table.html    ─┘     (warehouse)       (Staging)       (Analytics)          (Output)

```

## Project Structure
The repository is organized into several directories that represent the different stages of the data pipeline, from data collection and transformation to analysis and reporting.

- analysis_report/ - contains the final analytical outputs of the project, including Power BI report (.pbix) and exported PDF reports summary of the NBA playoff analysis.

- transformation/dbt_NBA/ - contains the dbt project used for transforming raw data into analytics-ready datasets.

- transformation/dbt_NBA/models/ directory is organized into a Bronze–Gold architecture, where the Bronze layer contains staging models that clean and standardize raw data (stg_ratings.sql, stg_teams_conf_standings.sql, stg_players.sql), while the Gold layer contains final analytical models (team_ratings.sql, conference_standing.sql, nba_players.sql). 
Each model has corresponding YAML files that define documentation, tests, and metadata.
Other folders such as macros/, seeds/, snapshots/, and tests/ support reusable SQL logic, seed data loading, historical tracking, and data quality testing.

- data/raw/ - stores the original datasets (CSV files) used in the project before transformation.

- ingestion/scrapping/ - contains the Python scripts used to scrape NBA data from the web, along with saved HTML snapshots of the source tables used during development.

- docs/data_dictionary.md - describes the datasets, including column definitions and descriptions.

- README.md - This is the root readme that provides an overview of the project

- .gitignore - ensures unnecessary files are excluded from version control.


```
NBA-playoff-analysis
    |───analysis report
    |     ├───NBA Project PowerBI report.pbix
    |     ├───NBA Project PowerBI report.pdf
    |     └───NBA Project Report.pdf
    |
    ├─── data
    |     └─── raw
    |          ├───players.csv
    |          ├───ratings.csv
    |          └───teams_conf_standings.csv
    |
    |─── docs
    |     └─── data dictionary.md
    |
    |─── ingestion
    |      ├─── raw_to_snowflake.py
    |      ├─── scrapping
    |      |     └─── web snapshots
    |      |           ├─── player table
    |      |           ├─── team_ratings table
    |      |           └─── team_stats table
    |      └─── webscrapping script.py
    |
    |─── transformation
    |     └───dbt_NBA  
    |          ├─── macros
    |          ├─── models
    |          |      ├─── bronze
    |          |      |      ├─── dot sql
    |          |      |      |      ├───stg_ratings.sql
    |          |      |      |      ├───stg_teams_conf_standings.sql
    |          |      |      |      └───stg_players.sql
    |          |      |      | 
    |          |      |      └─── dot yaml
    |          |      |             ├─── _stg_ratings.yml
    |          |      |             ├─── _stg_teams_conf_standings.yml
    |          |      |             ├─── _stg_players.yml
    |          |      |             └─── sources.yml      
    |          |      |
    |          |      |
    |          |      └─── gold
    |          |             ├─── dot sql 
    |          |             |      ├─── team_ratings.sql
    |          |             |      ├─── conference standing.sql
    |          |             |      └─── nba_players.sql
    |          |             | 
    |          |             └─── dot yaml
    |          |                    ├─── _team_ratings.yml
    |          |                    ├─── _conference_standing.yml
    |          |                    └─── _nba_players.yml                          
    |          ├─── seeds
    |          ├─── snapshots
    |          ├─── tests
    |          ├─── .gitignore
    |          ├─── dbt_project.yml
    |          ├─── packages.yml
    |          └─── readme.md
    |
    ├───.gitignore
    |
    └─── README.md
```
## Project Outcome
This project delivers a complete end-to-end NBA data analytics pipeline, transforming raw web-scraped basketball statistics into structured, analytics-ready datasets and interactive reports.

The pipeline begins with Python web scraping scripts that extract NBA player statistics, team ratings, and conference standings from online sources. The scraped data is stored as raw CSV files and then ingested into staging schema in snowflake.

Using dbt (Data Build Tool) with Snowflake, the raw datasets are transformed through a layered data architecture:

The Bronze layer performs initial staging and cleaning of the raw data, standardizing formats and preparing the datasets for analysis.

The Gold layer produces curated analytical models that combine and structure the data into meaningful datasets such as team ratings, conference standings, and player performance metrics.

These transformed datasets are then used to build an interactive Power BI dashboard, which enables exploration of NBA team performance, player statistics, and conference standings in a visual and intuitive format.

The final deliverables include:

- A fully reproducible dbt transformation pipeline

- Clean analytical datasets stored in Snowflake

- A Power BI dashboard for visual analysis

- Supporting documentation including a data dictionary and project report

## Data Dictionary

See [dictionary](/Dictionary.md)