"""
ETL Pipeline — run_pipeline.py
One-command runner: extract → transform → load → report
Run: python run_pipeline.py
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None

def main():
    print("=" * 55)
    print("  DataMind ETL Pipeline v1.0")
    print("=" * 55)

    print("\n[1/3] Extracting raw data...")
    from pipeline.extract import extract_all
    raw = extract_all()
    print(f"  Orders   : {len(raw['orders']):,} rows")
    print(f"  Customers: {len(raw['customers']):,} rows")
    print(f"  Products : {len(raw['products']):,} rows")

    print("\n[2/3] Transforming data (DuckDB)...")
    from pipeline.transform import transform_all
    warehouse = transform_all(raw)
    print(f"  fact_orders     : {len(warehouse['fact_orders']):,} rows")
    print(f"  dim_customers   : {len(warehouse['dim_customers']):,} rows")
    print(f"  dim_products    : {len(warehouse['dim_products']):,} rows")
    print(f"  agg_monthly     : {len(warehouse['agg_monthly']):,} rows")
    print(f"  agg_category    : {len(warehouse['agg_category']):,} rows")

    print("\n[3/3] Loading to DuckDB warehouse...")
    from pipeline.load import load_all
    db_path = load_all(warehouse)
    print(f"  Saved -> {db_path}")

    print("\n" + "=" * 55)
    print("  Pipeline complete! Launch dashboard:")
    print("  streamlit run dashboard/app.py")
    print("=" * 55)

if __name__ == "__main__":
    main()
