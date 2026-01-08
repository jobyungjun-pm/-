from __future__ import annotations
import streamlit as st
import pandas as pd
from .state import DashboardFilters

def build_sidebar_widgets(df: pd.DataFrame) -> DashboardFilters:
    """사이드바 위젯을 생성하고 상태를 반환합니다."""
    st.sidebar.header("🔎 필터")
    
    years = sorted(df["연도"].unique())
    cities = sorted(df["도시"].unique())
    
    selected_year = st.sidebar.selectbox("연도 선택", years)
    selected_cities = st.sidebar.multiselect("도시 선택", cities, default=[])
    warn_threshold = st.sidebar.number_input("경고 기준 인구수(만 명)", value=500)
    
    return DashboardFilters(
        selected_year=selected_year,
        selected_cities=selected_cities,
        warn_threshold=warn_threshold
    )