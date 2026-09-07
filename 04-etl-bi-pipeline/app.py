"""
Root entrypoint for 04-etl-bi-pipeline.
Allows running `streamlit run app.py` directly from project root.
"""
import sys
import os

# Ensure project root is on sys.path
proj_dir = os.path.dirname(os.path.abspath(__file__))
if proj_dir not in sys.path:
    sys.path.insert(0, proj_dir)

# Ensure DuckDB warehouse exists before launching dashboard
warehouse_path = os.path.join(proj_dir, "data", "warehouse.duckdb")
if not os.path.exists(warehouse_path):
    print("Warehouse database missing. Auto-generating via ETL pipeline...")
    from pipeline.extract import extract_all
    from pipeline.transform import transform_all
    from pipeline.load import load_all
    raw = extract_all()
    wh = transform_all(raw)
    load_all(wh)
    print("Warehouse ready!")

# Delegate to dashboard
dashboard_script = os.path.join(proj_dir, "dashboard", "app.py")
with open(dashboard_script, "r", encoding="utf-8") as f:
    code = f.read()

# Execute dashboard script in global scope
exec(compile(code, dashboard_script, "exec"), globals())
