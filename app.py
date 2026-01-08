from __future__ import annotations
import streamlit as st
from services.data_loader import load_population_data
from dashboard.layout import setup_page, create_tabs
from dashboard.widgets import build_sidebar_widgets
from dashboard.views import render_data_tab, render_chart_tab, render_monitor_tab

# 1. 초기 설정
st.set_page_config(page_title="도시 인구 대시보드", layout="wide", page_icon="🏙️")

def main() -> None:
    # 2. 레이아웃 배치
    setup_page()
    
    # 3. 데이터 로드
    df = load_population_data("data/population.csv")
    
    # 4. 사이드바 및 상태 관리
    state = build_sidebar_widgets(df)
    
    # 5. 필터링 로직 (Controller 역할)
    filtered = df[
        (df["연도"] == state.selected_year) & 
        (df["도시"].isin(state.selected_cities))
    ].copy()
    
    st.caption(f"현재 선택: 연도={state.selected_year}, 도시={len(state.selected_cities)}개")
    
    # 6. 탭 생성 및 렌더링
    tab_data, tab_chart, tab_monitor = create_tabs()
    
    render_data_tab(tab_data, df, filtered)
    render_chart_tab(tab_chart, filtered)
    render_monitor_tab(tab_monitor, filtered, state)

if __name__ == "__main__":
    main()