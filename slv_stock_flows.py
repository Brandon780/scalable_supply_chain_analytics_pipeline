from pathlib import Path
import duckdb

def main() -> None:
    # Carpeta donde está este script
    script_dir = Path(__file__).resolve().parent

    # Apunta a la misma DB donde creaste bronze
    db_path = script_dir / "inventory.duckdb"

    con = duckdb.connect(str(db_path))

    # ---------------------------------------------------------
    # SILVER TABLE: Inventory Movements
    # ---------------------------------------------------------
    con.execute("""
    CREATE OR REPLACE TABLE slv_stock_flows AS
    SELECT
        movement_id      AS MovementID,
        movement_ts      AS MovementTimestamp,
        movement_date    AS MovementDate,
        movement_type    AS MovementType,
        sku              AS ProductSKU,
        from_location_id AS FromLocationID,
        to_location_id   AS ToLocationID,
        qty              AS Quantity
    FROM brz_stock_events;
    """)

    con.close()
    print("🥈 Created silver")

if __name__ == "__main__":
    main()