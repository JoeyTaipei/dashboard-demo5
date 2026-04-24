from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


DATA_DIR = Path(__file__).resolve().parent / "data"
PLOTLY_TEMPLATE = "plotly_dark"
STAR_WARS_BG = "#070b12"
STAR_WARS_PANEL = "rgba(11, 18, 32, 0.88)"
STAR_WARS_PANEL_ALT = "rgba(18, 29, 48, 0.92)"
STAR_WARS_BORDER = "rgba(110, 189, 255, 0.25)"
STAR_WARS_TEXT = "#e6f1ff"
STAR_WARS_MUTED = "#8da7c7"
STAR_WARS_ACCENT = "#ffe81f"
COLOR_PRIMARY = "#ffe81f"
COLOR_SECONDARY = "#6ec8ff"
COLOR_TERTIARY = "#5af7b0"
COLOR_SCALE = [COLOR_PRIMARY, COLOR_SECONDARY, COLOR_TERTIARY, "#ff8a5b", "#a78bfa", "#ff6b6b"]
RFM_SEGMENT_NAMES = {
    "Champions": "冠軍顧客",
    "Loyal": "忠誠顧客",
    "Potential Loyalists": "潛力忠誠顧客",
    "Promising": "潛力新客",
    "At Risk": "流失風險顧客",
    "Hibernating": "沉睡顧客",
}
JEDI_PANEL_SVG = """
<svg viewBox="0 0 960 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Star Wars style command illustration">
  <defs>
    <linearGradient id="blade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#d7fbff"/>
      <stop offset="100%" stop-color="#6ec8ff"/>
    </linearGradient>
    <linearGradient id="robe" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#2a374f"/>
      <stop offset="100%" stop-color="#151d2b"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="6" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  <rect width="960" height="260" rx="24" fill="rgba(11,18,32,0.65)"/>
  <circle cx="120" cy="62" r="2" fill="#fff"/>
  <circle cx="220" cy="42" r="1.5" fill="#fff"/>
  <circle cx="330" cy="84" r="2" fill="#fff"/>
  <circle cx="680" cy="38" r="2" fill="#fff"/>
  <circle cx="820" cy="70" r="1.5" fill="#fff"/>
  <circle cx="900" cy="44" r="2" fill="#fff"/>
  <g transform="translate(80 24)">
    <path d="M130 168 C118 122, 122 78, 154 54 C175 38, 204 33, 228 42 C262 55, 281 90, 277 129 C274 155, 264 182, 250 206 L112 206 C124 194, 136 181, 130 168Z" fill="url(#robe)" stroke="#42557c" stroke-width="2"/>
    <ellipse cx="206" cy="86" rx="38" ry="31" fill="#88c778"/>
    <ellipse cx="165" cy="81" rx="19" ry="9" fill="#88c778"/>
    <ellipse cx="247" cy="81" rx="19" ry="9" fill="#88c778"/>
    <ellipse cx="205" cy="97" rx="30" ry="18" fill="#9ad987"/>
    <circle cx="193" cy="90" r="4" fill="#101820"/>
    <circle cx="217" cy="90" r="4" fill="#101820"/>
    <path d="M193 107 Q205 114 217 107" stroke="#101820" stroke-width="3" fill="none" stroke-linecap="round"/>
    <path d="M171 56 Q206 16 242 56" fill="#25324b" stroke="#42557c" stroke-width="2"/>
    <path d="M188 129 L230 129 L242 205 L176 205 Z" fill="#2f415e"/>
  </g>
  <g transform="translate(402 42)">
    <rect x="0" y="110" width="238" height="8" rx="4" fill="url(#blade)" filter="url(#glow)"/>
    <rect x="-18" y="105" width="24" height="18" rx="3" fill="#8b96a8"/>
    <rect x="-26" y="102" width="10" height="24" rx="2" fill="#4e5666"/>
  </g>
  <g transform="translate(640 26)">
    <text x="0" y="68" fill="#ffe81f" font-size="36" font-family="Segoe UI, Arial, sans-serif" font-weight="700">Jedi Market Signal</text>
    <text x="0" y="110" fill="#e6f1ff" font-size="20" font-family="Segoe UI, Arial, sans-serif">
      Channel traffic, customer force, and revenue balance
    </text>
    <text x="0" y="146" fill="#8da7c7" font-size="16" font-family="Segoe UI, Arial, sans-serif">
      Guide the galaxy with loyalty, recency, and brand performance
    </text>
  </g>
</svg>
"""


st.set_page_config(
    page_title="MarTech_Dashboard",
    page_icon=":milky_way:",
    layout="wide",
    initial_sidebar_state="expanded",
)


