"""Load: persist transformed tables to DuckDB warehouse file."""
import duckdb, os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'warehouse.duckdb')

def load_all(warehouse: dict) -> str:
    con = duckdb.connect(DB_PATH)
    for table_name, df in warehouse.items():
        con.execute(f"DROP TABLE IF EXISTS {table_name}")
        con.register(f'_tmp_{table_name}', df)
        con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM _tmp_{table_name}")
        con.unregister(f'_tmp_{table_name}')
    con.close()
    return DB_PATH

def load_warehouse():
    """Load all tables from warehouse for dashboard."""
    if not os.path.exists(DB_PATH):
        return None
    con = duckdb.connect(DB_PATH, read_only=True)
    tables = ['fact_orders','dim_customers','dim_products','agg_monthly','agg_category']
    data = {t: con.execute(f"SELECT * FROM {t}").df() for t in tables}
    con.close()
    return data
