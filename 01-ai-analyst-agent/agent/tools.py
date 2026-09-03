"""
Agent tools: High-Precision Natural Language Data Analyst Engine
Directly interprets any business question and calculates exact KPIs, Plotly charts, and tables.
"""
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os, re

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'ecommerce_sales.csv')

def load_data() -> pd.DataFrame:
    if os.path.exists(DATA_PATH):
        try:
            return pd.read_csv(DATA_PATH, parse_dates=['order_date'])
        except Exception:
            return pd.read_csv(DATA_PATH)
    return _generate_data()

def _generate_data() -> pd.DataFrame:
    np.random.seed(42)
    n = 1000
    dates     = pd.date_range('2023-01-01', '2023-12-31', periods=n)
    cats      = ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Sports', 'Beauty']
    countries = ['USA', 'UK', 'Germany', 'India', 'Canada', 'Australia', 'France']
    segments  = ['Consumer', 'Corporate', 'Home Office']
    payments  = ['Credit Card', 'PayPal', 'Bank Transfer', 'Crypto']

    df = pd.DataFrame({
        'order_id':          [f'ORD{i:05d}' for i in range(n)],
        'order_date':        np.random.choice(dates, n),
        'customer_id':       [f'CUST{np.random.randint(1,300):04d}' for _ in range(n)],
        'product_category':  np.random.choice(cats, n, p=[0.28, 0.22, 0.18, 0.12, 0.12, 0.08]),
        'country':           np.random.choice(countries, n, p=[0.35, 0.15, 0.12, 0.14, 0.10, 0.08, 0.06]),
        'customer_segment':  np.random.choice(segments, n, p=[0.52, 0.33, 0.15]),
        'payment_method':    np.random.choice(payments, n, p=[0.55, 0.25, 0.15, 0.05]),
        'units_sold':        np.random.randint(1, 20, n),
        'unit_price':        np.round(np.random.uniform(9.99, 499.99, n), 2),
        'discount_pct':      np.random.choice([0, 5, 10, 15, 20], n, p=[0.4, 0.2, 0.2, 0.1, 0.1]),
        'is_returned':       np.random.choice([0, 1], n, p=[0.88, 0.12]),
        'rating':            np.round(np.random.uniform(2.5, 5.0, n), 1),
    })
    df['revenue'] = np.round(df['units_sold'] * df['unit_price'] * (1 - df['discount_pct'] / 100), 2)
    df.sort_values('order_date', inplace=True)
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    df.to_csv(DATA_PATH, index=False)
    return df

_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(241,245,249,0.5)',
    font=dict(color='#334155', family='Plus Jakarta Sans, sans-serif'),
    height=340,
    margin=dict(t=35, b=25, l=20, r=20)
)

def _format_num(val, col_name=""):
    if pd.isna(val):
        return "N/A"
    is_curr = any(k in col_name.lower() for k in ('revenue', 'sales', 'price', 'amount', 'cost', 'profit', 'total'))
    if is_curr:
        if abs(val) >= 1_000_000:
            return f"${val/1_000_000:.2f}M"
        if abs(val) >= 1_000:
            return f"${val:,.0f}"
        return f"${val:,.2f}"
    if isinstance(val, (int, np.integer)):
        return f"{val:,}"
    if abs(val) >= 100:
        return f"{val:,.0f}"
    return f"{val:,.2f}"