def apply_star_wars_theme() -> None:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background:
                radial-gradient(circle at 20% 20%, rgba(255, 232, 31, 0.08), transparent 20%),
                radial-gradient(circle at 80% 10%, rgba(110, 200, 255, 0.10), transparent 24%),
                radial-gradient(circle at 70% 65%, rgba(167, 139, 250, 0.10), transparent 20%),
                linear-gradient(180deg, #02050b 0%, {STAR_WARS_BG} 45%, #02040a 100%);
            color: {STAR_WARS_TEXT};
        }}
        .stApp::before {{
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background-image:
                radial-gradient(2px 2px at 8% 18%, rgba(255,255,255,0.9), transparent 60%),
                radial-gradient(1.5px 1.5px at 22% 72%, rgba(255,255,255,0.7), transparent 60%),
                radial-gradient(2px 2px at 40% 28%, rgba(255,255,255,0.8), transparent 60%),
                radial-gradient(1.5px 1.5px at 58% 82%, rgba(255,255,255,0.65), transparent 60%),
                radial-gradient(2px 2px at 76% 42%, rgba(255,255,255,0.75), transparent 60%),
                radial-gradient(1.5px 1.5px at 88% 14%, rgba(255,255,255,0.7), transparent 60%);
            opacity: 0.9;
            z-index: 0;
        }}
        .block-container {{
            position: relative;
            z-index: 1;
            padding-top: 2rem;
        }}
        [data-testid="stSidebar"] {{
            background: linear-gradient(180deg, rgba(6, 12, 24, 0.98) 0%, rgba(10, 18, 34, 0.98) 100%);
            border-right: 1px solid {STAR_WARS_BORDER};
        }}
        [data-testid="stSidebar"] * {{
            color: {STAR_WARS_TEXT};
        }}
        [data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] > div,
        [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div {{
            background: {STAR_WARS_PANEL_ALT};
            border: 1px solid {STAR_WARS_BORDER};
        }}
        h1, h2, h3, label, p, span, div {{
            color: {STAR_WARS_TEXT};
        }}
        h1 {{
            letter-spacing: 0.05em;
            text-transform: uppercase;
            color: {STAR_WARS_ACCENT};
            text-shadow: 0 0 18px rgba(255, 232, 31, 0.18);
        }}
        [data-testid="stCaptionContainer"], .stCaption {{
            color: {STAR_WARS_MUTED} !important;
        }}
        [data-testid="stMetric"], .stDataFrame, [data-testid="stPlotlyChart"], .stTabs {{
            background: {STAR_WARS_PANEL};
            border: 1px solid {STAR_WARS_BORDER};
            border-radius: 18px;
            box-shadow: 0 18px 45px rgba(0,0,0,0.35);
        }}
        [data-testid="stMetric"] {{
            padding: 0.85rem 1rem;
        }}
        [data-testid="stTabs"] button[role="tab"] {{
            color: {STAR_WARS_MUTED};
            border-radius: 999px;
        }}
        [data-testid="stTabs"] button[aria-selected="true"] {{
            color: {STAR_WARS_ACCENT};
            background: rgba(255, 232, 31, 0.08);
        }}
        .stAlert {{
            background: {STAR_WARS_PANEL_ALT};
            color: {STAR_WARS_TEXT};
            border: 1px solid {STAR_WARS_BORDER};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def age_bucket(series: pd.Series) -> pd.Series:
    bins = [0, 24, 34, 44, 54, 200]
    labels = ["18-24", "25-34", "35-44", "45-54", "55+"]
    return pd.cut(series, bins=bins, labels=labels, include_lowest=True)


@st.cache_data(show_spinner="Loading CSV files and preparing the dashboard dataset...")
def load_data() -> pd.DataFrame:
    sales = pd.read_csv(
        DATA_DIR / "sales.csv",
        parse_dates=["order_date"],
        dtype={
            "order_id": "string",
            "product_id": "string",
            "store_id": "string",
            "customer_id": "string",
            "quantity": "int16",
            "unit_price": "float32",
            "discount": "float32",
            "revenue": "float32",
            "cost": "float32",
            "profit": "float32",
        },
    )

    customers = pd.read_csv(
        DATA_DIR / "customers.csv",
        parse_dates=["join_date"],
        dtype={
            "customer_id": "string",
            "age": "int16",
            "gender": "category",
            "loyalty_member": "int8",
        },
    )
    customers["loyalty_segment"] = customers["loyalty_member"].map({1: "Loyalty", 0: "Non-Loyalty"}).astype("category")
    customers["age_group"] = age_bucket(customers["age"]).astype("category")

    products = pd.read_csv(
        DATA_DIR / "products.csv",
        dtype={
            "product_id": "string",
            "product_name": "string",
            "brand": "category",
            "category": "category",
            "cocoa_percent": "int16",
            "weight_g": "int16",
        },
    )

    stores = pd.read_csv(
        DATA_DIR / "stores.csv",
        dtype={
            "store_id": "string",
            "store_name": "string",
            "city": "category",
            "country": "category",
            "store_type": "category",
        },
    )

    df = sales.merge(customers, on="customer_id", how="left").merge(products, on="product_id", how="left").merge(
        stores, on="store_id", how="left"
    )

    fill_values = {
        "gender": "Unknown",
        "loyalty_segment": "Unknown",
        "age_group": "Unknown",
        "product_name": "Unknown Product",
        "brand": "Unknown",
        "category": "Unknown",
        "city": "Unknown",
        "country": "Unknown",
        "store_type": "Unknown",
        "store_name": "Unknown Store",
    }
    for column, value in fill_values.items():
        df[column] = df[column].astype("object").fillna(value)

    df["year"] = df["order_date"].dt.year.astype("int16")
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    df["week_start"] = df["order_date"].dt.to_period("W-MON").apply(lambda period: period.start_time)
    df["order_count"] = 1

    customer_order_counts = df.groupby("customer_id", dropna=False)["order_id"].transform("count")
    df["customer_type"] = customer_order_counts.gt(1).map({True: "Returning", False: "New"})

    return df


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.title("Galactic Filters")

    years = sorted(df["year"].dropna().unique().tolist())
    countries = sorted(df["country"].dropna().unique().tolist())
    customer_types = sorted(df["customer_type"].dropna().unique().tolist())
    loyalty_segments = sorted(df["loyalty_segment"].dropna().unique().tolist())

    selected_years = st.sidebar.multiselect("Year", years, default=years)

    year_filtered = df[df["year"].isin(selected_years)].copy()

    available_countries = sorted(year_filtered["country"].dropna().unique().tolist())
    selected_countries = st.sidebar.multiselect("Country", available_countries, default=available_countries)

    country_filtered = year_filtered[year_filtered["country"].isin(selected_countries)].copy()

    available_cities = sorted(country_filtered["city"].dropna().unique().tolist())
    selected_cities = st.sidebar.multiselect("City", available_cities, default=available_cities)

    geo_filtered = country_filtered[country_filtered["city"].isin(selected_cities)].copy()

    available_brands = sorted(geo_filtered["brand"].dropna().unique().tolist())
    selected_brands = st.sidebar.multiselect("Brand", available_brands, default=available_brands)

    brand_filtered = geo_filtered[geo_filtered["brand"].isin(selected_brands)].copy()

    available_categories = sorted(brand_filtered["category"].dropna().unique().tolist())
    selected_categories = st.sidebar.multiselect("Category", available_categories, default=available_categories)

    category_filtered = brand_filtered[brand_filtered["category"].isin(selected_categories)].copy()

    available_store_types = sorted(category_filtered["store_type"].dropna().unique().tolist())
    selected_store_types = st.sidebar.multiselect("Store Type", available_store_types, default=available_store_types)

    store_filtered = category_filtered[category_filtered["store_type"].isin(selected_store_types)].copy()

    selected_customer_types = st.sidebar.multiselect("Customer Type", customer_types, default=customer_types)
    selected_loyalty_segments = st.sidebar.multiselect("Loyalty", loyalty_segments, default=loyalty_segments)

    filtered = store_filtered[
        store_filtered["customer_type"].isin(selected_customer_types)
        & store_filtered["loyalty_segment"].isin(selected_loyalty_segments)
    ].copy()

    st.sidebar.caption(f"Rows in sector view: {len(filtered):,}")
    st.sidebar.caption(f"Countries: {filtered['country'].nunique():,} | Cities: {filtered['city'].nunique():,} | Brands: {filtered['brand'].nunique():,}")
    return filtered


def metric_card(label: str, value: str) -> None:
    st.markdown(
        f"""
        <div style="padding:1rem 1.1rem;border-radius:18px;background:rgba(11,18,32,0.92);
        border:1px solid {STAR_WARS_BORDER};box-shadow:0 18px 45px rgba(0,0,0,0.35);">
            <div style="font-size:0.8rem;color:{STAR_WARS_MUTED};text-transform:uppercase;letter-spacing:0.12em;">{label}</div>
            <div style="font-size:2rem;font-weight:700;color:{STAR_WARS_ACCENT};margin-top:0.35rem;">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_figure(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=STAR_WARS_TEXT,
        legend_title_text="",
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=STAR_WARS_TEXT)),
        margin=dict(l=10, r=10, t=10, b=10),
    )
    fig.update_xaxes(showgrid=False, color=STAR_WARS_MUTED, zeroline=False)
    fig.update_yaxes(gridcolor="rgba(110,189,255,0.12)", color=STAR_WARS_MUTED, zeroline=False)
    return fig


def revenue_trend_chart(df: pd.DataFrame, freq: str) -> go.Figure:
    time_col = "month" if freq == "Monthly" else "week_start"
    trend = (
        df.groupby(time_col, as_index=False)
        .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), orders=("order_count", "sum"))
        .sort_values(time_col)
    )
    fig = px.line(
        trend,
        x=time_col,
        y=["revenue", "profit"],
        markers=True,
        color_discrete_sequence=[COLOR_PRIMARY, COLOR_SECONDARY],
        template=PLOTLY_TEMPLATE,
    )
    return style_figure(fig)


def bar_chart(df: pd.DataFrame, x: str, y: str, color: str | None = None, horizontal: bool = False) -> go.Figure:
    chart = px.bar(
        df,
        x=y if horizontal else x,
        y=x if horizontal else y,
        color=color,
        color_discrete_sequence=COLOR_SCALE,
        template=PLOTLY_TEMPLATE,
        text_auto=".2s",
    )
    chart.update_layout(showlegend=color is not None)
    return style_figure(chart)


def pie_chart(df: pd.DataFrame, names: str, values: str) -> go.Figure:
    chart = px.pie(
        df,
        names=names,
        values=values,
        hole=0.58,
        color=names,
        color_discrete_sequence=COLOR_SCALE,
        template=PLOTLY_TEMPLATE,
    )
    chart.update_traces(textfont_color=STAR_WARS_TEXT, marker=dict(line=dict(color=STAR_WARS_BG, width=2)))
    return style_figure(chart)


def format_currency(value: float) -> str:
    return f"${value:,.0f}"


def score_series(series: pd.Series, ascending: bool = True) -> pd.Series:
    ranked = series.rank(method="first", ascending=ascending)
    return pd.qcut(ranked, 5, labels=[1, 2, 3, 4, 5]).astype(int)


def rfm_segment(recency_score: int, frequency_score: int, monetary_score: int) -> str:
    if recency_score >= 4 and frequency_score >= 4 and monetary_score >= 4:
        return "Champions"
    if recency_score >= 3 and frequency_score >= 3 and monetary_score >= 3:
        return "Loyal"
    if recency_score >= 4 and frequency_score <= 2:
        return "Promising"
    if recency_score <= 2 and frequency_score >= 4 and monetary_score >= 3:
        return "At Risk"
    if recency_score <= 2 and frequency_score <= 2 and monetary_score <= 2:
        return "Hibernating"
    return "Potential Loyalists"


def build_rfm(df: pd.DataFrame) -> pd.DataFrame:
    snapshot_date = df["order_date"].max() + pd.Timedelta(days=1)
    customer_rfm = (
        df.groupby("customer_id", as_index=False)
        .agg(
            last_order_date=("order_date", "max"),
            frequency=("order_id", "nunique"),
            monetary=("revenue", "sum"),
        )
        .sort_values("monetary", ascending=False)
    )
    customer_rfm["recency_days"] = (snapshot_date - customer_rfm["last_order_date"]).dt.days
    customer_rfm["recency_score"] = score_series(customer_rfm["recency_days"], ascending=False)
    customer_rfm["frequency_score"] = score_series(customer_rfm["frequency"], ascending=True)
    customer_rfm["monetary_score"] = score_series(customer_rfm["monetary"], ascending=True)
    customer_rfm["rfm_score"] = (
        customer_rfm["recency_score"].astype(str)
        + customer_rfm["frequency_score"].astype(str)
        + customer_rfm["monetary_score"].astype(str)
    )
    customer_rfm["rfm_segment"] = customer_rfm.apply(
        lambda row: rfm_segment(row["recency_score"], row["frequency_score"], row["monetary_score"]),
        axis=1,
    )
    customer_rfm["rfm_name"] = customer_rfm["rfm_segment"].map(RFM_SEGMENT_NAMES).fillna(customer_rfm["rfm_segment"])
    return customer_rfm


def scale_to_score(series: pd.Series, reverse: bool = False) -> pd.Series:
    numeric = series.astype(float)
    if numeric.nunique(dropna=False) <= 1:
        return pd.Series([5.5] * len(numeric), index=series.index)
    scaled = 1 + (numeric - numeric.min()) * 9 / (numeric.max() - numeric.min())
    if reverse:
        scaled = 11 - scaled
    return scaled.clip(1, 10).round(1)


def build_brand_positioning(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df["brand"] != "Unknown"].copy()
    brand = (
        df.groupby("brand", as_index=False)
        .agg(
            products=("product_id", "nunique"),
            revenue=("revenue", "sum"),
            profit=("profit", "sum"),
            orders=("order_id", "nunique"),
            quantity=("quantity", "sum"),
            avg_unit_price=("unit_price", "mean"),
            avg_discount=("discount", "mean"),
            avg_cocoa=("cocoa_percent", "mean"),
            cocoa_std=("cocoa_percent", "std"),
            avg_weight=("weight_g", "mean"),
            category_count=("category", "nunique"),
        )
        .fillna({"cocoa_std": 0})
    )
    brand["profit_margin"] = brand["profit"] / brand["revenue"]
    brand["revenue_per_order"] = brand["revenue"] / brand["orders"]
    brand["product_breadth"] = brand["products"] / brand["products"].max()
    brand["category_breadth"] = brand["category_count"] / brand["category_count"].max()

    brand["taste_intensity"] = scale_to_score(brand["avg_cocoa"])
    brand["sweetness_approach"] = scale_to_score(brand["avg_cocoa"], reverse=True)
    brand["texture_variety"] = scale_to_score(brand["category_count"] * 0.7 + brand["cocoa_std"] * 0.3)
    brand["quality_premium"] = scale_to_score(brand["avg_unit_price"] * 0.45 + brand["profit_margin"] * 100 * 0.35 + brand["avg_cocoa"] * 0.20)
    brand["health_lightness"] = scale_to_score(brand["avg_cocoa"] * 0.65 + (1 - brand["avg_discount"]) * 10 * 0.35)
    brand["daily_accessibility"] = scale_to_score(
        brand["avg_unit_price"] * 0.45 + brand["revenue_per_order"] * 0.30 + brand["avg_discount"] * -10 * 0.25,
        reverse=True,
    )
    brand["gifting_fit"] = scale_to_score(brand["avg_unit_price"] * 0.45 + brand["avg_weight"] * 0.35 + brand["profit_margin"] * 100 * 0.20)
    brand["innovation_variety"] = scale_to_score(brand["product_breadth"] * 10 * 0.35 + brand["category_breadth"] * 10 * 0.35 + brand["cocoa_std"] * 0.30)
    brand["profit_power"] = scale_to_score(brand["profit_margin"] * 100)
    brand["market_momentum"] = scale_to_score(brand["revenue"] * 0.55 + brand["orders"] * 0.45)

    brand["position_x_premium"] = (brand["quality_premium"] * 0.55 + brand["gifting_fit"] * 0.45).round(1)
    brand["position_y_accessibility"] = (brand["daily_accessibility"] * 0.7 + brand["market_momentum"] * 0.3).round(1)

    return brand.sort_values("revenue", ascending=False)


def build_growth_tables(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    monthly = (
        df.assign(month_period=df["order_date"].dt.to_period("M"))
        .groupby("month_period", as_index=False)
        .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), orders=("order_count", "sum"))
        .sort_values("month_period")
    )
    monthly["period"] = monthly["month_period"].astype(str)
    monthly["mom_growth"] = (monthly["revenue"].pct_change() * 100).round(1)
    monthly["yoy_growth"] = (monthly["revenue"].pct_change(12) * 100).round(1)

    quarterly = (
        df.assign(quarter_period=df["order_date"].dt.to_period("Q"))
        .groupby("quarter_period", as_index=False)
        .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), orders=("order_count", "sum"))
        .sort_values("quarter_period")
    )
    quarterly["period"] = quarterly["quarter_period"].astype(str)
    quarterly["qoq_growth"] = (quarterly["revenue"].pct_change() * 100).round(1)
    quarterly["yoy_growth"] = (quarterly["revenue"].pct_change(4) * 100).round(1)

    return monthly, quarterly


def build_brand_growth_tables(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    base = df[df["brand"] != "Unknown"].copy()

    monthly = (
        base.assign(month_period=base["order_date"].dt.to_period("M"))
        .groupby(["brand", "month_period"], as_index=False)
        .agg(revenue=("revenue", "sum"))
        .sort_values(["brand", "month_period"])
    )
    monthly["period"] = monthly["month_period"].astype(str)
    monthly["mom_growth"] = (monthly.groupby("brand")["revenue"].pct_change() * 100).round(1)
    monthly["yoy_growth"] = (monthly.groupby("brand")["revenue"].pct_change(12) * 100).round(1)

    quarterly = (
        base.assign(quarter_period=base["order_date"].dt.to_period("Q"))
        .groupby(["brand", "quarter_period"], as_index=False)
        .agg(revenue=("revenue", "sum"))
        .sort_values(["brand", "quarter_period"])
    )
    quarterly["period"] = quarterly["quarter_period"].astype(str)
    quarterly["qoq_growth"] = (quarterly.groupby("brand")["revenue"].pct_change() * 100).round(1)
    quarterly["yoy_growth"] = (quarterly.groupby("brand")["revenue"].pct_change(4) * 100).round(1)

    return monthly, quarterly


def executive_tab(df: pd.DataFrame) -> None:
    total_revenue = float(df["revenue"].sum())
    total_profit = float(df["profit"].sum())
    total_orders = int(df["order_id"].nunique())
    avg_order_value = total_revenue / total_orders if total_orders else 0
    monthly, quarterly = build_growth_tables(df)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Revenue", format_currency(total_revenue))
    with c2:
        metric_card("Profit", format_currency(total_profit))
    with c3:
        metric_card("Orders", f"{total_orders:,}")
    with c4:
        metric_card("Avg Order Value", format_currency(avg_order_value))

    brand_perf = (
        df.groupby("brand", as_index=False)
        .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), orders=("order_count", "sum"))
        .sort_values("revenue", ascending=False)
        .head(8)
    )
    channel_perf = (
        df.groupby("store_type", as_index=False)
        .agg(revenue=("revenue", "sum"))
        .sort_values("revenue", ascending=False)
    )
    country_perf = (
        df.groupby("country", as_index=False)
        .agg(revenue=("revenue", "sum"))
        .sort_values("revenue", ascending=False)
    )
    customer_mix = (
        df.groupby("customer_type", as_index=False)
        .agg(revenue=("revenue", "sum"))
        .sort_values("revenue", ascending=False)
    )
    loyalty_mix = (
        df.groupby("loyalty_segment", as_index=False)
        .agg(revenue=("revenue", "sum"))
        .sort_values("revenue", ascending=False)
    )
    latest_mom = monthly.dropna(subset=["mom_growth"]).tail(1)
    latest_yoy = monthly.dropna(subset=["yoy_growth"]).tail(1)
    latest_qoq = quarterly.dropna(subset=["qoq_growth"]).tail(1)

    col_a, col_b = st.columns([1.35, 1])
    with col_a:
        st.subheader("Top brands by revenue")
        st.plotly_chart(bar_chart(brand_perf, "brand", "revenue"), use_container_width=True, key="executive-top-brands")
    with col_b:
        st.subheader("Command highlights")
        margin = (total_profit / total_revenue * 100) if total_revenue else 0
        customers = int(df["customer_id"].nunique())
        countries = int(df["country"].nunique())
        top_brand = brand_perf.iloc[0]["brand"] if not brand_perf.empty else "N/A"
        st.metric("Profit Margin", f"{margin:.1f}%")
        st.metric("Customers", f"{customers:,}")
        st.metric("Countries", f"{countries:,}")
        st.metric("Top Brand", str(top_brand))

    top_brand_name = brand_perf.iloc[0]["brand"] if not brand_perf.empty else "N/A"
    top_brand_revenue = brand_perf.iloc[0]["revenue"] if not brand_perf.empty else 0
    top_channel_name = channel_perf.iloc[0]["store_type"] if not channel_perf.empty else "N/A"
    top_country_name = country_perf.iloc[0]["country"] if not country_perf.empty else "N/A"
    top_customer_type = customer_mix.iloc[0]["customer_type"] if not customer_mix.empty else "N/A"
    top_loyalty_type = loyalty_mix.iloc[0]["loyalty_segment"] if not loyalty_mix.empty else "N/A"
    mom_text = f"{latest_mom.iloc[0]['mom_growth']:.1f}%" if not latest_mom.empty else "N/A"
    yoy_text = f"{latest_yoy.iloc[0]['yoy_growth']:.1f}%" if not latest_yoy.empty else "N/A"
    qoq_text = f"{latest_qoq.iloc[0]['qoq_growth']:.1f}%" if not latest_qoq.empty else "N/A"
    brand_share = (top_brand_revenue / total_revenue * 100) if total_revenue else 0

    st.subheader("Plain-English Summary")
    st.markdown(
        f"""
        <div style="padding:1.2rem 1.3rem;border-radius:18px;background:{STAR_WARS_PANEL_ALT};
        border:1px solid {STAR_WARS_BORDER};line-height:1.8;">
            <div style="font-size:1.05rem;color:{STAR_WARS_TEXT};font-weight:700;margin-bottom:0.65rem;">
                What this means for a non-marketer
            </div>
            <div style="color:{STAR_WARS_TEXT};">
                This dashboard is showing a business that generated <strong>{format_currency(total_revenue)}</strong> in sales
                from <strong>{total_orders:,}</strong> orders, with an average basket of <strong>{format_currency(avg_order_value)}</strong>.
                Profit is <strong>{format_currency(total_profit)}</strong>, so the business is keeping about
                <strong>{margin:.1f}%</strong> of revenue after product cost.
            </div>
            <div style="color:{STAR_WARS_TEXT};margin-top:0.6rem;">
                Right now, the strongest brand in this filtered view is <strong>{top_brand_name}</strong>, contributing about
                <strong>{brand_share:.1f}%</strong> of total revenue. The biggest sales channel is <strong>{top_channel_name}</strong>,
                and the strongest market is <strong>{top_country_name}</strong>.
            </div>
            <div style="color:{STAR_WARS_TEXT};margin-top:0.6rem;">
                From a customer angle, revenue is currently led by <strong>{top_customer_type}</strong> shoppers, while
                <strong>{top_loyalty_type}</strong> customers are the biggest membership group by sales. That tells us where repeat demand is really coming from.
            </div>
            <div style="color:{STAR_WARS_TEXT};margin-top:0.6rem;">
                Looking at growth, the latest movement is <strong>MoM {mom_text}</strong>,
                <strong>QoQ {qoq_text}</strong>, and <strong>YoY {yoy_text}</strong>.
                In simple terms: MoM shows short-term monthly change, QoQ shows quarter-to-quarter momentum, and YoY tells you whether the business is bigger or smaller than the same time last year.
            </div>
            <div style="color:{STAR_WARS_MUTED};margin-top:0.75rem;">
                If you only remember one thing: check whether the top brand, top channel, and latest YoY are moving in the same direction. That usually tells you whether growth is broad-based or relying on just one pocket of demand.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def trends_tab(df: pd.DataFrame) -> None:
    freq = st.radio("Trend Grain", ["Monthly", "Weekly"], horizontal=True)
    st.plotly_chart(revenue_trend_chart(df, freq), use_container_width=True, key=f"trends-revenue-{freq.lower()}")

    weekly_orders = (
        df.groupby("week_start", as_index=False).agg(orders=("order_count", "sum")).sort_values("week_start").tail(16)
    )
    st.subheader("Recent order velocity")
    st.plotly_chart(bar_chart(weekly_orders, "week_start", "orders"), use_container_width=True, key="trends-weekly-orders")


def growth_trends_tab(df: pd.DataFrame) -> None:
    monthly, quarterly = build_growth_tables(df)
    brand_monthly, brand_quarterly = build_brand_growth_tables(df)

    latest_month = monthly.dropna(subset=["mom_growth"]).tail(1)
    latest_yoy_month = monthly.dropna(subset=["yoy_growth"]).tail(1)
    latest_quarter = quarterly.dropna(subset=["qoq_growth"]).tail(1)

    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Latest MoM", f"{latest_month['mom_growth'].iloc[0]:.1f}%" if not latest_month.empty else "N/A")
    with c2:
        metric_card("Latest QoQ", f"{latest_quarter['qoq_growth'].iloc[0]:.1f}%" if not latest_quarter.empty else "N/A")
    with c3:
        metric_card("Latest YoY", f"{latest_yoy_month['yoy_growth'].iloc[0]:.1f}%" if not latest_yoy_month.empty else "N/A")

    st.subheader("Revenue trend with YoY baseline")
    trend_fig = go.Figure()
    trend_fig.add_trace(
        go.Scatter(
            x=monthly["period"],
            y=monthly["revenue"],
            mode="lines+markers",
            name="Revenue",
            line=dict(color=COLOR_PRIMARY, width=3),
        )
    )
    trend_fig.add_trace(
        go.Scatter(
            x=monthly["period"],
            y=monthly["profit"],
            mode="lines+markers",
            name="Profit",
            line=dict(color=COLOR_SECONDARY, width=2),
        )
    )
    st.plotly_chart(style_figure(trend_fig), use_container_width=True, key="growth-revenue-trend")

    left, right = st.columns(2)
    with left:
        st.subheader("Monthly growth view")
        monthly_growth_fig = go.Figure()
        monthly_growth_fig.add_trace(
            go.Bar(
                x=monthly["period"],
                y=monthly["mom_growth"],
                name="MoM %",
                marker_color=COLOR_SECONDARY,
                opacity=0.75,
            )
        )
        monthly_growth_fig.add_trace(
            go.Scatter(
                x=monthly["period"],
                y=monthly["yoy_growth"],
                name="YoY %",
                mode="lines+markers",
                line=dict(color=COLOR_PRIMARY, width=3),
            )
        )
        monthly_growth_fig.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.25)")
        monthly_growth_fig.update_layout(
            yaxis_title="Growth %",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(style_figure(monthly_growth_fig), use_container_width=True, key="growth-mom-yoy-redraw")
    with right:
        st.subheader("Quarterly growth view")
        quarterly_growth_fig = go.Figure()
        quarterly_growth_fig.add_trace(
            go.Bar(
                x=quarterly["period"],
                y=quarterly["qoq_growth"],
                name="QoQ %",
                marker_color=COLOR_TERTIARY,
                opacity=0.8,
            )
        )
        quarterly_growth_fig.add_trace(
            go.Scatter(
                x=quarterly["period"],
                y=quarterly["yoy_growth"],
                name="YoY %",
                mode="lines+markers",
                line=dict(color=COLOR_PRIMARY, width=3),
            )
        )
        quarterly_growth_fig.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.25)")
        quarterly_growth_fig.update_layout(
            yaxis_title="Growth %",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(style_figure(quarterly_growth_fig), use_container_width=True, key="growth-qoq-yoy-redraw")

    st.subheader("Growth detail table")
    growth_table = monthly.loc[:, ["period", "revenue", "profit", "orders", "mom_growth", "yoy_growth"]].copy()
    growth_table["revenue"] = growth_table["revenue"].map(format_currency)
    growth_table["profit"] = growth_table["profit"].map(format_currency)
    st.dataframe(growth_table, use_container_width=True, hide_index=True)

    st.subheader("Brand growth comparison")
    st.caption("Select a growth lens and compare multiple brands on the same trend chart.")

    brand_options = sorted(brand_monthly["brand"].dropna().unique().tolist())
    selected_growth = st.radio(
        "Growth Metric",
        ["MoM", "QoQ", "YoY"],
        horizontal=True,
        key="brand-growth-metric",
    )
    selected_brands = st.multiselect(
        "Brands",
        brand_options,
        default=brand_options[: min(4, len(brand_options))],
        key="brand-growth-selection",
    )

    if not selected_brands:
        st.info("Select at least one brand to display the growth trend.")
        return

    if selected_growth == "QoQ":
        brand_growth = brand_quarterly[brand_quarterly["brand"].isin(selected_brands)].copy()
        metric_col = "qoq_growth"
    elif selected_growth == "YoY":
        if brand_monthly["yoy_growth"].notna().sum() >= brand_quarterly["yoy_growth"].notna().sum():
            brand_growth = brand_monthly[brand_monthly["brand"].isin(selected_brands)].copy()
            metric_col = "yoy_growth"
        else:
            brand_growth = brand_quarterly[brand_quarterly["brand"].isin(selected_brands)].copy()
            metric_col = "yoy_growth"
    else:
        brand_growth = brand_monthly[brand_monthly["brand"].isin(selected_brands)].copy()
        metric_col = "mom_growth"

    brand_growth = brand_growth.dropna(subset=[metric_col])
    if brand_growth.empty:
        st.warning("Not enough history to calculate the selected growth metric for the chosen brands.")
        return

    brand_fig = px.line(
        brand_growth,
        x="period",
        y=metric_col,
        color="brand",
        markers=True,
        color_discrete_sequence=COLOR_SCALE,
        template=PLOTLY_TEMPLATE,
    )
    brand_fig.update_layout(
        yaxis_title=f"{selected_growth} Growth %",
        xaxis_title="Period",
    )
    brand_fig.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.25)")
    st.plotly_chart(style_figure(brand_fig), use_container_width=True, key="brand-growth-trend-chart")


def customers_tab(df: pd.DataFrame) -> None:
    loyalty = (
        df.groupby("loyalty_segment", as_index=False)
        .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), orders=("order_count", "sum"))
        .sort_values("revenue", ascending=False)
    )
    customer_type = (
        df.groupby("customer_type", as_index=False)
        .agg(customers=("customer_id", "nunique"), revenue=("revenue", "sum"))
        .sort_values("revenue", ascending=False)
    )
    age_mix = df.groupby("age_group", as_index=False).agg(revenue=("revenue", "sum")).sort_values("age_group")
    gender_mix = df.groupby("gender", as_index=False).agg(revenue=("revenue", "sum")).sort_values("revenue", ascending=False)
    rfm = build_rfm(df)
    rfm_summary = (
        rfm.groupby(["rfm_segment", "rfm_name"], as_index=False)
        .agg(customers=("customer_id", "nunique"), revenue=("monetary", "sum"), avg_recency_days=("recency_days", "mean"))
        .sort_values("revenue", ascending=False)
    )

    left, right = st.columns(2)
    with left:
        st.subheader("Loyalty vs non-loyalty")
        st.plotly_chart(pie_chart(loyalty, "loyalty_segment", "revenue"), use_container_width=True, key="customers-loyalty")
    with right:
        st.subheader("New vs returning customers")
        st.plotly_chart(
            bar_chart(customer_type, "customer_type", "revenue"),
            use_container_width=True,
            key="customers-new-vs-returning",
        )

    lower_left, lower_right = st.columns(2)
    with lower_left:
        st.subheader("Age segments")
        st.plotly_chart(bar_chart(age_mix, "age_group", "revenue"), use_container_width=True, key="customers-age-segments")
    with lower_right:
        st.subheader("Gender segments")
        st.plotly_chart(
            bar_chart(gender_mix, "gender", "revenue"),
            use_container_width=True,
            key="customers-gender-segments",
        )

    st.subheader("顧客 RFM 命名與分群")
    st.caption("Grouped by recency, frequency, and monetary value using quintile scores on the filtered dataset.")

    st.dataframe(
        pd.DataFrame([{"RFM Segment": segment, "顧客 RFM 命名": name} for segment, name in RFM_SEGMENT_NAMES.items()]),
        use_container_width=True,
        hide_index=True,
    )

    segment_left, segment_right = st.columns([1.1, 1.2])
    with segment_left:
        st.plotly_chart(bar_chart(rfm_summary, "rfm_name", "revenue"), use_container_width=True, key="customers-rfm-segments")
    with segment_right:
        scatter = px.scatter(
            rfm,
            x="frequency",
            y="monetary",
            color="rfm_name",
            size="recency_days",
            hover_data=["customer_id", "rfm_score", "rfm_segment"],
            color_discrete_sequence=COLOR_SCALE,
            template=PLOTLY_TEMPLATE,
        )
        st.plotly_chart(style_figure(scatter), use_container_width=True, key="customers-rfm-scatter")

    st.dataframe(
        rfm.loc[:, ["customer_id", "recency_days", "frequency", "monetary", "rfm_score", "rfm_segment", "rfm_name"]]
        .sort_values(["monetary", "frequency"], ascending=[False, False])
        .head(50)
        .assign(monetary=lambda table: table["monetary"].map(format_currency)),
        use_container_width=True,
        hide_index=True,
    )


def products_tab(df: pd.DataFrame) -> None:
    brand_perf = (
        df.groupby("brand", as_index=False)
        .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), orders=("order_count", "sum"))
        .sort_values("revenue", ascending=False)
        .head(12)
    )
    category_perf = (
        df.groupby("category", as_index=False)
        .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), orders=("order_count", "sum"))
        .sort_values("revenue", ascending=False)
    )

    left, right = st.columns(2)
    with left:
        st.subheader("Brand revenue")
        st.plotly_chart(bar_chart(brand_perf, "brand", "revenue"), use_container_width=True, key="products-brand-revenue")
    with right:
        st.subheader("Category revenue")
        st.plotly_chart(
            bar_chart(category_perf, "category", "revenue"),
            use_container_width=True,
            key="products-category-revenue",
        )

    st.subheader("Top brand table")
    st.dataframe(
        brand_perf.assign(
            revenue=brand_perf["revenue"].map(format_currency),
            profit=brand_perf["profit"].map(format_currency),
        ),
        use_container_width=True,
        hide_index=True,
    )


