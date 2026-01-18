# NBA Playoff Analysis Project


## Project Overview

This project uses historical NBA data (2022–2024) scraped from web to analyze team, player, and conference performance and identify patterns that inform 2024–2025 playoff expectations, using descriptive and comparative analytics in a three-page Power BI dashboard.

## Methodology

1. Raw data is scraped from the web using a python library.

2. Raw datasets land in snowflake DWH in the staging schema

3. Data is cleaned and transformed with DBT for Analytics readiness

4. Analysis and visualization with PowerBI


## Tools Used

- Webscrapping: Python

- DataWarehouse: Snowflake

- Transformations: DBT Cloud

- Analysis and Visualization: PowerBI


## Data Dictionary

For data dictionary see the [dictionary](/Dictionary.md)


## Project Structure

```
NBA-playoff-analysis
    ├───analysis report
    |     |_

    
    ├───raw data
    └───webscrapping scripts
        └───web snapshots
            ├───player table
            ├───team_ratings table
            └───team_stats table
            
```
           
## Future Enhancements

- Add API-based scraping to reduce Selenium dependency

- Expand dbt models to include advanced metrics (PER, win shares)

- Automate CI/CD for dbt with GitHub Actions

- Visualize inPower BI with live Snowflake connection (Direct Connect).
