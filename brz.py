from pathlib import Path
import duckdb

def main() -> None:
    script_dir = Path(__file__).resolve().parent
    db_path = script_dir / "inventory.duckdb"

    print(f"📦 Usando base de datos: {db_path}")

    con = duckdb.connect(str(db_path))

    # Crear tabla Bronze (niveles de inventario)
    con.execute("""
    CREATE OR REPLACE TABLE brz_stock_levels AS
    SELECT
        snapshot_date,
        location_id,
        sku,
        on_hand_qty
    FROM raw__inventory_snapshots__lite;
    """)

    print("🟤 [BRONCE] ")


if __name__ == "__main__":
    main()