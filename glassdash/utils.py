"""Utility functions for working with Polars DataFrames."""

from datetime import datetime

import polars as pl


def get_last_n_months(n: int = 12) -> pl.DataFrame:
    today = datetime.now()
    months = []
    for i in range(n - 1, -1, -1):
        d = datetime(today.year, today.month, 1)
        if i > 0:
            year = today.year
            month = today.month - i
            while month <= 0:
                month += 12
                year -= 1
            d = datetime(year, month, 1)
        months.append(d.strftime("%Y-%m"))
    return pl.DataFrame({"month": months})


def ensure_month_column(df: pl.DataFrame, col: str = "month") -> pl.DataFrame:
    if col not in df.columns:
        raise ValueError(f"DataFrame must contain '{col}' column")
    return df.with_columns(pl.col(col).cast(pl.Utf8))


def filter_to_current_month(df: pl.DataFrame, month_col: str = "month"):
    today = datetime.now()
    current = today.strftime("%Y-%m")
    mask = df[month_col] == current
    current_idx = df.filter(mask).height - 1 if mask.any() else -1
    return df, current_idx
