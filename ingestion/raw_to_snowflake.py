import os
import sys
import logging
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv

# Logging

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s [%(levelname)s] %(message)s",
    handlers = [logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)

# Config — edit these or set as env variables

load_dotenv()  # loads a .env file if present

SNOWFLAKE_CONFIG = {
    "user":        os.getenv("SNOWFLAKE_USER",     "YOUR_USERNAME"),
    "password":    os.getenv("SNOWFLAKE_PASSWORD", "YOUR_PASSWORD"),
    "account":     os.getenv("SNOWFLAKE_ACCOUNT",  "YOUR_ACCOUNT"),
    "warehouse":   "NBA_WH",
    "database":    "analytics",
    "schema":      "mart_raw",
}

# CSV file paths → Snowflake table names

FILES = {
     r"C:\Users\aolajide\Downloads\Personals\Projects\NBA_project\NBA-playoff-analysis\data\raw\players.csv": "players",
     r"C:\Users\aolajide\Downloads\Personals\Projects\NBA_project\NBA-playoff-analysis\data\raw\ratings.csv": "ratings",
     r"C:\Users\aolajide\Downloads\Personals\Projects\NBA_project\NBA-playoff-analysis\data\raw\teams_conf_standings.csv": "teams_conf_standings",
}

# Helpers

def get_connection() -> snowflake.connector.SnowflakeConnection:
    """Open and return a Snowflake connection."""
    cfg = {k: v for k, v in SNOWFLAKE_CONFIG.items() if v}  # drop empty strings
    log.info("Connecting to Snowflake account '%s' ...", cfg["account"])
    conn = snowflake.connector.connect(**cfg)
    log.info("Connected ✓")
    return conn


def ensure_schema(cursor, database: str, schema: str) -> None:
    """Make sure the target database + schema exist."""
    cursor.execute(f'CREATE DATABASE IF NOT EXISTS "{database}"')
    cursor.execute(f'USE DATABASE "{database}"')
    cursor.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema}"')
    cursor.execute(f'USE SCHEMA "{schema}"')
    log.info("Using %s.%s", database, schema)


def sanitise_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Snowflake is case-insensitive but write_pandas matches column names exactly.
    Upper-case all columns and replace spaces / special chars with underscores.
    """
    df.columns = (
        df.columns.str.strip()
                  .str.upper()
                  .str.replace(r"[^\w]", "_", regex=True)
    )
    return df


def load_csv(filepath: str) -> pd.DataFrame:
    """Read a CSV file and return a clean DataFrame."""
    log.info("Reading  %s ...", filepath)
    df = pd.read_csv(filepath)
    df = sanitise_columns(df)
    log.info("  → %d rows, %d columns", len(df), len(df.columns))
    return df


def upload_table(
    conn: snowflake.connector.SnowflakeConnection,
    df: pd.DataFrame,
    table_name: str,
    database: str,
    schema: str,
) -> None:
    """
    Create-or-replace the Snowflake table and bulk-load the DataFrame via
    write_pandas (uses a PUT + COPY internally — very fast).
    """
    log.info("Uploading → %s.%s.%s ...", database, schema, table_name)

    success, nchunks, nrows, _ = write_pandas(
        conn=conn,
        df=df,
        table_name=table_name.upper(),
        database=database.upper(),
        schema=schema.upper(),
        auto_create_table=True,      # creates the table if it doesn't exist
        overwrite=True,              # truncate + reload on each run
        quote_identifiers=False,
    )

    if success:
        log.info("  ✓ Loaded %d rows in %d chunk(s)", nrows, nchunks)
    else:
        raise RuntimeError(f"write_pandas reported failure for table '{table_name}'")


# Main

def main() -> None:
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            ensure_schema(cur, SNOWFLAKE_CONFIG["database"], SNOWFLAKE_CONFIG["schema"])

        for csv_file, table_name in FILES.items():
            if not os.path.exists(csv_file):
                log.warning("File not found, skipping: %s", csv_file)
                continue

            df = load_csv(csv_file)
            upload_table(
                conn=conn,
                df=df,
                table_name=table_name,
                database=SNOWFLAKE_CONFIG["database"],
                schema=SNOWFLAKE_CONFIG["schema"],
            )

        log.info("=" * 50)
        log.info("All files loaded successfully 🎉")
        log.info("=" * 50)

    except Exception as exc:
        log.error("Pipeline failed: %s", exc)
        raise

    finally:
        conn.close()
        log.info("Connection closed.")


if __name__ == "__main__":
    main()