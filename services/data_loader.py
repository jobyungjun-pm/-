from __future__ import annotations
import pandas as pd
import streamlit as st

@st.cache_data
def load_population_data(file_path: str) -> pd.DataFrame:
    """CSV 데이터를 로드하고 필수 컬럼 및 타입을 검증합니다."""
    df = pd.read_csv(file_path)
    
    # 1. 필수 컬럼 체크
    required_cols = ["도시", "연도", "인구수"]
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"누락된 컬럼: {set(required_cols) - set(df.columns)}")
    
    # 2. 타입 변환 및 전처리
    df["연도"] = pd.to_numeric(df["연도"])
    df["인구수"] = pd.to_numeric(df["인구수"])
    
    # 3. 데이터 복사본 반환 (원본 보호)
    return df.copy()