from pathlib import Path
import duckdb

def main() -> None:
    script_dir = Path(__file__).resolve().parent
    db_path = script_dir / "inventory.duckdb"

    con = duckdb.connect(str(db_path))

    print("🚀 VERSION NUEVA EJECUTANDO")
    print(__file__)

    con.execute("""
    CREATE OR REPLACE TABLE gold__fact_inventory_snapshots__lite AS

    WITH snapshots_clean AS (
        SELECT
            COALESCE(
                TRY_STRPTIME(SnapshotDate, '%d/%m/%Y'),
                TRY_STRPTIME(SnapshotDate, '%Y-%m-%d')
            )::DATE AS SnapDate,
            LocationID,
            ProductSKU,
            OnHandQuantity
        FROM silver__inventory_snapshots__lite
        WHERE SnapshotDate IS NOT NULL
    ),

    weekly_inventory AS (
        SELECT
            DATE_TRUNC('week', SnapDate) AS WeekStartDate,
            LocationID,
            ProductSKU,
            MAX(OnHandQuantity) AS WeekEndOnHandQty
        FROM snapshots_clean
        GROUP BY 1,2,3
    )

    SELECT *
    FROM weekly_inventory;
    """)

    # ✅ Verificación
    print("Filas creadas:",
          con.execute("SELECT COUNT(*) FROM gold__fact_inventory_snapshots__lite").fetchone()[0])

    con.close()
    print("✅ Created gold")

if __name__ == "__main__":
    main()