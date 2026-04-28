from pathlib import Path
import duckdb

def main() -> None:
    script_dir = Path(__file__).resolve().parent
    db_path = script_dir / "inventory.duckdb"
    con = duckdb.connect(str(db_path))

    print("DB path:", db_path)
    print("Tables:", con.execute("SHOW TABLES").fetchall())

    con.execute("""
    CREATE OR REPLACE TABLE gold__fact_inventory_exposure__lite AS

    -- 1️⃣ Ventas (YA es timestamp → NO usar STRPTIME)
    WITH weekly_sales AS (
        SELECT
            DATE_TRUNC('week', transaction_ts) AS WeekStartDate,
            location_id AS LocationID,
            sku AS ProductSKU,
            SUM(qty) AS WeeklySalesQty
        FROM silver__sales_transactions__lite
        GROUP BY 1,2,3
    ),

    -- 2️⃣ Inventario (fechas mixtas → limpiar)
    inventory_clean AS (
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
        FROM inventory_clean
        GROUP BY 1,2,3
    ),

    -- 3️⃣ Movimientos (fechas mixtas → limpiar)
    movements_clean AS (
        SELECT
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

    -- 4️⃣ Unión final
    SELECT
        COALESCE(s.WeekStartDate, i.WeekStartDate, m.WeekStartDate) AS WeekStartDate,
        COALESCE(s.LocationID, i.LocationID, m.LocationID) AS LocationID,
        COALESCE(s.ProductSKU, i.ProductSKU, m.ProductSKU) AS ProductSKU,
        COALESCE(s.WeeklySalesQty, 0) AS WeeklySalesQty,
        COALESCE(i.WeekEndOnHandQty, 0) AS WeekEndOnHandQty,
        COALESCE(m.NetMovementQty, 0) AS NetMovementQty
    FROM weekly_sales s
    FULL OUTER JOIN weekly_inventory i
        ON s.WeekStartDate = i.WeekStartDate
       AND s.LocationID = i.LocationID
       AND s.ProductSKU = i.ProductSKU
    FULL OUTER JOIN weekly_movements m
        ON COALESCE(s.WeekStartDate, i.WeekStartDate) = m.WeekStartDate
       AND COALESCE(s.LocationID, i.LocationID) = m.LocationID
       AND COALESCE(s.ProductSKU, i.ProductSKU) = m.ProductSKU;
    """)

    con.close()
    print("✅ Created gold__fact_inventory_exposure__lite")

if __name__ == "__main__":
    main()