def _find_matching_column(q: str, cols: list, exclude_ids: bool = True):
    """Smart fuzzy matcher between question string and dataframe column names."""
    q_lower = q.lower()
    q_words = re.findall(r'\w+', q_lower)
    clean_cols = [c for c in cols if not (exclude_ids and any(k in c.lower() for k in ('id', 'code', 'key', 'uuid')))]
    
    # Direct exact word match
    for c in clean_cols:
        c_clean = c.lower().replace('_', ' ')
        if re.search(r'\b' + re.escape(c_clean) + r'\b', q_lower) or c.lower() in q_words:
            return c
            
    # Synonyms dictionary with whole word matching
    synonyms = {
        'revenue': ['revenue', 'sales', 'turnover', 'income', 'earning', 'earnings', 'spent', 'spending', 'money'],
        'discount_pct': ['discount', 'discounts', 'markdown', 'promo', 'promotion', 'pct'],
        'unit_price': ['price', 'pricing', 'expensive', 'cheap', 'unit price'],
        'units_sold': ['units', 'quantity', 'volume', 'qty', 'pieces', 'sold', 'units sold'],
        'is_returned': ['return', 'returns', 'returned', 'refund', 'refunds', 'refunded', 'cancellation'],
        'rating': ['rating', 'ratings', 'score', 'scores', 'review', 'reviews', 'satisfaction', 'stars'],
        'product_category': ['category', 'categories', 'product', 'products', 'item', 'items', 'merchandise'],
        'country': ['country', 'countries', 'nation', 'nations', 'geography', 'region', 'regions', 'location', 'locations', 'global'],
        'customer_segment': ['segment', 'segments', 'customer segment', 'audience', 'tier', 'consumer', 'corporate'],
        'payment_method': ['payment', 'payments', 'payment method', 'method', 'paypal', 'credit card', 'crypto', 'bank']
    }

    for target_col, syn_list in synonyms.items():
        if target_col in clean_cols:
            if any(re.search(r'\b' + re.escape(s) + r'\b', q_lower) for s in syn_list):
                return target_col

    # Stemming check (e.g. countries -> country, categories -> category)
    for c in clean_cols:
        stem = c.lower().replace('_', '')
        if any(stem in w or w in stem for w in q_words if len(w) > 3):
            return c

    return None

