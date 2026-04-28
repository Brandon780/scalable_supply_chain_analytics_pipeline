from pathlib import Path
import duckdb

def main() -> None:
    script_dir = Path(__file__).resolve().parent

    
    db_path = script_dir / "inventory.duckdb"

    print("Usando DB en:", db_path)

    con = duckdb.connect(str(db_path))

    print("Tablas:", con.execute("SHOW TABLES").fetchall())

    con.execute("""
    CREATE OR REPLACE TABLE brz_stock_events AS
    SELECT
        movement_id,
        movement_ts,
        movement_date,
        movement_type,
        sku,
        from_location_id,
        to_location_id,
        qty
    FROM raw__inventory_movements__lite;
    """)

    con.close()
    print("🟤 Capa BRONCE completada: datos operativos de inventario cargados")

if __name__ == "__main__":
    main()