"""
Hotel IQ - data loading, cleaning, and metric computation helpers.
All numbers shown on the dashboard are computed here from the raw CSV.
"""

import pandas as pd
import numpy as np
import streamlit as st

MONTH_ORDER = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


@st.cache_data
def load_and_clean(path: str = "data/hotel_bookings_data.csv") -> pd.DataFrame:
    """Load the raw hotel bookings CSV and apply the cleaning steps:
    - drop duplicate rows
    - drop bookings with zero total guests
    - drop invalid adr (negative or extreme outliers)
    - fill missing children / city / agent / company
    - recategorise 'Undefined' meal entries
    - add a total_nights column
    """
    df = pd.read_csv(path)

    df = df.drop_duplicates()

    guest_total = df["adults"] + df["children"].fillna(0) + df["babies"]
    df = df[guest_total > 0]

    df = df[(df["adr"] >= 0) & (df["adr"] < 1000)]

    df["children"] = df["children"].fillna(0)
    df["city"] = df["city"].fillna("Unknown")
    df["agent"] = df["agent"].fillna(0)
    df["company"] = df["company"].fillna(0)

    df["meal"] = df["meal"].replace("Undefined", "No Meal")

    df["total_nights"] = df["stays_in_weekend_nights"] + df["stays_in_weekdays_nights"]

    return df.reset_index(drop=True)


def overview_kpis(df: pd.DataFrame) -> dict:
    city = df[df["hotel"] == "City Hotel"]
    resort = df[df["hotel"] == "Resort Hotel"]

    monthly = df["arrival_date_month"].value_counts().reindex(MONTH_ORDER)
    peak_month = monthly.idxmax()
    quiet_month = monthly.idxmin()

    return {
        "total_bookings": len(df),
        "city_bookings": len(city),
        "resort_bookings": len(resort),
        "cancel_rate": df["is_canceled"].mean() * 100,
        "city_cancel_rate": city["is_canceled"].mean() * 100,
        "resort_cancel_rate": resort["is_canceled"].mean() * 100,
        "avg_adr": df["adr"].mean(),
        "median_adr": df["adr"].median(),
        "repeat_guest_pct": df["is_repeated_guest"].mean() * 100,
        "avg_lead_time": df["lead_time"].mean(),
        "peak_month": peak_month,
        "quiet_month": quiet_month,
        "city_pct": len(city) / len(df) * 100,
        "resort_pct": len(resort) / len(df) * 100,
    }


def monthly_bookings(df: pd.DataFrame) -> pd.Series:
    return df["arrival_date_month"].value_counts().reindex(MONTH_ORDER).fillna(0)


def monthly_bookings_by_hotel(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby(["arrival_date_month", "hotel"]).size().unstack(fill_value=0)
    return grouped.reindex(MONTH_ORDER)


def cancel_rate_by_leadtime(df: pd.DataFrame) -> pd.Series:
    bins = [-1, 30, 100, 100000]
    labels = ["0 to 30 days", "31 to 100 days", "100+ days"]
    bucket = pd.cut(df["lead_time"], bins=bins, labels=labels)
    return df.groupby(bucket, observed=True)["is_canceled"].mean() * 100


def cancel_rate_by_stay_length(df: pd.DataFrame) -> pd.Series:
    bins = [-1, 2, 5, 10, 100000]
    labels = ["1 to 2 nights", "3 to 5 nights", "6 to 10 nights", "11+ nights"]
    bucket = pd.cut(df["total_nights"], bins=bins, labels=labels)
    return df.groupby(bucket, observed=True)["is_canceled"].mean() * 100


def market_segment_breakdown(df: pd.DataFrame) -> pd.Series:
    return (df["market_segment"].value_counts(normalize=True) * 100).round(1)


def special_requests_breakdown(df: pd.DataFrame) -> pd.Series:
    bucket = df["total_of_special_requests"].clip(upper=2).map(
        {0: "0 requests", 1: "1 request", 2: "2 or more"}
    )
    return (bucket.value_counts(normalize=True) * 100).round(1)


def guest_composition(df: pd.DataFrame) -> dict:
    return {
        "avg_adults": df["adults"].mean(),
        "pct_with_children": (df["children"] > 0).mean() * 100,
        "pct_with_babies": (df["babies"] > 0).mean() * 100,
        "repeat_guest_pct": df["is_repeated_guest"].mean() * 100,
        "avg_previous_cancellations": df["previous_cancellations"].mean(),
        "avg_special_requests": df["total_of_special_requests"].mean(),
    }


def deposit_type_breakdown(df: pd.DataFrame) -> pd.Series:
    return (df["deposit_type"].value_counts(normalize=True) * 100).round(1)


def meal_breakdown(df: pd.DataFrame) -> pd.Series:
    return (df["meal"].value_counts(normalize=True) * 100).round(1)


def customer_type_breakdown(df: pd.DataFrame) -> pd.Series:
    return (df["customer_type"].value_counts(normalize=True) * 100).round(1)


def cancel_rate_by_market_segment(df: pd.DataFrame) -> pd.Series:
    result = (df.groupby("market_segment", observed=True)["is_canceled"].mean() * 100).round(1)
    counts = df["market_segment"].value_counts()
    result = result[counts[counts >= 100].index]
    return result.sort_values(ascending=False)


def cancel_rate_by_deposit_type(df: pd.DataFrame) -> pd.Series:
    return (df.groupby("deposit_type", observed=True)["is_canceled"].mean() * 100).round(1)


def top_cities(df: pd.DataFrame, n: int = 5) -> pd.Series:
    counts = df["city"].value_counts()
    counts = counts[counts.index != "Unknown"]
    return (counts.head(n) / len(df) * 100).round(1)


def weekend_vs_weekday_nights(df: pd.DataFrame) -> pd.Series:
    weekend_only = ((df["stays_in_weekend_nights"] > 0) & (df["stays_in_weekdays_nights"] == 0)).sum()
    weekday_only = ((df["stays_in_weekdays_nights"] > 0) & (df["stays_in_weekend_nights"] == 0)).sum()
    both = ((df["stays_in_weekend_nights"] > 0) & (df["stays_in_weekdays_nights"] > 0)).sum()
    total = len(df)
    return pd.Series({
        "Weekday nights only": round(weekday_only / total * 100, 1),
        "Weekend nights only": round(weekend_only / total * 100, 1),
        "Both": round(both / total * 100, 1),
    })
