from pathlib import Path
import duckdb

def main() -> None:
    script_dir = Path(__file__).resolve().parent
    db_path = script_dir / "inventory.duckdb"

    print(f"📦 Usando base de datos: {db_path}")

    con = duckdb.connect(str(db_path))

    # Crear tabla Silver a partir de Bronze
    con.execute("""
    CREATE OR REPLACE TABLE slv_stock_levels AS
    SELECT
        snapshot_date,
        location_id,
        sku AS product_sku,
        on_hand_qty AS stock_qty
    FROM brz_stock_levels;
    """)

    print("🥈 [SILVER] Niveles de inventario procesados → tabla: slv_stock_levels")


if __name__ == "__main__":
    main()