def run_query(df: pd.DataFrame, question: str, demo_mode: bool = True, api_key: str = None, is_custom: bool = False) -> dict:
    """Intelligently answers natural language queries with exact metrics, Plotly visualizations, and data tables."""
    try:
        q = question.lower().strip()
        num_cols = df.select_dtypes(include='number').columns.tolist()
        cat_cols = df.select_dtypes(include='object').columns.tolist()
        date_cols = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]

        # Meaningful categorical columns (exclude order_id, customer_id, unique hashes)
        clean_cat_cols = [c for c in cat_cols if not any(k in c.lower() for k in ('id', 'code', 'key', 'num', 'uuid')) and df[c].nunique() < len(df) * 0.8]
        if not clean_cat_cols and cat_cols:
            clean_cat_cols = cat_cols

        # Identify target numerical metric
        metric_col = _find_matching_column(q, num_cols, exclude_ids=True)
        if not metric_col:
            # Default to primary revenue/sales/amount column
            prio = [c for c in num_cols if any(k in c.lower() for k in ('revenue', 'sales', 'amount', 'profit', 'total', 'price', 'unit', 'rating'))]
            metric_col = prio[0] if prio else (num_cols[0] if num_cols else None)

        # Identify categorical grouping dimension
        group_col = _find_matching_column(q, clean_cat_cols, exclude_ids=True)

        # Check for explicit value filter in query (e.g. "Electronics sales", "Sales in USA")
        filter_col, filter_val = None, None
        for c in clean_cat_cols:
            unique_vals = df[c].dropna().unique()
            for v in unique_vals:
                v_str = str(v).lower()
                if len(v_str) > 2 and v_str in q:
                    filter_col = c
                    filter_val = v
                    break
            if filter_col:
                break

        # 1. Specific Value Filter Query (e.g. "Electronics sales", "Orders in USA")
        if filter_col and filter_val:
            filtered_df = df[df[filter_col] == filter_val]
            tot = filtered_df[metric_col].sum() if metric_col else len(filtered_df)
            avg = filtered_df[metric_col].mean() if metric_col else len(filtered_df)
            tot_all = df[metric_col].sum() if metric_col else len(df)
            pct_share = (tot / tot_all * 100) if tot_all > 0 else 0

            # Generate breakdown by next category or time
            next_cats = [c for c in clean_cat_cols if c != filter_col]
            if next_cats:
                breakdown_cat = next_cats[0]
                grp = filtered_df.groupby(breakdown_cat)[metric_col].sum().reset_index().sort_values(metric_col, ascending=False).head(8)
                fig = px.bar(
                    grp, x=breakdown_cat, y=metric_col,
                    title=f'{filter_val} {metric_col.replace("_"," ").title()} by {breakdown_cat.replace("_"," ").title()}',
                    color=metric_col, color_continuous_scale='Purples'
                )
            elif date_cols:
                t_df = filtered_df.copy()
                t_df['Month'] = t_df[date_cols[0]].dt.strftime('%b')
                t_df['Month_Num'] = t_df[date_cols[0]].dt.month
                grp = t_df.groupby(['Month_Num', 'Month'])[metric_col].sum().reset_index().sort_values('Month_Num')
                fig = px.area(grp, x='Month', y=metric_col, title=f'{filter_val} Monthly {metric_col.title()}', color_discrete_sequence=['#6366f1'])
            else:
                fig = px.histogram(filtered_df, x=metric_col, title=f'{filter_val} {metric_col.title()} Distribution')

            fig.update_layout(**_LAYOUT)
            insight = (f"In **{filter_val}** ({filter_col.replace('_',' ')}), total **{metric_col.replace('_',' ')}** is **{_format_num(tot, metric_col)}** "
                       f"({pct_share:.1f}% of entire dataset) across **{len(filtered_df):,} records**. "
                       f"Average per transaction is **{_format_num(avg, metric_col)}**.")
            return {"insight": insight, "fig": fig, "table": filtered_df.head(10)}

        # 2. 3D / Multivariate / Scatter / Correlation
        if any(w in q for w in ['3d', 'scatter', 'multivariate', 'cluster', 'correlation', 'spread']):
            avail_nums = [c for c in num_cols if df[c].std() > 0][:3]
            if len(avail_nums) >= 3:
                fig = px.scatter_3d(
                    df.head(400), x=avail_nums[0], y=avail_nums[1], z=avail_nums[2],
                    color=group_col if group_col else (clean_cat_cols[0] if clean_cat_cols else None),
                    title=f'3D Scatter: {avail_nums[0].title()} × {avail_nums[1].title()} × {avail_nums[2].title()}',
                    color_discrete_sequence=['#6366f1', '#10b981', '#3b82f6', '#ec4899', '#f59e0b']
                )
                fig.update_layout(**_LAYOUT, height=380)
                insight = f"Generated interactive 3D model correlating **{avail_nums[0]}**, **{avail_nums[1]}**, and **{avail_nums[2]}**. You can drag, rotate, and zoom."
                return {"insight": insight, "fig": fig, "table": None}

        # 3. Refund / Return Rate Query
        if any(w in q for w in ['refund', 'return', 'returns', 'returned']) and ('is_returned' in df.columns or any('return' in c.lower() for c in num_cols)):
            ret_col = 'is_returned' if 'is_returned' in df.columns else [c for c in num_cols if 'return' in c.lower()][0]
            target_cat = group_col if group_col else (clean_cat_cols[0] if clean_cat_cols else None)
            if target_cat:
                grp = df.groupby(target_cat).agg(
                    return_rate=(ret_col, 'mean'),
                    total_orders=(df.columns[0], 'count')
                ).reset_index().sort_values('return_rate', ascending=False)
                grp['return_rate_pct'] = (grp['return_rate'] * 100).round(1)

                fig = px.bar(
                    grp, x='return_rate_pct', y=target_cat, orientation='h',
                    title=f'Return Rate (%) by {target_cat.replace("_"," ").title()}',
                    color='return_rate_pct', color_continuous_scale='Reds',
                    text_auto='.1f'
                )
                fig.update_layout(**_LAYOUT)
                avg_ret = df[ret_col].mean() * 100
                top_ret = grp.iloc[0]
                insight = (f"The average return rate is **{avg_ret:.1f}%**. "
                           f"**{top_ret[target_cat]}** has the highest return rate at **{top_ret['return_rate_pct']:.1f}%**, "
                           f"while **{grp.iloc[-1][target_cat]}** has the lowest at **{grp.iloc[-1]['return_rate_pct']:.1f}%**.")
                return {"insight": insight, "fig": fig, "table": grp.rename(columns={'return_rate_pct': 'Return Rate %', 'total_orders': 'Total Records'})}

        # 4. Temporal Trend / Time-Series Query
        if date_cols and any(w in q for w in ['monthly', 'trend', 'time', 'over time', 'timeline', 'growth', 'by month', 'year', 'quarter', 'trajectory', 'seasonality']):
            d_col = date_cols[0]
            t_df = df.copy()
            t_df['Month'] = t_df[d_col].dt.strftime('%b')
            t_df['Month_Num'] = t_df[d_col].dt.month
            m_grp = t_df.groupby(['Month_Num', 'Month'])[metric_col].sum().reset_index().sort_values('Month_Num')

            fig = px.area(
                m_grp, x='Month', y=metric_col,
                title=f'Monthly {metric_col.replace("_"," ").title()} Trajectory',
                color_discrete_sequence=['#6366f1']
            )
            fig.update_traces(fill='tozeroy', fillcolor='rgba(99,102,241,0.12)')
            fig.update_layout(**_LAYOUT)

            peak_row = m_grp.loc[m_grp[metric_col].idxmax()]
            low_row = m_grp.loc[m_grp[metric_col].idxmin()]
            tot_metric = m_grp[metric_col].sum()
            insight = (f"Monthly **{metric_col.replace('_',' ')}** reached its peak in **{peak_row['Month']}** at **{_format_num(peak_row[metric_col], metric_col)}** "
                       f"({peak_row[metric_col]/tot_metric*100:.1f}% of annual total). "
                       f"The lowest month was **{low_row['Month']}** with **{_format_num(low_row[metric_col], metric_col)}**. "
                       f"Total across all months is **{_format_num(tot_metric, metric_col)}**.")
            return {"insight": insight, "fig": fig, "table": m_grp[['Month', metric_col]].rename(columns={metric_col: f"Total {metric_col.title()}"})}

        # 5. Grouped Ranking / Top N / Comparison Query
        is_ranking_question = any(w in q for w in ['by ', 'top', 'which', 'compare', 'breakdown', 'share', 'distribution', 'per', 'most', 'best', 'highest', 'lowest', 'rank']) or bool(group_col)
        
        if is_ranking_question and clean_cat_cols and metric_col:
            target_group = group_col if group_col else clean_cat_cols[0]
            is_avg = any(w in q for w in ['average', 'mean', 'avg', 'rate'])
            agg_func = 'mean' if is_avg else 'sum'

            grp = df.groupby(target_group)[metric_col].agg(agg_func).reset_index().sort_values(metric_col, ascending=False)
            
            top_n = 5 if any(w in q for w in ['top 5', 'top5', '5']) else (10 if any(w in q for w in ['top 10', 'top10', '10']) else 8)
            disp_grp = grp.head(top_n)

            if any(w in q for w in ['pie', 'share', 'percent', 'portion']) or (len(disp_grp) <= 4 and not is_avg):
                fig = px.pie(
                    disp_grp, names=target_group, values=metric_col,
                    title=f'{metric_col.replace("_"," ").title()} Share by {target_group.replace("_"," ").title()}',
                    color_discrete_sequence=['#4f46e5', '#06b6d4', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6']
                )
            else:
                fig = px.bar(
                    disp_grp, x=target_group, y=metric_col,
                    title=f'{"Average" if is_avg else "Total"} {metric_col.replace("_"," ").title()} by {target_group.replace("_"," ").title()}',
                    color=metric_col, color_continuous_scale='Purples',
                    text_auto='.2s'
                )
            fig.update_layout(**_LAYOUT)

            top_item = grp.iloc[0]
            total_sum = grp[metric_col].sum() if not is_avg else df[metric_col].mean()
            pct_contrib = (top_item[metric_col] / total_sum * 100) if (not is_avg and total_sum > 0) else 0
            metric_clean = metric_col.replace('_', ' ')
            group_clean = target_group.replace('_', ' ')
            sub_desc = f"({pct_contrib:.1f}% of total {metric_clean})" if not is_avg else "average per transaction"

            insight = (f"**{top_item[target_group]}** ranks #1 in **{group_clean}** with "
                       f"**{_format_num(top_item[metric_col], metric_col)}** {sub_desc}. "
                       f"Total across all {df[target_group].nunique()} {group_clean} segments is **{_format_num(df[metric_col].sum(), metric_col)}**.")

            return {"insight": insight, "fig": fig, "table": disp_grp.rename(columns={metric_col: f'{"Avg" if is_avg else "Total"} {metric_col.title()}'})}

        # 6. Overall Metric Summary Query (e.g. "What is total revenue?", "Average rating")
        if metric_col:
            tot = df[metric_col].sum()
            avg = df[metric_col].mean()
            med = df[metric_col].median()
            mx = df[metric_col].max()
            mn = df[metric_col].min()

            fig = px.histogram(
                df, x=metric_col,
                title=f'Distribution of {metric_col.replace("_"," ").title()}',
                color_discrete_sequence=['#6366f1'],
                nbins=30
            )
            fig.update_layout(**_LAYOUT)

            insight = (f"Analysis for **{metric_col.replace('_',' ')}** across **{len(df):,} records**: "
                       f"Total: **{_format_num(tot, metric_col)}** | Average: **{_format_num(avg, metric_col)}** | "
                       f"Median: **{_format_num(med, metric_col)}** | Range: **{_format_num(mn, metric_col)}** to **{_format_num(mx, metric_col)}**.")

            summary_table = pd.DataFrame({
                "Metric": ["Total Sum", "Average / Mean", "Median", "Max Value", "Min Value", "Count"],
                "Value": [_format_num(tot, metric_col), _format_num(avg, metric_col), _format_num(med, metric_col), _format_num(mx, metric_col), _format_num(mn, metric_col), f"{len(df):,}"]
            })
            return {"insight": insight, "fig": fig, "table": summary_table}

        # 7. Fallback General Overview
        fig, data = _monthly_revenue(df) if (date_cols and metric_col) else (None, None)
        insight = (f"Analyzed **{len(df):,} records** in the active dataset across **{len(df.columns)} dimensions**. "
                   f"Try asking questions like *'Show revenue by category'*, *'Monthly trend'*, or *'Top countries by sales'*.")
        return {"insight": insight, "fig": fig, "table": df.head(10)}

    except Exception as e:
        insight = f"⚠️ Analyzed dataset preview across {len(df):,} rows and {len(df.columns)} columns."
        return {"insight": insight, "fig": None, "table": df.head(10)}


# ── Chart generators ──────────────────────────────────────────────────────────
def _monthly_revenue(df):
    date_cols = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]
    num_cols = df.select_dtypes(include='number').columns.tolist()
    d_col = date_cols[0] if date_cols else 'order_date'
    n_col = 'revenue' if 'revenue' in df.columns else (num_cols[0] if num_cols else None)

    df2 = df.copy()
    df2['month'] = df2[d_col].dt.month
    df2['month_label'] = df2[d_col].dt.strftime('%b')
    data = df2.groupby(['month', 'month_label'])[n_col].sum().reset_index().sort_values('month')
    fig = px.area(data, x='month_label', y=n_col, title=f'Monthly {n_col.replace("_"," ").title()}',
                  color_discrete_sequence=['#6366f1'])
    fig.update_traces(fill='tozeroy', fillcolor='rgba(99,102,241,0.08)')
    fig.update_layout(**_LAYOUT)
    return fig, data


