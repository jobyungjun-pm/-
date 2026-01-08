import pytest
import pandas as pd
from services.data_loader import load_population_data

def test_data_columns():
    df = load_population_data("data/population.csv")
    assert "도시" in df.columns
    assert "연도" in df.columns
    assert "인구수" in df.columns

def test_data_types():
    df = load_population_data("data/population.csv")
    assert pd.api.types.is_integer_dtype(df["연도"])
    assert pd.api.types.is_numeric_dtype(df["인구수"])