from pathlib import Path
import duckdb

def main() -> None:
    script_dir = Path(__file__).resolve().parent
    db_path = script_dir / "inventory.duckdb"
    con = duckdb.connect(str(db_path))

    con.execute("""
    CREATE OR REPLACE TABLE gold__fact_sales__lite AS
    SELECT
        DATE(transaction_date) AS SalesDate,
        location_id   AS LocationID,
        sku           AS ProductSKU,
        SUM(qty)      AS Quantity,
        AVG(unit_price) AS AvgUnitPrice
    FROM silver__sales_transactions__lite
    GROUP BY 1,2,3
    """)

    con.close()
    print("✅ Created gold__fact_sales__lite")

if __name__ == "__main__":
    main()