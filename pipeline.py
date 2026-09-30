import sqlite3
import numpy as np
import pandas as pd
import requests

START_DATE, END_DATE = "2024-05-01", "2024-08-31"
DB_PATH = "business_data.db"

CITY_COORDS = {
    "Paris": (48.8566, 2.3522),
    "Lyon": (45.7640, 4.8357),
    "Marseille": (43.2965, 5.3698),
    "Bordeaux": (44.8378, -0.5792),
    "Lille": (50.6292, 3.0573),
    "Nantes": (47.2184, -1.5536),
    "Toulouse": (43.6047, 1.4442),
    "Nice": (43.7102, 7.2620),
}


# ---------- EXTRACT ----------
def fetch_weather_for_city(city):
    """Fetch daily weather for ONE city."""
    lat, lon = CITY_COORDS[city]
    r = requests.get(
        "https://archive-api.open-meteo.com/v1/archive",
        params={
            "latitude": lat,
            "longitude": lon,
            "start_date": START_DATE,
            "end_date": END_DATE,
            "daily": "temperature_2m_max,temperature_2m_min,rain_sum,wind_speed_10m_max",
        },
        timeout=30,
    )
    r.raise_for_status()
    df = pd.DataFrame(r.json()["daily"]).rename(columns={
        "time": "Date",
        "temperature_2m_max": "Temp Max",
        "temperature_2m_min": "Temp Min",
        "rain_sum": "Precipitations",
        "wind_speed_10m_max": "Vent Max",
    })
    df["Date"] = pd.to_datetime(df["Date"])
    df["Ville"] = city
    return df[["Date", "Ville", "Temp Max", "Temp Min", "Precipitations", "Vent Max"]]


def fetch_all_weather():
    """Loop over all cities and stack the results."""
    return pd.concat([fetch_weather_for_city(c) for c in CITY_COORDS], ignore_index=True)


def extract():
    sales = pd.read_csv("sales.csv", parse_dates=["date"])
    sales = sales[sales["date"].between(START_DATE, END_DATE)].copy()

    marketing = pd.read_csv("marketing_campaigns.csv", parse_dates=["date"])
    marketing = marketing[marketing["date"].between(START_DATE, END_DATE)].copy()

    return {
        "sales_df": sales,
        "marketing_campaign_df": marketing,
        "weather_df": fetch_all_weather(),
    }


def init_database():
    """Create the stores and products tables from the .sql files and read them back."""
    conn = sqlite3.connect(DB_PATH)
    try:
        with open("stores.sql", encoding="utf-8") as f:
            conn.executescript(f.read())
        with open("products.sql", encoding="utf-8") as f:
            conn.executescript(f.read())
        stores_df = pd.read_sql("SELECT * FROM stores", conn)
        products_df = pd.read_sql("SELECT * FROM products", conn)
    finally:
        conn.close()
    return stores_df, products_df


# ---------- TRANSFORM ----------
def transform(data, stores_df, products_df):
    stores_df = stores_df.copy()
    stores_df["opening_date"] = pd.to_datetime(stores_df["opening_date"])

    # Rename weather keys so they match the sales columns (one copy of each key after merge)
    weather = data["weather_df"].rename(columns={"Date": "date", "Ville": "city"})

    df = (
        data["sales_df"]
        .merge(stores_df, on="store_id")
        .merge(products_df, on="product_id")
    )
    df = df.merge(weather, on=["city", "date"], how="left")

    df["is_weekend"] = np.where(df["date"].dt.dayofweek >= 5, 1, 0)
    df["temp_bucket"] = pd.cut(
        df["Temp Max"],
        bins=[-np.inf, 20, 25, 30, np.inf],
        labels=["<=20°C", "20-25°C", "25-30°C", ">30°C"],
    ).astype(str)
    df["rain_bucket"] = pd.cut(
        df["Precipitations"],
        bins=[-np.inf, 5, 20, np.inf],
        labels=["0-5 mm", "5-20 mm", ">20 mm"],
    ).astype(str)
    return df


def sales_kpis(df, group_cols):
    """Revenue, quantity and number of transactions for a given grouping."""
    return (
        df.groupby(group_cols)
        .agg(
            total_revenue=("revenue", "sum"),
            total_quantity=("quantity_sold", "sum"),
            nb_transactions=("sale_id", "count"),
        )
        .reset_index()
    )


def aggregate(final_merge):
    """Build the aggregated tables from the enriched sales data."""
    return {
        "sales_by_date": sales_kpis(final_merge, ["date"]),
        "sales_by_store": sales_kpis(final_merge, ["store_name"]),
        "sales_by_product": sales_kpis(final_merge, ["product_name"]),
        "sales_by_city": sales_kpis(final_merge, ["city"]),
        "sales_by_all": sales_kpis(final_merge, ["date", "store_name", "city", "product_name"]),
    }


# ---------- LOAD ----------
def check_columns(df, table_name):
    """SQLite column names are case-insensitive: fail early with a clear message."""
    dupes = df.columns[df.columns.str.lower().duplicated()]
    if len(dupes):
        raise ValueError(f"[{table_name}] duplicate column names (case-insensitive): {list(dupes)}")


def load(tables):
    """Write each DataFrame of the dict {table_name: df} to its own SQLite table."""
    conn = sqlite3.connect(DB_PATH)
    try:
        for table_name, df in tables.items():
            check_columns(df, table_name)
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            print(f"{table_name}: {len(df)} rows saved")
    finally:
        conn.close()


if __name__ == "__main__":
    stores_df, products_df = init_database()
    data = extract()
    final_merge = transform(data, stores_df, products_df)
    aggregates = aggregate(final_merge)

    load({
        "final_consolidated": final_merge,
        **aggregates,
    })