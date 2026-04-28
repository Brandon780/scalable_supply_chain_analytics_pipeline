# gold__dim_location__lite.py
from pathlib import Path
import duckdb

def main() -> None:
    script_dir = Path(__file__).resolve().parent
    db_path = script_dir / "inventory.duckdb"

    con = duckdb.connect(str(db_path))

    print("🚀 Creating gold__dim_location__lite")

    # Creamos la tabla Gold con LocationType incluida
    con.execute("""
    CREATE OR REPLACE TABLE gold__dim_location__lite AS
    SELECT
        location_id   AS LocationID,
        location_name AS LocationName,
        region        AS Region,
        location_type AS LocationType
    FROM silver__location_master__lite;
    """)

    count = con.execute("SELECT COUNT(*) FROM gold__dim_location__lite").fetchone()[0]
    con.close()
    print(f"✅ Created gold__dim_location__lite → {count} rows")

if __name__ == "__main__":
    main()