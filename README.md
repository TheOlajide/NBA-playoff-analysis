# NBA Playoff Analysis Project


## Project Overview

This project analyzes NBA playoff data, originally designed with Postgres + Spark for storage and transformations, and now updated to use Airflow + Snowflake + dbt for modern orchestration, warehousing, and analytics.

The project does the following:

1. Scrape NBA playoff data

2. Store raw datasets in snowflake

3. Clean and Transform raw data with DBT for Analytics readiness 

4. Analysis and visualization with PowerBI

## Aim

The aim of this project is to scrape useful web data and implement a medallion architecture, analyze historical NBA statistics to predict potential outcomes of the 2024–2025 NBA playoffs.

Rather than employing machine learning, this project relies on comparative and statistical analysis of past seasons (2022–2023 and 2023–2024) to identify key performance patterns and trends that can guide predictive insights.

## Architecture

- Data Storage: Snowflake

- Transformations: DBT Cloud

- Visualization: PowerBI


## Data Dictionary

For data dictionary see the [dictionary](/Dictionary.md)

## Workflow

1. Raw scraped data lands into Snowflake DataWarehouse

- Connect DBT to staging schema (transform data in three layers medallion architecture)
  dbt models:

    stg_games.sql, stg_players.sql, stg_stats.sql → clean staging tables

    fct_performance.sql → fact table for player performance

    dim_teams.sql, dim_players.sql → dimensions for analysis

2. Write transformed results back to Snowflake.

3. Analytics schema: Final dbt models materialized in Snowflake for BI tools.



## Rules-Based Framework

### Transformation rules:

- Standardize player/team names

- Remove duplicates

- Normalize date formats

### Business rules:

- Calculate playoff averages per player

- Identify top performers per round

- Derive team win/loss ratios

## Evaluation Metrics

- Data Quality

- Missing value checks

- Referential integrity (foreign key consistency)

- Duplicate detection

## Performance

- Query execution times in Snowflake

- Airflow DAG runtime efficiency

## Project Structure

```
└───NBA-playoff-analysis
    ├───for each
    │   ├───player
    │   ├───team_ratings
    │   └───team_stats
    ├───raw data
    └───webscrapping scripts

```

## Future Enhancements

- Add API-based scraping to reduce Selenium dependency

- Expand dbt models to include advanced metrics (PER, win shares)

- Automate CI/CD for dbt with GitHub Actions

- Visualize inPower BI with live Snowflake connection (Direct Connect).