# ── Auto Dashboard ─────────────────────────────────────────────────────────────
def build_dashboard(df: pd.DataFrame) -> list:
    """Auto-generate a comprehensive set of (key, fig) chart tuples for any DataFrame."""
    figs = []
    COLORS = ['#6366f1', '#10b981', '#3b82f6', '#ec4899', '#f59e0b', '#ef4444', '#8b5cf6']
    layout = dict(**_LAYOUT, title_font_size=14)

    date_cols = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]
    num_cols  = df.select_dtypes(include='number').columns.tolist()
    cat_cols  = [c for c in df.select_dtypes(include='object').columns.tolist()
                 if 2 <= df[c].nunique() <= 30]

    def _label(col): return col.replace('_', ' ').title()

    # 1. Time-series
    if date_cols and num_cols:
        date_col = date_cols[0]
        for num_col in num_cols[:2]:
            try:
                ts = df.set_index(date_col)[num_col].resample('ME').sum().reset_index()
                fig = px.area(ts, x=date_col, y=num_col,
                              title=f'📈 {_label(num_col)} Over Time',
                              color_discrete_sequence=['#6366f1'])
                fig.update_traces(fill='tozeroy', fillcolor='rgba(99,102,241,0.08)')
                fig.update_layout(**layout)
                figs.append((f'ts_{num_col}', fig))
            except Exception:
                pass

    # 2. Bar charts
    if cat_cols and num_cols:
        primary_num = num_cols[0]
        for cat_col in cat_cols[:2]:
            data = (df.groupby(cat_col)[primary_num].sum()
                      .reset_index()
                      .sort_values(primary_num, ascending=False)
                      .head(12))
            fig = px.bar(data, x=cat_col, y=primary_num,
                         title=f'📊 {_label(primary_num)} by {_label(cat_col)}',
                         color=primary_num, color_continuous_scale='Purples')
            fig.update_layout(**layout)
            figs.append((f'bar_{cat_col}', fig))

    # 3. Pie share
    if cat_cols and num_cols:
        cat_col, num_col = cat_cols[0], num_cols[0]
        pie_data = df.groupby(cat_col)[num_col].sum().reset_index()
        fig = px.pie(pie_data, names=cat_col, values=num_col,
                     title=f'🥧 {_label(num_col)} Share by {_label(cat_col)}',
                     color_discrete_sequence=COLORS)
        fig.update_layout(**layout)
        figs.append(('pie_share', fig))

    # 4. Histograms
    for num_col in num_cols[:2]:
        fig = px.histogram(df, x=num_col,
                           title=f'📉 Distribution: {_label(num_col)}',
                           color_discrete_sequence=['#10b981'], nbins=30)
        fig.update_layout(**layout)
        figs.append((f'hist_{num_col}', fig))

    return figs


def get_kpi_metrics(df: pd.DataFrame) -> dict:
    metrics = {}
    metrics["📦 Total Rows"] = f"{len(df):,}"
    num_cols = df.select_dtypes(include='number').columns.tolist()
    cat_cols = df.select_dtypes(include='object').columns.tolist()

    if 'revenue' in df.columns:
        metrics["💰 Total Revenue"] = f"${df['revenue'].sum():,.0f}"
        metrics["🛒 Avg Order Value"] = f"${df['revenue'].mean():.0f}"
    elif num_cols:
        primary = num_cols[0]
        label = primary.replace('_', ' ').title()
        metrics[f"∑ {label}"] = f"{df[primary].sum():,.1f}"
        metrics[f"⌀ {label}"] = f"{df[primary].mean():.2f}"

    if 'product_category' in df.columns:
        metrics["🏷️ Categories"] = str(df['product_category'].nunique())
    elif cat_cols:
        label = cat_cols[0].replace('_', ' ').title()
        metrics[f"# {label}"] = str(df[cat_cols[0]].nunique())

    return metrics
