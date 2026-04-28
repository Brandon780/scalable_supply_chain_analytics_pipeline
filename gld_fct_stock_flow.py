from pathlib import Path
import duckdb

def main() -> None:
    script_dir = Path(__file__).resolve().parent
    db_path = script_dir / "inventory.duckdb"

    con = duckdb.connect(str(db_path))

    con.execute("""
    CREATE OR REPLACE TABLE gold__fact_inventory_movements__lite AS

    WITH movements_clean AS (
        SELECT
            -- Manejo de fechas mixtas
            COALESCE(
                TRY_STRPTIME(MovementDate, '%d/%m/%Y'),
                TRY_STRPTIME(MovementDate, '%Y-%m-%d')
            )::DATE AS MoveDate,
            COALESCE(ToLocationID, FromLocationID) AS LocationID,
            ProductSKU,
            Quantity
        FROM silver__inventory_movements__lite
        WHERE MovementDate IS NOT NULL
    ),

    weekly_movements AS (
        SELECT
            DATE_TRUNC('week', MoveDate) AS WeekStartDate,
            LocationID,
            ProductSKU,
            SUM(Quantity) AS NetMovementQty
        FROM movements_clean
        WHERE LocationID IS NOT NULL
        GROUP BY 1,2,3
    )

    SELECT *
    FROM weekly_movements;
    """)

    con.close()
    print("✅ Created gold__fact_inventory_movements__lite")

if __name__ == "__main__":
    main()