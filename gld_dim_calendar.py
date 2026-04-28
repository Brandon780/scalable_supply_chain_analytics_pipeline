from pathlib import Path
import duckdb

def main() -> None:
    print("🚀 Creating gold__dim_date__lite")

    script_dir = Path(__file__).resolve().parent
    db_path = script_dir / "inventory.duckdb"
    con = duckdb.connect(str(db_path))

    con.execute("""
    CREATE OR REPLACE TABLE gold__dim_date__lite AS

    WITH all_dates AS (

        SELECT DISTINCT CAST(SalesDate AS DATE) AS TheDate
        FROM gold__fact_sales__lite

        UNION

        SELECT DISTINCT CAST(WeekStartDate AS DATE) AS TheDate
        FROM gold__fact_inventory_exposure__lite

        UNION

        SELECT DISTINCT CAST(WeekStartDate AS DATE) AS TheDate
        FROM gold__fact_inventory_snapshots__lite

        UNION

        SELECT DISTINCT CAST(WeekStartDate AS DATE) AS TheDate
        FROM gold__fact_inventory_movements__lite
    )

    SELECT
        TheDate                               AS FullDate,
        EXTRACT(YEAR    FROM TheDate)         AS Year,
        EXTRACT(MONTH   FROM TheDate)         AS Month,
        EXTRACT(DAY     FROM TheDate)         AS Day,
        EXTRACT(DOW     FROM TheDate)         AS WeekDay,
        DATE_TRUNC('week',    TheDate)        AS WeekStartDate,
        DATE_TRUNC('month',   TheDate)        AS MonthStartDate,
        DATE_TRUNC('quarter', TheDate)        AS QuarterStartDate,
        DATE_TRUNC('year',    TheDate)        AS YearStartDate
    FROM all_dates
    ORDER BY FullDate;
    """)

    count = con.execute("SELECT COUNT(*) FROM gold__dim_date__lite").fetchone()[0]
    con.close()
    print(f"✅ Created gold__dim_date__lite → {count} rows")

if __name__ == "__main__":
    main()