def channel_geo_tab(df: pd.DataFrame) -> None:
    channel_perf = (
        df.groupby("store_type", as_index=False)
        .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), orders=("order_count", "sum"))
        .sort_values("revenue", ascending=False)
    )
    country_perf = (
        df.groupby("country", as_index=False)
        .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), orders=("order_count", "sum"))
        .sort_values("revenue", ascending=False)
        .head(12)
    )

    left, right = st.columns(2)
    with left:
        st.subheader("Store type mix")
        st.plotly_chart(
            pie_chart(channel_perf, "store_type", "revenue"),
            use_container_width=True,
            key="channel-geo-store-type",
        )
    with right:
        st.subheader("Country revenue")
        st.plotly_chart(
            bar_chart(country_perf, "country", "revenue", horizontal=True),
            use_container_width=True,
            key="channel-geo-country-revenue",
        )


def brand_positioning_tab(df: pd.DataFrame) -> None:
    brand = build_brand_positioning(df)

    st.subheader("品牌定位評分")
    st.caption("1-10 分為相對分數，依目前資料中的產品組合、價格、可可濃度、折扣、銷售與獲利表現推估。")

    score_columns = {
        "brand": "品牌",
        "taste_intensity": "口味濃度",
        "sweetness_approach": "甜感親和",
        "texture_variety": "口感多樣性",
        "quality_premium": "品質精品感",
        "health_lightness": "健康輕負擔",
        "daily_accessibility": "日常可近性",
        "gifting_fit": "送禮體面感",
        "innovation_variety": "創新多樣性",
        "profit_power": "獲利能力",
        "market_momentum": "市場動能",
    }
    st.dataframe(brand.loc[:, score_columns.keys()].rename(columns=score_columns), use_container_width=True, hide_index=True)

    st.subheader("品牌定位圖")
    st.caption("X 軸代表精品感，Y 軸代表大眾可近性，泡泡大小代表市場動能。")

    fig = px.scatter(
        brand,
        x="position_x_premium",
        y="position_y_accessibility",
        size="market_momentum",
        color="brand",
        text="brand",
        hover_data={
            "quality_premium": True,
            "daily_accessibility": True,
            "gifting_fit": True,
            "taste_intensity": True,
            "market_momentum": True,
            "position_x_premium": False,
            "position_y_accessibility": False,
        },
        color_discrete_sequence=COLOR_SCALE,
        template=PLOTLY_TEMPLATE,
    )
    fig.update_traces(textposition="top center")
    fig.update_layout(
        xaxis_title="精品感 / Premium Positioning",
        yaxis_title="大眾可近性 / Mass Accessibility",
    )
    fig.add_hline(y=5.5, line_dash="dash", line_color="rgba(110,189,255,0.35)")
    fig.add_vline(x=5.5, line_dash="dash", line_color="rgba(110,189,255,0.35)")
    st.plotly_chart(style_figure(fig), use_container_width=True, key="brand-positioning-map")

    st.subheader("定位解讀")
    highlight = brand.loc[:, ["brand", "position_x_premium", "position_y_accessibility", "market_momentum"]].copy()
    highlight["定位特色"] = highlight.apply(
        lambda row: (
            "高精品 / 高普及" if row["position_x_premium"] >= 5.5 and row["position_y_accessibility"] >= 5.5
            else "高精品 / 低普及" if row["position_x_premium"] >= 5.5
            else "大眾 / 高普及" if row["position_y_accessibility"] >= 5.5
            else "大眾 / 利基"
        ),
        axis=1,
    )
    st.dataframe(highlight.rename(columns={"brand": "品牌", "position_x_premium": "精品感", "position_y_accessibility": "可近性", "market_momentum": "市場動能"}), use_container_width=True, hide_index=True)


def main() -> None:
    apply_star_wars_theme()
    st.title("Galactic MarTech Command Center")
    st.caption("Chocolate sales performance dashboard restyled as a Star Wars command console.")
    st.image(JEDI_PANEL_SVG, use_container_width=True)

    df = load_data()
    filtered = apply_filters(df)

    if filtered.empty:
        st.warning("No data matched the current filters.")
        return

    tabs = st.tabs(
        [
            "Executive KPIs",
            "Sales Trends",
            "YoY MoM QoQ",
            "Customer Analytics",
            "Brand Positioning",
            "Product & Brand Performance",
            "Channel & Geo",
        ]
    )

    with tabs[0]:
        executive_tab(filtered)
    with tabs[1]:
        trends_tab(filtered)
    with tabs[2]:
        growth_trends_tab(filtered)
    with tabs[3]:
        customers_tab(filtered)
    with tabs[4]:
        brand_positioning_tab(filtered)
    with tabs[5]:
        products_tab(filtered)
    with tabs[6]:
        channel_geo_tab(filtered)


if __name__ == "__main__":
    main()
